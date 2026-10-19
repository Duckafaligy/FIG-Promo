// /r/<restaurant>?from=<first name>: a restaurant someone shared from the FIG app.
// The name on the page is always the restaurant's real one, read from FIG (a live restaurant's public row), never from the link:
// a link's ?n= could say anything under FIG's name (FIX-LIST #135, spoofing). An id that isn't a live restaurant says so.
// ?from= shows only beside a real restaurant, cleaned, and never a name that claims to be FIG.
// Once FIG is in the stores (set STORE below):
// - iPhone: phones WITH FIG never see this page (the link opens the app directly, once the domain's app-link file is
//   set up), so anyone here doesn't have it: straight to the App Store. Never try fig:// on its own: without the app,
//   Safari shows an "address is invalid" error.
// - Android: one intent link opens FIG if it's installed, else Google Play.
// Until then, the page shows who shared what, with the waitlist.
(function () {
  var STORE = { ios: '', android: '' }; // e.g. https://apps.apple.com/app/id1234567890 and https://play.google.com/store/apps/details?id=com.figtechnologies.fig
  var PACKAGE = 'com.figtechnologies.fig';
  var id = location.pathname.split('/')[2] || '';
  // a first name: letters, spaces, ' . -, 30 at most; nothing that calls itself FIG
  var from = (new URLSearchParams(location.search).get('from') || '').replace(/[^\p{L}\p{M} '’.-]/gu, '').replace(/\s+/g, ' ').trim().slice(0, 30);
  if (/fig/i.test(from)) from = '';
  var title = document.getElementById('r-title');
  var line = document.getElementById('r-line');
  var open = document.getElementById('r-open');
  var web = document.getElementById('r-web'), fromEl = document.getElementById('r-from'), bubble = document.querySelector('.r-bubble');
  var nowhere = function () {
    title.textContent = 'This link doesn’t lead to a restaurant on FIG';
    line.textContent = 'It may have been mistyped, or the restaurant isn’t on FIG right now. See the restaurants and deals that are.';
    if (web) { web.textContent = 'See what’s on FIG'; web.href = '/app/'; }
    if (bubble) bubble.hidden = true;
  };
  if (!/^[0-9a-f-]{36}$/i.test(id)) return nowhere();
  var cfg = window.FIG_CONFIG || {};
  fetch(cfg.supabaseUrl + '/rest/v1/restaurants?select=name&status=eq.approved&id=eq.' + id, { headers: { apikey: cfg.supabaseKey } })
    .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
    .then(function (rows) {
      var name = rows && rows[0] && String(rows[0].name || '').slice(0, 60);
      if (!name) return nowhere();
      title.textContent = (from ? from + ' sent you ' : 'Check out ') + name + ' on FIG';
      line.textContent = 'See ' + name + '’s live deals, claim one, and show your QR at the counter. Free for diners.';
      if (from && fromEl) fromEl.textContent = from;
      if (web) { web.textContent = 'See ' + name + ' on FIG'; web.href = '/app/r/' + id + (from ? '?from=' + encodeURIComponent(from) : ''); }
      offerApp();
    }, function () { /* no answer: the page stays general (no name, no sender), and the button still opens FIG */ });

  function offerApp() {
    var path = 'r/' + id + (from ? '?from=' + encodeURIComponent(from) : '');
    var ua = navigator.userAgent;
    if (/Android/i.test(ua)) {
      var intent = 'intent://' + path + '#Intent;scheme=fig;package=' + PACKAGE + (STORE.android ? ';S.browser_fallback_url=' + encodeURIComponent(STORE.android) : '') + ';end';
      open.href = intent;
      open.hidden = false;
      if (STORE.android) location.replace(intent);
    } else if (/iPhone|iPad|iPod/i.test(ua)) {
      open.href = 'fig://' + path; // only when they tap it themselves
      open.hidden = false;
      if (STORE.ios) location.replace(STORE.ios);
    } else {
      open.href = 'fig://' + path;
      open.hidden = false;
    }
  }
})();
