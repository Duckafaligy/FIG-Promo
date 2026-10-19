// /api/admin-api?do=login|login-code|twostep-set|login-send|enrol-start|enrol-code|enrol-contact|enrol-contact-ok|enrol-done|logout|logout-all|second-get|data|charts|restaurant-get|person-get|ad-campaign|ad-account|premium|support|support-remove|waitlist-unsubscribe|waitlist-remove|two-step-off|ad-invoices|ad-invoice|blog-list|blog-set|agreed-csv|sources-get|qr|diners-get|diners-set|founding-cap|founding-until|opens-at|prospects-list|prospects-set  (POST, same origin; everything but login needs the session)
const { setTwoStep, resetLeftOn, login, loginCode, sendLoginCode, signedIn, logoutCookie, logoutEverywhere, enrolStart, enrolCode, enrolContact, enrolContactOk, enrolDone, secondState, send, readJson, sameOrigin } = require("./_lib/auth");
const qr = require("./_lib/qr");
const db = require("./_lib/db");
const blog = require("./_lib/blog");
const unsub = require("./_lib/unsub");

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
  // the second step and its set-up (FIX-LIST #103): before a session too; each checks the password step's cookie (or a session) itself
  const out2 = action === "login-send" ? await sendLoginCode(req, body.via)
    : action === "enrol-start" ? await enrolStart(req, body.code)
    : action === "enrol-code" ? await enrolCode(req, body.code)
    : action === "enrol-contact" ? await enrolContact(req, body.via, body.to)
    : action === "enrol-contact-ok" ? await enrolContactOk(req, body.code)
    : action === "enrol-done" ? await enrolDone(req, body.saved)
    : null;
  if (out2) {
    if (action === "enrol-start" && out2.status === 200) out2.body.qr = qr.svg(out2.body.uri);
    return send(res, out2.status, out2.body, out2.headers || []);
  }
  if (!(await signedIn(req))) return send(res, 401, { error: "Sign in again." });
  // everything below re-checks the session on the server, every time (FIX-LIST #83)
  if (action === "logout-all") {
    try { return send(res, 200, { ok: true }, await logoutEverywhere()); } catch { return send(res, 502, { error: "The database didn't answer, so nothing changed. Try again." }); }
  }
  if (action === "second-get") return send(res, 200, { ok: true, ...(await secondState()) });
  // "Require a code at every sign-in" (FIX-LIST #103 DESIGN): signed in (checked above and again inside), and always with a code
  if (action === "twostep-set") { await new Promise((r) => setTimeout(r, 400)); const o = await setTwoStep(req, body.on, body.code); return send(res, o.status, o.body, o.headers || []); }

  try {
    if (action === "data") return send(res, 200, { totp: true, resetLeftOn: await resetLeftOn(), ...(db.connected() ? { connected: true, ...(await db.overview()) } : { connected: false }) });
    if (!db.connected()) return send(res, 409, { error: "The database isn't connected yet." });
    // the charts and detail panels (FIX-LIST #85): reads only; ids are checked as uuids in db.js
    if (action === "charts") return send(res, 200, { ok: true, ...(await db.charts()) });
    if (action === "restaurant-get") return send(res, 200, { ok: true, ...(await db.restaurantDetail(body.id)) });
    if (action === "person-get") return send(res, 200, { ok: true, ...(await db.personDetail(body.id)) });
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
    // who agreed, each with their own unsubscribe link: the launch email is sent by hand, mail-merge style (FIX-LIST #103)
    if (action === "agreed-csv") { const site = "https://" + String(req.headers.host || ""); return send(res, 200, { ok: true, rows: (await db.agreedEmails()).map((e) => ({ email: e, unsubscribe: unsub.link(site, e) })) }); }
    if (action === "sources-get") return send(res, 200, { ok: true, ...(await db.sources()) });
    // a tracking link's QR (FIX-LIST #105): only this site's own ?src= links, classic black with FIG's tile
    if (action === "qr") {
      const url = String(body.url || ""), site = "https://" + String(req.headers.host || "");
      if (url.length > 120 || !(url.startsWith(site + "/?src=") || url.startsWith(site + "/app?src=")) || !/[?]src=[a-z0-9_-]{1,40}(#waitlist)?$/.test(url)) throw new Error("bad link");
      return send(res, 200, { ok: true, svg: qr.svg(url, 240, { tile: true, label: "QR code for " + url }) });
    }
    if (action === "diners-get") return send(res, 200, { ok: true, ...(await db.dinersState()) });
    if (action === "diners-set") return send(res, 200, { ok: true, ...(await db.setDinersMode(body.mode || (body.open === true ? "on" : body.open === false ? "off" : ""))) });
    if (action === "founding-cap") return send(res, 200, { ok: true, ...(await db.setFoundingCap(body.cap)) });
    if (action === "opens-at") return send(res, 200, { ok: true, ...(await db.setOpensAt(body.at === null ? null : String(body.at || ""))) });
    if (action === "founding-until") return send(res, 200, { ok: true, ...(await db.setFoundingUntil(body.until === null ? null : "now")) });
    if (action === "ad-invoice") { await db.setInvoice(body.id, body.status); return send(res, 200, { ok: true }); }
    // the founding pre-sale (FIX-LIST #141): the plans, the switch, start billing, refunds (the Stripe work is the presale-admin function's)
    if (action === "presale-get") return send(res, 200, { ok: true, ...(await db.presaleState()) });
    if (action === "presale-switch") return send(res, 200, { ok: true, ...(await db.setPresaleOn(body.on)) });
    if (action === "presale-start") return send(res, 200, { ok: true, ...(await db.presaleStart(body.at)) });
    if (action === "presale-refund") return send(res, 200, { ok: true, ...(await db.presaleRefund(body.restaurant, body.force)) });
    if (action === "presale-refund-all") return send(res, 200, { ok: true, ...(await db.presaleRefundAll()) });
  } catch (e) {
    // validation, not a database problem; the cap says what it takes (FIX-LIST #105)
    if (/^bad /.test(String(e.message))) return send(res, 400, { error: e.message === "bad cap" ? "Type a whole number from 1 to 1,000,000, or leave it empty for everyone."
      : e.message === "bad presale-not-ready" ? "The founding offer isn't ready: the presale functions must be deployed and the four live prices set first." : "That was not a valid request." });
    return send(res, 502, { error: "The database didn't answer. Try again." });
  }
  return send(res, 400, { error: "Unknown action." });
};
