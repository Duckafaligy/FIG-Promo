// The admin pages (from the Paper designs: Admin 00 Sign in, 01 Overview, 02 Restaurants, 03 Reports, 04 Leads; plus Ads,
// FIG's only income: every restaurant's ads, stop or restart one, account limits and holds, and the monthly invoices).
const LOGO = `<svg width="30" height="30" viewBox="743 716 100 100" aria-hidden="true"><path fill="#1E5EFF" d="M765.637 809.875C755.252 806.459 749.184 797.508 749.184 785.965V751.1C749.184 735.317 761.319 722.714 776.955 722.714H836.699L831.098 730.252C827.014 735.906 822.346 738.968 814.762 738.968H777.189C770.888 738.968 765.754 744.15 765.754 750.629V755.341L767.621 753.574C770.304 751.218 772.989 750.158 776.722 750.158H800.06L790.725 762.526C788.275 765.941 785.24 767.354 780.923 767.354H772.405C768.671 767.354 765.637 770.299 765.637 774.304V809.875Z"/><path fill="#1E5EFF" d="M793.759 769.592H836.699V784.08C836.699 799.746 824.563 811.171 809.044 811.171H770.888V795.387H809.161C815.462 795.387 820.013 790.794 820.013 784.433V783.256H781.623L793.759 769.592Z"/><path fill="#14C86B" d="M797.142 765.705L805.194 755.104C807.877 751.689 811.145 750.158 815.696 750.158H836.699V754.28C836.699 761.347 832.265 765.705 825.264 765.705H797.142Z"/></svg>`;

const BASE = `
@font-face { font-family: "Jakarta"; src: url("/assets/PlusJakartaSans.ttf") format("truetype"); font-weight: 200 800; font-display: swap; }
*,*::before,*::after { box-sizing: border-box; } html,body { margin: 0; }
body { font-family: "Jakarta", system-ui, sans-serif; color: #0A1020; background: #F4F6FB; -webkit-font-smoothing: antialiased; }
h1,h2,h3,p { margin: 0; } button, input { font: inherit; color: inherit; }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 19px; letter-spacing: -0.02em; }
.btn { height: 48px; padding: 0 22px; border: 0; border-radius: 999px; background: #1E5EFF; color: #fff; font-weight: 800; font-size: 16px; cursor: pointer; }
.btn:disabled { opacity: .55; cursor: default; }
.btn.sm { height: 38px; padding: 0 16px; font-size: 14px; }
input.f { width: 100%; height: 48px; padding: 0 16px; border-radius: 12px; border: 1.5px solid transparent; background: #F2F5FA; font-size: 16px; outline: none; }
input.f:focus { border-color: #1E5EFF; background: #EAF0FF; }
.muted { color: #5B6779; }
:focus-visible { outline: 3px solid #1E5EFF; outline-offset: 2px; }`;

const head = (title, extra) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>${title}</title><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><style>${BASE}${extra}</style></head>`;

function signInPage() {
  return head("FIG Admin", `
body { min-height: 100vh; display: grid; place-items: center; padding: 20px; }
.card { width: 100%; max-width: 420px; padding: 32px; border-radius: 24px; background: #fff; box-shadow: 0 30px 60px rgba(10,16,32,.08); }
h1 { margin-top: 28px; font-size: 28px; letter-spacing: -0.03em; }
.sub { margin-top: 6px; font-size: 15px; }
label { display: block; margin: 22px 0 8px; font-weight: 700; font-size: 14px; }
.btn { width: 100%; margin-top: 18px; }
.msg { margin-top: 14px; font-size: 14px; font-weight: 600; min-height: 20px; }
.msg.err { color: #C9353A; } .lock { color: #0A1020; }
.back { display: inline-block; margin-top: 18px; font-size: 13px; color: #5B6779; }`) + `<body>
<form class="card" id="f" autocomplete="off">
  <div class="brand">${LOGO}FIG Admin</div>
  <h1>Sign in</h1>
  <p class="sub muted">Only the FIG team gets in.</p>
  <label for="pw">Password</label>
  <input class="f" id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
  <button class="btn" id="go" type="submit">Sign in</button>
  <p class="msg" id="msg" role="status" aria-live="polite"></p>
  <a class="back" href="/">Back to FIG</a>
</form>
<script>
const f = document.getElementById("f"), pw = document.getElementById("pw"), go = document.getElementById("go"), msg = document.getElementById("msg");
let timer;
function locked(sec) {
  clearInterval(timer); go.disabled = true; pw.disabled = true; msg.className = "msg lock";
  const end = Date.now() + sec * 1000;
  const tick = () => {
    const s = Math.max(0, Math.round((end - Date.now()) / 1000));
    msg.textContent = "Too many tries. Try again in " + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0") + ".";
    if (s <= 0) { clearInterval(timer); go.disabled = false; pw.disabled = false; msg.textContent = ""; pw.focus(); }
  };
  tick(); timer = setInterval(tick, 1000);
}
f.addEventListener("submit", async (e) => {
  e.preventDefault(); go.disabled = true; msg.textContent = "";
  const r = await fetch("/api/admin-api?do=login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ password: pw.value }) }).catch(() => null);
  const j = r ? await r.json().catch(() => ({})) : {};
  pw.value = "";
  if (r && r.ok) return location.reload();
  if (j.locked) return locked(j.retryIn);
  go.disabled = false; msg.className = "msg err";
  msg.textContent = j.error ? j.error + (j.triesLeft != null ? " " + j.triesLeft + (j.triesLeft === 1 ? " try" : " tries") + " left before a lock." : "") : "Couldn't reach the server.";
  pw.focus();
});
</script></body></html>`;
}

function appPage() {
  return head("FIG Admin", `
.shell { display: grid; grid-template-columns: 232px 1fr; min-height: 100vh; }
aside { position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; gap: 6px; padding: 24px 16px; background: #fff; border-right: 1px solid #E2E7EF; }
aside .brand { padding: 0 10px 22px; }
.nav button { display: flex; justify-content: space-between; align-items: center; width: 100%; height: 42px; padding: 0 12px; border: 0; border-radius: 12px; background: none; text-align: left; font-weight: 600; font-size: 15px; cursor: pointer; }
.nav button:hover { background: #F2F5FA; }
.nav button.on { background: #EAF0FF; color: #1E5EFF; font-weight: 800; }
.badge { min-width: 22px; height: 22px; padding: 0 7px; border-radius: 99px; background: #E2E7EF; color: #0A1020; font-size: 12px; font-weight: 800; display: grid; place-items: center; }
.nav button.on .badge { background: #1E5EFF; color: #fff; }
.who { margin-top: auto; padding: 0 10px; font-size: 13px; }
.who button { margin-top: 8px; border: 0; background: none; padding: 0; color: #1E5EFF; font-weight: 700; cursor: pointer; font-size: 13px; }
main { padding: 36px 36px 60px; background: #fff; min-width: 0; }
h1 { font-size: 36px; letter-spacing: -0.03em; } .lead { margin-top: 6px; font-size: 16px; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 26px 0 30px; }
.stat { padding: 22px; border-radius: 18px; background: #F2F5FA; } .stat b { display: block; font-size: 34px; letter-spacing: -0.03em; } .stat span { color: #5B6779; font-size: 14px; }
.stat.blue b { color: #1E5EFF; } .stat.red b { color: #C9353A; }
h2 { font-size: 20px; letter-spacing: -0.02em; margin: 0 0 12px; }
.tbl { border: 1px solid #E2E7EF; border-radius: 16px; overflow: hidden; margin-bottom: 30px; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { background: #F2F5FA; text-align: left; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: #5B6779; padding: 13px 18px; }
td { padding: 15px 18px; border-top: 1px solid #E2E7EF; }
.pill { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 800; background: #EAF0FF; color: #1A52E0; }
.used { color: #067A55; font-weight: 800; }
.pill.g { background: #E3F7EF; color: #067A55; } .pill.r { background: #FDECEC; color: #B4282D; } .pill.k { background: #F2F5FA; color: #5B6779; }
.mono { font-family: ui-monospace, Consolas, monospace; font-weight: 700; letter-spacing: .02em; }
.empty { padding: 26px; border-radius: 16px; background: #F2F5FA; color: #5B6779; font-size: 15px; line-height: 1.6; }
.empty b { color: #0A1020; }
.make { padding: 22px; border: 1px solid #E2E7EF; border-radius: 18px; margin-bottom: 28px; }
.row { display: grid; grid-template-columns: 1fr 140px 140px auto; gap: 12px; align-items: end; margin-top: 14px; }
.row label { display: block; font-size: 13px; font-weight: 700; margin-bottom: 6px; }
.new { margin-top: 16px; padding: 18px; border-radius: 14px; background: #C8F135; display: none; }
.spot { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; padding: 22px; border-radius: 18px; background: #EAF0FF; margin-bottom: 16px; } .spot h2 { margin: 0 0 4px; } .spot .btn { flex-shrink: 0; width: auto; margin: 0; }
#q-new { margin: 0 0 28px; } .big .codes span { font-size: 26px; padding: 12px 18px; }
.new .codes { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; } .new .codes span { background: #fff; padding: 8px 12px; border-radius: 10px; }
.link { border: 0; background: none; padding: 0; color: #1E5EFF; font-weight: 800; cursor: pointer; } .link.red { color: #C9353A; margin-left: 14px; }
.note { font-size: 13px; color: #5B6779; }
.dsp { border: 1px solid #E2E7EF; border-radius: 20px; padding: 22px; margin-bottom: 18px; }
.dsp-h { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; align-items: baseline; }
.dsp-h h2 { margin: 0; }
.quote { margin: 14px 0; padding: 14px 16px; border-radius: 14px; background: #F2F5FA; font-size: 15px; line-height: 1.5; }
.cols { display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 16px; }
.box { padding: 16px; border-radius: 14px; border: 1px solid #E2E7EF; font-size: 14px; }
.box h3 { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: #5B6779; margin: 0 0 10px; }
.tl { display: grid; grid-template-columns: 1fr max-content; gap: 6px 12px; } .tl .no { color: #9AA4B2; }
.tl b.g { color: #067A55; } .tl b.r { color: #C9353A; }
.kv { display: grid; grid-template-columns: max-content 1fr; gap: 6px 14px; } .kv span { color: #5B6779; white-space: nowrap; } .kv b { text-align: right; overflow-wrap: anywhere; }
.hint { margin-top: 14px; padding: 12px 14px; border-radius: 12px; font-size: 14px; font-weight: 700; }
.hint.g { background: #E3F7EF; color: #067A55; } .hint.r { background: #FDECEC; color: #B4282D; } .hint.k { background: #F2F5FA; color: #0A1020; }
.act { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 16px; }
.act input { flex: 1; min-width: 200px; }
.btn.g { background: #067A55; } .btn.k { background: #0A1020; }
@media (max-width: 900px) { .cols { grid-template-columns: 1fr; } }
@media (max-width: 900px) { .shell { grid-template-columns: 1fr; } aside { position: static; height: auto; display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 10px; padding: 14px 16px; border-right: 0; border-bottom: 1px solid #E2E7EF; } aside .brand { padding: 0; } .who { grid-column: 2; grid-row: 1; text-align: right; } .nav { grid-column: 1 / -1; display: flex; gap: 6px; overflow-x: auto; margin: 0 -16px; padding: 0 16px; } .nav button { width: auto; flex-shrink: 0; gap: 8px; } .stats { grid-template-columns: 1fr 1fr; } .row { grid-template-columns: 1fr; } main { padding: 24px 18px; } .tbl { overflow-x: auto; } }`) + `<body>
<div class="shell">
  <aside>
    <div class="brand">${LOGO}FIG Admin</div>
    <div class="nav" id="nav">
      <button data-v="overview" class="on">Overview</button>
      <button data-v="restaurants">Restaurants <span class="badge" id="n-restaurants">–</span></button>
      <button data-v="reports">Reports <span class="badge" id="n-reports">–</span></button>
      <button data-v="leads">Leads <span class="badge" id="n-leads">–</span></button>
      <button data-v="diners">Diners</button>
      <button data-v="ads">Ads <span class="badge" id="n-ads">–</span></button>
    </div>
    <div class="who">Brendan · Owner<br><button id="out">Sign out</button></div>
  </aside>
  <main id="main"><p class="muted">Loading…</p></main>
</div>
<script>
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const ago = (t) => { const m = Math.round((Date.now() - Date.parse(t)) / 60000); return m < 60 ? m + " min ago" : m < 1440 ? Math.round(m / 60) + " h ago" : Math.round(m / 1440) + " days ago"; };
const LAUNCH = Date.parse("2027-01-01T00:00:00-05:00");
const days = Math.max(0, Math.ceil((LAUNCH - Date.now()) / 86400000));
let D = null, view = "overview";
const api = (what, body) => fetch("/api/admin-api?do=" + what, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) })
  .then(async (r) => { if (r.status === 401) location.reload(); return r.json(); });

const NOT_CONNECTED = '<div class="empty"><b>Not connected to FIG\\'s database yet.</b><br>In Vercel → fig-promo → Settings → Environment Variables, add <b>SUPABASE_URL</b> and <b>SUPABASE_SERVICE_ROLE_KEY</b> (Supabase → Project Settings → API), then redeploy. The key stays on the server; it is never sent to this page.</div>';
const stat = (n, label, cls = "") => '<div class="stat ' + cls + '"><b>' + (n == null ? "–" : n) + '</b><span>' + label + '</span></div>';
const table = (heads, rows, empty) => rows.length
  ? '<div class="tbl"><table><tr>' + heads.map((h) => "<th>" + h + "</th>").join("") + "</tr>" + rows.map((r) => "<tr>" + r.map((c) => "<td>" + c + "</td>").join("") + "</tr>").join("") + "</table></div>"
  : '<div class="empty">' + empty + "</div>";
const statusPill = (s) => s === "approved" ? '<span class="pill g">Live</span>' : s === "rejected" ? '<span class="pill r">Paused</span>' : '<span class="pill">Setting up</span>';

// a time on the order, in Ontario time ("Oct 6, 6:42 p.m.")
const when = (t) => t ? new Date(t).toLocaleString("en-CA", { timeZone: "America/Toronto", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : "";

const VIEWS = {
  overview: () => '<h1>Overview</h1><p class="lead muted">Before launch · ' + days + ' days to January 1, 2027</p>' + (!D.connected ? NOT_CONNECTED :
    '<div class="stats">' + stat(D.counts.diners, "Diners signed up", "blue") + stat(D.counts.live, "Restaurants live") + stat(D.counts.reports, "Open reports", "red") + "</div>" +
    "<h2>Latest restaurants</h2>" + table(["Restaurant", "Cuisine", "City", "Status", "Joined"], D.restaurants.slice(0, 6).map((r) => ["<b>" + esc(r.name) + "</b>", esc(r.cuisine), esc(r.city), statusPill(r.status), ago(r.created_at)]), "No restaurants yet.")),
  restaurants: () => '<h1>Restaurants</h1><p class="lead muted">Every restaurant on FIG, newest first. A restaurant goes live when it finishes setup.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED :
    table(["Restaurant", "Cuisine", "City", "Status", "Joined", "FIG Premium"], D.restaurants.map((r) => {
      // Premium ($50 a year) is per owner, for all their locations; the team can switch it on for a year, or off
      const p = (D.premium || []).find((x) => x.owner_id === r.owner_id && new Date(x.premium_until) > new Date());
      return ["<b>" + esc(r.name) + "</b>", esc(r.cuisine), esc(r.city), statusPill(r.status), ago(r.created_at),
        p ? '<span class="pill g">Until ' + esc(new Date(p.premium_until).toLocaleDateString("en-CA")) + '</span> <button class="link" data-prem="' + esc(r.owner_id) + '" data-years="0">Turn off</button>'
          : '<button class="link" data-prem="' + esc(r.owner_id) + '" data-years="1">Give a year</button>'];
    }), "No restaurants yet.")),
  reports: () => '<h1>Reports</h1><p class="lead muted">Visits diners or restaurants reported.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED :
    table(["Reason", "Details", "When", "Status"], D.reports.map((r) => ["<b>" + esc(r.reason) + "</b>", esc(r.details), ago(r.at), r.status === "open" ? '<span class="pill r">Open</span>' : '<span class="pill g">Settled</span>']), "No reports. Good news.")),
  leads: () => '<h1>Restaurant leads</h1><p class="lead muted">Restaurants that left their details on the website.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED :
    table(["Restaurant", "Contact", "Area", "Received", "From"], D.leads.map((l) => ["<b>" + esc(l.restaurant) + "</b>", esc(l.email || l.phone), esc(l.area), ago(l.created_at), esc(l.source)]), "No leads yet. They arrive from the website's sign-up form once the waitlist table is set up.")),
  diners: () => '<h1>Diners</h1><p class="lead muted">People signed up to FIG and on the website waitlist.</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
    '<div class="stats">' + stat(D.counts.diners, "Diner accounts", "blue") + stat(D.waitlist, "Website waitlist") + "</div>"),
  ads: () => {
    const A = D.ads || { campaigns: [], accounts: [], invoices: [] }, m$ = (n) => "$" + Number(n || 0).toFixed(2);
    const live = A.campaigns.filter((c) => c.status === "active");
    const lastMonth = new Date(); lastMonth.setDate(1); lastMonth.setMonth(lastMonth.getMonth() - 1);
    const ym = (d) => d.toISOString().slice(0, 7) + "-01";
    const st = (s) => s === "active" ? '<span class="pill g">Running</span>' : s === "stopped" ? '<span class="pill r">Stopped</span>' : '<span class="pill">' + esc(s) + "</span>";
    return '<h1>Ads</h1><p class="lead muted">Ad income (FIG Premium, $50 a year, is switched on under Restaurants). Restaurants make ads on fig-promo.vercel.app/ads and pay per tap (the auction’s second price, from $0.30). Invoice each owner at the start of the month.</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
      '<div class="stats">' + stat(live.length, "Ads running", "blue") + stat(m$(A.accounts.reduce((a, x) => a + Number(x.spent_month || 0), 0)), "Spent this month") + stat(A.invoices.filter((x) => x.status !== "paid" && x.status !== "void").length, "Invoices not paid", "red") + "</div>" +
      "<h2>Campaigns</h2>" + table(["Restaurant", "Ad", "Status", "Budget", "Views", "Taps", "Spent (month)", ""], A.campaigns.map((c) => [
        "<b>" + esc(c.restaurant) + '</b><br><span class="muted">' + esc(c.owner_email || "") + "</span>", esc(c.name) + '<br><span class="muted">' + esc(c.goal) + (c.note ? " · " + esc(c.note) : "") + "</span>", st(c.status),
        m$(c.daily_budget) + "/day" + (c.bid ? '<br><span class="muted">max ' + m$(c.bid) + "</span>" : ""), c.views, c.taps + '<br><span class="muted">' + (c.views ? (100 * c.taps / c.views).toFixed(1) : "0") + "%</span>", m$(c.spend_month),
        c.status === "stopped" ? '<button class="link" data-run="' + c.id + '">Let it run</button>' : c.status === "active" || c.status === "paused" ? '<input class="f" id="cn-' + c.id + '" maxlength="300" placeholder="Why (the owner sees it)" style="width:170px"> <button class="link" data-stop="' + c.id + '">Stop</button>' : ""]),
        "No ads yet. They appear here the moment a restaurant launches one.") +
      "<h2>Ad accounts</h2>" + table(["Owner", "Restaurants", "This month", "Monthly limit", "Status", ""], A.accounts.map((a) => [
        "<b>" + esc(a.name || "") + '</b><br><span class="muted">' + esc(a.email || "") + "</span>", esc(a.restaurants || ""), m$(a.spent_month),
        '<input class="f" id="al-' + a.owner_id + '" type="number" min="0" step="10" value="' + Number(a.monthly_limit) + '" style="width:100px"> <button class="link" data-limit="' + a.owner_id + '">Save</button>',
        a.status === "held" ? '<span class="pill r">On hold</span>' : '<span class="pill g">Active</span>',
        '<button class="link" data-hold="' + a.owner_id + '" data-held="' + (a.status === "held" ? "0" : "1") + '">' + (a.status === "held" ? "Lift hold" : "Hold all ads") + "</button>"]),
        "No ad accounts yet. One opens with a restaurant’s first ad.") +
      '<h2>Invoices</h2><div class="act" style="margin:0 0 14px"><button class="btn" data-mk="' + ym(lastMonth) + '">Make invoices for ' + lastMonth.toLocaleDateString("en-CA", { month: "long" }) + '</button><button class="btn k" data-mk="' + ym(new Date()) + '">Preview this month so far</button></div>' +
      table(["Owner", "Month", "Amount", "Status", ""], A.invoices.map((x) => [
        "<b>" + esc(x.owner.name || "") + '</b><br><span class="muted">' + esc(x.owner.email || "") + "</span>", esc(new Date(x.month + "T12:00:00").toLocaleDateString("en-CA", { month: "long", year: "numeric" })), "<b>" + m$(x.amount) + "</b>",
        { open: '<span class="pill">To send</span>', sent: '<span class="pill">Sent ' + (x.sent_at ? when(x.sent_at) : "") + "</span>", paid: '<span class="pill g">Paid ' + (x.paid_at ? when(x.paid_at) : "") + "</span>", void: '<span class="pill r">Cancelled</span>' }[x.status],
        x.status === "open" ? '<button class="link" data-inv="' + x.id + '" data-to="sent">Mark sent</button>' : x.status === "sent" ? '<button class="link" data-inv="' + x.id + '" data-to="paid">Mark paid</button> <button class="link" style="margin-left:12px" data-inv="' + x.id + '" data-to="void">Cancel</button>' : ""]),
        "No invoices yet. Make them at the start of each month; each owner’s taps for that month become one invoice."));
  },
};

function render() {
  document.querySelectorAll("#nav button").forEach((b) => b.classList.toggle("on", b.dataset.v === view));
  const on = $("#nav .on"); if (on) on.parentNode.scrollLeft = on.offsetLeft - 16;
  $("#main").innerHTML = VIEWS[view]();
  if (view === "ads" && D.connected) {
    const run = async (what, body, ask) => { if (ask && !confirm(ask)) return; const r = await api(what, body); if (r.error) alert(r.error); await load(); render(); };
    document.querySelectorAll("[data-stop]").forEach((b) => b.onclick = () => run("ad-campaign", { id: b.dataset.stop, stop: true, note: ($("#cn-" + b.dataset.stop) || {}).value || "" }, "Stop this ad? It stops showing now, and the owner sees your note."));
    document.querySelectorAll("[data-run]").forEach((b) => b.onclick = () => run("ad-campaign", { id: b.dataset.run, stop: false }, "Let this ad run again?"));
    document.querySelectorAll("[data-prem]").forEach((b) => b.onclick = () => run("premium", { owner: b.dataset.prem, years: +b.dataset.years }, b.dataset.years === "0" ? "Turn off FIG Premium for this owner (all their locations)?" : "Switch on FIG Premium for a year for this owner (all their locations)?"));
    document.querySelectorAll("[data-limit]").forEach((b) => b.onclick = () => run("ad-account", { owner: b.dataset.limit, limit: +$("#al-" + b.dataset.limit).value }));
    document.querySelectorAll("[data-hold]").forEach((b) => b.onclick = () => run("ad-account", { owner: b.dataset.hold, held: b.dataset.held === "1" }, b.dataset.held === "1" ? "Hold all of this owner’s ads?" : "Lift the hold? Their ads can run again."));
    document.querySelectorAll("[data-mk]").forEach((b) => b.onclick = () => run("ad-invoices", { month: b.dataset.mk }, "Make (or update) the invoices for this month? Sent and paid ones aren’t changed."));
    document.querySelectorAll("[data-inv]").forEach((b) => b.onclick = () => run("ad-invoice", { id: b.dataset.inv, status: b.dataset.to }));
  }
}
async function load() {
  D = await api("data");
  const set = (id, n) => { $(id).textContent = n == null ? "–" : n; };
  if (D.connected) { set("#n-restaurants", D.counts.restaurants); set("#n-reports", D.counts.reports); set("#n-leads", D.leads.length); set("#n-ads", ((D.ads || {}).campaigns || []).filter((x) => x.status === "active").length); }
}
document.querySelectorAll("#nav button").forEach((b) => b.onclick = () => { view = b.dataset.v; if (D) render(); }); // before the data arrives, load() renders the chosen view
$("#out").onclick = async () => { await api("logout"); location.reload(); };
load().then(render).catch(() => { $("#main").innerHTML = '<div class="empty">Couldn\\'t load. Refresh to try again.</div>'; });
</script></body></html>`;
}

module.exports = { signInPage, appPage };
