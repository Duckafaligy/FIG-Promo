// Shared micro-interactions on every page: sliding tab pill, press ripples, scroll reveals on inner pages.
(() => {
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // video loops: phones in Low Power Mode or data saver refuse to autoplay, so retry on the first touch
  const blocked = new Set();
  window.figPlay = (v) => {
    v.muted = true; v.playsInline = true; v.autoplay = true;
    const p = v.play();
    if (p) p.then(() => blocked.delete(v)).catch(() => blocked.add(v));
  };
  const retry = () => blocked.forEach((v) => {
    const r = v.getBoundingClientRect();
    if (r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth) window.figPlay(v);
  });
  ["touchend", "click", "keydown"].forEach((t) => document.addEventListener(t, retry, { capture: true, passive: true }));

  // tab groups: one pill slides to whichever tab is selected
  $$(".seg").forEach((seg) => {
    const pill = document.createElement("span");
    pill.className = "seg-pill";
    seg.prepend(pill);
    const place = () => {
      const b = seg.querySelector('[aria-selected="true"]');
      if (!b) return;
      const l = b.offsetLeft - 4, r = seg.clientWidth - 8 - l - b.offsetWidth;
      pill.style.clipPath = `inset(0 ${r}px 0 ${l}px round 999px)`;
    };
    new MutationObserver(place).observe(seg, { subtree: true, attributeFilter: ["aria-selected"] });
    addEventListener("resize", place);
    document.fonts.ready.then(() => { place(); requestAnimationFrame(() => seg.classList.add("pill-on")); });
    place();
  });

  // phones and tablets: the menu button opens the section links
  const nav = document.getElementById("nav"), menu = nav && nav.querySelector(".nav-menu");
  if (menu) {
    const set = (open) => { nav.classList.toggle("open", open); menu.setAttribute("aria-expanded", String(open)); };
    menu.addEventListener("click", () => set(!nav.classList.contains("open")));
    $$(".nav-sheet a", nav).forEach((a) => a.addEventListener("click", () => set(false)));
    document.addEventListener("click", (e) => { if (!nav.contains(e.target)) set(false); });
  }

  // phones: steps and feature boxes are swipe rows, with dots that follow along
  if (matchMedia("(max-width: 719px)").matches) $$(".steps, .bento").forEach((row) => {
    const kids = [...row.children];
    if (kids.length < 2) return;
    const dots = document.createElement("div");
    dots.className = "swipe-dots";
    dots.setAttribute("aria-hidden", "true");
    dots.innerHTML = kids.map(() => "<i></i>").join("");
    row.after(dots);
    const mark = () => {
      const i = Math.round(row.scrollLeft / (kids[1].offsetLeft - kids[0].offsetLeft));
      [...dots.children].forEach((d, k) => d.classList.toggle("on", k === i));
    };
    row.addEventListener("scroll", mark, { passive: true });
    mark();
  });

  if (still) return;

  // press ripple from the exact point you tapped
  document.addEventListener("pointerdown", (e) => {
    const el = e.target.closest(".btn, .dl, .seg button, .pp-replay, .card-l, .post-card, .tsteps li, .faq summary");
    if (!el) return;
    const r = el.getBoundingClientRect(), d = Math.max(r.width, r.height) * 2.2;
    const dot = document.createElement("span");
    dot.className = "ripple";
    dot.style.cssText = `width:${d}px;height:${d}px;left:${e.clientX - r.left - d / 2}px;top:${e.clientY - r.top - d / 2}px`;
    el.appendChild(dot);
    dot.animate([{ transform: "scale(0)", opacity: 0.32 }, { transform: "scale(1)", opacity: 0 }], { duration: 650, easing: "cubic-bezier(.2,.8,.3,1)" }).onfinish = () => dot.remove();
  });

  // inner pages: blocks rise in as they scroll into view (the home page does this with GSAP)
  if (!document.body.classList.contains("sub")) return;
  const els = $$(".reveal, .doc > *, .page-hero .wrap > *, .cell, .card-l, .post-card, .faq details, .tsteps li, .sitemap > div, .perks li, .tablet-wrap, .plan");
  els.forEach((el) => el.classList.add("rv"));
  const io = new IntersectionObserver((es) => {
    es.filter((e) => e.isIntersecting).forEach((e, i) => {
      const el = e.target;
      io.unobserve(el);
      el.style.transitionDelay = i * 70 + "ms";
      el.classList.add("in");
      setTimeout(() => { el.classList.remove("rv", "in"); el.style.transitionDelay = ""; }, 1100 + i * 70); // hand hover transitions back
    });
  }, { rootMargin: "0px 0px -8% 0px" });
  els.forEach((el) => io.observe(el));
})();

// "Sign up free" goes to the right store for the phone you're on
if (/android/i.test(navigator.userAgent)) document.querySelectorAll("[data-get-app]").forEach((a) => (a.href = "https://play.google.com/store/apps"));
