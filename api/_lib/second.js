// The admin's second step, always on (FIX-LIST #103, the user 2026-10-19): what auth.js needs besides TOTP.
// - the authenticator's secret is kept in settings, encrypted (AES-256-GCM) with a key derived from SESSION_SECRET under its own
//   label, so no agent ever sets an env var for it; ADMIN_TOTP_SECRET still overrides it. If SESSION_SECRET changes, the stored
//   secret can't be read: the user's reset flag (ADMIN_TOTP_RESET=1 in Vercel) is the way back.
// - "Email me a code instead" (Resend): one fixed address
//   or number, saved at set-up after a code sent to it proves it; 6 digits, 10 minutes, one use, only a hash kept.
const crypto = require("crypto");

const key = () => crypto.createHmac("sha256", process.env.SESSION_SECRET || "").update("fig-admin-totp-key-v1").digest();
/** Encrypted text for the database: "v1:" + iv, tag and ciphertext. */
function encrypt(text) {
  const iv = crypto.randomBytes(12), c = crypto.createCipheriv("aes-256-gcm", key(), iv);
  const enc = Buffer.concat([c.update(String(text), "utf8"), c.final()]);
  return "v1:" + Buffer.concat([iv, c.getAuthTag(), enc]).toString("base64url");
}
/** The text back, or null if it can't be read (another key, or tampered with). */
function decrypt(blob) {
  try {
    const b = Buffer.from(String(blob).replace(/^v1:/, ""), "base64url");
    const d = crypto.createDecipheriv("aes-256-gcm", key(), b.subarray(0, 12));
    d.setAuthTag(b.subarray(12, 28));
    return Buffer.concat([d.update(b.subarray(28)), d.final()]).toString("utf8");
  } catch { return null; }
}

// a real sender only: onboarding@resend.dev can only reach the Resend account's own address
const mailOn = () => !!(process.env.RESEND_API_KEY && process.env.RESEND_FROM) && !/@resend\.dev\b/i.test(process.env.RESEND_FROM);
const textOn = () => false; // no Twilio: FIG sends no texts (the owner 2026-10-25); kept so auth.js still loads
const newCode = () => String(crypto.randomInt(0, 1_000_000)).padStart(6, "0");
const hashCode = (code) => crypto.createHash("sha256").update("fig-admin-code:" + String(code).trim()).digest("hex");
const sameHash = (a, b) => typeof a === "string" && typeof b === "string" && a.length === b.length && crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/, PHONE = /^\+[1-9]\d{7,14}$/;
const cleanTo = (via, to) => { const t = String(to || "").trim(); return via === "text" ? (PHONE.test(t.replace(/[\s().-]/g, "")) ? t.replace(/[\s().-]/g, "") : "") : (t.length <= 254 && EMAIL.test(t) ? t.toLowerCase() : ""); };
/** "b•••@gmail.com" / "•••• 4567": enough to know which one, never the whole of it. */
const mask = (via, to) => !to ? "" : via === "text" ? "•••• " + String(to).slice(-4) : String(to).replace(/^(.).*(@.*)$/, "$1•••$2");

/** Sends a code; true if the service took it. */
async function sendCode(via, to, code) {
  const line = `Your FIG Admin code is ${code}. It works once, for 10 minutes. If you didn't just try to sign in, change the admin password.`;
  try {
    if (via === "text") return false; // FIG sends no texts (the owner 2026-10-25): email codes only
    if (!mailOn()) return false;
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST", signal: AbortSignal.timeout(8000),
      headers: { Authorization: "Bearer " + process.env.RESEND_API_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ from: process.env.RESEND_FROM, to: [to], subject: "Your FIG Admin code", text: line }),
    });
    return r.ok;
  } catch { return false; }
}

module.exports = { encrypt, decrypt, mailOn, textOn, newCode, hashCode, sameHash, cleanTo, mask, sendCode };
