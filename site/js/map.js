// Hero map: the same map the FIG app draws on the web (MapLibre + OpenFreeMap), in its dark style,
// with the app's food-photo pins around Hwy 7 & Kennedy, Markham. Falls back to a still image without WebGL.
(() => {
  const box = document.getElementById("map");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const wide = () => innerWidth >= 980;
  const PHOTOS = ["0EVQW1F2MSCJSTCDCG9YH93F6B", "0RYWBBV51KE94G17WYCQY5Q6HH", "14WZX6B42KWT8QRFSJ7NM4QQK9", "16V5JEZGGNE3NPX8DC2WNFT64K",
    "25833J5ACM7EB0TJ5F5B8QSRSY", "2AN6E5P3GDC1QW4REMTDK6AY57", "2PA5R36RQX1KQMXAC89CX7B167", "32TXW2T9HVFKGNMKXGWPF57X4S",
    "36VQAEPPGHX17KWN8CCCS2KG07", "3QG0YSDTY4W552YE3N1VHZSED2", "40WEZ22K5FV8YNHPYPQ7J6EWNN", "5PF706P8NNHG3TW4ARWFD6T17Z",
    "5PGYW83TMVHGAXX3X0D7SE751X", "6H6JKMMDC87EF7KF7FPAEH08V6", "6KDKWJ5BS8PPF6PS0HQ93G0VFP", "6TNFWB2ZQZXHJQ5RSG17V1F10X"];
  window.FIG_PINS = PHOTOS.map((p) => `/assets/pins/${p}.jpg`);
  if (!box || !window.maplibregl) return;

  let map;
  try {
    map = new maplibregl.Map({
      container: box, style: "https://tiles.openfreemap.org/styles/dark", center: [-79.302, 43.8555],
      zoom: wide() ? 13.8 : 13.3, interactive: false, attributionControl: false, fadeDuration: 0,
    });
  } catch (e) { return; } // no WebGL: the still image stays

  let seed = 11;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  map.on("load", () => {
    box.classList.add("ready");
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
      new maplibregl.Marker({ element: outer }).setLngLat(map.unproject([x, y])).addTo(map);
    }
    const you = document.createElement("div"); you.className = "you";
    new maplibregl.Marker({ element: you }).setLngLat(map.unproject([W * (wide() ? 0.7 : 0.5), H * (wide() ? 0.52 : 0.32)])).addTo(map);

    if (reduce) return;
    // slow drift, nudged by the mouse; stops while the hero is off screen
    let on = true, tx = 0, ty = 0, cx = 0, cy = 0, t0 = performance.now();
    new IntersectionObserver(([e]) => { on = e.isIntersecting; if (on) requestAnimationFrame(tick); }).observe(box);
    addEventListener("pointermove", (e) => { tx = (e.clientX / innerWidth - 0.5) * -26; ty = (e.clientY / innerHeight - 0.5) * -18; }, { passive: true });
    function tick(now) {
      if (!on) return;
      cx += (tx - cx) * 0.05; cy += (ty - cy) * 0.05;
      box.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      map.setBearing(Math.sin((now - t0) / 9000) * 4);
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
})();
