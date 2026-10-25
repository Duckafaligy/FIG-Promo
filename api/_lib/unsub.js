// The signed links in FIG's emails: /unsubscribe?e=<email>&t=<token> (FIX-LIST #103) and /confirm?e=<email>&t=<token> (2026-10-25, the waitlist's
// double opt-in). The token is an HMAC over "<purpose>:" + the email, keyed by its own key derived from a secret (so it can't stand in for a
// session signature). Purposes never validate each other. The Supabase mail function (supabase/functions/_shared/mailtoken.ts) makes the SAME
// tokens from the same secret; site/scripts/check.js and the app's scripts/check-emails.mjs both assert the same test vector.
// The secret is UNSUB_SECRET (its own, so these links don't hang on the removed admin's session secret); set the SAME value as a Supabase function secret.
// Until it is set, SESSION_SECRET, which the links already sent were signed with. A token is accepted under either, so setting
// UNSUB_SECRET later never breaks a link that is already in someone's inbox; to retire SESSION_SECRET too, set UNSUB_SECRET to its
// value first. With neither set nothing is valid: the page then still answers the same, and a message to FIG does it by hand.
const crypto = require("crypto");

const secrets = () => [process.env.UNSUB_SECRET, process.env.SESSION_SECRET].filter(Boolean);
const key = (secret) => crypto.createHmac("sha256", secret).update("fig-unsubscribe-v1").digest();
const clean = (email) => String(email || "").trim().toLowerCase();
/** The token for an email and purpose ("unsub" | "confirm"), from the first secret that is set (or an empty one: it then never validates): 32 url-safe characters. */
const tokenFor = (purpose, email, secret = secrets()[0] || "") => crypto.createHmac("sha256", key(secret)).update(purpose + ":" + clean(email)).digest("base64url").slice(0, 32);
/** True only for this email's own token for this purpose (and never without a secret). */
function validFor(purpose, email, t) {
  if (!clean(email)) return false;
  const got = Buffer.from(String(t || ""));
  return secrets().some((secret) => { const want = Buffer.from(tokenFor(purpose, email, secret)); return want.length === got.length && crypto.timingSafeEqual(want, got); });
}
const token = (email, secret) => tokenFor("unsub", email, secret);
const valid = (email, t) => validFor("unsub", email, t);
/** The link for one person, on this site. */
const link = (site, email) => site + "/unsubscribe?e=" + encodeURIComponent(clean(email)) + "&t=" + token(email);

module.exports = { token, valid, link, tokenFor, validFor, clean };
