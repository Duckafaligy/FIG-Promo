// Blog management for the admin page. The posts themselves are generated from the site's code; this file builds the list the admin shows
// (the generator's manifest on GitHub, or the live sitemap and feed until that exists) and merges the team's controls kept in the database
// (table blog_overrides: a post taken down, or its go-live time moved). Server only.
const db = require("./db");

const SITE = "https://fig-promo.vercel.app";
const RAW = "https://raw.githubusercontent.com/Duckafaligy/FIG-Promo/main/site/scripts/blog_manifest.json";
const get = (url) => fetch(url, { signal: AbortSignal.timeout(8000), headers: { "User-Agent": "fig-admin" } });
const text = async (url) => { const r = await get(url); if (!r.ok) throw new Error(url + " " + r.status); return r.text(); };
const decode = (s) => String(s).replace(/<!\[CDATA\[|\]\]>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#x([0-9a-f]+);/gi, (m, h) => String.fromCodePoint(parseInt(h, 16))).replace(/&#(\d+);/g, (m, d) => String.fromCodePoint(Number(d))).replace(/&apos;/g, "'").trim();

// every post the generator knows (live, queued and taken down). Before the manifest exists: what the live site publishes.
async function posts() {
  try {
    const m = JSON.parse(await text(RAW + "?t=" + Math.floor(Date.now() / 60000)));
    if (Array.isArray(m.posts) && m.posts.length) return { source: "manifest", posts: m.posts };
  } catch (e) { /* not there yet */ }
  const [sitemap, feed] = await Promise.all([text(SITE + "/sitemap.xml"), text(SITE + "/feed.xml").catch(() => "")]);
  const titles = new Map();
  for (const it of feed.matchAll(/<item>([\s\S]*?)<\/item>/g)) {
    const slug = (it[1].match(/<link>[^<]*\/blog\/([a-z0-9-]+)<\/link>/) || [])[1];
    const title = (it[1].match(/<title>([\s\S]*?)<\/title>/) || [])[1];
    const date = (it[1].match(/<pubDate>([\s\S]*?)<\/pubDate>/) || [])[1];
    if (slug) titles.set(slug, { title: decode(title || slug), date: date ? new Date(date).toISOString().slice(0, 10) : "" });
  }
  const slugs = [...new Set([...sitemap.matchAll(/<loc>[^<]*\/blog\/([a-z0-9-]+)<\/loc>/g)].map((m) => m[1]))];
  return { source: "live-site", posts: slugs.map((slug) => ({ slug, title: (titles.get(slug) || {}).title || slug, date: (titles.get(slug) || {}).date || "", topic: "", status: "live", words: null })) };
}

// is the page really being served right now?
async function served(slug) {
  try { const r = await fetch(`${SITE}/blog/${slug}?c=${Date.now()}`, { method: "HEAD", signal: AbortSignal.timeout(6000), redirect: "manual" }); return r.status === 200; } catch (e) { return null; }
}

async function list() {
  const [{ source, posts: base }, rows] = await Promise.all([posts(), db.blogOverrides()]);
  const ov = new Map(rows.map((r) => [r.slug, r]));
  const out = await Promise.all(base.map(async (p) => {
    const o = ov.get(p.slug) || {};
    const visible = await served(p.slug);
    const when = o.publish_at || p.publish_at || null; // the team's time wins over the one in the code
    const status = o.hidden ? "taken-down" : when && Date.parse(when) > Date.now() ? "queued" : "live";
    return { slug: p.slug, title: p.title, topic: p.topic || "", date: p.date || "", words: p.words ?? null, status, visible, publish_at: when, hidden: !!o.hidden, overridden: !!(o.hidden || o.publish_at) };
  }));
  out.sort((a, b) => (b.date || "").localeCompare(a.date || "") || a.slug.localeCompare(b.slug));
  return { source, posts: out };
}

module.exports = { list };
