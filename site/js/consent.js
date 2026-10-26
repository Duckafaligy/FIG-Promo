// The website's cookie choice (REVIEW 2026-10-24 E2: Quebec's law 25 and PIPEDA expect opt-in for analytics cookies).
// Google Analytics loads ONLY after "Accept" is saved in localStorage["fig.consent"] ("granted" | "denied"). With no answer, or after
// "No thanks", nothing from Google loads and no _ga cookie is set. Vercel Web Analytics sets no cookies and is separate.
// This file builds the notice itself (a labelled region at the bottom, over the content and under the nav, no layout shift), and
// any [data-cookie-settings] button (the footer's) opens it again. "No thanks" after "Accept" also deletes the _ga cookies.
// The /app web app has no analytics and doesn't load this.
(() => {
  const ID = "G-7L25CWPZ23", KEY = "fig.consent", OFF = "ga-disable-" + ID;
  const read = () => { try { const v = localStorage.getItem(KEY); return v === "granted" || v === "denied" ? v : null; } catch { return null; } };
  const save = (v) => { try { localStorage.setItem(KEY, v); } catch { /* no storage (private window): it asks again on the next page */ } };
  let loaded = false, box = null, opener = null;

  function on() {
    window[OFF] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    const gtag = window.gtag = function () { window.dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", ID, { allow_google_signals: false, allow_ad_personalization_signals: false }); // counting visits only, never Google's advertising features
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
    document.head.append(s);
  }

  // withdrawing: stop anything still to be sent from this page and delete the cookies Google Analytics set (on this host and the ones above it)
  function off() {
    window[OFF] = true;
    const parts = location.hostname.split("."), where = [""];
    for (let i = 0; i < parts.length - 1; i++) where.push(parts.slice(i).join("."), "." + parts.slice(i).join("."));
    document.cookie.split(";").map((c) => c.split("=")[0].trim()).filter((n) => /^_ga(_|$)|^_gid$|^_gat/.test(n))
      .forEach((n) => where.forEach((d) => { document.cookie = n + "=; Max-Age=0; path=/" + (d ? "; domain=" + d : ""); }));
  }

  function build() {
    box = document.createElement("section");
    box.className = "ck"; box.id = "cookie-notice"; box.hidden = true; box.tabIndex = -1;
    box.setAttribute("role", "region"); box.setAttribute("aria-label", "Cookie choice");
    box.innerHTML = '<p>FIG would like to count visits with Google Analytics cookies. They stay off unless you accept. We never use advertising cookies. <a href="/cookies">More about cookies</a></p>' +
      '<p class="ck-now" hidden></p>' +
      '<div class="ck-btns"><button class="btn btn-sm btn-ink" type="button" data-ck="granted">Accept</button><button class="btn btn-sm btn-ink" type="button" data-ck="denied">No thanks</button></div>';
    box.addEventListener("click", (e) => { const b = e.target.closest("[data-ck]"); if (b) choose(b.dataset.ck); });
    const skip = document.querySelector(".skip"); // right after "Skip to content", so a keyboard user meets it first
    skip ? skip.after(box) : document.body.prepend(box);
  }

  function open(from) {
    if (!box) build();
    const now = read(), line = box.querySelector(".ck-now");
    line.hidden = !now;
    line.textContent = now ? "Right now: Google Analytics is " + (now === "granted" ? "on." : "off.") : "";
    box.hidden = false;
    void box.offsetWidth; // the fade starts from hidden
    box.classList.add("in");
    if (from) { opener = from; box.focus(); }
  }

  function close() {
    if (box) { box.classList.remove("in"); box.hidden = true; }
    if (opener) { opener.focus(); opener = null; }
  }

  function choose(v) {
    save(v);
    if (v === "granted") on(); else off();
    close();
  }

  document.querySelectorAll("[data-cookie-settings]").forEach((b) => { b.hidden = false; }); // the footer button shows only where it works
  document.addEventListener("click", (e) => { const b = e.target.closest("[data-cookie-settings]"); if (b) open(b); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && box && !box.hidden && read()) close(); }); // looking at a choice already made: leave it as it is

  const saved = read();
  if (saved === "granted") on();
  else if (!saved) open();
})();
