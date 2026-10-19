// Hero map: the same map the FIG app draws on the web (MapLibre + OpenFreeMap), in its dark style,
// with the app's food-photo pins around Hwy 7 & Kennedy, Markham. Falls back to a still image without WebGL.
(() => {
  const box = document.getElementById("map");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const wide = () => innerWidth >= 980;
  const PHOTOS = ["golden-lantern", "chatime", "kinton-ramen", "seoul-house", "dumpling-house", "brew-lab", "sakura-house", "pho-hung", "bowl-lab", "noodle-bar", "wok-bar", "burger-co", "alt-tacos", "alt-pizza", "alt-hotpot", "alt-banhmi"]; // Unsplash License, see assets/food/CREDITS.txt
  window.FIG_PINS = PHOTOS.map((p) => `/assets/pins/${p}.jpg`);
  if (!box) return;
  // the still map paints first; MapLibre loads once the page is idle, so it never delays the hero text. The same pinned build as
  // the web app (6.11.2, /app/maplibre-load.js and its worker), so a visitor who goes on to /app doesn't download it twice (FIX-LIST #127)
  const LIB = "https://cdn.jsdelivr.net/npm/maplibre-gl@6.11.2/dist";
  const later = window.requestIdleCallback || ((f) => setTimeout(f, 1200));
  later(() => {
    const css = document.createElement("link"); css.rel = "stylesheet"; css.href = LIB + "/maplibre-gl.css"; document.head.appendChild(css);
    addEventListener("fig-maplibre", start, { once: true });
    const js = document.createElement("script"); js.type = "module"; js.src = "/app/maplibre-load.js"; document.head.appendChild(js);
  }, { timeout: 2500 });

  function start() {
  if (!window.maplibregl) return;
  let map;
  try {
    map = new maplibregl.Map({
      container: box, style: "https://tiles.openfreemap.org/styles/positron", center: [-79.302, 43.8555],
      zoom: wide() ? 13.8 : 13.3, interactive: false, attributionControl: false, fadeDuration: 0,
      // a 2x or 3x screen drew 4-9x the pixels for a map that sits under the hero's fade; 1.5 looks the same (FIX-LIST #144)
      pixelRatio: Math.min(devicePixelRatio || 1, 1.5),
    });
  } catch (e) { return; } // no WebGL: the still image stays

  let seed = 11;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  // the pins are decoration: MapLibre makes each marker a role=button that can't be focused or used, so screen readers skip them
  const deco = (m) => { const e = m.getElement(); e.removeAttribute("role"); e.removeAttribute("aria-label"); e.removeAttribute("tabindex"); e.setAttribute("aria-hidden", "true"); };
  // a lost WebGL canvas (memory pressure, a GPU reset) comes back blank until something draws it: draw it again
  map.on("webglcontextrestored", () => map.triggerRepaint());
  map.on("load", () => {
    box.classList.add("ready");
    map.triggerRepaint(); // one sure frame now the map is ready, with no drift loop to keep drawing
    const W = box.clientWidth, H = box.clientHeight, minX = wide() ? 0.53 : 0.04, maxY = wide() ? 0.95 : 0.5;
    const placed = [];
    for (let i = 0, tries = 0; placed.length < (wide() ? 22 : 10) && tries < 3000; tries++) {
      const x = W * minX + rnd() * W * (1 - minX - 0.04), y = 110 + rnd() * (H * maxY - 140);
      if (placed.some((p) => Math.hypot(p.x - x, p.y - y) < 80)) continue;
      placed.push({ x, y });
      const r = rnd(), kind = r < 0.62 ? "deal" : r < 0.76 ? "flash" : "place";
      const outer = document.createElement("div");
      const el = document.createElement("div");
      el.className = `pin ${kind} pin-in`;
      el.style.animationDelay = `${0.5 + Math.hypot(x - W * 0.7, y - H * 0.5) / 900}s`;
      el.innerHTML = `<img src="${window.FIG_PINS[i++ % PHOTOS.length]}" alt="">`;
      outer.appendChild(el);
      deco(new maplibregl.Marker({ element: outer }).setLngLat(map.unproject([x, y])).addTo(map));
    }
    const you = document.createElement("div"); you.className = "you";
    deco(new maplibregl.Marker({ element: you }).setLngLat(map.unproject([W * (wide() ? 0.7 : 0.5), H * (wide() ? 0.52 : 0.32)])).addTo(map));

    // phones and tablets: no drift. Turning the map redraws all of it every frame, which costs a phone ~1 s of main thread
    // per few seconds (slow taps, battery) for a 4° sway nobody sees on a small screen
    if (reduce || !matchMedia("(pointer: fine)").matches) return;
    // slow drift, nudged by the mouse (FIX-LIST #144: the hero lagged): it runs only while the hero is on screen, the tab is
    // visible and the mouse has moved in the last 1.5 s, at 30 fps; otherwise there's no frame loop at all. A moving mouse or
    // the hero coming back starts it again; the sway picks up where it stopped.
    let seen = false, raf = 0, tx = 0, ty = 0, cx = 0, cy = 0, moved = 0, last = 0, drift = 0;
    const run = () => { if (!raf && seen && !document.hidden && !document.documentElement.classList.contains("paused") && performance.now() - moved < 1500) raf = requestAnimationFrame(tick); };
    new IntersectionObserver(([e]) => { seen = e.isIntersecting; run(); }).observe(box);
    document.addEventListener("visibilitychange", run);
    addEventListener("pointermove", (e) => { tx = (e.clientX / innerWidth - 0.5) * -26; ty = (e.clientY / innerHeight - 0.5) * -18; moved = performance.now(); run(); }, { passive: true });
    function tick(now) {
      raf = 0;
      if (!seen || document.hidden || document.documentElement.classList.contains("paused") || now - moved > 1500) { last = 0; return; }
      if (now - last >= 33) {
        drift += last ? Math.min(now - last, 100) : 0; last = now;
        cx += (tx - cx) * 0.1; cy += (ty - cy) * 0.1;
        box.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
        map.setBearing(Math.sin(drift / 9000) * 4);
      }
      raf = requestAnimationFrame(tick);
    }
  });
}
})();
