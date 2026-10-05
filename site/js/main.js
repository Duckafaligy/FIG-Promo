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
  ["how", "features", "passport", "catch", "owners"].forEach((id) => { const s = document.getElementById(id); if (s) io.observe(s); });

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
  }


  // ---------- passport: stamps fill to 50, then confetti and the reward ----------
  (() => {
    const card = $("#pp"), num = $("#pp-num"), bar = $("#pp-bar"), box = $("#pp-stamps"), unlock = $("#pp-unlock");
    const rungs = $$(".rung"), pins = window.FIG_PINS || [];
    const C = 553; // ring circumference
    const label = (r, t) => { r.querySelector(".state").textContent = t; };
    const fire = window.confetti && confetti.create($("#pp-confetti"), { resize: true, useWorker: true });
    function reset() {
      num.textContent = "0"; bar.style.strokeDashoffset = C; box.innerHTML = "";
      rungs.forEach((r) => { r.classList.remove("hit"); label(r, "Locked"); });
      card.classList.remove("done");
      if (motion) gsap.set(unlock, { opacity: 0, y: 30, scale: 0.96 });
    }
    function final() {
      num.textContent = "50"; bar.style.strokeDashoffset = 0;
      box.innerHTML = pins.slice(0, 10).map((p) => `<span><img src="${p}" alt=""></span>`).join("");
      rungs[0].classList.add("hit"); label(rungs[0], "Claim");
      rungs[1].classList.add("hit"); label(rungs[1], "Unlocked");
      label(rungs[2], "50 to go");
      unlock.style.opacity = 1; unlock.style.transform = "none";
    }
    function play() {
      if (!motion) return final();
      reset();
      let shown = 0;
      const o = { v: 0 };
      const tl = gsap.timeline();
      tl.to(o, { v: 50, duration: 3.6, ease: "power1.inOut", onUpdate() {
        const v = Math.round(o.v);
        num.textContent = v;
        bar.style.strokeDashoffset = C * (1 - o.v / 50);
        while (shown < Math.floor(o.v / 5)) {
          const s = document.createElement("span");
          s.innerHTML = `<img src="${pins[shown % pins.length]}" alt="">`;
          box.appendChild(s);
          gsap.from(s, { scale: 0.2, rotate: -30, opacity: 0, duration: 0.45, ease: "back.out(2.6)" });
          shown++;
        }
        if (v >= 25 && !rungs[0].classList.contains("hit")) { rungs[0].classList.add("hit"); label(rungs[0], "Claim"); }
      } });
      tl.add(() => {
        rungs[1].classList.add("hit"); label(rungs[1], "Unlocked"); label(rungs[2], "50 to go");
        if (fire) {
          fire({ particleCount: 140, spread: 80, startVelocity: 42, origin: { x: 0.3, y: 0.45 }, colors: ["#1E5EFF", "#C8F135", "#14C86B", "#6E56FF", "#FFFFFF"] });
          setTimeout(() => fire({ particleCount: 90, spread: 110, startVelocity: 30, origin: { x: 0.7, y: 0.4 }, colors: ["#1E5EFF", "#C8F135", "#FFFFFF"] }), 220);
        }
      });
      tl.to(unlock, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "back.out(1.8)" }, "+=0.15");
      tl.add(() => card.classList.add("done"), "+=0.4");
    }
    $("#pp-replay").addEventListener("click", play);
    if (!motion) return final();
    reset();
    ScrollTrigger.create({ trigger: card, start: "top 70%", once: true, onEnter: play });
  })();

  // ---------- chats: a diner and the restaurant texting, 3-5 s per message ----------
  (() => {
    const body = $("#cp-body"), input = $("#cp-input"), send = $("#cp-send");
    const PH = "Message Golden Lantern";
    const CONVO = [
      ["d", "Hi! Is the 2-for-1 dim sum still on tonight?"],
      ["r", "Hi! Yes, it runs until 9 pm tonight."],
      ["d", "Amazing. We're a table of 4, around 7?"],
      ["r", "Perfect, we'll have a table for 4 ready at 7."],
      ["d", "Can each of us use the deal?"],
      ["r", "Yes, it's one per person per day, so everyone can claim it."],
      ["d", "Nice. Is it dine-in only?"],
      ["r", "Dine-in only for this one."],
      ["d", "Got it. Anything spicy you'd recommend?"],
      ["r", "Our chili wontons are a favourite. Not part of the deal, but worth it."],
      ["d", "Haha sold. Do we just show the code at the counter?"],
      ["r", "Yes, open your deal and show the QR when you order. We'll scan it."],
      ["d", "Perfect, see you at 7!"],
      ["r", "See you soon!"],
    ];
    let visible = false;
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    const whenVisible = async () => { while (!visible) await wait(400); };
    const gap = () => 1700 + Math.random() * 1100;
    function add(cls, html) {
      const b = document.createElement("div"); b.className = cls; b.innerHTML = html;
      body.appendChild(b);
      while (body.querySelectorAll(".bub").length > 12) body.querySelector(".bub").remove();
      return b;
    }
    const esc = (t) => t.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
    async function say(side, text) {
      const t0 = performance.now(), total = gap();
      if (side === "r") {
        await wait(400);
        const dots = add("bub a typing bub-in", "<i></i><i></i><i></i>");
        await wait(Math.min(total - 500, 700 + text.length * 12));
        dots.remove();
        add("bub a bub-in", esc(text));
      } else {
        input.classList.add("typing"); send.classList.add("on");
        for (let k = 1; k <= text.length; k++) { input.textContent = text.slice(0, k); await wait(18); }
        await wait(150);
        add("bub q bub-in", esc(text));
        input.textContent = PH; input.classList.remove("typing"); send.classList.remove("on");
      }
      await wait(Math.max(300, total - (performance.now() - t0)));
    }
    async function loop() {
      for (;;) {
        for (const [side, text] of CONVO) { await whenVisible(); await say(side, text); }
        await wait(4000);
        body.querySelectorAll(".bub").forEach((b) => b.remove());
      }
    }
    if (!motion) { CONVO.slice(-6).forEach(([side, text]) => add(`bub ${side === "d" ? "q" : "a"}`, esc(text))); return; }
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { threshold: 0.3 }).observe($(".chatphone"));
    loop();
  })();

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


  // ---------- what's the catch: the tutorial video (diner or restaurant), nothing else ----------
  const tutVideo = $("#tut-video");
  let tutRole = "";
  function selectTab(tab) {
    $$("#catch [data-tab]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === tab)));
    if (tab === tutRole) return;
    const first = !tutRole;
    tutRole = tab;
    const load = () => {
      $(".tutwrap").dataset.role = tab;
      tutVideo.poster = `/assets/clips/tut-${tab}.jpg`;
      tutVideo.src = `/assets/clips/tut-${tab}.mp4`;
      tutVideo.defaultPlaybackRate = tutVideo.playbackRate = 1.35; // a little quicker than the full-length video
      tutVideo.play().catch(() => {});
    };
    if (first || !root.classList.contains("motion")) return load();
    // switching point of view: the card flips over and comes back as the other side
    const card = $("#tut"), dir = tab === "restaurant" ? 1 : -1;
    card.getAnimations().forEach((a) => a.cancel());
    card.animate([{ transform: "perspective(1400px) rotateY(0) scale(1)" }, { transform: `perspective(1400px) rotateY(${dir * 90}deg) scale(.9)`, opacity: 0.6 }],
      { duration: 260, easing: "cubic-bezier(.55,0,.8,.2)" }).finished.then(() => {
      load();
      card.animate([{ transform: `perspective(1400px) rotateY(${-dir * 90}deg) scale(.9)`, opacity: 0.6 }, { transform: "perspective(1400px) rotateY(0) scale(1)", opacity: 1 }],
        { duration: 520, easing: "cubic-bezier(.2,1.25,.4,1)" });
      $(".tut-label span").animate([{ transform: "scale(1)" }, { transform: "scale(1.12) rotate(-3deg)" }, { transform: "scale(1)" }], { duration: 420, easing: "ease-out" });
    }).catch(() => {});
  }
  $$("#catch [data-tab]").forEach((b) => b.addEventListener("click", () => selectTab(b.dataset.tab)));
  new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return tutVideo.pause();
    if (!tutRole) selectTab("diner"); else tutVideo.play().catch(() => {});
  }, { threshold: 0.3 }).observe(tutVideo);

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
    selectTab("restaurant");
    setTimeout(() => $("#owners").scrollIntoView(), 300);
  }
})();
