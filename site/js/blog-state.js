// A post the team took down on the admin's Blog page disappears right away, before the next rebuild removes it for real
// (user 2026-10-14: "if I don't like a post I can delete it"). Asks /api/blog-state which posts are hidden: on such a post's
// own page the article gives way to a short note (and noindex); every card or link to it goes. Visible posts never move, and
// any error leaves the page as it is.
(() => {
  const post = document.querySelector("[data-post]");
  if (!post && !document.querySelector("[data-post-card]")) return;
  fetch("/api/blog-state", { headers: { accept: "application/json" } })
    .then((r) => (r.ok ? r.json() : null))
    .then((s) => {
      const hidden = new Set(s && Array.isArray(s.hidden) ? s.hidden : []);
      if (!hidden.size) return;
      document.querySelectorAll("[data-post-card]").forEach((c) => {
        if (hidden.has(c.dataset.postCard)) (c.closest(".bl-feature-band") || c).remove();
      });
      if (post && hidden.has(post.dataset.post)) {
        post.innerHTML = '<section class="ps-head"><div class="wrap"><h1 class="ps-h1">This post is no longer available</h1>' +
          '<p class="ps-dek"><a href="/blog">See the FIG blog</a></p></div></section>';
        let robots = document.querySelector('meta[name="robots"]');
        if (!robots) { robots = document.createElement("meta"); robots.name = "robots"; document.head.append(robots); }
        robots.content = "noindex";
        document.title = "Post not available · FIG";
      }
    })
    .catch(() => {});
})();
