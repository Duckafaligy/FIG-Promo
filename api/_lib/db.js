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
  const [diners, waiting, restaurants, live, reports, keys, recentR, recentRep, leads] = await Promise.all([
    safe(count("profiles?role=eq.diner"), null),
    safe(count("profiles?role=eq.diner&early_access=is.false"), null),
    safe(count("restaurants"), null),
    safe(count("restaurants?status=eq.approved"), null),
    safe(count("reports?status=eq.open"), null),
    safe(rest("access_keys?select=code,note,max_uses,uses,made_at&order=made_at.desc&limit=200"), { rows: [] }),
    safe(rest("restaurants?select=id,name,cuisine,city,status,created_at&order=created_at.desc&limit=100"), { rows: [] }),
    safe(rest("reports?select=id,reason,details,at,status&order=at.desc&limit=100"), { rows: [] }),
    safe(rest("waitlist?select=created_at,role,email,phone,restaurant,area,source&order=created_at.desc&limit=500"), { rows: [] }),
  ]);
  return {
    counts: { diners, waiting, restaurants, live, reports, keys: keys.rows.length },
    keys: keys.rows, restaurants: recentR.rows, reports: recentRep.rows,
    leads: leads.rows.filter((l) => l.role === "restaurant"), waitlist: leads.rows.filter((l) => l.role === "diner").length,
  };
}

// FIG-XXXXX-XXXXX from letters and digits that can't be misread (same alphabet as the app's make_access_keys)
const ABC = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function newCode() {
  const b = crypto.randomBytes(10);
  let c = "FIG-";
  for (let j = 0; j < 10; j++) c += ABC[b[j] % 32] + (j === 4 ? "-" : "");
  return c;
}
async function makeKeys(n, uses, note) {
  n = Math.max(1, Math.min(100, n | 0)); uses = Math.max(1, Math.min(10000, uses | 0));
  const rows = Array.from({ length: n }, () => ({ code: newCode(), note: String(note || "").trim().slice(0, 80), max_uses: uses }));
  await rest("access_keys", { method: "POST", body: JSON.stringify(rows), headers: { Prefer: "return=minimal" } });
  return rows.map((r) => r.code);
}
async function deleteKey(code) {
  if (!/^[A-Z0-9-]{4,20}$/.test(code)) throw new Error("bad key");
  await rest(`access_keys?code=eq.${encodeURIComponent(code)}`, { method: "DELETE", headers: { Prefer: "return=minimal" } });
}

module.exports = { connected, overview, makeKeys, deleteKey };
