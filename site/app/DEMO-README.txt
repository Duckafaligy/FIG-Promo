FIG web app, DEMO build (preview only).

This is the app from FIG-App commit e5d4337 (branch fix/owner-ui-test-2026-10-24, on top of feat/pickup-times-2026-10-24).
It was built with no backend keys: it runs on fake data kept in your own browser (local storage).
Nothing is saved on a server, nothing is live, no money moves, and no email, text or payment is sent.
Photos you add stay in your browser only. Clearing the site data starts it from empty again.

What the demo cannot do (it needs the real server): invites to staff, the payment log, fee statements, insights,
reading a menu from a photo, sign-in codes by email or text, card payments.

Sample places for the restaurant sign-up: type "gold", "maple" or "east" in the Location box ("sun" is a place that is
already on FIG, to see "Is this your restaurant?").
To see the wording used while diners are not allowed in yet, run this once in the browser console on the app page and reload:
  localStorage.setItem('fig.demo.gate','closed')
and to go back to the open wording:  localStorage.removeItem('fig.demo.gate')
