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
     "it is the founding payment, never a deposit", False),
    ("places", r"Toronto|\bGTA\b|York Region",
     "FIG is in Markham first, then Richmond Hill and Vaughan Mills", False),
    ("free-for-restaurants", r"post(ing)? deals? (on FIG )?(is|are) free|free to post|listing is free|do not need Premium|free for restaurants",
     "restaurants need a plan to go live and post deals", False),
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
        "places": "Deals across the GTA", "free-for-restaurants": "Posting deals on FIG is free", "takeout-pay-at-counter": "Takeout: pay at pickup",
    }
    for rule, text in bad.items():
        hits = check([post(sections=[("Head", f"<p>{text}</p>")])])
        assert {h[2] for h in hits} == {rule}, (rule, hits)
    good = ["Share the restaurant's link to your group chat", "the family chat", "Chatime bubble tea", "Uber Eats Premium plans 30%",
            "Restaurants can set up there today", "York University's Markham Campus", "Takeout is paid in the app when you order",
            "For dine-in you pay at the counter as usual", "Will FIG message me about flash deals?"]
    for text in good:
        assert not check([post(faq=[("Q?", text)])]), text
    assert not check([post(title="Is FIG Premium worth it?", claims_ok=["premium"])]), "claims_ok lets a deliberate mention through"
    assert check([post(dek="Open FIG on the web")]) and not check([post(dek="Open FIG on the web")], diners_open=True), "dated rules stop once FIG is open"
    assert check([post(keywords="restaurant counter code")]), "keywords are checked"
    print("blog_claims: self-check ok,", len(RULES), "rules")


if __name__ == "__main__":
    _selftest()
