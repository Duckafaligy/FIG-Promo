// FIG Ads Manager (/ads): restaurants run their ads here, signed in with their FIG account (user 2026-10-07: "run their
// ads/promotion via our website where they can also get a broader and better picture ... dynamic, like how facebook ads
// run"). Pay per tap from an auction, within a daily budget; the FIG team invoices monthly. Everything goes through FIG's
// database as the signed-in person (row security and the ads functions decide what they see and change): see
// app/supabase/migrations/20261007130000_ads.sql.
(() => {
  const cfg = window.FIG_ADS || {};
  const app = document.getElementById("app");
  if (!cfg.url || !window.supabase) { app.innerHTML = '<p class="boot">The Ads Manager can’t load right now. Try again in a minute.</p>'; return; }
  const db = window.supabase.createClient(cfg.url, cfg.key, { auth: { persistSession: true, storageKey: "fig-ads" } });

  // ------------------------------------------------------------------ small helpers
  const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const money = (n) => "$" + Number(n || 0).toFixed(2);
  const int = (n) => Math.round(Number(n || 0)).toLocaleString("en-CA");
  const pct = (a, b) => (b ? ((a / b) * 100).toFixed(1) : "0.0") + "%";
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const today = () => new Date().toLocaleDateString("en-CA");
  const day = (iso) => new Date(iso + (iso.length === 10 ? "T12:00:00" : "")).toLocaleDateString("en-CA", { month: "short", day: "numeric" });
  const hourName = (h) => (h % 12 || 12) + (h < 12 ? " am" : " pm");
  const store = { get: (k) => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* private mode */ } } };
  const P = (d) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const I = {
    home: P('<path d="M3 11 12 4l9 7v9h-6v-6H9v6H3z"/>'), list: P('<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'),
    plus: P('<path d="M12 5v14M5 12h14"/>'), chart: P('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'), card: P('<path d="M3 6h18v12H3zM3 10h18"/>'),
    out: P('<path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h10"/>'), bulb: P('<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>'),
    users: P('<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21c1-4 4-6 7-6s6 2 7 6M17 11a3 3 0 1 0 0-6M22 19c-.6-2.6-2.2-4-4-4.5"/>'),
    tag: P('<path d="M3 12V4h8l10 10-8 8zM7.5 8.5h.01"/>'), clock: P('<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2"/>'),
    warn: P('<path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>'),
  };
  const LOGO = '<svg viewBox="743 716 100 100" aria-hidden="true"><path fill="#1E5EFF" d="M765.637 809.875C755.252 806.459 749.184 797.508 749.184 785.965V751.1C749.184 735.317 761.319 722.714 776.955 722.714H836.699L831.098 730.252C827.014 735.906 822.346 738.968 814.762 738.968H777.189C770.888 738.968 765.754 744.15 765.754 750.629V755.341L767.621 753.574C770.304 751.218 772.989 750.158 776.722 750.158H800.06L790.725 762.526C788.275 765.941 785.24 767.354 780.923 767.354H772.405C768.671 767.354 765.637 770.299 765.637 774.304V809.875Z"/><path fill="#1E5EFF" d="M793.759 769.592H836.699V784.08C836.699 799.746 824.563 811.171 809.044 811.171H770.888V795.387H809.161C815.462 795.387 820.013 790.794 820.013 784.433V783.256H781.623L793.759 769.592Z"/><path fill="#14C86B" d="M797.142 765.705L805.194 755.104C807.877 751.689 811.145 750.158 815.696 750.158H836.699V754.28C836.699 761.347 832.265 765.705 825.264 765.705H797.142Z"/></svg>';
  const toast = (msg) => { const t = document.createElement("div"); t.className = "toast"; t.textContent = msg; document.body.appendChild(t); setTimeout(() => t.remove(), 2600); };
  const ok = ({ data, error }) => { if (error) throw new Error(error.message); return data; };

  const GOALS = {
    visits: ["More diners", "Show your restaurant to diners nearby while they decide where to eat.", I.users],
    deal: ["Promote a deal", "Put one of your deals first in Deals near you and in search.", I.tag],
    quiet: ["Fill quiet hours", "Run only during the hours you want busier, like weekday afternoons.", I.clock],
  };
  const PLACES = { home: "Featured on Home", deals: "Deals near you", search: "Search results", map: "The map" };
  const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // ------------------------------------------------------------------ state
  const S = { session: null, rests: [], rid: null, campaigns: [], stats: new Map(), account: null, invoices: [], deals: [], insights: null, draft: null, step: 1 };
  const rest = () => S.rests.find((r) => r.id === S.rid);

  // ------------------------------------------------------------------ sign in
  function signInView(problem = "") {
    app.innerHTML = `<div class="signin">
      <div class="side"><div class="brand" style="color:#fff">${LOGO.replace('fill="#1E5EFF"', 'fill="#fff"').replace('fill="#1E5EFF"', 'fill="#fff"')}FIG Ads Manager</div>
        <div style="display:grid;gap:22px"><h1>Get seen by diners nearby, right when they decide.</h1>
        <ul><li>Pay only when a diner taps your ad</li><li>Set a daily budget, stop anytime</li><li>Target by distance, hours and food</li><li>See who came in, not just clicks</li></ul></div>
        <p style="opacity:.85">Everything else on FIG is free for restaurants.</p></div>
      <form id="si" novalidate>
        <h2>Sign in</h2><p class="muted">Use the email and password of your FIG restaurant account.</p>
        <div><label class="l" for="em">Email</label><input class="f" id="em" type="email" autocomplete="username" required></div>
        <div><label class="l" for="pw">Password</label><input class="f" id="pw" type="password" autocomplete="current-password" required></div>
        ${problem ? `<p class="err">${esc(problem)}</p>` : ""}
        <button class="btn" type="submit">Sign in</button>
        <p class="muted small">No restaurant account yet? Download FIG and choose “I own a restaurant”. It’s free.</p>
      </form></div>`;
    document.getElementById("si").onsubmit = async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button"); btn.disabled = true; btn.textContent = "Signing in…";
      const { error } = await db.auth.signInWithPassword({ email: document.getElementById("em").value.trim(), password: document.getElementById("pw").value });
      if (error) return signInView(/invalid/i.test(error.message) ? "That email and password don’t match a FIG account." : "Couldn’t sign in. Check your connection and try again.");
      start();
    };
  }

  // ------------------------------------------------------------------ data
  async function loadRests() {
    const uid = S.session.user.id;
    const [own, staff] = await Promise.all([
      db.from("restaurants").select("id,name,city,photos,lat,lng,tags,cuisine,status,owner_id").eq("owner_id", uid).then(ok),
      db.from("staff").select("restaurant_id").eq("user_id", uid).eq("status", "active").eq("role", "Manager").then(ok),
    ]);
    const extra = staff.map((x) => x.restaurant_id).filter((id) => !own.some((r) => r.id === id));
    const managed = extra.length ? await db.from("restaurants").select("id,name,city,photos,lat,lng,tags,cuisine,status,owner_id").in("id", extra).then(ok) : [];
    S.rests = [...own, ...managed];
    S.rid = S.rests.some((r) => r.id === store.get("fig-ads-rest")) ? store.get("fig-ads-rest") : S.rests[0]?.id ?? null;
  }
  async function loadRest(radius = 3) {
    const rid = S.rid;
    const [campaigns, stats, accounts, invoices, deals, insights] = await Promise.all([
      db.from("campaigns").select("*").eq("restaurant_id", rid).order("created_at", { ascending: false }).then(ok),
      db.rpc("campaign_stats", { p_restaurant: rid }).then(ok),
      db.from("ad_accounts").select("*").then(ok),
      db.from("ad_invoices").select("*").order("month", { ascending: false }).then(ok),
      db.from("deals").select("id,title,photo,status,kind,flash").eq("restaurant_id", rid).neq("status", "ended").then(ok),
      db.rpc("ad_insights", { p_restaurant: rid, p_radius: radius }).then(ok),
    ]);
    const owner = rest()?.owner_id;
    Object.assign(S, { campaigns, stats: new Map(stats.map((x) => [x.campaign_id, x])), account: accounts.find((a) => a.owner_id === owner) || null,
      invoices: invoices.filter((x) => x.owner_id === owner), deals, insights, radius });
  }
  const st = (c) => S.stats.get(c.id) || { views: 0, taps: 0, spend: 0, spend_today: 0, spend_month: 0, diners: 0 };

  // ------------------------------------------------------------------ the bigger picture: forecasts and tips
  // what a campaign could do a day (ranges: these sharpen as FIG learns the area)
  function forecast(d) {
    const ins = S.insights || {};
    const ctr = Number(ins.ctr) || 0.03;
    const floor = Number(ins.floor) || 0.3;
    const cpc = d.bid ? clamp(Math.max(floor, Number(ins.cpc) || floor) * 1.1, floor, d.bid) : Math.max(floor, Number(ins.cpc) || floor);
    const cravers = d.foods.length ? (ins.cravings || []).filter((c) => d.foods.map((f) => f.toLowerCase()).includes(String(c.food).toLowerCase())).reduce((a, c) => a + c.n, 0) : null;
    const foodShare = cravers === null ? 1 : clamp(cravers / Math.max(1, ins.diners_all || 1), 0.12, 1);
    const hours = d.from === d.to ? 14 : (((+d.to.slice(0, 2) * 60 + +d.to.slice(3)) - (+d.from.slice(0, 2) * 60 + +d.from.slice(3)) + 1440) % 1440) / 60;
    const hourShare = clamp(hours / 14, 0.15, 1);
    const areaShare = clamp(Math.pow(d.radius / 8, 2), 0.08, 1);
    const base = Math.max(Number(ins.views_day) || 0, (ins.diners_area || 0) * 0.9, 60);
    const views = base * areaShare * foodShare * hourShare * (d.audience === "all" ? 1 : 0.6);
    const taps = Math.min(views * ctr, d.budget / cpc);
    const diners = taps * 0.12;
    const spend = taps * cpc;
    const best = views * ctr * cpc; // what it takes to get every tap available
    return { views, taps, diners, spend, cpc, best, perDiner: diners ? spend / diners : 0, monthMax: d.budget * 30.4 * (d.days.length / 7) };
  }
  const range = (n, f = int) => (n < 1 ? (n > 0.05 ? `${f(0)}–${f(1)}` : f(0)) : `${f(n * 0.6)}–${f(n * 1.4)}`);

  function tips() {
    const ins = S.insights; const out = [];
    if (!ins) return out;
    const peak = (rows) => { if (!rows?.length) return null; let best = null; for (let h = 0; h < 24; h++) { const n = [h, h + 1, h + 2].reduce((a, x) => a + (rows.find((r) => r.h === x % 24)?.n || 0), 0); if (!best || n > best.n) best = { h, n }; } return best.n ? best : null; };
    const area = peak(ins.claim_hours), mine = peak(ins.my_hours);
    if (area) out.push(["bulb", `Diners near you claim the most deals around ${hourName(area.h)} to ${hourName((area.h + 3) % 24)}.${mine && Math.abs(mine.h - area.h) >= 3 ? ` Your own scans peak around ${hourName(mine.h)}, so an ad in their peak can fill hours you don’t.` : " Target those hours to be seen when people decide."}`]);
    const top = (ins.cravings || [])[0];
    if (top) out.push(["users", `“${esc(top.food)}” is what diners on FIG crave most${(rest()?.tags || []).some((t) => t.toLowerCase() === String(top.food).toLowerCase()) ? ", and you serve it: target cravers of " + esc(top.food) + "." : "."}`]);
    out.push(["chart", ins.nearby_ads ? `${ins.nearby_ads} other ${ins.nearby_ads === 1 ? "restaurant runs" : "restaurants run"} ads within ${S.radius} km. A max bid around ${money(Math.max(ins.floor, ins.cpc) * 1.5)} a tap keeps you competitive.` : `Nobody within ${S.radius} km is advertising right now, so taps cost about the minimum (${money(ins.floor)}).`]);
    for (const c of S.campaigns.filter((x) => x.status === "active")) {
      const s = st(c);
      if (s.views >= 300 && s.taps / s.views < 0.02) out.push(["warn", `“${esc(c.name)}” is seen but rarely tapped (${pct(s.taps, s.views)}). Try a brighter food photo or a clearer deal in the headline.`]);
      if (Number(s.spend_today) >= Number(c.daily_budget) * 0.98 && new Date().getHours() < 17) out.push(["warn", `“${esc(c.name)}” used its whole budget before dinner today. Raise it to stay visible in the evening.`]);
    }
    if (!S.campaigns.length) out.push(["bulb", "New to ads? Start with $10 a day for a week, then keep what brings diners in."]);
    return out;
  }
  const tipHtml = (list) => list.map(([ic, txt]) => `<div class="tip ${ic === "warn" ? "warn" : ""}">${I[ic]}<div>${txt}</div></div>`).join("");

  // ------------------------------------------------------------------ the restaurant switcher (photo, name, city and status;
  // a menu of the owner's restaurants when there's more than one)
  const CHEV = P('<path d="m6 9 6 6 6-6"/>'), CHECK = P('<path d="m5 12 5 5 9-10"/>');
  const thumb = (x) => `<span class="pr-photo">${x.photos?.[0] ? `<img src="${esc(x.photos[0])}" alt="">` : esc((x.name || "?").trim()[0].toUpperCase())}</span>`;
  const line = (x) => `<span class="pr-line"><i class="dot ${x.status === "approved" ? "" : "wait"}"></i>${x.status === "approved" ? "Live" : "Setting up"}${x.city ? " · " + esc(x.city) : ""}</span>`;
  function switcher(r) {
    if (!r) return "";
    const many = S.rests.length > 1;
    const face = `${thumb(r)}<span class="pr-text"><b>${esc(r.name)}</b>${line(r)}</span>`;
    if (!many) return `<div class="place"><div class="pick-rest single" aria-label="${esc(r.name)}">${face}</div></div>`;
    return `<div class="place"><button class="pick-rest" id="rs" type="button" aria-haspopup="listbox" aria-expanded="false" aria-controls="rs-menu" aria-label="${esc(r.name)}. Switch restaurant">${face}<span class="pr-chev">${CHEV}</span></button>
      <div class="pr-menu" id="rs-menu" role="listbox" aria-label="Your restaurants" hidden><p class="pr-head">Your restaurants</p>
        ${S.rests.map((x) => `<button class="pr-opt" type="button" role="option" aria-selected="${x.id === S.rid}" data-rid="${x.id}">${thumb(x)}<span class="pr-text"><b>${esc(x.name)}</b>${line(x)}</span><span class="pr-check">${CHECK}</span></button>`).join("")}
        <p class="pr-foot">Add a location in the FIG app.</p></div></div>`;
  }
  function wireSwitcher() {
    const btn = document.getElementById("rs"), menu = document.getElementById("rs-menu");
    if (!btn) return;
    const opts = () => [...menu.querySelectorAll(".pr-opt")];
    const close = (focus) => { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); document.removeEventListener("pointerdown", outside); if (focus) btn.focus(); };
    const outside = (e) => { if (!menu.contains(e.target) && !btn.contains(e.target)) close(false); };
    const open = () => { menu.hidden = false; btn.setAttribute("aria-expanded", "true"); document.addEventListener("pointerdown", outside); (opts().find((o) => o.getAttribute("aria-selected") === "true") || opts()[0]).focus(); };
    btn.onclick = () => (menu.hidden ? open() : close(true));
    btn.onkeydown = (e) => { if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); open(); } };
    menu.onkeydown = (e) => {
      const list = opts(), i = list.indexOf(document.activeElement);
      if (e.key === "Escape") { e.preventDefault(); close(true); }
      else if (e.key === "ArrowDown") { e.preventDefault(); list[(i + 1) % list.length].focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); list[(i - 1 + list.length) % list.length].focus(); }
      else if (e.key === "Tab") close(false);
    };
    opts().forEach((o) => (o.onclick = async () => {
      close(true);
      if (o.dataset.rid === S.rid) return;
      S.rid = o.dataset.rid; store.set("fig-ads-rest", S.rid);
      btn.classList.add("busy");
      await loadRest(); route();
    }));
  }

  // ------------------------------------------------------------------ the shell
  const NAV =[["overview", "Overview", I.home], ["campaigns", "Ads", I.list], ["create", "Create an ad", I.plus], ["insights", "Insights", I.chart], ["billing", "Billing", I.card]];
  function shell(view, inner) {
    const r = rest();
    app.innerHTML = `<div class="shell"><aside>
      <div class="brand">${LOGO}FIG Ads</div>
      ${switcher(r)}
      <nav class="side">${NAV.map(([v, label, ic]) => `<button data-go="${v}" class="${view === v || (view === "detail" && v === "campaigns") ? "on" : ""}">${ic}${label}</button>`).join("")}</nav>
      <div class="foot"><span>${esc(S.session.user.email)}</span><button class="link" id="so" style="justify-self:start">Sign out</button></div>
    </aside><main>${r && r.status !== "approved" ? `<div class="tip warn" style="margin-bottom:20px">${I.warn}<div>${esc(r.name)} isn’t live on FIG yet. Finish setup in the app so your ads can show.</div></div>` : ""}${S.account?.status === "held" ? `<div class="tip warn" style="margin-bottom:20px">${I.warn}<div>Your ads are on hold. The FIG team will contact you about your account.</div></div>` : ""}${inner}</main></div>`;
    document.querySelectorAll("[data-go]").forEach((b) => (b.onclick = () => go(b.dataset.go)));
    wireSwitcher();
    document.getElementById("so").onclick = async () => { await db.auth.signOut(); location.hash = ""; signInView(); };
  }
  const go = (v) => { location.hash = v; };

  // ------------------------------------------------------------------ overview
  function overview() {
    const live = S.campaigns.filter((c) => c.status === "active");
    const sum = (k) => S.campaigns.reduce((a, c) => a + Number(st(c)[k] || 0), 0);
    const spend = sum("spend"), diners = sum("diners");
    shell("overview", `<div class="head"><div><h1>${esc(rest()?.name || "Your ads")}</h1><p>${live.length ? `${live.length} ${live.length === 1 ? "ad" : "ads"} running` : "No ads running"} · pay per tap, invoiced monthly</p></div>
      <button class="btn" data-go2="create">${I.plus}Create an ad</button></div>
      <div class="grid g4" style="margin-bottom:24px">
        <div class="stat"><span>Spent this month</span><b>${money(sum("spend_month"))}</b>${S.account ? `<em style="color:var(--slate)">of ${money(S.account.monthly_limit)} limit</em>` : ""}</div>
        <div class="stat"><span>Views</span><b>${int(sum("views"))}</b></div>
        <div class="stat"><span>Taps</span><b>${int(sum("taps"))}</b><em>${pct(sum("taps"), sum("views"))} tap rate</em></div>
        <div class="stat"><span>Diners who came in</span><b>${int(diners)}</b><em>${diners ? money(spend / diners) + " each" : "tapped, then scanned in"}</em></div>
      </div>
      <div class="grid g2">
        <div class="card"><h2>Running now</h2>${live.length ? `<div style="margin-top:12px">${live.map((c) => { const s = st(c); return `<div style="padding:12px 0;border-top:1px solid var(--hair);cursor:pointer" data-open="${c.id}"><div style="display:flex;justify-content:space-between;gap:8px"><h3>${esc(c.name)}</h3><span class="tag live">Running</span></div>
          <p class="muted small" style="margin:4px 0 8px">${money(s.spend_today)} of ${money(c.daily_budget)} today · ${int(s.taps)} taps · ${int(s.diners)} diners</p><div class="bar"><i style="width:${clamp((s.spend_today / c.daily_budget) * 100, 2, 100)}%"></i></div></div>`; }).join("")}</div>`
          : `<p class="muted" style="margin:8px 0 16px">Ads put you first when diners nearby are choosing where to eat. You only pay when someone taps.</p><button class="btn sm" data-go2="create">Create your first ad</button>`}</div>
        <div class="card"><h2>What to do next</h2><div class="grid" style="margin-top:12px">${tipHtml(tips()) || '<p class="muted">Tips appear here as FIG learns your area.</p>'}</div></div>
      </div>`);
    wire();
  }

  // ------------------------------------------------------------------ the list
  function campaignsView() {
    const rows = S.campaigns.map((c) => { const s = st(c); const tagc = c.status === "active" ? "live" : c.status === "stopped" ? "stop" : "";
      return `<tr class="row" data-open="${c.id}"><td><b>${esc(c.name)}</b><div class="muted small">${GOALS[c.goal][0]}</div></td>
        <td><span class="tag ${tagc}">${c.status === "active" ? "Running" : c.status === "stopped" ? "Stopped by FIG" : c.status[0].toUpperCase() + c.status.slice(1)}</span></td>
        <td>${money(c.daily_budget)}/day</td><td>${money(s.spend_today)}</td><td>${int(s.views)}</td><td>${int(s.taps)} <span class="muted small">${pct(s.taps, s.views)}</span></td>
        <td>${int(s.diners)}</td><td>${s.diners ? money(s.spend / s.diners) : "—"}</td><td>${money(s.spend)}</td>
        <td>${c.status === "active" || c.status === "paused" ? `<button class="switch ${c.status === "active" ? "on" : ""}" data-toggle="${c.id}" aria-label="${c.status === "active" ? "Pause" : "Resume"} ${esc(c.name)}"></button>` : ""}</td></tr>`; }).join("");
    shell("campaigns", `<div class="head"><div><h1>Ads</h1><p>Every ad for ${esc(rest()?.name || "")}, newest first.</p></div><button class="btn" data-go2="create">${I.plus}Create an ad</button></div>
      ${S.campaigns.length ? `<div class="tblwrap"><table class="tbl"><tr><th>Ad</th><th>Status</th><th>Budget</th><th>Spent today</th><th>Views</th><th>Taps</th><th>Diners</th><th>Per diner</th><th>Spent</th><th></th></tr>${rows}</table></div>`
        : `<div class="empty"><h3>No ads yet</h3><p>Pick a goal, a budget and who should see it. It takes about two minutes.</p><p style="margin-top:16px"><button class="btn" data-go2="create">Create an ad</button></p></div>`}`);
    wire();
  }

  // ------------------------------------------------------------------ one ad: results and settings
  async function detail(id) {
    const c = S.campaigns.find((x) => x.id === id);
    if (!c) return go("campaigns");
    const [daily, creatives] = await Promise.all([db.rpc("campaign_daily", { p_campaign: id, p_days: 14 }).then(ok), db.rpc("campaign_creatives", { p_campaign: id }).then(ok)]);
    const s = st(c);
    const max = Math.max(1, ...daily.map((d) => d.taps));
    const W = 700, H = 160, bw = W / daily.length;
    const chart = `<svg class="chart" viewBox="0 0 ${W} ${H + 22}" preserveAspectRatio="none" role="img" aria-label="Taps and diners by day">${daily.map((d, i) => {
      const th = (d.taps / max) * H, dh = (d.diners / max) * H;
      return `<g><title>${day(d.day)}: ${d.views} views, ${d.taps} taps, ${d.diners} diners, ${money(d.spend)}</title><rect x="${i * bw + bw * 0.18}" y="${H - th}" width="${bw * 0.4}" height="${Math.max(th, 1)}" rx="3" fill="#1E5EFF"/><rect x="${i * bw + bw * 0.6}" y="${H - dh}" width="${bw * 0.22}" height="${Math.max(dh, 1)}" rx="3" fill="#14C86B"/>
        ${i % 2 === 0 ? `<text x="${i * bw + bw / 2}" y="${H + 16}" font-size="11" text-anchor="middle" fill="#5C6470">${day(d.day)}</text>` : ""}</g>`; }).join("")}</svg>`;
    const crs = (c.creatives || []).length ? c.creatives : [{ photo: "", headline: "" }];
    const bestI = creatives.reduce((b, x) => ((x.taps + 1) / (x.views + 20) > (b ? (b.taps + 1) / (b.views + 20) : -1) ? x : b), null)?.creative;
    const editable = c.status !== "stopped";
    shell("detail", `<div class="head"><div><button class="link" data-go2="campaigns">← All ads</button><h1 style="margin-top:8px">${esc(c.name)}</h1>
      <p>${GOALS[c.goal][0]} · ${money(c.daily_budget)} a day · ${c.bid ? "max " + money(c.bid) + " a tap" : "automatic bid"} · from ${day(c.starts_on)}${c.ends_on ? " to " + day(c.ends_on) : ""}</p></div>
      ${c.status === "active" || c.status === "paused" ? `<button class="btn ${c.status === "active" ? "grey" : ""}" data-toggle="${c.id}">${c.status === "active" ? "Pause ad" : "Resume ad"}</button>` : `<span class="tag ${c.status === "stopped" ? "stop" : ""}">${c.status === "stopped" ? "Stopped by FIG" : "Ended"}</span>`}</div>
      ${c.status === "stopped" && c.note ? `<div class="tip warn" style="margin-bottom:20px">${I.warn}<div>The FIG team stopped this ad: ${esc(c.note)}</div></div>` : ""}
      <div class="grid g4" style="margin-bottom:20px">
        <div class="stat"><span>Spent today</span><b>${money(s.spend_today)}</b><em style="color:var(--slate)">of ${money(c.daily_budget)}</em></div>
        <div class="stat"><span>Views · taps</span><b>${int(s.views)} · ${int(s.taps)}</b><em>${pct(s.taps, s.views)} tap rate</em></div>
        <div class="stat"><span>Diners who came in</span><b>${int(s.diners)}</b><em>within 7 days of tapping</em></div>
        <div class="stat"><span>Spent in all</span><b>${money(s.spend)}</b><em>${s.diners ? money(s.spend / s.diners) + " per diner" : s.taps ? money(s.spend / s.taps) + " per tap" : ""}</em></div>
      </div>
      <div class="grid g2">
        <div class="card"><h2>Last 14 days</h2>${chart}<div class="legend"><span><i style="background:#1E5EFF"></i>Taps</span><span><i style="background:#14C86B"></i>Diners who came in</span><span>Hover a day for views and spend</span></div></div>
        <div class="card"><h2>Photos</h2><p class="muted small">FIG shows the one diners tap most, and keeps giving the others a fair try.</p><div style="margin-top:12px">${crs.map((x, i) => {
          const r = creatives.find((y) => y.creative === i) || { views: 0, taps: 0 };
          return `<div class="creative"><img src="${esc(x.photo || rest()?.photos?.[0] || "")}" alt=""><div><b style="font:700 15px var(--d)">${esc(x.headline || c.name)}</b><div class="muted small">${int(r.views)} views · ${int(r.taps)} taps · ${pct(r.taps, r.views)}</div></div>${bestI === i && crs.length > 1 && r.views ? '<span class="tag live">Winning</span>' : ""}</div>`; }).join("")}</div></div>
      </div>
      ${editable ? `<div class="card" style="margin-top:16px"><h2>Settings</h2><p class="muted small" style="margin-bottom:16px">Changes apply to the next auction, within seconds.</p>
        <div class="row2"><div class="field"><label class="l" for="e-b">Daily budget: <span id="e-bv">${money(c.daily_budget)}</span></label><input type="range" id="e-b" min="5" max="150" step="1" value="${c.daily_budget}"></div>
        <div class="field"><label class="l" for="e-bid">Max per tap (blank = automatic)</label><input class="f" id="e-bid" type="number" min="0.3" max="10" step="0.05" value="${c.bid ?? ""}" placeholder="Automatic"></div></div>
        <div class="row2"><div class="field"><label class="l" for="e-r">Distance: <span id="e-rv">${c.radius_km} km</span></label><input type="range" id="e-r" min="0.5" max="15" step="0.5" value="${c.radius_km}"></div>
        <div class="field"><label class="l" for="e-end">Last day (blank = until you pause)</label><input class="f" id="e-end" type="date" value="${c.ends_on ?? ""}" min="${c.starts_on}"></div></div>
        <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn" id="e-save">Save changes</button><button class="btn danger" id="e-end-now">End this ad</button></div></div>` : ""}`);
    wire();
    if (!editable) return;
    const b = document.getElementById("e-b"), r = document.getElementById("e-r");
    b.oninput = () => (document.getElementById("e-bv").textContent = money(b.value));
    r.oninput = () => (document.getElementById("e-rv").textContent = r.value + " km");
    document.getElementById("e-save").onclick = async () => {
      const bid = document.getElementById("e-bid").value;
      const { error } = await db.from("campaigns").update({ daily_budget: +b.value, bid: bid ? +bid : null, radius_km: +r.value, ends_on: document.getElementById("e-end").value || null }).eq("id", c.id);
      if (error) return toast("Couldn’t save. Check the values and try again.");
      toast("Saved"); await loadRest(S.radius); detail(c.id);
    };
    document.getElementById("e-end-now").onclick = async () => {
      if (!confirm("End this ad? It stops showing now. You can make a new one anytime.")) return;
      await db.from("campaigns").update({ status: "ended" }).eq("id", c.id); toast("Ad ended"); await loadRest(S.radius); detail(c.id);
    };
  }

  // ------------------------------------------------------------------ create an ad (5 steps, with a live forecast and preview)
  function newDraft() {
    const r = rest();
    return { goal: "visits", deal: S.deals.find((d) => d.status === "live")?.id || null, radius: 3, days: [0, 1, 2, 3, 4, 5, 6], from: "00:00", to: "00:00",
      foods: [], audience: "all", budget: 10, bid: null, starts: today(), ends: "", auto: true, placements: ["home", "deals", "search", "map"],
      creatives: [{ photo: r?.photos?.[0] || "", headline: "" }], name: "", agree: false };
  }
  const STEPS = ["Goal", "Audience", "Budget", "Photos", "Review"];
  function createView() {
    S.draft ||= newDraft();
    const d = S.draft, r = rest(), f = forecast(d);
    const deal = S.deals.find((x) => x.id === d.deal);
    const headline = (i = 0) => d.creatives[i]?.headline || (d.goal === "deal" && deal ? deal.title : r?.name || "");
    const step = {
      1: () => `<h2>What do you want from this ad?</h2><p class="muted" style="margin:6px 0 16px">FIG picks the best places to show it for this goal.</p>
        <div class="pick">${Object.entries(GOALS).map(([k, [t, sub, ic]]) => `<button class="opt ${d.goal === k ? "on" : ""}" data-goal="${k}">${ic}<div><b>${t}</b><span>${sub}</span></div></button>`).join("")}</div>
        ${d.goal === "deal" ? (S.deals.length ? `<div class="field" style="margin-top:18px"><label class="l">Which deal?</label><div class="chips">${S.deals.map((x) => `<button class="chip ${d.deal === x.id ? "on" : ""}" data-deal="${x.id}">${esc(x.title)}</button>`).join("")}</div></div>` : `<div class="tip warn" style="margin-top:16px">${I.warn}<div>Make a deal in the app first, then promote it here.</div></div>`) : ""}`,
      2: () => { const ins = S.insights || {}; const crav = (ins.cravings || []).slice(0, 8);
        return `<h2>Who should see it?</h2><p class="muted" style="margin:6px 0 16px">Narrower means fewer people, but closer to what you want.</p>
        <div class="field"><label class="l" for="w-r">Distance from ${esc(r?.name || "you")}: <span id="w-rv">${d.radius} km</span></label><input type="range" id="w-r" min="0.5" max="15" step="0.5" value="${d.radius}"></div>
        <div class="field"><label class="l">Days</label><div class="chips">${DAYS.map((x, i) => `<button class="chip ${d.days.includes(i) ? "on" : ""}" data-day="${i}">${x}</button>`).join("")}</div></div>
        <div class="field"><label class="l">Hours</label><div class="chips" style="margin-bottom:10px"><button class="chip ${d.from === d.to ? "on" : ""}" data-hours="all">All day</button><button class="chip ${d.from === "14:00" && d.to === "17:00" ? "on" : ""}" data-hours="14:00-17:00">Afternoons 2–5 pm</button><button class="chip ${d.from === "11:00" && d.to === "14:00" ? "on" : ""}" data-hours="11:00-14:00">Lunch</button><button class="chip ${d.from === "17:00" && d.to === "21:00" ? "on" : ""}" data-hours="17:00-21:00">Dinner</button><button class="chip ${d.from === "21:00" && d.to === "02:00" ? "on" : ""}" data-hours="21:00-02:00">Late night</button></div>
          <div class="row2"><input class="f" type="time" id="w-from" value="${d.from}" aria-label="From"><input class="f" type="time" id="w-to" value="${d.to}" aria-label="Until"></div></div>
        <div class="field"><label class="l">Diners who crave (optional)</label><div class="chips">${(crav.length ? crav.map((c) => c.food) : (r?.tags || []).slice(0, 6)).map((x) => `<button class="chip ${d.foods.includes(x) ? "on" : ""}" data-food="${esc(x)}">${esc(x)}</button>`).join("")}</div><p class="muted small">Leave all off to reach everyone nearby.</p></div>
        <div class="field"><label class="l">Diners</label><div class="chips">${[["all", "Everyone"], ["new", "New to you"], ["returning", "Been before"]].map(([k, t]) => `<button class="chip ${d.audience === k ? "on" : ""}" data-aud="${k}">${t}</button>`).join("")}</div></div>`; },
      3: () => `<h2>Budget and schedule</h2><p class="muted" style="margin:6px 0 16px">You pay per tap, never more than your daily budget. FIG spreads it through the day.</p>
        <div class="field"><label class="l" for="w-b">Daily budget</label><div class="val" id="w-bv">${money(d.budget)}</div><input type="range" id="w-b" min="5" max="150" step="1" value="${d.budget}">
          <p class="muted small">At most ${money(f.monthMax)} a month. ${f.best > d.budget ? `About ${money(Math.ceil(f.best))} a day would reach every diner available.` : "That covers every tap FIG expects for this audience."}</p></div>
        <div class="field"><label class="l">Bidding</label><div class="chips"><button class="chip ${d.auto ? "on" : ""}" data-bid="auto">Automatic (recommended)</button><button class="chip ${d.auto ? "" : "on"}" data-bid="max">Set a max per tap</button></div>
          ${d.auto ? `<p class="muted small">FIG bids for you and you pay just enough to beat the next ad, usually about ${money(f.cpc)} a tap here.</p>` : `<input class="f" type="number" id="w-bid" min="0.3" max="10" step="0.05" value="${d.bid ?? 1}" style="max-width:200px">`}</div>
        <div class="row2"><div class="field"><label class="l" for="w-s">Start</label><input class="f" type="date" id="w-s" value="${d.starts}" min="${today()}"></div>
          <div class="field"><label class="l" for="w-e">End (optional)</label><input class="f" type="date" id="w-e" value="${d.ends}" min="${d.starts}"></div></div>
        <div class="field"><label class="l">Where it shows</label><div class="chips"><button class="chip ${d.auto_places !== false ? "on" : ""}" data-pl="auto">Automatic (recommended)</button>${Object.entries(PLACES).map(([k, t]) => `<button class="chip ${d.auto_places === false && d.placements.includes(k) ? "on" : ""}" data-pl="${k}">${t}</button>`).join("")}</div></div>`,
      4: () => { const photos = [...new Set([...(r?.photos || []), ...S.deals.map((x) => x.photo).filter(Boolean), ...(d.uploads || [])])];
        return `<h2>Photos and headline</h2><p class="muted" style="margin:6px 0 16px">Add up to 3. FIG rotates them and shows the one diners tap most.</p>
        ${d.creatives.map((c, i) => `<div class="card grey" style="margin-bottom:12px"><div style="display:flex;justify-content:space-between;margin-bottom:10px"><h3>Version ${i + 1}</h3>${i ? `<button class="link" data-rmc="${i}">Remove</button>` : ""}</div>
          <div class="photos" data-drop="${i}">${photos.map((p) => `<button class="${c.photo === p ? "on" : ""}" data-photo="${i}" data-src="${esc(p)}" aria-label="Use this photo"><img src="${esc(p)}" alt=""></button>`).join("")}<label class="photos up" style="aspect-ratio:1;border-radius:10px;background:#fff;cursor:pointer;display:grid;place-items:center"><span>+ Upload<br><small>or drop one here</small></span><input type="file" accept="image/*" data-up="${i}" hidden></label></div>
          <div class="field" style="margin:12px 0 0"><label class="l" for="h${i}">Headline</label><input class="f" id="h${i}" data-head="${i}" maxlength="40" value="${esc(c.headline)}" placeholder="${esc(headline(i))}"></div></div>`).join("")}
        ${d.creatives.length < 3 ? `<button class="btn grey sm" id="addc">${I.plus}Add another version</button>` : ""}`; },
      5: () => `<h2>Review and launch</h2><div class="field" style="margin-top:14px"><label class="l" for="w-n">Ad name (only you see it)</label><input class="f" id="w-n" maxlength="60" value="${esc(d.name || GOALS[d.goal][0] + " · " + day(d.starts))}"></div>
        <div class="card grey" style="display:grid;gap:8px;font-size:15px">
          <div><b>Goal:</b> ${GOALS[d.goal][0]}${d.goal === "deal" && deal ? ` (${esc(deal.title)})` : ""}</div>
          <div><b>Who:</b> within ${d.radius} km · ${d.days.length === 7 ? "every day" : d.days.map((x) => DAYS[x]).join(", ")} · ${d.from === d.to ? "all day" : d.from + " to " + d.to}${d.foods.length ? " · craving " + d.foods.map(esc).join(", ") : ""}${d.audience !== "all" ? " · " + (d.audience === "new" ? "new diners" : "returning diners") : ""}</div>
          <div><b>Budget:</b> ${money(d.budget)} a day · ${d.auto ? "automatic bid" : "max " + money(d.bid) + " a tap"} · from ${day(d.starts)}${d.ends ? " to " + day(d.ends) : ", until you pause"}</div>
          <div><b>Shows on:</b> ${(d.auto_places === false ? d.placements : placesFor(d.goal)).map((p) => PLACES[p]).join(", ")}</div>
          <div><b>Versions:</b> ${d.creatives.length}</div></div>
        <label style="display:flex;gap:10px;align-items:flex-start;margin:18px 0;font-size:15px;line-height:1.45"><input type="checkbox" id="w-ok" ${d.agree ? "checked" : ""} style="margin-top:4px;width:18px;height:18px;accent-color:var(--cobalt)">
          <span>I agree to pay for taps on this ad, up to ${money(d.budget)} a day, invoiced monthly by the FIG team, under the <a href="/business-terms" target="_blank">business terms</a>.</span></label>
        <p class="err" id="w-err"></p>`,
    }[S.step]();
    const few = (S.insights?.diners_area || 0) < 200;
    const fc = `<div class="card blue forecast"><h3 style="color:#fff">Estimated results a day</h3><p class="muted small" style="margin-bottom:8px">${few ? `FIG has ${int(S.insights?.diners_area)} ${S.insights?.diners_area === 1 ? "diner" : "diners"} in ${esc(rest()?.city || "your area")} so far, so these start small and grow as diners join. You never pay for taps that don’t happen.` : "Estimates. They sharpen as FIG learns your area."}</p>
      <div class="num"><span>Views</span><b>${range(f.views)}</b></div><div class="num"><span>Taps</span><b>${range(f.taps)}</b></div>
      <div class="num"><span>Diners who come in</span><b>${range(f.diners)}</b></div><div class="num"><span>Spend</span><b>${range(f.spend, money)}</b></div>
      <div class="num"><span>Per tap</span><b>~${money(f.cpc)}</b></div></div>
      <div class="phone" style="margin-top:20px" aria-label="How diners see it"><div class="where">${d.goal === "deal" ? "Deals near you" : "Where are we eating?"}</div>
        <div class="ph">${d.creatives[0]?.photo ? `<img src="${esc(d.creatives[0].photo)}" alt="">` : ""}<span class="tag">Sponsored</span></div>
        <div class="meta"><div><b>${esc(r?.name || "")}</b><span>${esc(headline(0))}</span></div>${deal && d.goal === "deal" ? `<span class="tag">Deal</span>` : ""}</div></div>`;
    shell("create", `<div class="head"><div><h1>Create an ad</h1><p>For ${esc(r?.name || "")}. Pay only when diners tap.</p></div><button class="link" id="w-reset">Start over</button></div>
      <div class="steps">${STEPS.map((t, i) => `<span class="${i + 1 === S.step ? "on" : i + 1 < S.step ? "done" : ""}">${i + 1}. ${t}</span>`).join("")}</div>
      <div class="wiz"><div class="card">${step}<div style="display:flex;justify-content:space-between;margin-top:24px">${S.step > 1 ? '<button class="btn grey" id="w-back">Back</button>' : "<span></span>"}
        <button class="btn" id="w-next" ${S.step === 1 && d.goal === "deal" && !d.deal ? "disabled" : ""}>${S.step === 5 ? "Launch ad" : "Continue"}</button></div></div><div>${fc}</div></div>`);
    wire(); wireWizard();
  }
  const placesFor = (goal) => (goal === "deal" ? ["deals", "search"] : ["home", "map", "search"]);
  function wireWizard() {
    const d = S.draft, again = () => createView();
    const on = (sel, fn) => document.querySelectorAll(sel).forEach((el) => (el.onclick = () => fn(el)));
    on("[data-goal]", (el) => { d.goal = el.dataset.goal; if (d.goal === "quiet" && d.from === d.to) { d.from = "14:00"; d.to = "17:00"; } again(); });
    on("[data-deal]", (el) => { d.deal = el.dataset.deal; again(); });
    on("[data-day]", (el) => { const i = +el.dataset.day; d.days = d.days.includes(i) ? d.days.filter((x) => x !== i) : [...d.days, i].sort(); again(); });
    on("[data-hours]", (el) => { [d.from, d.to] = el.dataset.hours === "all" ? ["00:00", "00:00"] : el.dataset.hours.split("-"); again(); });
    on("[data-food]", (el) => { const x = el.dataset.food; d.foods = d.foods.includes(x) ? d.foods.filter((y) => y !== x) : [...d.foods, x]; again(); });
    on("[data-aud]", (el) => { d.audience = el.dataset.aud; again(); });
    on("[data-bid]", (el) => { d.auto = el.dataset.bid === "auto"; d.bid = d.auto ? null : d.bid || 1; again(); });
    on("[data-pl]", (el) => { const k = el.dataset.pl; if (k === "auto") d.auto_places = true; else { if (d.auto_places !== false) { d.auto_places = false; d.placements = []; } d.placements = d.placements.includes(k) ? d.placements.filter((x) => x !== k) : [...d.placements, k]; } again(); });
    on("[data-photo]", (el) => { d.creatives[+el.dataset.photo].photo = el.dataset.src; again(); });
    on("[data-rmc]", (el) => { d.creatives.splice(+el.dataset.rmc, 1); again(); });
    const addc = document.getElementById("addc"); if (addc) addc.onclick = () => { d.creatives.push({ photo: "", headline: "" }); again(); };
    document.querySelectorAll("[data-head]").forEach((el) => (el.oninput = () => { d.creatives[+el.dataset.head].headline = el.value; }));
    // a photo for version i: picked with the file chooser, or dragged onto that version's photos from the computer
    const upload = async (file, i) => {
      if (!file) return;
      if (!file.type.startsWith("image/")) return toast("That isn’t a photo. Drop a JPG or PNG.");
      if (file.size > 8e6) return toast("That photo is too big (8 MB at most).");
      toast("Uploading…");
      const path = `${S.rid}/ad-${Date.now().toString(36)}.${(file.type.split("/")[1] || "jpg").replace("jpeg", "jpg")}`;
      const { error } = await db.storage.from("photos").upload(path, file, { contentType: file.type });
      if (error) return toast("Couldn’t upload that photo. Try another.");
      const url = db.storage.from("photos").getPublicUrl(path).data.publicUrl;
      d.uploads = [...(d.uploads || []), url]; d.creatives[i].photo = url; again();
    };
    document.querySelectorAll("[data-up]").forEach((el) => (el.onchange = () => upload(el.files?.[0], +el.dataset.up)));
    document.querySelectorAll("[data-drop]").forEach((el) => {
      el.ondragover = (e) => { e.preventDefault(); el.classList.add("drop"); };
      el.ondragleave = (e) => { if (!el.contains(e.relatedTarget)) el.classList.remove("drop"); };
      el.ondrop = (e) => { e.preventDefault(); el.classList.remove("drop"); upload(e.dataTransfer?.files?.[0], +el.dataset.drop); };
    });
    const val = (id) => document.getElementById(id);
    if (val("w-r")) val("w-r").oninput = (e) => { d.radius = +e.target.value; val("w-rv").textContent = d.radius + " km"; };
    if (val("w-r")) val("w-r").onchange = again;
    if (val("w-from")) { val("w-from").onchange = (e) => { d.from = e.target.value || "00:00"; again(); }; val("w-to").onchange = (e) => { d.to = e.target.value || "00:00"; again(); }; }
    if (val("w-b")) { val("w-b").oninput = (e) => { d.budget = +e.target.value; val("w-bv").textContent = money(d.budget); }; val("w-b").onchange = again; }
    if (val("w-bid")) val("w-bid").onchange = (e) => { d.bid = clamp(+e.target.value || 1, 0.3, 10); again(); };
    if (val("w-s")) { val("w-s").onchange = (e) => { d.starts = e.target.value || today(); again(); }; val("w-e").onchange = (e) => { d.ends = e.target.value; again(); }; }
    if (val("w-n")) val("w-n").oninput = (e) => { d.name = e.target.value; };
    if (val("w-ok")) val("w-ok").onchange = (e) => { d.agree = e.target.checked; };
    val("w-reset").onclick = () => { S.draft = newDraft(); S.step = 1; again(); };
    if (val("w-back")) val("w-back").onclick = () => { S.step--; again(); };
    val("w-next").onclick = async () => {
      if (S.step === 2 && !d.days.length) return toast("Pick at least one day.");
      if (S.step === 3 && d.auto_places === false && !d.placements.length) return toast("Pick at least one place to show it.");
      if (S.step === 4 && !d.creatives.some((c) => c.photo)) return toast("Pick a photo for your ad.");
      if (S.step < 5) { S.step++; return again(); }
      if (!d.agree) { val("w-err").textContent = "Tick the box to agree to pay for taps."; return; }
      const btn = val("w-next"); btn.disabled = true; btn.textContent = "Launching…";
      const deal = d.goal === "deal" ? d.deal : null;
      const row = {
        restaurant_id: S.rid, name: (d.name || GOALS[d.goal][0] + " · " + day(d.starts)).slice(0, 60), goal: d.goal, deal_id: deal, daily_budget: d.budget, bid: d.auto ? null : d.bid,
        starts_on: d.starts, ends_on: d.ends || null, radius_km: d.radius, days: d.days, from_time: d.from, to_time: d.to, foods: d.foods, audience: d.audience,
        placements: d.auto_places === false ? d.placements : placesFor(d.goal), creatives: d.creatives.filter((c) => c.photo).map((c) => ({ photo: c.photo, headline: c.headline.trim() })),
      };
      const { data, error } = await db.from("campaigns").insert(row).select("id").single();
      if (error) { btn.disabled = false; btn.textContent = "Launch ad"; val("w-err").textContent = /not-your-deal|pick-a-deal/.test(error.message) ? "Pick one of your live deals." : "Couldn’t launch it. Check your connection and try again."; return; }
      S.draft = null; S.step = 1; toast("Your ad is live");
      await loadRest(S.radius); location.hash = "campaign/" + data.id;
    };
  }

  // ------------------------------------------------------------------ insights: the bigger picture
  function insightsView() {
    const ins = S.insights || {};
    // area insights are FIG Premium ($50 a year, bought in the FIG app): without it, a taste and what Premium adds
    if (ins.premium === false) {
      shell("insights", `<div class="head"><div><h1>Insights</h1><p>The bigger picture around ${esc(rest()?.name || "you")}, with FIG Premium.</p></div></div>
        <div class="grid g4" style="margin-bottom:20px">
          <div class="stat"><span>Diners on FIG in ${esc(rest()?.city || "your area")}</span><b>${int(ins.diners_area)}</b><em style="color:var(--slate)">${int(ins.diners_all)} across FIG</em></div>
          <div class="stat"><span>Cost per tap here</span><b>${money(Math.max(ins.floor || 0.3, ins.cpc || 0))}</b><em style="color:var(--slate)">${pct(ins.ctr || 0.03, 1)} of views get tapped</em></div>
        </div>
        <div class="card" style="display:grid;gap:12px;max-width:640px">
          <span class="tag blue" style="justify-self:start">FIG Premium · $50 a year</span>
          <h2>See your whole area</h2>
          <p class="muted">When diners near you claim deals, how that compares with your own scans, what they crave, food trends, and how many restaurants, deals and ads are around you. Premium also adds unlimited locations, weekly deal announcements to diners who crave your food, and a Premium badge.</p>
          <p><b>Get it in the FIG app:</b> Settings → FIG Premium. Everything else on FIG stays free.</p>
        </div>`);
      return;
    }
    const hours = Array.from({ length: 24 }, (_, h) => ({ h, area: ins.claim_hours?.find((x) => x.h === h)?.n || 0, mine: ins.my_hours?.find((x) => x.h === h)?.n || 0 }));
    const amax = Math.max(1, ...hours.map((x) => x.area)), mmax = Math.max(1, ...hours.map((x) => x.mine));
    const W = 720, H = 150, bw = W / 24;
    const hourChart = `<svg class="chart" viewBox="0 0 ${W} ${H + 22}" preserveAspectRatio="none" role="img" aria-label="Deal claims near you by hour, and your scans">${hours.map((x) => `
      <g><title>${hourName(x.h)}: ${x.area} claims near you, ${x.mine} of your scans</title><rect x="${x.h * bw + 2}" y="${H - (x.area / amax) * H}" width="${bw * 0.55}" height="${Math.max(1, (x.area / amax) * H)}" rx="3" fill="#C9D6FF"/>
      <rect x="${x.h * bw + bw * 0.5}" y="${H - (x.mine / mmax) * H}" width="${bw * 0.35}" height="${Math.max(1, (x.mine / mmax) * H)}" rx="3" fill="#1E5EFF"/>
      ${x.h % 3 === 0 ? `<text x="${x.h * bw + bw / 2}" y="${H + 16}" font-size="11" text-anchor="middle" fill="#5C6470">${hourName(x.h)}</text>` : ""}</g>`).join("")}</svg>`;
    const bars = (rows, total) => rows.length ? rows.map((x) => `<div class="hbar"><span>${esc(x.food)}</span><div class="bar"><i style="width:${clamp((x.n / Math.max(1, total)) * 100, 3, 100)}%"></i></div><span class="muted">${int(x.n)}</span></div>`).join("") : '<p class="muted">Not enough activity yet.</p>';
    shell("insights", `<div class="head"><div><h1>Insights</h1><p>The bigger picture around ${esc(rest()?.name || "you")}, before you spend a dollar.</p></div>
      <div class="chips">${[1, 2, 3, 5, 10].map((k) => `<button class="chip ${S.radius === k ? "on" : ""}" data-rad="${k}">${k} km</button>`).join("")}</div></div>
      <div class="grid g4" style="margin-bottom:20px">
        <div class="stat"><span>Diners on FIG in ${esc(rest()?.city || "your area")}</span><b>${int(ins.diners_area)}</b><em style="color:var(--slate)">${int(ins.diners_all)} across FIG</em></div>
        <div class="stat"><span>Restaurants within ${S.radius} km</span><b>${int(ins.nearby_places)}</b><em style="color:var(--slate)">${int(ins.nearby_deals)} with a live deal</em></div>
        <div class="stat"><span>Running ads nearby</span><b>${int(ins.nearby_ads)}</b><em style="color:var(--slate)">${ins.nearby_ads ? "you’d compete in the auction" : "nobody else, right now"}</em></div>
        <div class="stat"><span>Cost per tap here</span><b>${money(Math.max(ins.floor || 0.3, ins.cpc || 0))}</b><em style="color:var(--slate)">${pct(ins.ctr || 0.03, 1)} of views get tapped</em></div>
      </div>
      <div class="card" style="margin-bottom:16px"><h2>When diners near you claim deals</h2><p class="muted small">Last 30 days, within ${S.radius} km. Light bars: everyone nearby. Blue: your own scans.</p>${hourChart}
        <div class="legend"><span><i style="background:#C9D6FF"></i>Deal claims near you</span><span><i style="background:#1E5EFF"></i>Your scans</span></div></div>
      <div class="grid g2" style="margin-bottom:16px">
        <div class="card"><h2>What diners crave</h2><p class="muted small">From diners’ taste settings on FIG.</p>${bars(ins.cravings || [], (ins.cravings || [])[0]?.n)}</div>
        <div class="card"><h2>Trending near you</h2><p class="muted small">Foods of the deals claimed within ${S.radius} km, last 30 days.</p>${bars(ins.foods || [], (ins.foods || [])[0]?.n)}</div>
      </div>
      <div class="card"><h2>What to do next</h2><div class="grid" style="margin-top:12px">${tipHtml(tips())}</div><p style="margin-top:16px"><button class="btn" data-go2="create">Create an ad from this</button></p></div>`);
    wire();
    document.querySelectorAll("[data-rad]").forEach((b) => (b.onclick = async () => { await loadRest(+b.dataset.rad); insightsView(); }));
  }

  // ------------------------------------------------------------------ billing
  function billingView() {
    const month = S.campaigns.reduce((a, c) => a + Number(st(c).spend_month || 0), 0);
    const a = S.account;
    shell("billing", `<div class="head"><div><h1>Billing</h1><p>Pay per tap. The FIG team emails an invoice at the start of each month.</p></div></div>
      <div class="grid g4" style="margin-bottom:20px">
        <div class="stat"><span>This month so far</span><b>${money(month)}</b><em style="color:var(--slate)">for ${esc(rest()?.name || "")}</em></div>
        <div class="stat"><span>Monthly limit</span><b>${a ? money(a.monthly_limit) : "—"}</b><em style="color:var(--slate)">ads pause when it’s reached</em></div>
        <div class="stat"><span>Account</span><b style="font-size:22px">${a ? (a.status === "held" ? "On hold" : "In good standing") : "Opens with your first ad"}</b></div>
      </div>
      ${a ? `<div class="card grey" style="margin-bottom:16px"><div class="bar"><i style="width:${clamp((month / Math.max(1, a.monthly_limit)) * 100, 1, 100)}%"></i></div><p class="muted small" style="margin-top:8px">${money(month)} of ${money(a.monthly_limit)} this month. Need a higher limit? Email <a href="mailto:business@fig.app?subject=Ads%20limit">business@fig.app</a>.</p></div>` : ""}
      <h2 style="margin:24px 0 12px">Invoices</h2>
      ${S.invoices.length ? `<div class="tblwrap"><table class="tbl"><tr><th>Month</th><th>Amount</th><th>Status</th></tr>${S.invoices.map((x) => `<tr><td>${new Date(x.month + "T12:00:00").toLocaleDateString("en-CA", { month: "long", year: "numeric" })}</td><td><b>${money(x.amount)}</b></td><td><span class="tag ${x.status === "paid" ? "live" : x.status === "sent" ? "blue" : ""}">${{ open: "Being prepared", sent: "Sent", paid: "Paid", void: "Cancelled" }[x.status]}</span></td></tr>`).join("")}</table></div>`
        : `<div class="empty"><h3>No invoices yet</h3><p>Your first one arrives at the start of the month after your ads get taps.</p></div>`}
      <div class="card" style="margin-top:16px"><h3>How billing works</h3><ul class="muted" style="margin:10px 0 0;padding-left:18px;line-height:1.7">
        <li>You pay only for taps, at most your daily budget per ad, and never past your monthly limit.</li>
        <li>A diner tapping the same ad twice in a day is charged once.</li>
        <li>The FIG team emails your invoice at the start of each month with how to pay. Questions: <a href="mailto:business@fig.app">business@fig.app</a>.</li>
        <li>Listing, deals, scans, takeout and chats stay free.</li></ul></div>`);
    wire();
  }

  // ------------------------------------------------------------------ wiring and routes
  function wire() {
    document.querySelectorAll("[data-go2]").forEach((b) => (b.onclick = () => go(b.dataset.go2)));
    document.querySelectorAll("[data-open]").forEach((b) => (b.onclick = (e) => { if (e.target.closest("[data-toggle]")) return; location.hash = "campaign/" + b.dataset.open; }));
    document.querySelectorAll("[data-toggle]").forEach((b) => (b.onclick = async (e) => {
      e.stopPropagation();
      const c = S.campaigns.find((x) => x.id === b.dataset.toggle);
      const status = c.status === "active" ? "paused" : "active";
      const { error } = await db.from("campaigns").update({ status }).eq("id", c.id);
      if (error) return toast("Couldn’t change it. Try again.");
      c.status = status; toast(status === "active" ? "Ad running" : "Ad paused"); route();
    }));
  }
  function route() {
    if (!S.rid) {
      app.innerHTML = `<div class="signin"><div class="side"><div class="brand" style="color:#fff">FIG Ads Manager</div><h1>Ads are for restaurants on FIG.</h1><p></p></div>
        <div style="padding:48px;display:grid;gap:14px;align-content:center;max-width:460px"><h2>No restaurant on this account</h2><p class="muted">Sign up as a restaurant in the FIG app (it’s free), or ask the owner to add you as a manager. Then sign in here.</p><button class="btn grey" id="so2">Sign out</button></div></div>`;
      document.getElementById("so2").onclick = async () => { await db.auth.signOut(); signInView(); };
      return;
    }
    const h = location.hash.slice(1) || "overview";
    if (h.startsWith("campaign/")) return void detail(h.slice(9));
    ({ overview, campaigns: campaignsView, create: createView, insights: insightsView, billing: billingView }[h] || overview)();
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", () => S.session && route());

  async function start() {
    const { data } = await db.auth.getSession();
    S.session = data.session;
    if (!S.session) return signInView();
    try {
      await loadRests();
      if (S.rid) await loadRest(3);
      route();
    } catch (e) {
      app.innerHTML = `<p class="boot">Couldn’t load your ads. Refresh to try again.</p>`;
      console.error(e);
    }
  }
  start();
})();
