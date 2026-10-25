// The little result pages of the email links (/unsubscribe, /confirm): one card in the site's colours, light and dark, no scripts, no referrer.
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const ip = (req) => String(req.headers["x-real-ip"] || req.headers["x-vercel-forwarded-for"] || "?").split(",")[0].trim();

function page(title, body) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><meta name="referrer" content="no-referrer"><title>${esc(title)} · FIG</title>
<style>body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;background:#F5F7FB;color:#0A1020}main{max-width:460px;margin:12vh auto;padding:28px;background:#fff;border-radius:20px;box-shadow:0 10px 40px rgba(10,16,32,.08)}
h1{font-size:24px;margin:0 0 8px}p{color:#4A5568;margin:0 0 18px}button{font:inherit;font-weight:700;border:0;border-radius:99px;padding:12px 22px;background:#1E5EFF;color:#fff;cursor:pointer}a{color:#1E5EFF}
@media (prefers-color-scheme:dark){body{background:#0E1116;color:#F2F4F7}main{background:#171B22}p{color:#A6B0C3}}</style></head>
<body><main>${body}</main></body></html>`;
}

/** Per server instance: wrong tokens per address and hour (a right token is never counted), enough to stop a flood from one address. */
function limiter(max = 30) {
  const tries = new Map(); // ip -> { n, since }
  return (req) => {
    const now = Date.now(), who = ip(req), r = tries.get(who);
    const n = r && now - r.since < 3_600_000 ? r.n + 1 : 1;
    tries.set(who, { n, since: r && n > 1 ? r.since : now });
    return n > max;
  };
}

module.exports = { esc, page, limiter };
