// Reads FIG's database for the admin page, on the server only. Needs (Vercel environment variables, never in the page):
//   SUPABASE_URL                https://<project>.supabase.co
//   SUPABASE_SERVICE_ROLE_KEY   the service_role key (Supabase → Project Settings → API). It bypasses row security,
//                               so it must only ever live here.
const url = () => (process.env.SUPABASE_URL || "").replace(/\/$/, "");
const key = () => process.env.SUPABASE_SERVICE_ROLE_KEY || "";
const connected = () => !!(url() && key());

async function rest(path, opts = {}) {
  const r = await fetch(`${url()}/rest/v1/${path}`, {
    ...opts,
    headers: { apikey: key(), Authorization: `Bearer ${key()}`, "Content-Type": "application/json", Prefer: "count=exact", ...(opts.headers || {}) },
  });
  if (!r.ok) throw new Error(`${r.status} ${path.split("?")[0]}`);
  const range = r.headers.get("content-range") || "";
  const count = Number(range.split("/")[1]) || 0;
  const text = await r.text();
  return { rows: text ? JSON.parse(text) : [], count };
}
const count = async (path) => (await rest(path + (path.includes("?") ? "&" : "?") + "select=id&limit=1")).count;
const safe = (p, fallback) => p.catch(() => fallback);

// FIX-LIST #85 v2: the admin's charts and detail panels. Read-only. Days are Toronto calendar days ("2026-10-19").
const dayKey = (t) => new Date(t).toLocaleDateString("en-CA", { timeZone: "America/Toronto" });
// ponytail: steps back 24 h from now, so within an hour of midnight on a DST day one date can repeat; fine for a chart
const dayKeys = (n) => Array.from({ length: n }, (_, i) => dayKey(Date.now() - (n - 1 - i) * 86400000));
function bucketer(keys) {
  const at = new Map(keys.map((k, i) => [k, i]));
  return (rows, col, val) => {
    const out = new Array(keys.length).fill(0);
    for (const r of rows) { const i = at.get(dayKey(r[col])); if (i !== undefined) out[i] += val ? Number(r[val]) || 0 : 1; }
    return out.map((v) => Math.round(v * 100) / 100);
  };
}
// the end of a deal, from what's stored: when it was ended, a flash deal's end, or the last day of a one-day / until deal
const dealEnd = (d) => d.ended_at || (d.flash && d.ends_at) || ((d.repeats === "once" || d.repeats === "until") && d.until_at) || null;

/** 90 days of the numbers behind the Overview's charts, and the deals for the calendar. */
// ponytail: reads up to the row limits below (90 days of rows); move the counting into the database if they're ever reached
async function charts() {
  const keys = dayKeys(90), from = new Date(Date.now() - 91 * 86400000).toISOString(), by = bucketer(keys);
  const [wl, wlTotal, cl, st, dl, od, rs] = await Promise.all([
    rest(`diner_waitlist?select=joined_at&joined_at=gte.${from}&limit=20000`),
    count("diner_waitlist"),
    rest(`claims?select=claimed_at&claimed_at=gte.${from}&limit=50000`),
    rest(`stamps?select=at&at=gte.${from}&limit=50000`),
    rest("deals?select=id,title,restaurant_id,status,flash,ends_at,until_at,repeats,created_at,ended_at,restaurants(name)&order=created_at.desc&limit=2000"),
    rest(`orders?select=placed_at,total,fig_fee,status&placed_at=gte.${from}&limit=20000`),
    rest("restaurants?select=created_at,status&limit=5000"),
  ]);
  // Growth (FIX-LIST #103): every day since the first sign-up of any kind, new per day; the page adds them up
  // ponytail: up to 20,000 rows each; a count per day in the database if FIG ever gets there
  const [gw, gd] = await Promise.all([
    rest("diner_waitlist?select=joined_at&order=joined_at&limit=20000"),
    rest("profiles?select=created_at&role=eq.diner&admin=eq.false&order=created_at&limit=20000"),
  ]);
  const firsts = [gw.rows[0] && gw.rows[0].joined_at, gd.rows[0] && gd.rows[0].created_at, ...rs.rows.map((r) => r.created_at)].filter(Boolean).map((t) => Date.parse(t));
  const span = firsts.length ? Math.max(1, Math.ceil((Date.now() - Math.min(...firsts)) / 86400000) + 1) : 1;
  const gkeys = dayKeys(Math.max(span, 7)), gby = bucketer(gkeys);
  const fresh = by(wl.rows, "joined_at");
  let run = wlTotal - fresh.reduce((a, b) => a + b, 0);
  const cumulative = fresh.map((n) => (run += n));
  // a deal counts on a day it had started (and wasn't still only scheduled) and hadn't ended
  const running = keys.map((k) => dl.rows.filter((d) => d.status !== "scheduled" && dayKey(d.created_at) <= k && !(dealEnd(d) && dayKey(dealEnd(d)) < k)).length);
  const placed = od.rows.filter((o) => o.status !== "unpaid");
  const picked = od.rows.filter((o) => o.status === "picked");
  // restaurants by the day they joined, split by their status today (approval dates aren't stored)
  const upTo = (status) => keys.map((k) => rs.rows.filter((r) => (status === "setup" ? r.status === "pending" : r.status === status) && dayKey(r.created_at) <= k).length);
  return {
    keys,
    waitlist: { total: cumulative, fresh },
    claims: by(cl.rows, "claimed_at"), scans: by(st.rows, "at"), deals: running,
    orders: { placed: by(placed, "placed_at"), value: by(picked, "placed_at", "total"), fees: by(picked, "placed_at", "fig_fee") },
    restaurants: { live: upTo("approved"), setup: upTo("setup"), hidden: upTo("rejected") },
    growth: { keys: gkeys, waitlist: gby(gw.rows, "joined_at"), diners: gby(gd.rows, "created_at"), restaurants: gby(rs.rows, "created_at") },
    calendar: dl.rows.slice(0, 400).map((d) => ({ id: d.id, title: d.title, restaurant_id: d.restaurant_id, restaurant: (d.restaurants || {}).name || "", status: d.status, start: d.created_at, end: dealEnd(d) })),
  };
}

/** One restaurant for its side panel: only the fields it shows. */
async function restaurantDetail(id) {
  uuid(id);
  const keys = dayKeys(30), from = new Date(Date.now() - 31 * 86400000).toISOString(), by = bucketer(keys);
  const [r, deals, staff, menu, orders, reports, scans] = await Promise.all([
    rest(`restaurants?id=eq.${id}&select=id,owner_id,name,cuisine,address,city,phone,status,created_at,photos,hours,takeout`),
    rest(`deals?restaurant_id=eq.${id}&select=id,title,status,flash,ends_at,until_at,repeats,created_at,ended_at&order=created_at.desc&limit=50`),
    rest(`staff?restaurant_id=eq.${id}&select=name,email,role,status&order=invited_at`),
    count(`menu_items?restaurant_id=eq.${id}`),
    rest(`orders?restaurant_id=eq.${id}&select=number,status,total,placed_at&order=placed_at.desc&limit=20`),
    rest(`reports?restaurant_id=eq.${id}&select=reason,details,at,status&order=at.desc&limit=20`),
    rest(`stamps?restaurant_id=eq.${id}&at=gte.${from}&select=at&limit=20000`),
  ]);
  const row = r.rows[0];
  if (!row) return { found: false };
  const ids = deals.rows.map((d) => d.id);
  const [owner, bill, claims] = await Promise.all([
    rest(`profiles?id=eq.${uuid(row.owner_id)}&select=name,email`),
    rest(`billing_accounts?owner_id=eq.${uuid(row.owner_id)}&select=payments_demo,stripe_ready,stripe_payouts`),
    ids.length ? rest(`claims?deal_id=in.(${ids.join(",")})&claimed_at=gte.${from}&select=claimed_at&limit=20000`) : { rows: [] },
  ]);
  const b = bill.rows[0] || {};
  return {
    found: true,
    restaurant: { id: row.id, owner_id: row.owner_id, name: row.name, cuisine: row.cuisine, address: row.address, city: row.city, phone: row.phone, status: row.status, created_at: row.created_at, photos: (row.photos || []).slice(0, 3), takeout: row.takeout },
    owner: owner.rows[0] || {}, staff: staff.rows,
    setup: [["3 photos or more", (row.photos || []).length >= 3], ["Address", !!row.address], ["Opening hours", (row.hours || []).some(Boolean)], ["Menu", menu > 0], ["A deal", deals.rows.length > 0],
      ...(row.takeout ? [["Takeout payments", !!(b.payments_demo || (b.stripe_ready && b.stripe_payouts))]] : [])],
    deals: deals.rows.map((d) => ({ id: d.id, title: d.title, status: d.status, start: d.created_at, end: dealEnd(d) })),
    orders: orders.rows, reports: reports.rows,
    series: { keys, claims: by(claims.rows, "claimed_at"), scans: by(scans.rows, "at") },
  };
}

/** Who wrote or reported something, for the inbox: their account, their restaurants and their latest orders. */
async function personDetail(id) {
  uuid(id);
  const [p, places, orders] = await Promise.all([
    rest(`profiles?id=eq.${id}&select=name,role,created_at`),
    rest(`restaurants?owner_id=eq.${id}&select=id,name,status`),
    rest(`orders?user_id=eq.${id}&select=number,status,total,placed_at,restaurant_id&order=placed_at.desc&limit=5`),
  ]);
  return p.rows[0] ? { found: true, person: p.rows[0], restaurants: places.rows, orders: orders.rows } : { found: false };
}

// a 14-day daily series and this week against the week before, from the rows' times (FIX-LIST #85: the Overview's
// sparklines and deltas). Read-only. ponytail: reads up to 10,000 rows of 28 days; a database count per day if it ever grows past that
async function series(table, col) {
  const from = new Date(Date.now() - 28 * 86400000).toISOString();
  const rows = (await rest(`${table}?select=${col}&${col}=gte.${from}&order=${col}.desc&limit=10000`)).rows;
  const ago = rows.map((r) => Math.floor((Date.now() - Date.parse(r[col])) / 86400000)).filter((d) => d >= 0 && d < 28);
  const n = (a, b) => ago.filter((d) => d >= a && d < b).length;
  return { days: Array.from({ length: 14 }, (_, i) => n(13 - i, 14 - i)), week: n(0, 7), prev: n(7, 14) };
}

async function overview() {
  const since = new Date(Date.now() - 30 * 86400000).toISOString();
  const week = new Date(Date.now() - 7 * 86400000).toISOString();
  const none = { days: [], week: null, prev: null };
  const [diners, restaurants, live, reports, recentR, premiumRows, recentRep, leads, support, owners, changes, orders30, ordersOpen, dealsLive, claims7, scans7, waitlist, waitlist7, sWait, sClaims, sScans] = await Promise.all([
    safe(count("profiles?role=eq.diner"), null),
    safe(count("restaurants"), null),
    safe(count("restaurants?status=eq.approved"), null),
    safe(count("reports?status=eq.open"), null),
    safe(rest("restaurants?select=id,owner_id,name,cuisine,city,status,created_at,photos&order=created_at.desc&limit=100"), { rows: [] }),
    safe(rest("billing_accounts?select=owner_id,premium_until,premium_source,comped,payments_demo,stripe_ready,stripe_payouts"), { rows: [] }),
    safe(rest("reports?select=id,reason,details,at,status,user_id,restaurant_id,claim_id&order=at.desc&limit=100"), { rows: [] }),
    safe(rest("waitlist?select=created_at,role,email,phone,restaurant,area,source&order=created_at.desc&limit=500"), { rows: [] }),
    // what people wrote through "Message us" in the app and on the website (user 2026-10-11: nobody could read these)
    safe(rest("support_messages?select=id,email,topic,body,at,status,user_id&order=at.desc&limit=200"), { rows: [] }),
    safe(rest("profiles?select=id,email,name&role=eq.business&limit=500"), { rows: [] }),
    // who a restaurant is changed (name, address) or handed to (the hand-over feature's record)
    safe(rest("restaurant_changes?select=id,restaurant_id,kind,before,after,at&order=at.desc&limit=40"), { rows: [] }),
    safe(count(`orders?placed_at=gte.${since}`), null),
    safe(count("orders?status=in.(unpaid,sent,accepted,ready)"), null),
    // the Overview's week (FIX-LIST #83 review): deals running, claims and counter scans in 7 days, the diner waitlist
    safe(count("deals?status=eq.live"), null),
    safe(count(`claims?claimed_at=gte.${week}`), null),
    safe(count(`stamps?at=gte.${week}`), null),
    safe(count("diner_waitlist"), null),
    safe(count(`diner_waitlist?joined_at=gte.${week}`), null),
    safe(series("diner_waitlist", "joined_at"), none),
    safe(series("claims", "claimed_at"), none),
    safe(series("stamps", "at"), none),
  ]);
  return {
    counts: { diners, restaurants, live, reports, orders30, ordersOpen, dealsLive, claims7, scans7, waitlist, waitlist7, support: support.rows.filter((m) => m.status === "open").length },
    series: { waitlist: sWait, claims: sClaims, scans: sScans },
    support: support.rows, owners: owners.rows, changes: changes.rows,
    restaurants: recentR.rows, premium: premiumRows.rows, reports: recentRep.rows,
    leads: leads.rows.filter((l) => l.role === "restaurant"), waitlist: leads.rows.filter((l) => l.role === "diner").length,
  };
}

// ads (restaurants pay per tap, the team invoices monthly): every campaign with its results, every ad account with this
// month's spend, and the invoices. Dormant while ads are off in the app (ADS_ON): the admin page doesn't show them (FIX-LIST #83)
async function ads() {
  const [campaigns, accounts, invoices] = await Promise.all([
    rest("rpc/admin_campaigns", { method: "POST", body: "{}" }),
    rest("rpc/admin_ad_accounts", { method: "POST", body: "{}" }),
    rest("ad_invoices?select=id,owner_id,month,amount,status,sent_at,paid_at&order=month.desc&limit=300"),
  ]);
  const names = new Map(accounts.rows.map((a) => [a.owner_id, a]));
  return { campaigns: campaigns.rows, accounts: accounts.rows, invoices: invoices.rows.map((x) => ({ ...x, owner: names.get(x.owner_id) || {} })) };
}
const uuid = (id) => { if (typeof id !== "string" || !/^[0-9a-f-]{36}$/i.test(id)) throw new Error("bad id"); return id; }; // a string only (#153)
// stop an ad (with a note the owner sees) or let it run again
async function setCampaign(id, stop, note) {
  await rest(`campaigns?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify(stop ? { status: "stopped", note: String(note || "").slice(0, 300) || null } : { status: "active", note: null }), headers: { Prefer: "return=minimal" } });
}
// an owner's monthly limit, or a hold on every ad (an unpaid invoice)
async function setAccount(owner, limit, held) {
  const change = {};
  if (limit != null) { const n = Number(limit); if (!(n >= 0 && n <= 100000)) throw new Error("bad limit"); change.monthly_limit = n; }
  if (held != null) change.status = held ? "held" : "active";
  await rest(`ad_accounts?owner_id=eq.${uuid(owner)}`, { method: "PATCH", body: JSON.stringify(change), headers: { Prefer: "return=minimal" } });
}
// FIG Premium ($50 a year) switched on by the team for some years from now, or off (0)
async function setPremium(owner, years) {
  const y = Number(years);
  if (!(y >= 0 && y <= 5)) throw new Error("bad years");
  await rest("rpc/set_premium", { method: "POST", body: JSON.stringify({ p_owner: uuid(owner), p_until: y ? new Date(Date.now() + y * 365 * 86400000).toISOString() : null, p_source: "fig" }) });
}
// a message from the inbox: answered, or open again
// someone asks to stop the emails, or to be forgotten (FIX-LIST #95, CASL and PIPEDA requests): by the email on the list
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const listEmail = (e) => { const x = String(e || "").trim().toLowerCase(); if (x.length > 254 || !EMAIL.test(x)) throw new Error("bad email"); return x; };
/** No more emails: consent off, and when they asked. They stay on the list (their place in line keeps). */
async function waitlistUnsubscribe(email) {
  const r = await rest(`diner_waitlist?email=eq.${encodeURIComponent(listEmail(email))}`, { method: "PATCH", body: JSON.stringify({ consent: false, unsubscribed_at: new Date().toISOString() }), headers: { Prefer: "return=representation" } });
  return { found: r.rows.length > 0 };
}
/** The account with this address stops getting FIG's marketing emails (profiles.marketing_emails false); the privacy policy says every one of them has a working unsubscribe. */
async function accountUnsubscribe(email) {
  await rest(`profiles?email=eq.${encodeURIComponent(listEmail(email))}&marketing_emails=is.true`, { method: "PATCH", body: JSON.stringify({ marketing_emails: false }), headers: { Prefer: "return=minimal" } });
}
/** Off the list for good (their row is deleted). */
async function waitlistRemove(email) {
  const r = await rest(`diner_waitlist?email=eq.${encodeURIComponent(listEmail(email))}`, { method: "DELETE", headers: { Prefer: "return=representation" } });
  return { found: r.rows.length > 0 };
}
/** A message deleted for good (someone asked for it, or it was spam). */
async function supportRemove(id) {
  const r = await rest(`support_messages?id=eq.${uuid(id)}`, { method: "DELETE", headers: { Prefer: "return=representation" } });
  return { found: r.rows.length > 0 };
}
/** Free text from the public (a school, a link's source) for the admin: letters, digits, spaces and . , ' ’ - & @ ( ) only,
 *  one space at a time, at most 80 characters (FIX-LIST #170: never a formula or markup). */
const tidyText = (t) => (t == null ? t : String(t).normalize("NFC").replace(/\s+/g, " ").replace(/[^\p{L}\p{N} .,'’&@()\-]/gu, "").replace(/ +/g, " ").trim().slice(0, 80));
async function setSupport(id, status) {
  if (!["open", "answered"].includes(status)) throw new Error("bad status");
  await rest(`support_messages?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify({ status }), headers: { Prefer: "return=minimal" } });
}
// Someone lost the phone with their authenticator app and wrote to FIG (check it's really them first: they write from the
// account's email and know the phone number on it). Removes their authenticators, so they sign in with the password alone
// and can switch two-step login on again. By account id, or by email (looked up in profiles).
async function twoStepOff({ id, email }) {
  let uid = id ? uuid(id) : null;
  if (!uid) {
    const e = String(email || "").trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+$/.test(e)) throw new Error("bad email");
    uid = (await rest(`profiles?select=id&email=eq.${encodeURIComponent(e)}&limit=1`)).rows[0]?.id;
    if (!uid) return { found: false, removed: 0 };
  }
  const auth = (method, path) => fetch(`${url()}/auth/v1/admin/users/${uid}/${path}`, { method, headers: { apikey: key(), Authorization: `Bearer ${key()}` } });
  const list = await auth("GET", "factors");
  if (!list.ok) throw new Error("factors " + list.status);
  const body = await list.json();
  const factors = Array.isArray(body) ? body : body.factors || [];
  for (const f of factors) { const d = await auth("DELETE", `factors/${uuid(f.id)}`); if (!d.ok) throw new Error("factor " + d.status); }
  console.log("admin: two-step login turned off for", uid, "authenticators:", factors.length); // the id only, never the email
  return { found: true, removed: factors.length };
}
async function makeInvoices(month) {
  if (!/^\d{4}-\d{2}-01$/.test(String(month))) throw new Error("bad month");
  await rest("rpc/make_ad_invoices", { method: "POST", body: JSON.stringify({ p_month: month }) });
}
async function setInvoice(id, status) {
  if (!["sent", "paid", "void", "open"].includes(status)) throw new Error("bad status");
  const stamp = status === "sent" ? { sent_at: new Date().toISOString() } : status === "paid" ? { paid_at: new Date().toISOString() } : {};
  await rest(`ad_invoices?id=eq.${uuid(id)}`, { method: "PATCH", body: JSON.stringify({ status, ...stamp }), headers: { Prefer: "return=minimal" } });
}


// the blog's controls (table blog_overrides): a post taken down, or its go-live time moved. The blog is generated from the site's code;
// these only say what to leave out or when to publish, so nothing here can change a post's words.
const SLUG = /^[a-z0-9-]{1,100}$/;
async function blogOverrides() { return (await rest("blog_overrides?select=slug,hidden,publish_at,note,updated_at&order=slug")).rows; }
async function setBlog(slug, change) {
  if (!SLUG.test(String(slug))) throw new Error("bad slug");
  const cur = (await rest(`blog_overrides?select=slug,hidden,publish_at,note&slug=eq.${slug}`)).rows[0] || { hidden: false, publish_at: null, note: null };
  const next = { hidden: cur.hidden, publish_at: cur.publish_at, note: cur.note };
  if ("hidden" in change) next.hidden = !!change.hidden;
  if ("publish_at" in change) {
    if (change.publish_at === null) next.publish_at = null;
    else { const t = Date.parse(change.publish_at); if (!(t > Date.now() - 86400000 && t < Date.now() + 366 * 86400000)) throw new Error("bad time"); next.publish_at = new Date(t).toISOString(); }
  }
  if ("note" in change) next.note = change.note ? String(change.note).slice(0, 300) : null;
  if (!next.hidden && !next.publish_at) { await rest(`blog_overrides?slug=eq.${slug}`, { method: "DELETE", headers: { Prefer: "return=minimal" } }); return { cleared: true }; }
  await rest("blog_overrides?on_conflict=slug", { method: "POST", body: JSON.stringify({ slug, ...next }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  return { saved: true };
}

// the diner side switch (settings key diners_open: 'off' = restaurants only, 'waitlist' = founding members only, 'on' or no row = everyone),
// the founding cap (settings key founding_cap: only the first N on the waitlist; no row = all of it) and the diner waitlist (closed to the public)
async function dinersState() {
  const flags = (await rest("settings?select=key,value&key=in.(diners_open,founding_cap,founding_until,opens_at)")).rows;
  const site = (await rest("rpc/site_mode", { method: "POST", body: "{}" })).rows || {}; // the effective mode (a passed opening date opens it)
  const v = (k) => (flags.find((f) => f.key === k) || {}).value;
  const mode = v("diners_open") === "off" ? "off" : v("diners_open") === "waitlist" ? "waitlist" : "on";
  // what a person typed (their school) or a link carried (the source) reaches the admin tidied (FIX-LIST #170)
  const wl = (await rest("diner_waitlist?select=email,school,consent,source,joined_at,consent_at,unsubscribed_at&order=joined_at.desc&limit=5000")).rows
    .map((w) => ({ ...w, school: tidyText(w.school), source: tidyText(w.source) }));
  const accounts = (await rest("profiles?select=id&role=eq.diner&admin=eq.false&limit=5000")).rows.length;
  return { mode, effective: site.mode || mode, open: (site.mode || mode) === "on", cap: v("founding_cap") ? Number(v("founding_cap")) : null, until: v("founding_until") || null, opens: v("opens_at") || null, closes: site.founding_until || null, waitlist: wl, accounts };
}
async function setDinersMode(mode) {
  if (!["off", "waitlist", "on"].includes(mode)) throw new Error("bad mode");
  const was = ((await rest("settings?select=value&key=eq.diners_open")).rows[0] || {}).value || "on"; // no row = everyone
  await rest("settings?on_conflict=key", { method: "POST", body: JSON.stringify({ key: "diners_open", value: mode }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  // the founding cutoff belongs to one opening to founding members (FIX-LIST #184): opening to them (from off or on) closes the
  // list now, every time, so who joined before now gets in and later sign-ups wait; off or on clears it, so a later opening (by
  // the switch or the opening date) never inherits an old cutoff. Waitlist again while already on waitlist keeps it.
  if (mode !== "waitlist") await setFoundingUntil(null);
  else if (was !== "waitlist") await setFoundingUntil("now");
  console.log("admin: diner side ->", mode);
  return { mode, open: mode === "on" };
}
// when the founding list closes: "now", or null to reopen it (everyone on the list, whenever they joined)
async function setFoundingUntil(when) {
  if (when === null) { await rest("settings?key=eq.founding_until", { method: "DELETE", headers: { Prefer: "return=minimal" } }); return { until: null }; }
  if (when !== "now") throw new Error("bad until");
  const at = new Date().toISOString();
  await rest("settings?on_conflict=key", { method: "POST", body: JSON.stringify({ key: "founding_until", value: at }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  return { until: at };
}
// the opening date: an ISO time in the future, or null to clear it
async function setOpensAt(at) {
  if (at === null) { await rest("settings?key=eq.opens_at", { method: "DELETE", headers: { Prefer: "return=minimal" } }); return { opens: null }; }
  const d = new Date(at);
  if (isNaN(d) || d < new Date(Date.now() - 60000)) throw new Error("bad date");
  await rest("settings?on_conflict=key", { method: "POST", body: JSON.stringify({ key: "opens_at", value: d.toISOString() }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  return { opens: d.toISOString() };
}
async function setFoundingCap(cap) {
  if (cap === null || cap === "" || cap === undefined) {
    await rest("settings?key=eq.founding_cap", { method: "DELETE", headers: { Prefer: "return=minimal" } });
    return { cap: null };
  }
  const n = Number(cap);
  if (!Number.isInteger(n) || n < 1 || n > 1000000) throw new Error("bad cap");
  await rest("settings?on_conflict=key", { method: "POST", body: JSON.stringify({ key: "founding_cap", value: String(n) }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  return { cap: n };
}

// restaurant prospects: every place in the Markham directory, with the team's shortlist, status and note (server-only functions prospect_list / prospect_set)
const PSTAT = ["new", "contacted", "interested", "not-interested", "signed"];
async function prospects(f) {
  f = f || {};
  const body = { p_q: f.q ? String(f.q).slice(0, 80) : null, p_kind: f.kind ? String(f.kind).slice(0, 60) : null, p_status: PSTAT.includes(f.status) ? f.status : null,
    p_short: !!f.short, p_independent: f.independent !== false, p_hide_fig: !!f.hideFig, p_off: Math.max(0, Math.min(5000, parseInt(f.offset, 10) || 0)), p_lim: 50 };
  return (await rest("rpc/prospect_list", { method: "POST", body: JSON.stringify(body) })).rows;
}
async function setProspect(id, change) {
  if (!/^(osm|fsq|ovt):[A-Za-z0-9_-]{1,60}$/.test(String(id))) throw new Error("bad place"); // all three map sources (FIX-LIST #27)
  const body = { p_place: id };
  if ("short" in change) body.p_short = !!change.short;
  if ("status" in change) { if (!PSTAT.includes(change.status)) throw new Error("bad status"); body.p_status = change.status; }
  if ("note" in change) { if (change.note === "" || change.note === null) body.p_clear_note = true; else body.p_note = String(change.note).slice(0, 500); }
  await rest("rpc/prospect_set", { method: "POST", body: JSON.stringify(body) });
  return { saved: true };
}

// where people came from (FIX-LIST #105): the ?src= tag on the waitlist and on accounts, and accounts' answers to "How did you
// hear about FIG?". Accounts: null until the #105 migration is in (the columns aren't there yet). Test accounts left out.
async function sources() {
  const wl = (await rest("diner_waitlist?select=source,joined_at&order=joined_at.desc&limit=20000")).rows;
  let accounts = null;
  try { accounts = (await rest("profiles?select=role,source,heard_from,heard_from_note,created_at&admin=eq.false&order=created_at.desc&limit=20000")).rows; } catch { /* before the migration */ }
  return { waitlist: wl.map((w) => ({ source: w.source, at: w.joined_at })), accounts: accounts && accounts.map((a) => ({ role: a.role, source: a.source, heard: a.heard_from, note: a.heard_from_note, at: a.created_at })) };
}

/** The waitlist emails that agreed to be emailed (and haven't unsubscribed), oldest first: who gets the launch email. */
async function agreedEmails() {
  return (await rest("diner_waitlist?select=email&consent=is.true&order=joined_at&limit=20000")).rows.map((r) => r.email);
}

// ---- the founding pre-sale (FIX-LIST #141): the presale-admin Supabase function does the Stripe work with FIG's own key; the admin
// only asks it, with the service key, and only for these four things
const PRESALE_DO = new Set(["list", "start-billing", "admin-refund", "refund-all", "comp"]);
async function presale(action, body = {}) {
  if (!PRESALE_DO.has(action)) throw new Error("bad action");
  const r = await fetch(`${url()}/functions/v1/presale-admin`, { method: "POST", headers: { apikey: key(), Authorization: `Bearer ${key()}`, "Content-Type": "application/json" }, body: JSON.stringify({ ...body, action }) });
  const out = await r.json().catch(() => null);
  return !out || (!r.ok && !out.error) ? { error: "not-deployed" } : out; // no function there yet: Supabase's own 404
}
/** The page: the switch (settings presale_on) and the plans; the plans can't load before the function is deployed. */
async function presaleState() {
  const on = ((await rest("settings?select=value&key=eq.presale_on")).rows[0] || {}).value === "on";
  return { on, ...(await presale("list").catch(() => ({ error: "not-deployed" }))) };
}
/** The offer on or off. On only once the function answers and the four live prices are set (its "ready"); off always works. */
async function setPresaleOn(on) {
  if (typeof on !== "boolean") throw new Error("bad switch");
  if (on) { const l = await presale("list").catch(() => null); if (!l || l.error || !l.ready) throw new Error("bad presale-not-ready"); }
  await rest("settings?on_conflict=key", { method: "POST", body: JSON.stringify({ key: "presale_on", value: on ? "on" : "off" }), headers: { Prefer: "resolution=merge-duplicates,return=minimal" } });
  return { on };
}
/** Start billing on a day (the function checks 14 to 360 days ahead), one deposit's refund (force: after the 14 days), every deposit's. */
async function presaleStart(at) {
  const t = Date.parse(String(at || ""));
  if (!Number.isFinite(t)) throw new Error("bad date");
  return presale("start-billing", { at: new Date(t).toISOString() });
}
const presaleRefund = async (owner, force) => presale("admin-refund", { owner: uuid(owner), force: force === true }); // one plan per owner (#27)
const presaleRefundAll = async () => presale("refund-all");
/** FIG's comp for an owner (#141): on or off, with the reason the database keeps. */
const presaleComp = async (owner, on, note) => {
  if (typeof on !== "boolean") throw new Error("bad comp");
  return presale("comp", { owner: uuid(owner), on, note: String(note || "").trim().slice(0, 200) });
};

module.exports = { presaleState, setPresaleOn, presaleStart, presaleRefund, presaleRefundAll, presaleComp, tidyText, agreedEmails, sources, waitlistUnsubscribe, accountUnsubscribe, waitlistRemove, supportRemove, charts, restaurantDetail, personDetail, prospects, setProspect, dinersState, setDinersMode, setFoundingCap, setFoundingUntil, setOpensAt, connected, overview, setCampaign, setAccount, setPremium, setSupport, twoStepOff, makeInvoices, setInvoice, blogOverrides, setBlog };
