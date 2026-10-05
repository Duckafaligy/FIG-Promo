// /r/<restaurant>?n=<name>&from=<first name>: a restaurant someone shared from the FIG app. Phones that have FIG open it
// there (fig://r/<id>); everyone else sees who shared what, and how to get FIG.
(function () {
  var id = location.pathname.split('/')[2] || '';
  var q = new URLSearchParams(location.search);
  var name = (q.get('n') || '').slice(0, 60);
  var from = (q.get('from') || '').slice(0, 30);
  var title = document.getElementById('r-title');
  var line = document.getElementById('r-line');
  var open = document.getElementById('r-open');
  if (name) title.textContent = (from ? from + ' sent you ' : 'Check out ') + name + ' on FIG';
  else if (from) title.textContent = from + ' sent you a spot on FIG';
  if (name) line.textContent = 'See ' + name + '’s live deals, claim one, and show your QR at the counter. Free for diners.';
  if (/^[0-9a-f-]{36}$/i.test(id)) {
    var app = 'fig://r/' + id + (from ? '?from=' + encodeURIComponent(from) : '');
    open.href = app;
    open.hidden = false;
    if (/iPhone|iPad|Android/i.test(navigator.userAgent)) location.href = app; // opens FIG if it's installed; otherwise nothing happens
  }
})();
