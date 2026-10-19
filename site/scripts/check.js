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
  for (const p of ["/", "/about", "/admin", "/blogger", "/app/welcome", "/contact"]) assert.deepStrictEqual(frame(p), [["DENY"], ["'none'"]], p + " can't be framed");
  console.log("ok: framing: the blog by FIG's own pages only, everything else by nobody");
}
