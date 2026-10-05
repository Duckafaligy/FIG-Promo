// Shared micro-interactions on every page: sliding tab pill, press ripples, scroll reveals on inner pages.
(() => {
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // tab groups: one pill slides to whichever tab is selected
  $$(".seg").forEach((seg) => {
    const pill = document.createElement("span");
    pill.className = "seg-pill";
    seg.prepend(pill);
    const place = () => {
      const b = seg.querySelector('[aria-selected="true"]');
      if (!b) return;
      pill.style.width = b.offsetWidth + "px";
      pill.style.transform = `translateX(${b.offsetLeft - 4}px)`;
    };
    new MutationObserver(place).observe(seg, { subtree: true, attributeFilter: ["aria-selected"] });
    addEventListener("resize", place);
    document.fonts.ready.then(() => { place(); requestAnimationFrame(() => seg.classList.add("pill-on")); });
    place();
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
