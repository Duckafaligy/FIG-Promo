FIG web app, DEMO build (preview only).

This is the app from FIG-App commit 6db45cf (branch fix/owner-ui-test-2026-10-24, on top of feat/pickup-times-2026-10-24).
It was built with no backend keys: it runs on fake data kept in your own browser (local storage).
Nothing is saved on a server, nothing is live, no money moves, and no email, text or payment is sent.
Photos you add stay in your browser only. Clearing the site data starts it from empty again.

LOCKED like the real app: the diner side is closed until January 1, 2027. Guests and signed-in diners see only
"Only restaurants can use FIG for now", and Welcome offers only "I run a restaurant" and "Join the diner waitlist".
To open the diner side for your own testing, run this once in the browser console on the app page and reload:
  localStorage.setItem('fig.demo.gate','open')
and to lock it again:  localStorage.removeItem('fig.demo.gate')

What the demo cannot do (it needs the real server): invites to staff, the payment log, fee statements, insights,
reading a menu from a photo, sign-in codes by email or text, card payments, joining the waitlist with an email on the wall.

Sample places for the restaurant sign-up: type "gold", "maple" or "east" in the Location box ("sun" is a place that is
already on FIG, to see "Is this your restaurant?").
