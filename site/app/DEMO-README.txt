FIG web app, DEMO build (preview only).

This is the app from FIG-App commit 6a2a595 (branch test/stripe-ui-2026-10-25, on top of fix/pre-merge-review-2026-10-25, which has Connect Stripe to publish).
It was built with no backend keys: it runs on fake data kept in your own browser (local storage).
Nothing is saved on a server, nothing is live, no money moves, and no email, text or payment is sent.
Photos you add stay in your browser only. Clearing the site data starts it from empty again.

NEW: Connect Stripe to publish. A new restaurant builds its page, menu and deals as DRAFTS (pill "Draft"). Anything that would publish
(Publish my page, a deal going live, switching a draft deal on, turning takeout on) opens the sheet "Connect Stripe to publish".
There is no Stripe in the demo, so that sheet has a grey "Pretend to connect Stripe (demo)" button: it plays the way back from Stripe
(Checking with Stripe..., then "You connected Stripe!" with Publish now / Turn on takeout / Done). A staff manager sees "Ask the owner to connect Stripe".

LOCKED like the real app: the diner side is closed until January 1, 2027. Guests and signed-in diners see only
"Only restaurants can use FIG for now", and Welcome offers only "I run a restaurant" and "Join the diner waitlist".
To open the diner side for your own testing, run this once in the browser console on the app page and reload:
  localStorage.setItem('fig.demo.gate','open')
and to lock it again:  localStorage.removeItem('fig.demo.gate')
(These two lines are the only switches. The demo starts LOCKED.)

What the demo cannot do (it needs the real server): invites to staff, the payment log, fee statements, insights,
reading a menu from a photo, sign-in codes by email or text, card payments, joining the waitlist with an email on the wall.

Sample places for the restaurant sign-up: type "gold", "maple" or "east" in the Location box ("sun" is a place that is
already on FIG, to see "Is this your restaurant?").
