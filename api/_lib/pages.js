// The admin pages. Redone for FIX-LIST #83 (user 2026-10-18: "only include blogs, waitlist, restaurants, overview, and whatever
// also makes sense; remodel everything"): Overview, Restaurants (+ Outreach), Waitlist, Blog, Inbox (Messages + Reports), and
// Security under the account, in the website's look (site/css/tokens.css) and at phone width. Hidden while they're switched off
// in the app, with their server actions left in admin-api.js: FIG Premium (PREMIUM_ON) and Ads (ADS_ON).
// The client script below sits inside a template literal: a backslash in it must be written twice.
const LOGO = `<svg width="30" height="30" viewBox="743 716 100 100" aria-hidden="true"><path fill="#1E5EFF" d="M765.637 809.875C755.252 806.459 749.184 797.508 749.184 785.965V751.1C749.184 735.317 761.319 722.714 776.955 722.714H836.699L831.098 730.252C827.014 735.906 822.346 738.968 814.762 738.968H777.189C770.888 738.968 765.754 744.15 765.754 750.629V755.341L767.621 753.574C770.304 751.218 772.989 750.158 776.722 750.158H800.06L790.725 762.526C788.275 765.941 785.24 767.354 780.923 767.354H772.405C768.671 767.354 765.637 770.299 765.637 774.304V809.875Z"/><path fill="#1E5EFF" d="M793.759 769.592H836.699V784.08C836.699 799.746 824.563 811.171 809.044 811.171H770.888V795.387H809.161C815.462 795.387 820.013 790.794 820.013 784.433V783.256H781.623L793.759 769.592Z"/><path fill="#14C86B" d="M797.142 765.705L805.194 755.104C807.877 751.689 811.145 750.158 815.696 750.158H836.699V754.28C836.699 761.347 832.265 765.705 825.264 765.705H797.142Z"/></svg>`;

const BASE = `
@font-face { font-family: "Jakarta"; src: url("/assets/PlusJakartaSans.ttf") format("truetype"); font-weight: 200 800; font-display: swap; }
*,*::before,*::after { box-sizing: border-box; } html,body { margin: 0; }
body { font-family: "Jakarta", system-ui, sans-serif; color: #0A1020; background: #EEF3FF; -webkit-font-smoothing: antialiased; }
h1,h2,h3,p { margin: 0; } button, input { font: inherit; color: inherit; }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 19px; letter-spacing: -0.02em; }
.btn { height: 48px; padding: 0 22px; border: 0; border-radius: 999px; background: #1E5EFF; color: #fff; font-weight: 800; font-size: 16px; cursor: pointer; box-shadow: 0 12px 28px rgba(30,94,255,.24); }
.btn:hover { background: #1550E6; }
.btn:disabled { opacity: .55; cursor: default; }
.btn.sm { height: 38px; padding: 0 16px; font-size: 14px; }
input.f, select.f { width: 100%; height: 48px; padding: 0 16px; border-radius: 12px; border: 1.5px solid #DCE4F7; background: #fff; font-size: 16px; outline: none; }
input.f:focus, select.f:focus { border-color: #1E5EFF; }
.muted { color: #66718A; }
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
  <label for="pw" id="pw-l">Password</label>
  <input class="f" id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
  <button class="btn" id="go" type="submit">Sign in</button>
  <p class="msg" id="msg" role="status" aria-live="polite"></p>
  <a class="back" href="/">Back to FIG</a>
</form>
<script>
const f = document.getElementById("f"), pw = document.getElementById("pw"), go = document.getElementById("go"), msg = document.getElementById("msg");
let timer, step = "password"; // "code" once the password is right and the authenticator step is on (FIX-LIST #83)
function codeStep(on) {
  step = on ? "code" : "password";
  document.getElementById("pw-l").textContent = on ? "Code from your authenticator app" : "Password";
  pw.type = on ? "text" : "password"; pw.autocomplete = on ? "one-time-code" : "current-password"; pw.inputMode = on ? "numeric" : "text";
  pw.placeholder = on ? "6 digits, or a backup code" : "";
  go.textContent = on ? "Continue" : "Sign in"; pw.value = ""; pw.focus();
}
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
  const code = step === "code";
  const r = await fetch("/api/admin-api?do=" + (code ? "login-code" : "login"), { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(code ? { code: pw.value } : { password: pw.value }) }).catch(() => null);
  const j = r ? await r.json().catch(() => ({})) : {};
  pw.value = "";
  if (j.needCode) { go.disabled = false; return codeStep(true); }
  if (j.again) codeStep(false);
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
.shell { display: grid; grid-template-columns: 248px 1fr; min-height: 100vh; }
aside { position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; gap: 6px; padding: 24px 16px; background: #fff; border-right: 1px solid #DCE4F7; }
aside .brand { padding: 0 10px 22px; }
.nav button { display: flex; justify-content: space-between; align-items: center; width: 100%; height: 44px; padding: 0 14px; border: 0; border-radius: 999px; background: none; text-align: left; font-weight: 700; font-size: 15px; cursor: pointer; }
.nav button:hover { background: #EEF3FF; }
.nav button.on { background: #0A1020; color: #fff; }
.badge { min-width: 24px; height: 22px; padding: 0 8px; border-radius: 99px; background: #EEF3FF; color: #0A1020; font-size: 12px; font-weight: 800; display: grid; place-items: center; }
.badge.hot, .nav button.on .badge { background: #C8F135; color: #0A1020; }
.who { margin-top: auto; padding: 0 12px; font-size: 13px; color: #66718A; }
.who button { margin-top: 8px; border: 0; background: none; padding: 0; color: #1E5EFF; font-weight: 700; cursor: pointer; font-size: 13px; }
.who button.on { color: #0A1020; text-decoration: underline; text-underline-offset: 3px; }
main { padding: 40px 40px 72px; min-width: 0; max-width: 1240px; }
h1 { font-size: 40px; letter-spacing: -0.035em; line-height: 1.1; } .lead { margin-top: 8px; font-size: 17px; }
.tabs { display: inline-flex; gap: 4px; padding: 4px; margin: 24px 0 22px; border-radius: 999px; background: #fff; border: 1px solid #DCE4F7; max-width: 100%; overflow-x: auto; }
.tabs button { height: 38px; padding: 0 16px; border: 0; border-radius: 999px; background: none; font-weight: 700; font-size: 14px; cursor: pointer; white-space: nowrap; }
.tabs button.on { background: #1E5EFF; color: #fff; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 26px 0 32px; }
.stat { padding: 22px; border-radius: 24px; background: #fff; box-shadow: 0 1px 2px rgba(10,16,32,.06), 0 2px 8px rgba(10,16,32,.05); }
.stat b { display: block; font-size: 36px; letter-spacing: -0.03em; } .stat span { color: #66718A; font-size: 14px; }
.stat.blue b { color: #1E5EFF; } .stat.red b { color: #D92D3A; }
h2 { font-size: 22px; letter-spacing: -0.02em; margin: 6px 0 12px; }
.tbl { border-radius: 24px; overflow: hidden; margin-bottom: 32px; background: #fff; box-shadow: 0 1px 2px rgba(10,16,32,.06), 0 2px 8px rgba(10,16,32,.05); }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { text-align: left; font-size: 13px; font-weight: 700; color: #66718A; padding: 14px 18px; border-bottom: 1px solid #DCE4F7; }
td { padding: 15px 18px; border-top: 1px solid #EEF3FF; vertical-align: top; }
.pill { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 800; background: #EEF3FF; color: #1E5EFF; }
.pill.g { background: #E3F7EF; color: #087A42; } .pill.r { background: #FDECEC; color: #B4282D; } .pill.k { background: #EEF3FF; color: #66718A; }
.mono { font-family: ui-monospace, Consolas, monospace; font-weight: 700; letter-spacing: .02em; }
.empty { padding: 26px; border-radius: 24px; background: #fff; color: #66718A; font-size: 15px; line-height: 1.6; margin-bottom: 18px; }
.empty b { color: #0A1020; }
.link { border: 0; background: none; padding: 0; color: #1E5EFF; font-weight: 800; cursor: pointer; text-decoration: none; } .link.red { color: #D92D3A; margin-left: 14px; }
.link:disabled { color: #A3ADBF; cursor: default; }
.note { font-size: 13px; color: #66718A; }
.red { color: #D92D3A; }
.line { display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; justify-content: space-between; }
.hint { margin-top: 14px; padding: 16px 18px; border-radius: 20px; font-size: 14px; background: #fff; line-height: 1.5; }
.hint.g { background: #E3F7EF; color: #087A42; } .hint.r { border: 1.5px solid #1E5EFF; } .hint.k { color: #0A1020; }
.act { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 16px; }
.act input { flex: 1; min-width: 200px; }
.btn.k { background: #0A1020; box-shadow: none; }
label input[type=checkbox] { margin-right: 6px; }
@media (max-width: 900px) {
  .shell { grid-template-columns: 1fr; }
  aside { z-index: 5; height: auto; display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 10px; padding: 12px 16px; border-right: 0; border-bottom: 1px solid #DCE4F7; }
  aside .brand { padding: 0; } .who { grid-column: 2; grid-row: 1; text-align: right; padding: 0; } .who br { display: none; } .who button { margin: 0 0 0 4px; }
  .nav { grid-column: 1 / -1; display: flex; gap: 6px; overflow-x: auto; margin: 0 -16px; padding: 0 16px; } .nav button { width: auto; flex-shrink: 0; gap: 8px; }
  .stats { grid-template-columns: 1fr 1fr; gap: 12px; } .stat { padding: 16px; border-radius: 20px; } .stat b { font-size: 28px; }
  main { padding: 24px 16px 56px; } h1 { font-size: 30px; } .tbl { overflow-x: auto; border-radius: 20px; } td, th { padding: 12px 14px; }
}`) + `<body>
<div class="shell">
  <aside>
    <div class="brand">${LOGO}FIG Admin</div>
    <div class="nav" id="nav">
      <button data-v="overview" class="on">Overview</button>
      <button data-v="restaurants">Restaurants <span class="badge" id="n-restaurants">–</span></button>
      <button data-v="waitlist">Waitlist <span class="badge" id="n-waitlist">–</span></button>
      <button data-v="blog">Blog <span class="badge" id="n-blog">–</span></button>
      <button data-v="inbox">Inbox <span class="badge" id="n-inbox">–</span></button>
    </div>
    <div class="who">Brendan · Owner<br><button id="sec" data-v="security">Security</button> · <button id="out">Sign out</button></div>
  </aside>
  <main id="main"><p class="muted">Loading…</p></main>
</div>
<script>
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const ago = (t) => { const m = Math.round((Date.now() - Date.parse(t)) / 60000); if (m < 1) return "just now"; if (m < 60) return m + " min ago"; if (m < 1440) return Math.round(m / 60) + " h ago"; const d = Math.round(m / 1440); return d === 1 ? "yesterday" : d + " days ago"; };
const LAUNCH = Date.parse("2027-01-01T00:00:00-05:00");
const days = Math.max(0, Math.ceil((LAUNCH - Date.now()) / 86400000));
let D = null, view = "overview";
const SUB = { restaurants: "fig", inbox: "messages" }; // the switch on Restaurants (On FIG / Outreach) and Inbox (Messages / Reports)
const tabs = (v, list) => '<div class="tabs" role="tablist">' + list.map(([k, label]) => '<button role="tab" data-sub="' + v + ":" + k + '" aria-selected="' + (SUB[v] === k) + '"' + (SUB[v] === k ? ' class="on"' : "") + ">" + label + "</button>").join("") + "</div>";
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

// who changed a restaurant's name or address, and who handed a restaurant to whom (kept by the database, 3 changes in 30 days at most)
function changesTable() {
  const name = (id) => ((D.restaurants || []).find((r) => r.id === id) || {}).name || "a restaurant";
  const who = (id) => ((D.owners || []).find((o) => o.id === id) || {}).email || "someone";
  const rows = (D.changes || []).map((c) => c.kind === "transfer"
    ? ['<span class="pill">Handed over</span>', "<b>" + esc(name(c.restaurant_id)) + "</b>", esc(who(c.before.owner)) + " → " + esc(who(c.after.owner) || c.after.to_email || ""), ago(c.at)]
    : ['<span class="pill">Details changed</span>', "<b>" + esc(name(c.restaurant_id)) + "</b>", esc([c.before.name !== c.after.name ? c.before.name + " → " + c.after.name : "", c.before.address !== c.after.address ? c.before.address + " → " + c.after.address : ""].filter(Boolean).join(" · ") || "location moved"), ago(c.at)]);
  return "<h2>Handovers and name changes</h2>" + table(["What", "Restaurant", "Detail", "When"], rows, "None yet. Changes to a restaurant’s name or address, and hand-overs between owners, are recorded here.");
}

// sign-in protection (FIX-LIST #83): the authenticator app and "Sign out everywhere"
function securityHtml() {
  return '<h1>Security</h1><p class="lead muted">Only you get in: your password, then a code from your phone.</p>' +
    '<h2>Authenticator app</h2><p>' + (D.totp ? '<span class="pill g">On</span> Signing in asks for a code from your authenticator app after the password.' : '<span class="pill">Off</span> Signing in uses the password only.') + '</p>' +
    '<div id="totp"><button class="btn" id="totp-go">' + (D.totp ? "Move it to a new phone" : "Set up an authenticator app") + '</button></div>' +
    '<h2>Sign out everywhere</h2><p class="muted">Signs out every browser, this one too, and forgets every remembered device. Use it if a computer was lost or you think someone else signed in.</p>' +
    '<button class="btn k" id="out-all">Sign out everywhere</button>';
}
function securityWire() {
  const box = $("#totp");
  $("#out-all").onclick = async () => {
    if (!confirm("Sign out every browser, including this one?")) return;
    const r = await api("logout-all"); if (r.error) return alert(r.error); location.reload();
  };
  $("#totp-go").onclick = async () => {
    const r = await api("totp-start"); if (r.error) return alert(r.error);
    box.innerHTML = '<ol><li>Open an authenticator app on your phone (Google Authenticator, Microsoft Authenticator, 1Password…) and add an account.</li>' +
      '<li>Scan this code, or type the key below.</li></ol><div style="margin:14px 0">' + r.qr + '</div>' +
      '<p>Key: <b style="font-family:monospace;letter-spacing:.06em">' + esc(r.secret) + '</b></p>' +
      '<label for="totp-c"><b>Then type the 6-digit code the app shows</b></label><div class="act"><input class="f" id="totp-c" inputmode="numeric" autocomplete="one-time-code" maxlength="6"><button class="btn" id="totp-ok">Check the code</button></div>' +
      '<p class="muted">This set-up times out in 10 minutes. Nothing changes until the last step.</p>';
    $("#totp-ok").onclick = async () => {
      const c = await api("totp-confirm", { code: $("#totp-c").value });
      if (c.error) return alert(c.error);
      box.innerHTML = '<p><span class="pill g">The code matched</span></p>' +
        (c.backup ? '<h2>Your backup codes</h2><p>Each one works once, if your phone is lost. Save them somewhere safe now: they are not shown again.</p><p style="font-family:monospace;font-size:16px;line-height:1.9">' + c.backup.map(esc).join("<br>") + '</p>'
          : '<p class="red">The backup codes couldn’t be saved (the database didn’t answer). Start again before you switch it on.</p>') +
        '<h2>Last step: switch it on in Vercel</h2><ol><li>Vercel → fig-promo → Settings → Environment Variables → Add.</li><li>Name: <b>' + esc(c.env) + '</b>. Value: <b style="font-family:monospace">' + esc(c.secret) + '</b>. Environment: Production. Mark it Sensitive.</li><li>Redeploy (Deployments → the latest → Redeploy).</li></ol>' +
        '<p class="muted">Until then, signing in stays password only. Afterwards, sign in once in a private window to check it, before you close this one.</p>';
    };
  };
}

const VIEWS = {
  security: () => securityHtml(),
  overview: () => '<h1>Overview</h1><p class="lead muted">Before launch · ' + days + ' days to January 1, 2027</p>' + (!D.connected ? NOT_CONNECTED :
    '<div id="launchbox">' + launchLine() + "</div>" + needsYou() +
    '<div class="stats">' + stat(D.counts.live, "Restaurants live", "blue") + stat(setup().length, "Restaurants in setup") + stat(D.counts.dealsLive, "Deals live now") +
    stat(D.counts.waitlist, "On the waitlist" + (D.counts.waitlist7 ? " · " + D.counts.waitlist7 + " new this week" : "")) + stat(D.counts.claims7, "Deals claimed this week") + stat(D.counts.scans7, "Scanned at the counter this week") +
    stat(D.counts.diners, "Diner accounts") + stat(D.counts.orders30, "Takeout orders, 30 days") + '<div class="stat"><b id="q-posts">–</b><span>Posts queued</span></div></div>' +
    '<div class="line"><h2>Latest restaurants</h2><button class="link" data-go="restaurants">See all</button></div>' + table(["Restaurant", "Cuisine", "City", "Status", "Joined"], D.restaurants.slice(0, 6).map((r) => ["<b>" + esc(r.name) + "</b>", esc(r.cuisine), esc(r.city), statusPill(r.status), ago(r.created_at)]), "No restaurants yet.")),
  restaurants: () => '<h1>Restaurants</h1><p class="lead muted">Who’s on FIG, and the places you could bring on.</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
    tabs("restaurants", [["fig", "On FIG · " + D.restaurants.length], ["outreach", "Outreach · " + D.leads.length + (D.leads.length === 1 ? " lead" : " leads")]]) +
    (SUB.restaurants === "outreach" ? outreachHtml()
      : '<p class="muted" style="margin:-8px 0 14px">Newest first. A restaurant goes live when it finishes setup.</p>' +
        table(["Restaurant", "Owner", "City", "Status", "Joined", "Payments"], D.restaurants.map((r) => {
          const b = (D.premium || []).find((x) => x.owner_id === r.owner_id) || {};
          const owner = (D.owners || []).find((o) => o.id === r.owner_id) || {};
          const pay = b.payments_demo ? '<span class="pill k">Pretend</span>' : b.stripe_ready && b.stripe_payouts ? '<span class="pill g">Live, ready</span>' : b.stripe_ready ? '<span class="pill">Live, bank needed</span>' : '<span class="pill k">Not set up</span>';
          return ["<b>" + esc(r.name) + '</b><br><span class="muted">' + esc(r.cuisine || "") + "</span>", esc(owner.name || "") + '<br><span class="muted">' + esc(owner.email || "") + '</span><br><button class="link" data-2fa="' + esc(r.owner_id) + '">Turn off two-step login</button>', esc(r.city), statusPill(r.status), ago(r.created_at), pay];
        }), "No restaurants yet.") + changesTable())),
  waitlist: () => '<h1>Waitlist</h1><p class="lead muted">The launch plan, and the diners waiting to get in.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED : '<div id="dinerbox">' + dinersHtml() + "</div>"),
  blog: () => '<h1>Blog</h1><p class="lead muted">Every post on the FIG blog. Take one down if you don’t like it, or put it back.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED : '<div id="blogbox">' + blogHtml() + "</div>"),
  inbox: () => '<h1>Inbox</h1><p class="lead muted">What people wrote to FIG, and visits that were reported.</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
    tabs("inbox", [["messages", "Messages" + (D.counts.support ? " · " + D.counts.support + " open" : "")], ["reports", "Reports" + (D.counts.reports ? " · " + D.counts.reports + " open" : "")]]) +
    (SUB.inbox === "reports"
      ? table(["Reason", "Details", "When", "Status"], D.reports.map((r) => ["<b>" + esc(r.reason) + "</b>", '<div style="max-width:520px;white-space:pre-wrap">' + esc(r.details) + "</div>", ago(r.at), r.status === "open" ? '<span class="pill r">Open</span>' : '<span class="pill g">Settled</span>']), "No reports. Good news.")
      : '<p class="muted" style="margin:-8px 0 14px">From “Message us” in the app and on the website. Reply by email, then mark it answered.</p>' +
        table(["From", "About", "Message", "When", ""], (D.support || []).map((m) => [
          '<a class="link" href="mailto:' + esc(m.email) + "?subject=" + encodeURIComponent("FIG: " + (m.topic || "your message")) + '">' + esc(m.email) + '</a><br><button class="link" data-2fa-email="' + esc(m.email) + '">Turn off two-step login</button>', esc(m.topic), '<div style="max-width:520px;white-space:pre-wrap">' + esc(m.body) + "</div>", ago(m.at),
          m.status === "open" ? '<button class="link" data-sup="' + esc(m.id) + '" data-to="answered">Mark answered</button>' : '<span class="pill g">Answered</span> <button class="link" data-sup="' + esc(m.id) + '" data-to="open">Reopen</button>']), "No messages. When someone writes to FIG, it shows up here."))),
};
// restaurants that started setup but aren't live (paused ones excluded), and the ones stuck there 3 days or more
const setup = () => D.restaurants.filter((r) => r.status !== "approved" && r.status !== "rejected");
// the Overview's "Needs you": what's waiting on the team, each one a link to where it's dealt with
function needsYou() {
  const stuck = setup().filter((r) => Date.now() - Date.parse(r.created_at) >= 3 * 86400000);
  const items = [];
  if (D.counts.support) items.push('<button class="link" data-go="inbox:messages">' + D.counts.support + (D.counts.support === 1 ? " message" : " messages") + " to answer</button>");
  if (D.counts.reports) items.push('<button class="link" data-go="inbox:reports">' + D.counts.reports + (D.counts.reports === 1 ? " open report" : " open reports") + "</button>");
  stuck.forEach((r) => items.push('<button class="link" data-go="restaurants:fig">' + esc(r.name) + "</button> has been in setup for " + Math.floor((Date.now() - Date.parse(r.created_at)) / 86400000) + " days"));
  return '<div class="hint"><div style="font-size:17px;font-weight:800;margin-bottom:6px">Needs you</div>' +
    (items.length ? items.map((x) => '<div style="padding:6px 0">' + x + "</div>").join("") : '<span class="muted">Nothing right now.</span>') + "</div>";
}
// Restaurants > Outreach: restaurants that left their details on the website, then every place in Markham to approach
function outreachHtml() {
  return "<h2>Leads from the website</h2>" + table(["Restaurant", "Contact", "Area", "Received", "From"], D.leads.map((l) => ["<b>" + esc(l.restaurant) + "</b>", esc(l.email || l.phone), esc(l.area), ago(l.created_at), esc(l.source)]), "No leads yet. Restaurants that fill in the website’s form show up here.") +
    '<h2>Every place in Markham</h2><p class="muted" style="margin:-4px 0 14px">Search, shortlist the ones to approach yourself, and keep notes. Only the FIG team sees this.</p><div id="prosbox">' + prosHtml() + "</div>";
}

// ---- Blog: every post, whether it is live, and the team's controls (table blog_overrides through /api/admin-api). Words stay in the site's code; this only takes a post down, puts it back or moves its time.
let BLOG = null;
const blogWhen = (t) => t ? new Date(t).toLocaleString("en-CA", { timeZone: "America/Toronto", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : "";
function blogHtml() {
  if (!BLOG) return '<p class="muted">Loading…</p>';
  if (BLOG.error) return '<div class="empty"><b>Could not load the posts.</b><br>' + esc(BLOG.error) + "</div>";
  const P = BLOG.posts || [];
  const live = P.filter((p) => p.status === "live").length, queued = P.filter((p) => p.status === "queued").length, down = P.filter((p) => p.status === "taken-down").length;
  const pill = (p) => p.status === "taken-down" ? '<span class="pill r">Taken down</span>' + (p.visible ? '<br><span class="note">Hidden for visitors now; removed completely at the next site update</span>' : "")
    : p.status === "queued" ? '<span class="pill">Goes live ' + esc(blogWhen(p.publish_at)) + "</span>"
    : p.visible === false ? '<span class="pill">Going live at the next site update</span>' : '<span class="pill g">Live</span>';
  const acts = (p) => {
    const s = esc(p.slug);
    if (p.status === "taken-down") return '<button class="link" data-bup="' + s + '">Put back</button>';
    if (p.status === "queued") return '<button class="link" data-bnow="' + s + '">Publish now</button><br><input class="f" type="datetime-local" id="bt-' + s + '" style="width:200px;height:38px;margin-top:6px"> <button class="link" data-btime="' + s + '">Save time</button>';
    return '<span style="display:flex;gap:16px;flex-wrap:wrap"><a class="link" href="/blog/' + s + '" target="_blank" rel="noopener">Open</a><button class="link red" style="margin:0" data-bdown="' + s + '">Take down</button></span>';
  };
  const warn = BLOG.hooks === false ? '<div class="hint r" style="margin:0 0 16px"><b>Not connected to the live blog yet.</b> Your choices are saved here, but the site does not act on them until the next site update that connects this page. Taking a post down will do nothing visible before then.</div>' : "";
  return warn + '<div class="stats">' + stat(live, "Posts live", "blue") + stat(queued, "Scheduled") + stat(down, "Taken down", down ? "red" : "") + stat(P.length, "Posts in total") + "</div>" +
    '<div class="empty" style="margin-bottom:18px"><b>How changes reach the site.</b> Taking a post down hides it for everyone within about a minute, and the next site update (within the hour) removes it completely. Publishing now or changing a time also takes effect at the next site update. Scheduled posts publish on their own at their time, at 12 am, 6 am, 12 pm or 6 pm Toronto time. Nothing here changes a post’s words.' +
    (BLOG.source === "live-site" ? "<br><br>Showing the posts on the live site for now (the full list with scheduled posts appears after the next site update)." : "") + "</div>" +
    table(["Post", "Status", "Date", "Words", ""], P.map((p) => [
      "<b>" + esc(p.title) + '</b><br><span class="muted mono">/blog/' + esc(p.slug) + "</span>" + (p.topic ? '<br><span class="muted">' + esc(p.topic) + "</span>" : ""),
      pill(p), esc(p.date || ""), p.words ? p.words.toLocaleString("en-CA") : "–", acts(p)]), "No posts yet.");
}
async function blogLoad() {
  BLOG = await api("blog-list").catch(() => ({ error: "The list did not load. Refresh to try again." }));
  const n = $("#n-blog"); if (n) n.textContent = BLOG.posts ? BLOG.posts.filter((p) => p.status === "live").length : "–";
  const q = $("#q-posts"); if (q) q.textContent = BLOG.posts ? BLOG.posts.filter((p) => p.status === "queued").length : "–";
  if (view === "blog" && $("#blogbox")) { $("#blogbox").innerHTML = blogHtml(); blogWire(); }
}
function blogWire() {
  const set = async (body, ask) => { if (ask && !confirm(ask)) return; const r = await api("blog-set", body); if (r.error) alert(r.error); await blogLoad(); };
  document.querySelectorAll("[data-bdown]").forEach((b) => b.onclick = () => set({ slug: b.dataset.bdown, hidden: true }, "Take this post down? It disappears for visitors within about a minute. You can put it back any time."));
  document.querySelectorAll("[data-bup]").forEach((b) => b.onclick = () => set({ slug: b.dataset.bup, hidden: false }));
  document.querySelectorAll("[data-bnow]").forEach((b) => b.onclick = () => set({ slug: b.dataset.bnow, publish_at: new Date(Date.now() - 60000).toISOString() }, "Publish this post now? It goes live at the next site update (within the hour)."));
  document.querySelectorAll("[data-btime]").forEach((b) => b.onclick = () => { const v = ($("#bt-" + b.dataset.btime) || {}).value; if (!v) return alert("Pick a date and time first."); set({ slug: b.dataset.btime, publish_at: new Date(v).toISOString() }); });
}

// ---- Diners: the switch that opens or closes the diner side, and the waitlist (table diner_waitlist through /api/admin-api)
let DIN = null;
// The launch plan (the user, 2026-10-17), the same panel on the Overview and the Diners tab:
// 1 collect the waitlist (closed) -> 2 the first N -> 3 the opening date (founding members get in by themselves then; the list closes then)
// -> 4 everyone. The effective mode comes from the database (site_mode), so a passed opening date shows as open to founding members.
// waitlist: setDinersMode closes the list now only the first time; a cutoff already set stays (FIX-LIST #57)
const MODE_ASK = {
  off: () => "Close FIG to diners and collect the waitlist? Diners see the waitlist; restaurants aren't affected.",
  waitlist: () => "Open to founding members now? People on the waitlist (the first N, if set) can sign in and use everything; " +
    (DIN.until ? "the list keeps its cutoff (" + atText(DIN.until) + "), so who joined before it gets in." : "the list closes now."),
  on: () => "Open FIG to everyone now? Anyone can sign up, browse, claim deals and order. This is the public launch.",
};
const atText = (iso) => new Date(iso).toLocaleString("en-CA", { dateStyle: "medium", timeStyle: "short" });
const localInput = (iso) => { if (!iso) return ""; const d = new Date(iso); const p = (n) => String(n).padStart(2, "0"); return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()) + "T" + p(d.getHours()) + ":" + p(d.getMinutes()); };
// what the opening date does depends on where FIG is now (FIX-LIST #56): the help under it and its Save confirm say so.
// The list closes at founding_closes() = coalesce(founding_until, opens_at): a founding cutoff, once set, always wins (#65).
// The switch still "off" but founding members in = they got in because the date passed: a new date or Clear shuts them out again (#66).
const dot = (s) => (s.endsWith(".") ? s : s + "."); // "12:00 a.m." already ends the sentence (#67)
const openedByDate = () => DIN.mode === "off" && (DIN.effective || DIN.mode) === "waitlist";
const passed = (iso) => !!iso && new Date(iso) <= new Date();
function opensHelp(eff) {
  if (eff === "on") return "FIG is already open to everyone. The date only shows on the website as the launch date.";
  const cutoffOf = (your) => DIN.until ? your + " founding cutoff (" + esc(atText(DIN.until)) + ") " + (passed(DIN.until) ? "closed" : "closes") + " the list" : "";
  const cutoff = cutoffOf("Your");
  if (openedByDate()) return "Founding members got in when this date passed" + (cutoff ? "; " + cutoffOf("your") : ", and the list closed then") + ". Saving a new date closes FIG to them again until that date; clearing it closes FIG to them again until you set a new date. To change it without shutting them out, open FIG to everyone (step 4).";
  if (eff === "waitlist") return cutoff ? cutoff + "; this date only shows on the website as the launch date." : "The list closes at this time (later sign-ups wait for the next wave).";
  return "At this time FIG opens to founding members by itself" + (cutoff ? ". " + cutoff + "." : ", and the list closes then (later sign-ups wait for the next wave).");
}
function opensAsk(eff, when) {
  if (eff === "on") return "Show " + when + " on the website as the launch date? FIG is already open to everyone; this changes nothing else.";
  if (openedByDate()) return "Founding members are in now. Saving " + when + " closes FIG to them again until then. Save it anyway?";
  if (eff === "waitlist") return DIN.until ? "Show " + when + " on the website as the launch date? Your founding cutoff (" + atText(DIN.until) + ") closes the list, so nothing else changes." : "Close the founding list on " + when + "? People who join after it wait for the next wave.";
  return "Open to founding members on " + when + "? Until then FIG stays closed to diners and keeps collecting the waitlist" + (DIN.until ? "; your founding cutoff (" + atText(DIN.until) + ") closes the list." : "; the list closes then.");
}
function nowText(eff, first) {
  return eff === "on" ? "<b>Right now: open to everyone.</b> Anyone can sign up, browse, claim and order."
    : eff === "waitlist" ? "<b>Right now: founding members are in.</b> " + first.charAt(0).toUpperCase() + first.slice(1) + " on the waitlist" + (DIN.closes ? " who joined before " + esc(atText(DIN.closes)) : "") + " can use FIG, plus restaurants. Everyone else sees the waitlist."
    : "<b>Right now: collecting the waitlist.</b> Only restaurants can use FIG; diners join the list." + (DIN.opens ? " Opens to founding members " + esc(dot(atText(DIN.opens))) : "");
}
// the Overview's line: where the launch stands, and the way to the full plan on Waitlist
function launchLine() {
  if (!DIN) return '<div class="hint"><span class="muted">Loading the launch plan…</span></div>';
  if (DIN.error) return '<div class="hint"><b>The launch plan could not load.</b> <button class="link" data-go="waitlist">Open Waitlist</button></div>';
  const eff = DIN.effective || DIN.mode;
  return '<div class="hint line"><span>' + nowText(eff, DIN.cap ? "the first " + DIN.cap.toLocaleString("en-CA") : "everyone") + " " + (DIN.waitlist || []).length.toLocaleString("en-CA") + ' on the list.</span><button class="link" data-go="waitlist">The launch plan</button></div>';
}
function modeHtml() {
  if (!DIN) return "";
  if (DIN.error) return '<div class="hint r" style="margin:0 0 18px"><b>The launch plan could not load.</b> ' + esc(DIN.error) + ' <button class="link" id="lnch-retry" style="margin-left:12px">Try again</button></div>';
  const n = (DIN.waitlist || []).length, agreed = (DIN.waitlist || []).filter((w) => w.consent).length, eff = DIN.effective || DIN.mode;
  const first = DIN.cap ? "the first " + DIN.cap.toLocaleString("en-CA") : "everyone";
  const now = nowText(eff, first);
  const row = (num, title, body) => '<div style="display:flex;gap:14px;padding:12px 0;border-top:1px solid #E3E8F2"><div style="flex:none;width:26px;height:26px;border-radius:50%;background:#1E5EFF;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center">' + num + '</div><div style="flex:1"><div style="font-weight:800;margin-bottom:6px">' + title + "</div>" + body + "</div></div>";
  const s1 = row(1, "Collect the waitlist", '<div class="muted" style="margin-bottom:8px">' + n.toLocaleString("en-CA") + " on the list · " + agreed.toLocaleString("en-CA") + " agreed to be emailed. Creator links: fig-promo.vercel.app/?src=their-name#waitlist</div>" +
    (eff === "off" ? '<span class="pill g">Collecting now</span>' : '<button class="link" data-mode="off">Close FIG to diners and collect the waitlist</button>'));
  const s2 = row(2, "How many get in first", '<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span>The first</span><input class="f" id="cap-n" type="number" min="1" placeholder="everyone" value="' + (DIN.cap || "") + '" style="width:120px;height:40px"><span>on the list</span><button class="link" id="cap-save">Save</button></div><div class="muted" style="margin-top:6px">Empty = everyone on the list. Raise it or clear it later to let the next wave in.</div>');
  const s3 = row(3, "Opening date", '<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><input class="f" id="opens-at" type="datetime-local" value="' + localInput(DIN.opens) + '" style="height:40px"><button class="link" id="opens-save">Save</button>' + (DIN.opens ? '<button class="link red" id="opens-clear">Clear</button>' : "") + "</div>" +
    '<div class="muted" style="margin-top:6px">' + opensHelp(eff) + (eff === "on" ? "" : " The website shows the date." + (openedByDate() ? "" : " " +
    "Send the launch email before it: it isn't sent automatically. Copy the emails that agreed, below; every email needs FIG's name, a mailing address and an unsubscribe line.")) + "</div>" +
    (eff === "waitlist" ? "" : '<div style="margin-top:8px"><button class="link" data-mode="waitlist">Or open to founding members now</button></div>'));
  const s4 = row(4, "Everyone", eff === "on" ? '<span class="pill g">Open to everyone</span>' : '<button class="link" data-mode="on">Open FIG to everyone (public launch)</button>');
  const extra = eff === "waitlist" ? '<div class="muted" style="margin-top:6px">The founding list ' + (DIN.closes ? (passed(DIN.closes) ? "closed " : "closes ") + esc(dot(atText(DIN.closes))) + " " : "is open. ") + '<button class="link" id="until-now">Let in everyone who joined until now</button></div>' : "";
  return '<div class="hint' + (eff === "on" ? "" : " r") + '" style="margin:0 0 18px"><div style="font-size:17px;font-weight:800;margin-bottom:4px">Launch plan</div><div style="margin-bottom:8px">' + now + "</div>" + s1 + s2 + s3 + s4 + extra + "</div>";
}
function modeWire() {
  const t = $("#lnch-retry"); if (t) t.onclick = () => dinersLoad();
  const after = async (r) => { if (r && r.error) alert(r.error); await dinersLoad(); };
  document.querySelectorAll("[data-mode]").forEach((b) => b.onclick = async () => { const m = b.dataset.mode; if (!confirm(MODE_ASK[m]())) return; after(await api("diners-set", { mode: m })); });
  const cs = $("#cap-save"); if (cs) cs.onclick = async () => { const v = ($("#cap-n") || {}).value || ""; after(await api("founding-cap", { cap: v === "" ? null : Number(v) })); };
  const os = $("#opens-save"); if (os) os.onclick = async () => {
    const v = ($("#opens-at") || {}).value || ""; if (!v) return alert("Pick a date and time first.");
    const at = new Date(v); if (isNaN(at) || at < new Date()) return alert("Pick a time in the future.");
    if (!confirm(opensAsk(DIN.effective || DIN.mode, atText(at.toISOString())))) return;
    after(await api("opens-at", { at: at.toISOString() }));
  };
  const oc = $("#opens-clear"); if (oc) oc.onclick = async () => { if (!confirm(openedByDate() ? "Founding members are in now. Clearing the date closes FIG to them again until you set a new date. Clear it anyway?" : "Clear the opening date?")) return; after(await api("opens-at", { at: null })); };
  const un = $("#until-now"); if (un) un.onclick = async () => { if (!confirm("Let in everyone who has joined the list until now (within the first N, if set)? Later sign-ups still wait.")) return; after(await api("founding-until", { until: "now" })); };
}
function dinersHtml() {
  if (!DIN) return '<p class="muted">Loading…</p>';
  if (DIN.error) return '<div class="empty"><b>Could not load this.</b><br>' + esc(DIN.error) + "</div>";
  const W = DIN.waitlist || [], agreed = W.filter((w) => w.consent).length;
  const by = {}; W.forEach((w) => { const k = w.source || "website"; by[k] = (by[k] || 0) + 1; });
  const sources = Object.entries(by).sort((a, b) => b[1] - a[1]);
  return modeHtml() + '<div class="stats">' + stat(W.length, "On the waitlist", "blue") + stat(agreed, "Agreed to be emailed") + stat(DIN.accounts, "Diner accounts") + "</div>" +
    "<h2>Where sign-ups came from</h2>" + table(["Link", "Sign-ups"], sources.map((x) => [esc(x[0]), String(x[1])]), "No sign-ups yet. Give each creator a link like fig-promo.vercel.app/?src=their-name#waitlist") +
    '<div style="display:flex;gap:16px;margin:16px 0 14px;flex-wrap:wrap"><button class="link" id="din-copy">Copy the emails that agreed</button><button class="link" id="din-csv">Download as a table (CSV)</button></div>' +
    table(["Email", "School", "May email", "From", "Joined"], W.slice(0, 300).map((w) => [esc(w.email), esc(w.school || ""), w.consent ? '<span class="pill g">Yes</span>' : '<span class="pill">No</span>', esc(w.source || "website"), ago(w.joined_at)]), "Nobody yet.");
}
async function dinersLoad() {
  DIN = await api("diners-get").catch(() => ({ error: "It did not load. Refresh to try again." }));
  const n = $("#n-waitlist"); if (n && DIN.waitlist) n.textContent = DIN.waitlist.length;
  if (view === "overview" && $("#launchbox")) { $("#launchbox").innerHTML = launchLine(); goWire(); }
  if (view === "waitlist" && $("#dinerbox")) { $("#dinerbox").innerHTML = dinersHtml(); dinersWire(); }
}
function dinersWire() {
  modeWire();
  const rows = (DIN && DIN.waitlist) || [];
  const cp = $("#din-copy"); if (cp) cp.onclick = async () => { const t = rows.filter((w) => w.consent).map((w) => w.email).join(", "); try { await navigator.clipboard.writeText(t); alert(rows.filter((w) => w.consent).length + " emails copied."); } catch { prompt("Copy these:", t); } };
  const cs = $("#din-csv"); if (cs) cs.onclick = () => {
    const q = (v) => '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"';
    const csv = ["email,school,may_email,source,joined"].concat(rows.map((w) => [q(w.email), q(w.school), w.consent ? "yes" : "no", q(w.source), q(w.joined_at)].join(","))).join("\\n");
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" })); a.download = "fig-diner-waitlist.csv"; a.click();
  };
}

// ---- Prospects: the places directory with the team's shortlist / status / note (through /api/admin-api -> prospect_list, prospect_set)
let PRO = null; const PF = { q: "", kind: "", status: "", short: false, independent: true, hideFig: false, offset: 0 };
const PSTATS = [["new", "Not contacted"], ["contacted", "Contacted"], ["interested", "Interested"], ["not-interested", "Not interested"], ["signed", "Signed up"]];
const mapsUrl = (p) => "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(p.name + " " + p.street + " Markham Ontario");
function prosHtml() {
  if (!PRO) return '<p class="muted">Loading…</p>';
  if (PRO.error) return '<div class="empty"><b>Could not load this.</b><br>' + esc(PRO.error) + "</div>";
  const kinds = '<option value="">All kinds</option>' + (PRO.kinds || []).map((k) => '<option value="' + esc(k) + '"' + (PF.kind === k ? " selected" : "") + ">" + esc(k.replace(/_/g, " ")) + "</option>").join("");
  const stat2 = '<option value="">Any status</option>' + PSTATS.map((s) => '<option value="' + s[0] + '"' + (PF.status === s[0] ? " selected" : "") + ">" + s[1] + "</option>").join("");
  const bar = '<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:0 0 16px"><input class="f" id="pr-q" placeholder="Search name, street or postcode" value="' + esc(PF.q) + '" style="width:300px;height:44px"> <select class="f" id="pr-kind" style="height:44px">' + kinds + '</select> <select class="f" id="pr-status" style="height:44px">' + stat2 + '</select>' +
    '<label><input type="checkbox" id="pr-short"' + (PF.short ? " checked" : "") + "> Shortlist only</label><label><input type=\\"checkbox\\" id=\\"pr-ind\\"" + (PF.independent ? " checked" : "") + "> Independents only (hide big chains)</label><label><input type=\\"checkbox\\" id=\\"pr-fig\\"" + (PF.hideFig ? " checked" : "") + "> Hide ones already on FIG</label> <button class=\\"btn\\" id=\\"pr-go\\" style=\\"height:44px\\">Search</button></div>";
  const from = PRO.total ? PF.offset + 1 : 0, to = Math.min(PF.offset + 50, PRO.total);
  const rows = (PRO.rows || []).map((p) => [
    '<button class="link" data-star="' + esc(p.id) + '" data-on="' + (p.shortlisted ? 1 : 0) + '" title="Shortlist" style="font-size:24px;margin:0">' + (p.shortlisted ? "★" : "☆") + "</button>",
    "<b>" + esc(p.name) + "</b>" + (p.chain ? ' <span class="pill">Chain</span>' : "") + (p.on_fig ? ' <span class="pill g">On FIG</span>' : "") + '<br><span class="muted">' + esc(p.street) + (p.postcode ? ", " + esc(p.postcode) : "") + '</span><br><a class="link" href="' + esc(mapsUrl(p)) + '" target="_blank" rel="noopener">Open in Maps</a>',
    esc((p.kind || "").replace(/_/g, " ")),
    '<select class="f" data-st="' + esc(p.id) + '" style="height:40px">' + PSTATS.map((s) => '<option value="' + s[0] + '"' + (p.status === s[0] ? " selected" : "") + ">" + s[1] + "</option>").join("") + "</select>" + (p.contacted_at ? '<br><span class="muted">First contact ' + ago(p.contacted_at) + "</span>" : ""),
    '<input class="f" data-note="' + esc(p.id) + '" value="' + esc(p.note || "") + '" placeholder="Notes: who to ask for, when to come back" maxlength="500" style="width:100%;min-width:240px;height:40px">']);
  return '<div class="stats">' + stat(PRO.places, "Places in Markham") + stat(PRO.shortlisted, "Shortlisted", "blue") + stat(PRO.contacted, "Contacted") + stat(PRO.interested, "Interested") + stat(PRO.signed, "On FIG") + "</div>" + bar +
    '<p class="muted" style="margin:0 0 10px">' + PRO.total.toLocaleString("en-CA") + " places match. Showing " + from + "–" + to + ". Your shortlist comes first.</p>" +
    table(["", "Place", "Kind", "Status", "Notes"], rows, "No places match.") +
    '<div style="display:flex;gap:16px;margin:16px 0"><button class="link" id="pr-prev"' + (PF.offset ? "" : " disabled") + ">← Previous 50</button><button class=\\"link\\" id=\\"pr-next\\"" + (to < PRO.total ? "" : " disabled") + ">Next 50 →</button></div>";
}
async function prosLoad() {
  PRO = await api("prospects-list", PF).catch(() => ({ error: "It did not load. Refresh to try again." }));
  if (view === "restaurants" && SUB.restaurants === "outreach" && $("#prosbox")) { $("#prosbox").innerHTML = prosHtml(); prosWire(); }
}
function prosWire() {
  const read = () => { PF.q = ($("#pr-q") || {}).value || ""; PF.kind = ($("#pr-kind") || {}).value || ""; PF.status = ($("#pr-status") || {}).value || ""; PF.short = !!($("#pr-short") || {}).checked; PF.independent = !!($("#pr-ind") || {}).checked; PF.hideFig = !!($("#pr-fig") || {}).checked; };
  const go = () => { read(); PF.offset = 0; prosLoad(); };
  const g = $("#pr-go"); if (g) g.onclick = go;
  const q = $("#pr-q"); if (q) q.onkeydown = (e) => { if (e.key === "Enter") go(); };
  ["#pr-kind", "#pr-status", "#pr-short", "#pr-ind", "#pr-fig"].forEach((s) => { const el = $(s); if (el) el.onchange = go; });
  const pv = $("#pr-prev"), nx = $("#pr-next");
  if (pv) pv.onclick = () => { read(); PF.offset = Math.max(0, PF.offset - 50); prosLoad(); };
  if (nx) nx.onclick = () => { read(); PF.offset += 50; prosLoad(); };
  const save = async (body) => { const r = await api("prospects-set", body); if (r.error) alert(r.error); };
  document.querySelectorAll("[data-star]").forEach((b) => b.onclick = async () => { const on = b.dataset.on === "1"; await save({ id: b.dataset.star, short: !on }); read(); prosLoad(); });
  document.querySelectorAll("[data-st]").forEach((s) => s.onchange = async () => { await save({ id: s.dataset.st, status: s.value }); read(); prosLoad(); });
  document.querySelectorAll("[data-note]").forEach((i) => i.onchange = () => save({ id: i.dataset.note, note: i.value }));
}

// links that move to another view (the Overview's "See all" and "The launch plan")
function goWire() { document.querySelectorAll("[data-go]").forEach((b) => b.onclick = () => { const [v, k] = b.dataset.go.split(":"); view = v; if (k) SUB[v] = k; render(); scrollTo(0, 0); }); }
function render() {
  document.querySelectorAll("#nav button, #sec").forEach((b) => b.classList.toggle("on", b.dataset.v === view));
  const on = $("#nav .on"); if (on) on.parentNode.scrollLeft = on.offsetLeft - 16;
  $("#main").innerHTML = VIEWS[view]();
  goWire();
  document.querySelectorAll("[data-sub]").forEach((b) => b.onclick = () => { const [v, k] = b.dataset.sub.split(":"); SUB[v] = k; render(); });
  if (D.connected) {
    const run = async (what, body, ask) => { if (ask && !confirm(ask)) return; const r = await api(what, body); if (r.error) alert(r.error); await load(); render(); };
    document.querySelectorAll("[data-2fa],[data-2fa-email]").forEach((b) => b.onclick = async () => {
      if (!confirm("Turn off two-step login for this person? Only after checking it is really them: they write from the account's email and know the phone number on it. They then sign in with their password alone, and can switch two-step login back on.")) return;
      const r = await api("two-step-off", b.dataset["2fa"] ? { id: b.dataset["2fa"] } : { email: b.dataset["2faEmail"] });
      alert(r.error || (r.found === false ? "No FIG account has that email." : r.removed ? r.removed + " authenticator(s) removed. They can sign in with the password now." : "That account had no two-step login to remove."));
    });
    document.querySelectorAll("[data-sup]").forEach((b) => b.onclick = () => run("support", { id: b.dataset.sup, status: b.dataset.to }));
  }
  if (view === "security") securityWire();
  if ((view === "blog" || view === "overview") && D.connected) blogLoad();
  if ((view === "waitlist" || view === "overview") && D.connected) dinersLoad();
  if (view === "restaurants" && SUB.restaurants === "outreach" && D.connected) prosLoad();
}
async function load() {
  D = await api("data");
  const set = (id, n) => { const el = $(id); if (el) el.textContent = n == null ? "–" : n; };
  if (D.connected) {
    set("#n-restaurants", D.counts.restaurants);
    const open = (D.counts.support || 0) + (D.counts.reports || 0);
    set("#n-inbox", open); const nb = $("#n-inbox"); if (nb) nb.classList.toggle("hot", open > 0);
  }
}
document.querySelectorAll("#nav button, #sec").forEach((b) => b.onclick = () => { view = b.dataset.v; if (D) render(); }); // before the data arrives, load() renders the chosen view
$("#out").onclick = async () => { await api("logout"); location.reload(); };
load().then(() => { render(); if (D.connected && view !== "waitlist" && view !== "overview") dinersLoad(); }).catch(() => { $("#main").innerHTML = '<div class="empty">Couldn\\'t load. Refresh to try again.</div>'; });
</script></body></html>`;
}

module.exports = { signInPage, appPage };
