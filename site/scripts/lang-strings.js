// The English strings js/site-lang.js would look up on a page, read the same way it reads them in the browser:
// every text node (whitespace squeezed, trimmed) and the placeholder, aria-label, alt and title attributes, outside
// <script>, <style>, <noscript>, <svg> and anything under translate="no"; plus the page's <title>. A string with fewer
// than 2 letters (a number, a price, "·") is never looked up. check.js uses this to require a translation for each one.
const ENT = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", middot: "·", rarr: "→", larr: "←", lsaquo: "‹", rsaquo: "›",
  check: "✓", times: "×", minus: "−", copy: "©", mdash: "—", ndash: "–", hellip: "…", rsquo: "’", lsquo: "‘", ldquo: "“", rdquo: "”" };
const decode = (s) => s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, n) => {
  if (n[0] === "#") return String.fromCodePoint(n[1].toLowerCase() === "x" ? parseInt(n.slice(2), 16) : +n.slice(1));
  if (!(n in ENT)) throw new Error("lang-strings.js: unknown entity " + m);
  return ENT[n];
});
const key = (s) => s.replace(/\s+/g, " ").trim();
const wanted = (k) => (k.match(/[A-Za-z]/g) || []).length >= 2;
const VOID = new Set("area base br col embed hr img input link meta source track wbr".split(" "));
const RAW = new Set(["script", "style", "noscript", "textarea"]);
const ATTRS = ["placeholder", "aria-label", "alt", "title"];

function strings(html) {
  const out = new Set();
  const add = (s) => { const k = key(decode(s)); if (wanted(k)) out.add(k); };
  const t = /<title>([\s\S]*?)<\/title>/.exec(html);
  if (t && !/<main\b[^>]*translate="no"/.test(html)) add(t[1]); // a page kept in English keeps its English title
  const body = html.slice(html.search(/<body[\s>]/));
  const stack = []; // [tag, skip]
  const skipping = () => stack.length && stack[stack.length - 1][1];
  const re = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][\w-]*)((?:\s+[^\s=>\/]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(body))) {
    if (m[5] !== undefined) { if (!skipping()) add(m[5]); continue; }
    if (!m[2]) continue; // a comment
    const tag = m[2].toLowerCase();
    if (m[1]) { // </tag>: close up to the matching one
      const i = stack.map((x) => x[0]).lastIndexOf(tag);
      if (i >= 0) stack.length = i;
      continue;
    }
    const attrs = {};
    for (const a of m[3].matchAll(/([^\s=>\/]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) attrs[a[1].toLowerCase()] = a[2] ?? a[3] ?? a[4] ?? "";
    const parentSkip = skipping();
    const skip = tag === "svg" || (attrs.translate === "no") || (attrs.translate === "yes" ? false : parentSkip);
    if (!skip) for (const a of ATTRS) if (a in attrs) add(attrs[a]);
    if (RAW.has(tag)) { // its text is never a text node the page shows (noscript: with scripts on), so jump past it
      const end = body.toLowerCase().indexOf("</" + tag, re.lastIndex);
      re.lastIndex = end < 0 ? body.length : end;
      continue;
    }
    if (!VOID.has(tag) && !m[4]) stack.push([tag, skip]);
  }
  return out;
}

// the words the site's scripts write onto translated pages (messages, the cookie notice, the marquee, the chat):
// every quoted or `template` literal that reads like words, comments left out; ${...} becomes {0}, {1}... (as the dictionaries write it)
const NOT_WORDS = /^(Content-Type|America\/Toronto|Escape)$/;
function scriptStrings(js) {
  const out = new Set();
  js = js.replace(/\/\*[\s\S]*?\*\//g, "").replace(/(^|[\s;{}(),])\/\/[^\n]*/g, "$1");
  for (const m of js.matchAll(/"((?:[^"\\\n]|\\.)*)"|'((?:[^'\\\n]|\\.)*)'|`((?:[^`\\]|\\.)*)`/g)) {
    let s = (m[1] ?? m[2] ?? m[3]).replace(/\\(.)/g, "$1");
    if (m[3] !== undefined) { let n = 0; s = s.replace(/\$\{(?:[^{}]|\{[^}]*\})*\}/g, () => `{${n++}}`); }
    if (/<[a-z]/i.test(s)) { for (const k of strings("<body>" + s)) out.add(k); continue; } // a bit of HTML
    const k = key(s);
    if (!wanted(k) || NOT_WORDS.test(k)) continue;
    // words: starts with a capital letter (or {n}), and isn't code, a URL, a CSS value or a camelCase name
    if (/^(\{\d\}|[A-Z][a-z]|FIG\b)/.test(k) && !/[=;(){}\[\]<>|]|\/\/|\b(px|ms)\b|^[A-Z][a-z]+[A-Z]|^\S*\/\S*$/.test(k.replace(/\{\d\}/g, ""))) out.add(k);
  }
  return out;
}

module.exports = { strings, scriptStrings, key };
