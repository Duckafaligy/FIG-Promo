// FIG admin: password check, lockout and sessions. Everything secret lives in Vercel environment variables:
//   ADMIN_PASSWORD_HASH  "scrypt:<salt hex>:<hash hex>" (never the password itself)
//   SESSION_SECRET       random string used to sign the session cookie
//   ADMIN_TOTP_SECRET    optional: an authenticator secret (base32) that overrides the one kept in the database
//   ADMIN_TOTP_RESET     the user's way back (a new value each time, e.g. today's date; redeploy): while "Require a code" is on,
//                        the next password sign-in sets up a new phone (each value once)
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
// - the second step (FIX-LIST #103) is on once the user turns on "Require a code at every sign-in" in Security (settings
//   admin_twostep_required; off until then: the password signs in, plus the code step when a working authenticator is saved).
//   While it's on, the password only opens a 5-minute code step: a code from
//   the authenticator app (each one works once: settings admin_totp_last_step, or memory when the database is down), one of 8
//   one-time backup codes (settings admin_backup_codes, SHA-256 only), or a code sent to the admin's own email or phone
//   (6 digits, 10 minutes, one use, 3 sends an hour, hash only). With nothing set up yet (or the user's ADMIN_TOTP_RESET=1), the
//   password opens a 15-minute set-up instead: scan, a code, the backup codes saved, then the secret is stored (encrypted,
//   second.js) and only then a session starts. The secret is never saved before a right code AND "I saved the codes".
const crypto = require("crypto");
const totp = require("./totp");
const second = require("./second");

const FREE_TRIES = 5;
const LOCKS_MIN = [1, 5, 15, 60]; // minutes, after try 5, 6, 7, 8+
const SESSION_HOURS = 8;
const GLOBAL = { key: "*", fails: 20, hourMs: 3_600_000, lockMs: 5 * 60_000 };
const DEVICE_DAYS = 90;
const CODE_MIN = 5; // the time to type the code after the password
const ENROL_MIN = 15; // the time to set up the authenticator after the password
const DOWN = "The database isn't answering, so the second step can't be checked. Try again in a minute.";
const UNREADABLE = "The saved authenticator can't be read (the server's secret changed). Set ADMIN_TOTP_RESET=1 in Vercel, redeploy, and sign in to set up your phone again.";
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
  const on = await twoStepRequired();
  if (on === null && !process.env.ADMIN_TOTP_SECRET) return { status: 503, body: { error: DOWN } }; // can't tell: never guess "off"
  if (!on) {
    // OFF (the user turns it on in Security, FIX-LIST #103): as before, the code step only when a working authenticator is saved
    // (or ADMIN_TOTP_SECRET); no set-up from the password alone, and the reset flag does nothing
    const sec = await secretState();
    if (sec.down) return { status: 503, body: { error: DOWN } }; // fail closed: a saved phone that can't be read now is never skipped (#152)
    if (sec.secret) return { status: 200, body: { needCode: true, ...(await contacts()) }, headers: [cookie("fig_admin_step", seal({ step: 1, exp: now + CODE_MIN * 60_000, v: v ?? 0 }), CODE_MIN * 60)] };
    return welcome(req, now, v);
  }
  // ON: always a second step (a known device doesn't skip it): the password alone only opens the code box, or the set-up
  const sec = await secretState();
  if (sec.down) return { status: 503, body: { error: DOWN } };
  if (sec.unreadable) return { status: 503, body: { error: UNREADABLE } };
  if (sec.none) return { status: 200, body: { needEnrol: true, mail: second.mailOn(), text: second.textOn() }, headers: [cookie("fig_admin_step", seal({ step: 1, enrol: 1, exp: now + ENROL_MIN * 60_000, v: v ?? 0 }), ENROL_MIN * 60)] };
  return { status: 200, body: { needCode: true, ...(await contacts()), ...((await resetUsed()) ? { resetUsed: true } : {}) }, headers: [cookie("fig_admin_step", seal({ step: 1, exp: now + CODE_MIN * 60_000, v: v ?? 0 }), CODE_MIN * 60)] };
}
/** The authenticator's secret: { secret }, { none } (nothing set up yet, or the user's reset flag), { down } or { unreadable }. */
async function secretState() {
  if (process.env.ADMIN_TOTP_SECRET) return { secret: process.env.ADMIN_TOTP_SECRET };
  // the user's reset flag works ONCE per value (Agent #4): when its set-up completes the value is recorded, and a used value is
  // never honoured again, whatever deploys follow; resetting again takes a NEW value (the card says: today's date)
  if (process.env.ADMIN_TOTP_RESET && (await twoStepRequired()) === true) { // only while the two-step is required
    const used = await usedResets();
    if (used === null) return { down: true };
    if (!used.includes(process.env.ADMIN_TOTP_RESET)) return { none: true, reset: true };
  }
  const v = await getSetting("admin_totp_secret_enc");
  if (v === null) return { down: true };
  if (v === undefined) return { none: true };
  const secret = second.decrypt(v);
  return secret ? { secret } : { unreadable: true };
}
/** "Require a code at every sign-in" (FIX-LIST #103 DESIGN, the user 2026-10-19): off until the user turns it on in Security.
 *  true / false, or null when the database can't say. */
async function twoStepRequired() {
  const v = await getSetting("admin_twostep_required");
  return v === null ? null : v === "on";
}
/** The reset values already used (a list), or null when the database can't say. */
async function usedResets() {
  const v = await getSetting("admin_totp_reset_used");
  if (v === null) return null;
  try { const l = JSON.parse(v || "[]"); return Array.isArray(l) ? l.map(String) : []; } catch { return []; }
}
/** The flag is set but its value was already used: it does nothing, and the pages say to set a new one or delete it. */
async function resetUsed() {
  if (!process.env.ADMIN_TOTP_RESET) return false;
  const used = await usedResets();
  return !!used && used.includes(process.env.ADMIN_TOTP_RESET);
}
/** The flag is set but used (or a phone is set up anyway): every admin page shows a red line until it's deleted in Vercel. */
async function resetLeftOn() {
  if (!process.env.ADMIN_TOTP_RESET) return false;
  return (await resetUsed()) || !!(await getSetting("admin_totp_secret_enc"));
}
/** Which "send me a code" ways the code step offers: on the server, with an address saved (never the address itself). */
async function contacts() {
  const out = {};
  if (second.mailOn() && await getSetting("admin_email")) out.mail = true;
  if (second.textOn() && await getSetting("admin_phone")) out.text = true;
  return out;
}

/** An authenticator code (once only), a backup code or a code sent by email / text: true, false, or a message when it can't be checked. */
async function codeOk(code, now, secret) {
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
  const step = totp.matchStep(secret, typed, now);
  if (step === null) return sentCodeOk(typed, now);
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
/** A code sent to the admin's email or phone: once, within 10 minutes. */
async function sentCodeOk(typed, now) {
  if (!/^\d{6}$/.test(typed)) return false;
  const saved = await getSetting("admin_contact_code");
  if (!saved) return false;
  let c; try { c = JSON.parse(saved); } catch { return false; }
  if (!c.h || !(c.exp > now) || !second.sameHash(c.h, second.hashCode(typed))) return false;
  return (await setSetting("admin_contact_code", "{}")) || DOWN; // used up only once that's saved
}
/** "Email me a code" / "Text me a code" in the code step: the same answer whether it was sent or not, and every send counts
 *  toward the global throttle; at most 3 an hour. Only to the address saved at set-up, never one typed here. */
async function sendLoginCode(req, via) {
  const now = Date.now();
  const v = await version();
  const { stop } = await gate(req, now, v);
  if (stop) return stop;
  const step = open(cookies(req).fig_admin_step);
  if (!step || step.step !== 1 || step.enrol || !current(step, v, now)) return { status: 401, body: { error: "Sign in again.", again: true }, headers: [cookie("fig_admin_step", "", 0)] };
  const way = via === "text" ? "text" : "mail";
  const same = { status: 200, body: { ok: true, sent: way === "text" ? "If texts are set up, a code is on its way to the admin phone." : "If email codes are set up, a code is on its way to the admin email." } };
  await globalMiss();
  if (!(way === "text" ? second.textOn() : second.mailOn())) return same;
  const to = await getSetting(way === "text" ? "admin_phone" : "admin_email");
  if (!to) return same;
  let sends = []; try { sends = JSON.parse((await getSetting("admin_contact_sends")) || "[]").filter((t) => t > now - 3_600_000); } catch { /* start over */ }
  if (sends.length >= 3) return same;
  const code = second.newCode();
  if (!(await setSetting("admin_contact_sends", JSON.stringify(sends.concat(now))))) return same;
  if (!(await setSetting("admin_contact_code", JSON.stringify({ h: second.hashCode(code), exp: now + 10 * 60_000 })))) return same;
  await second.sendCode(way === "text" ? "text" : "email", to, code);
  return same;
}

/** The code after the password. */
async function loginCode(req, code) {
  const now = Date.now();
  const v = await version();
  const { st, known, stop } = await gate(req, now, v);
  if (stop) return stop;
  const step = open(cookies(req).fig_admin_step);
  if (!step || step.step !== 1 || step.enrol || !current(step, v, now)) return { status: 401, body: { error: "Sign in again.", again: true }, headers: [cookie("fig_admin_step", "", 0)] };
  const sec = await secretState();
  if (!sec.secret) return { status: 503, body: { error: sec.unreadable ? UNREADABLE : sec.none ? "Sign in again to set up the authenticator." : DOWN } };
  const ok = await codeOk(code, now, sec.secret);
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

// setting up the authenticator (FIX-LIST #103): right after the password when nothing is set up (the step cookie says enrol), or
// signed in to move it to a new phone. The new secret and everything else wait in a 15-minute ENCRYPTED cookie until the last
// step; the database gets them only after a right code AND "I saved the backup codes". A contact (email / phone) is optional and
// only saved once a code sent to it comes back.
const ENROL = "fig_admin_enrol";
const enrolCookie = (e) => cookie(ENROL, second.encrypt(JSON.stringify(e)), ENROL_MIN * 60);
function readEnrol(req) {
  const raw = cookies(req)[ENROL];
  const e = raw && second.decrypt(raw);
  try { const o = e && JSON.parse(e); return o && o.exp > Date.now() ? o : null; } catch { return null; }
}
/** Who may set up: a signed-in session, or the enrol step from a right password while nothing is set up. */
async function enrolWho(req) {
  if (await signedIn(req)) return { session: true };
  const now = Date.now(), v = await version();
  const step = open(cookies(req).fig_admin_step);
  if (!step || step.step !== 1 || !step.enrol || !current(step, v, now)) return null;
  if ((await twoStepRequired()) !== true) return null; // while off, set-up happens only signed in (Security), never from the password alone
  const sec = await secretState();
  return sec.none ? { session: false, v, reset: !!sec.reset } : null; // one was set up meanwhile: back to the code step
}
const notNow = { status: 401, body: { error: "Sign in again.", again: true } };
async function enrolStart(req, code) {
  const who = await enrolWho(req);
  if (!who) return notNow;
  if (who.session) {
    // replacing the phone: a code from the current one (or a backup code) first, so a borrowed open session can't swap it
    const now = Date.now(), v = await version(), sec = await secretState();
    if (sec.down) return { status: 503, body: { error: DOWN } };
    if (sec.secret) { // nothing working set up yet (none, or one it can't read): the session is enough to set up the first
      const { st, known, stop } = await gate(req, now, v);
      if (stop) return stop;
      const ok = await codeOk(code, now, sec.secret);
      if (typeof ok === "string") return { status: 503, body: { error: ok } };
      if (!ok) return miss(req, st, known, now, "Type a code from your current phone, or a backup code.");
    }
  }
  const s = totp.newSecret();
  return { status: 200, body: { ok: true, secret: s, uri: totp.uri(s), mail: second.mailOn(), text: second.textOn() }, headers: [enrolCookie({ s, exp: Date.now() + ENROL_MIN * 60_000 })] };
}
async function enrolCode(req, code) {
  const who = await enrolWho(req), e = readEnrol(req);
  if (!who) return notNow;
  if (!e || !e.s) return { status: 400, body: { error: "That set-up timed out. Start again." } };
  const now = Date.now();
  const step = totp.matchStep(e.s, code, now);
  if (step === null) {
    if (who.session) return { status: 400, body: { error: "That code didn't match. Check the app and try the newest code." } };
    const { st, known, stop } = await gate(req, now, who.v);
    return stop || miss(req, st, known, now, "That code didn't match. Check the app and try the newest code."); // counts, like a wrong sign-in code
  }
  const backup = totp.backupCodes();
  return { status: 200, body: { ok: true, backup }, headers: [enrolCookie({ ...e, ok: 1, step, bh: backup.map(totp.hashBackup) })] };
}
/** An email or phone for "send me a code": a code goes to it now; it's saved only when that code comes back. */
async function enrolContact(req, via, to) {
  const who = await enrolWho(req), e = readEnrol(req) || (who && who.session ? { exp: Date.now() + ENROL_MIN * 60_000 } : null);
  if (!who) return notNow;
  if (!e || (!who.session && !e.ok)) return { status: 400, body: { error: "Set up the authenticator first." } };
  const way = via === "text" ? "text" : "email";
  if (!(way === "text" ? second.textOn() : second.mailOn())) return { status: 400, body: { error: way === "text" ? "Texts aren't set up on the server yet." : "Email codes can't be sent: the server has no email sender set up yet (Resend)." } };
  const addr = second.cleanTo(way, to);
  if (!addr) return { status: 400, body: { error: way === "text" ? "Type the number with its country code, like +1 647 555 0123." : "Check the email address." } };
  const now = Date.now();
  let sends = []; try { sends = JSON.parse((await getSetting("admin_contact_sends")) || "[]").filter((t) => t > now - 3_600_000); } catch { /* start over */ }
  if (sends.length >= 3) return { status: 429, body: { error: "3 codes were sent in the last hour. Try again later." } };
  await setSetting("admin_contact_sends", JSON.stringify(sends.concat(now)));
  const code = second.newCode();
  if (!(await second.sendCode(way, addr, code))) return { status: 502, body: { error: way === "text" ? "The text didn't go out. Check the number and try again." : "The email didn't go out. Check the address and try again." } };
  return { status: 200, body: { ok: true, to: second.mask(way, addr) }, headers: [enrolCookie({ ...e, contact: { via: way, to: addr, h: second.hashCode(code), exp: now + 10 * 60_000, n: 0 } })] };
}
async function enrolContactOk(req, code) {
  const who = await enrolWho(req), e = readEnrol(req);
  if (!who) return notNow;
  const c = e && e.contact;
  if (!c || !(c.exp > Date.now()) || c.n >= 5) return { status: 400, body: { error: "That code expired. Send a new one." } };
  if (!second.sameHash(c.h, second.hashCode(code))) return { status: 400, body: { error: "That code didn't match." }, headers: [enrolCookie({ ...e, contact: { ...c, n: c.n + 1 } })] };
  const key = c.via === "text" ? "admin_phone" : "admin_email";
  if (who.session && !e.ok) { // signed in, changing only the address: saved now
    if (!(await setSetting(key, c.to))) return { status: 503, body: { error: DOWN } };
    return { status: 200, body: { ok: true, saved: true, to: second.mask(c.via, c.to) }, headers: [cookie(ENROL, "", 0)] };
  }
  return { status: 200, body: { ok: true, to: second.mask(c.via, c.to) }, headers: [enrolCookie({ ...e, contact: undefined, contactOk: { key, to: c.to } })] };
}
/** The last step: only after a right code and "I saved the backup codes". Everything is saved, the secret last; then a session. */
async function enrolDone(req, saved) {
  const who = await enrolWho(req), e = readEnrol(req);
  if (!who) return notNow;
  if (!e || !e.ok || !e.s) return { status: 400, body: { error: "That set-up timed out. Start again." } };
  if (saved !== true) return { status: 400, body: { error: "Tick that you saved the backup codes first." } };
  const ok = (await setSetting("admin_backup_codes", JSON.stringify(e.bh))) && (await setSetting("admin_totp_last_step", e.step)) &&
    (!e.contactOk || (await setSetting(e.contactOk.key, e.contactOk.to))) && (await setSetting("admin_totp_secret_enc", second.encrypt(e.s)));
  if (!ok) return { status: 503, body: { error: "The database didn't save it, so nothing changed. Try again in a minute." } };
  lastStepMem = Math.max(lastStepMem, e.step);
  if (who.session) {
    // a new phone: every other session and remembered device signs out (a new session version); this browser stays in
    try { await bumpVersion(); } catch { return { status: 503, body: { error: "The new phone is set up, but other browsers couldn't be signed out. Use Sign out everywhere." }, headers: [cookie(ENROL, "", 0)] }; }
    const out = await welcome(req, Date.now(), await version());
    out.headers.push(cookie(ENROL, "", 0));
    return out;
  }
  if (who.reset) { const used = (await usedResets()) || []; await setSetting("admin_totp_reset_used", JSON.stringify(used.concat(process.env.ADMIN_TOTP_RESET))); } // that value has done its one job
  const out = await welcome(req, Date.now(), who.v);
  if (who.reset) out.body.removeFlag = true;
  out.headers.push(cookie(ENROL, "", 0));
  return out;
}
/** Security's "Require a code at every sign-in" (FIX-LIST #103 DESIGN). Signed in only, and always with a right code (from the
 *  authenticator, or a backup code). On only once a working authenticator is saved WITH its backup codes (they're saved only after
 *  "I saved the backup codes"), so it can never lock the user out; off again needs a session plus a code too. */
async function setTwoStep(req, on, code) {
  if (!(await signedIn(req))) return notNow;
  const now = Date.now(), v = await version();
  const sec = await secretState();
  if (sec.down) return { status: 503, body: { error: DOWN } };
  if (on === true) {
    if (!sec.secret) return { status: 400, body: { error: "Set up an authenticator first." } };
    let codes = null; try { codes = JSON.parse((await getSetting("admin_backup_codes")) || "null"); } catch { /* none */ }
    if (!Array.isArray(codes) || !codes.length) return { status: 400, body: { error: "Set up the authenticator here first, so you have backup codes." } };
  } else if (on !== false) return { status: 400, body: { error: "That was not a valid request." } };
  if (!sec.secret && !totp.looksBackup(String(code || "").trim())) return { status: 400, body: { error: "Type a backup code." } };
  const { st, known, stop } = await gate(req, now, v);
  if (stop) return stop;
  const ok = await codeOk(code, now, sec.secret);
  if (typeof ok === "string") return { status: 503, body: { error: ok } };
  if (!ok) return miss(req, st, known, now, "Wrong code.");
  if (!(await setSetting("admin_twostep_required", on ? "on" : "off"))) return { status: 503, body: { error: "The database didn't save it, so nothing changed. Try again in a minute." } };
  return { status: 200, body: { ok: true, on } };
}
/** For the Security page: what's set up (never a secret or a whole address). */
async function secondState() {
  const [enc, email, phone, codes] = await Promise.all([getSetting("admin_totp_secret_enc"), getSetting("admin_email"), getSetting("admin_phone"), getSetting("admin_backup_codes")]);
  let left = null; try { left = JSON.parse(codes || "[]").length; } catch { /* unknown */ }
  return { required: await twoStepRequired(), env: !!process.env.ADMIN_TOTP_SECRET, reset: !!process.env.ADMIN_TOTP_RESET, resetUsed: await resetUsed(), saved: !!enc, mail: second.mailOn(), text: second.textOn(),
    email: second.mask("email", email), phone: second.mask("text", phone), backupLeft: codes === null ? null : left };
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

module.exports = { setTwoStep, twoStepRequired, resetLeftOn, login, loginCode, sendLoginCode, signedIn, logoutCookie, logoutEverywhere, enrolStart, enrolCode, enrolContact, enrolContactOk, enrolDone, secondState, send, readJson, sameOrigin,
  _test: { seal, open, lockFor, passwordOk, GLOBAL, reset: () => { tries.clear(); lastStepMem = 0; } } };
