// node api/_lib/check.js  -- checks the admin lock schedule, cookie signing and password hashing
const assert = require("assert");
const crypto = require("crypto");
process.env.SESSION_SECRET = "test-secret";
const salt = crypto.randomBytes(16);
process.env.ADMIN_PASSWORD_HASH = "scrypt:" + salt.toString("hex") + ":" + crypto.scryptSync("right", salt, 32).toString("hex");
const { login, _test } = require("./auth");

assert.strictEqual(_test.lockFor(4), 0);
assert.strictEqual(_test.lockFor(5), 60_000);
assert.strictEqual(_test.lockFor(6), 300_000);
assert.strictEqual(_test.lockFor(8), 3_600_000);
assert.strictEqual(_test.lockFor(20), 3_600_000);
assert.deepStrictEqual(_test.open(_test.seal({ a: 1 })), { a: 1 });
assert.strictEqual(_test.open(_test.seal({ a: 1 }).replace(/.$/, "x")), null);
assert.strictEqual(_test.passwordOk("right"), true);
assert.strictEqual(_test.passwordOk("wrong"), false);

const req = { headers: { "x-forwarded-for": "1.2.3.4" } };
for (let i = 1; i <= 4; i++) assert.strictEqual(login(req, "nope").status, 401);
const fifth = login(req, "nope");
assert.ok(fifth.body.locked && fifth.body.retryIn === 60, "locked for a minute after 5 misses");
assert.strictEqual(login(req, "right").status, 429, "even the right password waits out the lock");
console.log("ok: admin auth");
