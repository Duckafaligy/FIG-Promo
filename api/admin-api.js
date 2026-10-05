// /api/admin-api?do=login|logout|data|make-keys|delete-key|make-plan-codes|delete-plan-code  (POST, same origin; everything but login needs the session)
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
    if (action === "make-keys") return send(res, 200, { codes: await db.makeKeys(body.count, body.uses, body.note) });
    if (action === "delete-key") { await db.deleteKey(String(body.code || "")); return send(res, 200, { ok: true }); }
    if (action === "make-plan-codes") return send(res, 200, { codes: await db.makePlanCodes(body.count, body.note) });
    if (action === "delete-plan-code") { await db.deletePlanCode(String(body.code || "")); return send(res, 200, { ok: true }); }
  } catch (e) {
    return send(res, 502, { error: "The database didn't answer. Try again." });
  }
  return send(res, 400, { error: "Unknown action." });
};
