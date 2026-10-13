// GET /api/health: is the site up, and which version is live? For an uptime monitor. No database, no secrets, never cached.
module.exports = (req, res) => {
  res.statusCode = req.method === "GET" || req.method === "HEAD" ? 200 : 405;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex");
  if (req.method === "HEAD") return res.end();
  res.end(JSON.stringify({ ok: res.statusCode === 200, version: (process.env.VERCEL_GIT_COMMIT_SHA || "dev").slice(0, 7), time: new Date().toISOString() }));
};
