// /r/<restaurant>?n=<name>&from=<first name>: a restaurant someone shared from the FIG app.
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
  var q = new URLSearchParams(location.search);
  var name = (q.get('n') || '').slice(0, 60);
  var from = (q.get('from') || '').slice(0, 30);
  var ok = /^[0-9a-f-]{36}$/i.test(id);
  var title = document.getElementById('r-title');
  var line = document.getElementById('r-line');
  var open = document.getElementById('r-open');
  if (name) title.textContent = (from ? from + ' sent you ' : 'Check out ') + name + ' on FIG';
  else if (from) title.textContent = from + ' sent you a spot on FIG';
  if (name) line.textContent = 'See ' + name + '’s live deals, claim one, and show your QR at the counter. Free for diners.';
  if (!ok) return;
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
})();
