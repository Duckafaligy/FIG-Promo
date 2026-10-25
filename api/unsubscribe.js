// /unsubscribe?e=<email>&t=<token> (also /api/unsubscribe): stop FIG's marketing emails to one address. Works signed out.
// GET shows one button (so a mail scanner opening the link doesn't unsubscribe anyone); POST does it, and a mail app's one-click
// unsubscribe (RFC 8058: the List-Unsubscribe-Post header, "List-Unsubscribe=One-Click") posts to the same link. Only a valid token changes anything:
// the address goes on the do-not-email list (email_suppressions, reason unsubscribed), the waitlist row loses its consent, and the account with that
// address stops getting marketing email, all in one database call (unsubscribe_address). Emails you ask for (codes, order updates) keep coming.
// The page answers the same for any address or token, so nobody can probe who's on the list.
// Rate limit (REVIEW 2026-10-24 E9): only a WRONG token counts, 30 an hour per address, and past that a wrong token gets a 429. A right
// token is always honoured and never counted, so a mail provider's one-click requests (many people, one address) are not dropped.
// The link carries the email and token, so the page sends no referrer: "Join the list again" must not hand them to Home and its analytics.
const { send } = require("./_lib/auth");
const unsub = require("./_lib/unsub");
const db = require("./_lib/db");
const { esc, page, limiter } = require("./_lib/page");

const tooMany = limiter(30);

module.exports = async (req, res) => {
  res.setHeader("Referrer-Policy", "no-referrer");
  const q = new URL(req.url, "https://fig.invalid").searchParams;
  const email = String(q.get("e") || "").slice(0, 254), t = String(q.get("t") || "").slice(0, 64);
  // the page repeats the address only when it looks like one, so a crafted link can't put any words it likes on FIG's page (#172)
  const shown = /^[^\s@<>"'`]{1,64}@[^\s@<>"'`]{1,190}\.[A-Za-z]{2,24}$/.test(email) ? email : "this address";
  if (req.method === "POST") {
    if (unsub.valid(email, t)) {
      // (the source is only a note for FIG: a mail app's one-click request is a POST with no page behind it)
      const source = String(req.headers["content-type"] || "").includes("x-www-form-urlencoded") && !String(req.headers["sec-fetch-mode"] || "") ? "one-click" : "link";
      try { await db.unsubscribeAddress(email, source); } catch { /* the same answer; FIG can do it by hand */ }
    } else if (tooMany(req)) {
      return send(res, 429, page("Too many tries", "<h1>Too many tries</h1><p>Try again in an hour.</p>"));
    }
    return send(res, 200, page("Unsubscribed", `<h1>You're unsubscribed</h1><p>FIG won't send ${esc(shown)} marketing emails again. You'll still get the emails you ask for, like sign-in codes and order updates. Changed your mind? Join the list again on <a href="/">www.figpromo.ca</a>.</p>`));
  }
  if (req.method !== "GET" && req.method !== "HEAD") return send(res, 405, page("Not allowed", "<h1>Not allowed</h1>"));
  return send(res, 200, page("Unsubscribe", `<h1>Stop FIG's marketing emails?</h1><p>FIG won't send ${esc(shown)} marketing emails again. You'll still get the emails you ask for, like sign-in codes and order updates.</p>` +
    `<form method="post" action="/unsubscribe?e=${encodeURIComponent(shown === email ? email : "")}&amp;t=${encodeURIComponent(t)}"><button type="submit">Unsubscribe</button></form>`));
};
