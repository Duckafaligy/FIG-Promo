// The waitlist emails' unsubscribe links (FIX-LIST #103): /api/unsubscribe?e=<email>&t=<token>, the token an HMAC over
// "unsub:" + the email, keyed by its own key derived from SESSION_SECRET (so it can't stand in for a session signature).
// If SESSION_SECRET ever changes, old links stop working: the page then still answers the same, and the admin's Unsubscribe
// (or a message to FIG) does it by hand.
const crypto = require("crypto");

const key = () => crypto.createHmac("sha256", process.env.SESSION_SECRET || "").update("fig-unsubscribe-v1").digest();
const clean = (email) => String(email || "").trim().toLowerCase();
/** The token for an email: 32 url-safe characters. */
const token = (email) => crypto.createHmac("sha256", key()).update("unsub:" + clean(email)).digest("base64url").slice(0, 32);
/** True only for this email's own token (and never without a secret). */
function valid(email, t) {
  if (!process.env.SESSION_SECRET || !clean(email)) return false;
  const want = Buffer.from(token(email)), got = Buffer.from(String(t || ""));
  return want.length === got.length && crypto.timingSafeEqual(want, got);
}
/** The link for one person, on this site. */
const link = (site, email) => site + "/api/unsubscribe?e=" + encodeURIComponent(clean(email)) + "&t=" + token(email);

module.exports = { token, valid, link };
