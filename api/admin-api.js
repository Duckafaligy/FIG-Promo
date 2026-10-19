// /api/admin-api?do=login|login-code|logout|logout-all|totp-start|totp-confirm|data|ad-campaign|ad-account|premium|support|support-remove|waitlist-unsubscribe|waitlist-remove|two-step-off|ad-invoices|ad-invoice|blog-list|blog-set|diners-get|diners-set|founding-cap|founding-until|opens-at|prospects-list|prospects-set  (POST, same origin; everything but login needs the session)
const { login, loginCode, signedIn, logoutCookie, logoutEverywhere, enrolStart, enrolConfirm, send, readJson, sameOrigin } = require("./_lib/auth");
const qr = require("./_lib/qr");
const db = require("./_lib/db");
const blog = require("./_lib/blog");

module.exports = async (req, res) => {
  if (req.method !== "POST" || !sameOrigin(req)) return send(res, 405, { error: "Not allowed." });
  const action = new URL(req.url, "http://x").searchParams.get("do");
  const body = await readJson(req);

  if (action === "login") {
    // a short pause on every try slows guessing even before the lock
    await new Promise((r) => setTimeout(r, 400));
    const out = await login(req, body.password);
    return send(res, out.status, out.body, out.headers || []);
  }
  if (action === "login-code") {
    await new Promise((r) => setTimeout(r, 400));
    const out = await loginCode(req, body.code);
    return send(res, out.status, out.body, out.headers || []);
  }
  if (action === "logout") return send(res, 200, { ok: true }, [logoutCookie()]);
  if (!(await signedIn(req))) return send(res, 401, { error: "Sign in again." });
  // everything below re-checks the session on the server, every time (FIX-LIST #83)
  if (action === "logout-all") {
    try { return send(res, 200, { ok: true }, await logoutEverywhere()); } catch { return send(res, 502, { error: "The database didn't answer, so nothing changed. Try again." }); }
  }
  if (action === "totp-start") { const e = enrolStart(); return send(res, 200, { ok: true, on: !!process.env.ADMIN_TOTP_SECRET, secret: e.secret, qr: qr.svg(e.uri) }, [e.cookie]); }
  if (action === "totp-confirm") { const out = await enrolConfirm(req, body.code); return send(res, out.status, out.body, out.headers || []); }

  try {
    if (action === "data") return send(res, 200, { totp: !!process.env.ADMIN_TOTP_SECRET, ...(db.connected() ? { connected: true, ...(await db.overview()) } : { connected: false }) });
    if (!db.connected()) return send(res, 409, { error: "The database isn't connected yet." });
    if (action === "ad-campaign") { await db.setCampaign(body.id, !!body.stop, body.note); return send(res, 200, { ok: true }); }
    if (action === "ad-account") { await db.setAccount(body.owner, body.limit ?? null, body.held ?? null); return send(res, 200, { ok: true }); }
    if (action === "premium") { await db.setPremium(body.owner, body.years ?? 0); return send(res, 200, { ok: true }); }
    if (action === "support") { await db.setSupport(body.id, body.status); return send(res, 200, { ok: true }); }
    // requests to stop the emails or to be forgotten (FIX-LIST #95): writes, so only behind the session check above
    if (action === "waitlist-unsubscribe") return send(res, 200, { ok: true, ...(await db.waitlistUnsubscribe(body.email)) });
    if (action === "waitlist-remove") return send(res, 200, { ok: true, ...(await db.waitlistRemove(body.email)) });
    if (action === "support-remove") return send(res, 200, { ok: true, ...(await db.supportRemove(body.id)) });
    if (action === "two-step-off") return send(res, 200, { ok: true, ...(await db.twoStepOff({ id: body.id, email: body.email })) });
    if (action === "ad-invoices") { await db.makeInvoices(body.month); return send(res, 200, { ok: true }); }
    if (action === "blog-list") return send(res, 200, { ok: true, ...(await blog.list()) });
    if (action === "blog-set") { const r = await db.setBlog(body.slug, { ...(body.hidden !== undefined ? { hidden: body.hidden } : {}), ...(body.publish_at !== undefined ? { publish_at: body.publish_at } : {}), ...(body.note !== undefined ? { note: body.note } : {}) }); return send(res, 200, { ok: true, ...r }); }
    if (action === "prospects-list") return send(res, 200, { ok: true, ...(await db.prospects(body)) });
    if (action === "prospects-set") return send(res, 200, { ok: true, ...(await db.setProspect(body.id, body)) });
    if (action === "diners-get") return send(res, 200, { ok: true, ...(await db.dinersState()) });
    if (action === "diners-set") return send(res, 200, { ok: true, ...(await db.setDinersMode(body.mode || (body.open === true ? "on" : body.open === false ? "off" : ""))) });
    if (action === "founding-cap") return send(res, 200, { ok: true, ...(await db.setFoundingCap(body.cap)) });
    if (action === "opens-at") return send(res, 200, { ok: true, ...(await db.setOpensAt(body.at === null ? null : String(body.at || ""))) });
    if (action === "founding-until") return send(res, 200, { ok: true, ...(await db.setFoundingUntil(body.until === null ? null : "now")) });
    if (action === "ad-invoice") { await db.setInvoice(body.id, body.status); return send(res, 200, { ok: true }); }
  } catch (e) {
    // validation, not a database problem; the cap says what it takes (FIX-LIST #105)
    if (/^bad /.test(String(e.message))) return send(res, 400, { error: e.message === "bad cap" ? "Type a whole number from 1 to 1,000,000, or leave it empty for everyone." : "That was not a valid request." });
    return send(res, 502, { error: "The database didn't answer. Try again." });
  }
  return send(res, 400, { error: "Unknown action." });
};
