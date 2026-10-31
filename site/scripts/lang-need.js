// Every English string the translated parts of the website show: what check.js requires in each of lang/fr.js, zh-Hans.js, zh-Hant.js.
// node site/scripts/lang-need.js prints them (one per line) for a translator.
const fs = require("fs"), path = require("path");
const { strings, scriptStrings } = require("./lang-strings.js");
const SITE = path.join(__dirname, "..");
// the scripts that write words on Home, About, Help, Contact and into the navbar, footer and cookie notice everywhere
const SCRIPTS = ["main.js", "contact-form.js", "consent.js", "fx.js", "help.js"];
function need() {
  const out = new Map(); // string -> the first file it's in
  const pages = (dir) => fs.readdirSync(path.join(SITE, dir)).filter((f) => f.endsWith(".html")).map((f) => path.join(dir, f));
  for (const f of [...pages("."), ...pages("blog")]) for (const s of strings(fs.readFileSync(path.join(SITE, f), "utf8"))) if (!out.has(s)) out.set(s, f);
  for (const f of SCRIPTS) for (const s of scriptStrings(fs.readFileSync(path.join(SITE, "js", f), "utf8"))) if (!out.has(s)) out.set(s, "js/" + f);
  return out;
}
module.exports = { need };
if (require.main === module) for (const [s] of need()) console.log(s);
