// /api/blog-state  (GET, public): the slugs of blog posts the team has taken down. The blog pages read this (js/blog-state.js) and hide such a post for
// everyone within about 15 seconds, before the next site update removes it for good. Slugs only, nothing else; cached for 10 seconds.
const db = require("./_lib/db");

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "public, s-maxage=10, stale-while-revalidate=20");
  if (req.method !== "GET" && req.method !== "HEAD") { res.statusCode = 405; return res.end('{"error":"Not allowed."}'); }
  if (!db.connected()) return res.end('{"hidden":[]}');
  try {
    const rows = await db.blogOverrides();
    res.end(JSON.stringify({ hidden: rows.filter((r) => r.hidden).map((r) => r.slug).sort() }));
  } catch (e) {
    res.statusCode = 200; // never break a post page because the lookup failed: show nothing as hidden
    res.setHeader("Cache-Control", "public, s-maxage=15");
    res.end('{"hidden":[]}');
  }
};
