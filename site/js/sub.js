// Inner pages: navbar shadow, video loops that play only on screen, tap-to-open boxes on touch, tablet tabs.
(() => {
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const nav = document.getElementById("nav");
  const onScroll = () => nav && nav.classList.toggle("scrolled", scrollY > 30);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  const io = new IntersectionObserver((es) => es.forEach((e) => {
    const v = e.target;
    if (!e.isIntersecting) return v.pause();
    if (!v.getAttribute("src")) v.src = v.dataset.src;
    if (v.dataset.rate) v.defaultPlaybackRate = v.playbackRate = +v.dataset.rate;
    figPlay(v);
  }), { threshold: 0.35 });
  $$("video[data-src]").forEach((v) => io.observe(v));

  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  $$(".cell").forEach((c) => {
    c.addEventListener("pointermove", (ev) => { const r = c.getBoundingClientRect(); c.style.setProperty("--cx", ev.clientX - r.left + "px"); c.style.setProperty("--cy", ev.clientY - r.top + "px"); });
    if (!fine) c.addEventListener("click", () => c.classList.toggle("open"));
  });

  const shots = $$(".tablet img"), tabs = $$("[data-tshot]");
  tabs.forEach((b) => b.addEventListener("click", () => {
    const i = +b.dataset.tshot;
    shots.forEach((s, k) => s.classList.toggle("on", k === i));
    tabs.forEach((t, k) => t.setAttribute("aria-selected", String(k === i)));
  }));
})();

// blog: topic filter and share button
document.querySelectorAll("[data-topic]").forEach((b) => b.tagName === "BUTTON" && b.addEventListener("click", () => {
  document.querySelectorAll(".blog-filter button").forEach((x) => x.setAttribute("aria-selected", String(x === b)));
  document.querySelectorAll(".post-card").forEach((c) => (c.hidden = b.dataset.topic !== "All" && c.dataset.topic !== b.dataset.topic));
}));
document.querySelectorAll("[data-share]").forEach((b) => b.addEventListener("click", async () => {
  const data = { title: document.title, url: location.href };
  try {
    if (navigator.share) return await navigator.share(data);
    await navigator.clipboard.writeText(location.href);
    b.querySelector("span").textContent = "Link copied";
  } catch {}
}));
