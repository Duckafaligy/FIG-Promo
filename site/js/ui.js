// Home life: numbers count up, and the app recordings play (2026-10-26).
// A recording goes into its phone as soon as the page starts (the hero and the first phones) or 800 px before it scrolls into view.
// It plays while near the screen and pauses when far away. If it has not moved 2 s after it should be playing (some browsers hold
// back autoplay), the phone swaps to an animated picture made from the same clip. The drawn screen only shows where no clip exists.
// A tap or Enter on a clip opens it larger in a dialog with controls. Reduced motion: the first frame (poster) only.
(() => {
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;
  const LOOPS = ["d1", "d2", "d3", "d4", "d5", "r1", "r2", "r3", "r4", "r5", "r6", "r7"];
  const canWebm = !!document.createElement("video").canPlayType("video/webm");

  // count up (the final number is already in the page; this only animates it)
  const nums = $$("[data-count]");
  if (nums.length && !calm && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return; io.unobserve(e.target);
      const el = e.target, end = +el.dataset.count, t0 = performance.now();
      const step = (t) => { const k = Math.min(1, (t - t0) / 1100); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); else el.textContent = end; };
      requestAnimationFrame(step);
    }), { threshold: 0.6 });
    nums.forEach((n) => io.observe(n));
  }

  // recordings
  const slots = $$(".mk-scr[data-loop]").filter((s) => LOOPS.includes(s.dataset.loop));
  const make = (scr, eager) => {
    const n = scr.dataset.loop, v = document.createElement("video");
    v.className = "mk-vid"; v.muted = true; v.defaultMuted = true; v.loop = true; v.playsInline = true; v.autoplay = !calm; v.disablePictureInPicture = true;
    v.setAttribute("muted", ""); v.setAttribute("playsinline", ""); v.setAttribute("width", "390"); v.setAttribute("height", "844");
    v.preload = eager ? "auto" : "metadata"; v.poster = `/assets/clips/${n}-poster.webp`;
    v.innerHTML = (canWebm ? `<source src="/assets/clips/${n}.webm" type="video/webm">` : "") + `<source src="/assets/clips/${n}.mp4" type="video/mp4">`;
    if (scr.closest(".step, .bento")) v.addEventListener("loadedmetadata", () => { v.defaultPlaybackRate = v.playbackRate = 1.25; });
    const show = () => scr.classList.add("has-vid"); v.addEventListener("loadeddata", show, { once: true }); v.addEventListener("playing", show, { once: true }); if (v.readyState >= 2) show();
    scr.appendChild(v); return v;
  };
  const fallback = (scr, v) => {
    if (scr.dataset.anim) return; scr.dataset.anim = "1"; v.pause();
    const img = new Image(); img.className = "mk-vid mk-anim"; img.alt = ""; img.width = 390; img.height = 844; img.decoding = "async";
    img.addEventListener("load", () => scr.classList.add("has-vid"), { once: true }); img.src = `/assets/clips/anim/${scr.dataset.loop}.webp`; v.replaceWith(img);
  };
  const state = new WeakMap();
  const play = (scr, v) => {
    if (!v || calm || root.classList.contains("paused")) return;
    const p = v.play(); if (p && p.catch) p.catch(() => {});
    const s = state.get(scr) || {}; if (s.dog) return;
    const t0 = v.currentTime; state.set(scr, { ...s, dog: setTimeout(() => { state.set(scr, { ...state.get(scr), dog: 0 }); if (!scr.dataset.anim && v.isConnected && !v.paused && v.currentTime === t0) fallback(scr, v); else if (!scr.dataset.anim && v.isConnected && v.paused && !root.classList.contains("paused")) fallback(scr, v); }, 2200) });
  };
  if (slots.length) {
    slots.forEach((scr) => { if (!calm && scr.closest(".hp-cycle, .step") && !scr.querySelector("video")) make(scr, true); }); // the rest are made when they come near (below)
    if ("IntersectionObserver" in window) {
      const near = new IntersectionObserver((es) => es.forEach((e) => {
        const scr = e.target; let v = scr.querySelector("video.mk-vid");
        if (!v && !scr.dataset.anim && e.isIntersecting && !calm) v = make(scr, true);
        if (!v) return;
        if (e.isIntersecting) { if (v.preload !== "auto") v.preload = "auto"; play(scr, v); } else v.pause();
      }), { rootMargin: "800px 0px 800px 0px", threshold: 0 });
      slots.forEach((s) => near.observe(s));
    } else slots.forEach((s) => play(s, s.querySelector("video")));
    // "Pause animations" / back to the tab
    document.addEventListener("visibilitychange", () => { if (!document.hidden) slots.forEach((s) => { const v = s.querySelector("video.mk-vid"); if (v && v.getBoundingClientRect().top < innerHeight + 800 && v.getBoundingClientRect().bottom > -800) play(s, v); }); });
    // a click or Enter opens the clip larger
    let box = null;
    const open = (scr) => {
      if (!box) {
        box = document.createElement("dialog"); box.className = "vbox"; box.setAttribute("aria-label", "App recording");
        box.innerHTML = '<button type="button" class="vbox-x" aria-label="Close">&times;</button><video muted loop playsinline controls preload="auto"></video>';
        document.body.appendChild(box);
        const close = () => { const bv = box.querySelector("video"); bv.pause(); box.close(); };
        box.querySelector(".vbox-x").addEventListener("click", close);
        box.addEventListener("click", (ev) => { if (ev.target === box) close(); });
        box.addEventListener("close", () => { const bv = box.querySelector("video"); bv.pause(); if (box._from) box._from.focus(); });
      }
      const n = scr.dataset.loop, bv = box.querySelector("video"); box._from = scr;
      bv.poster = `/assets/clips/${n}-poster.webp`; bv.muted = true;
      bv.innerHTML = (canWebm ? `<source src="/assets/clips/${n}.webm" type="video/webm">` : "") + `<source src="/assets/clips/${n}.mp4" type="video/mp4">`; bv.load();
      if (!box.open) box.showModal(); const p = bv.play(); if (p && p.catch) p.catch(() => {});
      box.querySelector(".vbox-x").focus();
    };
    if (typeof HTMLDialogElement !== "undefined") slots.forEach((scr) => {
      scr.tabIndex = 0; scr.setAttribute("role", "button"); scr.style.cursor = "zoom-in";
      scr.setAttribute("aria-label", "Open this recording larger: " + (scr.closest("[role=img]") ? scr.closest("[role=img]").getAttribute("aria-label") : "app screen"));
      scr.addEventListener("click", () => open(scr));
      scr.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(scr); } });
    });
  }
})();
