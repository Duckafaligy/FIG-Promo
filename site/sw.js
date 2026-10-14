// The FIG web app's service worker (scope /app/, registered by /js/app-lang.js): repeat visits open from the phone's copy,
// and the pages already opened still open offline.
// Pages: the network first, so a new deploy shows at once and a page never points at script files that are gone; the
// saved copy only when the network is down or slower than 3 s. Hashed files (/app/_expo/static/) and resized photos
// (/_vercel/image) are saved on first use and served from the copy after (a new version has a new name). /assets/ is
// served from the copy and refreshed in the background. Nothing else is touched: /api, /admin, /js, Supabase, map tiles.
// To change how it caches, bump V: the next visit installs it and drops the old caches.
const V = "1";
const PAGES = "fig-pages-" + V, FILES = "fig-files-" + V;

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k !== PAGES && k !== FILES) await caches.delete(k);
  if (self.registration.navigationPreload) await self.registration.navigationPreload.enable();
  await self.clients.claim();
})()));

// ponytail: drops the oldest entries past a count (cache keys keep insertion order); a size budget if photos pile up
const trim = async (name, max) => { const c = await caches.open(name); const keys = await c.keys(); for (const k of keys.slice(0, Math.max(0, keys.length - max))) await c.delete(k); };

const OFFLINE = `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>FIG · Offline</title>
<body style="margin:0;min-height:100vh;display:grid;place-items:center;font:16px/1.5 system-ui,sans-serif;color:#0A1020;background:#fff;text-align:center;padding:24px;box-sizing:border-box">
<div><img src="/assets/favicon.svg" alt="" width="56" height="56"><h1 style="font-size:22px;margin:16px 0 6px">You're offline</h1>
<p style="margin:0 0 20px;color:#66718A">FIG opens again as soon as you're back online.</p>
<a href="" style="display:inline-block;padding:12px 22px;border-radius:99px;background:#1E5EFF;color:#fff;font-weight:700;text-decoration:none">Try again</a></div>`;

async function page(e) {
  const c = await caches.open(PAGES), key = location.origin + new URL(e.request.url).pathname;
  const net = Promise.resolve(e.preloadResponse).then((r) => r || fetch(e.request)).then((r) => {
    if (r.ok && r.type === "basic") e.waitUntil(c.put(key, r.clone()).then(() => trim(PAGES, 40)));
    return r;
  });
  // the saved copy of this page (a page never opened here needs script files that were never saved: the offline page)
  const copy = () => c.match(key);
  const slow = new Promise((ok) => setTimeout(ok, 3000)).then(copy);
  const r = await Promise.race([net.catch(copy), slow.then((x) => x || net.catch(copy))]);
  return r || new Response(OFFLINE, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}

async function saved(req) {
  const c = await caches.open(FILES);
  const hit = await c.match(req);
  if (hit) return hit;
  const r = await fetch(req);
  if (r.ok) { await c.put(req, r.clone()); trim(FILES, 200); }
  return r;
}

async function fresh(e) {
  const c = await caches.open(FILES);
  const hit = await c.match(e.request);
  const net = fetch(e.request).then((r) => { if (r.ok) c.put(e.request, r.clone()); return r; });
  if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
  return net;
}

// the first page opened loaded before this worker was here: it sends its address and the files it used, saved now
self.addEventListener("message", (e) => {
  const { page: at, files = [] } = e.data || {};
  const save = async (u, name, key) => {
    const url = new URL(u, location.origin);
    if (url.origin !== location.origin) return;
    const r = await fetch(url.href).catch(() => null);
    if (r && r.ok) await (await caches.open(name)).put(key || url.href, r);
  };
  e.waitUntil(Promise.all([
    /^\/app(\/|$)/.test(at || "") && save(at, PAGES, location.origin + at),
    ...files.filter((u) => /^\/(app\/_expo\/static|assets)\//.test(new URL(u, location.origin).pathname)).map((u) => save(u, FILES)),
  ]));
});

self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  if (req.mode === "navigate") { if (/^\/app(\/|$)/.test(url.pathname)) e.respondWith(page(e)); return; }
  if (url.pathname.startsWith("/app/_expo/static/") || url.pathname === "/_vercel/image") e.respondWith(saved(req));
  else if (url.pathname.startsWith("/assets/")) e.respondWith(fresh(e));
});
