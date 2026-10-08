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
  const [diners, restaurants, live, reports, recentR, premiumRows, recentRep, leads] = await Promise.all([
    safe(count("profiles?role=eq.diner"), null),
    safe(count("restaurants"), null),
    safe(count("restaurants?status=eq.approved"), null),
    safe(count("reports?status=eq.open"), null),
    safe(rest("restaurants?select=id,owner_id,name,cuisine,city,status,created_at&order=created_at.desc&limit=100"), { rows: [] }),
    safe(rest("billing_accounts?select=owner_id,premium_until,premium_source&premium_until=not.is.null"), { rows: [] }),
    safe(rest("reports?select=id,reason,details,at,status&order=at.desc&limit=100"), { rows: [] }),
    safe(rest("waitlist?select=created_at,role,email,phone,restaurant,area,source&order=created_at.desc&limit=500"), { rows: [] }),
  ]);
  return {
    counts: { diners, restaurants, live, reports },
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
async function makeInvoices(month) {
  if (!/^\d{4}-\d{2}-01$/.test(String(month))) throw new Error("bad month");
  await rest("rpc/make_ad_invoices", { method: "POST", body: JSON.stringify({ p_month: month }) });
}
async function setInvoice(id, status) {
  if (!["sent", "paid", "void", "open"].includes(status)) throw new Error("bad status");
  const stamp = status === "sent" ? { sent_at: new Date().toISOString() } : status === "paid" ? { paid_at: new Date().toISOString() } : {};
  await rest(`ad_invoices?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify({ status, ...stamp }), headers: { Prefer: "return=minimal" } });
}

module.exports = { connected, overview, setCampaign, setAccount, setPremium, makeInvoices, setInvoice };
