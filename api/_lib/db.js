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
  const [diners, restaurants, live, reports, recentR, recentRep, leads] = await Promise.all([
    safe(count("profiles?role=eq.diner"), null),
    safe(count("restaurants"), null),
    safe(count("restaurants?status=eq.approved"), null),
    safe(count("reports?status=eq.open"), null),
    safe(rest("restaurants?select=id,name,cuisine,city,status,created_at&order=created_at.desc&limit=100"), { rows: [] }),
    safe(rest("reports?select=id,reason,details,at,status&order=at.desc&limit=100"), { rows: [] }),
    safe(rest("waitlist?select=created_at,role,email,phone,restaurant,area,source&order=created_at.desc&limit=500"), { rows: [] }),
  ]);
  return {
    counts: { diners, restaurants, live, reports },
    disputes: await safe(disputes(), []),
    suspended: await safe(suspended(), []),
    ads: await safe(ads(), { campaigns: [], accounts: [], invoices: [] }), restaurants: recentR.rows, reports: recentRep.rows,
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
async function makeInvoices(month) {
  if (!/^\d{4}-\d{2}-01$/.test(String(month))) throw new Error("bad month");
  await rest("rpc/make_ad_invoices", { method: "POST", body: JSON.stringify({ p_month: month }) });
}
async function setInvoice(id, status) {
  if (!["sent", "paid", "void", "open"].includes(status)) throw new Error("bad status");
  const stamp = status === "sent" ? { sent_at: new Date().toISOString() } : status === "paid" ? { paid_at: new Date().toISOString() } : {};
  await rest(`ad_invoices?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify({ status, ...stamp }), headers: { Prefer: "return=minimal" } });
}

// contested no-shows, newest first: each with its order's every timestamp, and both accounts' track record
async function disputes() {
  const d = (await rest("disputes?select=id,order_id,user_id,restaurant_id,reason,status,created_at,decided_at,note&order=created_at.desc&limit=100")).rows;
  if (!d.length) return [];
  const ids = (k) => [...new Set(d.map((x) => x[k]))].join(",");
  const [orders, people, rests, dinerOrders, restOrders] = await Promise.all([
    rest(`orders?id=in.(${ids("order_id")})&select=id,number,total,status,placed_at,accepted_at,pickup_at,ready_at,nudged_at,arrived_at,arrived_m,picked_at,noshow_at`),
    rest(`profiles?id=in.(${ids("user_id")})&select=id,name,username,email,strikes,created_at`),
    rest(`restaurants?id=in.(${ids("restaurant_id")})&select=id,name,city,false_noshows`),
    rest(`orders?user_id=in.(${ids("user_id")})&select=user_id,status,arrived_at&limit=5000`),
    rest(`orders?restaurant_id=in.(${ids("restaurant_id")})&select=restaurant_id,status&limit=5000`),
  ]);
  const n = (rows, f) => rows.filter(f).length;
  // where each diner stands: strikes in force, and any takeout suspension (the same rule the app uses)
  const live = {};
  await Promise.all([...new Set(d.map((x) => x.user_id))].map(async (u) => {
    live[u] = await takeoutStatus(u);
  }));
  return d.map((x) => {
    const mine = dinerOrders.rows.filter((o) => o.user_id === x.user_id);
    const theirs = restOrders.rows.filter((o) => o.restaurant_id === x.restaurant_id);
    const past = d.filter((y) => y.user_id === x.user_id && y.id !== x.id);
    const p = people.rows.find((y) => y.id === x.user_id) || {};
    const r = rests.rows.find((y) => y.id === x.restaurant_id) || {};
    return {
      ...x,
      order: orders.rows.find((o) => o.id === x.order_id) || {},
      diner: { ...p, strikes: live[x.user_id]?.strikes ?? p.strikes, suspended_until: live[x.user_id]?.suspended_until, banned: live[x.user_id]?.banned, orders: mine.length, picked: n(mine, (o) => o.status === "picked"), noshows: n(mine, (o) => o.status === "noshow"), checkins: n(mine, (o) => o.arrived_at),
        disputes: past.length, upheld: n(past, (y) => y.status === "upheld") },
      restaurant: { ...r, orders: theirs.length, picked: n(theirs, (o) => o.status === "picked"), noshows: n(theirs, (o) => o.status === "noshow") },
    };
  });
}
const takeoutStatus = (u) => rest("rpc/takeout_status", { method: "POST", body: JSON.stringify({ p_user: u }) }).then((r) => r.rows[0], () => null);
// diners whose takeout is paused or off: anyone with a no-show in the last 2 years, checked one by one (few, at pilot size)
async function suspended() {
  const ns = (await rest("orders?status=eq.noshow&select=user_id&noshow_at=gte." + new Date(Date.now() - 730 * 864e5).toISOString() + "&limit=2000")).rows;
  const ids = [...new Set(ns.map((o) => o.user_id))];
  const out = [];
  for (const u of ids) {
    const s = await takeoutStatus(u);
    if (s && (s.banned || (s.suspended_until && Date.parse(s.suspended_until) > Date.now()))) out.push({ user_id: u, ...s, noshows: ns.filter((o) => o.user_id === u).length });
  }
  if (!out.length) return [];
  const people = (await rest(`profiles?id=in.(${out.map((x) => x.user_id).join(",")})&select=id,name,username,email`)).rows;
  return out.map((x) => ({ ...x, ...(people.find((p) => p.id === x.user_id) || {}) }));
}
async function liftTakeout(id) {
  if (!/^[0-9a-f-]{36}$/i.test(String(id))) throw new Error("bad id");
  await rest("rpc/lift_takeout", { method: "POST", body: JSON.stringify({ p_user: id }), headers: { Prefer: "return=minimal" } });
}
// the FIG team's call: upheld = the diner was right (their strike comes off, the restaurant gets a false-report strike)
async function decideDispute(id, upheld, note) {
  if (!/^[0-9a-f-]{36}$/i.test(String(id))) throw new Error("bad id");
  await rest("rpc/decide_dispute", { method: "POST", body: JSON.stringify({ p_dispute: id, p_upheld: !!upheld, p_note: String(note || "").slice(0, 300) }), headers: { Prefer: "return=minimal" } });
}

module.exports = { connected, overview, disputes, decideDispute, liftTakeout, setCampaign, setAccount, makeInvoices, setInvoice };
