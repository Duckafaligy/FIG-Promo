(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const root = document.documentElement;
  const motion = root.classList.contains("motion") && window.gsap && window.ScrollTrigger;
  if (!motion) root.classList.remove("motion");
  else gsap.registerPlugin(ScrollTrigger);

  // ---------- nav ----------
  const nav = $(".nav");
  const onScroll = () => nav.classList.toggle("solid", scrollY > 40);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // ---------- real app screens, scaled into the device frames ----------
  const screensReady = Promise.all($$(".screen-slot").map((slot) =>
    fetch(`/screens/${slot.dataset.screen}.html`).then((r) => r.text()).then((html) => { slot.innerHTML = html; })));
  $$(".device").forEach((dev) => {
    const scr = $(".device-screen", dev);
    const fit = () => { const s = scr.clientWidth / +dev.dataset.w; $$(".screen-slot", dev).forEach((sl) => { sl.style.transform = `scale(${s})`; }); };
    new ResizeObserver(fit).observe(scr); fit();
  });

  // ---------- letter rise (the videos' headline move) ----------
  function split(el) {
    const chars = [];
    [...el.childNodes].forEach((n) => {
      if (n.nodeType !== 3) return;
      const frag = document.createDocumentFragment();
      n.textContent.split(/( )/).forEach((w) => {
        if (!w) return;
        if (w === " ") { frag.appendChild(document.createTextNode(" ")); return; }
        const word = document.createElement("span"); word.style.cssText = "display:inline-block;white-space:nowrap";
        for (const c of w) { const s = document.createElement("span"); s.className = "ch"; s.textContent = c; word.appendChild(s); chars.push(s); }
        frag.appendChild(word);
      });
      n.replaceWith(frag);
    });
    return chars;
  }
  function rise(h, delay) {
    const lines = $$(".line", h).map(split);
    lines.forEach((chars, i) => gsap.fromTo(chars, { yPercent: 118 }, { yPercent: 0, duration: 0.75, ease: "power3.out", stagger: 0.028, delay: delay + i * 0.32 }));
  }
  $$(".rise").forEach((h) => $$(".mask", h).forEach((m) => m.setAttribute("aria-hidden", "true")));

  if (motion) {
    rise($(".hero .rise"), 0.5);
    gsap.fromTo(".hero .chip", { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power2.out", delay: 0.3 });
    gsap.fromTo(".hero .fade-in", { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: "power2.out", stagger: 0.12, delay: 1.3 });

    const outro = $(".outro");
    gsap.set($$(".line", outro), { yPercent: 118 });
    ScrollTrigger.create({ trigger: outro, start: "top 70%", once: true, onEnter: () => {
      gsap.set($$(".line", outro), { yPercent: 0 });
      rise($(".rise", outro), 0.35);
      gsap.fromTo(".outro .logo", { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power2.out" });
      gsap.fromTo("#outro-leaf", { y: -18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: "bounce.out", delay: 0.25 });
    } });
  }

  // ---------- how it works: one pinned phone, four steps ----------
  const steps = $$(".step"), pips = $$(".pips i"), phoneSlots = $$(".how .screen-slot");
  let cur = 0;
  function setStep(i) {
    if (i === cur) return;
    const dir = i > cur ? 1 : -1;
    gsap.to(steps[cur], { y: -16 * dir, opacity: 0, duration: 0.3, ease: "power2.in", overwrite: true });
    gsap.fromTo(steps[i], { y: 18 * dir, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out", delay: 0.15, overwrite: true });
    gsap.to(phoneSlots[cur], { opacity: 0, y: -24 * dir, duration: 0.35, ease: "power2.in", overwrite: true });
    gsap.fromTo(phoneSlots[i], { opacity: 0, y: 40 * dir }, { opacity: 1, y: 0, duration: 0.6, ease: "back.out(1.4)", delay: 0.1, overwrite: true });
    pips.forEach((p, k) => p.classList.toggle("on", k === i));
    cur = i;
  }
  pips[0] && pips[0].classList.add("on");
  if (motion) ScrollTrigger.create({ trigger: ".how", start: "top top", end: "bottom bottom",
    onUpdate: (st) => setStep(Math.min(steps.length - 1, Math.floor(st.progress * steps.length))) });

  // ---------- passport stamps ----------
  const grid = $("#stamps");
  const pins = window.FIG_PINS || [];
  for (let i = 0; i < 25; i++) {
    const slot = document.createElement("div"); slot.className = "slot";
    const st = document.createElement("div"); st.className = "st";
    st.style.backgroundImage = `url(${pins[(i * 7) % pins.length]})`;
    slot.appendChild(st); grid.appendChild(slot);
  }
  const stamps = $$(".st", grid);
  if (motion) {
    gsap.timeline({ scrollTrigger: { trigger: grid, start: "top 80%", end: "bottom 40%", scrub: 0.6 } })
      .fromTo(stamps, { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, ease: "back.out(2.2)", duration: 0.4, stagger: 0.1 });
  } else stamps.forEach((s) => { s.style.opacity = 1; });

  // ---------- what's the catch? ----------
  function playChat(panel) {
    if (!motion) return;
    gsap.fromTo($$(".q, .a", panel), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power2.out", stagger: 0.12, overwrite: true });
  }
  function selectTab(name) {
    $$(".catch [data-tab]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === name)));
    $$(".catch [data-panel]").forEach((p) => { p.hidden = p.dataset.panel !== name; if (!p.hidden) playChat(p); });
  }
  $$(".catch [data-tab]").forEach((b) => b.addEventListener("click", () => selectTab(b.dataset.tab)));
  if (motion) {
    gsap.set($$(".catch .q, .catch .a"), { opacity: 0 });
    ScrollTrigger.create({ trigger: ".catch .chat", start: "top 80%", once: true, onEnter: () => playChat($(".catch [data-panel]:not([hidden])")) });
  }

  // ---------- restaurant tablet: tap through, or it steps itself while visible ----------
  const tSlots = $$(".owners .screen-slot"), tTabs = $$("[data-tscreen]");
  let tCur = 0, tTimer = null;
  function showT(i) {
    if (i === tCur) return;
    tSlots.forEach((s, k) => { if (motion) gsap.to(s, { opacity: k === i ? 1 : 0, duration: 0.4, overwrite: true }); else s.style.opacity = k === i ? 1 : 0; });
    tTabs.forEach((b, k) => b.setAttribute("aria-selected", String(k === i)));
    tCur = i;
  }
  tTabs.forEach((b) => b.addEventListener("click", () => { clearInterval(tTimer); tTimer = "stopped"; showT(+b.dataset.tscreen); }));
  new IntersectionObserver(([e]) => {
    if (tTimer === "stopped") return;
    clearInterval(tTimer); tTimer = null;
    if (e.isIntersecting && motion) tTimer = setInterval(() => showT((tCur + 1) % tSlots.length), 3200);
  }, { threshold: 0.5 }).observe($(".owners .tablet"));

  // ---------- waitlist ----------
  const form = $("#waitlist"), msg = $("#form-msg"), btn = $("#submit");
  const contact = form.elements.contact;
  function setRole(role) {
    form.elements.role.value = role;
    $$("[data-only=restaurant]", form).forEach((el) => { el.hidden = role !== "restaurant"; });
    btn.textContent = role === "restaurant" ? "Get my restaurant on FIG" : "Join the waitlist";
    $("legend", form).textContent = role === "restaurant" ? "Where is your restaurant?" : "Where do you eat most?";
  }
  $$("input[name=role]", form).forEach((r) => r.addEventListener("change", () => setRole(r.value)));
  $$("[data-role-link=restaurant]").forEach((a) => a.addEventListener("click", () => { setRole("restaurant"); selectTab("restaurant"); }));
  contact.addEventListener("input", () => contact.removeAttribute("aria-invalid"));

  const say = (text, err) => { msg.textContent = text; msg.classList.toggle("err", !!err); };
  const cfg = window.FIG_CONFIG || {};
  const api = (path, body) => fetch(`${cfg.supabaseUrl}/rest/v1/${path}`, {
    method: "POST", headers: { apikey: cfg.supabaseKey, "Content-Type": "application/json", Prefer: "return=minimal" }, body: JSON.stringify(body) });

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    if (form.elements.website.value) return; // bots fill the hidden field
    const role = form.elements.role.value;
    const who = parseContact(contact.value);
    if (!who) { contact.setAttribute("aria-invalid", "true"); contact.focus(); return say("Enter an email, or a 10-digit mobile number.", true); }
    const restaurant = form.elements.restaurant.value.trim();
    if (role === "restaurant" && !restaurant) { form.elements.restaurant.focus(); return say("Add your restaurant's name.", true); }
    if (!form.elements.consent.checked) return say("Tick the box so we're allowed to message you.", true);
    if (!cfg.supabaseUrl || !cfg.supabaseKey) return say("Sign-ups open in the next few days. Check back soon!", true);

    btn.disabled = true; say("");
    const src = new URLSearchParams(location.search).get("src") || (location.pathname.startsWith("/owners") ? "owners" : "site");
    try {
      const r = await api("waitlist", { role, ...who, restaurant: role === "restaurant" ? restaurant : null,
        area: (form.elements.area.value || null), consent: true, source: src.slice(0, 60) });
      if (!r.ok && r.status !== 409) throw new Error(r.status);
      done(role, restaurant);
    } catch (e) {
      btn.disabled = false;
      say("Something went wrong. Try again in a moment.", true);
    }
  });

  function done(role, restaurant) {
    const box = document.createElement("div"); box.className = "done";
    box.innerHTML = `<div class="tick"><svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <h3>You're on the list.</h3><p></p>`;
    $("p", box).textContent = role === "restaurant"
      ? `We'll reach out to set up ${restaurant} before launch.`
      : "We'll message you the day FIG opens in Markham.";
    if (navigator.share) {
      const share = document.createElement("button"); share.className = "btn btn-ghost"; share.type = "button"; share.textContent = "Tell a friend";
      share.addEventListener("click", () => navigator.share({ title: "FIG", text: "Local deals in Markham, coming soon on FIG", url: location.origin }).catch(() => {}));
      box.appendChild(share);
    }
    form.replaceChildren(box);
    if (motion) gsap.fromTo(".done .tick", { scale: 0.4 }, { scale: 1, duration: 0.7, ease: "back.out(2)" });
  }

  // real waitlist count, shown once it's worth showing
  if (cfg.supabaseUrl && cfg.supabaseKey) {
    api("rpc/waitlist_count", {}).then((r) => r.ok ? r.json() : null).then((n) => {
      if (n >= 100) { const c = $("#counter"); c.innerHTML = `<b>${Number(n).toLocaleString()}</b> people in Markham are already waiting.`; c.hidden = false; }
    }).catch(() => {});
  }

  // figpromo.com/owners: the link to open on your phone when you walk into a restaurant
  if (location.pathname.startsWith("/owners")) {
    setRole("restaurant"); selectTab("restaurant");
    screensReady.then(() => $("#owners").scrollIntoView());
  }
})();
