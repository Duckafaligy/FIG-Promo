// /api/admin-api?do=login|logout|data|ad-campaign|ad-account|premium|support|two-step-off|ad-invoices|ad-invoice|blog-list|blog-set|diners-get|diners-set|founding-cap|founding-until|opens-at|prospects-list|prospects-set  (POST, same origin; everything but login needs the session)
const { login, signedIn, logoutCookie, send, readJson, sameOrigin } = require("./_lib/auth");
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
  if (action === "logout") return send(res, 200, { ok: true }, [logoutCookie()]);
  if (!signedIn(req)) return send(res, 401, { error: "Sign in again." });

  try {
    if (action === "data") return send(res, 200, db.connected() ? { connected: true, ...(await db.overview()) } : { connected: false });
    if (!db.connected()) return send(res, 409, { error: "The database isn't connected yet." });
    if (action === "ad-campaign") { await db.setCampaign(body.id, !!body.stop, body.note); return send(res, 200, { ok: true }); }
    if (action === "ad-account") { await db.setAccount(body.owner, body.limit ?? null, body.held ?? null); return send(res, 200, { ok: true }); }
    if (action === "premium") { await db.setPremium(body.owner, body.years ?? 0); return send(res, 200, { ok: true }); }
    if (action === "support") { await db.setSupport(body.id, body.status); return send(res, 200, { ok: true }); }
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
    if (/^bad /.test(String(e.message))) return send(res, 400, { error: "That was not a valid request." }); // validation, not a database problem
    return send(res, 502, { error: "The database didn't answer. Try again." });
  }
  return send(res, 400, { error: "Unknown action." });
};
