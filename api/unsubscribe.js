// /api/unsubscribe?e=<email>&t=<token>: stop FIG's waitlist emails to one address (FIX-LIST #103). Works signed out.
// GET shows one button (so a mail scanner opening the link doesn't unsubscribe anyone); POST does it, and a mail app's one-click
// unsubscribe (RFC 8058, "List-Unsubscribe=One-Click") posts to the same link. Only a valid token changes anything, and only
// consent (false) + unsubscribed_at; the page answers the same for any address or token, so nobody can probe who's on the list.
// Rate-limited per address (30 an hour, then nothing more is done; the answer stays the same).
const { send } = require("./_lib/auth");
const unsub = require("./_lib/unsub");
const db = require("./_lib/db");

const tries = new Map(); // ip -> { n, since }: per server instance; enough to stop a flood from one address
const ip = (req) => String(req.headers["x-real-ip"] || req.headers["x-vercel-forwarded-for"] || "?").split(",")[0].trim();
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

function page(title, body) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>${esc(title)} · FIG</title>
<style>body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;background:#F5F7FB;color:#0A1020}main{max-width:460px;margin:12vh auto;padding:28px;background:#fff;border-radius:20px;box-shadow:0 10px 40px rgba(10,16,32,.08)}
h1{font-size:24px;margin:0 0 8px}p{color:#4A5568;margin:0 0 18px}button{font:inherit;font-weight:700;border:0;border-radius:99px;padding:12px 22px;background:#1E5EFF;color:#fff;cursor:pointer}a{color:#1E5EFF}
@media (prefers-color-scheme:dark){body{background:#0E1116;color:#F2F4F7}main{background:#171B22}p{color:#A6B0C3}}</style></head>
<body><main>${body}</main></body></html>`;
}

module.exports = async (req, res) => {
  const q = new URL(req.url, "https://fig.invalid").searchParams;
  const email = String(q.get("e") || "").slice(0, 254), t = String(q.get("t") || "").slice(0, 64);
  if (req.method === "POST") {
    const now = Date.now(), who = ip(req), r = tries.get(who);
    const n = r && now - r.since < 3_600_000 ? r.n + 1 : 1;
    tries.set(who, { n, since: r && n > 1 ? r.since : now });
    if (n <= 30 && unsub.valid(email, t)) { try { await db.waitlistUnsubscribe(email); } catch { /* the same answer; FIG can do it by hand */ } }
    return send(res, 200, page("Unsubscribed", `<h1>You're unsubscribed</h1><p>FIG won't email ${esc(email || "this address")} about the waitlist again. Changed your mind? Join the list again on <a href="/">fig-promo.vercel.app</a>.</p>`));
  }
  if (req.method !== "GET" && req.method !== "HEAD") return send(res, 405, page("Not allowed", "<h1>Not allowed</h1>"));
  return send(res, 200, page("Unsubscribe", `<h1>Stop FIG's emails?</h1><p>FIG won't email ${esc(email || "this address")} about the waitlist again. You keep your place on the list.</p>` +
    `<form method="post" action="/api/unsubscribe?e=${encodeURIComponent(email)}&amp;t=${encodeURIComponent(t)}"><button type="submit">Unsubscribe</button></form>`));
};
