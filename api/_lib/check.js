// node api/_lib/check.js  -- the admin's sign-in checks (Vercel runs it on every build):
// the lock schedule, cookies, the password, the global throttle and the known device, sessions voided by "Sign out everywhere",
// the authenticator step (RFC 6238 test vectors, one use per code, backup codes), and a probe of every admin-api action.
// Never the live database: on Vercel the build has its keys, so they're replaced by a fake one in memory here (test misses
// against the real login_attempts once locked every deploy, 2026-10-11).
const assert = require("assert");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

process.env.SUPABASE_URL = "https://fake.invalid";
process.env.SUPABASE_SERVICE_ROLE_KEY = "fake";
process.env.SESSION_SECRET = "test-secret";
delete process.env.ADMIN_TOTP_SECRET;
const salt = crypto.randomBytes(16);
process.env.ADMIN_PASSWORD_HASH = "scrypt:" + salt.toString("hex") + ":" + crypto.scryptSync("right", salt, 32).toString("hex");

// the fake database: the two tables auth.js uses (settings, login_attempts); "down" makes every call fail
const table = { settings: new Map(), login_attempts: new Map() };
let down = false;
global.fetch = async (url, opts = {}) => {
  if (down) throw new Error("database down");
  const u = new URL(url);
  const name = u.pathname.split("/").pop();
  const t = table[name];
  if (!t) throw new Error("the check touched " + u.pathname);
  const json = (rows) => ({ ok: true, status: 200, json: async () => rows, text: async () => JSON.stringify(rows) });
  const key = (u.searchParams.get("key") || "").replace(/^eq\./, "");
  if (!opts.method || opts.method === "GET") return json(t.has(key) ? [t.get(key)] : []);
  if (opts.method === "DELETE") { t.delete(key); return json([]); }
  const row = JSON.parse(opts.body); t.set(row.key, row); return json([]);
};

const auth = require("./auth");
const totp = require("./totp");
const { login, loginCode, signedIn, logoutEverywhere, enrolStart, enrolConfirm, _test } = auth;
const jar = (headers = []) => Object.fromEntries(headers.map((h) => { const [kv] = h.split(";"); const i = kv.indexOf("="); return [kv.slice(0, i), decodeURIComponent(kv.slice(i + 1))]; }));
const asCookie = (c) => Object.entries(c).filter(([, v]) => v).map(([k, v]) => k + "=" + encodeURIComponent(v)).join("; ");
const reqFrom = (ip, c = {}) => ({ headers: { "x-real-ip": ip, cookie: asCookie(c) } });
const fresh = () => { _test.reset(); table.settings.clear(); table.login_attempts.clear(); down = false; delete process.env.ADMIN_TOTP_SECRET; };

(async () => {
  // the lock schedule, cookies, password
  assert.strictEqual(_test.lockFor(4), 0);
  assert.strictEqual(_test.lockFor(5), 60_000);
  assert.strictEqual(_test.lockFor(6), 300_000);
  assert.strictEqual(_test.lockFor(8), 3_600_000);
  assert.strictEqual(_test.lockFor(20), 3_600_000);
  assert.deepStrictEqual(_test.open(_test.seal({ a: 1 })), { a: 1 });
  assert.strictEqual(_test.open(_test.seal({ a: 1 }).replace(/.$/, "x")), null);
  assert.strictEqual(_test.passwordOk("right"), true);
  assert.strictEqual(_test.passwordOk("wrong"), false);

  // per address: 5 misses lock it, and even the right password waits
  fresh();
  for (let i = 1; i <= 4; i++) assert.strictEqual((await login(reqFrom("1.2.3.4"), "nope")).status, 401);
  const fifth = await login(reqFrom("1.2.3.4"), "nope");
  assert.ok(fifth.body.locked && fifth.body.retryIn === 60, "locked for a minute after 5 misses");
  assert.strictEqual((await login(reqFrom("1.2.3.4"), "right")).status, 429, "even the right password waits out the lock");
  console.log("ok: per-address lock (5 misses, then 1 min)");

  // the global throttle: 20 misses from 20 addresses lock everyone out for 5 minutes, before any password work...
  fresh();
  for (let i = 0; i < 20; i++) assert.strictEqual((await login(reqFrom("10.0.0." + i), "nope")).status, 401);
  const g = await login(reqFrom("10.9.9.9"), "right");
  assert.strictEqual(g.status, 429, "a new address is locked out by the global throttle");
  assert.ok(g.body.retryIn > 290 && g.body.retryIn <= 300, "for 5 minutes");
  assert.strictEqual(table.login_attempts.get("admin:*").fails, 20, "the global count is kept in the database");
  // ...except a known device, which skips the global lock only
  fresh();
  const first = await login(reqFrom("8.8.8.8"), "right");
  const device = jar(first.headers).fig_admin_device;
  assert.ok(device, "signing in leaves a known-device cookie");
  for (let i = 0; i < 20; i++) await login(reqFrom("10.1.0." + i), "nope");
  assert.strictEqual((await login(reqFrom("10.9.9.9"), "right")).status, 429, "a stranger is locked out");
  assert.strictEqual((await login(reqFrom("10.9.9.9", { fig_admin_device: device }), "right")).status, 200, "the owner's device still gets in");
  for (let i = 0; i < 5; i++) await login(reqFrom("7.7.7.7", { fig_admin_device: device }), "nope");
  assert.strictEqual((await login(reqFrom("7.7.7.7", { fig_admin_device: device }), "right")).status, 429, "a known device never skips the per-address lock");
  const forgedDevice = _test.seal({ dev: 1, exp: Date.now() + 1e9, v: 1 }).replace(/^./, "x");
  assert.strictEqual((await login(reqFrom("10.9.9.8", { fig_admin_device: forgedDevice }), "right")).status, 429, "a forged device cookie doesn't skip it");
  console.log("ok: global throttle (20 misses/hour -> 5 min for everyone), known device skips only that");

  // "Sign out everywhere": old sessions and old known devices stop working
  fresh();
  const a = jar((await login(reqFrom("8.8.8.8"), "right")).headers);
  assert.strictEqual(await signedIn(reqFrom("8.8.8.8", a)), true, "signed in");
  await logoutEverywhere();
  assert.strictEqual(table.settings.get("admin_session_version").value, "2");
  assert.strictEqual(await signedIn(reqFrom("8.8.8.8", a)), false, "the old session is void");
  for (let i = 0; i < 20; i++) await login(reqFrom("10.2.0." + i), "nope");
  assert.strictEqual((await login(reqFrom("10.9.9.9", { fig_admin_device: a.fig_admin_device }), "right")).status, 429, "the old device cookie is void too");
  // a database outage never locks the admin out: the cookie's expiry decides
  down = true;
  assert.strictEqual(await signedIn(reqFrom("8.8.8.8", a)), true, "with the database down, an in-date cookie still works");
  down = false;
  const expired = { fig_admin: _test.seal({ exp: Date.now() - 1000, v: 2 }) };
  assert.strictEqual(await signedIn(reqFrom("8.8.8.8", expired)), false, "an expired session is out");
  console.log("ok: session version voids old sessions and devices; an outage falls back to expiry");

  // the authenticator: RFC 6238 test vectors (SHA-1 secret "12345678901234567890", the 6 low digits of the 8-digit values)
  const rfc = totp.base32(Buffer.from("12345678901234567890"));
  for (const [t, code] of [[59, "287082"], [1111111109, "081804"], [1111111111, "050471"], [1234567890, "005924"], [2000000000, "279037"], [20000000000, "353130"]])
    assert.strictEqual(totp.codeAt(totp.unbase32(rfc), Math.floor(t / 30)), code, "RFC 6238 at T=" + t);
  assert.strictEqual(totp.matchStep(rfc, "287082", 59_000), 1);
  assert.strictEqual(totp.matchStep(rfc, "287082", 89_000), 1, "one step late still counts");
  assert.strictEqual(totp.matchStep(rfc, "287082", 119_000), null, "two steps late doesn't");
  assert.deepStrictEqual(totp.unbase32(totp.base32(Buffer.from([1, 2, 3, 250]))), Buffer.from([1, 2, 3, 250]));
  console.log("ok: TOTP matches the RFC 6238 test vectors (6 digits, 30 s, one step either side)");

  // the code step: off while ADMIN_TOTP_SECRET is unset; on, the password alone isn't enough, each code works once
  fresh();
  assert.strictEqual((await login(reqFrom("8.8.8.8"), "right")).body.ok, true, "no secret set: password only, as today");
  const enrol = enrolStart();
  const e = await enrolConfirm(reqFrom("8.8.8.8", jar([enrol.cookie])), totp.codeAt(totp.unbase32(enrol.secret), Math.floor(Date.now() / 30000)));
  assert.strictEqual(e.status, 200, "enrolment needs a valid code from the new secret");
  assert.strictEqual(e.body.backup.length, 8, "8 backup codes");
  assert.ok(!JSON.stringify([...table.settings.values()]).includes(enrol.secret), "the secret is never in the database");
  assert.ok(!JSON.stringify([...table.settings.values()]).includes(e.body.backup[0]), "backup codes are kept only as hashes");
  assert.strictEqual((await enrolConfirm(reqFrom("8.8.8.8", jar([enrol.cookie])), "000000")).status, 400, "a wrong code doesn't enrol");
  const s = enrol.secret; // the user puts the enrolled secret in Vercel
  process.env.ADMIN_TOTP_SECRET = s;
  const T = Math.floor(Date.now() / 30000);
  assert.strictEqual(totp.matchStep(s, totp.codeAt(totp.unbase32(s), T), Date.now()) <= Number(table.settings.get("admin_totp_last_step").value), true, "the enrolment code is used up");
  const pw = await login(reqFrom("8.8.8.8", { fig_admin_device: device }), "right");
  assert.ok(pw.body.needCode && !jar(pw.headers).fig_admin, "the password opens the code step only, even on a known device");
  const stepCookie = jar(pw.headers);
  const now = totp.codeAt(totp.unbase32(s), T + 1); // the next code (one step ahead still counts)
  assert.strictEqual((await loginCode(reqFrom("8.8.8.8"), now)).status, 401, "no code without the password step");
  const ok1 = await loginCode(reqFrom("8.8.8.8", stepCookie), now);
  assert.strictEqual(ok1.status, 200, "the right code signs in");
  assert.ok(jar(ok1.headers).fig_admin);
  const replay = await loginCode(reqFrom("8.8.8.8", stepCookie), now);
  assert.strictEqual(replay.status, 401, "the same code twice is a wrong code");
  assert.strictEqual(replay.body.triesLeft, 4, "and counts as a try");
  down = true; _test.reset(); // memory only: replay protection still holds there
  const late = totp.codeAt(totp.unbase32(s), T - 1); // not used yet in this server's memory
  assert.strictEqual((await loginCode(reqFrom("8.8.8.9", stepCookie), late)).status, 200, "with the database down, a code still works");
  assert.strictEqual((await loginCode(reqFrom("8.8.8.9", stepCookie), late)).status, 401, "and its replay is blocked from memory");
  const noDb = await loginCode(reqFrom("8.8.8.9", stepCookie), e.body.backup[0]);
  assert.ok(noDb.status === 503 && /database/.test(noDb.body.error), "backup codes say they need the database");
  down = false;
  const b1 = await loginCode(reqFrom("8.8.8.10", stepCookie), e.body.backup[0]);
  assert.strictEqual(b1.status, 200, "a backup code works");
  assert.strictEqual((await loginCode(reqFrom("8.8.8.10", stepCookie), e.body.backup[0])).status, 401, "once");
  assert.strictEqual(JSON.parse(table.settings.get("admin_backup_codes").value).length, 7, "7 left");
  for (let i = 0; i < 4; i++) await loginCode(reqFrom("6.6.6.6", stepCookie), "123456");
  assert.ok((await loginCode(reqFrom("6.6.6.6", stepCookie), "123456")).body.locked, "wrong codes share the per-address lock");
  console.log("ok: code step off until ADMIN_TOTP_SECRET is set; then required (even on a known device), one use per code, backup codes once each");

  // the probe: every admin-api action refuses without a real, current session, and cross-origin
  fresh();
  const api = require("../admin-api");
  const page = require("../admin");
  const actions = [...fs.readFileSync(path.join(__dirname, "../admin-api.js"), "utf8").matchAll(/action === "([a-z0-9-]+)"/g)].map((m) => m[1]).filter((x, i, all) => all.indexOf(x) === i);
  const open = ["login", "login-code", "logout"]; // these work without a session (and do nothing without the password)
  const good = jar((await login(reqFrom("8.8.8.8"), "right")).headers).fig_admin;
  const tries = {
    "no cookie": {},
    "forged cookie": { fig_admin: Buffer.from(JSON.stringify({ exp: Date.now() + 1e9, v: 1 })).toString("base64url") + ".forged" },
    "cookie signed with another secret": { fig_admin: Buffer.from(JSON.stringify({ exp: Date.now() + 1e9, v: 1 })).toString("base64url") + "." + crypto.createHmac("sha256", "other").update(Buffer.from(JSON.stringify({ exp: Date.now() + 1e9, v: 1 })).toString("base64url")).digest("base64url") },
    "expired cookie": { fig_admin: _test.seal({ exp: Date.now() - 1000, v: 1 }) },
    "old-version cookie": { fig_admin: _test.seal({ exp: Date.now() + 1e9, v: 0 }) },
  };
  const call = async (handler, action, c, extra = {}) => {
    const res = { statusCode: 0, headers: {}, setHeader(k, v) { this.headers[k] = v; }, end(b) { this.body = b; } };
    await handler({ method: extra.method || "POST", url: "/api/admin-api?do=" + action, headers: { host: "fig-promo.vercel.app", "x-real-ip": "9.9.9.9", cookie: asCookie(c), ...(extra.origin ? { origin: extra.origin } : {}) }, body: {} }, res);
    return res;
  };
  let refused = 0, total = 0;
  for (const action of actions.filter((x) => !open.includes(x))) {
    for (const [what, c] of Object.entries(tries)) { total++; const r = await call(api, action, c); assert.strictEqual(r.statusCode, 401, action + " with " + what); refused++; }
    total++; assert.strictEqual((await call(api, action, { fig_admin: good }, { origin: "https://evil.example" })).statusCode, 405, action + " cross-origin"); refused++;
    total++; assert.strictEqual((await call(api, action, { fig_admin: good }, { method: "GET" })).statusCode, 405, action + " as GET"); refused++;
  }
  assert.notStrictEqual((await call(api, "data", { fig_admin: good })).statusCode, 401, "a real session gets in (the probe isn't refusing everything)");
  for (const [what, c] of Object.entries(tries)) { const r = await call(page, "", c, { method: "GET" }); assert.ok(!/id="nav"/.test(r.body), "/admin shows the sign-in card with " + what); }
  console.log(`ok: probe: ${refused}/${total} refused across ${actions.length - open.length} signed-in actions (no cookie, forged, other secret, expired, old version, cross-origin, GET); /admin shows only the sign-in card`);
  // the set-up QR: module for module the same as the qrcode package's (the app's copy, when it's there; Vercel's build has no app/)
  const qr = require("./qr");
  assert.ok(/^<svg[^>]+viewBox="0 0 53 53"/.test(qr.svg(totp.uri("JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"))), "an otpauth link (111 characters) is a version 7 code (45 modules + border)");
  let ref = null;
  try { ref = require(path.join(__dirname, "../../app/node_modules/qrcode")); } catch { /* not on Vercel */ }
  if (ref) {
    let n = 0;
    for (const text of ["A", "hello world", totp.uri(totp.newSecret()), "x".repeat(150), "y".repeat(210)]) for (let mask = 0; mask < 8; mask++) {
      const mine = qr.make(text, { mask }), theirs = ref.create([{ data: text, mode: "byte" }], { errorCorrectionLevel: "M", version: mine.version, maskPattern: mask });
      for (let r = 0; r < mine.size; r++) for (let c = 0; c < mine.size; c++) assert.strictEqual(mine.dark[r][c], !!theirs.modules.get(r, c), "QR v" + mine.version + " mask " + mask + " at " + r + "," + c);
      if (mask === 0) assert.strictEqual(qr.make(text).mask, ref.create([{ data: text, mode: "byte" }], { errorCorrectionLevel: "M", version: mine.version }).maskPattern, "the same mask choice");
      n++;
    }
    console.log("ok: QR codes match the qrcode package module for module (" + n + " codes, versions 1-10, all 8 masks)");
  }
  console.log("ok: admin auth");
})().catch((e) => { console.error(e); process.exit(1); });
