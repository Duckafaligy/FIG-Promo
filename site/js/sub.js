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

  $$(".cell").forEach((c) => {
    c.addEventListener("pointermove", (ev) => { const r = c.getBoundingClientRect(); c.style.setProperty("--cx", ev.clientX - r.left + "px"); c.style.setProperty("--cy", ev.clientY - r.top + "px"); });
  });

  const shots = $$(".tablet .mk-tab-scr"), tabs = $$("[data-tshot]");
  tabs.forEach((b) => b.addEventListener("click", () => {
    const i = +b.dataset.tshot;
    shots.forEach((s, k) => s.classList.toggle("on", k === i));
    tabs.forEach((t, k) => t.setAttribute("aria-selected", String(k === i)));
  }));
})();

// blog: one group at a time (FIX-LIST #145). The groups are plain sections with their own anchors (/blog#fill-quiet-hours),
// so without this script every link still lands on its group; with it, a pill or an anchor shows just that group
(() => {
  const pills = document.querySelectorAll(".blog-filter a[data-group]");
  if (!pills.length) return;
  const band = document.querySelector(".bl-feature-band");
  const show = (g, jump) => {
    pills.forEach((p) => p.setAttribute("aria-current", String(p.dataset.group === g)));
    document.querySelectorAll(".bl-group").forEach((s) => (s.hidden = g !== "all" && s.id !== g));
    if (band) band.hidden = g !== "all";
    if (jump && g !== "all") document.getElementById(g).scrollIntoView({ block: "start" });
  };
  const fromHash = () => { const g = location.hash.slice(1); show(document.getElementById(g)?.classList.contains("bl-group") ? g : "all", true); };
  pills.forEach((p) => p.addEventListener("click", (ev) => {
    ev.preventDefault();
    const g = p.dataset.group;
    history.replaceState(null, "", g === "all" ? location.pathname : "#" + g);
    show(g, false);
  }));
  addEventListener("hashchange", fromHash);
  fromHash();
})();
document.querySelectorAll("[data-share]").forEach((b) => b.addEventListener("click", async () => {
  const data = { title: document.title, url: location.href };
  try {
    if (navigator.share) return await navigator.share(data);
    await navigator.clipboard.writeText(location.href);
    b.querySelector("span").textContent = "Link copied";
  } catch {}
}));
