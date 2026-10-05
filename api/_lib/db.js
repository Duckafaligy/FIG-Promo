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
// plan codes: one-time PLAN-XXXXX-XXXXX codes; each turns one restaurant owner's plan on free for a year (in the app)
async function makePlanCodes(n, note) {
  n = Math.max(1, Math.min(50, n | 0));
  const rows = Array.from({ length: n }, () => ({ code: newCode("PLAN-"), note: String(note || "").trim().slice(0, 80), max_uses: 1, days: 365 }));
  await rest("plan_codes", { method: "POST", body: JSON.stringify(rows), headers: { Prefer: "return=minimal" } });
  return rows.map((r) => r.code);
}
async function deletePlanCode(code) {
  if (!/^[A-Z0-9-]{4,24}$/.test(code)) throw new Error("bad code");
  await rest(`plan_codes?code=eq.${encodeURIComponent(code)}`, { method: "DELETE", headers: { Prefer: "return=minimal" } });
}

module.exports = { connected, overview, makePlanCodes, deletePlanCode };
