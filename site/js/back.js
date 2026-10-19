// The pages Stripe sends people back to, when it wasn't the happy ending:
// /paid?order=<id>&cancelled=1 (they backed out of paying: FIX-LIST #133) and /stripe?again=1 (the set-up link expired: #134).
(function () {
  var q = new URLSearchParams(location.search);
  var card = document.querySelector('.st-card');
  if (!card) return;
  var say = function (icon, title, lead, note, buttons) {
    card.querySelector('.st-badge').textContent = icon;
    card.querySelector('.st-badge').classList.add('go');
    card.querySelector('.st-h1').textContent = title;
    card.querySelector('.st-lead').textContent = lead;
    var n = card.querySelector('.st-note'); if (n) n.textContent = note;
    card.querySelector('.st-btns').innerHTML = buttons;
  };
  var path = location.pathname.replace(/\/$/, '');
  if (path === '/paid' && q.get('cancelled') === '1') {
    var order = /^[0-9a-f-]{36}$/i.test(q.get('order') || '') ? q.get('order') : '';
    say('×', 'Payment cancelled', 'Nothing was charged.', 'Your order is still in FIG. Open it to pay, or just leave it: nothing is sent to the restaurant until you pay.',
      '<a class="btn btn-lg" href="/app/' + (order ? 'order/' + order : '') + '">' + (order ? 'Back to your order' : 'Open FIG') + '</a><a class="btn btn-lg btn-soft" href="/help">Help center</a>');
  } else if (path === '/stripe' && q.get('again') === '1') {
    say('→', 'That Stripe link expired', 'Stripe’s set-up links only last a few minutes.', 'Open FIG, go to Settings → Get paid, and tap the button again for a fresh link. You pick up where you left off.',
      '<a class="btn btn-lg" href="/app/biz/get-paid">Open Get paid</a><a class="btn btn-lg btn-soft" href="/business-terms">Business terms</a>');
  }
})();
