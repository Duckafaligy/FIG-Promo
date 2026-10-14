// The web app's shell (+html.tsx), outside React: its language before the app loads, from the phone (FIG's 4 languages,
// Traditional Chinese for Taiwan, Hong Kong and Macau, like the app's phoneLang), and the shell's "Back to FIG" link in it.
// The app sets <html lang> once it knows the language (picked or the phone's); the link follows it. Also, early: the signed-out
// look, which screen the loading skeleton draws, and the service worker.
(() => {
  const T = { fr: "Retour à FIG", "zh-Hans": "返回 FIG", "zh-Hant": "返回 FIG" };
  const l = (navigator.languages && navigator.languages[0]) || navigator.language || "en";
  const root = document.documentElement;
  // the signed-out pages start in the shell's "auth" look (the app sets the same once it knows who's here), so the screen
  // doesn't drop 56 px under the "Back to FIG" bar after it loads (CLS 0.066 on /sign-in at phone width)
  const path = location.pathname.replace(/^\/app/, "");
  const auth = /^\/(sign-in|sign-in-phone|sign-up|sign-up-business|forgot-password|new-password|welcome|verify-phone|verify-email)\/?$/.test(path);
  if (auth) root.dataset.figScreen = "auth";
  // which screen the shell's skeleton draws until the app is here (+html.tsx), and which tab it lights
  const seg = path.split("/")[1] || "home";
  root.dataset.figPath = auth ? "auth" : { home: "home", map: "map", search: "search", restaurant: "rest", r: "rest", voucher: "tab", saved: "tab", chats: "tab", deals: "tab", profile: "profile" }[seg] || "other";
  root.dataset.figTab = seg === "deals" ? "voucher" : seg;
  // repeat visits open from the phone's copy, and work offline (/sw.js); after the page has loaded, never competing with it
  // (the first time, this page loaded before the worker: it's told what to save, so this page opens offline too)
  const sw = "serviceWorker" in navigator && navigator.serviceWorker, before = sw && sw.controller; // did this page load through it?
  if (sw) addEventListener("load", () => sw.register("/sw.js", { scope: "/app/" }).then(() => sw.ready).then((reg) => {
    const save = () => reg.active.postMessage({ page: location.pathname, files: performance.getEntriesByType("resource").map((x) => x.name) });
    if (!before) { save(); setTimeout(save, 10000); } // and again for the files still on their way when it took over
  }).catch(() => {}));
  root.lang = /^zh/i.test(l) ? (/Hant|-(TW|HK|MO)\b/i.test(l) ? "zh-Hant" : "zh-Hans") : /^fr/i.test(l) ? "fr" : "en";
  const apply = () => { const t = document.querySelector(".fig-backlink span"); if (t) t.textContent = T[root.lang] || "Back to FIG"; };
  new MutationObserver(apply).observe(root, { attributes: true, attributeFilter: ["lang"] });
  document.addEventListener("DOMContentLoaded", apply);
})();
