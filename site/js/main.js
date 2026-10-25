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
    ScrollTrigger.batch(".reveal", { start: "top 88%", once: true,
      onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out", stagger: 0.08, overwrite: true }) });
    root.classList.add("reveal-on"); // the reveals above are set up: the CSS fallback (site.css) for a script that never gets here stands down
  }



  // ---------- chats: a diner and the restaurant texting, 3-5 s per message ----------
  (() => {
    const body = $("#cp-body"), input = $("#cp-input"), send = $("#cp-send");
    if (!body) return; // the chat section is hidden for launch (2026-10-17)
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

  // ---------- bento cells: spotlight (opening them is in fx.js) ----------
  $$(".cell").forEach((c) => {
    c.addEventListener("pointermove", (e) => { const r = c.getBoundingClientRect(); c.style.setProperty("--cx", e.clientX - r.left + "px"); c.style.setProperty("--cy", e.clientY - r.top + "px"); });
  });

  // ---------- video loops: loaded a screen and a half ahead, playing while on screen ----------
  // (user 2026-10-14: they start on their own, already moving when you get there; the play button is only for a phone
  // that refuses autoplay.) On a phone the bento row scrolls sideways, where a look-ahead can't see: each loop that's
  // near or playing also loads the next card's. Data Saver: each loads only when it's on screen, as before.
  // reduced motion (FIX-LIST #154): no Home video loads or plays by itself; each shows its poster (the tutorial can still be
  // played with its own controls, and only then is its file fetched)
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const ahead = !(navigator.connection && navigator.connection.saveData);
  const load = (v) => { if (v && !v.src) { v.preload = "auto"; v.src = v.dataset.src; } };
  const next = (v) => v.closest(".cell")?.nextElementSibling?.querySelector("video[data-src]");
  const lio = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    load(e.target); load(next(e.target)); lio.unobserve(e.target);
  }), { rootMargin: "150% 0px" });
  const vio = new IntersectionObserver((es) => es.forEach((e) => {
    const v = e.target;
    if (e.isIntersecting) {
      load(v); if (ahead) load(next(v));
      figPlay(v);
    } else v.pause();
  }), { threshold: 0.1 });
  if (!still) $$("video[data-src]").forEach((v) => { vio.observe(v); if (ahead) lio.observe(v); });
  // "Good to know" loops (FIX-LIST #145): each loads only once its card is on screen, plays while it is, pauses off it;
  // with reduced motion only the poster shows
  if (!still) {
    const gio = new IntersectionObserver((es) => es.forEach((e) => {
      const v = e.target;
      if (!e.isIntersecting) return v.pause();
      if (root.classList.contains("paused")) return; // "Pause animations" is on
      if (!v.src) v.src = v.dataset.loop;
      v.play().catch(() => {}); // refused (Low Power Mode, data saver): the poster stays
    }), { threshold: 0.25 });
    $$("video.gtk-loop").forEach((v) => gio.observe(v));
  }
  // ---------- Pause animations (FIX-LIST #149, WCAG 2.2.2): one button stops every loop on Home for the visit ----------
  // (the head script sets html.paused from the tab's memory before anything plays; the CSS stops the endless CSS loops,
  // figPlay and the loops above won't start a video while it's on, and the map's drift stays still)
  const mt = $(".motion-toggle");
  if (mt) {
    const onScreen = (v) => { const r = v.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight && r.width > 0; };
    const set = (p) => {
      root.classList.toggle("paused", p);
      mt.setAttribute("aria-pressed", String(p));
      try { sessionStorage.setItem("fig.paused", p ? "1" : "0"); } catch {}
      $$("video").forEach((v) => {
        if (p) { v.pause(); if (v.readyState) v.currentTime = 0; } // back to the start, as still as its poster
        else if (onScreen(v)) { // on again: what's on screen plays (loading it first if it came into view while paused)
          if (still) return; // reduced motion: nothing loads or plays by itself (#154)
          if (!v.src && (v.dataset.loop || v.dataset.src)) v.src = v.dataset.loop || v.dataset.src;
          if (v.src) v.classList.contains("gtk-loop") ? v.play().catch(() => {}) : figPlay(v);
        }
      });
    };
    mt.addEventListener("click", () => set(!root.classList.contains("paused")));
    if (root.classList.contains("paused")) set(true);
  }
  // posters too: fetched only when a video is about a screen away (they were ~300 KB on first load)
  const pio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.poster = e.target.dataset.poster; pio.unobserve(e.target); } }), { rootMargin: "800px 0px" });
  $$("video[data-poster]").forEach((v) => pio.observe(v));


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
      if (still) { tutVideo.preload = "none"; tutVideo.controls = true; } // reduced motion: the poster, and play only if they choose to
      if (!tutVideo.src.endsWith(`/tut-${tab}.mp4`)) tutVideo.src = `/assets/clips/tut-${tab}.mp4`; // the look-ahead may have loaded it
      tutVideo.defaultPlaybackRate = tutVideo.playbackRate = 1.35; // a little quicker than the full-length video
      if (!still) figPlay(tutVideo);
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
  // loaded a screen and a half ahead, like the loops (the diner's side is the one that shows first)
  if (ahead && !still) { const tio = new IntersectionObserver(([e]) => { if (e.isIntersecting && !tutVideo.src) { tutVideo.preload = "auto"; tutVideo.src = "/assets/clips/tut-diner.mp4"; tio.disconnect(); } }, { rootMargin: "150% 0px" }); tio.observe(tutVideo); }
  new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return tutVideo.pause();
    if (!tutRole) selectTab("diner"); else if (!still) figPlay(tutVideo);
  }, { threshold: 0.3 }).observe(tutVideo);

  // ---------- restaurant tablet: steps itself while visible, until tapped ----------
  const shots = $$(".tablet .mk-tab-scr"), tabs = $$("[data-tshot]");
  let cur = 0, timer = null, stopped = false;
  function show(i) { cur = i; shots.forEach((s, k) => s.classList.toggle("on", k === i)); tabs.forEach((b, k) => b.setAttribute("aria-selected", String(k === i))); }
  tabs.forEach((b) => b.addEventListener("click", () => { stopped = true; clearInterval(timer); show(+b.dataset.tshot); }));
  new IntersectionObserver(([e]) => {
    clearInterval(timer);
    if (e.isIntersecting && !stopped && motion) timer = setInterval(() => show((cur + 1) % shots.length), 3500);
  }, { threshold: 0.4 }).observe($(".tablet"));

  // ---------- the diner waitlist (2026-10-15: restaurants first, diners join January 1, 2027) ----------
  const cfg = window.FIG_CONFIG || {};
  const rpc = (fn, body) => fetch(`${cfg.supabaseUrl}/rest/v1/rpc/${fn}`, { method: "POST",
    headers: { apikey: cfg.supabaseKey, "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
  // a creator's link (?src=name, 2026-10-17): kept for this tab so the waitlist form can say who sent them (first one wins)
  try {
    const src = (new URLSearchParams(location.search).get("src") || "").toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 40);
    if (src && !sessionStorage.getItem("fig.src")) sessionStorage.setItem("fig.src", src);
  } catch {}
  const wl = $("#waitlist form");
  if (wl) {
    const msg = $(".form-msg", wl), btn = $("button[type=submit]", wl), email = wl.elements.email;
    const say = (t, kind) => { msg.textContent = t; msg.className = "form-msg " + (kind || ""); };
    // the count only shows once it's worth showing
    // the opening line (the user's words, 2026-10-17): the date and the order from site_mode; the HTML has a true fallback.
    // An order, never exclusivity.
    rpc("site_mode").then((r) => r.ok && r.json()).then((m) => {
      if (!m) return;
      // open to everyone and no launch date still ahead: nothing left to announce (FIX-LIST #56)
      if ((m.mode || (m.diners_open ? "on" : "off")) === "on" && !(m.opens_at && new Date(m.opens_at) > new Date())) { $(".wl-count", wl).hidden = true; return; }
      let when = "FIG opens in Markham on January 1, 2027."; // no date set yet: the date the site gives everywhere (FIX-LIST #137)
      try { if (m.opens_at) when = `FIG opens in Markham on ${new Date(m.opens_at).toLocaleDateString("en-US", { timeZone: "America/Toronto", month: "long", day: "numeric", year: "numeric" })}.`; } catch {}
      const line = $(".wl-line", wl);
      if (line) line.textContent = `${when} ${m.founding_cap && m.mode === "waitlist" ? `The first ${Number(m.founding_cap).toLocaleString("en-CA")} on the list get in first.` : "The first members get in first."}`;
      if (m.waitlist >= 25) $(".wl-count", wl).append(` ${m.waitlist.toLocaleString("en-CA")} people are already waiting.`);
    }).catch(() => {});
    email.addEventListener("input", () => email.removeAttribute("aria-invalid"));
    // joining needs the email consent (FIX-LIST #103): Join stays off until the box is ticked (the database refuses without it too)
    const ok = () => { btn.disabled = !wl.elements.consent.checked; };
    wl.elements.consent.addEventListener("change", ok); ok();
    addEventListener("pageshow", ok); // back/forward restores a ticked box: Join follows it
    wl.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      if (wl.elements.website.value) return; // bots fill the hidden field
      // an empty field and a mistyped one get their own words (FIX-LIST #136)
      if (!email.value.trim() || !email.checkValidity()) { email.setAttribute("aria-invalid", "true"); email.focus(); return say(email.value.trim() ? "That email doesn't look right." : "Enter your email.", "err"); }
      btn.disabled = true; say("");
      try {
        let src = ""; try { src = sessionStorage.getItem("fig.src") || ""; } catch {}
        const r = await rpc("join_waitlist", { p_email: email.value.trim(), p_consent: wl.elements.consent.checked, ...(src ? { p_source: src } : {}) });
        if (!r.ok) throw new Error(await r.text());
        const said = await r.json().catch(() => "ok");
        wl.querySelectorAll("input, button").forEach((el) => (el.disabled = true));
        // founding members (2026-10-17): after the founding list closed the answer is 'ok-late', the same for any email
        if (said === "ok-late") {
          say("You're on the list. Check your email and tap the link to confirm. Founding members are in now; we'll let you in at the public launch. Already a founding member? ", "ok");
          const a = document.createElement("a"); a.href = "/app/sign-in"; a.textContent = "Sign in"; msg.appendChild(a);
        } else say("You're on the list. Check your email and tap the link to confirm; then we'll email you the day FIG opens.", "ok");
      } catch (e) {
        btn.disabled = false;
        // no answer at all (fetch throws a TypeError) is the connection, not FIG
        btn.disabled = !wl.elements.consent.checked;
        say(/too-many/.test(e.message) ? "Too many tries. Try again in 15 minutes." : /bad-email/.test(e.message) ? "That email doesn't look right." : /consent-needed/.test(e.message) ? "Tick the box to agree to emails from FIG, then join." : e instanceof TypeError || !navigator.onLine ? "You seem to be offline. Check your connection and try again." : "Something went wrong. Try again in a moment.", "err");
      }
    });
  }

  // figpromo.com/owners: the link to open on your phone when you walk into a restaurant
  if (location.pathname.startsWith("/owners")) {
    selectTab("restaurant");
    setTimeout(() => $("#owners").scrollIntoView(), 300);
  }
})();


// numbers strip: count up when it scrolls into view (226 places, 4 languages)
(() => {
  const nums = [...document.querySelectorAll(".stats b")].filter((b) => /^\d+$/.test(b.textContent.trim()) && +b.textContent > 1);
  if (!nums.length || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return; io.unobserve(e.target);
    const el = e.target, end = +el.textContent, t0 = performance.now();
    const step = (t) => { const k = Math.min(1, (t - t0) / 1400); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); };
    el.textContent = "0"; requestAnimationFrame(step);
  }), { threshold: 0.6 });
  nums.forEach((n) => io.observe(n));
})();
