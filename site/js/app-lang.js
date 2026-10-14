// The web app's shell (+html.tsx), outside React: its language before the app loads, from the phone (FIG's 4 languages,
// Traditional Chinese for Taiwan, Hong Kong and Macau, like the app's phoneLang), and the shell's "Back to FIG" link in it.
// The app sets <html lang> once it knows the language (picked or the phone's); the link follows it.
(() => {
  const T = { fr: "Retour à FIG", "zh-Hans": "返回 FIG", "zh-Hant": "返回 FIG" };
  const l = (navigator.languages && navigator.languages[0]) || navigator.language || "en";
  const root = document.documentElement;
  root.lang = /^zh/i.test(l) ? (/Hant|-(TW|HK|MO)\b/i.test(l) ? "zh-Hant" : "zh-Hans") : /^fr/i.test(l) ? "fr" : "en";
  const apply = () => { const t = document.querySelector(".fig-backlink span"); if (t) t.textContent = T[root.lang] || "Back to FIG"; };
  new MutationObserver(apply).observe(root, { attributes: true, attributeFilter: ["lang"] });
  document.addEventListener("DOMContentLoaded", apply);
})();
