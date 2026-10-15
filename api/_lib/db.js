// Reads FIG's database for the admin page, on the server only. Needs (Vercel environment variables, never in the page):
//   SUPABASE_URL                https://<project>.supabase.co
//   SUPABASE_SERVICE_ROLE_KEY   the service_role key (Supabase → Project Settings → API). It bypasses row security,
//                               so it must only ever live here.
const url = () => (process.env.SUPABASE_URL || "").replace(/\/$/, "");
const key = () => process.env.SUPABASE_SERVICE_ROLE_KEY || "";
const connected = () => !!(url() && key());

async function rest(path, opts = {}) {
  const r = await fetch(`${url()}/rest/v1/${path}`, {
    ...opts,
    headers: { apikey: key(), Authorization: `Bearer ${key()}`, "Content-Type": "application/json", Prefer: "count=exact", ...(opts.headers || {}) },
  });
  if (!r.ok) throw new Error(`${r.status} ${path.split("?")[0]}`);
  const range = r.headers.get("content-range") || "";
  const count = Number(range.split("/")[1]) || 0;
  const text = await r.text();
  return { rows: text ? JSON.parse(text) : [], count };
}
const count = async (path) => (await rest(path + (path.includes("?") ? "&" : "?") + "select=id&limit=1")).count;
const safe = (p, fallback) => p.catch(() => fallback);

async function overview() {
  const since = new Date(Date.now() - 30 * 86400000).toISOString();
  const [diners, restaurants, live, reports, recentR, premiumRows, recentRep, leads, support, owners, changes, orders30, ordersOpen] = await Promise.all([
    safe(count("profiles?role=eq.diner"), null),
    safe(count("restaurants"), null),
    safe(count("restaurants?status=eq.approved"), null),
    safe(count("reports?status=eq.open"), null),
    safe(rest("restaurants?select=id,owner_id,name,cuisine,city,status,created_at&order=created_at.desc&limit=100"), { rows: [] }),
    safe(rest("billing_accounts?select=owner_id,premium_until,premium_source,comped,payments_demo,stripe_ready,stripe_payouts"), { rows: [] }),
    safe(rest("reports?select=id,reason,details,at,status&order=at.desc&limit=100"), { rows: [] }),
    safe(rest("waitlist?select=created_at,role,email,phone,restaurant,area,source&order=created_at.desc&limit=500"), { rows: [] }),
    // what people wrote through "Message us" in the app and on the website (user 2026-10-11: nobody could read these)
    safe(rest("support_messages?select=id,email,topic,body,at,status&order=at.desc&limit=200"), { rows: [] }),
    safe(rest("profiles?select=id,email,name&role=eq.business&limit=500"), { rows: [] }),
    // who a restaurant is changed (name, address) or handed to (the hand-over feature's record)
    safe(rest("restaurant_changes?select=id,restaurant_id,kind,before,after,at&order=at.desc&limit=40"), { rows: [] }),
    safe(count(`orders?placed_at=gte.${since}`), null),
    safe(count("orders?status=in.(unpaid,sent,accepted,ready)"), null),
  ]);
  return {
    counts: { diners, restaurants, live, reports, orders30, ordersOpen, support: support.rows.filter((m) => m.status === "open").length },
    support: support.rows, owners: owners.rows, changes: changes.rows,
    ads: await safe(ads(), { campaigns: [], accounts: [], invoices: [] }), restaurants: recentR.rows, premium: premiumRows.rows, reports: recentRep.rows,
    leads: leads.rows.filter((l) => l.role === "restaurant"), waitlist: leads.rows.filter((l) => l.role === "diner").length,
  };
}

// ads (FIG's only income: restaurants pay per tap, the team invoices monthly): every campaign with its results, every
// ad account with this month's spend, and the invoices
async function ads() {
  const [campaigns, accounts, invoices] = await Promise.all([
    rest("rpc/admin_campaigns", { method: "POST", body: "{}" }),
    rest("rpc/admin_ad_accounts", { method: "POST", body: "{}" }),
    rest("ad_invoices?select=id,owner_id,month,amount,status,sent_at,paid_at&order=month.desc&limit=300"),
  ]);
  const names = new Map(accounts.rows.map((a) => [a.owner_id, a]));
  return { campaigns: campaigns.rows, accounts: accounts.rows, invoices: invoices.rows.map((x) => ({ ...x, owner: names.get(x.owner_id) || {} })) };
}
const uuid = (id) => { if (!/^[0-9a-f-]{36}$/i.test(String(id))) throw new Error("bad id"); return id; };
// stop an ad (with a note the owner sees) or let it run again
async function setCampaign(id, stop, note) {
  await rest(`campaigns?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify(stop ? { status: "stopped", note: String(note || "").slice(0, 300) || null } : { status: "active", note: null }), headers: { Prefer: "return=minimal" } });
}
// an owner's monthly limit, or a hold on every ad (an unpaid invoice)
async function setAccount(owner, limit, held) {
  const change = {};
  if (limit != null) { const n = Number(limit); if (!(n >= 0 && n <= 100000)) throw new Error("bad limit"); change.monthly_limit = n; }
  if (held != null) change.status = held ? "held" : "active";
  await rest(`ad_accounts?owner_id=eq.${uuid(owner)}`, { method: "PATCH", body: JSON.stringify(change), headers: { Prefer: "return=minimal" } });
}
// FIG Premium ($50 a year) switched on by the team for some years from now, or off (0)
async function setPremium(owner, years) {
  const y = Number(years);
  if (!(y >= 0 && y <= 5)) throw new Error("bad years");
  await rest("rpc/set_premium", { method: "POST", body: JSON.stringify({ p_owner: uuid(owner), p_until: y ? new Date(Date.now() + y * 365 * 86400000).toISOString() : null, p_source: "fig" }) });
}
// a message from the inbox: answered, or open again
async function setSupport(id, status) {
  if (!["open", "answered"].includes(status)) throw new Error("bad status");
  await rest(`support_messages?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify({ status }), headers: { Prefer: "return=minimal" } });
}
// Someone lost the phone with their authenticator app and wrote to FIG (check it's really them first: they write from the
// account's email and know the phone number on it). Removes their authenticators, so they sign in with the password alone
// and can switch two-step login on again. By account id, or by email (looked up in profiles).
async function twoStepOff({ id, email }) {
  let uid = id ? uuid(id) : null;
  if (!uid) {
    const e = String(email || "").trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+$/.test(e)) throw new Error("bad email");
    uid = (await rest(`profiles?select=id&email=eq.${encodeURIComponent(e)}&limit=1`)).rows[0]?.id;
    if (!uid) return { found: false, removed: 0 };
  }
  const auth = (method, path) => fetch(`${url()}/auth/v1/admin/users/${uid}/${path}`, { method, headers: { apikey: key(), Authorization: `Bearer ${key()}` } });
  const list = await auth("GET", "factors");
  if (!list.ok) throw new Error("factors " + list.status);
  const body = await list.json();
  const factors = Array.isArray(body) ? body : body.factors || [];
  for (const f of factors) { const d = await auth("DELETE", `factors/${uuid(f.id)}`); if (!d.ok) throw new Error("factor " + d.status); }
  console.log("admin: two-step login turned off for", uid, "authenticators:", factors.length); // the id only, never the email
  return { found: true, removed: factors.length };
}
async function makeInvoices(month) {
  if (!/^\d{4}-\d{2}-01$/.test(String(month))) throw new Error("bad month");
  await rest("rpc/make_ad_invoices", { method: "POST", body: JSON.stringify({ p_month: month }) });
}
async function setInvoice(id, status) {
  if (!["sent", "paid", "void", "open"].includes(status)) throw new Error("bad status");
  const stamp = status === "sent" ? { sent_at: new Date().toISOString() } : status === "paid" ? { paid_at: new Date().toISOString() } : {};
  await rest(`ad_invoices?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify({ status, ...stamp }), headers: { Prefer: "return=minimal" } });
}


// the blog's controls (table blog_overrides): a post taken down, or its go-live time moved. The blog is generated from the site's code;
// these only say what to leave out or when to publish, so nothing here can change a post's words.
const SLUG = /^[a-z0-9-]{1,100}$/;
async function blogOverrides() { return (await rest("blog_overrides?select=slug,hidden,publish_at,note,updated_at&order=slug")).rows; }
async function setBlog(slug, change) {
  if (!SLUG.test(String(slug))) throw new Error("bad slug");
  const cur = (await rest(`blog_overrides?select=slug,hidden,publish_at,note&slug=eq.${slug}`)).rows[0] || { hidden: false, publish_at: null, note: null };
  const next = { hidden: cur.hidden, publish_at: cur.publish_at, note: cur.note };
  if ("hidden" in change) next.hidden = !!change.hidden;
  if ("publish_at" in change) {
    if (change.publish_at === null) next.publish_at = null;
    else { const t = Date.parse(change.publish_at); if (!(t > Date.now() - 86400000 && t < Date.now() + 366 * 86400000)) throw new Error("bad time"); next.publish_at = new Date(t).toISOString(); }
  }
  if ("note" in change) next.note = change.note ? String(change.note).slice(0, 300) : null;
  if (!next.hidden && !next.publish_at) { await rest(`blog_overrides?slug=eq.${slug}`, { method: "DELETE", headers: { Prefer: "return=minimal" } }); return { cleared: true }; }
  await rest("blog_overrides?on_conflict=slug", { method: "POST", body: JSON.stringify({ slug, ...next }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  return { saved: true };
}

module.exports = { connected, overview, setCampaign, setAccount, setPremium, setSupport, twoStepOff, makeInvoices, setInvoice, blogOverrides, setBlog };
