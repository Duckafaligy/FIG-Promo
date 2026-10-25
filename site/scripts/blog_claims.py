"""The blog's claims guard (REVIEW 2026-10-24 E3): stops a post from saying what FIG no longer offers, or what isn't true yet.

pages.py calls enforce(posts, DINERS_OPEN) on every post it is about to build (live or due; the batch writer's
`FIG_NOW=2030-01-01T00:00:00Z python3 site/scripts/pages.py` makes every queued post due, so it checks them all). If any post
says something below, pages.py exits non-zero with a list: post, field, rule, excerpt. The publisher job runs pages.py and stops
on a failure, so a post that breaks a rule is never published.

A post that needs to mention one of these on purpose (say, a post explaining why FIG has no Premium) lists the rule's name in its
dict: claims_ok=["premium"]. The names are the first column of RULES.

Texts checked: title, dek, desc, seo, keywords, key points, every section heading and body, every FAQ question and answer.
Run `python site/scripts/blog_claims.py` to run the self-check of the rules themselves.
"""
import html
import re
import sys

# (name, pattern, why it's wrong today, dated). A "dated" rule is about the diner side not being open yet: it stops applying once
# DINERS_OPEN is True in pages.py (the day FIG opens to diners). All patterns are case-insensitive and run on plain text with
# curly apostrophes made straight.
RULES = [
    ("premium", r"FIG Premium|Premium badge|\$50(\.00)?\s*(a|per|/)\s*(year|yr)\b|\$50\s*(annual|yearly)",
     "FIG Premium is hidden", False),
    ("announcements", r"deal announcements?|announcements? every|(send|post|make|write)s? an announcement",
     "deal announcements are hidden", False),
    ("messaging", r"(?<!group )(?<!family )\bchat\b|direct messages?|message (a|the|your) restaurant|messag\w+ (from|with) (the )?(app|diner|restaurant)|in-app messag\w+|diner messages?",
     "messaging between diners and restaurants is hidden (a link shared to a group chat is fine)", False),
    ("counter-code", r"counter code|scan the counter|scans? the restaurant'?s? (own )?(counter )?code",
     "the Counter code is hidden: staff scan the diner's code", False),
    ("stamps", r"\bstamps?\b|passport|loyalty points?",
     "FIG has no stamps, passport or points", False),
    ("works-today", r"works today|web app works|use FIG (on the web )?(at \S+ )?(today|now)|open FIG on the web|explore the map( and restaurants)? (now|today)",
     "FIG isn't open to diners until January 1, 2027 (diners join the waitlist)", True),
    ("deposit", r"\bdeposits?\b",
     "restaurants pay nothing up front: no deposit and no founding payment", False),
    ("places", r"Toronto|\bGTA\b|York Region",
     "FIG is in Markham first, then Richmond Hill and Vaughan Mills", False),
    # 2026-10-24 (the owner): restaurants are completely free. FIG earns only on takeout paid in the app. No prices, no plans, no founding offer.
    ("restaurant-price", r"\$\s?(49\.99|29\.99|299\.99)\b",
     "restaurants pay no plan: FIG is free for them and earns only on takeout paid in the app", False),
    ("founding-offer", r"founding[- ](payment|price|prices|plan|plans|restaurants?|offer|rate|rates|deal)|lock(ing)? in (a |your |the )?(founding|early|lower|launch)",
     "there is no founding payment, price or plan: restaurants are free", False),
    ("restaurant-plan", r"\b(flat|regular|one|annual|yearly|monthly) (restaurant )?plan\b|\bFIG(\u2019|')?s plan\b|\b(choose|pick|buy|upgrade to|sign up for|pay for) (a|an|your|the) (paid |flat |regular |monthly |yearly |annual )?plan\b|\b(needs?|needed|requires?) (a|an|your) (paid |flat |regular )?plan to\b|\bwithout a plan\b|(go(es)? live|going live)[^.<]{0,30}\bplan\b|\byour plan (covers|includes|renews|ends)\b",
     "FIG has no plan for restaurants to choose or pay for: it is free", False),
    ("billing", r"billing (starts?|begins?|date|notice|has started)|\b(starts?|begins?|before|until) billing\b|written notice (before|that)",
     "FIG does not bill restaurants: there is no billing date or notice", False),
    ("plan-refund", r"March 1,? 2027|14[- ]day (plan )?refund|within 14 days of (your |the )?(first )?pay|refunds?[^.<]{0,40}first payment",
     "there is no plan to refund (the March 1, 2027 rule is gone with the founding payment)", False),
    ("takeout-pay-at-counter", r"takeout[^.<]{0,40}\bpay (at|when)\b[^.<]{0,25}(counter|pickup|arriv)|make it when (they|you) arrive|pay at (the )?pickup",
     "takeout is paid in the app", False),
]
_COMPILED = [(n, re.compile(p, re.I), why, dated) for n, p, why, dated in RULES]


def _plain(text):
    """A field as the reader sees it: no tags, entities decoded, straight apostrophes, one space between words."""
    text = html.unescape(re.sub(r"<[^>]+>", " ", text)).replace("’", "'")
    return re.sub(r"\s+", " ", text)


def _fields(post):
    yield "title", post["title"]
    yield "dek", post["dek"]
    for key in ("desc", "seo"):
        if post.get(key):
            yield key, post[key]
    yield "keywords", post["keywords"]
    for i, point in enumerate(list(post.get("points", [])) + list(post.get("takeaways", []))):
        yield f"points[{i}]", point
    for heading, body in post["sections"]:
        yield f"heading '{heading}'", heading
        yield f"section '{heading}'", body
    for q, a in post["faq"]:
        yield f"faq '{q[:50]}'", q
        yield f"faq '{q[:50]}' (answer)", a


def check(posts, diners_open=False):
    """The hits in these posts: a list of (slug, field, rule, why, excerpt)."""
    hits = []
    for post in posts:
        ok = set(post.get("claims_ok", ()))
        for field, text in _fields(post):
            plain = _plain(text)
            for name, rx, why, dated in _COMPILED:
                if name in ok or (dated and diners_open):
                    continue
                for m in rx.finditer(plain):
                    hits.append((post["slug"], field, name, why, plain[max(0, m.start() - 50):m.end() + 50]))
    return hits


def enforce(posts, diners_open=False):
    hits = check(posts, diners_open)
    if hits:
        lines = [f"  {slug} | {field} | {name} | ...{excerpt}... ({why})" for slug, field, name, why, excerpt in hits]
        sys.exit(f"blog_claims: {len(hits)} claim(s) FIG doesn't make today, in posts that are about to be built:\n" + "\n".join(lines)
                 + "\nFix the words; for a deliberate mention add claims_ok=[\"<rule>\"] to that post (see site/scripts/blog_claims.py).")


def _selftest():
    def post(**kw):
        base = dict(slug="t", title="A title", dek="A dek", keywords="a, b", points=["A point"], sections=[("Head", "<p>Body</p>")], faq=[("Q?", "A.")])
        base.update(kw)
        return base
    bad = {
        "premium": "Is FIG Premium worth $50 a year?", "announcements": "Send an announcement to every diner",
        "messaging": "You can message the restaurant from the app", "counter-code": "or scan the restaurant’s own counter code",
        "stamps": "Collect a stamp at every visit", "works-today": "The web app works today", "deposit": "Pay a founding deposit",
        "places": "Deals across the GTA", "takeout-pay-at-counter": "Takeout: pay at pickup",
        "restaurant-price": "Restaurants pay $29.99 a month", "founding-offer": "Join as a founding restaurant before launch",
        "restaurant-plan": "FIG charges one flat plan", "billing": "Before billing starts you pay nothing", "plan-refund": "Refunded in full by March 1, 2027",
    }
    # each bad text above must trip exactly its own rule, and a few more phrasings must trip too
    more = {"restaurant-price": ["The founding payment is $49.99 once", "$299.99 a year"], "founding-offer": ["a founding price that is always lower", "the founding payment"],
            "restaurant-plan": ["Choose a plan", "Going live needs a plan", "Without a plan you cannot post", "your plan covers every location", "a monthly plan"],
            "billing": ["FIG starts billing on a date it tells you", "a billing notice"], "plan-refund": ["a refund within 14 days of your first payment", "the 14-day refund"]}
    for rule, texts in more.items():
        for text in texts:
            assert rule in {h[2] for h in check([post(sections=[("Head", f"<p>{text}</p>")])])}, (rule, text)
    for rule, text in bad.items():
        hits = check([post(sections=[("Head", f"<p>{text}</p>")])])
        assert {h[2] for h in hits} == {rule}, (rule, hits)
    good = ["Share the restaurant's link to your group chat", "the family chat", "Chatime bubble tea", "Uber Eats Premium plans 30%",
            "Restaurants can set up there today", "York University's Markham Campus", "Takeout is paid in the app when you order",
            "For dine-in you pay at the counter as usual", "Will FIG message me about flash deals?",
            "Posting deals on FIG is free", "FIG is free for restaurants", "Join the waitlist: founding members get in first", "the 25% commission plan", "Delivery, 30% plan $9.00",
            "Uber Eats lists marketplace plans at 20%", "A ten-minute training plan", "You need a plan for the evening", "a date night plan, with the math", "an 8% to 10% pickup plan",
            "choose a table", "Plan your visit", "a $12 starter and a $22 main", "The $1.50 FIG fee", "Stripe charges 2.9% + $0.30", "billing address"]
    for text in good:
        assert not check([post(faq=[("Q?", text)])]), text
    assert not check([post(title="Is FIG Premium worth it?", claims_ok=["premium"])]), "claims_ok lets a deliberate mention through"
    assert check([post(dek="Open FIG on the web")]) and not check([post(dek="Open FIG on the web")], diners_open=True), "dated rules stop once FIG is open"
    assert check([post(keywords="restaurant counter code")]), "keywords are checked"
    print("blog_claims: self-check ok,", len(RULES), "rules")


if __name__ == "__main__":
    _selftest()
