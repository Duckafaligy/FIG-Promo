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
input.f, select.f { width: 100%; height: 48px; padding: 0 16px; border-radius: 12px; border: 1.5px solid #7D8798; background: #fff; font-size: 16px; outline: none; }
input.f:focus, select.f:focus { border-color: #1E5EFF; } input.f:focus-visible, select.f:focus-visible { outline: 3px solid #1E5EFF; outline-offset: 2px; }
.muted { color: #66718A; }
:focus-visible { outline: 3px solid #1E5EFF; outline-offset: 2px; }`;

const head = (title, extra) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>${title}</title><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><style>${BASE}${extra}</style></head>`;

function signInPage(nonce = "") { // nonce: the response's own (api/admin.js, FIX-LIST #160)
  return head("FIG Admin", `
body { min-height: 100vh; display: grid; place-items: center; padding: 20px; }
.card { width: 100%; max-width: 420px; padding: 32px; border-radius: 24px; background: #fff; box-shadow: 0 30px 60px rgba(10,16,32,.08); }
h1 { margin-top: 28px; font-size: 28px; letter-spacing: -0.03em; }
.sub { margin-top: 6px; font-size: 15px; }
label { display: block; margin: 22px 0 8px; font-weight: 700; font-size: 14px; }
.btn { width: 100%; margin-top: 18px; }
.msg { margin-top: 14px; font-size: 14px; font-weight: 600; min-height: 20px; }
.msg.err { color: #C9353A; } .lock { color: #0A1020; }
.back { display: inline-block; margin-top: 18px; font-size: 13px; color: #5B6779; }
.alt { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; } .alt[hidden], #enrol[hidden], #f[hidden] { display: none; }
.linkb { background: none; border: 0; padding: 0; font: inherit; font-size: 14px; font-weight: 700; color: #1E5EFF; cursor: pointer; }
#enrol ol { padding-left: 20px; margin: 12px 0; font-size: 14px; } #enrol .qr { display: inline-block; padding: 8px; background: #fff; border-radius: 12px; margin: 8px 0; }
#enrol .key, #enrol .codes { font-family: ui-monospace, Consolas, monospace; font-size: 15px; word-break: break-all; } #enrol .codes { line-height: 1.9; margin: 8px 0; }
#enrol .row { display: flex; gap: 8px; margin-top: 8px; } #enrol .row input { flex: 1; } #enrol .row .btn { width: auto; margin: 0; }
#enrol .tick { display: flex; gap: 10px; align-items: flex-start; font-weight: 600; margin-top: 16px; } #enrol h2 { font-size: 18px; margin-top: 20px; }
@media (prefers-color-scheme: dark) { body { background: #0B0E15; color: #EEF2F8; } .card { background: #121722; box-shadow: none; border: 1px solid #232B3B; }
  input.f { background: #0B0E15; border-color: #646F84; color: #EEF2F8; } .muted, .back { color: #97A3B8; } .lock { color: #EEF2F8; } }`) + `<body>
<form class="card" id="f" autocomplete="off">
  <div class="brand">${LOGO}FIG Admin</div>
  <h1>Sign in</h1>
  <p class="sub muted">Only the FIG team gets in.</p>
  <label for="pw" id="pw-l">Password</label>
  <input class="f" id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
  <button class="btn" id="go" type="submit">Sign in</button>
  <div class="alt" id="alt" hidden><button class="linkb" type="button" id="by-mail" hidden>Email me a code instead</button><button class="linkb" type="button" id="by-text" hidden>Text me a code instead</button></div>
  <p class="msg" id="msg" role="status" aria-live="polite"></p>
  <a class="back" href="/">Back to FIG</a>
</form>
<div class="card" id="enrol" hidden aria-live="polite"></div>
<script nonce="${nonce}">
const f = document.getElementById("f"), pw = document.getElementById("pw"), go = document.getElementById("go"), msg = document.getElementById("msg");
let timer, step = "password"; // "code" once the password is right and the authenticator step is on (FIX-LIST #83)
function codeStep(on, j) {
  step = on ? "code" : "password";
  // the second step is always on (FIX-LIST #103); a code by email or text where one was set up
  document.getElementById("alt").hidden = !on || !(j && (j.mail || j.text));
  document.getElementById("by-mail").hidden = !(on && j && j.mail); document.getElementById("by-text").hidden = !(on && j && j.text);
  document.getElementById("pw-l").textContent = on ? "Code from your authenticator app" : "Password";
  pw.type = on ? "text" : "password"; pw.autocomplete = on ? "one-time-code" : "current-password"; pw.inputMode = on ? "numeric" : "text";
  pw.placeholder = on ? "6 digits, or a backup code" : "";
  document.getElementById("pw-l").textContent = on ? "Code from your authenticator app (or the one we sent)" : "Password";
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
  if (j.needCode) { go.disabled = false; codeStep(true, j); if (j.resetUsed) { msg.className = "msg err"; msg.textContent = "That reset value was already used. Set a new one in Vercel (for example today’s date), or delete ADMIN_TOTP_RESET."; } return; }
  if (j.needEnrol) return enrol(j);
  if (j.again) codeStep(false);
  if (r && r.ok) return location.reload();
  if (j.locked) return locked(j.retryIn);
  go.disabled = false; msg.className = "msg err";
  msg.textContent = j.error ? j.error + (j.triesLeft != null ? " " + j.triesLeft + (j.triesLeft === 1 ? " try" : " tries") + " left before a lock." : "") : "Couldn't reach the server.";
  pw.focus();
});
const post = (what, body) => fetch("/api/admin-api?do=" + what, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) })
  .then((r) => r.json().catch(() => ({}))).catch(() => ({ error: "Couldn't reach the server." }));
for (const [id, via] of [["by-mail", "mail"], ["by-text", "text"]]) document.getElementById(id).onclick = async () => {
  const j = await post("login-send", { via });
  msg.className = "msg"; msg.textContent = j.sent || j.error || ""; if (j.again) codeStep(false); pw.focus();
};
// the first sign-in (or after the user's reset): set up the authenticator before anything else (FIX-LIST #103)
async function enrol(first) {
  const box = document.getElementById("enrol"), H = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  f.hidden = true; box.hidden = false;
  const say = (t, bad) => { const m = box.querySelector(".msg"); if (m) { m.className = "msg" + (bad ? " err" : ""); m.textContent = t || ""; } };
  const s = await post("enrol-start");
  if (!s.ok) { box.innerHTML = '<p class="msg err">' + H(s.error || "That didn't work.") + '</p><a class="back" href="/admin">Start again</a>'; return; }
  box.innerHTML = '<div class="brand">${LOGO}FIG Admin</div><h1>Set up your second step</h1><p class="sub muted">Signing in needs a code from your phone every time. This takes a minute, once.</p>' +
    '<ol><li>Open an authenticator app (Google Authenticator, Microsoft Authenticator, 1Password…) and add an account.</li><li>Scan this, or type the key.</li></ol>' +
    '<div class="qr">' + s.qr + '</div><p class="key">Key: ' + H(s.secret) + '</p>' +
    '<label for="ec">Then type the 6-digit code the app shows</label><div class="row"><input class="f" id="ec" inputmode="numeric" autocomplete="one-time-code" maxlength="6"><button class="btn" id="ec-go" type="button">Check</button></div>' +
    '<p class="msg" role="status"></p><p class="muted" style="font-size:13px">Nothing is saved until the last step. This times out in 15 minutes.</p>';
  box.querySelector("#ec").focus();
  box.querySelector("#ec-go").onclick = async () => {
    const c = await post("enrol-code", { code: box.querySelector("#ec").value });
    if (c.locked) return say("Too many tries. Wait a few minutes, then sign in again.", true);
    if (!c.ok) return say((c.error || "That didn't work.") + (c.triesLeft != null ? " " + c.triesLeft + " tries left." : ""), true);
    box.innerHTML = '<div class="brand">${LOGO}FIG Admin</div><h1>Save your backup codes</h1><p class="sub muted">If your phone is lost, each of these signs you in once. They aren’t shown again.</p>' +
      '<p class="codes">' + c.backup.map(H).join("<br>") + '</p>' +
      (s.mail ? '<h2>Codes by email too (optional)</h2><p class="muted" style="font-size:14px">One address that can get a sign-in code instead. A code goes to it now to check it.</p>' +
        '<div class="row"><input class="f" id="em" type="email" autocomplete="email" placeholder="you@example.com"><button class="btn" id="em-go" type="button">Send a code</button></div>' +
        '<div class="row" id="em2" hidden><input class="f" id="emc" inputmode="numeric" maxlength="6" placeholder="6 digits"><button class="btn" id="emc-go" type="button">Confirm</button></div>'
        : '<p class="muted" style="font-size:14px;margin-top:16px">Email codes can’t be sent yet: the server has no email sender set up. Backup codes are your way back meanwhile.</p>') +
      '<label class="tick"><input type="checkbox" id="kept"> I saved these codes somewhere safe</label>' +
      '<button class="btn" id="done" type="button" disabled>Finish and sign in</button><p class="msg" role="status"></p>';
    const kept = box.querySelector("#kept"), done = box.querySelector("#done");
    kept.onchange = () => { done.disabled = !kept.checked; };
    const eg = box.querySelector("#em-go");
    if (eg) {
      eg.onclick = async () => { const r = await post("enrol-contact", { via: "email", to: box.querySelector("#em").value }); if (!r.ok) return say(r.error, true); box.querySelector("#em2").hidden = false; say("A code is on its way to " + r.to + "."); box.querySelector("#emc").focus(); };
      box.querySelector("#emc-go").onclick = async () => { const r = await post("enrol-contact-ok", { code: box.querySelector("#emc").value }); if (!r.ok) return say(r.error, true); say("Confirmed: codes can go to " + r.to + "."); box.querySelector("#em2").hidden = true; };
    }
    done.onclick = async () => {
      done.disabled = true;
      const d = await post("enrol-done", { saved: kept.checked });
      if (d.ok && d.removeFlag) {
        box.innerHTML = '<div class="brand">${LOGO}FIG Admin</div><h1>Your new phone is set up</h1><p class="sub">Last step: in Vercel, delete <b>ADMIN_TOTP_RESET</b> (Settings → Environment Variables) and redeploy. Until then every admin page shows a red line.</p><a class="btn" href="/admin" style="display:block;text-align:center;margin-top:18px">Open the admin</a>';
        return;
      }
      if (d.ok) return location.reload();
      done.disabled = false; say(d.error || "That didn't work.", true);
    };
  };
}
</script></body></html>`;
}

// FIX-LIST #85 v2 (the user: "use actual graphs, a real inbox to see everything in detail, buttons, a calendar, the entire UI
// should be better"): the same actions and security as a859985, rebuilt as a console. Charts with axes, gridlines and hover
// (7, 30 or 90 days), side panels for a restaurant, a waitlist person and a post, a two-pane inbox (j / k / e), a calendar, one
// button system with spinners, in-page confirm dialogs and toasts, Ctrl/⌘K search, skeletons while loading, dark mode.
// Reads only: the new actions (charts, restaurant-get, person-get) change nothing. Type 12/14/16/20/28/40, 8 px spacing, cobalt
// the one accent, lime only for good news; cards rise 40 ms apart, 150 ms hovers, the Snap curve; none with reduced motion.
const ICON = {
  overview: '<path d="M4 4h6v7H4zM14 4h6v4h-6zM14 12h6v8h-6zM4 15h6v5H4z"/>',
  restaurants: '<path d="M4 10l1.5-5h13L20 10M4 10v10h16V10M4 10h16M9 20v-5h6v5"/>',
  paid: '<path d="M3 6h18v12H3zM3 10h18M7 15h4"/>',
  waitlist: '<path d="M16 19v-1a4 4 0 00-4-4H7a4 4 0 00-4 4v1M9.5 10a3.5 3.5 0 100-7 3.5 3.5 0 000 7zM21 19v-1a4 4 0 00-3-3.9M16 3.1a3.5 3.5 0 010 6.8"/>',
  calendar: '<path d="M4 6h16v14H4zM4 10h16M8 3v5M16 3v5"/>',
  blog: '<path d="M6 3h9l4 4v14H6zM14 3v5h5M9 13h7M9 17h5"/>',
  inbox: '<path d="M3 13l3-8h12l3 8v6H3zM3 13h5l1 3h6l1-3h5"/>',
  security: '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/>',
  out: '<path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h10"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  chevron: '<path d="M9 6l6 6-6 6"/>',
  back: '<path d="M15 6l-6 6 6 6"/>',
  close: '<path d="M6 6l12 12M18 6L6 18"/>',
  search: '<path d="M11 18a7 7 0 100-14 7 7 0 000 14zM20 20l-4-4"/>',
  refresh: '<path d="M20 11a8 8 0 10-2.3 5.7M20 4v7h-7"/>',
  more: '<path d="M5 12h.01M12 12h.01M19 12h.01"/>',
  mail: '<path d="M4 6h16v12H4zM4 7l8 6 8-6"/>',
};
const icon = (n, size = 20) => `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON[n]}</svg>`;
const NAV = [["overview", "Overview"], ["restaurants", "Restaurants"], ["paid", "Paid restaurants"], ["waitlist", "Waitlist"], ["calendar", "Calendar"], ["blog", "Blog"], ["inbox", "Support"]];
const TABS = [["overview", "Overview"], ["restaurants", "Restaurants"], ["waitlist", "Waitlist"], ["inbox", "Support"]]; // a phone: these four, and More for the rest

const APP_CSS = `
:root { --bg: #F6F8FC; --panel: #FFFFFF; --line: #E4E9F2; --line2: #EEF2F8; --text: #0A1020; --muted: #5F6A82; --faint: #636E84; --edge: #7D8798;
  --accent: #1E5EFF; --accent-hover: #1550E6; --accent-soft: #EEF3FF; --on-accent: #FFFFFF; --lime: #C8F135; --good: #0B7A3E; --good-soft: #E6F6EC;
  --bad: #C8323C; --bad-soft: #FDECEC; --hover: #F3F6FB; --sk: #EDF1F7; --scrim: rgba(10,16,32,.32); --shadow: 0 1px 2px rgba(10,16,32,.04), 0 1px 1px rgba(10,16,32,.03);
  --float: 0 24px 60px rgba(10,16,32,.18); --c1: #1E5EFF; --c2: #66718A; --c3: #14A85A; --c4: #8A95A9; --c5: #C27A10; --c6: #8B5CF6; --c7: #E5484D; --c8: #0D93A1; --snap: cubic-bezier(.2,.8,.2,1); color-scheme: light; }
@media (prefers-color-scheme: dark) { :root { --bg: #0B0E15; --panel: #121722; --line: #232B3B; --line2: #1A2130; --text: #EEF2F8; --muted: #97A3B8; --faint: #8792A6; --edge: #646F84;
  --accent: #6B95FF; --accent-hover: #86A8FF; --accent-soft: rgba(30,94,255,.16); --on-accent: #0B0E15; --good: #7FE0A3; --good-soft: rgba(20,200,107,.14);
  --bad: #FF8A8F; --bad-soft: rgba(217,45,58,.16); --hover: #171E2B; --sk: #1A2130; --scrim: rgba(0,0,0,.55); --shadow: none; --float: 0 24px 60px rgba(0,0,0,.5);
  --c1: #6B95FF; --c2: #7C8AA5; --c3: #4CC982; --c4: #66728A; --c5: #F5B556; --c6: #A78BFA; --c7: #F2777B; --c8: #34C3D1; color-scheme: dark; } }
body { background: var(--bg); color: var(--text); font-size: 14px; line-height: 1.45; }
a { color: inherit; } .ic { flex: none; display: block; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.shell { display: grid; grid-template-columns: 240px minmax(0, 1fr); min-height: 100vh; }
.side { position: sticky; top: 0; height: 100vh; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; padding: 16px 12px; background: var(--panel); border-right: 1px solid var(--line); }
.side .brand { padding: 8px 12px 24px; font-size: 16px; } .side .brand span { color: var(--muted); font-weight: 600; }
.nav { display: flex; flex-direction: column; gap: 2px; }
.nav button, .side .acct button { display: flex; align-items: center; gap: 12px; width: 100%; height: 40px; padding: 0 12px; border: 0; border-radius: 12px; background: none; color: var(--muted);
  text-align: left; font-weight: 600; font-size: 14px; cursor: pointer; transition: background .15s var(--snap), color .15s var(--snap); }
.nav button:hover, .side .acct button:hover { background: var(--hover); color: var(--text); }
.nav button.on, .side .acct button.on { background: var(--accent-soft); color: var(--accent); }
.nav .label { flex: 1; }
.badge { min-width: 22px; height: 20px; padding: 0 6px; border-radius: 99px; background: var(--line2); color: var(--muted); font-size: 12px; font-weight: 700; display: grid; place-items: center; font-variant-numeric: tabular-nums; }
.badge.hot { background: var(--accent); color: var(--on-accent); }
.badge[hidden] { display: none; }
.side .acct { margin-top: auto; padding-top: 12px; border-top: 1px solid var(--line); display: flex; flex-direction: column; gap: 2px; }
.who { display: flex; align-items: center; gap: 12px; padding: 8px 12px 12px; }
.avatar { width: 32px; height: 32px; border-radius: 99px; background: var(--accent); color: var(--on-accent); display: grid; place-items: center; font-weight: 800; font-size: 14px; flex: none; }
.who b { display: block; font-size: 14px; } .who span { color: var(--muted); font-size: 12px; }
.top { position: sticky; top: 0; z-index: 4; min-height: 64px; display: flex; align-items: center; gap: 12px; padding: 8px 32px; background: color-mix(in srgb, var(--bg) 88%, transparent); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }
.top h1 { font-size: 20px; letter-spacing: -0.02em; } .top .sub { color: var(--muted); font-size: 14px; }
.top .grow { flex: 1; min-width: 0; }
.top .actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.top .mark, .top .more { display: none; }
.upd { color: var(--muted); font-size: 12px; white-space: nowrap; }
.kbd { font-size: 12px; color: var(--faint); border: 1px solid var(--line); border-radius: 6px; padding: 0 6px; margin-left: 8px; }
main { padding: 24px 32px 64px; max-width: 1280px; min-width: 0; }
.lead { color: var(--muted); font-size: 16px; margin: 0 0 24px; }
h2 { font-size: 16px; letter-spacing: -0.01em; margin: 32px 0 12px; display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
h2 .count { color: var(--muted); font-weight: 600; } h2 .push { margin-left: auto; }
h3 { font-size: 14px; margin: 0 0 8px; }
.muted { color: var(--muted); } .note { font-size: 12px; color: var(--muted); }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; box-shadow: var(--shadow); }
.grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
.grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid.six { grid-template-columns: repeat(6, minmax(0, 1fr)); }
.charts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.stat { padding: 16px; display: flex; flex-direction: column; gap: 8px; min-height: 128px; }
.stat .k { color: var(--muted); font-size: 14px; font-weight: 600; }
.stat .v { font-size: 28px; font-weight: 800; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; line-height: 1.1; }
.stat .row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-top: auto; }
.mini { padding: 12px 16px; } .mini .k { color: var(--muted); font-size: 12px; font-weight: 600; } .mini .v { font-size: 20px; font-weight: 800; font-variant-numeric: tabular-nums; }
.delta { display: inline-flex; align-items: center; gap: 4px; height: 22px; padding: 0 8px; border-radius: 99px; font-size: 12px; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }
.delta.up { background: var(--lime); color: #0A1020; } .delta.down { background: var(--bad-soft); color: var(--bad); } .delta.flat { background: var(--line2); color: var(--muted); }
.spark { display: block; color: var(--c1); }
.chartcard { padding: 16px 16px 8px; min-width: 0; }
.chartcard .head { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
.chartcard .head b { font-size: 14px; } .chartcard .head .big { font-size: 20px; font-weight: 800; font-variant-numeric: tabular-nums; }
.hbars { display: grid; gap: 6px; margin: 8px 0 12px; } .hb { display: grid; grid-template-columns: minmax(0, 150px) 1fr auto; align-items: center; gap: 10px; font-size: 13px; }
.hb span { color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; } .hb i { display: block; height: 10px; width: var(--w); border-radius: 99px; background: var(--c1); } .hb b { font-variant-numeric: tabular-nums; }
.src .tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; } .src .note { margin: 8px 0; } .srcnote { padding: 16px; }
.linktool { padding: 16px; } .lt-form { display: grid; grid-template-columns: auto 180px minmax(0, 1fr); gap: 12px; align-items: end; } .lt-form label { display: grid; gap: 6px; font-size: 12px; font-weight: 700; color: var(--muted); }
.lt-out { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin: 14px 0 8px; } .lt-out code { font-size: 13px; padding: 8px 10px; border-radius: 8px; background: var(--line2); overflow-wrap: anywhere; max-width: 100%; }
.lt-qr { flex-basis: 100%; display: flex; align-items: flex-end; gap: 12px; flex-wrap: wrap; } .lt-qr svg { width: 180px; height: 180px; border-radius: 8px; border: 1px solid var(--line); }
@media (max-width: 760px) { .lt-form { grid-template-columns: 1fr; } .hb { grid-template-columns: minmax(0, 110px) 1fr auto; } }
.legend { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--muted); margin: 4px 0 8px; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
.chart { position: relative; width: 100%; touch-action: pan-y; }
.chart svg { display: block; overflow: visible; }
.chart text { fill: var(--faint); font-size: 12px; font-family: inherit; font-variant-numeric: tabular-nums; }
.tip { position: absolute; top: 0; pointer-events: none; padding: 8px 12px; border-radius: 12px; background: var(--text); color: var(--panel); font-size: 12px; white-space: nowrap; box-shadow: var(--float); z-index: 2; }
.tip b { display: block; margin-bottom: 2px; } .tip i { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 6px; }
.seg { display: inline-flex; gap: 2px; padding: 2px; border-radius: 10px; background: var(--line2); }
.seg button { height: 28px; padding: 0 10px; border: 0; border-radius: 8px; background: none; color: var(--muted); font-weight: 700; font-size: 12px; cursor: pointer; font-variant-numeric: tabular-nums; }
.seg button.on { background: var(--panel); color: var(--text); box-shadow: var(--shadow); }
.needs { padding: 16px; margin-bottom: 16px; }
.needs .head { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.needs .head b { font-size: 16px; } .dot { width: 32px; height: 32px; border-radius: 99px; display: grid; place-items: center; background: var(--accent-soft); color: var(--accent); flex: none; }
.needs.clear .dot { background: var(--good-soft); color: var(--good); }
.item { display: flex; align-items: center; gap: 12px; width: 100%; padding: 12px 8px; border: 0; border-top: 1px solid var(--line2); background: none; color: var(--text); text-align: left; font-size: 14px; cursor: pointer; border-radius: 8px; transition: background .15s var(--snap); }
.item:hover { background: var(--hover); } .item .t { flex: 1; } .item .ic { color: var(--faint); }
.launch { padding: 16px; display: flex; flex-wrap: wrap; gap: 8px 24px; align-items: center; margin-bottom: 16px; }
.launch .days { font-size: 28px; font-weight: 800; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.launch .t { flex: 1; min-width: 240px; color: var(--muted); } .launch .t b { color: var(--text); }
.tools { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 12px; }
.search { position: relative; flex: 1; min-width: 200px; max-width: 360px; }
.search .ic { position: absolute; left: 12px; top: 10px; color: var(--faint); }
.search input { width: 100%; height: 40px; padding: 0 12px 0 40px; border-radius: 12px; border: 1px solid var(--edge); background: var(--panel); color: var(--text); font-size: 14px; outline: none; transition: border-color .15s var(--snap); }
.search input:focus { border-color: var(--accent); }
.tbl { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; overflow: auto; max-height: 72vh; margin-bottom: 24px; box-shadow: var(--shadow); }
table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; }
th { position: sticky; top: 0; z-index: 1; background: var(--panel); text-align: left; font-size: 12px; font-weight: 700; color: var(--muted); padding: 12px 16px; border-bottom: 1px solid var(--line); white-space: nowrap; }
td { padding: 12px 16px; border-bottom: 1px solid var(--line2); vertical-align: middle; }
tr:last-child td { border-bottom: 0; }
tbody tr { transition: background .15s var(--snap); } tbody tr:hover { background: var(--hover); }
tbody tr[data-open] { cursor: pointer; }
th.n, td.n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
td .sub, .sub { display: block; color: var(--muted); font-size: 12px; margin-top: 2px; }
.who-cell { display: flex; align-items: center; gap: 12px; min-width: 200px; }
.thumb { width: 36px; height: 36px; border-radius: 10px; object-fit: cover; flex: none; background: var(--accent-soft); color: var(--accent); display: grid; place-items: center; font-weight: 800; font-size: 14px; }
.thumb.big { width: 56px; height: 56px; border-radius: 14px; font-size: 20px; }
.pill { display: inline-flex; align-items: center; gap: 6px; height: 22px; padding: 0 8px; border-radius: 99px; font-size: 12px; font-weight: 700; background: var(--line2); color: var(--muted); white-space: nowrap; }
.pill::before { content: ""; width: 6px; height: 6px; border-radius: 99px; background: currentColor; }
.pill.g { background: var(--good-soft); color: var(--good); } .pill.b { background: var(--accent-soft); color: var(--accent); } .pill.r { background: var(--bad-soft); color: var(--bad); }
.empty { padding: 32px 24px; text-align: center; color: var(--muted); } .empty b { color: var(--text); display: block; margin-bottom: 4px; }
.link { border: 0; background: none; padding: 0; color: var(--accent); font-weight: 700; font-size: 14px; cursor: pointer; text-decoration: none; }
.link:hover { color: var(--accent-hover); } .link.red { color: var(--bad); } .link:disabled { color: var(--faint); cursor: default; }
.b { display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 36px; padding: 0 14px; border-radius: 10px; border: 1px solid transparent; font: inherit; font-weight: 700; font-size: 14px; cursor: pointer; white-space: nowrap; text-decoration: none;
  transition: background .15s var(--snap), border-color .15s var(--snap), color .15s var(--snap); }
.b.primary { background: var(--accent); color: var(--on-accent); } .b.primary:hover { background: var(--accent-hover); }
.b.secondary { background: var(--panel); color: var(--text); border-color: var(--edge); } .b.secondary:hover { background: var(--hover); }
.b.ghost { background: none; color: var(--muted); } .b.ghost:hover { background: var(--hover); color: var(--text); }
.b.danger { background: var(--bad-soft); color: var(--bad); } .b.danger:hover { border-color: var(--bad); }
.b.icon { width: 36px; padding: 0; }
.b:disabled, .b[aria-busy="true"] { opacity: .6; cursor: default; }
.spin { width: 14px; height: 14px; border-radius: 99px; border: 2px solid currentColor; border-right-color: transparent; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
input.f, select.f { height: 36px; border-radius: 10px; border: 1px solid var(--edge); background: var(--panel); color: var(--text); font-size: 14px; padding: 0 12px; outline: none; }
input.f:focus, select.f:focus { border-color: var(--accent); }
/* FIX-LIST #159: every field shows the focus ring, not only a border colour; a skip link; text only screen readers get */
input.f:focus-visible, select.f:focus-visible, .search input:focus-visible, .dialog textarea:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.palette input:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
tr:has(.row-open:focus-visible) { outline: 2px solid var(--accent); outline-offset: -2px; } /* the row's button is hidden: its row shows the ring */
.skip { position: absolute; left: 8px; top: -60px; z-index: 50; padding: 8px 14px; border-radius: 10px; background: var(--accent); color: var(--on-accent); font-weight: 700; text-decoration: none; } .skip:focus { top: 8px; }
.tabs { display: inline-flex; gap: 4px; padding: 4px; margin: 0 0 16px; border-radius: 12px; background: var(--line2); max-width: 100%; overflow-x: auto; }
.tabs button { height: 32px; padding: 0 12px; border: 0; border-radius: 8px; background: none; color: var(--muted); font-weight: 700; font-size: 14px; cursor: pointer; white-space: nowrap; transition: background .15s var(--snap), color .15s var(--snap); }
.tabs button.on { background: var(--panel); color: var(--text); box-shadow: var(--shadow); }
.steps { padding: 8px 16px; margin-bottom: 24px; }
.wl-plan { padding: 8px 16px; margin-bottom: 24px; } .wl-row { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line2); flex-wrap: wrap; }
.wl-k { display: grid; gap: 2px; min-width: 0; flex: 1 1 260px; } .wl-k b { font-size: 15px; } .wl-counts { padding: 12px 0 4px; }
.switch { width: 52px; height: 30px; border-radius: 99px; border: 0; background: var(--line); position: relative; cursor: pointer; flex: none; transition: background .2s; }
.switch span { position: absolute; top: 3px; left: 3px; width: 24px; height: 24px; border-radius: 99px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.25); transition: transform .2s var(--snap); }
.switch.on { background: var(--accent); } .switch.on span { transform: translateX(22px); }
.more-opts { margin: 8px 0 8px; } .more-opts summary { cursor: pointer; font-weight: 700; padding: 10px 0; color: var(--accent); }
.more-opts .mo { display: grid; gap: 6px; padding: 12px 0; border-top: 1px solid var(--line2); }
.step { display: grid; grid-template-columns: 32px minmax(0, 1fr); gap: 16px; position: relative; padding: 16px 0; }
.step:not(:last-child)::after { content: ""; position: absolute; left: 15px; top: 52px; bottom: -8px; width: 2px; background: var(--line); }
.step.done:not(:last-child)::after { background: var(--accent); }
.mk { width: 32px; height: 32px; border-radius: 99px; display: grid; place-items: center; font-weight: 800; font-size: 14px; border: 2px solid var(--line); color: var(--muted); background: var(--panel); position: relative; z-index: 1; }
.step.done .mk { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }
.step.now .mk { border-color: var(--accent); color: var(--accent); box-shadow: 0 0 0 4px var(--accent-soft); }
.step .title { font-weight: 800; font-size: 16px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 4px; }
.step .body { color: var(--muted); } .step .body b { color: var(--text); }
.ctl { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 8px; color: var(--text); }
.state { padding: 16px; margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-start; }
.hint { margin: 0 0 16px; padding: 12px 16px; border-radius: 12px; background: var(--accent-soft); font-size: 14px; } .hint.r { background: var(--bad-soft); }
.mono { font-family: ui-monospace, Consolas, monospace; font-weight: 700; letter-spacing: .02em; }
.red { color: var(--bad); }
label input[type=checkbox] { margin-right: 6px; accent-color: var(--accent); }
.sk { background: var(--sk); border-radius: 8px; }
.skrow { height: 14px; margin: 12px 0; } .skcard { height: 128px; border-radius: 16px; }
dl.kv { display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 8px 16px; margin: 0; } dl.kv dt { color: var(--muted); } dl.kv dd { margin: 0; overflow-wrap: anywhere; }
.checks { display: grid; gap: 8px; } .checks div { display: flex; align-items: center; gap: 8px; }
.checks .ok { color: var(--good); } .checks .no { color: var(--faint); }
.bar { height: 6px; border-radius: 99px; background: var(--line2); overflow: hidden; margin: 8px 0 12px; } .bar i { display: block; height: 100%; background: var(--accent); border-radius: 99px; }
.list > div { display: flex; justify-content: space-between; gap: 12px; padding: 8px 0; border-top: 1px solid var(--line2); } .list > div:first-child { border-top: 0; }
/* side panel, dialogs, toasts, the search */
.scrim { position: fixed; inset: 0; z-index: 20; background: var(--scrim); animation: fade .2s var(--snap) both; }
.panel { position: fixed; top: 0; right: 0; bottom: 0; z-index: 21; width: min(560px, 100%); background: var(--panel); border-left: 1px solid var(--line); box-shadow: var(--float); display: flex; flex-direction: column; animation: slide .24s var(--snap) both; outline: none; }
.panel header { display: flex; align-items: center; gap: 12px; padding: 16px 24px; border-bottom: 1px solid var(--line); }
.panel header h2 { margin: 0; flex: 1; font-size: 20px; min-width: 0; }
.panel .body { padding: 24px; overflow: auto; flex: 1; } .panel section { margin-bottom: 24px; }
.panel iframe { width: 100%; height: 360px; border: 1px solid var(--line); border-radius: 12px; background: #fff; }
.dialog { position: fixed; left: 50%; top: 18vh; transform: translateX(-50%); z-index: 31; width: min(440px, calc(100% - 32px)); padding: 24px; border-radius: 16px; background: var(--panel); border: 1px solid var(--line); box-shadow: var(--float); animation: pop .2s var(--snap) both; outline: none; }
.dialog h2 { margin: 0 0 8px; font-size: 20px; } .dialog p { color: var(--muted); margin: 0 0 16px; }
.dialog .ctl { justify-content: flex-end; margin-top: 16px; } .dialog textarea { width: 100%; min-height: 120px; border-radius: 10px; border: 1px solid var(--edge); background: var(--bg); color: var(--text); padding: 8px; font: inherit; }
.scrim.top { z-index: 30; }
.toasts { position: fixed; right: 24px; bottom: 24px; z-index: 40; display: flex; flex-direction: column; gap: 8px; align-items: flex-end; pointer-events: none; }
.toast { padding: 12px 16px; border-radius: 12px; background: var(--text); color: var(--panel); font-weight: 600; box-shadow: var(--float); animation: pop .2s var(--snap) both; max-width: 360px; }
.toast.bad { background: var(--bad); color: #fff; }
.palette { position: fixed; left: 50%; top: 12vh; transform: translateX(-50%); z-index: 31; width: min(600px, calc(100% - 32px)); border-radius: 16px; background: var(--panel); border: 1px solid var(--line); box-shadow: var(--float); overflow: hidden; animation: pop .2s var(--snap) both; }
.palette input { width: 100%; height: 56px; border: 0; border-bottom: 1px solid var(--line); background: none; color: var(--text); font-size: 16px; padding: 0 20px; outline: none; }
.palette ul { list-style: none; margin: 0; padding: 8px; max-height: 50vh; overflow: auto; }
.palette li button { display: flex; align-items: center; gap: 12px; width: 100%; padding: 10px 12px; border: 0; border-radius: 10px; background: none; color: var(--text); text-align: left; font-size: 14px; cursor: pointer; }
.palette li button[aria-selected="true"] { background: var(--accent-soft); } .palette li .kind { margin-left: auto; color: var(--faint); font-size: 12px; }
/* inbox */
.inbox { display: grid; grid-template-columns: 360px minmax(0, 1fr); height: calc(100vh - 160px); min-height: 480px; overflow: hidden; }
.inbox .ib-list { border-right: 1px solid var(--line); display: flex; flex-direction: column; min-height: 0; }
.inbox .ib-list .tools { padding: 12px; margin: 0; border-bottom: 1px solid var(--line); }
.inbox .rows { overflow: auto; flex: 1; }
.msg { display: block; width: 100%; padding: 12px 16px; border: 0; border-bottom: 1px solid var(--line2); background: none; color: var(--text); text-align: left; cursor: pointer; font-size: 14px; }
.msg:hover { background: var(--hover); } .msg.on { background: var(--accent-soft); }
.msg .l1 { display: flex; gap: 8px; align-items: center; } .msg .l1 b { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.msg .snip { color: var(--muted); font-size: 12px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-top: 2px; }
.msg .new { width: 8px; height: 8px; border-radius: 99px; background: var(--accent); flex: none; }
.thread { overflow: auto; padding: 24px; min-width: 0; }
.thread .bodytext { white-space: pre-wrap; font-size: 16px; line-height: 1.6; padding: 16px; border-radius: 12px; background: var(--bg); margin: 16px 0; }
.thread .back { display: none; }
/* calendar */
.cal { padding: 0; overflow: hidden; }
.cal .dow, .cal .days { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); }
.cal .dow div { padding: 8px 12px; font-size: 12px; font-weight: 700; color: var(--muted); border-bottom: 1px solid var(--line); }
.cal .day { min-height: 112px; padding: 8px; border-right: 1px solid var(--line2); border-bottom: 1px solid var(--line2); min-width: 0; }
.cal .day:nth-child(7n) { border-right: 0; } .cal .day.out { background: var(--bg); } .cal .day.out .n { color: var(--faint); }
.cal .day .n { font-size: 12px; font-weight: 700; color: var(--muted); margin-bottom: 4px; font-variant-numeric: tabular-nums; }
.cal .day.today .n { display: inline-grid; place-items: center; min-width: 22px; height: 22px; border-radius: 99px; background: var(--accent); color: var(--on-accent); }
.cal.week .day { min-height: 320px; }
.ev { display: block; width: 100%; margin: 0 0 4px; padding: 2px 6px; border: 0; border-radius: 6px; font-size: 12px; font-weight: 600; text-align: left; cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; background: var(--line2); color: var(--text); }
.ev.post { background: var(--accent-soft); color: var(--accent); } .ev.launch { background: var(--good-soft); color: var(--good); } .ev.cut { background: var(--bad-soft); color: var(--bad); }
.ev.deal { background: none; border: 1px solid var(--line); color: var(--muted); } .ev .more { color: var(--muted); }
.callegend { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.rise { animation: rise .32s var(--snap) both; animation-delay: calc(var(--i, 0) * 40ms); }
.still .rise { animation: none; }
@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@keyframes fade { from { opacity: 0; } } @keyframes slide { from { transform: translateX(24px); opacity: 0; } } @keyframes pop { from { opacity: 0; transform: translate(-50%, 6px); } }
.toast { animation-name: fade; }
@media (prefers-reduced-motion: reduce) { .rise, .scrim, .panel, .dialog, .palette, .toast { animation: none; } * { transition: none !important; } }
.tabbar, .sheet { display: none; }
@media (max-width: 1180px) { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .grid.six { grid-template-columns: repeat(3, minmax(0, 1fr)); } .charts { grid-template-columns: 1fr; } }
@media (max-width: 760px) {
  .shell { display: block; } .side { display: none; }
  .top { padding: 8px 16px; min-height: 56px; } .top .mark { display: block; } .top .sub, .top .kbd, .upd { display: none; }
  main { padding: 16px 16px calc(96px + env(safe-area-inset-bottom)); }
  .grid, .grid.three { grid-template-columns: 1fr 1fr; gap: 8px; } .grid.six { grid-template-columns: 1fr 1fr; } .stat { min-height: 112px; padding: 12px; } .stat .v { font-size: 24px; } .spark { width: 64px; }
  .tabbar { display: grid; grid-template-columns: repeat(5, 1fr); position: fixed; left: 0; right: 0; bottom: 0; z-index: 6; padding: 8px 8px calc(8px + env(safe-area-inset-bottom)); background: var(--panel); border-top: 1px solid var(--line); }
  .tabbar button { display: flex; flex-direction: column; align-items: center; gap: 4px; height: 48px; border: 0; background: none; color: var(--muted); font-size: 12px; font-weight: 600; cursor: pointer; position: relative; }
  .tabbar button.on { color: var(--accent); }
  .tabbar .badge { position: absolute; top: -2px; left: calc(50% + 6px); min-width: 18px; height: 18px; padding: 0 4px; }
  .sheet:not([hidden]) { display: block; position: fixed; left: 8px; right: 8px; bottom: calc(80px + env(safe-area-inset-bottom)); z-index: 21; padding: 8px; border-radius: 16px; background: var(--panel); border: 1px solid var(--line); box-shadow: var(--float); }
  .sheet button { display: flex; align-items: center; gap: 12px; width: 100%; height: 48px; padding: 0 12px; border: 0; border-radius: 12px; background: none; color: var(--text); font-weight: 600; font-size: 16px; cursor: pointer; }
  .tbl { max-height: none; border-radius: 12px; } td, th { padding: 12px; } .search { max-width: none; }
  .panel { width: 100%; border-left: 0; } .panel header { padding: 12px 16px; } .panel .body { padding: 16px; }
  .inbox { grid-template-columns: 1fr; height: auto; min-height: 0; } .inbox .ib-list { border-right: 0; } .inbox .rows { max-height: none; }
  .inbox.reading .ib-list { display: none; } .inbox:not(.reading) .thread { display: none; } .thread { padding: 16px; } .thread .back { display: inline-flex; margin-bottom: 8px; }
  .cal .day { min-height: 72px; padding: 4px; } .ev { font-size: 0; height: 6px; padding: 0; margin: 0 0 3px; border-radius: 99px; } .ev.deal { border-width: 2px; }
  .seg button { padding: 0 8px; } .toasts { left: 16px; right: 16px; bottom: calc(88px + env(safe-area-inset-bottom)); align-items: stretch; }
}`;

function appPage(nonce = "") {
  const navBtn = ([v, label]) => `<button data-v="${v}"${v === "overview" ? ' class="on" aria-current="page"' : ""}>${icon(v)}<span class="label">${label}</span><span class="badge" id="n-${v}" hidden>–</span></button>`;
  const tabBtn = ([v, label]) => `<button data-v="${v}"${v === "overview" ? ' class="on"' : ""}>${icon(v, 22)}${label}${v === "inbox" ? '<span class="badge hot" id="t-inbox" hidden></span>' : ""}</button>`;
  return head("FIG Admin", APP_CSS) + `<body>
<a class="skip" href="#main">Skip to the content</a>
<div class="shell">
  <aside class="side">
    <div class="brand">${LOGO}FIG <span>Admin</span></div>
    <nav class="nav" id="nav" aria-label="Admin">${NAV.map(navBtn).join("")}</nav>
    <div class="acct">
      <div class="who"><div class="avatar" aria-hidden="true">B</div><div><b>Brendan</b><span>Owner</span></div></div>
      <button id="sec" data-v="security">${icon("security")}Security</button>
      <button id="out">${icon("out")}Sign out</button>
    </div>
  </aside>
  <div style="min-width:0">
    <header class="top">
      <span class="mark">${LOGO}</span>
      <div class="grow"><h1 id="title">Overview</h1><span class="sub" id="sub"></span></div>
      <div class="actions" id="actions"></div>
    </header>
    <main id="main" tabindex="-1"></main>
  </div>
</div>
<nav class="tabbar" id="tabbar" aria-label="Admin">${TABS.map(tabBtn).join("")}<button id="more-btn" aria-haspopup="true" aria-expanded="false">${icon("more", 22)}More</button></nav>
<div class="sheet" id="sheet" hidden><button data-v="paid">${icon("paid")}Paid restaurants</button><button data-v="calendar">${icon("calendar")}Calendar</button><button data-v="blog">${icon("blog")}Blog</button><button data-v="security">${icon("security")}Security</button><button id="out2">${icon("out")}Sign out</button></div>
<div class="toasts" id="toasts" role="status" aria-live="polite"></div>
<script nonce="${nonce}">${CLIENT}</script></body></html>`;
}

// the page's own script. String.raw keeps every backslash as written; it must hold no "\${" and no backtick
const CLIENT = String.raw`
const $ = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const ago = (t) => { const m = Math.round((Date.now() - Date.parse(t)) / 60000); if (m < 1) return "just now"; if (m < 60) return m + " min ago"; if (m < 1440) return Math.round(m / 60) + " h ago"; const d = Math.round(m / 1440); return d === 1 ? "yesterday" : d + " days ago"; };
const num = (n) => n == null ? "–" : Number(n).toLocaleString("en-CA");
const money = (n) => "$" + Number(n || 0).toLocaleString("en-CA", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const short = (v, isMoney) => { const a = Math.abs(v), s = a >= 1000 ? (v / 1000).toFixed(a >= 10000 ? 0 : 1) + "k" : Number.isInteger(v) ? String(v) : v.toFixed(isMoney ? 0 : 1); return (isMoney ? "$" : "") + s; };
const dayLabel = (key) => new Date(key + "T12:00:00").toLocaleDateString("en-CA", { month: "short", day: "numeric" });
const dayKey = (t) => new Date(t).toLocaleDateString("en-CA", { timeZone: "America/Toronto" });
const when = (t) => t ? new Date(t).toLocaleString("en-CA", { timeZone: "America/Toronto", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : "";
const fullDate = (t) => t ? new Date(t).toLocaleString("en-CA", { timeZone: "America/Toronto", dateStyle: "medium", timeStyle: "short" }) : "";
const LAUNCH = Date.parse("2027-01-01T00:00:00-05:00");
const days = Math.max(0, Math.ceil((LAUNCH - Date.now()) / 86400000));
let D = null, view = "overview", CH = null, RANGE = 30, UPDATED = 0;
const SUB = { restaurants: "fig", inbox: "open" };
const TITLES = { overview: "Overview", restaurants: "Restaurants", paid: "Paid restaurants", waitlist: "Waitlist", calendar: "Calendar", blog: "Blog", inbox: "Support", security: "Security" };
const ICONS = __ICONS__;
const ic = (n, size) => '<svg class="ic" width="' + (size || 20) + '" height="' + (size || 20) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[n] + "</svg>";
const api = (what, body) => fetch("/api/admin-api?do=" + what, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) })
  .then(async (r) => { if (r.status === 401) location.reload(); return r.json(); });
let rise = 0; const R = () => ' style="--i:' + (rise++) + '"'; // cards fade up one after another (40 ms apart)
const card = (cls, inner) => '<div class="card rise ' + cls + '"' + R() + ">" + inner + "</div>";

// ---- one button system: busy buttons with a spinner, in-page confirm dialogs, toasts, the copy fallback
async function busy(btn, work) {
  if (!btn || btn.getAttribute("aria-busy") === "true") return;
  const was = btn.innerHTML; btn.setAttribute("aria-busy", "true"); btn.disabled = true; btn.innerHTML = '<span class="spin" aria-hidden="true"></span>' + was;
  try { return await work(); } finally { if (btn.isConnected) { btn.removeAttribute("aria-busy"); btn.disabled = false; btn.innerHTML = was; } }
}
function toast(text, bad) {
  const t = document.createElement("div"); t.className = "toast" + (bad ? " bad" : ""); t.textContent = text;
  $("#toasts").appendChild(t); setTimeout(() => t.remove(), bad ? 6000 : 3500);
}
const LAYERS = [];
// a dialog or panel: Tab stays inside it, Esc closes the top one, focus goes back to what opened it
function layer(box, scrim, onClose) {
  const before = document.activeElement;
  const focusable = () => $$("button, [href], input, select, textarea, iframe, [tabindex]:not([tabindex='-1'])", box).filter((el) => !el.disabled && el.offsetParent !== null);
  box.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return;
    const a = focusable(); if (!a.length) { e.preventDefault(); return; }
    const i = a.indexOf(document.activeElement);
    if (e.shiftKey && i <= 0) { e.preventDefault(); a[a.length - 1].focus(); } else if (!e.shiftKey && i === a.length - 1) { e.preventDefault(); a[0].focus(); }
  });
  const L = { close: () => { const i = LAYERS.indexOf(L); if (i < 0) return; LAYERS.splice(i, 1); box.remove(); if (scrim) scrim.remove(); if (onClose) onClose(); if (before && before.isConnected) before.focus(); } };
  if (scrim) scrim.onclick = L.close;
  LAYERS.push(L); setTimeout(() => (focusable()[0] || box).focus(), 0);
  return L;
}
// ask({ title, body, ok, danger, input }) -> true / false, or the typed text for an input
function ask(o) {
  return new Promise((done) => {
    const scrim = document.createElement("div"); scrim.className = "scrim top";
    const box = document.createElement("div"); box.className = "dialog"; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-labelledby", "dlg-t"); box.tabIndex = -1;
    box.innerHTML = '<h2 id="dlg-t">' + esc(o.title) + "</h2>" + (o.body ? "<p>" + o.body + "</p>" : "") + (o.input ? o.input : "") +
      '<div class="ctl">' + (o.cancel === false ? "" : '<button class="b secondary" data-no>' + esc(o.cancel || "Cancel") + "</button>") + '<button class="b ' + (o.danger ? "danger" : "primary") + '" data-yes>' + esc(o.ok || "Confirm") + "</button></div>";
    document.body.append(scrim, box);
    let answer = false;
    const L = layer(box, scrim, () => done(answer));
    $("[data-yes]", box).onclick = () => { const f = $("input, textarea", box); answer = o.input && f ? f.value : true; L.close(); };
    const no = $("[data-no]", box); if (no) no.onclick = L.close;
  });
}
async function copyText(text, what) {
  try { await navigator.clipboard.writeText(text); toast(what + " copied."); }
  catch { await ask({ title: "Copy " + what.toLowerCase(), body: "Select the text and copy it.", input: '<textarea readonly>' + esc(text) + "</textarea>", ok: "Done", cancel: false }); }
}

const NOT_CONNECTED = card("empty", "<b>Not connected to FIG’s database yet.</b>In Vercel → fig-promo → Settings → Environment Variables, add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (Supabase → Project Settings → API), then redeploy. The key stays on the server; it is never sent to this page.");
const skeleton = (rows) => '<div class="card" style="padding:16px">' + Array.from({ length: rows || 6 }, (_, i) => '<div class="sk skrow" style="width:' + (92 - (i % 3) * 14) + '%"></div>').join("") + "</div>";
const emptyState = (title, what) => card("empty", "<b>" + title + "</b>" + what);
// a table: heads are text, or [text, "n"] for a right-aligned number column; rows can open a side panel (open: "kind:id" per row)
function table(heads, rows, empty, search, open) {
  const n = heads.map((h) => Array.isArray(h) && h[1] === "n");
  const box = search ? '<div class="tools"><label class="search">' + ic("search", 18) + '<input type="search" data-filter placeholder="' + esc(search) + '" aria-label="' + esc(search) + '"></label></div>' : "";
  if (!rows.length) return box + emptyState(empty[0], empty[1]);
  const name = (TITLES[view] || "Table") + ": " + heads.map((h) => (Array.isArray(h) ? h[0] : h)).filter(Boolean).join(", ");
  return box + '<div class="tbl rise"' + R() + '><table aria-label="' + esc(name) + '"><thead><tr>' + heads.map((h, i) => '<th scope="col"' + (n[i] ? ' class="n"' : "") + ">" + (Array.isArray(h) ? h[0] : h) + "</th>").join("") + "</tr></thead><tbody>" +
    rows.map((r, j) => "<tr" + (open ? ' data-open="' + esc(open[j]) + '"' : "") + ">" + r.map((c, i) => "<td" + (n[i] ? ' class="n"' : "") + ">" + c + "</td>").join("") + "</tr>").join("") + "</tbody></table></div>";
}
const statusPill = (s) => s === "approved" ? '<span class="pill g">Live</span>' : s === "rejected" ? '<span class="pill">Hidden</span>' : '<span class="pill b">In setup</span>';
const dealPill = (s) => s === "live" ? '<span class="pill g">Live</span>' : s === "scheduled" ? '<span class="pill b">Scheduled</span>' : s === "paused" ? '<span class="pill">Paused</span>' : '<span class="pill">Ended</span>';
const thumb = (r, big) => { const p = (r.photos || [])[0]; return p && /^(https:|[/])/.test(p) ? '<img class="thumb' + (big ? " big" : "") + '" src="' + esc(p) + '" alt="" loading="lazy">' : '<span class="thumb' + (big ? " big" : "") + '" aria-hidden="true">' + esc((r.name || "?").trim().charAt(0).toUpperCase()) + "</span>"; };
const tabs = (v, list) => '<div class="tabs" role="group" aria-label="Show">' + list.map(([k, label]) => '<button data-sub="' + v + ":" + k + '" aria-pressed="' + (SUB[v] === k) + '"' + (SUB[v] === k ? ' class="on"' : "") + ">" + label + "</button>").join("") + "</div>";

// ---- charts: hand-built SVG with axes, gridlines and a hover read-out (any pointer, touch too)
let CHARTS = [];
const COLORS = ["var(--c1)", "var(--c2)", "var(--c3)", "var(--c4)", "var(--c5)", "var(--c6)", "var(--c7)", "var(--c8)"];
// series: [{ name, values, kind: "line" | "area" | "bar", color }]; stack: areas piled up; money: dollar axis
function chartBox(spec) { CHARTS.push(spec); return '<div class="chart" data-chart="' + (CHARTS.length - 1) + '" style="height:' + (spec.h || 200) + 'px"></div>'; }
function legend(series) { return series.length > 1 ? '<div class="legend">' + series.map((s) => '<span><i style="background:' + s.color + '"></i>' + esc(s.name) + "</span>").join("") + "</div>" : ""; }
function chartCard(title, big, spec) { return card("chartcard", '<div class="head"><b>' + title + '</b><span class="big">' + big + "</span></div>" + legend(spec.series) + chartBox(spec)); }
const niceStep = (v) => { if (v <= 1) return 1; const p = Math.pow(10, Math.floor(Math.log10(v))), m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 5 ? 5 : 10) * p; };
// a chart in words (FIX-LIST #159): a per-day count (bars) by its total and its busiest day; a level (lines, areas: the list's
// size, deals running, running totals) by where it ended and where it started
function chartText(s) {
  const fmt = (v) => (s.money ? money(v) : num(v));
  const span = s.keys.length ? dayLabel(s.keys[0]) + " to " + dayLabel(s.keys[s.keys.length - 1]) : "";
  return (s.label ? s.label + ". " : "") + span + ". " + s.series.map((x) => {
    const v = x.values;
    if (x.kind !== "bar") return x.name + ": " + fmt(v[v.length - 1] || 0) + " now, from " + fmt(v[0] || 0);
    const total = v.reduce((a, n) => a + n, 0), top = Math.max(0, ...v), at = v.indexOf(top);
    return x.name + ": " + fmt(total) + " in all" + (top > 0 && at >= 0 ? ", most on " + dayLabel(s.keys[at]) + " (" + fmt(top) + ")" : "");
  }).join("; ") + ".";
}
function drawChart(el, s) {
  const W = Math.max(240, el.clientWidth), H = el.clientHeight, L = 44, Rp = 8, T = 8, B = 24, iw = W - L - Rp, ih = H - T - B, n = s.keys.length;
  const bars = s.series.some((x) => x.kind === "bar");
  const tops = s.stack ? s.keys.map((_, i) => s.series.reduce((a, x) => a + x.values[i], 0)) : s.series.flatMap((x) => x.values);
  const step = niceStep(Math.max(1, ...tops) / 4), max = step * Math.max(1, Math.ceil(Math.max(1, ...tops) / step));
  const X = (i) => L + (bars ? (i + 0.5) * iw / n : n === 1 ? iw / 2 : i * iw / (n - 1)), Y = (v) => T + ih - (v / max) * ih;
  let g = "";
  for (let v = 0; v <= max + 1e-9; v += step) g += '<line x1="' + L + '" x2="' + (W - Rp) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" stroke="var(--line2)"/><text x="' + (L - 8) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + short(v, s.money) + "</text>";
  const every = Math.max(1, Math.ceil(n / (W < 480 ? 3 : 6)));
  for (let i = n - 1; i >= 0; i -= every) g += '<text x="' + X(i).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="' + (i === n - 1 ? "end" : "middle") + '">' + dayLabel(s.keys[i]) + "</text>";
  const base = s.keys.map(() => 0);
  s.series.forEach((x) => {
    const lo = base.slice(), hi = x.values.map((v, i) => (s.stack ? lo[i] + v : v));
    if (s.stack) hi.forEach((v, i) => (base[i] = v));
    if (x.kind === "bar") { const w = Math.max(1, iw / n * 0.62); x.values.forEach((v, i) => { if (v) g += '<rect x="' + (X(i) - w / 2).toFixed(1) + '" y="' + Y(hi[i]).toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + (Y(lo[i]) - Y(hi[i])).toFixed(1) + '" rx="2" fill="' + x.color + '"/>'; }); return; } // stacked: each on the last
    const pts = hi.map((v, i) => X(i).toFixed(1) + "," + Y(v).toFixed(1));
    if (x.kind === "area") { const under = lo.map((v, i) => X(i).toFixed(1) + "," + Y(v).toFixed(1)).reverse(); g += '<polygon points="' + pts.concat(under).join(" ") + '" fill="' + x.color + '" fill-opacity="' + (s.stack ? 0.55 : 0.12) + '"/>'; }
    g += '<polyline points="' + pts.join(" ") + '" fill="none" stroke="' + x.color + '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>';
  });
  el.innerHTML = '<svg width="' + W + '" height="' + H + '" role="img" aria-label="' + esc(chartText(s)) + '">' + g + '<line class="cross" x1="0" x2="0" y1="' + T + '" y2="' + (T + ih) + '" stroke="var(--faint)" stroke-dasharray="3 3" visibility="hidden"/></svg><div class="tip" hidden></div>';
  const tip = $(".tip", el), cross = $(".cross", el);
  el.onpointermove = (e) => {
    const x = e.clientX - el.getBoundingClientRect().left;
    const i = Math.min(n - 1, Math.max(0, bars ? Math.floor((x - L) / (iw / n)) : Math.round((x - L) / (iw / Math.max(1, n - 1)))));
    cross.setAttribute("x1", X(i)); cross.setAttribute("x2", X(i)); cross.setAttribute("visibility", "visible");
    tip.innerHTML = "<b>" + dayLabel(s.keys[i]) + "</b>" + s.series.map((x) => "<div><i style=\"background:" + x.color + "\"></i>" + esc(x.name) + ": " + (s.money ? money(x.values[i]) : num(x.values[i])) + "</div>").join("");
    tip.hidden = false; const tw = tip.offsetWidth; tip.style.left = Math.min(Math.max(0, X(i) + 12), W - tw) + "px";
  };
  el.onpointerleave = () => { tip.hidden = true; cross.setAttribute("visibility", "hidden"); };
}
const drawCharts = () => $$("[data-chart]").forEach((el) => drawChart(el, CHARTS[+el.dataset.chart]));
let resizeT; addEventListener("resize", () => { clearTimeout(resizeT); resizeT = setTimeout(drawCharts, 150); });
const last = (a, n) => a.slice(-n), sum = (a) => a.reduce((x, y) => x + y, 0);
// a little line for a stat card (the last RANGE days)
function spark(values) {
  if (!values || values.length < 2) return "";
  const w = 96, h = 32, max = Math.max(1, ...values), step = w / (values.length - 1);
  const pts = values.map((v, i) => (i * step).toFixed(1) + "," + (h - 2 - (v / max) * (h - 4)).toFixed(1));
  return '<svg class="spark" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + " " + h + '" aria-hidden="true"><polyline points="' + pts.join(" ") + '" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}
// this range against the one before it (the 90-day view has nothing before it to compare with)
function delta(values) {
  if (RANGE >= 90 || !values) return "";
  const now = sum(last(values, RANGE)), before = sum(values.slice(-2 * RANGE, -RANGE));
  if (now === before) return '<span class="delta flat">Same as the ' + RANGE + " days before</span>";
  const up = now > before, pct = before ? Math.round(Math.abs(now - before) / before * 100) + "%" : "new";
  return '<span class="delta ' + (up ? "up" : "down") + '" title="These ' + RANGE + " days " + now + ", the " + RANGE + " before " + before + '">' + (up ? "▲ " : "▼ ") + pct + "</span>";
}
const stat = (label, value, values) => card("stat", '<span class="k">' + label + '</span><span class="v">' + value + '</span><div class="row">' + delta(values) + spark(values && last(values, RANGE)) + "</div>");
const mini = (label, value, id) => card("mini", '<div class="k">' + label + '</div><div class="v"' + (id ? ' id="' + id + '"' : "") + ">" + value + "</div>");

// restaurants still setting up (status pending: not approved, not rejected), and the ones stuck there 3 days or more
const setup = () => D.restaurants.filter((r) => r.status !== "approved" && r.status !== "rejected");
function needsYou() {
  const stuck = setup().filter((r) => Date.now() - Date.parse(r.created_at) >= 3 * 86400000);
  const item = (go, text) => '<button class="item" data-go="' + go + '"><span class="t">' + text + "</span>" + ic("chevron", 18) + "</button>";
  const items = [];
  if (D.counts.support) items.push(item("inbox:open", "<b>" + D.counts.support + "</b>" + (D.counts.support === 1 ? " message" : " messages") + " to answer"));
  if (D.counts.reports) items.push(item("inbox:reports", "<b>" + D.counts.reports + "</b>" + (D.counts.reports === 1 ? " open report" : " open reports")));
  stuck.forEach((r) => items.push(item("r:" + r.id, "<b>" + esc(r.name) + "</b> has been in setup for " + Math.floor((Date.now() - Date.parse(r.created_at)) / 86400000) + " days")));
  if (!items.length) return card("needs clear", '<div class="head"><span class="dot">' + ic("check") + '</span><div><b>All clear</b><div class="muted">Nothing needs you right now.</div></div></div>');
  return card("needs", '<div class="head"><span class="dot">' + ic("inbox") + "</span><b>Needs you</b></div>" + items.join(""));
}
function launchLine() {
  const left = '<div><div class="days">' + days + '</div><div class="note">days to January 1, 2027</div></div>';
  if (!DIN) return card("launch", left + '<div class="t"><div class="sk skrow" style="width:70%"></div></div>');
  if (DIN.error) return card("launch", left + '<div class="t">The launch plan could not load.</div><button class="b secondary" data-go="waitlist">Open Waitlist</button>');
  const eff = DIN.effective || DIN.mode;
  return card("launch", left + '<div class="t">' + nowText(eff, DIN.cap ? "the first " + DIN.cap.toLocaleString("en-CA") : "everyone") + '</div><button class="b secondary" data-go="waitlist">The launch plan</button>');
}

// ---- views
const VIEWS = {
  overview() {
    if (!D.connected) return NOT_CONNECTED;
    let out = needsYou() + launchLine();
    if (!CH) return out + '<div class="grid">' + '<div class="sk skcard"></div>'.repeat(4) + "</div><div style=\"height:16px\"></div>" + skeleton(8);
    const keys = last(CH.keys, RANGE), cut = (a) => last(a, RANGE), r = CH.restaurants;
    out += '<div class="grid">' + stat("New on the waitlist", num(sum(cut(CH.waitlist.fresh))), CH.waitlist.fresh) + stat("Deals claimed", num(sum(cut(CH.claims))), CH.claims) +
      stat("Scanned at the counter", num(sum(cut(CH.scans))), CH.scans) + stat("Takeout orders", num(sum(cut(CH.orders.placed))), CH.orders.placed) + "</div>";
    out += '<div class="grid six" style="margin-top:16px">' + mini("On the waitlist", num(D.counts.waitlist)) + mini("Restaurants live", num(D.counts.live)) + mini("In setup", num(setup().length)) +
      mini("Deals live now", num(D.counts.dealsLive)) + mini("Diner accounts", num(D.counts.diners)) + mini("Posts queued", "–", "q-posts") + "</div>";
    out += growthHtml();
    out += "<h2>Trends</h2>" + '<div class="charts">' +
      chartCard("Waitlist size", num(last(CH.waitlist.total, 1)[0]), { keys, label: "Waitlist size per day", series: [{ name: "On the list", values: cut(CH.waitlist.total), kind: "area", color: COLORS[0] }] }) +
      chartCard("New sign-ups per day", num(sum(cut(CH.waitlist.fresh))), { keys, label: "New waitlist sign-ups per day", series: [{ name: "New sign-ups", values: cut(CH.waitlist.fresh), kind: "bar", color: COLORS[0] }] }) +
      chartCard("Claims and counter scans per day", num(sum(cut(CH.claims))) + " / " + num(sum(cut(CH.scans))), { keys, label: "Claims and scans per day", series: [{ name: "Deals claimed", values: cut(CH.claims), kind: "line", color: COLORS[0] }, { name: "Scanned at the counter", values: cut(CH.scans), kind: "line", color: COLORS[1] }] }) +
      chartCard("Deals running per day", num(last(CH.deals, 1)[0]), { keys, label: "Deals running per day", series: [{ name: "Deals running", values: cut(CH.deals), kind: "area", color: COLORS[0] }] }) +
      chartCard("Takeout orders per day", num(sum(cut(CH.orders.placed))), { keys, label: "Takeout orders per day", series: [{ name: "Orders placed", values: cut(CH.orders.placed), kind: "bar", color: COLORS[1] }] }) +
      chartCard("Picked-up order totals", money(sum(cut(CH.orders.value))), { keys, money: true, label: "Picked-up order totals per day", series: [{ name: "Order totals (as stored)", values: cut(CH.orders.value), kind: "line", color: COLORS[0] }, { name: "FIG fees (as stored)", values: cut(CH.orders.fees), kind: "line", color: COLORS[2] }] }) +
      chartCard("Restaurants by when they joined", num(last(r.live, 1)[0] + last(r.setup, 1)[0] + last(r.hidden, 1)[0]), { keys, stack: true, h: 200, label: "Restaurants by join date, split by their status today", series: [{ name: "Live today", values: cut(r.live), kind: "area", color: COLORS[2] }, { name: "In setup today", values: cut(r.setup), kind: "area", color: COLORS[0] }, { name: "Hidden today", values: cut(r.hidden), kind: "area", color: COLORS[3] }] }) +
      "</div>";
    out += sourcesHtml();
    out += '<h2>Latest restaurants <button class="b ghost push" data-go="restaurants">See all</button></h2>' +
      table(["Restaurant", "City", "Status", ["Joined", "n"]], D.restaurants.slice(0, 6).map((x) => ['<div class="who-cell">' + thumb(x) + "<div><b>" + esc(x.name) + '</b><span class="sub">' + esc(x.cuisine || "") + "</span></div></div>", esc(x.city), statusPill(x.status), ago(x.created_at)]),
        ["No restaurants yet", "They appear here as soon as one signs up on the website."], null, D.restaurants.slice(0, 6).map((x) => "r:" + x.id));
    return out;
  },
  restaurants() {
    if (!D.connected) return NOT_CONNECTED;
    return tabs("restaurants", [["fig", "On FIG · " + D.restaurants.length], ["outreach", "Outreach · " + D.leads.length + (D.leads.length === 1 ? " lead" : " leads")]]) +
      (SUB.restaurants === "outreach" ? outreachHtml()
        : table(["Restaurant", "Owner", "Status", "Payments", ["Joined", "n"]], D.restaurants.map((r) => {
            const b = (D.premium || []).find((x) => x.owner_id === r.owner_id) || {};
            const owner = (D.owners || []).find((o) => o.id === r.owner_id) || {};
            const pay = b.payments_demo ? '<span class="pill">Pretend</span>' : b.stripe_ready && b.stripe_payouts ? '<span class="pill g">Live, ready</span>' : b.stripe_ready ? '<span class="pill b">Live, bank needed</span>' : '<span class="pill">Not set up</span>';
            return ['<div class="who-cell">' + thumb(r) + "<div><b>" + esc(r.name) + '</b><span class="sub">' + esc(r.cuisine || "") + " · " + esc(r.city) + "</span></div></div>",
              esc(owner.name || "") + '<span class="sub">' + esc(owner.email || "") + "</span>", statusPill(r.status), pay, ago(r.created_at)];
          }), ["No restaurants yet", "Share the website’s restaurant sign-up; new ones show up here as they join."], "Search restaurants or owners", D.restaurants.map((r) => "r:" + r.id)) + changesTable());
  },
  waitlist: () => !D.connected ? NOT_CONNECTED : '<div id="dinerbox">' + dinersHtml() + "</div>",
  paid: () => !D.connected ? NOT_CONNECTED : paidHtml(),
  calendar: () => !D.connected ? NOT_CONNECTED : calendarHtml(),
  blog: () => !D.connected ? NOT_CONNECTED : '<div id="blogbox">' + blogHtml() + "</div>",
  inbox: () => !D.connected ? NOT_CONNECTED : '<p class="note" style="margin:-4px 0 14px">Messages people send from Help or Contact, and reports about restaurants or orders.</p>' + inboxHtml(),
  security: () => securityHtml(),
};
function changesTable() {
  const name = (id) => ((D.restaurants || []).find((r) => r.id === id) || {}).name || "a restaurant";
  const who = (id) => ((D.owners || []).find((o) => o.id === id) || {}).email || "someone";
  const rows = (D.changes || []).map((c) => c.kind === "transfer"
    ? ['<span class="pill b">Handed over</span>', "<b>" + esc(name(c.restaurant_id)) + "</b>", esc(who(c.before.owner)) + " → " + esc(who(c.after.owner) || c.after.to_email || ""), ago(c.at)]
    : ['<span class="pill">Details changed</span>', "<b>" + esc(name(c.restaurant_id)) + "</b>", esc([c.before.name !== c.after.name ? c.before.name + " → " + c.after.name : "", c.before.address !== c.after.address ? c.before.address + " → " + c.after.address : ""].filter(Boolean).join(" · ") || "location moved"), ago(c.at)]);
  return "<h2>Handovers and name changes</h2>" + table(["What", "Restaurant", "Detail", ["When", "n"]], rows, ["No changes yet", "Name, address and owner changes are recorded here."]);
}
function outreachHtml() {
  return '<h2>Leads from the website <span class="count">' + D.leads.length + "</span></h2>" + table(["Restaurant", "Contact", "Area", "From", ["Received", "n"]], D.leads.map((l) => ["<b>" + esc(l.restaurant) + "</b>", esc(l.email || l.phone), esc(l.area), esc(l.source), ago(l.created_at)]), ["No leads yet", "Restaurants that fill in the website’s form show up here."]) +
    '<h2>Every place in Markham</h2><p class="muted" style="margin:-4px 0 12px">Search, shortlist the ones to approach yourself, and keep notes. Only the FIG team sees this.</p><div id="prosbox">' + prosHtml() + "</div>";
}

// ---- detail panels: a restaurant, a waitlist person, a post (side panel on a computer, full screen on a phone)
function openPanel(title, inner, after) {
  closePanels();
  const scrim = document.createElement("div"); scrim.className = "scrim";
  const box = document.createElement("aside"); box.className = "panel"; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-label", title); box.tabIndex = -1;
  box.innerHTML = "<header><h2>" + esc(title) + '</h2><button class="b icon ghost" data-close aria-label="Close">' + ic("close") + '</button></header><div class="body">' + inner + "</div>";
  document.body.append(scrim, box);
  const L = layer(box, scrim); $("[data-close]", box).onclick = L.close; box._layer = L;
  if (after) after(box);
  return box;
}
function closePanels() { $$(".panel").forEach((p) => p._layer && p._layer.close()); }
async function openRestaurant(id) {
  const base = D.restaurants.find((x) => x.id === id) || { name: "Restaurant" };
  const box = openPanel(base.name, skeleton(10));
  const r = await api("restaurant-get", { id }).catch(() => ({ error: "It didn’t load. Try again." }));
  if (!box.isConnected) return;
  const body = $(".body", box);
  if (r.error || !r.found) { body.innerHTML = emptyState("This restaurant didn’t load", esc(r.error || "It may have been removed.")); return; }
  const x = r.restaurant, done = r.setup.filter((s) => s[1]).length;
  CHARTS = [];
  body.innerHTML =
    '<section><div class="who-cell">' + thumb(x, true) + "<div><b style=\"font-size:16px\">" + esc(x.name) + "</b> " + statusPill(x.status) + '<span class="sub">' + esc([x.cuisine, x.address, x.city].filter(Boolean).join(" · ")) + "</span></div></div>" +
    ((x.photos || []).length > 1 ? '<div style="display:flex;gap:8px;margin-top:12px">' + x.photos.map((p) => /^(https:|[/])/.test(p) ? '<img src="' + esc(p) + '" alt="" style="width:33%;aspect-ratio:4/3;object-fit:cover;border-radius:10px">' : "").join("") + "</div>" : "") + "</section>" +
    '<section><dl class="kv"><dt>Joined</dt><dd>' + fullDate(x.created_at) + "</dd><dt>Phone</dt><dd>" + esc(x.phone || "–") + "</dd><dt>Takeout</dt><dd>" + (x.takeout ? "On" : "Off") + "</dd></dl></section>" +
    "<section><h3>Setup · " + done + " of " + r.setup.length + '</h3><div class="bar"><i style="width:' + Math.round(done / r.setup.length * 100) + '%"></i></div><div class="checks">' + r.setup.map((s) => "<div>" + (s[1] ? '<span class="ok">' + ic("check", 16) + "</span>" : '<span class="no">' + ic("close", 16) + "</span>") + esc(s[0]) + "</div>").join("") + "</div></section>" +
    '<section><h3>Owner and staff</h3><div class="list"><div><span><b>' + esc(r.owner.name || "Owner") + '</b><span class="sub">' + esc(r.owner.email || "") + '</span></span><span class="pill b">Owner</span></div>' +
      r.staff.filter((s) => s.role !== "Owner").map((s) => "<div><span><b>" + esc(s.name || s.email) + '</b><span class="sub">' + esc(s.email) + "</span></span><span class=\"pill" + (s.status === "active" ? " g" : "") + "\">" + esc(s.role) + (s.status === "invited" ? ", invited" : "") + "</span></div>").join("") + "</div>" +
      '<div class="ctl"><button class="b secondary" data-2fa="' + esc(x.owner_id) + '">Turn off the owner’s two-step login</button><a class="b ghost" href="/app/restaurant/' + esc(x.id) + '" target="_blank" rel="noopener">See their page</a></div></section>' +
    "<section><h3>Claims and counter scans, 30 days</h3>" + legend([{ name: "Deals claimed", color: COLORS[0] }, { name: "Scanned", color: COLORS[1] }]) + chartBox({ keys: r.series.keys, h: 160, label: "Claims and scans, 30 days", series: [{ name: "Deals claimed", values: r.series.claims, kind: "line", color: COLORS[0] }, { name: "Scanned", values: r.series.scans, kind: "line", color: COLORS[1] }] }) + "</section>" +
    "<section><h3>Deals</h3>" + (r.deals.length ? '<div class="list">' + r.deals.map((d) => "<div><span><b>" + esc(d.title) + '</b><span class="sub">Started ' + fullDate(d.start) + (d.end ? " · ends " + fullDate(d.end) : "") + "</span></span>" + dealPill(d.status) + "</div>").join("") + "</div>" : '<p class="muted">No deals yet.</p>') + "</section>" +
    "<section><h3>Latest takeout orders</h3>" + (r.orders.length ? '<div class="list">' + r.orders.map((o) => "<div><span><b>" + esc(o.number) + '</b><span class="sub">' + when(o.placed_at) + " · " + esc(o.status) + '</span></span><span class="n" style="font-variant-numeric:tabular-nums">' + money(o.total) + "</span></div>").join("") + "</div>" : '<p class="muted">No takeout orders yet.</p>') + "</section>" +
    "<section><h3>Reports</h3>" + (r.reports.length ? '<div class="list">' + r.reports.map((p) => "<div><span><b>" + esc(p.reason) + '</b><span class="sub">' + esc(p.details) + " · " + ago(p.at) + "</span></span>" + (p.status === "open" ? '<span class="pill r">Open</span>' : '<span class="pill g">Settled</span>') + "</div>").join("") + "</div>" : '<p class="muted">No reports. Good news.</p>') + "</section>";
  wireActions(box); drawCharts();
}
// founding status, from the list's own order: within the first N (if set) and joined before the cutoff (if any)
function foundingOf(w) {
  const order = (DIN.waitlist || []).slice().sort((a, b) => Date.parse(a.joined_at) - Date.parse(b.joined_at));
  const place = order.indexOf(w) + 1, closes = DIN.closes || DIN.until;
  if (closes && Date.parse(w.joined_at) >= Date.parse(closes)) return [place, "Next wave (joined after the founding list closed)", ""];
  if (DIN.cap && place > DIN.cap) return [place, "Next wave (beyond the first " + DIN.cap.toLocaleString("en-CA") + ")", ""];
  return [place, "In the founding wave", " g"];
}
function openPerson(i) {
  const w = (DIN.waitlist || [])[i]; if (!w) return;
  const [place, status, cls] = foundingOf(w);
  openPanel(w.email, '<section><dl class="kv"><dt>Joined</dt><dd>' + fullDate(w.joined_at) + "</dd><dt>Place in line</dt><dd>" + num(place) + " of " + num(DIN.waitlist.length) + '</dd><dt>Founding</dt><dd><span class="pill' + cls + '">' + esc(status) + "</span></dd>" +
    "<dt>Came from</dt><dd>" + esc(w.source || "website") + "</dd><dt>School</dt><dd>" + esc(w.school || "–") + "</dd><dt>May email</dt><dd>" +
    (w.consent ? "Yes, ticked " + (w.consent_at ? fullDate(w.consent_at) : "when they joined (before the date was recorded)") : w.unsubscribed_at ? "No, unsubscribed " + fullDate(w.unsubscribed_at) : "No. Only send them what the law allows without consent.") + "</dd></dl></section>" +
    '<section><div class="ctl"><button class="b secondary" data-copy>Copy the email</button>' + (w.consent ? '<button class="b secondary" data-unsub>Unsubscribe</button>' : "") + '<button class="b danger" data-remove>Remove from the list</button></div>' +
    '<p class="note">Unsubscribe when they ask to stop the emails; they keep their place. Remove when they ask to be forgotten.</p></section>', (box) => {
      $("[data-copy]", box).onclick = () => copyText(w.email, "Email");
      // a request to stop the emails, or to be forgotten (FIX-LIST #95)
      const act = async (btn, what, q) => {
        if (!(await ask(q))) return;
        await busy(btn, async () => { const r = await api(what, { email: w.email }); if (r.error) return toast(r.error, true); toast(what === "waitlist-remove" ? "Removed from the waitlist." : "Unsubscribed. They won’t be emailed."); closePanels(); await dinersLoad(); });
      };
      const u = $("[data-unsub]", box); if (u) u.onclick = () => act(u, "waitlist-unsubscribe", { title: "Stop emailing them?", body: esc(w.email) + " stays on the list in the same place. Joining again with the box ticked opts them back in.", ok: "Unsubscribe" });
      const rm = $("[data-remove]", box); rm.onclick = () => act(rm, "waitlist-remove", { title: "Remove them from the waitlist?", body: esc(w.email) + " comes off the list for good, and their place in line is gone.", ok: "Remove", danger: true });
    });
}
function openPost(slug) {
  const p = ((BLOG || {}).posts || []).find((x) => x.slug === slug); if (!p) return;
  const live = p.status === "live" && p.visible !== false;
  openPanel(p.title, "<section>" + postPill(p) + '<dl class="kv" style="margin-top:12px"><dt>Address</dt><dd class="mono">/blog/' + esc(p.slug) + "</dd>" + (p.date ? "<dt>Date</dt><dd>" + esc(p.date) + "</dd>" : "") + (p.publish_at ? "<dt>Goes live</dt><dd>" + fullDate(p.publish_at) + "</dd>" : "") + "<dt>Words</dt><dd>" + (p.words ? num(p.words) : "–") + "</dd>" + (p.topic ? "<dt>Topic</dt><dd>" + esc(p.topic) + "</dd>" : "") + "</dl></section>" +
    '<section><div class="ctl">' + postActions(p) + "</div></section>" +
    "<section><h3>Preview</h3>" + (live ? '<iframe src="/blog/' + esc(p.slug) + '" title="' + esc(p.title) + '" loading="lazy" sandbox="allow-same-origin"></iframe>' : '<p class="muted">The preview appears once the post is live.</p>') + "</section>",
    (box) => blogWire(box));
}

// ---- inbox: messages and reports in one list, the selected one beside it; j / k move, e marks answered or reopens
let SEL = null, CTX = {};
function inboxItems() {
  const q = (($("#ib-q") || {}).value || "").trim().toLowerCase();
  const msgs = (D.support || []).map((m) => ({ kind: "m", id: m.id, open: m.status === "open", at: m.at, who: m.email, title: m.topic || "Message", text: m.body, m }));
  const reps = (D.reports || []).map((r) => ({ kind: "r", id: r.id, open: r.status === "open", at: r.at, who: ((D.restaurants.find((x) => x.id === r.restaurant_id) || {}).name || "A restaurant"), title: r.reason, text: r.details, r }));
  const pick = SUB.inbox === "open" ? msgs.filter((x) => x.open) : SUB.inbox === "answered" ? msgs.filter((x) => !x.open) : SUB.inbox === "reports" ? reps : msgs.concat(reps);
  return pick.filter((x) => !q || (x.who + " " + x.title + " " + x.text).toLowerCase().includes(q)).sort((a, b) => Date.parse(b.at) - Date.parse(a.at));
}
function inboxHtml() {
  const open = (D.support || []).filter((m) => m.status === "open").length, answered = (D.support || []).length - open;
  return tabs("inbox", [["open", "Open · " + open], ["answered", "Answered · " + answered], ["reports", "Reports · " + (D.reports || []).length], ["all", "All"]]) +
    '<div class="card inbox rise' + (SEL ? " reading" : "") + '"' + R() + '><div class="ib-list"><div class="tools"><label class="search" style="max-width:none">' + ic("search", 18) + '<input type="search" id="ib-q" placeholder="Search support" aria-label="Search the inbox"></label></div><div class="rows" id="ib-rows"></div></div><div class="thread" id="ib-thread"></div></div>' +
    '<p class="note">Keys: j and k move through the list, e marks a message answered or opens it again.</p>';
}
function inboxRows() {
  const items = inboxItems(), box = $("#ib-rows"); if (!box) return;
  if (SEL && !items.some((x) => x.kind + x.id === SEL)) SEL = null;
  box.innerHTML = items.length ? items.map((x) => '<button class="msg' + (x.kind + x.id === SEL ? " on" : "") + '"' + (x.kind + x.id === SEL ? ' aria-current="true"' : "") + ' data-pick="' + x.kind + x.id + '"><div class="l1">' + (x.open ? '<span class="new" aria-hidden="true"></span><span class="sr">Open: </span>' : "") + "<b>" + esc(x.who) + '</b><span class="note">' + ago(x.at) + '</span></div><div class="snip"><b>' + esc(x.title) + "</b> · " + esc(x.text) + "</div></button>").join("")
    : '<div class="empty"><b>' + (SUB.inbox === "open" ? "Nothing to answer" : "Nothing here") + "</b>" + (SUB.inbox === "open" ? "New messages from “Message us” land here." : "Try another filter or clear the search.") + "</div>";
  $$("[data-pick]", box).forEach((b) => b.onclick = async () => { SEL = b.dataset.pick; inboxRows(); await inboxThread(); const h = $("#ib-h"); if (h) h.focus(); }); // read where you are (FIX-LIST #165)
}
async function inboxThread() {
  const box = $("#ib-thread"), wrap = $(".inbox"); if (!box) return;
  const x = inboxItems().find((i) => i.kind + i.id === SEL);
  if (wrap) wrap.classList.toggle("reading", !!x);
  if (!x) { box.innerHTML = '<div class="empty"><b>Pick a message</b>Its sender, their account and anything else they wrote show up here.</div>'; return; }
  const uid = x.kind === "m" ? x.m.user_id : x.r.user_id;
  const others = x.kind === "m" ? (D.support || []).filter((m) => m.email === x.m.email && m.id !== x.id) : [];
  const ctx = (c) => !uid ? '<p class="muted">They wrote without a FIG account.</p>' : !c ? '<div class="sk skrow" style="width:60%"></div><div class="sk skrow" style="width:40%"></div>' : !c.found ? '<p class="muted">Their account is gone.</p>' :
    '<dl class="kv"><dt>Name</dt><dd>' + esc(c.person.name || "–") + "</dd><dt>Account</dt><dd>" + (c.person.role === "business" ? "Restaurant side" : "Diner") + ", since " + fullDate(c.person.created_at) + "</dd>" +
    (c.restaurants.length ? "<dt>Restaurants</dt><dd>" + c.restaurants.map((p) => '<button class="link" data-go="r:' + esc(p.id) + '">' + esc(p.name) + "</button>").join(", ") + "</dd>" : "") +
    (c.orders.length ? "<dt>Latest orders</dt><dd>" + c.orders.map((o) => esc(o.number) + " · " + esc(o.status) + " · " + money(o.total) + " · " + when(o.placed_at)).join("<br>") + "</dd>" : "") + "</dl>";
  const head = '<button class="b ghost back" data-back>' + ic("back", 18) + 'Back</button><div class="line" style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap"><div><h2 id="ib-h" tabindex="-1" style="font-size:16px;margin:0">' + esc(x.title) + '</h2><span class="sub">' + (x.kind === "m" ? esc(x.m.email) : "Report about " + esc(x.who)) + " · " + fullDate(x.at) + "</span></div>" +
    (x.kind === "m" ? (x.open ? '<span class="pill b">Open</span>' : '<span class="pill g">Answered</span>') : x.open ? '<span class="pill r">Open</span>' : '<span class="pill g">Settled</span>') + "</div>";
  const actions = x.kind === "m"
    ? '<div class="ctl"><a class="b primary" href="mailto:' + esc(x.m.email) + "?subject=" + encodeURIComponent("FIG: " + (x.m.topic || "your message")) + '">' + ic("mail", 18) + "Reply by email</a>" +
      (x.open ? '<button class="b secondary" data-sup="' + esc(x.id) + '" data-to="answered">Mark answered</button>' : '<button class="b secondary" data-sup="' + esc(x.id) + '" data-to="open">Reopen</button>') +
      '<button class="b ghost" data-2fa-email="' + esc(x.m.email) + '">Turn off two-step login</button><button class="b danger" data-sup-remove="' + esc(x.id) + '">Remove</button></div><p class="note">Their address: <span class="mono">' + esc(x.m.email) + "</span> (if the email link does nothing, copy it from here)</p>"
    : '<div class="ctl">' + (x.r.restaurant_id ? '<button class="b secondary" data-go="r:' + esc(x.r.restaurant_id) + '">Open the restaurant</button>' : "") + "</div>" + (x.r.claim_id ? '<p class="note">About claim <span class="mono">' + esc(x.r.claim_id.slice(0, 8)) + "</span></p>" : "");
  const render = () => {
    box.innerHTML = head + '<div class="bodytext">' + esc(x.text) + "</div>" + actions + "<h2>" + (x.kind === "m" ? "Who wrote" : "Who reported it") + "</h2>" + ctx(CTX[uid]) +
      (others.length ? "<h2>Their other messages</h2>" + '<div class="list">' + others.map((m) => "<div><span><b>" + esc(m.topic) + '</b><span class="sub">' + esc(m.body) + "</span></span><span class=\"note\">" + ago(m.at) + "</span></div>").join("") + "</div>" : "");
    wireActions(box); const back = $("[data-back]", box); if (back) back.onclick = () => { SEL = null; inboxRows(); inboxThread(); };
  };
  render();
  if (uid && !CTX[uid]) { CTX[uid] = await api("person-get", { id: uid }).catch(() => ({ found: false })); if (SEL === x.kind + x.id) render(); }
}
function inboxMove(step) {
  const items = inboxItems(); if (!items.length) return;
  const i = items.findIndex((x) => x.kind + x.id === SEL), next = items[Math.min(items.length - 1, Math.max(0, i + step))];
  SEL = next.kind + next.id; inboxRows(); inboxThread();
  const on = $(".msg.on"); if (on) on.scrollIntoView({ block: "nearest" });
}
function inboxToggle() { const b = $("#ib-thread [data-sup]"); if (b) b.click(); }

// ---- calendar: posts, the opening date, the founding cutoff, deals starting and ending; a queued post can move to another time
let CAL = { at: new Date(), week: false };
function calEvents() {
  const ev = [];
  ((BLOG || {}).posts || []).forEach((p) => { const t = p.publish_at || (p.date && Date.parse(p.date + " 12:00")); if (t && p.status !== "taken-down") ev.push({ day: dayKey(t), kind: "post", label: (p.status === "queued" ? "Post: " : "Posted: ") + p.title, slug: p.slug, queued: p.status === "queued", at: t }); });
  if (DIN && DIN.opens) ev.push({ day: dayKey(DIN.opens), kind: "launch", label: "Opens to founding members" });
  if (DIN && (DIN.until || DIN.closes)) ev.push({ day: dayKey(DIN.until || DIN.closes), kind: "cut", label: "Founding list closes" });
  ev.push({ day: dayKey(LAUNCH), kind: "launch", label: "Launch day (January 1)" });
  ((CH || {}).calendar || []).forEach((d) => { ev.push({ day: dayKey(d.start), kind: "deal", label: "Starts: " + d.title + (d.restaurant ? " · " + d.restaurant : ""), rid: d.restaurant_id }); if (d.end) ev.push({ day: dayKey(d.end), kind: "deal", label: "Ends: " + d.title + (d.restaurant ? " · " + d.restaurant : ""), rid: d.restaurant_id }); });
  return ev;
}
function calendarHtml() {
  if (!CH || !BLOG || !DIN) return skeleton(12);
  const a = CAL.at, today = dayKey(Date.now()), ev = calEvents(), wide = innerWidth > 760, week = CAL.week && wide;
  const start = new Date(a.getFullYear(), a.getMonth(), week ? a.getDate() : 1); start.setDate(start.getDate() - start.getDay());
  const cells = week ? 7 : 42, first = new Date(a.getFullYear(), a.getMonth(), 1), month = a.getMonth();
  const title = week ? "Week of " + start.toLocaleDateString("en-CA", { month: "long", day: "numeric" }) : first.toLocaleDateString("en-CA", { month: "long", year: "numeric" });
  let grid = "";
  for (let i = 0; i < cells; i++) {
    const d = new Date(start); d.setDate(start.getDate() + i);
    const key = d.toLocaleDateString("en-CA"), mine = ev.filter((e) => e.day === key), cap = week ? 20 : 3;
    grid += '<div class="day' + (!week && d.getMonth() !== month ? " out" : "") + (key === today ? " today" : "") + '"><div class="n"><span aria-hidden="true">' + d.getDate() + '</span><span class="sr">' + d.toLocaleDateString("en-CA", { weekday: "long", month: "long", day: "numeric" }) + "</span></div>" +
      mine.slice(0, cap).map((e) => '<button class="ev ' + e.kind + '" title="' + esc(e.label) + '" aria-label="' + esc(e.label + ", " + d.toLocaleDateString("en-CA", { month: "long", day: "numeric" })) + '"' + (e.slug ? ' data-post="' + esc(e.slug) + '"' : e.rid ? ' data-go="r:' + esc(e.rid) + '"' : "") + ">" + esc(e.label) + "</button>").join("") +
      (mine.length > cap ? '<span class="note">+' + (mine.length - cap) + " more</span>" : "") + "</div>";
  }
  return '<div class="tools"><button class="b secondary icon" data-cal="-1" aria-label="Earlier">' + ic("back", 18) + '</button><b style="font-size:16px;min-width:180px;text-align:center">' + title + '</b><button class="b secondary icon" data-cal="1" aria-label="Later">' + ic("chevron", 18) + '</button><button class="b ghost" data-cal="0">Today</button>' +
    (wide ? '<span style="margin-left:auto"></span><div class="seg" role="group" aria-label="Calendar view"><button data-calv="m"' + (week ? "" : ' class="on"') + '>Month</button><button data-calv="w"' + (week ? ' class="on"' : "") + ">Week</button></div>" : "") + "</div>" +
    '<div class="card cal rise' + (week ? " week" : "") + '"' + R() + '><div class="dow">' + ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => "<div>" + d + "</div>").join("") + '</div><div class="days">' + grid + "</div></div>" +
    '<div class="callegend"><span class="ev post" style="width:auto">Posts</span><span class="ev launch" style="width:auto">Opening dates</span><span class="ev cut" style="width:auto">Founding cutoff</span><span class="ev deal" style="width:auto">Deals start and end</span></div>' +
    '<p class="note">Click a scheduled post to move it to another time.</p>';
}
function calendarWire() {
  $$("[data-cal]").forEach((b) => b.onclick = () => { const s = +b.dataset.cal; if (!s) CAL.at = new Date(); else if (CAL.week && innerWidth > 760) CAL.at.setDate(CAL.at.getDate() + 7 * s); else CAL.at = new Date(CAL.at.getFullYear(), CAL.at.getMonth() + s, 1); paint(); });
  $$("[data-calv]").forEach((b) => b.onclick = () => { CAL.week = b.dataset.calv === "w"; paint(); });
  $$("[data-post]").forEach((b) => b.onclick = async () => {
    const p = BLOG.posts.find((x) => x.slug === b.dataset.post); if (!p) return;
    if (p.status !== "queued") return openPost(p.slug);
    const v = await ask({ title: "Move this post", body: esc(p.title) + " goes live at the next site update after this time.", input: '<input class="f" type="datetime-local" id="dlg-time" value="' + localInput(p.publish_at) + '" style="width:100%">', ok: "Save time" });
    if (v === false) return; if (!v) return toast("Pick a date and time first.", true);
    const r = await api("blog-set", { slug: p.slug, publish_at: new Date(v).toISOString() });
    if (r.error) return toast(r.error, true); toast("Time saved."); await blogLoad(); paint();
  });
}

// ---- Blog
let BLOG = null;
const postPill = (p) => p.status === "taken-down" ? '<span class="pill r">Taken down</span>' : p.status === "queued" ? '<span class="pill b">Goes live ' + esc(when(p.publish_at)) + "</span>" : p.visible === false ? '<span class="pill">Going live at the next site update</span>' : '<span class="pill g">Live</span>';
function postActions(p) {
  const s = esc(p.slug);
  if (p.status === "taken-down") return '<button class="b secondary" data-bup="' + s + '">Put back</button>';
  if (p.status === "queued") return '<button class="b primary" data-bnow="' + s + '">Publish now</button><input class="f" type="datetime-local" id="bt-' + s + '" aria-label="New time" value="' + localInput(p.publish_at) + '"><button class="b secondary" data-btime="' + s + '">Save time</button>';
  return '<a class="b secondary" href="/blog/' + s + '" target="_blank" rel="noopener">Open</a><button class="b danger" data-bdown="' + s + '">Take down</button>';
}
function blogHtml() {
  if (!BLOG) return skeleton(8);
  if (BLOG.error) return emptyState("Could not load the posts", esc(BLOG.error));
  const P = BLOG.posts || [];
  const warn = BLOG.hooks === false ? '<div class="hint r"><b>Not connected to the live blog yet.</b> Your choices are saved here, but the site does not act on them until the next site update that connects this page.</div>' : "";
  return warn + '<div class="grid three">' + mini("Live", P.filter((p) => p.status === "live").length) + mini("Scheduled", P.filter((p) => p.status === "queued").length) + mini("Taken down", P.filter((p) => p.status === "taken-down").length) + "</div>" +
    '<p class="note" style="margin:16px 0">Taking a post down hides it within about a minute; the next site update (within the hour) removes it completely. Publishing now or a new time takes effect at the next site update. Scheduled posts go live on their own at 12 am, 6 am, 12 pm or 6 pm Toronto time. Nothing here changes a post’s words.' +
    (BLOG.source === "live-site" ? " Showing the posts on the live site for now (the full list with scheduled posts appears after the next site update)." : "") + "</p>" +
    table(["Post", "Status", ["Words", "n"]], P.map((p) => ["<b>" + esc(p.title) + '</b><span class="sub">' + esc(p.date || "") + (p.topic ? " · " + esc(p.topic) : "") + "</span>", postPill(p), p.words ? num(p.words) : "–"]),
      ["No posts yet", "Posts are written in the site’s code; they show up here to schedule or take down."], "Search posts", P.map((p) => "p:" + p.slug));
}
async function blogLoad() {
  BLOG = await api("blog-list").catch(() => ({ error: "The list did not load. Refresh to try again." }));
  badge("blog", BLOG.posts ? BLOG.posts.filter((p) => p.status === "live").length : null);
  const q = $("#q-posts"); if (q) q.textContent = BLOG.posts ? BLOG.posts.filter((p) => p.status === "queued").length : "–";
  if (view === "blog" || view === "calendar") paint();
}
function blogWire(root) {
  const set = async (btn, body, ask1) => {
    if (ask1 && !(await ask(ask1))) return;
    await busy(btn, async () => { const r = await api("blog-set", body); if (r.error) toast(r.error, true); else toast("Saved."); });
    closePanels(); await blogLoad();
  };
  $$("[data-bdown]", root).forEach((b) => b.onclick = () => set(b, { slug: b.dataset.bdown, hidden: true }, { title: "Take this post down?", body: "It disappears for visitors within about a minute. You can put it back any time.", ok: "Take down", danger: true }));
  $$("[data-bup]", root).forEach((b) => b.onclick = () => set(b, { slug: b.dataset.bup, hidden: false }));
  $$("[data-bnow]", root).forEach((b) => b.onclick = () => set(b, { slug: b.dataset.bnow, publish_at: new Date(Date.now() - 60000).toISOString() }, { title: "Publish this post now?", body: "It goes live at the next site update (within the hour).", ok: "Publish now" }));
  $$("[data-btime]", root).forEach((b) => b.onclick = () => { const v = ($("#bt-" + b.dataset.btime, root) || {}).value; if (!v) return toast("Pick a date and time first.", true); set(b, { slug: b.dataset.btime, publish_at: new Date(v).toISOString() }); });
}

// ---- Paid restaurants: the founding pre-sale (FIX-LIST #141) through /api/admin-api; the Stripe work is the presale-admin function's.
// The switch (on only when ready), Start billing (a day 15 to 360 days ahead, typed START), each deposit's refund (after the 14 days
// only as FIG's choice, said so), and every deposit's refund (from March 1, 2027 while FIG is closed to diners, typed REFUND ALL).
let PS = null;
const PLAN_NAME = { monthly: "Founding monthly", annual: "Founding annual" };
const PLAN_PRICE = { monthly: "$9.99/mo to month 12, then $29.99/mo", annual: "$59.99 the first year, then $299.99/yr" };
const PS_STATUS = { trialing: ["Deposit held", "b"], active: ["Paying", "g"], past_due: ["Payment failed", "r"], unpaid: ["Unpaid", "r"], canceled: ["Cancelled", ""], incomplete: ["Not finished", ""] };
const PS_WORDS = { "too-soon": "Pick a day at least 14 days from today.", "too-far": "Pick a day within 360 days.", "not-set-up": "The live Stripe prices aren’t set yet.",
  "deposit-locked": "The 14 days have passed.", "already-refunded": "That deposit was already refunded.", "not-paid": "No deposit was paid for this plan.", "payment-not-found": "Stripe hasn’t shown this deposit’s payment yet. Try again in a few minutes, or refund it in Stripe.",
  "not-subscribed": "There’s no plan for this restaurant.", "too-early": "Every deposit can be refunded from March 1, 2027.",
  "opened": "FIG has opened to diners, so the March 1 refund doesn’t apply.", "not-deployed": "The presale functions aren’t deployed yet." };
const psWord = (e) => PS_WORDS[e] || e;
const longDay = (t) => t ? new Date(t).toLocaleDateString("en-CA", { timeZone: "America/Toronto", dateStyle: "long" }) : "";
const dayIn = (n) => dayKey(Date.now() + n * 86400000);
const refundLeft = (p) => p.deposit_paid_at ? Math.ceil((Date.parse(p.deposit_paid_at) + 14 * 86400000 - Date.now()) / 86400000) : null;
function paidHtml() {
  if (!PS) return skeleton(8);
  const rows = PS.rows || [], kept = rows.filter((p) => !p.refunded_at && p.status !== "canceled");
  const held = kept.reduce((s, p) => s + (p.deposit_cents || 0), 0) / 100;
  const problem = PS.error ? '<div class="hint r"><b>Not ready yet.</b> ' + esc(psWord(PS.error)) + "</div>"
    : !PS.ready ? '<div class="hint r"><b>Not ready yet.</b> The four live Stripe prices aren’t set, so the offer can’t be turned on.</div>' : "";
  const sw = '<div class="wl-row"><div class="wl-k"><b>Founding offer</b><span class="note">' + (PS.on
      ? "On: owners see “Lock in your founding spot” in Settings and can pay a deposit."
      : "Off: owners can’t start a plan. Plans already paid keep working, and refunds and billing still run.") + "</span></div>" +
    '<button class="switch' + (PS.on ? " on" : "") + '" id="ps-on" role="switch" aria-checked="' + !!PS.on + '" aria-label="Founding offer"><span></span></button></div>';
  const start = PS.startsAt
    ? '<div class="wl-row"><div class="wl-k"><b>Billing starts ' + esc(longDay(PS.startsAt)) + '</b><span class="note">Each deposit pays its first month or year from that day. New founding plans are closed.</span></div></div>'
    : '<div class="mo"><b>Start billing</b><div class="ctl"><input class="f" id="ps-at" type="date" style="width:200px" min="' + dayIn(15) + '" max="' + dayIn(360) + '" aria-label="Billing start day"><button class="b primary" id="ps-start">Start billing</button></div>' +
      '<div class="note">The day FIG opens to diners, 15 to 360 days from today. Tell every owner the date in writing at least 14 days before. Each deposit then pays its first month or year from that day, and new founding plans close. It can’t be undone here.</div></div>';
  const d = PS.daysToNoLaunch;
  const march = '<div class="wl-row"><div class="wl-k"><b>March 1, 2027 refund</b><span class="note">' + (PS.opened ? "FIG has opened to diners, so this doesn’t apply."
      : d > 0 ? "If FIG hasn’t opened to diners by March 1, 2027 (" + num(d) + " days from now), every deposit for a plan that hasn’t started is refunded in full. The button works from that day."
      : "FIG hasn’t opened to diners by March 1, 2027: refund every deposit for a plan that hasn’t started.") + "</span></div>" +
    '<button class="b danger" id="ps-all"' + (PS.opened || !(d <= 0) ? " disabled" : "") + ">Refund every deposit</button></div>";
  const minis = '<div class="grid three">' + mini("Founding plans", num(kept.length)) + mini("Deposits held", money(held)) +
    mini("Annual · monthly", num(kept.filter((p) => p.plan === "annual").length) + " · " + num(kept.filter((p) => p.plan === "monthly").length)) + "</div>";
  return problem + card("wl-plan", sw + start + march) + minis +
    // one plan per owner, covering all their restaurants (the user, #27): the row is the owner; where it started and how many it covers
    table(["Owner", "Plan", "Status", "First period starts", ["Deposit", "n"], ""], rows.map((p) => {
      // an annual plan stays "trialing" at Stripe through its paid first year: once its start day has passed it's paying (#186)
      const started = !!p.starts_at && Date.parse(p.starts_at) <= Date.now();
      const st = p.refunded_at ? ["Refunded", ""] : p.status === "trialing" && started ? PS_STATUS.active : PS_STATUS[p.status] || [p.status, ""], left = refundLeft(p);
      const n = p.restaurant_count || 0;
      return ["<b>" + esc((p.profiles || {}).email || "An owner") + '</b><span class="sub">' + num(n) + (n === 1 ? " restaurant" : " restaurants") + ((p.restaurants || {}).name ? " · started at " + esc(p.restaurants.name) : "") + "</span>",
        esc(PLAN_NAME[p.plan] || p.plan) + '<span class="sub">' + esc(PLAN_PRICE[p.plan] || "") + "</span>",
        '<span class="pill ' + st[1] + '">' + esc(st[0]) + "</span>" + (p.paid_through ? '<span class="sub">Paid through ' + esc(longDay(p.paid_through)) + "</span>" : ""),
        p.starts_at ? esc(longDay(p.starts_at)) : '<span class="sub">When billing starts</span>',
        p.deposit_cents ? money(p.deposit_cents / 100) + '<span class="sub">' + (p.refunded_at ? "Refunded " + esc(longDay(p.refunded_at)) : left > 0 ? num(left) + (left === 1 ? " day" : " days") + " to refund" : "Paid " + esc(longDay(p.deposit_paid_at))) + "</span>" : "–",
        p.refunded_at || !p.deposit_cents ? "" : '<button class="b secondary" data-psref="' + esc(p.owner_id) + '" data-late="' + (left > 0 ? "0" : "1") + '">Refund</button>'];
    }), ["No founding plans yet", "When an owner pays a founding deposit, it shows up here."], "Search restaurants or owners");
}
async function paidLoad() {
  PS = await api("presale-get").catch(() => ({ error: "It did not load. Refresh to try again." }));
  if (view === "paid") paint();
}
// a typed word for the two big actions: the dialog's field, compared without case
const typedOk = (v, word) => typeof v === "string" && v.trim().toUpperCase() === word;
function paidWire() {
  const run = async (btn, what, body, done) => { await busy(btn, async () => { const r = await api(what, body); if (r && r.error) toast(psWord(r.error), true); else toast(done(r || {})); }); await paidLoad(); };
  const many = (r) => (r.failed && r.failed.length ? " " + num(r.failed.length) + " didn’t go through: try again." : "");
  const sw = $("#ps-on"); if (sw) sw.onclick = async () => {
    const on = sw.getAttribute("aria-checked") !== "true";
    if (!(await ask(on ? { title: "Turn the founding offer on?", body: "Owners can pay a real deposit from now on. Turn it on only after the test-mode run passed, with the live prices set and the website’s prices published.", ok: "Turn it on" }
      : { title: "Turn the founding offer off?", body: "No new founding plans. Plans already paid keep working, and refunds and billing still run.", ok: "Turn it off", danger: true }))) return;
    run(sw, "presale-switch", { on }, () => on ? "The founding offer is on." : "The founding offer is off.");
  };
  const st = $("#ps-start"); if (st) st.onclick = async () => {
    const v = ($("#ps-at") || {}).value || ""; if (!v) return toast("Pick the day first.", true);
    const at = new Date(v + "T00:00:00"), day = at.toLocaleDateString("en-CA", { dateStyle: "long" });
    const typed = await ask({ title: "Start billing on " + day + "?", body: esc("Each deposit’s first month or year starts that day, and the next charge follows it. New founding plans close. Have you told every owner in writing, at least 14 days before? Type START to confirm."),
      ok: "Start billing", danger: true, input: '<input class="f" id="dlg-start" autocomplete="off" aria-label="Type START">' });
    if (typed === false) return;
    if (!typedOk(typed, "START")) return toast("Type START to confirm.", true);
    run(st, "presale-start", { at: at.toISOString() }, (r) => "Billing starts " + day + ": " + num(r.moved || 0) + (r.moved === 1 ? " plan" : " plans") + " moved." + many(r));
  };
  $$("[data-psref]").forEach((b) => b.onclick = async () => {
    const p = (PS.rows || []).find((x) => x.owner_id === b.dataset.psref) || {}, late = b.dataset.late === "1";
    const name = (p.profiles || {}).email || "this owner";
    if (!(await ask({ title: "Refund " + name + "’s deposit?", body: esc((late ? "The 14 days have passed, so this refund is FIG’s choice, not the owner’s right. " : "") + "The whole deposit goes back to their card and the plan is cancelled now."), ok: late ? "Refund anyway" : "Refund", danger: true }))) return;
    run(b, "presale-refund", { owner: p.owner_id, force: late }, () => "Refunded. It reaches their card in 5 to 10 days.");
  });
  const all = $("#ps-all"); if (all) all.onclick = async () => {
    const w = PS.refundAllWould || { count: 0, cents: 0 };
    if (!w.count) return toast("No plan is waiting for its start, so there's nothing to refund.", true);
    const typed = await ask({ title: "Refund " + num(w.count) + (w.count === 1 ? " deposit" : " deposits") + ", " + money(w.cents / 100) + "?", body: esc("Each plan that hasn’t started (" + num(w.count) + ", " + money(w.cents / 100) + " in all) is refunded in full and cancelled. Plans already paying are left alone. Type REFUND ALL to confirm."),
      ok: "Refund every deposit", danger: true, input: '<input class="f" id="dlg-all" autocomplete="off" aria-label="Type REFUND ALL">' });
    if (typed === false) return;
    if (!typedOk(typed, "REFUND ALL")) return toast("Type REFUND ALL to confirm.", true);
    run(all, "presale-refund-all", {}, (r) => num(r.refunded || 0) + " refunded." + many(r));
  };
}

// ---- Waitlist: the launch plan and the list (diner_waitlist through /api/admin-api)
let DIN = null;
// The launch plan (the user, 2026-10-17): 1 collect the waitlist (closed) -> 2 the first N -> 3 the opening date (founding members
// get in by themselves then; the list closes then) -> 4 everyone. The effective mode comes from the database (site_mode), so a
// passed opening date shows as open to founding members. waitlist: setDinersMode closes the list now only the first time; a
// cutoff already set stays (FIX-LIST #57)
const MODE_ASK = {
  off: () => "Diners will only be able to join the waitlist (anyone already using FIG as a diner sees it too); restaurants aren't affected.",
  waitlist: () => (DIN.cap ? "The first " + DIN.cap.toLocaleString("en-CA") + " on the waitlist" : "Everyone on the waitlist") + " can sign in and use everything now, as founding members; " +
    (DIN.until ? "the list keeps its cutoff (" + atText(DIN.until) + "), so who joined before it gets in." : "the list closes now."),
  on: () => "FIG opens to everyone: anyone can sign up, browse, claim deals and order. This is the public launch.",
};
const MODE_OK = { off: "Turn waitlist mode on", waitlist: "Let them in", on: "Turn waitlist mode off" };
const atText = (iso) => new Date(iso).toLocaleString("en-CA", { dateStyle: "medium", timeStyle: "short", timeZone: "America/Toronto" });
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
// the plan in two controls (the user, FIX-LIST #103): waitlist mode on or off, and letting the people on the list in.
// Everything finer (how many get in first, an opening date, the founding cutoff) sits under More options, closed by default.
let MORE = false;
function modeHtml() {
  if (!DIN) return "";
  if (DIN.error) return '<div class="hint r"><b>The launch plan could not load.</b> ' + esc(DIN.error) + ' <button class="b secondary" id="lnch-retry" style="margin-left:12px">Try again</button></div>';
  const n = (DIN.waitlist || []).length, agreed = (DIN.waitlist || []).filter((w) => w.consent).length, eff = DIN.effective || DIN.mode;
  const first = DIN.cap ? "the first " + DIN.cap.toLocaleString("en-CA") : "everyone";
  const on = eff !== "on"; // waitlist mode: diners can only join the list (closed, or founding members only)
  const sw = '<div class="wl-row"><div class="wl-k"><b>Waitlist mode</b><span class="note">' + (on
      ? "On: diners can only join the waitlist" + (eff === "waitlist" ? " (founding members are in)" : "") + ". Restaurants use FIG as normal."
      : "Off: FIG is open to everyone. Anyone can sign up, browse, claim and order.") + '</span></div>' +
    '<button class="switch' + (on ? " on" : "") + '" id="wl-mode" role="switch" aria-checked="' + on + '" aria-label="Waitlist mode"><span></span></button></div>';
  const who = DIN.cap ? "The first " + DIN.cap.toLocaleString("en-CA") + " on the list" : "Everyone on the list";
  const letIn = !on ? "" : eff === "off"
    ? '<div class="wl-row"><div class="wl-k"><b>Let everyone on the waitlist in</b><span class="note">' + who + " gets in now as founding members. Later sign-ups wait for the next wave.</span></div>" +
      '<button class="b primary" id="let-in">Let them in</button></div>'
    : '<div class="wl-row"><div class="wl-k"><b>Founding members are in</b><span class="note">' + who + (DIN.closes ? " who joined before " + esc(dot(atText(DIN.closes))) : ".") + " Let in the people who joined since, too:</span></div>" +
      '<button class="b secondary" id="until-now">Let in everyone who joined until now</button></div>';
  const counts = '<div class="note wl-counts">' + n.toLocaleString("en-CA") + " on the list · " + agreed.toLocaleString("en-CA") + " agreed to be emailed</div>";
  // More options: the cap, the opening date (with the #56-#69 help), the founding cutoff
  const cap = '<div class="mo"><b>How many get in first</b><div class="ctl"><span>The first</span><input class="f" id="cap-n" type="number" min="1" placeholder="everyone" value="' + (DIN.cap || "") + '" style="width:120px" aria-label="How many get in first"><span>on the list</span><button class="b secondary" id="cap-save">Save</button></div>' +
    '<div class="note">Empty = everyone on the list. Raise it or clear it later to let the next wave in.</div></div>';
  const date = '<div class="mo"><b>Opening date</b><div class="ctl"><input class="f" id="opens-at" type="datetime-local" value="' + localInput(DIN.opens) + '" aria-label="Opening date"><button class="b secondary" id="opens-save">Save</button>' + (DIN.opens ? '<button class="b danger" id="opens-clear">Clear</button>' : "") + "</div>" +
    '<div class="note">' + (eff === "off" && !DIN.opens ? "No date set. FIG stays closed until you open it here or with the switch; nothing opens by itself." // (FIX-LIST #138)
      : opensHelp(eff) + (eff === "on" ? "" : " The website shows the date." + (openedByDate() ? "" : " " +
    "Send the launch email before it: it isn't sent automatically. Download who agreed (below): each person has their own unsubscribe link to put in their email, which also needs FIG's name and a mailing address."))) + "</div></div>";
  const cutoff = eff !== "waitlist" ? "" : '<div class="mo"><b>Founding cutoff</b><div class="note">The founding list ' + (DIN.closes ? (passed(DIN.closes) ? "closed " : "closes ") + esc(dot(atText(DIN.closes))) : "is open.") + " People who join after it wait for the next wave.</div></div>";
  const more = '<details class="more-opts" id="more-opts"' + (MORE ? " open" : "") + '><summary>More options</summary>' + cap + date + cutoff + "</details>";
  return card("launch", '<div class="t">' + nowText(eff, first) + "</div>") + card("wl-plan", sw + letIn + counts + more);
}
function modeWire() {
  const t = $("#lnch-retry"); if (t) t.onclick = () => dinersLoad();
  const mo = $("#more-opts"); if (mo) mo.ontoggle = () => { MORE = mo.open; };
  const setMode = async (b, m) => { if (!(await ask({ title: MODE_OK[m] + "?", body: esc(MODE_ASK[m]()), ok: MODE_OK[m], danger: m === "off" }))) return; run(b, "diners-set", { mode: m }); };
  const sw = $("#wl-mode"); if (sw) sw.onclick = () => setMode(sw, sw.getAttribute("aria-checked") === "true" ? "on" : "off");
  const li = $("#let-in"); if (li) li.onclick = () => setMode(li, "waitlist");
  const run = async (btn, what, body) => { await busy(btn, async () => { const r = await api(what, body); if (r && r.error) toast(r.error, true); else toast("Saved."); }); await dinersLoad(); };
  $$("[data-mode]").forEach((b) => b.onclick = async () => { const m = b.dataset.mode; if (!(await ask({ title: MODE_OK[m] + "?", body: esc(MODE_ASK[m]()), ok: MODE_OK[m], danger: m === "off" }))) return; run(b, "diners-set", { mode: m }); });
  // empty = everyone (null). A number field reads "" for text it can't parse ("5,000"), so that's refused, never saved as everyone; clearing a set number asks first (FIX-LIST #105)
  const cs = $("#cap-save"); if (cs) cs.onclick = async () => {
    const f = $("#cap-n"), v = f.value.trim();
    if (f.validity.badInput || (v !== "" && !(Number.isInteger(Number(v)) && Number(v) >= 1 && Number(v) <= 1000000))) return toast("Type a whole number from 1 to 1,000,000, or leave it empty for everyone.", true);
    if (v === "" && DIN.cap && !(await ask({ title: "Let everyone on the list in?", body: "With no number, everyone on the list gets in as a founding member, not just the first " + DIN.cap.toLocaleString("en-CA") + ".", ok: "Let everyone in" }))) return;
    run(cs, "founding-cap", { cap: v === "" ? null : Number(v) });
  };
  const os = $("#opens-save"); if (os) os.onclick = async () => {
    const v = ($("#opens-at") || {}).value || ""; if (!v) return toast("Pick a date and time first.", true);
    const at = new Date(v); if (isNaN(at) || at < new Date()) return toast("Pick a time in the future.", true);
    if (!(await ask({ title: "Save the opening date?", body: esc(opensAsk(DIN.effective || DIN.mode, atText(at.toISOString()))), ok: "Save the date" }))) return;
    run(os, "opens-at", { at: at.toISOString() });
  };
  const oc = $("#opens-clear"); if (oc) oc.onclick = async () => { if (!(await ask({ title: "Clear the opening date?", body: openedByDate() ? "Founding members are in now. Clearing the date closes FIG to them again until you set a new date." : "The website stops showing a date.", ok: "Clear it", danger: true }))) return; run(oc, "opens-at", { at: null }); };
  const un = $("#until-now"); if (un) un.onclick = async () => { if (!(await ask({ title: "Let them in?", body: "Let in everyone who has joined the list until now (within the first N, if set)? Later sign-ups still wait.", ok: "Let them in" }))) return; run(un, "founding-until", { until: "now" }); };
}
function dinersHtml() {
  if (!DIN) return skeleton(10);
  if (DIN.error) return emptyState("Could not load this", esc(DIN.error));
  const W = DIN.waitlist || [], agreed = W.filter((w) => w.consent).length;
  return modeHtml() + '<div class="grid three">' + mini("On the waitlist", num(W.length)) + mini("Agreed to be emailed", num(agreed)) + mini("Diner accounts", num(DIN.accounts)) + "</div>" +
    sourcesHtml() + linkToolHtml() +
    '<h2>Everyone on the list <span class="count">' + num(W.length) + '</span><span class="push"></span><button class="b secondary" id="din-copy">Who agreed, with unsubscribe links (CSV)</button><button class="b secondary" id="din-csv">Download as a table (CSV)</button></h2>' +
    table(["Email", "School", "May email", "From", ["Joined", "n"]], W.slice(0, 600).map((w) => [esc(w.email), esc(w.school || ""), w.consent ? '<span class="pill g">Yes</span>' : '<span class="pill">No</span>', esc(w.source || "website"), ago(w.joined_at)]),
      ["Nobody yet", "Sign-ups from the website’s waitlist form appear here."], "Search emails, schools or links", W.slice(0, 600).map((_, i) => "w:" + i));
}
async function dinersLoad() {
  DIN = await api("diners-get").catch(() => ({ error: "It did not load. Refresh to try again." }));
  badge("waitlist", DIN.waitlist ? DIN.waitlist.length : null);
  if (view === "overview" || view === "waitlist" || view === "calendar") paint();
}
function dinersWire() {
  modeWire();
  const rows = (DIN && DIN.waitlist) || [];
  // the launch email goes out by hand: each person with their own unsubscribe link, ready for a mail merge (FIX-LIST #103)
  // a CSV cell (FIX-LIST #170): quoted, and a cell that starts like a formula (= + - @, a tab or a CR) gets a ' in front, so a
  // spreadsheet shows it as text instead of running it (a school typed as =WEBSERVICE(...) could send the list's emails out)
  const csvCell = (v) => { let t = String(v == null ? "" : v); if (/^[=+\-@\t\r]/.test(t)) t = "'" + t; return '"' + t.split('"').join('""') + '"'; };
  const cp = $("#din-copy"); if (cp) cp.onclick = () => busy(cp, async () => {
    const r = await api("agreed-csv"); if (!r || !r.rows) return toast((r && r.error) || "It didn't load. Try again.", true);
    const q = csvCell;
    const csv = ["email,unsubscribe_link"].concat(r.rows.map((x) => q(x.email) + "," + q(x.unsubscribe))).join(String.fromCharCode(10));
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" })); a.download = "fig-waitlist-agreed.csv"; a.click();
    toast(r.rows.length + " people. Put each one's link in their email.");
  });
  const cs = $("#din-csv"); if (cs) cs.onclick = () => {
    const q = csvCell;
    const csv = ["email,school,may_email,source,joined"].concat(rows.map((w) => [q(w.email), q(w.school), w.consent ? "yes" : "no", q(w.source), q(w.joined_at)].join(","))).join(String.fromCharCode(10));
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" })); a.download = "fig-diner-waitlist.csv"; a.click();
  };
}

// ---- Growth (FIX-LIST #103): the waitlist, diner accounts and restaurants, all time: running totals as lines, new per day as
// bars, over 7 / 30 / 90 days or all time (its own switch); today's totals are the legend. Read-only.
let GR = 30;
function growthHtml() {
  const g = CH && CH.growth;
  if (!g) return "";
  const n = GR === 0 ? g.keys.length : Math.min(GR, g.keys.length), keys = g.keys.slice(-n);
  const S = [["Waitlist", g.waitlist, COLORS[0]], ["Diner accounts", g.diners, COLORS[2]], ["Restaurants", g.restaurants, COLORS[4]]];
  const totals = S.map(([name, fresh, color]) => { let run = 0; return { name, color, total: fresh.map((v) => (run += v)), fresh }; });
  const seg = '<span class="seg" role="group" aria-label="Growth range">' + [[7, "7 days"], [30, "30 days"], [90, "90 days"], [0, "All time"]].map(([v, label]) =>
    '<button data-gr="' + v + '"' + (GR === v ? ' class="on" aria-pressed="true"' : ' aria-pressed="false"') + ">" + label + "</button>").join("") + "</span>";
  const legendNow = '<div class="legend">' + totals.map((t) => '<span><i style="background:' + t.color + '"></i>' + esc(t.name) + " <b>" + num(t.total[t.total.length - 1]) + "</b> today</span>").join("") + "</div>";
  return '<h2>Growth<span class="push"></span>' + seg + "</h2>" + card("chartcard growth", legendNow +
    chartBox({ keys, h: 220, label: "Running totals: waitlist, diner accounts and restaurants", series: totals.map((t) => ({ name: t.name, values: t.total.slice(-n), kind: "line", color: t.color })) }) +
    '<div class="note" style="margin:10px 0 4px">New per day</div>' +
    chartBox({ keys, h: 120, stack: true, label: "New per day: waitlist, diner accounts and restaurants", series: totals.map((t) => ({ name: t.name, values: t.fresh.slice(-n), kind: "bar", color: t.color })) }));
}

// ---- Sources (FIX-LIST #105): where the waitlist, diner accounts and restaurants came from. "Link they came from" is the ?src= tag,
// its kind read from how the link maker starts it (creator-, qr-, flyer-; anything else is a link; none is direct). "What they told us"
// is the answer to "How did you hear about FIG?" (accounts only). Bars per day over the page's range, stacked by kind.
let SRC = null, SRC_WHO = "waitlist";
const SRC_KINDS = [["creator", "Creator"], ["qr", "QR code"], ["flyer", "Flyer"], ["link", "Other link"], ["app", "Signed up in the app"], ["direct", "Direct"]];
const HEARD = [["tiktok", "TikTok"], ["instagram", "Instagram"], ["friend", "A friend"], ["flyer", "Flyer or QR code"], ["restaurant", "At a restaurant"], ["school", "School"], ["google", "Google"],
  ["owner", "Another restaurant owner"], ["fig", "FIG reached out"], ["other", "Other"], ["skipped", "Skipped"]];
const srcKind = (t) => !t ? "direct" : t === "account" ? "app" : (SRC_KINDS.find(([k]) => t.startsWith(k + "-")) || ["link"])[0];
async function sourcesLoad() {
  SRC = await api("sources-get").catch(() => ({ error: "It did not load." }));
  if (view === "overview" || view === "waitlist") paint();
}
function hbars(rows, total) {
  if (!total) return '<div class="note">Nobody in this range yet.</div>';
  return '<div class="hbars">' + rows.filter((r) => r[1]).map(([label, n, color]) => '<div class="hb"><span>' + esc(label) + '</span><i style="--w:' + Math.max(2, Math.round(n / total * 100)) + '%;background:' + color + '"></i><b>' + num(n) + "</b></div>").join("") + "</div>";
}
function sourcesHtml() {
  const head = "<h2>Sources" + '<span class="push"></span><span class="seg" role="group" aria-label="Who">' + [["waitlist", "Waitlist"], ["diner", "Diner accounts"], ["business", "Restaurants"]].map(([k, label]) =>
    '<button data-src-who="' + k + '"' + (SRC_WHO === k ? ' class="on" aria-pressed="true"' : ' aria-pressed="false"') + ">" + label + "</button>").join("") + "</span></h2>";
  if (!SRC) return head + skeleton(3);
  if (SRC.error) return head + emptyState("Could not load this", esc(SRC.error));
  const keys = Array.from({ length: RANGE }, (_, i) => dayKey(Date.now() - (RANGE - 1 - i) * 86400000)), from = keys[0];
  const accounts = SRC.accounts;
  if (SRC_WHO !== "waitlist" && !accounts) return head + card("srcnote", '<div class="note">Accounts don’t record where they came from yet. This fills in once the sources update is switched on in the database.</div>');
  const rows = (SRC_WHO === "waitlist" ? SRC.waitlist : accounts.filter((a) => a.role === SRC_WHO)).filter((r) => dayKey(r.at) >= from);
  const series = (list, kindOf, kinds) => kinds.map(([k, label], i) => ({ name: label, values: keys.map((d) => list.filter((r) => kindOf(r) === k && dayKey(r.at) === d).length), kind: "bar", color: COLORS[i % COLORS.length] })).filter((x) => sum(x.values));
  const count = (list, kindOf, kinds) => kinds.map(([k, label], i) => [label, list.filter((r) => kindOf(r) === k).length, COLORS[i % COLORS.length]]).sort((a, b) => b[1] - a[1]); // each bar in its legend colour
  const byLink = (r) => srcKind(r.source), byHeard = (r) => r.heard || "none";
  const linkKinds = SRC_KINDS.filter(([k]) => k !== "app" || SRC_WHO === "waitlist");
  const tags = {}; rows.forEach((r) => { if (r.source && r.source !== "account") tags[r.source] = (tags[r.source] || 0) + 1; });
  const tagRows = Object.entries(tags).sort((a, b) => b[1] - a[1]).slice(0, 8);
  const ls = series(rows, byLink, linkKinds);
  const left = card("chartcard src", '<div class="head"><b>Link they came from</b><span class="big">' + num(rows.length) + "</span></div>" + hbars(count(rows, byLink, linkKinds), rows.length) +
    (ls.length ? legend(ls) + chartBox({ keys, stack: true, h: 160, label: "Sign-ups per day by the kind of link", series: ls }) : "") +
    (tagRows.length ? '<div class="tags">' + tagRows.map(([t, n]) => '<span class="pill">' + esc(t) + " · " + num(n) + "</span>").join(" ") + "</div>" : ""));
  let right;
  if (SRC_WHO === "waitlist") right = card("chartcard src", '<div class="head"><b>What they told us</b></div><div class="note">The waitlist doesn’t ask. Diner accounts and restaurants are asked “How did you hear about FIG?” once, right after they sign up.</div>');
  else {
    const kinds = HEARD.filter(([k]) => SRC_WHO === "business" || (k !== "owner" && k !== "fig")), asked = rows.filter((r) => r.heard);
    const hs = series(asked, byHeard, kinds), notes = [...new Set(asked.filter((r) => r.heard === "other" && r.note).map((r) => r.note))].slice(0, 6);
    right = card("chartcard src", '<div class="head"><b>What they told us</b><span class="big">' + num(asked.length) + "</span></div>" + hbars(count(asked, byHeard, kinds), asked.length) +
      (hs.length ? legend(hs) + chartBox({ keys, stack: true, h: 160, label: "Answers per day", series: hs }) : "") +
      (notes.length ? '<div class="note">Other: ' + notes.map((n) => "“" + esc(n) + "”").join(", ") + "</div>" : "") +
      (rows.length > asked.length ? '<div class="note">' + num(rows.length - asked.length) + " not answered yet (or signed up before the question).</div>" : ""));
  }
  return head + '<div class="note" style="margin:-4px 0 10px">The last ' + RANGE + " days. Restaurants and diners never see this.</div>" + '<div class="charts">' + left + right + "</div>";
}
// the link maker: a ?src= link to the waitlist or the app, its kind first in the tag, copy it, and a QR with FIG's tile
const LT = { where: "waitlist", kind: "creator", name: "" };
const ltTag = () => { const n = LT.name.toLowerCase().replace(/[^a-z0-9_-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40 - LT.kind.length - 1); return n ? LT.kind + "-" + n : ""; };
const ltUrl = () => ltTag() ? location.origin + (LT.where === "app" ? "/app?src=" : "/?src=") + ltTag() + (LT.where === "app" ? "" : "#waitlist") : "";
function linkToolHtml() {
  return "<h2>Make a tracking link</h2>" + card("linktool", '<div class="lt-form">' +
    '<label>Where it goes<span class="seg" role="group" aria-label="Where it goes">' + [["waitlist", "Waitlist (website)"], ["app", "The app"]].map(([k, label]) => '<button data-lt-where="' + k + '"' + (LT.where === k ? ' class="on" aria-pressed="true"' : ' aria-pressed="false"') + ">" + label + "</button>").join("") + "</span></label>" +
    '<label>What it’s for<select class="f" id="lt-kind">' + SRC_KINDS.slice(0, 4).map(([k, label]) => '<option value="' + k + '"' + (LT.kind === k ? " selected" : "") + ">" + label + "</option>").join("") + "</select></label>" +
    '<label>A name<input class="f" id="lt-name" maxlength="32" placeholder="e.g. jane, front-counter" value="' + esc(LT.name) + '"></label></div>' +
    '<div class="lt-out" id="lt-out"></div>' +
    '<div class="note">The app link feeds the app’s waitlist while diners are closed. Sign-ups through either show here under Sources.</div>');
}
function linkToolOut() {
  const box = $("#lt-out"); if (!box) return;
  const url = ltUrl();
  box.innerHTML = url ? '<code id="lt-url">' + esc(url) + '</code><button class="b secondary" id="lt-copy">Copy the link</button><div id="lt-qr" class="lt-qr" aria-live="polite"></div>' : '<div class="note">Type a name to make the link.</div>';
  if (!url) return;
  $("#lt-copy").onclick = () => copyText(url, "Link");
  clearTimeout(linkToolOut.t);
  linkToolOut.t = setTimeout(async () => {
    const r = await api("qr", { url }).catch(() => ({}));
    const q = $("#lt-qr"); if (!q || ltUrl() !== url) return;
    if (!r.svg) { q.innerHTML = '<div class="note">The QR code didn’t load.</div>'; return; }
    q.innerHTML = r.svg + '<a class="b secondary" download="fig-qr-' + esc(ltTag()) + '.svg" href="data:image/svg+xml;charset=utf-8,' + encodeURIComponent(r.svg) + '">Download the QR (SVG)</a>';
  }, 300);
}
function sourcesWire() {
  $$("[data-src-who]").forEach((b) => b.onclick = () => { SRC_WHO = b.dataset.srcWho; paint(); });
  $$("[data-lt-where]").forEach((b) => b.onclick = () => { LT.where = b.dataset.ltWhere; $$("[data-lt-where]").forEach((x) => { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", String(x === b)); }); linkToolOut(); });
  const k = $("#lt-kind"); if (k) k.onchange = () => { LT.kind = k.value; linkToolOut(); };
  const n = $("#lt-name"); if (n) n.oninput = () => { LT.name = n.value; linkToolOut(); };
  linkToolOut();
}

// ---- Outreach's places directory (through /api/admin-api -> prospect_list, prospect_set)
let PRO = null; const PF = { q: "", kind: "", status: "", short: false, independent: true, hideFig: false, offset: 0 };
const PSTATS = [["new", "Not contacted"], ["contacted", "Contacted"], ["interested", "Interested"], ["not-interested", "Not interested"], ["signed", "Signed up"]];
const mapsUrl = (p) => "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(p.name + " " + p.street + " Markham Ontario");
function prosHtml() {
  if (!PRO) return skeleton(8);
  if (PRO.error) return emptyState("Could not load this", esc(PRO.error));
  const kinds = '<option value="">All kinds</option>' + (PRO.kinds || []).map((k) => '<option value="' + esc(k) + '"' + (PF.kind === k ? " selected" : "") + ">" + esc(k.split("_").join(" ")) + "</option>").join("");
  const stat2 = '<option value="">Any status</option>' + PSTATS.map((s) => '<option value="' + s[0] + '"' + (PF.status === s[0] ? " selected" : "") + ">" + s[1] + "</option>").join("");
  const check = (id, on, label) => '<label><input type="checkbox" id="' + id + '"' + (on ? " checked" : "") + "> " + label + "</label>";
  const bar = '<div class="tools"><label class="search">' + ic("search", 18) + '<input id="pr-q" placeholder="Search name, street or postcode" value="' + esc(PF.q) + '" aria-label="Search places"></label><select class="f" id="pr-kind" aria-label="Kind">' + kinds + '</select><select class="f" id="pr-status" aria-label="Status">' + stat2 + '</select><button class="b primary" id="pr-go">Search</button></div>' +
    '<div class="tools" style="gap:16px">' + check("pr-short", PF.short, "Shortlist only") + check("pr-ind", PF.independent, "Independents only (hide big chains)") + check("pr-fig", PF.hideFig, "Hide ones already on FIG") + "</div>";
  const from = PRO.total ? PF.offset + 1 : 0, to = Math.min(PF.offset + 50, PRO.total);
  const rows = (PRO.rows || []).map((p) => [
    '<button class="link" data-star="' + esc(p.id) + '" data-on="' + (p.shortlisted ? 1 : 0) + '" aria-label="' + (p.shortlisted ? "Take off the shortlist" : "Shortlist") + '" style="font-size:20px">' + (p.shortlisted ? "★" : "☆") + "</button>",
    "<b>" + esc(p.name) + "</b>" + (p.chain ? ' <span class="pill">Chain</span>' : "") + (p.on_fig ? ' <span class="pill g">On FIG</span>' : "") + '<span class="sub">' + esc(p.street) + (p.postcode ? ", " + esc(p.postcode) : "") + ' · <a class="link" style="font-size:12px" href="' + esc(mapsUrl(p)) + '" target="_blank" rel="noopener">Open in Maps</a></span>',
    esc((p.kind || "").split("_").join(" ")),
    '<select class="f" data-st="' + esc(p.id) + '" aria-label="Status">' + PSTATS.map((s) => '<option value="' + s[0] + '"' + (p.status === s[0] ? " selected" : "") + ">" + s[1] + "</option>").join("") + "</select>" + (p.contacted_at ? '<span class="sub">First contact ' + ago(p.contacted_at) + "</span>" : ""),
    '<input class="f" data-note="' + esc(p.id) + '" value="' + esc(p.note || "") + '" placeholder="Who to ask for, when to come back" maxlength="500" style="width:100%;min-width:220px" aria-label="Notes">']);
  return '<div class="grid six">' + mini("Places", num(PRO.places)) + mini("Shortlisted", num(PRO.shortlisted)) + mini("Contacted", num(PRO.contacted)) + mini("Interested", num(PRO.interested)) + mini("On FIG", num(PRO.signed)) + "</div><div style=\"height:16px\"></div>" + bar +
    '<p class="note" style="margin:0 0 8px">' + num(PRO.total) + " places match. Showing " + from + "–" + to + ". Your shortlist comes first.</p>" +
    table(["", "Place", "Kind", "Status", "Notes"], rows, ["No places match", "Clear a filter or search for a street or postcode."]) +
    '<div class="tools"><button class="b secondary" id="pr-prev"' + (PF.offset ? "" : " disabled") + '>← Previous 50</button><button class="b secondary" id="pr-next"' + (to < PRO.total ? "" : " disabled") + ">Next 50 →</button></div>";
}
async function prosLoad() {
  PRO = await api("prospects-list", PF).catch(() => ({ error: "It did not load. Refresh to try again." }));
  if (view === "restaurants" && SUB.restaurants === "outreach" && $("#prosbox")) { rise = 0; $("#prosbox").innerHTML = prosHtml(); prosWire(); }
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
  const save = async (body) => { const r = await api("prospects-set", body); if (r.error) toast(r.error, true); else toast("Saved."); };
  $$("[data-star]").forEach((b) => b.onclick = async () => { const on = b.dataset.on === "1"; await save({ id: b.dataset.star, short: !on }); read(); prosLoad(); });
  $$("[data-st]").forEach((s) => s.onchange = async () => { await save({ id: s.dataset.st, status: s.value }); read(); prosLoad(); });
  $$("[data-note]").forEach((i) => i.onchange = () => save({ id: i.dataset.note, note: i.value }));
}

// ---- Security (FIX-LIST #83): the authenticator app and "Sign out everywhere"
let SEC = null; // what's set up for the second step (second-get)
function securityHtml() {
  if (!SEC) { api("second-get").then((r) => { SEC = r && r.ok ? r : { error: (r && r.error) || "It didn't load." }; if (view === "security") paint(); }); return skeleton(4); }
  if (SEC.error) return emptyState("Could not load this", esc(SEC.error));
  const warn = SEC.reset ? card("state", '<span class="dot">' + ic("security") + '</span><div style="flex:1"><b class="red">ADMIN_TOTP_RESET is set</b><div class="muted" style="margin-top:4px">' + (SEC.resetUsed ? "That reset value was already used, so it does nothing. Delete it in Vercel (Settings → Environment Variables) and redeploy; to reset again, set a new value (for example today’s date)." : "Delete it in Vercel (Settings → Environment Variables) and redeploy. Each value works once.") + '</div></div>') : "";
  // "Require a code at every sign-in" (FIX-LIST #103 DESIGN): off until the user turns it on here; on only with a working
  // authenticator and its backup codes, and switching it either way takes a code
  const have = SEC.saved || SEC.env, ready = have && SEC.backupLeft > 0;
  const req = card("state", '<span class="dot">' + ic("security") + '</span><div style="flex:1"><b>Require a code at every sign-in</b> ' + (SEC.required ? '<span class="pill g">On</span>' : '<span class="pill">Off</span>') +
    '<div class="muted" style="margin:4px 0 12px">' + (SEC.required ? "Your password, then a code from the authenticator (or a backup code, or an emailed code), every time." :
      ready ? "Right now your password signs you in, then a code from the authenticator. Turn this on and setting up a new phone is only possible signed in, and the reset flag starts to work."
      : "Right now your password alone signs you in. Set up the authenticator above first: it gives you backup codes, and then this can be turned on.") + "</div>" +
    (ready || SEC.required ? '<div class="ctl"><input class="f" id="req-c" autocomplete="one-time-code" maxlength="12" placeholder="Code from the app, or a backup code"><button class="b ' + (SEC.required ? "secondary" : "primary") + '" id="req-go">' + (SEC.required ? "Turn off" : "Turn on") + "</button></div>" : "") + "</div>");
  return '<p class="lead">' + (SEC.required ? "Only you get in: your password, then a code, every time." : "Your password signs you in" + (have ? ", then a code from the authenticator." : ". Set up the authenticator, then turn on “Require a code” when you’re ready.")) + "</p>" + warn +
    card("state", '<span class="dot">' + ic("security") + '</span><div style="flex:1"><b>Authenticator app</b> ' + (SEC.required ? '<span class="pill g">Always on</span>' : have ? '<span class="pill g">Set up</span>' : '<span class="pill">Not set up</span>') +
      '<div class="muted" style="margin:4px 0 12px">' + (SEC.env ? "Using the secret set in Vercel (ADMIN_TOTP_SECRET)." : SEC.saved ? "Its secret is kept in the database, encrypted." : "An app like Google Authenticator or 1Password shows a new 6-digit code every 30 seconds.") +
      (SEC.backupLeft != null ? " " + SEC.backupLeft + " backup code" + (SEC.backupLeft === 1 ? "" : "s") + " left." : "") + "</div>" +
      '<div id="totp">' + (SEC.env ? "" : '<button class="b ' + (SEC.saved ? "secondary" : "primary") + '" id="totp-go">' + (SEC.saved ? "Move it to a new phone" : "Set up the authenticator") + "</button>") + "</div></div>") + req +
    card("state", '<span class="dot">' + ic("mail") + '</span><div style="flex:1"><b>Codes by email</b> ' + (SEC.email ? '<span class="pill b">' + esc(SEC.email) + "</span>" : '<span class="pill">Not set</span>') +
      '<div class="muted" style="margin:4px 0 12px">' + (SEC.mail ? "“Email me a code instead” at sign-in sends a code here: 6 digits, 10 minutes, one use, 3 an hour." : "Email codes can’t be sent: the server has no email sender (Resend) set up yet.") + "</div>" +
      (SEC.mail ? '<div id="mail"><button class="b secondary" id="mail-go">' + (SEC.email ? "Change the address" : "Add an address") + "</button></div>" : "") + "</div>") +
    (SEC.text ? card("state", '<span class="dot">' + ic("mail") + '</span><div style="flex:1"><b>Codes by text</b> ' + (SEC.phone ? '<span class="pill b">' + esc(SEC.phone) + "</span>" : '<span class="pill">Not set</span>') +
      '<div id="sms" style="margin-top:12px"><button class="b secondary" id="sms-go">' + (SEC.phone ? "Change the number" : "Add a number") + "</button></div></div>") : "") +
    card("state", '<span class="dot">' + ic("back") + '</span><div style="flex:1"><b>If you’re locked out</b><ol class="muted" style="padding-left:20px;margin:8px 0 0">' +
      "<li>Type one of your backup codes in the code box (each works once).</li>" + (SEC.mail && SEC.email ? "<li>Or tap “Email me a code instead”.</li>" : "") +
      "<li>Lost both? In Vercel → fig-promo → Settings → Environment Variables, add <b>ADMIN_TOTP_RESET</b> = today’s date (Production), redeploy, sign in with the password and set up your phone again. Then delete ADMIN_TOTP_RESET and redeploy. It only matters while “Require a code” is on; while it’s off the password alone signs you in.</li>" +
      "<li>If SESSION_SECRET is ever changed, the saved authenticator can’t be read: use the same reset.</li></ol></div>") +
    card("state", '<span class="dot">' + ic("out") + '</span><div style="flex:1"><b>Sign out everywhere</b><div class="muted" style="margin:4px 0 12px">Signs out every browser, this one too, and forgets every remembered device. Use it if a computer was lost or you think someone else signed in.</div>' +
    '<button class="b danger" id="out-all">Sign out everywhere</button></div>');
}
function securityWire() {
  $("#out-all") && ($("#out-all").onclick = async (e) => {
    if (!(await ask({ title: "Sign out everywhere?", body: "Every browser signs out, including this one.", ok: "Sign out everywhere", danger: true }))) return;
    await busy(e.currentTarget || $("#out-all"), async () => { const r = await api("logout-all"); if (r.error) return toast(r.error, true); location.reload(); });
  });
  // a new phone: the same steps as the first sign-in; nothing changes until the last one
  const go = $("#totp-go"); if (go) go.onclick = () => {
    const first = !SEC.saved && !SEC.env; // nothing set up yet: signed in is enough, so the current-code box is skipped
    $("#totp").innerHTML = (first ? "<div hidden>" : "<div>") + '<label for="cur-c"><b>First, a code from your current phone (or a backup code)</b></label><div class="ctl"><input class="f" id="cur-c" autocomplete="one-time-code" maxlength="12"><button class="b primary" id="cur-ok">Continue</button></div><p class="note">When the new phone is set up, every other browser signs out.</p></div>';
    $("#cur-ok").onclick = () => busy($("#cur-ok"), async () => {
    const box = $("#totp"), r = await api("enrol-start", { code: $("#cur-c").value }); if (!r.ok) return toast(r.error || (r.locked ? "Too many tries. Wait a few minutes." : "That didn't work."), true);
    box.innerHTML = '<ol class="muted" style="padding-left:20px;margin:0"><li>In your authenticator app on the new phone, add an account.</li><li>Scan this, or type the key below.</li></ol>' +
      '<div style="margin:16px 0;display:inline-block;padding:8px;background:#fff;border-radius:12px">' + r.qr + '</div><p>Key: <b class="mono">' + esc(r.secret) + "</b></p>" +
      '<label for="totp-c"><b>Then type the 6-digit code it shows</b></label><div class="ctl"><input class="f" id="totp-c" inputmode="numeric" autocomplete="one-time-code" maxlength="6"><button class="b primary" id="totp-ok">Check the code</button></div>' +
      '<p class="note">Your old phone keeps working until the last step. This times out in 15 minutes.</p>';
    $("#totp-ok").onclick = () => busy($("#totp-ok"), async () => {
      const c = await api("enrol-code", { code: $("#totp-c").value }); if (!c.ok) return toast(c.error || "That didn't work.", true);
      box.innerHTML = "<h2>New backup codes</h2><p>They replace the old ones. Each works once; they aren’t shown again.</p>" + '<p class="mono" style="font-size:16px;line-height:1.9">' + c.backup.map(esc).join("<br>") + "</p>" +
        '<label class="ctl"><input type="checkbox" id="kept"> I saved these codes somewhere safe</label><div class="ctl"><button class="b primary" id="totp-done" disabled>Switch to the new phone</button></div>';
      $("#kept").onchange = () => { $("#totp-done").disabled = !$("#kept").checked; };
      $("#totp-done").onclick = () => busy($("#totp-done"), async () => { const d = await api("enrol-done", { saved: $("#kept").checked }); if (!d.ok) return toast(d.error || "That didn't work.", true); toast("Your new phone is set up. Other browsers are signed out."); SEC = null; paint(); });
    });
    });
    if (first) $("#cur-ok").click();
  };
  // Require a code at every sign-in: on or off, always with a code (FIX-LIST #103 DESIGN)
  const rq = $("#req-go"); if (rq) rq.onclick = () => busy(rq, async () => {
    const on = !SEC.required;
    if (on && !(await ask({ title: "Require a code at every sign-in?", body: "From now on your password alone won’t sign you in: you’ll also need the authenticator, a backup code or an emailed code. Keep your backup codes somewhere safe.", ok: "Turn it on" }))) return;
    const r = await api("twostep-set", { on, code: $("#req-c").value });
    if (!r.ok) return toast(r.error || (r.locked ? "Too many tries. Wait a few minutes." : "That didn't work."), true);
    toast(on ? "A code is now required at every sign-in." : "The code is no longer required."); SEC = null; paint();
  });
  // the email (or phone) for codes: a code to the NEW address first; saved when it comes back
  for (const [id, box, via, kind, ph] of [["mail-go", "mail", "email", "email", "you@example.com"], ["sms-go", "sms", "text", "tel", "+1 647 555 0123"]]) {
    const b = $("#" + id); if (!b) continue;
    b.onclick = () => {
      $("#" + box).innerHTML = '<div class="ctl"><input class="f" id="' + box + '-to" type="' + kind + '" placeholder="' + ph + '"><button class="b primary" id="' + box + '-send">Send a code</button></div><div class="ctl" id="' + box + '-2" hidden><input class="f" id="' + box + '-c" inputmode="numeric" maxlength="6" placeholder="6 digits"><button class="b primary" id="' + box + '-ok">Confirm</button></div>';
      $("#" + box + "-send").onclick = () => busy($("#" + box + "-send"), async () => { const r = await api("enrol-contact", { via, to: $("#" + box + "-to").value }); if (!r.ok) return toast(r.error, true); $("#" + box + "-2").hidden = false; toast("A code is on its way to " + r.to + "."); });
      $("#" + box + "-ok").onclick = () => busy($("#" + box + "-ok"), async () => { const r = await api("enrol-contact-ok", { code: $("#" + box + "-c").value }); if (!r.ok) return toast(r.error, true); toast("Saved: codes go to " + r.to + "."); SEC = null; paint(); });
    };
  }
}

// ---- Ctrl/⌘K: jump to any page, restaurant, person on the list, post or message
function openPalette() {
  if ($(".palette")) return;
  const items = [].concat(
    Object.keys(TITLES).map((v) => ({ label: TITLES[v], kind: "Page", go: v })),
    (D && D.restaurants || []).map((r) => ({ label: r.name, kind: "Restaurant", go: "r:" + r.id })),
    ((BLOG || {}).posts || []).map((p) => ({ label: p.title, kind: "Post", go: "p:" + p.slug })),
    ((DIN || {}).waitlist || []).slice(0, 600).map((w, i) => ({ label: w.email, kind: "Waitlist", go: "w:" + i })),
    (D && D.support || []).map((m) => ({ label: m.email + " · " + m.topic, kind: "Message", go: "m:" + m.id })));
  const scrim = document.createElement("div"); scrim.className = "scrim top";
  const box = document.createElement("div"); box.className = "palette"; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-label", "Search");
  box.innerHTML = '<input id="pal-q" placeholder="Search restaurants, people, posts, messages…" aria-label="Search" autocomplete="off"><ul id="pal-list" role="listbox"></ul>';
  document.body.append(scrim, box);
  const L = layer(box, scrim);
  let sel = 0, shown = [];
  const draw = () => {
    const q = $("#pal-q", box).value.trim().toLowerCase();
    shown = items.filter((x) => !q || x.label.toLowerCase().includes(q)).slice(0, 30); sel = Math.min(sel, Math.max(0, shown.length - 1));
    $("#pal-list", box).innerHTML = shown.length ? shown.map((x, i) => '<li><button role="option" data-i="' + i + '" aria-selected="' + (i === sel) + '">' + esc(x.label) + '<span class="kind">' + x.kind + "</span></button></li>").join("") : '<li class="empty">Nothing matches.</li>';
    $$("[data-i]", box).forEach((b) => b.onclick = () => { L.close(); go(shown[+b.dataset.i].go); });
  };
  const input = $("#pal-q", box);
  input.oninput = () => { sel = 0; draw(); };
  input.onkeydown = (e) => {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = Math.max(0, Math.min(shown.length - 1, sel + (e.key === "ArrowDown" ? 1 : -1))); draw(); const on = $("[aria-selected='true']", box); if (on) on.scrollIntoView({ block: "nearest" }); }
    if (e.key === "Enter" && shown[sel]) { e.preventDefault(); L.close(); go(shown[sel].go); }
  };
  draw();
}

// ---- moving around: views, tabs, panels; one place wires every action button
function go(target) {
  const [k, v] = [target.slice(0, target.indexOf(":") > -1 ? target.indexOf(":") : target.length), target.indexOf(":") > -1 ? target.slice(target.indexOf(":") + 1) : ""];
  if (k === "r") return openRestaurant(v);
  if (k === "w") return openPerson(+v);
  if (k === "p") return openPost(v);
  if (k === "m") { closePanels(); view = "inbox"; SUB.inbox = "all"; SEL = "m" + v; render(); return; }
  closePanels(); view = k; if (v) SUB[k] = v; render(); scrollTo(0, 0);
}
function badge(v, n) { const el = $("#n-" + v); if (el) { el.textContent = n == null ? "–" : n; el.hidden = n == null; } }
function wireActions(root) {
  $$("[data-go]", root).forEach((b) => b.onclick = () => go(b.dataset.go));
  $$("tr[data-open]", root).forEach((tr) => {
    tr.onclick = (e) => { if (!e.target.closest("button, a, input, select")) go(tr.dataset.open); };
    // keyboard and screen readers: a button (Enter and Space, "Open <name>"), not a focusable row (FIX-LIST #165)
    const b = document.createElement("button"); b.className = "sr row-open"; b.type = "button";
    const c0 = tr.cells[0], named = c0 && (c0.querySelector("b") || c0); // the name, not a thumbnail's letter
    b.textContent = "Open " + ((named && named.innerText.split("\n").map((t) => t.trim()).find((t) => t.length > 1)) || "details");
    b.onclick = (e) => { e.stopPropagation(); go(tr.dataset.open); };
    if (tr.cells[0]) tr.cells[0].prepend(b);
  });
  $$("[data-filter]", root).forEach((inp) => inp.oninput = () => {
    const t = inp.closest(".tools").nextElementSibling, q = inp.value.trim().toLowerCase();
    // the row's own words, not its hidden "Open ..." button (#166: "open" matched every row)
    if (t) $$("tbody tr", t).forEach((tr) => { const own = tr.textContent.replace((tr.querySelector(".row-open") || {}).textContent || "", ""); tr.hidden = !!q && !own.toLowerCase().includes(q); });
  });
  if (!D || !D.connected) return;
  $$("[data-2fa],[data-2fa-email]", root).forEach((b) => b.onclick = async () => {
    if (!(await ask({ title: "Turn off two-step login?", body: "Only after checking it is really them: they write from the account’s email and know the phone number on it. They then sign in with their password alone, and can switch two-step login back on.", ok: "Turn it off", danger: true }))) return;
    await busy(b, async () => {
      const r = await api("two-step-off", b.dataset["2fa"] ? { id: b.dataset["2fa"] } : { email: b.dataset["2faEmail"] });
      if (r.error) return toast(r.error, true);
      toast(r.found === false ? "No FIG account has that email." : r.removed ? r.removed + " authenticator(s) removed. They can sign in with the password now." : "That account had no two-step login to remove.");
    });
  });
  $$("[data-sup-remove]", root).forEach((b) => b.onclick = async () => {
    if (!(await ask({ title: "Delete this message?", body: "It’s deleted for good. Do it when they asked to be forgotten, or it’s spam.", ok: "Delete", danger: true }))) return;
    await busy(b, async () => { const r = await api("support-remove", { id: b.dataset.supRemove }); if (r.error) return toast(r.error, true); toast("Message deleted."); SEL = null; await load(); paint(); });
  });
  $$("[data-sup]", root).forEach((b) => b.onclick = () => busy(b, async () => {
    const r = await api("support", { id: b.dataset.sup, status: b.dataset.to });
    if (r.error) return toast(r.error, true);
    toast(b.dataset.to === "answered" ? "Marked answered." : "Opened again."); await load(); paint();
  }));
}
// the top bar: the range (on the Overview), when it last loaded, refresh and search
function topBar() {
  $("#title").textContent = TITLES[view];
  $("#sub").textContent = view === "overview" ? days + " days to January 1, 2027" : "";
  document.title = TITLES[view] + " · FIG Admin";
  $("#actions").innerHTML = (view === "overview" ? '<div class="seg" role="group" aria-label="Range">' + [7, 30, 90].map((n) => '<button data-range="' + n + '"' + (RANGE === n ? ' class="on" aria-pressed="true"' : ' aria-pressed="false"') + ">" + n + " days</button>").join("") + "</div>" : "") +
    '<span class="upd" id="upd"></span><button class="b icon secondary" id="refresh" aria-label="Refresh">' + ic("refresh", 18) + '</button><button class="b secondary" id="find">' + ic("search", 18) + '<span class="label">Search</span><span class="kbd">Ctrl K</span></button>';
  $$("[data-range]").forEach((b) => b.onclick = () => { RANGE = +b.dataset.range; render(); });
  $("#refresh").onclick = () => busy($("#refresh"), async () => { CH = null; await load(); render(); toast("Up to date."); });
  $("#find").onclick = openPalette;
  tick();
}
function tick() { const u = $("#upd"); if (u && UPDATED) u.textContent = "Updated " + ago(new Date(UPDATED).toISOString()); }
setInterval(tick, 30000);
// redraw the current view in place (after data arrives)
function paint() {
  CHARTS = []; $("#main").classList.add("still"); // a repaint (data arriving) doesn't replay the rise
  $("#main").innerHTML = VIEWS[view]();
  wireAll();
}
function wireAll() {
  $$("[data-sub]").forEach((b) => b.onclick = () => { const [v, k] = b.dataset.sub.split(":"); SUB[v] = k; if (v === "inbox") SEL = null; render(); });
  wireActions(document);
  if (view === "security") securityWire();
  if (view === "waitlist") dinersWire();
  if (view === "paid") paidWire();
  if (view === "waitlist" || view === "overview") sourcesWire();
  $$("[data-gr]").forEach((b) => b.onclick = () => { GR = +b.dataset.gr; paint(); });
  if (view === "blog") blogWire(document);
  if (view === "calendar") calendarWire();
  if (view === "inbox") { const q = $("#ib-q"); if (q) q.oninput = inboxRows; inboxRows(); inboxThread(); }
  drawCharts();
}
function render() {
  $$("#nav button, #tabbar button[data-v], #sec, #sheet button[data-v]").forEach((b) => { b.classList.toggle("on", b.dataset.v === view); if (b.dataset.v === view) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current"); });
  $("#sheet").hidden = true; $("#more-btn").setAttribute("aria-expanded", "false");
  topBar();
  rise = 0; CHARTS = []; $("#main").classList.remove("still");
  $("#main").innerHTML = VIEWS[view]();
  wireAll();
  if (!D.connected) return;
  if ((view === "blog" || view === "overview" || view === "calendar") && !BLOG) blogLoad();
  if ((view === "waitlist" || view === "overview" || view === "calendar") && !DIN) dinersLoad();
  if ((view === "overview" || view === "calendar") && !CH) chartsLoad();
  if ((view === "overview" || view === "waitlist") && !SRC) sourcesLoad();
  if (view === "restaurants" && SUB.restaurants === "outreach") prosLoad();
  if (view === "paid" && !PS) paidLoad();
}
async function chartsLoad() {
  CH = await api("charts").catch(() => null);
  if (CH && CH.error) CH = null;
  if (view === "overview" || view === "calendar") paint();
}
async function load() {
  D = await api("data"); UPDATED = Date.now(); tick();
  // the reset flag left on after it was used: say so on every page until it's deleted in Vercel (Agent #4, #103)
  if (D.resetLeftOn && !$("#reset-line")) $("#main").insertAdjacentHTML("beforebegin", '<div id="reset-line" class="hint r" role="alert" style="margin:12px 16px 0"><b>ADMIN_TOTP_RESET is still set in Vercel.</b> Delete it (Settings → Environment Variables) and redeploy. Each value works once, but don’t leave it there.</div>');
  if (D.connected) {
    badge("restaurants", D.counts.restaurants);
    const open = (D.counts.support || 0) + (D.counts.reports || 0);
    badge("inbox", open || null); const nb = $("#n-inbox"); if (nb) nb.classList.add("hot");
    const tb = $("#t-inbox"); if (tb) { tb.textContent = open; tb.hidden = !open; }
  }
}
// keys: Esc closes the top dialog or panel; Ctrl/⌘K searches; in the inbox j / k / e. Never while typing in a field
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && LAYERS.length) { e.preventDefault(); LAYERS[LAYERS.length - 1].close(); return; }
  if (e.target.closest && e.target.closest("input, textarea, select, [contenteditable]")) return;
  if ((e.metaKey || e.ctrlKey) && !e.altKey && e.key.toLowerCase() === "k") { e.preventDefault(); if (D) openPalette(); return; }
  if (e.metaKey || e.ctrlKey || e.altKey || LAYERS.length || view !== "inbox") return;
  if (e.key === "j") inboxMove(1); else if (e.key === "k") inboxMove(-1); else if (e.key === "e") inboxToggle();
});
$$("#nav button, #tabbar button[data-v], #sec, #sheet button[data-v]").forEach((b) => b.onclick = () => { view = b.dataset.v; if (view === "inbox") SEL = null; if (D) render(); });
$("#more-btn").onclick = () => { const s = $("#sheet"); s.hidden = !s.hidden; $("#more-btn").setAttribute("aria-expanded", String(!s.hidden)); };
const out = async (e) => { await busy(e.currentTarget, () => api("logout")); location.reload(); };
$("#out").onclick = out; $("#out2").onclick = out;
$("#main").innerHTML = '<div class="grid">' + '<div class="sk skcard"></div>'.repeat(4) + '</div><div style="height:16px"></div>' + skeleton(8);
load().then(() => { render(); if (D.connected) { if (!DIN) dinersLoad(); if (!BLOG) blogLoad(); } }).catch(() => { $("#main").innerHTML = emptyState("Couldn’t load", "Check your connection, then refresh."); });
`.replace("__ICONS__", JSON.stringify(ICON));

module.exports = { signInPage, appPage };
