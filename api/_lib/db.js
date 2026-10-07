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
    boosts: await safe(boosts(), []), restaurants: recentR.rows, reports: recentRep.rows,
    leads: leads.rows.filter((l) => l.role === "restaurant"), waitlist: leads.rows.filter((l) => l.role === "diner").length,
  };
}

// boosts (FIG's only income): every request, live and past week, with its restaurant, the owner's email (to settle the
// price), the deal it boosts, and its results; customers = diners scanned in during the week
async function boosts() {
  const b = (await rest("promotions?select=id,restaurant_id,placement,kind,deal_id,status,cost,start_at,end_at,requested_at,note,views,taps&status=neq.cancelled&order=start_at.desc&limit=200")).rows;
  if (!b.length) return [];
  const ids = (xs) => [...new Set(xs.filter(Boolean))].join(",");
  const [rests, deals] = await Promise.all([
    rest(`restaurants?id=in.(${ids(b.map((x) => x.restaurant_id))})&select=id,name,city,owner_id`),
    b.some((x) => x.deal_id) ? rest(`deals?id=in.(${ids(b.map((x) => x.deal_id))})&select=id,title`) : { rows: [] },
  ]);
  const owners = ids(rests.rows.map((r) => r.owner_id));
  const people = owners ? (await rest(`profiles?id=in.(${owners})&select=id,name,email,phone`)).rows : [];
  return Promise.all(b.map(async (x) => {
    const r = rests.rows.find((y) => y.id === x.restaurant_id) || {};
    const started = Date.parse(x.start_at) <= Date.now() && x.status !== "requested" && x.status !== "declined";
    const scans = started ? (await safe(rest(`redemptions?restaurant_id=eq.${x.restaurant_id}&at=gte.${encodeURIComponent(x.start_at)}&at=lt.${encodeURIComponent(x.end_at)}&select=user_id&limit=5000`), { rows: [] })).rows : [];
    return {
      ...x, restaurant: r.name, city: r.city, owner: people.find((p) => p.id === r.owner_id) || {},
      deal: (deals.rows.find((d) => d.id === x.deal_id) || {}).title, customers: new Set(scans.map((s) => s.user_id)).size,
    };
  }));
}
// the team's call on a request: live (it runs that week) or declined with a note; the owner gets a notice either way
async function decideBoost(id, live, note) {
  if (!/^[0-9a-f-]{36}$/i.test(String(id))) throw new Error("bad id");
  await rest("rpc/decide_boost", { method: "POST", body: JSON.stringify({ p_id: id, p_live: !!live, p_note: String(note || "").slice(0, 300) }), headers: { Prefer: "return=minimal" } });
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

module.exports = { connected, overview, disputes, decideDispute, liftTakeout, decideBoost };
