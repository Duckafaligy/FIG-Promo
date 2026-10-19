// The admin's second step (FIX-LIST #83, the user chose an authenticator app): TOTP as in RFC 6238 (HMAC-SHA1, 6 digits,
// 30-second steps, one step either side for a phone's clock), Node's crypto only. The secret is base32 (what the apps take).
const crypto = require("crypto");

const STEP = 30, DIGITS = 6, B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

function base32(buf) {
  let bits = 0, val = 0, out = "";
  for (const b of buf) {
    val = (val << 8) | b; bits += 8;
    while (bits >= 5) { out += B32[(val >>> (bits - 5)) & 31]; bits -= 5; }
  }
  return bits ? out + B32[(val << (5 - bits)) & 31] : out;
}
function unbase32(s) {
  let bits = 0, val = 0;
  const out = [];
  for (const ch of String(s).toUpperCase().replace(/[\s=-]/g, "")) {
    const i = B32.indexOf(ch);
    if (i < 0) return null;
    val = (val << 5) | i; bits += 5;
    if (bits >= 8) { out.push((val >>> (bits - 8)) & 255); bits -= 8; }
  }
  return Buffer.from(out);
}

/** The code for one 30-second step (RFC 4226's truncation). */
function codeAt(key, step) {
  const msg = Buffer.alloc(8);
  msg.writeBigUInt64BE(BigInt(step));
  const h = crypto.createHmac("sha1", key).update(msg).digest();
  const o = h[h.length - 1] & 15;
  const n = ((h[o] & 127) << 24) | (h[o + 1] << 16) | (h[o + 2] << 8) | h[o + 3];
  return String(n % 10 ** DIGITS).padStart(DIGITS, "0");
}

/** The step a typed code matches (now, or one either side), or null. Compares in constant time. */
function matchStep(secret, code, now = Date.now()) {
  const key = unbase32(secret);
  const got = Buffer.from(String(code || "").replace(/\s/g, ""));
  if (!key || !key.length || got.length !== DIGITS) return null;
  const t = Math.floor(now / 1000 / STEP);
  let hit = null;
  for (const s of [t - 1, t, t + 1]) if (crypto.timingSafeEqual(Buffer.from(codeAt(key, s)), got) && hit === null) hit = s;
  return hit;
}

const newSecret = () => base32(crypto.randomBytes(20)); // 160 bits, as RFC 4226 recommends
const uri = (secret) => `otpauth://totp/FIG%20Admin?secret=${secret}&issuer=FIG&algorithm=SHA1&digits=${DIGITS}&period=${STEP}`;

// backup codes: 8 one-time codes like "k3m9-x2qp-7d", shown once; only their SHA-256 is kept (they're random, so no salt needed)
const backupCodes = () => Array.from({ length: 8 }, () => {
  const s = Array.from(crypto.randomBytes(10), (b) => "abcdefghjkmnpqrstuvwxyz23456789"[b % 31]).join("");
  return `${s.slice(0, 4)}-${s.slice(4, 8)}-${s.slice(8)}`;
});
const hashBackup = (code) => crypto.createHash("sha256").update(String(code).toLowerCase().replace(/[^a-z0-9]/g, "")).digest("hex");
const looksBackup = (code) => /^[a-z0-9]{4}-?[a-z0-9]{4}-?[a-z0-9]{2}$/i.test(String(code || "").trim());

module.exports = { base32, unbase32, codeAt, matchStep, newSecret, uri, backupCodes, hashBackup, looksBackup, STEP };
