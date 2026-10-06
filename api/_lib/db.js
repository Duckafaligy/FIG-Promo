// Reads FIG's database for the admin page, on the server only. Needs (Vercel environment variables, never in the page):
//   SUPABASE_URL                https://<project>.supabase.co
//   SUPABASE_SERVICE_ROLE_KEY   the service_role key (Supabase → Project Settings → API). It bypasses row security,
//                               so it must only ever live here.
const crypto = require("crypto");

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
  const [diners, restaurants, live, reports, recentR, recentRep, leads, plans, planUsed] = await Promise.all([
    safe(count("profiles?role=eq.diner"), null),
    safe(count("restaurants"), null),
    safe(count("restaurants?status=eq.approved"), null),
    safe(count("reports?status=eq.open"), null),
    safe(rest("restaurants?select=id,name,cuisine,city,status,created_at&order=created_at.desc&limit=100"), { rows: [] }),
    safe(rest("reports?select=id,reason,details,at,status&order=at.desc&limit=100"), { rows: [] }),
    safe(rest("waitlist?select=created_at,role,email,phone,restaurant,area,source&order=created_at.desc&limit=500"), { rows: [] }),
    safe(rest("plan_codes?select=code,note,days,max_uses,uses,made_at&order=made_at.desc&limit=200"), { rows: [] }),
    safe(rest("billing_accounts?select=owner_id,plan_code&plan_code=not.is.null"), { rows: [] }),
  ]);
  // which restaurants each plan code turned on
  const owners = [...new Set(planUsed.rows.map((b) => b.owner_id))];
  const names = owners.length ? (await safe(rest(`restaurants?select=owner_id,name&owner_id=in.(${owners.join(",")})`), { rows: [] })).rows : [];
  const planCodes = plans.rows.map((k) => ({ ...k, used_by: planUsed.rows.filter((b) => b.plan_code === k.code).flatMap((b) => names.filter((n) => n.owner_id === b.owner_id).map((n) => n.name)) }));
  return {
    counts: { diners, restaurants, live, reports },
    disputes: await safe(disputes(), []),
    planCodes, restaurants: recentR.rows, reports: recentRep.rows,
    leads: leads.rows.filter((l) => l.role === "restaurant"), waitlist: leads.rows.filter((l) => l.role === "diner").length,
  };
}

// codes from letters and digits that can't be misread (no 0/O or 1/I)
const ABC = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function newCode(prefix) {
  const b = crypto.randomBytes(10);
  let c = prefix;
  for (let j = 0; j < 10; j++) c += ABC[b[j] % 32] + (j === 4 ? "-" : "");
  return c;
}
// free codes: one-time FIG-XXXXX-XXXXX codes; each turns one restaurant owner's plan on free for a year (in the app)
// a custom code (like GOLDENLANTERN) is one code, still one-time; "409" when it's taken (any case or dashes)
async function makePlanCodes(n, note, custom) {
  n = Math.max(1, Math.min(50, n | 0));
  custom = String(custom || "").trim().toUpperCase();
  if (custom && !/^[A-Z0-9][A-Z0-9-]{3,23}$/.test(custom)) throw new Error("400 bad custom code");
  const codes = custom ? [custom] : Array.from({ length: n }, () => newCode("FIG-"));
  const rows = codes.map((code) => ({ code, note: String(note || "").trim().slice(0, 80), max_uses: 1, days: 365 }));
  await rest("plan_codes", { method: "POST", body: JSON.stringify(rows), headers: { Prefer: "return=minimal" } });
  return rows.map((r) => r.code);
}
async function deletePlanCode(code) {
  if (!/^[A-Z0-9-]{4,24}$/.test(code)) throw new Error("bad code");
  // a used code stays on the list as a record (uses=0 in the filter: nothing happens to it)
  await rest(`plan_codes?code=eq.${encodeURIComponent(code)}&uses=eq.0`, { method: "DELETE", headers: { Prefer: "return=minimal" } });
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
  return d.map((x) => {
    const mine = dinerOrders.rows.filter((o) => o.user_id === x.user_id);
    const theirs = restOrders.rows.filter((o) => o.restaurant_id === x.restaurant_id);
    const past = d.filter((y) => y.user_id === x.user_id && y.id !== x.id);
    const p = people.rows.find((y) => y.id === x.user_id) || {};
    const r = rests.rows.find((y) => y.id === x.restaurant_id) || {};
    return {
      ...x,
      order: orders.rows.find((o) => o.id === x.order_id) || {},
      diner: { ...p, orders: mine.length, picked: n(mine, (o) => o.status === "picked"), noshows: n(mine, (o) => o.status === "noshow"), checkins: n(mine, (o) => o.arrived_at),
        disputes: past.length, upheld: n(past, (y) => y.status === "upheld") },
      restaurant: { ...r, orders: theirs.length, picked: n(theirs, (o) => o.status === "picked"), noshows: n(theirs, (o) => o.status === "noshow") },
    };
  });
}
// the FIG team's call: upheld = the diner was right (their strike comes off, the restaurant gets a false-report strike)
async function decideDispute(id, upheld, note) {
  if (!/^[0-9a-f-]{36}$/i.test(String(id))) throw new Error("bad id");
  await rest("rpc/decide_dispute", { method: "POST", body: JSON.stringify({ p_dispute: id, p_upheld: !!upheld, p_note: String(note || "").slice(0, 300) }), headers: { Prefer: "return=minimal" } });
}

module.exports = { connected, overview, disputes, decideDispute, makePlanCodes, deletePlanCode };
