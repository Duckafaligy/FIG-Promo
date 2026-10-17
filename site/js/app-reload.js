// The web app (/app) after a deploy (FIX-LIST #36): a tab opened before it asks for the old build's chunks, which are gone,
// and gets HTML or an unknown module on every screen. On that error, reload once to pick up the new build. A flag in
// sessionStorage stops a loop; it clears after a minute of running fine, so the next deploy can reload again.
(function () {
  var KEY = "fig.reloadedForDeploy";
  var STALE = /Requiring unknown module|Loading chunk|ChunkLoadError|dynamically imported module|Unexpected token '<'/;
  function reloadOnce() {
    try {
      if (sessionStorage.getItem(KEY)) return;
      sessionStorage.setItem(KEY, "1");
    } catch (e) {
      return; // no storage: never risk a reload loop
    }
    location.reload();
  }
  addEventListener("error", function (e) {
    var t = e.target;
    if (t && t.tagName === "SCRIPT" && /\/_expo\//.test(t.src || "")) reloadOnce();
    else if (STALE.test(e.message || "")) reloadOnce();
  }, true);
  addEventListener("unhandledrejection", function (e) {
    var r = e.reason;
    if (STALE.test(String((r && r.message) || r || ""))) reloadOnce();
  });
  addEventListener("load", function () {
    setTimeout(function () {
      try { sessionStorage.removeItem(KEY); } catch (e) { /* nothing to clear */ }
    }, 60000);
  });
})();
