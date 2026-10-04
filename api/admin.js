// /admin (rewritten here): the sign-in card, or the admin app once signed in. The admin HTML is only ever sent to a
// signed-in browser; nothing about it ships with the public site.
const { signedIn, send } = require("./_lib/auth");
const { signInPage, appPage } = require("./_lib/pages");

module.exports = (req, res) => send(res, 200, signedIn(req) ? appPage() : signInPage());
