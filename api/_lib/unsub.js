// The waitlist emails' unsubscribe links (FIX-LIST #103): /api/unsubscribe?e=<email>&t=<token>, the token an HMAC over
// "unsub:" + the email, keyed by its own key derived from a secret (so it can't stand in for a session signature).
// The secret is UNSUB_SECRET (REVIEW 2026-10-24 E9: its own, so these links don't hang on the removed admin's session secret);
// until that is set, SESSION_SECRET, which the links already sent were signed with. A token is accepted under either, so setting
// UNSUB_SECRET later never breaks a link that is already in someone's inbox; to retire SESSION_SECRET too, set UNSUB_SECRET to its
// value first. With neither set nothing is valid: the page then still answers the same, and the admin's Unsubscribe (or a message
// to FIG) does it by hand.
const crypto = require("crypto");

const secrets = () => [process.env.UNSUB_SECRET, process.env.SESSION_SECRET].filter(Boolean);
const key = (secret) => crypto.createHmac("sha256", secret).update("fig-unsubscribe-v1").digest();
const clean = (email) => String(email || "").trim().toLowerCase();
/** The token for an email, from the first secret that is set (or an empty one: it then never validates): 32 url-safe characters. */
const token = (email, secret = secrets()[0] || "") => crypto.createHmac("sha256", key(secret)).update("unsub:" + clean(email)).digest("base64url").slice(0, 32);
/** True only for this email's own token (and never without a secret). */
function valid(email, t) {
  if (!clean(email)) return false;
  const got = Buffer.from(String(t || ""));
  return secrets().some((secret) => { const want = Buffer.from(token(email, secret)); return want.length === got.length && crypto.timingSafeEqual(want, got); });
}
/** The link for one person, on this site. */
const link = (site, email) => site + "/api/unsubscribe?e=" + encodeURIComponent(clean(email)) + "&t=" + token(email);

module.exports = { token, valid, link };
