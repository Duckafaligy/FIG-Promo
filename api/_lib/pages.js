// The admin pages (from the Paper designs: Admin 00 Sign in, 01 Overview, 02 Restaurants, 03 Reports, 04 Leads, 05 Access keys).
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
.pill.g { background: #E3F7EF; color: #067A55; } .pill.r { background: #FDECEC; color: #B4282D; } .pill.k { background: #F2F5FA; color: #5B6779; }
.mono { font-family: ui-monospace, Consolas, monospace; font-weight: 700; letter-spacing: .02em; }
.empty { padding: 26px; border-radius: 16px; background: #F2F5FA; color: #5B6779; font-size: 15px; line-height: 1.6; }
.empty b { color: #0A1020; }
.make { padding: 22px; border: 1px solid #E2E7EF; border-radius: 18px; margin-bottom: 28px; }
.row { display: grid; grid-template-columns: 1fr 140px 140px auto; gap: 12px; align-items: end; margin-top: 14px; }
.row label { display: block; font-size: 13px; font-weight: 700; margin-bottom: 6px; }
.new { margin-top: 16px; padding: 18px; border-radius: 14px; background: #C8F135; display: none; }
.new .codes { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; } .new .codes span { background: #fff; padding: 8px 12px; border-radius: 10px; }
.link { border: 0; background: none; padding: 0; color: #1E5EFF; font-weight: 800; cursor: pointer; } .link.red { color: #C9353A; margin-left: 14px; }
.note { font-size: 13px; color: #5B6779; }
@media (max-width: 900px) { .shell { grid-template-columns: 1fr; } aside { position: static; height: auto; flex-direction: row; flex-wrap: wrap; } .stats { grid-template-columns: 1fr 1fr; } .row { grid-template-columns: 1fr; } main { padding: 24px 18px; } .tbl { overflow-x: auto; } }`) + `<body>
<div class="shell">
  <aside>
    <div class="brand">${LOGO}FIG Admin</div>
    <div class="nav" id="nav">
      <button data-v="overview" class="on">Overview</button>
      <button data-v="restaurants">Restaurants <span class="badge" id="n-restaurants">–</span></button>
      <button data-v="reports">Reports <span class="badge" id="n-reports">–</span></button>
      <button data-v="leads">Leads <span class="badge" id="n-leads">–</span></button>
      <button data-v="diners">Diners</button>
      <button data-v="keys">Access keys <span class="badge" id="n-keys">–</span></button>
      <button data-v="plans">Plan codes <span class="badge" id="n-plans">–</span></button>
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

const VIEWS = {
  overview: () => '<h1>Overview</h1><p class="lead muted">Before launch · ' + days + ' days to January 1, 2027</p>' + (!D.connected ? NOT_CONNECTED :
    '<div class="stats">' + stat(D.counts.diners, "Diners signed up") + stat(D.counts.waiting, "Waiting on the early-bird page", "blue") + stat(D.counts.live, "Restaurants live") + stat(D.counts.reports, "Open reports", "red") + "</div>" +
    "<h2>Latest restaurants</h2>" + table(["Restaurant", "Cuisine", "City", "Status", "Joined"], D.restaurants.slice(0, 6).map((r) => ["<b>" + esc(r.name) + "</b>", esc(r.cuisine), esc(r.city), statusPill(r.status), ago(r.created_at)]), "No restaurants yet.")),
  restaurants: () => '<h1>Restaurants</h1><p class="lead muted">Every restaurant on FIG, newest first. A restaurant goes live when it finishes setup.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED :
    table(["Restaurant", "Cuisine", "City", "Status", "Joined"], D.restaurants.map((r) => ["<b>" + esc(r.name) + "</b>", esc(r.cuisine), esc(r.city), statusPill(r.status), ago(r.created_at)]), "No restaurants yet.")),
  reports: () => '<h1>Reports</h1><p class="lead muted">Visits diners or restaurants reported.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED :
    table(["Reason", "Details", "When", "Status"], D.reports.map((r) => ["<b>" + esc(r.reason) + "</b>", esc(r.details), ago(r.at), r.status === "open" ? '<span class="pill r">Open</span>' : '<span class="pill g">Settled</span>']), "No reports. Good news.")),
  leads: () => '<h1>Restaurant leads</h1><p class="lead muted">Restaurants that left their details on the website.</p><div style="height:24px"></div>' + (!D.connected ? NOT_CONNECTED :
    table(["Restaurant", "Contact", "Area", "Received", "From"], D.leads.map((l) => ["<b>" + esc(l.restaurant) + "</b>", esc(l.email || l.phone), esc(l.area), ago(l.created_at), esc(l.source)]), "No leads yet. They arrive from the website's sign-up form once the waitlist table is set up.")),
  diners: () => '<h1>Diners</h1><p class="lead muted">People signed up to FIG and on the website waitlist.</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
    '<div class="stats">' + stat(D.counts.diners, "Diner accounts") + stat(D.counts.waiting, "Waiting on the early-bird page", "blue") + stat(D.waitlist, "Website waitlist") + stat(days, "Days to launch") + "</div>"),
  keys: () => '<h1>Access keys</h1><p class="lead muted">Codes that let diners past the app\\'s early-bird page · ' + days + ' days to January 1, 2027</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
    '<div class="stats">' + stat(D.counts.waiting, "Waiting on the early-bird page") + stat(D.keys.reduce((n, k) => n + k.uses, 0), "Let in with a key", "blue") + stat(D.keys.length, "Keys made") + stat(D.keys.reduce((n, k) => n + Math.max(0, k.max_uses - k.uses), 0), "Uses left") + "</div>" +
    '<div class="make"><h2>Make keys</h2><p class="note">One key per person, or one key a whole group can use.</p><div class="row">' +
    '<div><label for="k-note">Who it\\'s for</label><input class="f" id="k-note" maxlength="80" placeholder="Pho Metro staff"></div>' +
    '<div><label for="k-n">How many keys</label><input class="f" id="k-n" type="number" min="1" max="100" value="3"></div>' +
    '<div><label for="k-u">People per key</label><input class="f" id="k-u" type="number" min="1" max="10000" value="1"></div>' +
    '<button class="btn" id="k-make">Make keys</button></div><div class="new" id="k-new"><b id="k-title"></b><div class="codes" id="k-codes"></div></div></div>' +
    "<h2>All keys</h2>" + table(["Key", "Who it's for", "Used", "Made", ""], D.keys.map((k) => ['<span class="mono">' + esc(k.code) + "</span>", esc(k.note), k.uses ? k.uses + " of " + k.max_uses : '<span class="pill">Not used yet</span>', ago(k.made_at),
      '<button class="link" data-copy="' + esc(k.code) + '">Copy</button><button class="link red" data-del="' + esc(k.code) + '">Delete</button>']), "No keys yet.") +
    '<p class="note">Restaurants don\\'t need a key. Deleting a key stops anyone new from using it; people it already let in stay in.</p>'),
  plans: () => '<h1>Plan codes</h1><p class="lead muted">Founding restaurants: their first year of FIG is on us. One code per restaurant; each works once.</p>' + (!D.connected ? '<div style="height:24px"></div>' + NOT_CONNECTED :
    '<div class="stats">' + stat(D.planCodes.length, "Codes made") + stat(D.planCodes.filter((k) => k.uses > 0).length, "Restaurants on a free year", "blue") + stat(D.planCodes.filter((k) => !k.uses).length, "Not used yet") + stat(D.counts.live, "Restaurants live") + "</div>" +
    '<div class="make"><h2>Make codes</h2><p class="note">Make one for the restaurant you\\'re visiting. They enter it in the app: Settings, Your FIG plan, Enter a code from FIG.</p><div class="row">' +
    '<div><label for="p-note">Which restaurant</label><input class="f" id="p-note" maxlength="80" placeholder="Golden Lantern, Kennedy & Bur Oak"></div>' +
    '<div><label for="p-n">How many codes</label><input class="f" id="p-n" type="number" min="1" max="50" value="1"></div>' +
    '<div></div><button class="btn" id="p-make">Make codes</button></div><div class="new" id="p-new"><b id="p-title"></b><div class="codes" id="p-codes"></div></div></div>' +
    "<h2>All plan codes</h2>" + table(["Code", "For", "Status", "Made", ""], D.planCodes.map((k) => ['<span class="mono">' + esc(k.code) + "</span>", esc(k.note),
      k.uses ? '<span class="pill g">Used by ' + esc(k.used_by.join(", ") || "a restaurant") + "</span>" : '<span class="pill">Not used yet</span>', ago(k.made_at),
      '<button class="link" data-pcopy="' + esc(k.code) + '">Copy</button><button class="link" style="margin-left:14px" data-card="' + esc(k.code) + '" data-for="' + esc(k.note) + '">Card</button><button class="link red" data-pdel="' + esc(k.code) + '">Delete</button>']), "No plan codes yet.") +
    '<p class="note">A used code can\\'t be used again, so it\\'s safe to hand over. Deleting a code stops it working; plans it already turned on keep running.</p>'),
};

// a printable "first year on us" card to hand a restaurant with its code
const CARD_LOGO = ${JSON.stringify(LOGO)};
function printCard(code, who) {
  const w = window.open("", "_blank");
  if (!w) return alert("Allow pop-ups to print the card.");
  w.document.write('<!doctype html><html><head><meta charset="utf-8"><title>FIG founding card</title><style>' +
    '@page{size:auto;margin:16mm}body{font-family:"Plus Jakarta Sans",system-ui,sans-serif;margin:0;display:grid;place-items:center;min-height:100vh;color:#0A1020}' +
    '.c{width:400px;border-radius:26px;padding:30px;color:#fff;background:linear-gradient(135deg,#3B78FF,#1E5EFF 42%,#1239B8);-webkit-print-color-adjust:exact;print-color-adjust:exact}' +
    '.b{display:flex;align-items:center;gap:10px;font-weight:800;font-size:15px;letter-spacing:.06em}.b span.m{display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:#fff}.b svg{width:28px;height:28px}' +
    '.p{display:inline-block;margin-top:22px;padding:6px 13px;border-radius:99px;background:#C8F135;color:#0A1020;font-weight:800;font-size:13px}' +
    'h1{font-size:34px;line-height:1.05;letter-spacing:-.03em;margin:12px 0 6px}.f{font-size:15px;opacity:.9;margin:0 0 20px}' +
    '.k{background:#fff;color:#0A1020;border-radius:16px;padding:16px;text-align:center}.k small{display:block;font-size:11px;font-weight:800;letter-spacing:.12em;color:#5B6779}.k b{display:block;font-family:ui-monospace,Consolas,monospace;font-size:24px;letter-spacing:.06em;margin-top:6px}' +
    'ol{margin:18px 0 0;padding-left:20px;font-size:13.5px;line-height:1.7}.n{margin-top:14px;font-size:12px;opacity:.75}</style></head><body><div class="c">' +
    '<div class="b"><span class="m">' + CARD_LOGO + '</span>FIG FOR RESTAURANTS</div>' +
    '<span class="p">Founding restaurant</span><h1>Your first year<br>of FIG is on us</h1><p class="f">' + esc(who || "Welcome to FIG") + '</p>' +
    '<div class="k"><small>YOUR CODE</small><b>' + esc(code) + '</b></div>' +
    '<ol><li>Open FIG and sign up as a restaurant</li><li>Settings, then Your FIG plan</li><li>Tap Enter a code from FIG and type this code</li></ol>' +
    '<div class="n">One-time code for this restaurant only. Free until a year after you enter it.</div></div></body></html>');
  w.document.close();
  w.focus();
  setTimeout(() => w.print(), 300);
}

function render() {
  document.querySelectorAll("#nav button").forEach((b) => b.classList.toggle("on", b.dataset.v === view));
  $("#main").innerHTML = VIEWS[view]();
  if (view === "keys" && D.connected) {
    $("#k-make").onclick = async () => {
      const r = await api("make-keys", { count: +$("#k-n").value, uses: +$("#k-u").value, note: $("#k-note").value });
      if (!r.codes) return alert(r.error || "Couldn't make keys.");
      await load(); view = "keys"; render();
      $("#k-new").style.display = "block"; $("#k-title").textContent = r.codes.length + " new keys" + ($("#k-note").value ? " · " + $("#k-note").value : "");
      $("#k-codes").innerHTML = r.codes.map((c) => '<span class="mono">' + esc(c) + "</span>").join("");
    };
    document.querySelectorAll("[data-copy]").forEach((b) => b.onclick = () => navigator.clipboard.writeText(b.dataset.copy).then(() => { b.textContent = "Copied"; }));
    document.querySelectorAll("[data-del]").forEach((b) => b.onclick = async () => { if (!confirm("Delete " + b.dataset.del + "?")) return; await api("delete-key", { code: b.dataset.del }); await load(); render(); });
  }
  if (view === "plans" && D.connected) {
    $("#p-make").onclick = async () => {
      const note = $("#p-note").value;
      const r = await api("make-plan-codes", { count: +$("#p-n").value, note });
      if (!r.codes) return alert(r.error || "Couldn't make codes.");
      await load(); view = "plans"; render();
      $("#p-new").style.display = "block"; $("#p-title").textContent = (r.codes.length === 1 ? "New code" : r.codes.length + " new codes") + (note ? " · " + note : "");
      $("#p-codes").innerHTML = r.codes.map((c) => '<span class="mono">' + esc(c) + "</span>").join("");
    };
    document.querySelectorAll("[data-pcopy]").forEach((b) => b.onclick = () => navigator.clipboard.writeText(b.dataset.pcopy).then(() => { b.textContent = "Copied"; }));
    document.querySelectorAll("[data-card]").forEach((b) => b.onclick = () => printCard(b.dataset.card, b.dataset.for));
    document.querySelectorAll("[data-pdel]").forEach((b) => b.onclick = async () => { if (!confirm("Delete " + b.dataset.pdel + "? It stops working; a plan it already turned on keeps running.")) return; await api("delete-plan-code", { code: b.dataset.pdel }); await load(); render(); });
  }
}
async function load() {
  D = await api("data");
  const set = (id, n) => { $(id).textContent = n == null ? "–" : n; };
  if (D.connected) { set("#n-restaurants", D.counts.restaurants); set("#n-reports", D.counts.reports); set("#n-leads", D.leads.length); set("#n-keys", D.counts.keys); set("#n-plans", D.planCodes.length); }
}
document.querySelectorAll("#nav button").forEach((b) => b.onclick = () => { view = b.dataset.v; if (D) render(); }); // before the data arrives, load() renders the chosen view
$("#out").onclick = async () => { await api("logout"); location.reload(); };
load().then(render).catch(() => { $("#main").innerHTML = '<div class="empty">Couldn\\'t load. Refresh to try again.</div>'; });
</script></body></html>`;
}

module.exports = { signInPage, appPage };
