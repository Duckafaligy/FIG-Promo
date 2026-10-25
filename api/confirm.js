// /confirm?e=<email>&t=<token> (also /api/confirm): the link in the waitlist's confirmation email (double opt-in, 2026-10-25). Works signed out.
// GET shows one button, so a mail scanner or a link preview opening the link can't confirm anyone for them; POST confirms. Only a valid token
// (the "confirm" token for that address, made with the same secret as the unsubscribe links) changes anything, through the database call
// confirm_waitlist, which also checks the address really ticked the consent box. The page answers the same for a wrong link and for an address
// that is not on the list, so nobody can probe the list. Wrong tokens are rate limited like the unsubscribe page.
const { send } = require("./_lib/auth");
const unsub = require("./_lib/unsub");
const db = require("./_lib/db");
const { esc, page, limiter } = require("./_lib/page");

const tooMany = limiter(30);
const SORRY = page("This link doesn't work", `<h1>This link doesn't work</h1><p>It may be old or copied wrong. You can join the list again on <a href="/">www.figpromo.ca</a>, and we'll send a new one.</p>`);

module.exports = async (req, res) => {
  res.setHeader("Referrer-Policy", "no-referrer");
  const q = new URL(req.url, "https://fig.invalid").searchParams;
  const email = String(q.get("e") || "").slice(0, 254), t = String(q.get("t") || "").slice(0, 64);
  const shown = /^[^\s@<>"'`]{1,64}@[^\s@<>"'`]{1,190}\.[A-Za-z]{2,24}$/.test(email) ? email : "this address";
  const good = unsub.validFor("confirm", email, t);
  if (req.method === "POST") {
    if (!good) return tooMany(req) ? send(res, 429, page("Too many tries", "<h1>Too many tries</h1><p>Try again in an hour.</p>")) : send(res, 200, SORRY);
    let said = "unknown";
    try { said = await db.confirmWaitlist(email); } catch { return send(res, 200, page("Try again", "<h1>Something went wrong</h1><p>Try the link again in a minute.</p>")); }
    if (said === "unknown") return send(res, 200, SORRY);
    return send(res, 200, page("Confirmed", `<h1>You're on the list</h1><p>${esc(shown)} is confirmed. We'll email you once, the day FIG opens to diners in Markham.</p>`));
  }
  if (req.method !== "GET" && req.method !== "HEAD") return send(res, 405, page("Not allowed", "<h1>Not allowed</h1>"));
  if (!good) return send(res, 200, SORRY);
  return send(res, 200, page("Confirm your email", `<h1>Confirm your email</h1><p>One tap, and ${esc(shown)} is on the FIG list.</p>` +
    `<form method="post" action="/confirm?e=${encodeURIComponent(email)}&amp;t=${encodeURIComponent(t)}"><button type="submit">Confirm my email</button></form>`));
};
