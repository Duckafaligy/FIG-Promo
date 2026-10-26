// Home life (2026-10-26): numbers count up, the code countdown ticks, and the app recordings load only when they are on screen.
// Everything here is skipped with reduced motion (the drawn screens and the final numbers just sit there).
(() => {
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;
  // count up
  const nums = $$("[data-count]");
  if (nums.length && !calm && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return; io.unobserve(e.target);
      const el = e.target, end = +el.dataset.count, pre = el.dataset.pre || "", suf = el.dataset.suf || "", t0 = performance.now();
      const step = (t) => { const k = Math.min(1, (t - t0) / 1200); el.textContent = pre + Math.round(end * (1 - Math.pow(1 - k, 3))) + suf; if (k < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }), { threshold: 0.6 });
    nums.forEach((n) => io.observe(n));
  }
  // the QR countdown (4:32 and down); it loops back to 5:00 so it never reads 0:00
  const cds = $$(".mk-cd[data-cd]");
  if (cds.length && !calm) {
    const left = cds.map((c) => +c.dataset.cd);
    setInterval(() => {
      if (root.classList.contains("paused") || document.hidden) return;
      cds.forEach((c, i) => { left[i] = left[i] > 1 ? left[i] - 1 : 299; const m = Math.floor(left[i] / 60), s = left[i] % 60; c.textContent = m + ":" + String(s).padStart(2, "0"); });
    }, 1000);
  }
  // recordings: names listed here exist in /assets/clips as <name>.webm, <name>.mp4 and <name>-poster.webp. Empty until they are copied in.
  const LOOPS = [];
  const slots = $$(".mk-scr[data-loop]").filter((s) => LOOPS.includes(s.dataset.loop));
  if (slots.length && !calm && "IntersectionObserver" in window) {
    const vio = new IntersectionObserver((es) => es.forEach((e) => {
      const scr = e.target; let v = scr.querySelector("video.mk-vid");
      if (e.isIntersecting && !v) {
        const n = scr.dataset.loop; v = document.createElement("video");
        v.className = "mk-vid"; v.muted = true; v.loop = true; v.playsInline = true; v.preload = "none"; v.poster = `/assets/clips/${n}-poster.webp`;
        v.innerHTML = `<source src="/assets/clips/${n}.webm" type="video/webm"><source src="/assets/clips/${n}.mp4" type="video/mp4">`;
        v.addEventListener("canplay", () => scr.classList.add("has-vid"), { once: true });
        v.addEventListener("error", () => v.remove(), { once: true }); scr.appendChild(v);
      }
      if (v) { if (e.isIntersecting && !root.classList.contains("paused")) v.play().catch(() => {}); else v.pause(); }
    }), { threshold: 0.25 });
    slots.forEach((s) => vio.observe(s));
  }
})();
