// The website in FIG's four languages (the founder 2026-10-30: "a way to translate the entire site... a dropdown small one in the corner").
// Runs in <head>, before the page draws. The language: the visitor's pick (localStorage "fig.siteLang"), else the browser's, mapped
// like js/app-lang.js (Traditional Chinese for Taiwan, Hong Kong and Macau). English stops here: nothing more loads.
// Otherwise /lang/<lang>.js (keyed by the exact English, like the app's dictionaries) comes in and hands its words to figLang().
// Once the page is read, before the other scripts run, every text node, placeholder, aria-label, alt and title, and the <title>,
// whose English is in it is swapped; then a MutationObserver does the same for whatever a script writes later (form messages,
// the cookie notice). Nothing under translate="no" is touched: the legal pages and the blog stay in English (pages.py).
// The body stays hidden until the swap (site.css html.lang-wait, at most 2 s), so French and Chinese visitors see no English flash.
// site/scripts/check.js requires a translation of every English string on the pages (scripts/lang-strings.js reads them the same way).
(() => {
  const KEY = "fig.siteLang", LANGS = ["en", "fr", "zh-Hans", "zh-Hant"], root = document.documentElement;
  let lang = null;
  try { lang = localStorage.getItem(KEY); } catch { /* no storage: the browser's language */ }
  if (!LANGS.includes(lang)) {
    const l = (navigator.languages && navigator.languages[0]) || navigator.language || "en";
    lang = /^zh/i.test(l) ? (/Hant|-(TW|HK|MO)\b/i.test(l) ? "zh-Hant" : "zh-Hans") : /^fr/i.test(l) ? "fr" : "en";
  }
  root.lang = lang;

  // the picker (pages.py writes it into the navbar and the legal pages' band): a button that opens a list of the four languages
  document.addEventListener("DOMContentLoaded", () => {
    root.classList.remove("lang-wait");
    if (lang !== "en") document.querySelectorAll(".lang-note").forEach((n) => { n.hidden = false; });
    document.querySelectorAll(".lang").forEach((box) => {
      const btn = box.querySelector(".lang-btn"), list = box.querySelector(".lang-list");
      const show = (open) => { btn.setAttribute("aria-expanded", String(open)); list.hidden = !open; };
      list.querySelectorAll("[data-lang]").forEach((b) => b.dataset.lang === lang && b.setAttribute("aria-current", "true"));
      btn.addEventListener("click", () => { show(list.hidden); if (!list.hidden) list.querySelector("[aria-current]")?.focus(); });
      list.addEventListener("click", (e) => {
        const b = e.target.closest("[data-lang]");
        if (!b) return;
        try { localStorage.setItem(KEY, b.dataset.lang); } catch { /* private window: this page only */ }
        if (b.dataset.lang === lang) { show(false); btn.focus(); } else location.reload();
      });
      box.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !list.hidden) { show(false); btn.focus(); }
        if ((e.key === "ArrowDown" || e.key === "ArrowUp") && !list.hidden) { // up and down move through the list too
          const bs = [...list.querySelectorAll("button")], i = bs.indexOf(document.activeElement);
          bs[(i + (e.key === "ArrowDown" ? 1 : bs.length - 1)) % bs.length].focus(); e.preventDefault();
        }
      });
      box.addEventListener("focusout", (e) => { if (!box.contains(e.relatedTarget)) show(false); });
      document.addEventListener("click", (e) => { if (!box.contains(e.target)) show(false); });
    });
  });
  if (lang === "en") return;

  root.classList.add("lang-wait");
  setTimeout(() => root.classList.remove("lang-wait"), 2000); // never left hidden, even if the words don't come
  const ATTRS = ["placeholder", "aria-label", "alt", "title"];
  window.figLang = (dict) => {
    // "We'll reply to {0}, usually within 24 hours.": a key with {n} matches any text there, carried into the translation
    const pats = Object.keys(dict).filter((k) => /\{\d\}/.test(k)).map((k) => [new RegExp("^" + k.split(/\{\d\}/).map((p) => p.replace(/[.*+?^$()|[\]\\{}]/g, "\\$&")).join("(.+?)") + "$"), dict[k], (k.match(/\{\d\}/g) || []).map((x) => +x[1])]);
    const tr = (s) => {
      const k = s.replace(/\s+/g, " ").trim();
      if (!k) return null;
      // a full stop or comma alone, after a link in a sentence: Chinese writes it full-width
      if (lang !== "fr" && /^[.,:;!?]$/.test(k)) return "。，：；！？"[".,:;!?".indexOf(k)];
      if (Object.prototype.hasOwnProperty.call(dict, k)) return dict[k];
      for (const [re, v, order] of pats) {
        const m = re.exec(k);
        if (m) return v.replace(/\{(\d)\}/g, (_, n) => { const x = m[order.indexOf(+n) + 1]; return tr(x) ?? x; });
      }
      return null;
    };
    const off = (el) => !el || el.closest("script, style, noscript, textarea, svg") || el.closest("[translate]")?.getAttribute("translate") === "no";
    const text = (n) => {
      if (off(n.parentElement)) return;
      const t = tr(n.data);
      if (t != null) n.data = n.data.match(/^\s*/)[0] + t + n.data.match(/\s*$/)[0];
    };
    const attrs = (el) => {
      if (off(el)) return;
      for (const a of ATTRS) { const v = el.getAttribute(a), t = v && tr(v); if (t != null && t !== v) el.setAttribute(a, t); }
    };
    const walk = (node) => {
      if (node.nodeType === 3) return text(node);
      if (node.nodeType !== 1) return;
      attrs(node);
      const w = document.createTreeWalker(node, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
      for (let n = w.nextNode(); n; n = w.nextNode()) n.nodeType === 3 ? text(n) : attrs(n);
    };
    // "interactive" comes after the whole page is read and before the deferred scripts (main.js splits the headline into letters)
    const start = () => {
      walk(root);
      const mo = new MutationObserver((rs) => {
        for (const r of rs) r.type === "childList" ? r.addedNodes.forEach(walk) : r.type === "characterData" ? text(r.target) : attrs(r.target);
        mo.takeRecords(); // our own changes
      });
      mo.observe(root, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS });
    };
    if (document.readyState === "loading") document.addEventListener("readystatechange", start, { once: true }); else start();
  };
  // ponytail: document.write keeps the words in step with the page (they're here before the body is read), at the cost of a
  // blocking request for French and Chinese visitors only; a fetch would race main.js's headline split
  document.write('<script src="/lang/' + lang + '.js"><\/script>');
})();
