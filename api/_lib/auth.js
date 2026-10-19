// FIG admin: password check, lockout and sessions. Everything secret lives in Vercel environment variables:
//   ADMIN_PASSWORD_HASH  "scrypt:<salt hex>:<hash hex>" (never the password itself)
//   SESSION_SECRET       random string used to sign the session cookie
//   ADMIN_TOTP_SECRET    the authenticator app's secret (base32). Unset = no code step (FIX-LIST #83: the user sets it themselves)
// Lockout works like an iPhone passcode: 5 wrong tries, then 1 min, then 5, 15 and 60 minutes after each further miss.
// Tries are counted per IP in FIG's database (login_attempts, key "admin:<ip>"), so a cold start or a visitor who throws away
// the cookie can't reset the lock (user 2026-10-10: harden). If the database can't be reached, this server's memory and the
// signed cookie still count, so a database outage never locks the admin out.
// On top of that (FIX-LIST #83, user 2026-10-18: "impossible for other people to get in except me; I don't want bots flooding it"):
// - a GLOBAL throttle (key "admin:*"): 20 wrong passwords or codes in an hour, from anywhere, lock sign-in for 5 minutes. A browser
//   that signed in before carries a "known device" cookie (90 days) that skips this one lock only, never the per-IP lock, the
//   password or the code, so a botnet can't lock the owner out with it. Checked before any password work;
// - a session version (settings admin_session_version) sealed into the session and device cookies: "Sign out everywhere" bumps
//   it and every older cookie stops working. If the database can't say, the cookies' own expiry decides, as before;
// - with ADMIN_TOTP_SECRET set, the password only opens a 5-minute code step: a code from the authenticator app (each one works
//   once: settings admin_totp_last_step, or memory when the database is down) or one of 8 one-time backup codes (settings
//   admin_backup_codes, SHA-256 only; they need the database).
const crypto = require("crypto");
const totp = require("./totp");

const FREE_TRIES = 5;
const LOCKS_MIN = [1, 5, 15, 60]; // minutes, after try 5, 6, 7, 8+
const SESSION_HOURS = 8;
const GLOBAL = { key: "*", fails: 20, hourMs: 3_600_000, lockMs: 5 * 60_000 };
const DEVICE_DAYS = 90;
const CODE_MIN = 5; // the time to type the code after the password
const tries = new Map(); // ip (or "*") -> { fails, until | last }: the fallback when the database can't be reached
let lastStepMem = 0; // the last authenticator step used, when the database can't keep it
const DB = () => ({ url: (process.env.SUPABASE_URL || "").replace(/\/$/, ""), key: process.env.SUPABASE_SERVICE_ROLE_KEY || "" });
const H = (key, more) => ({ apikey: key, Authorization: `Bearer ${key}`, ...more });

/** The login_attempts row for "admin:<who>" ({} when there's none), or null when there's no database to ask. */
async function dbRow(who) {
  const { url, key } = DB();
  if (!url || !key) return null;
  try {
    const r = await fetch(`${url}/rest/v1/login_attempts?key=eq.${encodeURIComponent("admin:" + who)}&select=fails,last_at`, { headers: H(key), signal: AbortSignal.timeout(3000) });
    if (!r.ok) return null;
    const [row] = await r.json();
    return row || {};
  } catch { return null; }
}
/** The shared lock for an IP (database), or null when there's no database to ask. */
async function dbState(ip_) {
  const row = await dbRow(ip_);
  if (!row) return null;
  if (!row.last_at) return { fails: 0, until: 0 };
  const last = new Date(row.last_at).getTime();
  if (Date.now() - last > 24 * 3_600_000) return { fails: 0, until: 0 }; // a day of quiet forgives
  return { fails: row.fails, until: last + lockFor(row.fails) };
}
async function dbWrite(who, fails) {
  const { url, key } = DB();
  if (!url || !key) return;
  const h = H(key, { "Content-Type": "application/json", Prefer: "resolution=merge-duplicates" });
  try {
    if (fails === 0) await fetch(`${url}/rest/v1/login_attempts?key=eq.${encodeURIComponent("admin:" + who)}`, { method: "DELETE", headers: h, signal: AbortSignal.timeout(3000) });
    else await fetch(`${url}/rest/v1/login_attempts?on_conflict=key`, { method: "POST", headers: h, body: JSON.stringify({ key: "admin:" + who, fails, last_at: new Date().toISOString() }), signal: AbortSignal.timeout(3000) });
  } catch { /* the cookie and memory still count */ }
}
/** A database function (FIX-LIST #84): its answer, or undefined when it can't be called (no database, or the function isn't there yet). */
async function rpc(fn, args) {
  const { url, key } = DB();
  if (!url || !key) return undefined;
  try {
    const r = await fetch(`${url}/rest/v1/rpc/${fn}`, { method: "POST", headers: H(key, { "Content-Type": "application/json" }), body: JSON.stringify(args), signal: AbortSignal.timeout(3000) });
    return r.ok ? r.json() : undefined;
  } catch { return undefined; }
}
/** One more miss for "admin:<who>", counted in one statement (admin_login_miss); null when the database can't count it. */
async function dbMiss(who, windowHours, fallback) {
  const n = await rpc("admin_login_miss", { p_key: "admin:" + who, p_window_hours: windowHours });
  if (typeof n === "number") return n;
  // ponytail: until that migration is in, read-then-write: two misses at the same instant can count as one
  await dbWrite(who, fallback);
  return null;
}
/** A settings value: the text, undefined when there's no row, or null when the database can't say. */
async function getSetting(name) {
  const { url, key } = DB();
  if (!url || !key) return null;
  try {
    const r = await fetch(`${url}/rest/v1/settings?key=eq.${name}&select=value`, { headers: H(key), signal: AbortSignal.timeout(3000) });
    if (!r.ok) return null;
    const [row] = await r.json();
    return row ? row.value : undefined;
  } catch { return null; }
}
/** Saves a settings value; false when the database can't. */
async function setSetting(name, value) {
  const { url, key } = DB();
  if (!url || !key) return false;
  try {
    const r = await fetch(`${url}/rest/v1/settings?on_conflict=key`, { method: "POST", headers: H(key, { "Content-Type": "application/json", Prefer: "resolution=merge-duplicates,return=minimal" }),
      body: JSON.stringify({ key: name, value: String(value) }), signal: AbortSignal.timeout(3000) });
    return r.ok;
  } catch { return false; }
}

/** The global throttle: { fails, last } across every address (database, else this server's memory). */
async function globalState() {
  const row = await dbRow(GLOBAL.key);
  const g = row ? { fails: row.fails || 0, last: row.last_at ? new Date(row.last_at).getTime() : 0 } : tries.get(GLOBAL.key) || { fails: 0, last: 0 };
  return Date.now() - g.last > GLOBAL.hourMs ? { fails: 0, last: 0 } : g; // an hour with no misses starts over
}
const globalUntil = (g) => (g.fails >= GLOBAL.fails ? g.last + GLOBAL.lockMs : 0);
async function globalMiss() {
  const g = await globalState();
  const counted = await dbMiss(GLOBAL.key, GLOBAL.hourMs / 3_600_000, g.fails + 1);
  tries.set(GLOBAL.key, { fails: counted ?? g.fails + 1, last: Date.now() });
}

/** The admin session version (1 when unset), or null when the database can't say. */
async function version() {
  const v = await getSetting("admin_session_version");
  return v === null ? null : Number(v) || 1;
}
/** "Sign out everywhere": every session and known-device cookie made before stops working. Throws when the database can't. */
async function bumpVersion() {
  const v = await version();
  if (v === null || !(await setSetting("admin_session_version", v + 1))) throw new Error("no database");
}
// a sealed cookie still counts when its version is the current one, or when the database can't say (never locked out by an outage)
const current = (c, v, now) => !!c && c.exp > now && (v === null || c.v === v);

// the address Vercel saw (x-real-ip / x-vercel-forwarded-for are set by Vercel; a caller can prepend anything to x-forwarded-for) (FIX-LIST #28)
const ip = (req) => String(req.headers["x-real-ip"] || req.headers["x-vercel-forwarded-for"] || req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "?").split(",")[0].trim();
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
async function lockState(req) {
  const mem = tries.get(ip(req)) || { fails: 0, until: 0 };
  const c = open(cookies(req).fig_admin_tries) || { fails: 0, until: 0 };
  const d = (await dbState(ip(req))) || { fails: 0, until: 0 };
  return { fails: Math.max(mem.fails, c.fails || 0, d.fails), until: Math.max(mem.until, c.until || 0, d.until) };
}
function lockFor(fails) {
  if (fails < FREE_TRIES) return 0;
  return LOCKS_MIN[Math.min(fails - FREE_TRIES, LOCKS_MIN.length - 1)] * 60_000;
}
const locked = (until, now) => ({ status: 429, body: { locked: true, retryIn: Math.ceil((until - now) / 1000) } });

/** The locks before any password or code work: this address, then the global one unless this is a known device. */
async function gate(req, now, v) {
  const st = await lockState(req);
  if (st.until > now) return { st, stop: locked(st.until, now) };
  const dev = open(cookies(req).fig_admin_device);
  const known = current(dev, v, now) && dev.dev === 1;
  if (!known) { const until = globalUntil(await globalState()); if (until > now) return { st, known, stop: locked(until, now) }; }
  return { st, known, stop: null };
}
/** A wrong password or code: counts for this address and (unless a known device) globally. */
async function miss(req, st, known, now, wrong) {
  const fails = Math.max(st.fails + 1, (await dbMiss(ip(req), 24, st.fails + 1)) ?? 0); // a day of quiet forgives, as dbState
  const until = now + lockFor(fails);
  tries.set(ip(req), { fails, until });
  if (!known) await globalMiss();
  const left = Math.max(0, FREE_TRIES - fails);
  return {
    status: 401,
    body: until > now ? { locked: true, retryIn: Math.ceil((until - now) / 1000) } : { error: wrong, triesLeft: left },
    headers: [cookie("fig_admin_tries", seal({ fails, until }), 24 * 3600)],
  };
}
/** In: the session cookie, a known-device cookie for 90 days, and the try count cleared. */
async function welcome(req, now, v) {
  tries.delete(ip(req));
  await dbWrite(ip(req), 0);
  const ver = v ?? 0; // 0 never matches the database's version: once it answers again, sign in again
  return { status: 200, body: { ok: true }, headers: [
    cookie("fig_admin", seal({ exp: now + SESSION_HOURS * 3_600_000, v: ver }), SESSION_HOURS * 3600),
    cookie("fig_admin_device", seal({ dev: 1, exp: now + DEVICE_DAYS * 86_400_000, v: ver }), DEVICE_DAYS * 86400),
    cookie("fig_admin_tries", "", 0), cookie("fig_admin_step", "", 0),
  ] };
}

/** Handles a sign-in attempt. Returns { status, body, headers }. */
async function login(req, password) {
  const now = Date.now();
  const v = await version();
  const { st, known, stop } = await gate(req, now, v);
  if (stop) return stop;
  if (!secret() || !process.env.ADMIN_PASSWORD_HASH) return { status: 503, body: { error: "Admin isn't set up on the server yet." } };
  if (!passwordOk(password)) return miss(req, st, known, now, "Wrong password.");
  // the code step (a known device doesn't skip it): the password alone only opens the code box for a few minutes
  if (process.env.ADMIN_TOTP_SECRET) return { status: 200, body: { needCode: true }, headers: [cookie("fig_admin_step", seal({ step: 1, exp: now + CODE_MIN * 60_000, v: v ?? 0 }), CODE_MIN * 60)] };
  return welcome(req, now, v);
}

/** An authenticator code (once only) or a backup code: true, false, or a message when it can't be checked. */
async function codeOk(code, now) {
  const typed = String(code || "").trim();
  if (totp.looksBackup(typed)) {
    const saved = await getSetting("admin_backup_codes");
    if (saved === null) return "Backup codes need the database, which isn't answering. Use the code from your authenticator app.";
    const left = JSON.parse(saved || "[]");
    const want = Buffer.from(totp.hashBackup(typed));
    const i = left.findIndex((h) => String(h).length === want.length && crypto.timingSafeEqual(Buffer.from(String(h)), want));
    if (i < 0) return false;
    left.splice(i, 1);
    // used up only if that saved; a right code that couldn't be crossed off isn't a wrong try (FIX-LIST #84)
    return (await setSetting("admin_backup_codes", JSON.stringify(left))) || "That backup code is right, but the database didn’t save it as used. Try again in a minute, or use the code from your authenticator app.";
  }
  const step = totp.matchStep(process.env.ADMIN_TOTP_SECRET, typed, now);
  if (step === null) return false;
  if (step <= lastStepMem) return false; // used already: a replayed code is a wrong one
  // compare-and-set in one statement, so the same code sent twice at once passes once (FIX-LIST #84)
  const fresh = await rpc("admin_totp_use", { p_step: step });
  if (fresh === false) return false;
  if (fresh === undefined) {
    // ponytail: the database can't (or the function isn't there yet): read-then-write, plus this server's memory
    const saved = await getSetting("admin_totp_last_step");
    if (step <= (Number(saved) || 0)) return false;
    await setSetting("admin_totp_last_step", step);
  }
  lastStepMem = Math.max(lastStepMem, step);
  return true;
}
/** The code after the password. */
async function loginCode(req, code) {
  const now = Date.now();
  const v = await version();
  const { st, known, stop } = await gate(req, now, v);
  if (stop) return stop;
  const step = open(cookies(req).fig_admin_step);
  if (!process.env.ADMIN_TOTP_SECRET || !step || step.step !== 1 || !current(step, v, now)) return { status: 401, body: { error: "Sign in again.", again: true }, headers: [cookie("fig_admin_step", "", 0)] };
  const ok = await codeOk(code, now);
  if (typeof ok === "string") return { status: 503, body: { error: ok } };
  if (!ok) return miss(req, st, known, now, "Wrong code.");
  return welcome(req, now, v);
}

/** Signed in: a session cookie in date whose version is the current one. */
async function signedIn(req) {
  const s = open(cookies(req).fig_admin);
  if (!s || !(s.exp > Date.now())) return false;
  return current(s, await version(), Date.now());
}
const logoutCookie = () => cookie("fig_admin", "", 0);
/** "Sign out everywhere": a new version, then this browser's cookies go too. */
async function logoutEverywhere() {
  await bumpVersion();
  return [logoutCookie(), cookie("fig_admin_device", "", 0)];
}

// setting up the authenticator (signed in only): a new secret waits in a 10-minute sealed cookie (never the database or a log)
// until a code from the app proves it was added; then 8 backup codes, and the Vercel step for the user
function enrolStart() {
  const s = totp.newSecret();
  return { secret: s, uri: totp.uri(s), cookie: cookie("fig_admin_enrol", seal({ s, exp: Date.now() + 10 * 60_000 }), 600) };
}
async function enrolConfirm(req, code) {
  const e = open(cookies(req).fig_admin_enrol);
  if (!e || !(e.exp > Date.now()) || !e.s) return { status: 400, body: { error: "That set-up timed out. Start again." } };
  const step = totp.matchStep(e.s, code);
  if (step === null) return { status: 400, body: { error: "That code didn't match. Check the app and try the newest code." } };
  const backup = totp.backupCodes();
  const saved = (await setSetting("admin_backup_codes", JSON.stringify(backup.map(totp.hashBackup)))) && (await setSetting("admin_totp_last_step", step));
  lastStepMem = step;
  return { status: 200, body: { ok: true, secret: e.s, env: "ADMIN_TOTP_SECRET", backup: saved ? backup : null }, headers: [cookie("fig_admin_enrol", "", 0)] };
}

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

module.exports = { login, loginCode, signedIn, logoutCookie, logoutEverywhere, enrolStart, enrolConfirm, send, readJson, sameOrigin,
  _test: { seal, open, lockFor, passwordOk, GLOBAL, reset: () => { tries.clear(); lastStepMem = 0; } } };
