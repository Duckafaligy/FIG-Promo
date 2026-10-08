// /api/admin-api?do=login|logout|data|ad-campaign|ad-account|premium|ad-invoices|ad-invoice|decide-dispute|lift-takeout  (POST, same origin; everything but login needs the session)
const { login, signedIn, logoutCookie, send, readJson, sameOrigin } = require("./_lib/auth");
const db = require("./_lib/db");

module.exports = async (req, res) => {
  if (req.method !== "POST" || !sameOrigin(req)) return send(res, 405, { error: "Not allowed." });
  const action = new URL(req.url, "http://x").searchParams.get("do");
  const body = await readJson(req);

  if (action === "login") {
    // a short pause on every try slows guessing even before the lock
    await new Promise((r) => setTimeout(r, 400));
    const out = login(req, body.password);
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
    if (action === "ad-invoices") { await db.makeInvoices(body.month); return send(res, 200, { ok: true }); }
    if (action === "ad-invoice") { await db.setInvoice(body.id, body.status); return send(res, 200, { ok: true }); }
    if (action === "lift-takeout") { await db.liftTakeout(body.id); return send(res, 200, { ok: true }); }
    if (action === "decide-dispute") {
      try { await db.decideDispute(body.id, body.upheld, body.note); } catch { return send(res, 409, { error: "Already decided, or not found." }); }
      return send(res, 200, { ok: true });
    }
  } catch (e) {
    return send(res, 502, { error: "The database didn't answer. Try again." });
  }
  return send(res, 400, { error: "Unknown action." });
};
