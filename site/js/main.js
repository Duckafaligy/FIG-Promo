(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const root = document.documentElement;
  const motion = root.classList.contains("motion") && window.gsap && window.ScrollTrigger;
  if (!motion) root.classList.remove("motion");
  else gsap.registerPlugin(ScrollTrigger);
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;

  // ---------- cursor-lit background ----------
  if (finePointer) {
    let mx = 0, my = 0, queued = false;
    addEventListener("pointermove", (e) => {
      mx = e.clientX; my = e.clientY;
      if (!document.body.classList.contains("pointer")) document.body.classList.add("pointer");
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => { root.style.setProperty("--mx", mx + "px"); root.style.setProperty("--my", my + "px"); queued = false; });
    }, { passive: true });
    document.addEventListener("pointerleave", () => document.body.classList.remove("pointer"));
  }

  // ---------- nav ----------
  const nav = $("#nav");
  const onScroll = () => nav.classList.toggle("scrolled", scrollY > 30);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  const links = $$(".nav-links a");
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) links.forEach((a) => a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" });
  ["how", "features", "catch", "owners"].forEach((id) => { const s = document.getElementById(id); if (s) io.observe(s); });

  // ---------- food strip ----------
  const FOOD = [["golden-lantern", "Dim sum"], ["kinton-ramen", "Ramen"], ["chatime", "Bubble tea"], ["pho-hung", "Pho"], ["sakura-house", "Sushi"],
    ["burger-co", "Burgers"], ["seoul-house", "Korean BBQ"], ["alt-tacos", "Tacos"], ["alt-pizza", "Pizza"], ["alt-hotpot", "Hot pot"],
    ["alt-banhmi", "Banh mi"], ["brew-lab", "Coffee"], ["bowl-lab", "Rice bowls"], ["dumpling-house", "Dumplings"], ["noodle-bar", "Noodles"], ["wok-bar", "Stir-fry"]];
  const chip = ([f, n]) => `<span class="food"><img src="/assets/food/${f}.webp" alt="" loading="lazy" width="40" height="40">${n}</span>`;
  $$("[data-marquee]").forEach((t, k) => {
    const list = k ? [...FOOD.slice(8), ...FOOD.slice(0, 8)] : FOOD;
    const html = list.map(chip).join("");
    t.innerHTML = html + html; // twice, so the loop is seamless
  });

  // ---------- passport stamps ----------
  const pins = window.FIG_PINS || [];
  $("#stamps").innerHTML = pins.slice(0, 12).map((p) => `<span class="stamp"><img src="${p}" alt="" loading="lazy"></span>`).join("");

  // ---------- letter rise (the videos' headline move) ----------
  function split(line) {
    const chars = [];
    const text = line.textContent; line.textContent = "";
    text.split(/( )/).forEach((w) => {
      if (!w) return;
      if (w === " ") { line.appendChild(document.createTextNode(" ")); return; }
      const word = document.createElement("span"); word.style.cssText = "display:inline-block;white-space:nowrap";
      for (const c of w) { const s = document.createElement("span"); s.className = "ch"; s.textContent = c; word.appendChild(s); chars.push(s); }
      line.appendChild(word);
    });
    return chars;
  }
  $$(".rise .mask").forEach((m) => m.setAttribute("aria-hidden", "true"));
  function rise(h, delay = 0) {
    $$(".line", h).forEach((l, i) => gsap.fromTo(split(l), { yPercent: 118 }, { yPercent: 0, duration: 0.8, ease: "power3.out", stagger: 0.028, delay: delay + i * 0.3 }));
  }

  if (motion) {
    rise($(".hero .rise"), 0.25);
    gsap.to(".intro", { opacity: 1, y: 0, duration: 0.8, ease: "power3.out", stagger: 0.1, delay: 0.55 });
    ScrollTrigger.batch(".reveal", { start: "top 88%", once: true,
      onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out", stagger: 0.08, overwrite: true }) });
    const closing = $(".closing .rise");
    gsap.set($$(".line", closing), { yPercent: 118 });
    ScrollTrigger.create({ trigger: closing, start: "top 85%", once: true, onEnter: () => { gsap.set($$(".line", closing), { yPercent: 0 }); rise(closing); } });
    // stamps slam in one after another
    gsap.from(".stamp", { scale: 0.2, opacity: 0, rotate: -25, duration: 0.5, ease: "back.out(2.4)", stagger: 0.06,
      scrollTrigger: { trigger: "#stamps", start: "top 85%", once: true } });
    // reward numbers count up
    $$("[data-count]").forEach((b) => {
      const n = +b.dataset.count, o = { v: 0 };
      gsap.to(o, { v: n, duration: 1.4, ease: "power2.out", onUpdate: () => (b.textContent = Math.round(o.v)),
        scrollTrigger: { trigger: b, start: "top 90%", once: true } });
    });
  }

  // ---------- tilt + glare on phones ----------
  if (finePointer && motion) $$(".tilt").forEach((el) => {
    el.addEventListener("pointermove", (e) => {
      const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      el.style.transform = `perspective(900px) rotateY(${(x - 0.5) * 12}deg) rotateX(${(0.5 - y) * 10}deg) translateY(-6px)`;
      el.style.setProperty("--px", x * 100 + "%"); el.style.setProperty("--py", y * 100 + "%");
    });
    el.addEventListener("pointerleave", () => { el.style.transform = ""; });
  });

  // ---------- bento cells: spotlight, tap to open on touch ----------
  $$(".cell").forEach((c) => {
    c.addEventListener("pointermove", (e) => { const r = c.getBoundingClientRect(); c.style.setProperty("--cx", e.clientX - r.left + "px"); c.style.setProperty("--cy", e.clientY - r.top + "px"); });
    if (!finePointer) c.addEventListener("click", () => c.classList.toggle("open"));
  });

  // ---------- video loops: load and play only while on screen ----------
  const vio = new IntersectionObserver((es) => es.forEach((e) => {
    const v = e.target;
    if (e.isIntersecting) {
      if (!v.src) v.src = v.dataset.src;
      v.play().catch(() => {});
    } else v.pause();
  }), { threshold: 0.35 });
  $$("video[data-src]").forEach((v) => vio.observe(v));

  // ---------- what's the catch: a chat that types ----------
  const QA = {
    diner: [["is it actually free?", "Yes. Deals are free to claim and use."], ["so what do I pay?", "Just your bill, at the restaurant, like normal."],
      ["do restaurants get my number?", "Never. You chat in the app and your number stays private."], ["can someone use my screenshot?", "No. Your code changes every 5 minutes."],
      ["are the deals real?", "Every deal and its hours are set by the restaurant itself."]],
    restaurant: [["do I need new equipment?", "No. Any phone or tablet scans."], ["what if a code won't scan?", "Type it in. Same check."],
      ["what if we get too busy?", "You set a daily cap. Pause anytime."], ["ok so what does it cost?", "$50 a year. No fee per diner."],
      ["I have two locations", "One plan covers every location."]],
  };
  const body = $("#chat-body");
  let run = 0;
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  function bubble(kind, text) {
    const b = document.createElement("div"); b.className = `bub ${kind} bub-in`;
    if (kind === "typing") { b.className = "bub a typing bub-in"; b.innerHTML = "<i></i><i></i><i></i>"; } else b.textContent = text;
    body.appendChild(b); return b;
  }
  async function play(tab) {
    const id = ++run; body.innerHTML = "";
    for (const [q, a] of QA[tab]) {
      if (id !== run) return;
      if (!motion) { bubble("q", q); bubble("a", a); continue; }
      bubble("q", q); await wait(450);
      if (id !== run) return;
      const t = bubble("typing"); await wait(750);
      if (id !== run) return;
      t.remove(); bubble("a", a); await wait(500);
    }
  }
  function selectTab(tab) {
    $$("#catch [data-tab]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === tab)));
    play(tab);
  }
  $$("#catch [data-tab]").forEach((b) => b.addEventListener("click", () => selectTab(b.dataset.tab)));
  let chatStarted = false;
  new IntersectionObserver(([e]) => { if (e.isIntersecting && !chatStarted) { chatStarted = true; play("diner"); } }, { threshold: 0.3 }).observe($(".chatwin"));

  // ---------- restaurant tablet: steps itself while visible, until tapped ----------
  const shots = $$(".tablet img"), tabs = $$("[data-tshot]");
  let cur = 0, timer = null, stopped = false;
  function show(i) { cur = i; shots.forEach((s, k) => s.classList.toggle("on", k === i)); tabs.forEach((b, k) => b.setAttribute("aria-selected", String(k === i))); }
  tabs.forEach((b) => b.addEventListener("click", () => { stopped = true; clearInterval(timer); show(+b.dataset.tshot); }));
  new IntersectionObserver(([e]) => {
    clearInterval(timer);
    if (e.isIntersecting && !stopped && motion) timer = setInterval(() => show((cur + 1) % shots.length), 3500);
  }, { threshold: 0.4 }).observe($(".tablet"));

  // ---------- forms (waitlist: diners and restaurants) ----------
  const cfg = window.FIG_CONFIG || {};
  const src = new URLSearchParams(location.search).get("src") || (location.pathname.startsWith("/owners") ? "owners" : "site");
  $$("form.join").forEach((form) => {
    const msg = $(".form-msg", form), btn = $("button[type=submit]", form);
    const say = (t, kind) => { msg.textContent = t; msg.className = "form-msg " + (kind || ""); };
    form.addEventListener("input", (e) => e.target.removeAttribute("aria-invalid"));
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      if (form.elements.website.value) return; // bots fill the hidden field
      const role = form.dataset.role;
      const restaurant = role === "restaurant" ? form.elements.restaurant.value.trim() : null;
      if (role === "restaurant" && !restaurant) { form.elements.restaurant.setAttribute("aria-invalid", "true"); form.elements.restaurant.focus(); return say("Add your restaurant's name.", "err"); }
      const who = parseContact(form.elements.contact.value);
      if (!who) { form.elements.contact.setAttribute("aria-invalid", "true"); form.elements.contact.focus(); return say("Enter an email, or a 10-digit mobile number.", "err"); }
      if (!form.elements.consent.checked) return say("Tick the box so we're allowed to message you.", "err");
      if (!cfg.supabaseUrl || !cfg.supabaseKey) return say("Sign-ups open in the next few days. Check back soon!", "err");
      btn.disabled = true; say("");
      try {
        const r = await fetch(`${cfg.supabaseUrl}/rest/v1/waitlist`, { method: "POST",
          headers: { apikey: cfg.supabaseKey, "Content-Type": "application/json", Prefer: "return=minimal" },
          body: JSON.stringify({ role, ...who, restaurant, consent: true, source: src.slice(0, 60) }) });
        if (!r.ok && r.status !== 409) throw new Error(r.status);
        form.querySelectorAll("input, button, .consent").forEach((el) => (el.disabled = true));
        say(role === "restaurant" ? `Thanks! We'll reach out to set up ${restaurant}.` : "You're on the list. We'll message you the day FIG opens in Markham.", "ok");
      } catch (e) {
        btn.disabled = false; say("Something went wrong. Try again in a moment.", "err");
      }
    });
  });

  // figpromo.com/owners: the link to open on your phone when you walk into a restaurant
  if (location.pathname.startsWith("/owners")) {
    selectTab("restaurant"); chatStarted = true;
    setTimeout(() => $("#owners").scrollIntoView(), 300);
  }
})();
