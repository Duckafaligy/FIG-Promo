// FIG admin: password check, lockout and sessions. Everything secret lives in Vercel environment variables:
//   ADMIN_PASSWORD_HASH  "scrypt:<salt hex>:<hash hex>" (never the password itself)
//   SESSION_SECRET       random string used to sign the session cookie
// Lockout works like an iPhone passcode: 5 wrong tries, then 1 min, then 5, 15 and 60 minutes after each further miss.
// ponytail: tries are counted per IP in this server's memory plus a signed cookie. A cold start forgets the memory part;
// for a lock that survives everything, keep the count in a database (Supabase or Upstash) instead.
const crypto = require("crypto");

const FREE_TRIES = 5;
const LOCKS_MIN = [1, 5, 15, 60]; // minutes, after try 5, 6, 7, 8+
const SESSION_HOURS = 8;
const tries = new Map(); // ip -> { fails, until }

const ip = (req) => String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "?").split(",")[0].trim();
const secret = () => process.env.SESSION_SECRET || "";

function sign(value) {
  return crypto.createHmac("sha256", secret()).update(value).digest("base64url");
}
function seal(obj) {
  const body = Buffer.from(JSON.stringify(obj)).toString("base64url");
  return body + "." + sign(body);
}
function open(token) {
  if (!token || !secret()) return null;
  const [body, mac] = String(token).split(".");
  if (!body || !mac) return null;
  const want = Buffer.from(sign(body)), got = Buffer.from(mac);
  if (want.length !== got.length || !crypto.timingSafeEqual(want, got)) return null;
  try { return JSON.parse(Buffer.from(body, "base64url").toString()); } catch { return null; }
}
function cookies(req) {
  const out = {};
  String(req.headers.cookie || "").split(";").forEach((c) => { const i = c.indexOf("="); if (i > 0) out[c.slice(0, i).trim()] = decodeURIComponent(c.slice(i + 1).trim()); });
  return out;
}
const cookie = (name, value, maxAge) =>
  `${name}=${encodeURIComponent(value)}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAge}`;

function passwordOk(password) {
  const stored = process.env.ADMIN_PASSWORD_HASH || "";
  const [kind, saltHex, hashHex] = stored.split(":");
  if (kind !== "scrypt" || !saltHex || !hashHex) return false;
  const want = Buffer.from(hashHex, "hex");
  const got = crypto.scryptSync(String(password || ""), Buffer.from(saltHex, "hex"), want.length);
  return crypto.timingSafeEqual(want, got);
}

/** The lock state for this visitor: from memory, and from their signed cookie (whichever is stricter). */
function lockState(req) {
  const mem = tries.get(ip(req)) || { fails: 0, until: 0 };
  const c = open(cookies(req).fig_admin_tries) || { fails: 0, until: 0 };
  return { fails: Math.max(mem.fails, c.fails || 0), until: Math.max(mem.until, c.until || 0) };
}
function lockFor(fails) {
  if (fails < FREE_TRIES) return 0;
  return LOCKS_MIN[Math.min(fails - FREE_TRIES, LOCKS_MIN.length - 1)] * 60_000;
}

/** Handles a sign-in attempt. Returns { status, body, headers }. */
function login(req, password) {
  const now = Date.now();
  const st = lockState(req);
  if (st.until > now) return { status: 429, body: { locked: true, retryIn: Math.ceil((st.until - now) / 1000) } };
  if (!secret() || !process.env.ADMIN_PASSWORD_HASH) return { status: 503, body: { error: "Admin isn't set up on the server yet." } };
  if (passwordOk(password)) {
    tries.delete(ip(req));
    return { status: 200, body: { ok: true }, headers: [
      cookie("fig_admin", seal({ exp: now + SESSION_HOURS * 3_600_000 }), SESSION_HOURS * 3600),
      cookie("fig_admin_tries", "", 0),
    ] };
  }
  const fails = st.fails + 1;
  const until = now + lockFor(fails);
  tries.set(ip(req), { fails, until });
  const left = Math.max(0, FREE_TRIES - fails);
  return {
    status: 401,
    body: until > now ? { locked: true, retryIn: Math.ceil((until - now) / 1000) } : { error: "Wrong password.", triesLeft: left },
    headers: [cookie("fig_admin_tries", seal({ fails, until }), 24 * 3600)],
  };
}

const signedIn = (req) => { const s = open(cookies(req).fig_admin); return !!s && s.exp > Date.now(); };
const logoutCookie = () => cookie("fig_admin", "", 0);

function send(res, status, body, headers = []) {
  res.statusCode = status;
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex, nofollow");
  if (headers.length) res.setHeader("Set-Cookie", headers);
  if (typeof body === "string") { res.setHeader("Content-Type", "text/html; charset=utf-8"); res.end(body); }
  else { res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(body)); }
}

async function readJson(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = [];
  for await (const c of req) { chunks.push(c); if (chunks.reduce((n, x) => n + x.length, 0) > 10_000) break; }
  try { return JSON.parse(Buffer.concat(chunks).toString() || "{}"); } catch { return {}; }
}

/** Same-site check for POSTs (the cookie is SameSite=Strict too). */
function sameOrigin(req) {
  const o = req.headers.origin;
  return !o || o === `https://${req.headers.host}`;
}

module.exports = { login, signedIn, logoutCookie, send, readJson, sameOrigin, _test: { seal, open, lockFor, passwordOk } };
