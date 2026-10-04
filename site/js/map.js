// Hero map: the same light Markham map + food-photo pins as the video outro (OpenStreetMap data, ODbL).
// Plays a short intro (camera settles, pins ripple out from Hwy 7 & Kennedy), then stays still.
(() => {
  const cvs = document.getElementById("map");
  if (!cvs) return;
  const ctx = cvs.getContext("2d");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const K = 0.42;
  const ROAD = { 5: [7, "#f4c542"], 4: [4.5, "#ffffff"], 3: [3.4, "#ffffff"], 2: [2.6, "#fbf9f5"], 1: [1.6, "#f7f4ee"] };
  const PIN_FILES = ["0EVQW1F2MSCJSTCDCG9YH93F6B", "0RYWBBV51KE94G17WYCQY5Q6HH", "14WZX6B42KWT8QRFSJ7NM4QQK9", "16V5JEZGGNE3NPX8DC2WNFT64K",
    "25833J5ACM7EB0TJ5F5B8QSRSY", "2AN6E5P3GDC1QW4REMTDK6AY57", "2PA5R36RQX1KQMXAC89CX7B167", "32TXW2T9HVFKGNMKXGWPF57X4S",
    "36VQAEPPGHX17KWN8CCCS2KG07", "3QG0YSDTY4W552YE3N1VHZSED2", "40WEZ22K5FV8YNHPYPQ7J6EWNN", "5PF706P8NNHG3TW4ARWFD6T17Z",
    "5PGYW83TMVHGAXX3X0D7SE751X", "6H6JKMMDC87EF7KF7FPAEH08V6", "6KDKWJ5BS8PPF6PS0HQ93G0VFP", "6TNFWB2ZQZXHJQ5RSG17V1F10X"];
  window.FIG_PINS = PIN_FILES.map((f) => `/assets/pins/${f}.jpg`);

  const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const clamp = (v) => Math.max(0, Math.min(1, v));
  const lerp = (a, b, u) => a + (b - a) * u;
  const ease = (u) => 1 - Math.pow(1 - u, 3);

  let MAP = null, PINS = [], W = 0, H = 0, S = 1, CX = 0, CY = 0, T0 = 0;
  const imgs = window.FIG_PINS.map((src) => { const im = new Image(); im.src = src; im.onload = () => draw(lastT); return im; });
  let lastT = 0;

  function size() {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    W = cvs.clientWidth; H = cvs.clientHeight;
    cvs.width = Math.round(W * dpr); cvs.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const wide = W > 900;
    S = wide ? Math.max(W * 0.62, H) / 1080 : Math.max(W, H * 0.5625) / 1080;
    CX = wide ? W * 0.8 : W / 2;
    CY = wide ? H * 0.52 : H * 0.34;
  }

  function camera(T) {
    const f = ease(clamp(T / 2.6));
    return { tilt: lerp(64, 50, f) * Math.PI / 180, cy: lerp(700, 160, f), zoom: lerp(1.2, 1.0, f) };
  }
  function proj(cam, x, y) {
    const yr = y - cam.cy;
    const depth = 1400 - yr * Math.sin(cam.tilt);
    if (depth < 160) return null;
    const s = (1400 / depth) * cam.zoom * S;
    return { x: CX + x * s, y: CY + yr * Math.cos(cam.tilt) * s, s };
  }
  function path(cam, flat, close) {
    let started = false;
    ctx.beginPath();
    for (let i = 0; i < flat.length; i += 2) {
      const v = proj(cam, flat[i] * K, flat[i + 1] * K);
      if (!v || v.y < -200 || v.y > H + 400) { started = false; continue; }
      if (started) ctx.lineTo(v.x, v.y); else { ctx.moveTo(v.x, v.y); started = true; }
    }
    if (close) ctx.closePath();
  }

  function draw(T) {
    lastT = T;
    if (!MAP || !W) return;
    const cam = camera(T);
    ctx.fillStyle = "#ebe6dc"; ctx.fillRect(0, 0, W, H);
    const lw = cam.zoom * S * (1400 / (1400 + 300 * Math.sin(cam.tilt)));
    ctx.lineJoin = "round"; ctx.lineCap = "round";
    ctx.fillStyle = "#cde6c0"; MAP.parks.forEach((f) => { path(cam, f, true); ctx.fill(); });
    ctx.fillStyle = "#a9d3f5"; MAP.water.forEach((f) => { path(cam, f, true); ctx.fill(); });
    ctx.strokeStyle = "#a9d3f5"; ctx.lineWidth = 2.5 * lw; MAP.streams.forEach((f) => { path(cam, f, false); ctx.stroke(); });
    [1, 2, 3, 4, 5].forEach((cls) => {
      const [w, col] = ROAD[cls];
      ctx.strokeStyle = col; ctx.lineWidth = w * lw * 1.6;
      MAP.roads.forEach((r) => { if (r[0] === cls) { path(cam, r.slice(1), false); ctx.stroke(); } });
    });
    PINS.forEach((p) => {
      const on = clamp((T - 0.3 - p.d / 1700 * 1.9) / 0.35);
      if (on <= 0) return;
      const pp = proj(cam, p.x, p.y);
      if (!pp || pp.y < -60 || pp.y > H + 60) return;
      // light bounce in: overshoot a touch, then settle
      const pop = on < 1 ? 1 + Math.sin(on * Math.PI) * 0.18 : 1;
      const r = p.s * Math.max(0.35, pp.s) * pop * on;
      if (r < 1) return;
      ctx.globalAlpha = clamp(on * 1.5);
      if (p.img.complete && p.img.naturalWidth) {
        ctx.save(); ctx.beginPath(); ctx.arc(pp.x, pp.y, r, 0, Math.PI * 2); ctx.clip();
        ctx.drawImage(p.img, pp.x - r, pp.y - r, r * 2, r * 2); ctx.restore();
      }
      ctx.strokeStyle = p.c; ctx.lineWidth = Math.max(1.5, r * 0.18);
      ctx.beginPath(); ctx.arc(pp.x, pp.y, r, 0, Math.PI * 2); ctx.stroke();
    });
    ctx.globalAlpha = 1;
  }

  function loop(now) {
    const T = (now - T0) / 1000;
    draw(T);
    if (T < 4.2) requestAnimationFrame(loop);
  }

  fetch("/assets/markham-map.json").then((r) => r.json()).then((m) => {
    MAP = m;
    PINS = m.pins.map(([x, y], i) => {
      const r = hash(i * 1.9 + 5);
      return { x: x * K, y: y * K, d: Math.hypot(x, y) * K, img: imgs[i % imgs.length],
               c: r < 0.6 ? "#1e5eff" : r < 0.72 ? "#c8f135" : "#ffffff", s: 26 + hash(i * 2.3) * 8 };
    });
    size();
    if (reduce) { draw(10); return; }
    T0 = performance.now();
    requestAnimationFrame(loop);
  });

  let rt;
  addEventListener("resize", () => {
    clearTimeout(rt);
    rt = setTimeout(() => { const w = cvs.clientWidth; if (w !== W || Math.abs(cvs.clientHeight - H) > 120) { size(); draw(Math.max(lastT, 10)); } }, 150);
  });
})();
