// Shows the business address lines (.fig-mail, hidden in the page) once site/js/config.js says showEmail: true.
(function () {
  var c = window.FIG_CONFIG || {};
  if (!c.showEmail) return;
  document.querySelectorAll('.fig-mail').forEach(function (e) { e.hidden = false; });
})();
