// node site/scripts/check.js  -- checks the email/phone parser used by the waitlist form
const assert = require("assert"), fs = require("fs"), path = require("path");
const { parseContact } = require("../js/contact.js");

assert.deepStrictEqual(parseContact(" Me@Example.com "), { email: "me@example.com" });
assert.deepStrictEqual(parseContact("905 555 0123"), { phone: "+19055550123" });
assert.deepStrictEqual(parseContact("(647) 555-0199"), { phone: "+16475550199" });
assert.deepStrictEqual(parseContact("+1 416-555-0100"), { phone: "+14165550100" });
assert.strictEqual(parseContact("555 0123"), null);
assert.strictEqual(parseContact("not@email"), null);
assert.strictEqual(parseContact("0123456789"), null);
assert.strictEqual(parseContact(""), null);
console.log("ok: contact parser");

// Home's hero map can't be blocked by the site's own security policy again (FIX-LIST #144: since #127 MapLibre's worker couldn't
// load its code, and the map stayed blank). Every outside origin the map's files use must be allowed, in the directive that
// governs that use, by the Content-Security-Policy vercel.json sends for "/" (the page that loads map.js).
{
  const site = path.join(__dirname, "..");
  const vercel = JSON.parse(fs.readFileSync(path.join(site, "..", "vercel.json"), "utf8"));
  const rule = vercel.headers.find((h) => new RegExp(`^${h.source}$`).test("/") && h.headers.some((x) => x.key === "Content-Security-Policy"));
  assert.ok(rule, 'vercel.json: no Content-Security-Policy for "/"');
  const csp = Object.fromEntries(rule.headers.find((x) => x.key === "Content-Security-Policy").value.split(";").map((d) => d.trim().split(/\s+/)).filter((d) => d[0]).map(([k, ...v]) => [k, v]));
  const read = (f) => fs.readFileSync(path.join(site, f), "utf8");
  const origin = (u) => new URL(u).origin;
  const needs = [];
  const map = read("js/map.js");
  for (const m of map.matchAll(/const LIB = "(https:[^"]+)"/g)) needs.push(["style-src", origin(m[1]), "map.js's stylesheet"]);
  for (const m of map.matchAll(/style: "(https:[^"]+)"/g)) needs.push(["connect-src", origin(m[1]), "map.js's map style and tiles"]);
  for (const m of read("app/maplibre-load.js").matchAll(/from '(https:[^']+)'/g)) needs.push(["script-src", origin(m[1]), "maplibre-load.js's import"]);
  for (const m of read("app/maplibre-worker.js").matchAll(/import '(https:[^']+)'/g)) needs.push(["worker-src", origin(m[1]), "the worker's import"]);
  assert.ok(needs.length >= 4, "map.js, maplibre-load.js or the worker no longer name their origins the way this check reads them");
  for (const [dir, o, why] of needs) {
    const list = csp[dir] || csp["default-src"] || [];
    assert.ok(list.includes(o), `vercel.json: "/" ${dir} must allow ${o} (${why}), or Home's map is blocked`);
  }
  console.log("ok: Home's map origins allowed by its CSP");
}

// the blog's groups (FIX-LIST #145): every post, queued ones too, sits in one of the four groups, and /blog has a section for
// each group with something live (its anchor the group's slug); Home's cards link to the same groups
const man = JSON.parse(fs.readFileSync(path.join(__dirname, "blog_manifest.json"), "utf8"));
assert.strictEqual(man.groups.length, 4);
for (const p of man.posts) assert.ok(man.groups.includes(p.group), `${p.slug}: no group, or one that isn't in GROUPS`);
const blogHtml = fs.readFileSync(path.join(__dirname, "..", "blog.html"), "utf8"), homeHtml = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
for (const g of man.groups) {
  if (man.posts.some((p) => p.group === g && p.status === "live")) assert.ok(blogHtml.includes(`id="${g}"`), `/blog has no section #${g}`);
  assert.ok(homeHtml.includes(`href="/blog#${g}"`), `Home doesn't link /blog#${g}`);
}
console.log("ok: blog groups");

// the database by name, not a wildcard (FIX-LIST #160 b): every CSP names FIG's own Supabase project in connect-src, never *.supabase.co
{
  const vercel = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "vercel.json"), "utf8"));
  const host = new URL(/supabaseUrl:\s*"([^"]+)"/.exec(fs.readFileSync(path.join(__dirname, "..", "js", "config.js"), "utf8"))[1]).host;
  const csps = vercel.headers.flatMap((h) => h.headers.filter((x) => x.key === "Content-Security-Policy").map((x) => [h.source, x.value]));
  for (const [src, v] of csps) assert.ok(!/\*\.supabase\.co/.test(v), `vercel.json ${src}: a *.supabase.co wildcard`);
  // nothing loads from Google Fonts (FIX-LIST #160 d: the site and the app ship their own font files), so no CSP allows it
  for (const [src, v] of csps) assert.ok(!/fonts\.g(oogleapis|static)\.com/.test(v), `vercel.json ${src}: Google Fonts is allowed but nothing uses it`);
  for (const p of ["/", "/app/welcome"]) {
    const v = (csps.find(([src]) => new RegExp(`^${src}$`).test(p)) || [])[1] || "";
    assert.ok(new RegExp(`connect-src [^;]*https://${host.replace(/\./g, "\.")}`).test(v), `vercel.json: ${p} connect-src names ${host}`);
  }
  console.log("ok: CSP names FIG's own database host");
}

// framing (FIX-LIST #164): the blog may be framed by FIG's own pages (the admin's blog preview), nothing else by anyone; every
// path gets exactly one X-Frame-Options and one frame-ancestors
{
  const vercel = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "vercel.json"), "utf8"));
  const frame = (p) => {
    const xfo = [], fa = [];
    for (const h of vercel.headers) if (new RegExp(`^${h.source}$`).test(p)) for (const x of h.headers) {
      if (x.key === "X-Frame-Options") xfo.push(x.value);
      if (x.key === "Content-Security-Policy") fa.push((/frame-ancestors ([^;]*)/.exec(x.value) || [])[1]);
    }
    return [xfo, fa];
  };
  for (const p of ["/blog", "/blog/how-fig-makes-money"]) assert.deepStrictEqual(frame(p), [["SAMEORIGIN"], ["'self'"]], p + " can be framed by FIG's own pages only");
  for (const p of ["/", "/about", "/blogger", "/app/welcome", "/contact"]) assert.deepStrictEqual(frame(p), [["DENY"], ["'none'"]], p + " can't be framed");
  console.log("ok: framing: the blog by FIG's own pages only, everything else by nobody");
}

// the build files aren't public (REVIEW 2026-10-24 E1): vercel.json publishes all of site/, so the post sources, generator and manifest in
// /scripts/ are sent to a path that 404s. A rewrite can't do it (files win over rewrites on Vercel); a redirect runs before the files.
{
  const vercel = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "vercel.json"), "utf8"));
  const rule = (vercel.redirects || []).find((r) => r.source === "/scripts/:path*");
  assert.ok(rule, "vercel.json: no redirect for /scripts/*, so posts.py, pages.py and the manifest are downloadable");
  const dest = path.join(__dirname, "..", rule.destination.replace(/^\//, ""));
  assert.ok(!fs.existsSync(dest) && !fs.existsSync(dest + ".html"), `vercel.json: ${rule.destination} is a real page, so /scripts/* would show it instead of a 404`);
  assert.ok(!fs.existsSync(path.join(__dirname, "..", "supabase")), "site/supabase/ would be public: keep SQL out of site/");
  console.log("ok: build files (/scripts) are not public");
}

// analytics only after consent (REVIEW 2026-10-24 E2): no page loads Google Analytics by itself (js/consent.js does, after "Accept"),
// every page has the cookie notice, its two choices look alike, and the CSP still lets Google's script load once accepted
{
  const site = path.join(__dirname, "..");
  const pages = (dir) => fs.readdirSync(path.join(site, dir)).filter((f) => f.endsWith(".html")).map((f) => path.join(dir, f));
  for (const f of [...pages("."), ...pages("blog")]) {
    const h = fs.readFileSync(path.join(site, f), "utf8");
    assert.ok(!/googletagmanager\.com|gtag\(/.test(h), `${f}: Google Analytics is written into the page; it may only load from js/consent.js after "Accept"`);
    assert.ok(/<script defer src="\/js\/consent\.js(\?v=[0-9a-f]+)?"><\/script>/.test(h), `${f}: no js/consent.js, so no cookie notice`);
    assert.ok(h.includes("data-cookie-settings"), `${f}: no "Cookie settings" button in the footer`);
  }
  const js = fs.readFileSync(path.join(site, "js", "consent.js"), "utf8");
  const looks = [...js.matchAll(/<button class="([^"]+)" type="button" data-ck="(granted|denied)"/g)];
  assert.deepStrictEqual(looks.map((m) => m[2]).sort(), ["denied", "granted"], "consent.js: Accept and No thanks are both needed");
  assert.strictEqual(new Set(looks.map((m) => m[1])).size, 1, "consent.js: Accept and No thanks must look the same");
  const vj = fs.readFileSync(path.join(site, "..", "vercel.json"), "utf8");
  assert.ok(/script-src[^;"]*https:\/\/www\.googletagmanager\.com/.test(vj) && /connect-src[^;"]*google-analytics\.com/.test(vj), "vercel.json: the CSP wouldn't let Google Analytics load after Accept");
  console.log("ok: Google Analytics only after consent");
}

// scripts by hash, not 'unsafe-inline' (REVIEW 2026-10-24 E9): a page may run its own files and only those inline scripts whose sha256 its CSP names
// (the Vercel analytics line on every page, Home's motion line). Edit one of them and the build says which hash to put in vercel.json's script-src.
{
  const crypto = require("crypto");
  const site = path.join(__dirname, "..");
  const vercel = JSON.parse(fs.readFileSync(path.join(site, "..", "vercel.json"), "utf8"));
  const scriptSrc = (url) => {
    const csps = vercel.headers.filter((h) => new RegExp(`^${h.source}$`).test(url)).flatMap((h) => h.headers).filter((x) => x.key === "Content-Security-Policy");
    assert.strictEqual(csps.length, 1, `vercel.json: ${url} needs exactly one Content-Security-Policy`);
    return (/script-src ([^;]*)/.exec(csps[0].value) || [])[1] || "";
  };
  const pagesIn = (dir) => fs.readdirSync(path.join(site, dir)).filter((f) => f.endsWith(".html")).map((f) => (dir === "." ? f : dir + "/" + f));
  let inline = 0;
  for (const f of [...pagesIn("."), ...pagesIn("blog")]) {
    const url = "/" + f.replace(/(^|\/)index\.html$/, "$1").replace(/\.html$/, "");
    const src = scriptSrc(url);
    assert.ok(!/'unsafe-inline'/.test(src), `vercel.json: ${url} allows 'unsafe-inline' scripts`);
    for (const m of fs.readFileSync(path.join(site, f), "utf8").matchAll(/<script\b(?![^>]*\ssrc=)([^>]*)>([\s\S]*?)<\/script>/g)) {
      if (/application\/ld\+json/.test(m[1])) continue; // data, never run
      const hash = `'sha256-${crypto.createHash("sha256").update(m[2].replace(/\r\n/g, "\n")).digest("base64")}'`;
      assert.ok(src.includes(hash), `${f}: this inline script isn't allowed by its CSP (${m[2].slice(0, 50)}...). Add ${hash} to the script-src of the CSPs for ${url} in vercel.json, or move it to a file`);
      inline++;
    }
    assert.ok(!/\son[a-z]+\s*=\s*"/.test(fs.readFileSync(path.join(site, f), "utf8")), `${f}: an inline event handler (onclick=...) can't run without 'unsafe-inline'; use addEventListener in a file`);
  }
  assert.ok(inline > 0, "no inline scripts were found: this check reads the pages wrong");
  console.log("ok: inline scripts allowed by hash (" + inline + " in the pages), no 'unsafe-inline' for scripts");
}

// the email links (2026-10-25): /unsubscribe and /confirm. Tokens are the SAME as the Supabase mail function makes (the app's
// scripts/check-emails.mjs asserts this vector too), a confirm token can't unsubscribe and the reverse, GET never changes anything, POST does only
// with the right token, a mail app's one-click POST works, and the pages answer the same for a wrong link
// no eyebrow labels on the website's own pages (owner 2026-10-04 and 2026-10-25): the pages, the stylesheets and the scripts
{
  const site = path.join(__dirname, "..");
  const pages = [...fs.readdirSync(site).filter((f) => f.endsWith(".html")).map((f) => path.join(site, f)), ...fs.readdirSync(path.join(site, "blog")).filter((f) => f.endsWith(".html")).map((f) => path.join(site, "blog", f))];
  for (const f of pages) {
    const html = fs.readFileSync(f, "utf8");
    assert.ok(!/class="[^"]*(eyebrow|kicker|overline|ph-k|city-tag)/.test(html), `${path.basename(f)}: an eyebrow label class is back`);
    assert.ok(!/New code in\s*[0-9]/i.test(html), `${path.basename(f)}: a QR countdown is back (a code changes after every scan, never with time)`);
    assert.ok(!/assets\/screens\//.test(html), `${path.basename(f)}: it shows an app screenshot (use the native mock screens)`);
    assert.ok(!/class="phone[^"]*"[^>]*>\s*<img/.test(html), `${path.basename(f)}: a phone mockup holds an image`);
  }
  for (const f of ["css/site.css", "css/pages.css", "css/tokens.css"]) assert.ok(!/text-transform:\s*uppercase/.test(fs.readFileSync(path.join(site, f), "utf8")), `${f}: uppercase text-transform (an eyebrow look) is back`);
  console.log("ok: no eyebrow labels (classes, uppercase) on the website's pages");
}
(async () => {
  process.env.UNSUB_SECRET = "test-secret-for-fig-emails"; delete process.env.SESSION_SECRET;
  const unsub = require("../../api/_lib/unsub");
  assert.strictEqual(unsub.tokenFor("unsub", "mei@example.com"), "6RGWktdssoX6ABV4z8C6mbgdV-xXfMG1", "unsubscribe token vector");
  assert.strictEqual(unsub.tokenFor("confirm", "Mei@Example.com "), "vgD9wWgTGIwenaxe-U5kRZ-efG59Ia_w", "confirm token vector");
  assert.ok(unsub.valid("mei@example.com", unsub.tokenFor("unsub", "mei@example.com")) && !unsub.valid("mei@example.com", unsub.tokenFor("confirm", "mei@example.com")), "purposes stay apart");
  assert.ok(unsub.validFor("confirm", "mei@example.com", unsub.tokenFor("confirm", "mei@example.com")) && !unsub.validFor("confirm", "sam@example.com", unsub.tokenFor("confirm", "mei@example.com")), "one address's token is no other's");
  const db = require("../../api/_lib/db");
  const calls = [];
  db.unsubscribeAddress = async (e, s) => { calls.push(["unsub", e, s]); };
  db.confirmWaitlist = async (e) => { calls.push(["confirm", e]); return e === "gone@example.com" ? "unknown" : "confirmed"; };
  const handlers = { unsubscribe: require("../../api/unsubscribe"), confirm: require("../../api/confirm") };
  const run = async (name, method, e, t, headers = {}) => {
    const res = { headers: {}, setHeader(k, v) { this.headers[k.toLowerCase()] = v; }, end(b) { this.body = b; } };
    await handlers[name]({ method, url: `/${name}?e=${encodeURIComponent(e)}&t=${t}`, headers }, res);
    return res;
  };
  const U = unsub.tokenFor("unsub", "mei@example.com"), C = unsub.tokenFor("confirm", "mei@example.com");
  let r = await run("unsubscribe", "GET", "mei@example.com", U);
  assert.ok(r.statusCode === 200 && /<form method="post"/.test(r.body) && calls.length === 0, "GET only shows the button: a mail scanner unsubscribes nobody");
  r = await run("unsubscribe", "POST", "mei@example.com", "wrongtoken");
  assert.ok(r.statusCode === 200 && calls.length === 0 && /You're unsubscribed/.test(r.body), "a wrong token changes nothing and the page says the same");
  const same = r.body;
  r = await run("unsubscribe", "POST", "mei@example.com", U, { "content-type": "application/x-www-form-urlencoded" });
  assert.deepStrictEqual(calls, [["unsub", "mei@example.com", "one-click"]], "the right token unsubscribes through the database call (a mail app's one-click post)");
  assert.strictEqual(r.body.replace("mei@example.com", "this address"), same.replace("mei@example.com", "this address"), "and the page is the same either way");
  r = await run("unsubscribe", "POST", "mei@example.com", C);
  assert.strictEqual(calls.length, 1, "a confirm token does not unsubscribe");
  r = await run("confirm", "GET", "mei@example.com", C);
  assert.ok(/<form method="post"/.test(r.body) && calls.length === 1, "confirm: GET only shows the button");
  r = await run("confirm", "POST", "mei@example.com", U);
  assert.ok(calls.length === 1 && /doesn't work/.test(r.body), "an unsubscribe token does not confirm");
  r = await run("confirm", "POST", "mei@example.com", C);
  assert.ok(calls.length === 2 && calls[1][0] === "confirm" && /You're on the list/.test(r.body), "the right token confirms");
  const gone = unsub.tokenFor("confirm", "gone@example.com");
  r = await run("confirm", "POST", "gone@example.com", gone);
  assert.ok(/doesn't work/.test(r.body), "an address that is not on the list gets the same answer as a wrong link");
  for (let i = 0; i < 31; i++) r = await run("unsubscribe", "POST", "mei@example.com", "bad" + i);
  assert.strictEqual(r.statusCode, 429, "a flood of wrong tokens is stopped");
  r = await run("unsubscribe", "POST", "mei@example.com", U);
  assert.ok(r.statusCode === 200 && calls[calls.length - 1][0] === "unsub", "but a right token is always honoured");
  const vercel = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "vercel.json"), "utf8"));
  for (const n of ["confirm", "unsubscribe"]) assert.ok(vercel.rewrites.some((x) => x.source === "/" + n && x.destination === "/api/" + n), `vercel.json: /${n} is not routed to /api/${n}`);
  // the contact page's email line stays hidden until the owner flips the one setting (site/js/config.js showEmail)
  const cfg = fs.readFileSync(path.join(__dirname, "..", "js", "config.js"), "utf8");
  assert.ok(/showEmail:\s*false/.test(cfg), "config.js: showEmail must be false until the owner has tested the mailbox");
  for (const f of ["contact.html", "help.html"]) assert.ok(/class="[^"]*\bfig-mail\b[^"]*" hidden/.test(fs.readFileSync(path.join(__dirname, "..", f), "utf8")), `${f}: the email line must be hidden in the HTML`);
  console.log("ok: email links: same tokens as the mail function, GET changes nothing, POST needs the right token, one-click works, same page for wrong links, rate limited, routes, email line hidden");
})().catch((e) => { console.error(e); process.exit(1); });
