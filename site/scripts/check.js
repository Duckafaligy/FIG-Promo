// node site/scripts/check.js  -- checks the email/phone parser used by the waitlist form
const assert = require("assert");
const { parseContact } = require("../js/contact.js");

assert.deepStrictEqual(parseContact(" Me@Example.com "), { email: "me@example.com" });
assert.deepStrictEqual(parseContact("905 555 0123"), { phone: "+19055550123" });
assert.deepStrictEqual(parseContact("(647) 555-0199"), { phone: "+16475550199" });
assert.deepStrictEqual(parseContact("+1 416-555-0100"), { phone: "+14165550100" });
assert.strictEqual(parseContact("555 0123"), null);
assert.strictEqual(parseContact("not@email"), null);
assert.strictEqual(parseContact("0123456789"), null);
assert.strictEqual(parseContact(""), null);
console.log("ok: contact parser");
