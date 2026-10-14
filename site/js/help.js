// Help center search (UI pass 2026-10-14): filters the questions as you type, opens the ones that match, hides sections with
// none, and says "No match. Message us" when nothing fits. Clearing the box puts everything back.
(function () {
  var box = document.getElementById('help-q');
  var none = document.getElementById('help-none');
  if (!box) return;
  var items = Array.prototype.slice.call(document.querySelectorAll('details.qa'));
  var opened = items.map(function (d) { return d.open; });
  var plain = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  var words = items.map(function (d) { return plain(d.textContent || ''); });
  box.addEventListener('input', function () {
    var q = plain(box.value.trim());
    var parts = q.split(/\s+/).filter(Boolean);
    var shown = 0;
    items.forEach(function (d, i) {
      var hit = !parts.length || parts.every(function (w) { return words[i].indexOf(w) !== -1; });
      d.hidden = !hit;
      d.open = parts.length ? hit : opened[i];
      if (hit) shown++;
    });
    document.querySelectorAll('.faq').forEach(function (sec) {
      var any = sec.querySelector('details.qa:not([hidden])');
      sec.closest('section').hidden = !any && parts.length > 0;
    });
    if (none) none.hidden = !parts.length || shown > 0;
  });
})();
