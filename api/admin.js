// /admin (rewritten here): the sign-in card, or the admin app once signed in. The admin HTML is only ever sent to a
// signed-in browser; nothing about it ships with the public site.
const crypto = require("crypto");
const { signedIn, send } = require("./_lib/auth");
const { signInPage, appPage } = require("./_lib/pages");

// FIX-LIST #160: a fresh nonce on every response, so only the page's own two scripts run here (no 'unsafe-inline' for scripts).
// The site-wide policy from vercel.json still comes too, and a browser enforces both, so this only ever narrows it.
const policy = (nonce) => ["default-src 'self'", `script-src 'nonce-${nonce}'`, "style-src 'self' 'unsafe-inline'", "img-src 'self' data: blob:",
  "connect-src 'self'", "frame-src 'self'", "frame-ancestors 'none'", "base-uri 'none'", "form-action 'self'", "object-src 'none'"].join("; ");

module.exports = async (req, res) => {
  const nonce = crypto.randomBytes(16).toString("base64");
  res.setHeader("Content-Security-Policy", policy(nonce));
  res.setHeader("Cross-Origin-Opener-Policy", "same-origin"); // no other site's window keeps a handle on this one (FIX-LIST #160 e)
  return send(res, 200, (await signedIn(req)) ? appPage(nonce) : signInPage(nonce));
};
module.exports.policy = policy;
