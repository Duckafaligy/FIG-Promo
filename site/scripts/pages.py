"""Builds the whole site around index.html: nav, footer, every extra page, sitemap.xml, robots.txt and the web manifest.

run: python site/scripts/pages.py
- Legal pages come from legal.json (exported from the app's src/content/legal.ts, so they match the app word for word).
- Nav and footer are written into index.html too, so every page shares them.
- Sections that also live on the home page (how it works, features, restaurants) are copied from index.html, so they never drift.
- SITE_URL is the address search engines see: change it once figpromo.com is connected.
"""
import datetime, hashlib, html, json, os, pathlib, re, sys, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import ABOUT, ABOUT_FAQ, POSTS
from posts import GROUPS

# every post belongs to exactly one of the blog's groups (FIX-LIST #145): a missing or unknown one stops the build, so no post
# (a queued one included) can go out ungrouped
_bad = [x["slug"] for x in POSTS if x.get("group") not in {g for g, _, _ in GROUPS}]
if _bad:
    sys.exit(f"pages.py: these posts have no group (or one that isn't in GROUPS): {', '.join(_bad)}")

SITE_URL = "https://fig-promo.vercel.app"
SITE = pathlib.Path(__file__).resolve().parents[1]
ROOT = SITE.parent
index = (SITE / "index.html").read_text(encoding="utf-8")
SPRITE = re.search(r'<svg width="0" height="0".*?</svg>', index, re.S).group(0)
MEGA = re.search(r'<div class="mega".*?Save fast\.</span>\s*</div>', index, re.S).group(0)
STORES = re.search(r'<div class="badges small">.*?</div>', index, re.S).group(0)
SECTION = lambda sid: re.search(rf'<section class="section[^"]*" id="{sid}">.*?</section>', index, re.S).group(0)
e = html.escape
BASE_KW = "FIG, FIG app, restaurant deals Markham, Markham restaurants, food deals Ontario, local restaurant deals app"
PAGES = []  # (path, title, group) for sitemap.xml and the site map page
HIDDEN = {"404", "r", "paid", "stripe", "premium-on"}  # not indexed, no breadcrumbs, not in the sitemap

# Scheduled posts (user 2026-10-14: "Schedule + reviewed batches"): a post with `publish_at` (ISO 8601 with its offset) is
# left out of everything until then: no page, not in the blog, its topics, "Keep reading", the feed, the sitemap, llms.txt or
# any structured data. FIG_NOW (ISO) stands in for the clock in tests. An hourly job runs this at the four slots.
NOW = datetime.datetime.fromisoformat(os.environ["FIG_NOW"]) if os.environ.get("FIG_NOW") else datetime.datetime.now(datetime.timezone.utc)
if NOW.tzinfo is None:
    NOW = NOW.replace(tzinfo=datetime.timezone.utc)


# The team's overrides from the admin's Blog page (user 2026-10-14: "if I don't like a post I can delete it"): a slug in
# `hidden` is taken down (left out exactly like a queued post), `publish_at[slug]` replaces the post's own time. Read with the
# public key the website already ships (js/config.js); the last good answer is kept in blog_overrides.cache.json, used when the
# database can't be reached; with neither, no overrides. FIG_BLOG_OVERRIDES (a JSON file) stands in for the network in tests.
def _overrides():
    cache = pathlib.Path(__file__).with_name("blog_overrides.cache.json")
    if os.environ.get("FIG_BLOG_OVERRIDES"):
        return json.loads(pathlib.Path(os.environ["FIG_BLOG_OVERRIDES"]).read_text(encoding="utf-8"))
    try:
        cfg = (SITE / "js" / "config.js").read_text(encoding="utf-8")
        url, key = re.search(r'supabaseUrl:\s*"([^"]+)"', cfg).group(1), re.search(r'supabaseKey:\s*"([^"]+)"', cfg).group(1)
        req = urllib.request.Request(url + "/rest/v1/rpc/blog_overrides", data=b"{}", method="POST",
                                     headers={"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as r:
            ov = json.load(r)
        if not isinstance(ov, dict):
            raise ValueError("not an object")
        ov = {"hidden": sorted(set(ov.get("hidden") or [])), "publish_at": dict(sorted((ov.get("publish_at") or {}).items()))}
        text = json.dumps(ov, indent=1) + "\n"
        if not cache.exists() or cache.read_text(encoding="utf-8") != text:
            cache.write_text(text, encoding="utf-8", newline="\n")
        return ov
    except Exception as err:  # never fail the build over this
        print(f"blog: WARNING overrides not reachable ({err}); using the last saved ones", file=sys.stderr)
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            return {}


_ov = _overrides()
TAKEN_DOWN = set(_ov.get("hidden") or [])
for _p in POSTS:
    _p["source_publish_at"] = _p.get("publish_at")
    if _p["slug"] in (_ov.get("publish_at") or {}):
        _p["publish_at"] = _ov["publish_at"][_p["slug"]]
        if not _p["publish_at"]:
            del _p["publish_at"]
live = lambda post: post["slug"] not in TAKEN_DOWN and (not post.get("publish_at") or datetime.datetime.fromisoformat(post["publish_at"]) <= NOW)
# every post that isn't live (queued or taken down): links to it are plain text on every page until it is
NOT_LIVE = sorted(x["slug"] for x in POSTS if not live(x))
_unlink = (lambda h: re.sub(rf'<a\s[^>]*href="/blog/(?:{"|".join(re.escape(x) for x in NOT_LIVE)})(?:[#?][^"]*)?"[^>]*>(.*?)</a>', lambda m: m.group(1), h, flags=re.S)) if NOT_LIVE else (lambda h: h)

# what the admin's Blog page lists (it reads this file from GitHub): every post, live, queued or taken down, newest first.
# No clock in it, so it only changes when the posts or the overrides do.
_words = lambda post: len(re.sub(r"<[^>]+>", " ", " ".join(t for _, t in post["sections"])).split())
_manifest = {"generated": max((x["date"] for x in POSTS), default=""), "groups": [g for g, _, _ in GROUPS], "posts": [
    {"slug": x["slug"], "title": x["title"], "topic": x["topic"], "group": x["group"], "date": x["date"], "publish_at": x["source_publish_at"],
     "status": "taken-down" if x["slug"] in TAKEN_DOWN else "live" if live(x) else "queued", "words": _words(x), "dek": x["dek"]}
    for x in sorted(POSTS, key=lambda x: (x["date"], x.get("source_publish_at") or ""), reverse=True)]}
_mtext = json.dumps(_manifest, indent=1, ensure_ascii=False) + "\n"
_mpath = pathlib.Path(__file__).with_name("blog_manifest.json")
if not _mpath.exists() or _mpath.read_text(encoding="utf-8") != _mtext:
    _mpath.write_text(_mtext, encoding="utf-8", newline="\n")

# the nav is Home's own (index.html, Home v2 2026-10-13): every link scrolls to a section of Home, and its button opens the
# web app. Every other page copies it as it is, so the two never drift.
NAV = re.search(r'<header class="nav".*?</header>', index, re.S).group(0)
NAV_LINKS = re.findall(r'<a href="(/#[a-z]+)"[^>]*>([^<]+)</a>', re.search(r'<nav class="nav-links".*?</nav>', NAV, re.S).group(0))


def nav(current=""):
    return NAV


FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/"><svg class="logo"><use href="#logo"/></svg><span>FIG</span></a>
        <p>Live deals from local restaurants, on a map. Starting in Markham, Ontario. Expanding to Richmond Hill and Vaughan Mills.</p>
        {STORES}
      </div>
      <div class="foot-cols">
        <div><p class="foot-h">Diners</p><a href="/#how">How it works</a><a href="/#features">Features</a><a href="/#catch">Tutorial</a><a href="/help">Help center</a></div>
        <div><p class="foot-h">Restaurants</p><a href="/#owners">Pricing</a><a href="/blog/how-fig-makes-money">How pricing works</a><a href="/business-terms">Business terms</a><a href="/help#restaurants">Restaurant help</a></div>
        <div><p class="foot-h">Company</p><a href="/about">About</a><a href="/blog">Blog</a><a href="/contact">Contact</a></div>
        <div><p class="foot-h">Legal</p><a href="/terms">Terms of service</a><a href="/privacy">Privacy policy</a><a href="/cookies">Cookies</a></div>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 FIG · Markham, Ontario</span>
      <span>App screens show example restaurants and deals. Map data © OpenStreetMap contributors, OpenFreeMap. App Store is a trademark of Apple Inc. Google Play is a trademark of Google LLC.</span>
    </div>
  </div>
</footer>'''


def head_meta(path, title, desc, extra="", og_type="website", image="/assets/og.png"):
    url = SITE_URL + ("" if path == "/" else path)
    return f'''  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="FIG">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE_URL}{image}">
  <link rel="alternate" type="application/rss+xml" title="The FIG blog" href="/feed.xml">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">{extra}'''


# ---------- the home page gets the same nav, footer and head tags ----------
index = re.sub(r'<footer class="foot">.*?</footer>', FOOTER, index, count=1, flags=re.S)
index = re.sub(r'\n  <!-- seo -->.*?<!-- /seo -->', "", index, flags=re.S)
ORG = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "name": "FIG", "url": SITE_URL, "logo": SITE_URL + "/assets/icons/icon-512.png",
     "address": {"@type": "PostalAddress", "addressLocality": "Markham", "addressRegion": "ON", "addressCountry": "CA"}},
    {"@type": "WebSite", "name": "FIG", "url": SITE_URL},
    {"@type": "MobileApplication", "name": "FIG", "operatingSystem": "iOS, Android", "applicationCategory": "LifestyleApplication",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"}}]})
index = index.replace('  <meta name="theme-color"', '  <!-- seo -->\n' + head_meta("/", "FIG · Restaurant deals in Markham, Ontario", "Markham restaurants: post deals for your quiet hours and diners find you on the map. No commission on dine-in. Founding restaurants: $9.99 a month or $59.99 for the first year. Diners join January 1, 2027.",
                      f'\n  <script type="application/ld+json">{ORG}</script>') + '\n  <!-- /seo -->\n  <meta name="theme-color"', 1)

# ---------- Home's "Good to know": the blog's groups as cards (FIX-LIST #145), from the same GROUPS as /blog ----------
# Each card's loop (site/assets/loops/<group>.mp4 + -poster.webp) shows only once its files exist: the poster first, the video
# loaded and played only while it's on screen (main.js), never with reduced motion. A loop over ~400 KB stops the build.
LOOPS = SITE / "assets" / "loops"
def _vis(slug):
    mp4, poster = LOOPS / f"{slug}.mp4", LOOPS / f"{slug}-poster.webp"
    if mp4.exists() and mp4.stat().st_size > 450_000:
        sys.exit(f"pages.py: {mp4.name} is {mp4.stat().st_size // 1000} KB; a Home loop must stay under ~400 KB")
    if mp4.exists() and poster.exists():
        return (f'<video class="gtk-loop" muted loop playsinline preload="none" data-poster="/assets/loops/{slug}-poster.webp" '
                f'data-loop="/assets/loops/{slug}.mp4" disablepictureinpicture disableremoteplayback></video>')
    if poster.exists():
        return f'<img src="/assets/loops/{slug}-poster.webp" alt="" width="800" height="500" loading="lazy">'
    return '<svg class="gtk-mark"><use href="#logo"/></svg>'
GTK = ("<!-- good-to-know: written by pages.py from posts.py GROUPS (FIX-LIST #145) -->\n"
       '  <section class="section ice gtk" id="good-to-know">\n    <div class="wrap">\n'
       '      <h2 class="h2 reveal">Good to know</h2>\n      <p class="body gtk-sub reveal">Short reads for diners and restaurants.</p>\n'
       '      <div class="gtk-grid reveal">' + "".join(
           f'<a class="gtk-card" href="/blog#{g}"><span class="gtk-vis" aria-hidden="true">{_vis(g)}</span>'
           f'<div class="gtk-text"><h3>{e(t)}</h3><p>{e(d)}</p><span class="gtk-more">Learn more <i aria-hidden="true">→</i></span></div></a>' for g, t, d in GROUPS) + "</div>\n"
       '      <div class="gtk-wide reveal"><div><h3>Everything we write, in one place.</h3><nav class="gtk-pills" aria-label="Blog groups">'
       + "".join(f'<a href="/blog#{g}">{e(t)}</a>' for g, t, _ in GROUPS) + "</nav></div>"
       '<a class="btn btn-lg btn-ink gtk-all" href="/blog">Read the blog <span aria-hidden="true">→</span></a></div>\n'
       "    </div>\n  </section>\n  <!-- /good-to-know -->")
index, _n = re.subn(r'<!-- good-to-know.*?<!-- /good-to-know -->', lambda m: GTK, index, flags=re.S)
if _n != 1:
    sys.exit("pages.py: index.html needs one <!-- good-to-know --> … <!-- /good-to-know --> block (between #catch and #faq)")
(SITE / "index.html").write_text(index, encoding="utf-8")
PAGES.append(("/", "Home", "Main"))


def ld(obj):
    return '\n  <script type="application/ld+json">' + json.dumps(obj) + "</script>"


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, "item": SITE_URL + u} for k, (n, u) in enumerate(items)]}


BLOG_JS = '\n<script src="/js/blog-state.js" defer></script>'  # blog pages: hides a post taken down since the build


# chrome="back": no site navbar, the page brings its own way back (the legal pages, user 2026-10-14: "remove it, and only add a back to landing page")
def page(slug, title, desc, body, group="More", wide=False, extra_head="", keywords="", og_type="website", trail=None, image="/assets/og.png", chrome="nav", seo=None):
    path = "/" + slug
    # the search title: " · FIG" only while it fits in 60 (FIX-LIST #106); seo= is a shorter one for a long headline
    full = (seo or title) + (" · FIG" if len(seo or title) + 6 <= 60 else "")
    if slug not in HIDDEN:
        extra_head = ld(crumbs([("Home", "/")] + (trail or []) + [(title, path)])) + extra_head
    current = path if path in dict(NAV_LINKS) else ""
    out = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(full)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="keywords" content="{e(keywords or BASE_KW)}">
  <meta name="robots" content="{'noindex' if slug in HIDDEN else 'index, follow, max-image-preview:large'}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{head_meta(path, full, desc, extra_head, og_type, image)}
  <link rel="stylesheet" href="/css/site.css">
  <link rel="stylesheet" href="/css/pages.css">
</head>
<body class="sub">
<a class="skip" href="#main">Skip to content</a>
{SPRITE}
<div class="bg" aria-hidden="true"><div class="bg-grid"></div></div>
{nav(current) if chrome == 'nav' else ''}
<main id="main"{' class="page"' if wide else ' class="wrap doc"'}{f' data-post="{slug[5:]}"' if slug.startswith("blog/") else ""}>
{body}
</main>
{FOOTER}
{MEGA if chrome == 'nav' else ''}
<script src="/js/fx.js" defer></script>
<script src="/js/sub.js" defer></script>{BLOG_JS if slug == "blog" or slug.startswith("blog/") else ""}
</body>
</html>
'''
    out = _unlink(out)
    p = SITE / (slug + ".html")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")
    if slug not in HIDDEN:
        PAGES.append((path, title, group))


# ---------- the light v2 pages (2026-10-13, from the Paper file "FIG Website · Pages"); their styles are in css/pages.css
slug_id = lambda h: re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")


def hero(title, lead="", side="", cls=""):
    """A page's top: a big title, a line under it, and something on the right (no eyebrow label: the user had those removed, 2026-10-04)."""
    lead = f'<p class="pg-lead">{lead}</p>' if lead else ""
    return f'''<section class="pg-hero{" " + cls if cls else ""}"><div class="wrap pg-hero-in">
<div class="pg-hero-text"><h1 class="pg-h1">{title}</h1>{lead}</div>{side}
</div></section>'''


def qa_list(qs, open_first=0):
    return '<div class="faq-list">' + "".join(f'<details class="qa"{" open" if k < open_first else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for k, (q, a) in enumerate(qs)) + "</div>"


def back_to_fig(title, lead, note, second, icon="✓", cls=""):
    """Where Stripe sends people back: one card over the faded map, Open FIG and one more link."""
    return f'''<section class="st"><div class="st-card">
<div class="st-badge{" " + cls if cls else ""}" aria-hidden="true">{icon}</div>
<h1 class="st-h1">{title}</h1><p class="st-lead">{lead}</p>{f'<p class="st-note">{note}</p>' if note else ""}
<div class="st-btns">{second}</div>
</div></section>
<script src="/js/back.js" defer></script>'''


def faq_ld(qs):
    return '\n  <script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}) + "</script>"


# a search description where the first short line is too thin (FIX-LIST #106: /terms's was 46 characters)
LEGAL_DESC = {"terms": "FIG's terms of service: your account, how deals and claims work, playing fair, restaurants and your food, what you send us, and leaving FIG."}
LEGAL_TABS = [("terms", "Terms of service"), ("privacy", "Privacy policy"), ("business-terms", "Business terms"), ("cookies", "Cookies")]


def para(p):
    """A legal paragraph: lines that start with a bullet become a bullet."""
    return f'<p class="lg-bullet">{e(p[1:].strip())}</p>' if p.startswith("•") else f"<p>{e(p)}</p>"


LEGAL_DATES = {}


def legal(slug, doc, extra=""):
    LEGAL_DATES["/" + slug] = datetime.datetime.strptime(doc["updated"].replace("Last updated ", ""), "%B %d, %Y").date().isoformat()  # for the sitemap
    short = "".join(f"<li>{e(x)}</li>" for x in doc["short"])
    secs = [(s["heading"], "".join(para(p) for p in s["paragraphs"])) for s in doc["sections"]]
    if extra:  # (title, html) sections only this page has
        secs += [(h, t) for h, t in extra]
    tabs = '<nav class="pg-pills" aria-label="Legal documents">' + "".join(
        f'<a href="/{s}"{" aria-current=page" if s == slug else ""}>{t}</a>' for s, t in LEGAL_TABS) + "</nav>"
    links = "".join(f'<a href="#{slug_id(h)}">{e(h)}</a>' for h, _ in secs)
    # a band pinned at the top: the title as big as every other page's, the date, the documents (user 2026-10-13/14: they stay
    # put and only the document scrolls, and the title is "enlarged like before"); under 1024 px it also holds the
    # "On this page" menu, from 1024 the contents are a column pinned right under it (js/legal.js keeps that line exact)
    band = ('<section class="lg-band"><div class="wrap lg-band-in">'
            '<a class="lg-back" href="/"><span class="lg-back-arrow" aria-hidden="true">&larr;</span><svg class="logo" aria-hidden="true"><use href="#logo"/></svg><span>Back to FIG</span></a>'
            f'<div class="lg-title"><h1 class="lg-h1">{e(doc["title"])}</h1>'
            f'<p class="lg-upd">{e(doc["updated"])}</p></div>{tabs if slug in dict(LEGAL_TABS) else ""}'
            '<button class="lg-toc-btn" type="button" aria-expanded="false" aria-controls="lg-toc"><span class="lg-toc-lbl">On this page</span><span class="lg-toc-now" aria-hidden="true"></span></button>'
            f'<nav class="lg-rail lg-menu" id="lg-toc" aria-label="On this page">{links}</nav></div></section>')
    col = f'<nav class="lg-rail lg-col" aria-label="Contents"><b>On this page</b>{links}</nav>'
    doc_html = (f'<div class="pg-short"><h2>The short version</h2><ul>{short}</ul></div>'
                + "".join(f'<section class="lg-sec" id="{slug_id(h)}"><h2>{e(h)}</h2>{t}</section>' for h, t in secs)
                + f'<div class="lg-ask"><div><b>{e(doc["contactAsk"])}</b><span>{e(doc["contactLine"])}</span></div><a class="btn" href="/contact">Contact us</a></div>')
    body = band + f'<section class="section lg lg-top"><div class="wrap lg-grid">{col}<article class="lg-doc">{doc_html}</article></div></section>'
    page(slug, doc["title"], LEGAL_DESC.get(slug, doc["short"][0]), body, group="Legal", wide=True, extra_head='\n  <script src="/js/legal.js" defer></script>', chrome="back")


L = json.loads((SITE / "scripts" / "legal.json").read_text(encoding="utf-8"))
legal("terms", L["terms"])
legal("business-terms", L["business-terms"])
legal("privacy", L["privacy"], [("The waitlist", '''<p>While FIG opens to restaurants first, diners can join a waitlist, here on the website or in the FIG app. We keep your email, your school if you add one (in the app: picked from a list of local high schools, colleges and universities built into the app, or typed in; it only helps us see which schools to reach first), that you agreed to “I agree to get emails from FIG and can unsubscribe at any time.” and when (joining needs it), when you joined, and which link brought you, if any. We email you to say FIG is open in Markham. If you unsubscribe, the emails stop and you keep your place. Every email comes from FIG, Markham, Ontario, and has an unsubscribe link: you can withdraw your consent anytime, through that link or by messaging us. To stop people flooding the list, we briefly count tries from your internet address. If you make a FIG account instead, your account is your place on the list. We never sell the list or share it with restaurants or advertisers.</p>''')])

# Cookies: the fourth legal document, in the same layout as the other three (user 2026-10-14: "work the same for every extra page")
legal("cookies", {"title": "Cookies", "updated": "Last updated October 19, 2026",
                  "short": ["No cookies for visitors, and no advertising, tracking or analytics.", "The website keeps three small notes in your browser.", "The web app keeps your sign-in and settings in your browser, not in cookies."],
                  "sections": [], "contactAsk": "Questions about cookies?", "contactLine": "FIG, Markham, Ontario"},
      [("What the website stores", "<ul><li><b>No cookies.</b> Browsing the site and joining the waitlist don't set any. The website keeps three small notes in your browser instead: which link brought you here (until you close the tab, so a creator gets credit if you join the waitlist), whether FIG is open to diners, and an offline copy of the pages.</li>"
        "<li><b>FIG team only:</b> signing in to the admin page sets secure, HttpOnly cookies: one keeps you signed in for 8 hours, one remembers that browser for 90 days, one counts wrong tries, and short-lived ones (10 minutes at most) hold a sign-in or set-up step.</li></ul>"),
       ("What the web app keeps", "<p>When you use FIG in your browser, it keeps your sign-in and your settings (like your language) in this browser's own storage, so you stay signed in and it remembers them. They're not cookies and they don't track you anywhere else. Signing out removes your sign-in; clearing this site's data in your browser removes the rest.</p>"),
       ("Things loaded from other services", "<p>The map tiles come from OpenFreeMap and the map library from jsDelivr; the animation library is served from FIG's own site. They see a normal web request (like any website you visit) but we don't send them anything about you.</p>")])

page("about", "About FIG", "FIG is the restaurant deals app for Markham, Ontario: live deals on a map, free for diners, with one flat plan for restaurants.",
     hero('The restaurant deals app for <span class="accent">Markham.</span>',
          "Live deals from local restaurants, on a map. Diners claim a deal in one tap and show a code at the counter. Restaurants pay one flat plan and no commission on dine-in.",
          '<div class="ab-photos" aria-hidden="true"><img src="/assets/about/dumpling-house.webp" srcset="/assets/about/dumpling-house-360.webp 360w, /assets/about/dumpling-house.webp 720w" sizes="180px" alt="" width="720" height="1040"><img src="/assets/about/brew-lab.webp" srcset="/assets/about/brew-lab-360.webp 360w, /assets/about/brew-lab.webp 720w" sizes="180px" alt="" width="720" height="1360"></div>', "ab-hero")
     + ABOUT.replace("{faq}", qa_list(ABOUT_FAQ, 1)), wide=True,
     keywords=BASE_KW + ", about FIG, Markham startup", group="Company",
     extra_head=ld({"@context": "https://schema.org", "@type": "AboutPage", "name": "About FIG", "url": SITE_URL + "/about",
                    "mainEntity": {"@type": "Organization", "name": "FIG", "url": SITE_URL, "foundingLocation": "Markham, Ontario",
                                   "areaServed": ["Markham, Ontario"], "description": "FIG is a restaurant deals app for Markham, Ontario."}}) + faq_ld(ABOUT_FAQ))

# a real inbox (user 2026-10-11): the @fig.app addresses never existed. The form goes to support_messages through
# contact_fig (limited per address and per network), the same inbox as Message us in the app; the admin site shows it.
page("contact", "Contact", "Message the FIG team. A real person reads every message.", wide=True, body='''<section class="pg-hero ct-band"><div class="wrap ct-grid">
<div class="pg-hero-text"><h1 class="pg-h1">Talk to a real person.</h1>
<p class="pg-lead">A real person reads every message and replies by email, usually within 24 hours.</p></div>
<form class="contact ct-card" novalidate>
<label class="ct-field"><span>Your email</span><input name="email" type="email" autocomplete="email" placeholder="you@example.com" required></label>
<label class="ct-field"><span>What's it about?</span><select name="topic">
<option>A question</option><option>My restaurant</option><option>Privacy or my data</option><option>Terms or anything official</option><option>Something else</option>
</select></label>
<label class="ct-field"><span>Message</span><textarea name="body" rows="6" maxlength="4000" placeholder="How can we help?" required></textarea></label>
<input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" type="submit">Send message</button>
<p class="form-msg" role="status" aria-live="polite"></p>
</form>
</div></section>
<section class="section ct-more"><div class="wrap"><h2 class="h2 pg-sub">Other ways</h2><div class="ct-ways">
<a class="ct-way" href="/help"><b>Help center</b><span>Answers to the questions people ask most.</span><em>Read the help</em></a>
<div class="ct-way"><b>In the app</b><span>Profile, then Help, then Message us. Restaurants: Settings, then Help for restaurants.</span><em class="leaf">Same inbox</em></div>
</div></div></section>
<script src="/js/config.js"></script>
<script src="/js/contact-form.js" defer></script>''')

HELP = [
    ("diners", "For diners", [
        ("Is FIG free?", "Yes, completely. Deals are free to claim and use."),
        ("How do I use a deal?", "Claim it in the app. It waits on your Deals page for as long as the deal runs. Show the QR code at the counter when you order, and staff scan it or type the 8 characters under it."),
        ("Can someone use my screenshot?", "No. Your code changes every 5 minutes, so only the live code on your phone works."),
        ("What do I pay?", "Just your bill, like normal, with the deal taken off. Some restaurants let you pay for takeout in the app; that money goes to the restaurant. FIG never charges diners anything."),
        ("How do reviews work?", "Only diners whose visit was scanned can review, so every review comes from a real visit. Rate a visit right after it, or later from Past visits on your Deals page."),
        ("Do restaurants see my phone number?", "Never. Takeout orders go through the app and your number stays private."),
        ("Can I order takeout?", "Yes. Tap Takeout on a deal that allows it, add what you want, watch it get made, and pick it up. Some restaurants also take takeout at full price: tap Order takeout on their page. FIG doesn't deliver."),
        ("What if a restaurant won't honour a deal?", "Report the visit in the app. A real person looks at every report and replies within 24 hours."),
    ]),
    ("restaurants", "For restaurants", [
        ("What does FIG cost?", "One plan for all your restaurants: $29.99 a month or $299.99 a year from the day FIG opens to diners, before tax, for your pages, deals, scans and insights, with no commission on dine-in. Before launch, founding restaurants lock in less: $9.99 a month for the first 12 months, or $59.99 for the first year, paid now as a deposit (refundable within 14 days, or in full if FIG hasn't opened to diners by March 1, 2027 and your plan hasn't started). On takeout orders diners pay for in the app, FIG also keeps 5% of the food (before tax), and Stripe's card fee (2.9% + $0.30 for most Canadian cards) comes off the same payment. Stripe pays the rest out to your bank on its usual schedule, often a few business days."),
        ("Do I need new equipment?", "No. Any phone, tablet or computer can scan: open FIG on the web (the iPhone and Android apps are coming soon). Invite your staff in Settings: they scan with their own FIG sign-in."),
        ("What if a code won't scan?", "Tap Enter code and type the 8 characters under the diner's QR. It runs the same check as a scan."),
        ("How do I post a deal?", "In the app, open Deals and tap New deal. Pick the dishes (or the whole order, for dine-in), the offer, the days and hours, and check it the way diners will see it. You can pause it anytime, or post an ended deal again in one tap."),
        ("When does my page go live?", "It's ready as soon as you finish setup: photos, address, hours and cuisine. Setting up is free; your plan starts the day FIG opens to diners (a founding price is locked in before that with a deposit). Diners see it from January 1, 2027. An HST number and bank details only matter for takeout paid in the app, and you can add them later."),
        ("Can diners order takeout?", "Yes. Add your menu: first the sections, then the dishes in each. Turn on takeout and pick how many deals one order can use: 1, 2, 3, more or no limit, or 0 to take orders at full price. You scan their pickup code when they collect. The diner's card is charged when you accept the order; decline it and nothing is charged."),
        ("Can I refund an order?", "Yes, owners and managers can: open the order and tap Refund, for all of it or part. FIG gives back its fee in proportion; Stripe keeps its card fee."),
        ("What if a scan looks wrong?", "Message us from Help within 14 days. We review it, and if it was a mistake we remove it."),
        ("Can I pause takeout in a rush?", "Yes. Tap Takeout: On on your dashboard or Orders to pause new orders for 20 or 40 minutes or until tomorrow's opening, or to add prep time. Orders already in aren't touched, and it comes back on by itself."),
        ("How do I stop?", "Monthly: cancel any time, it ends at the end of the month you've paid. Annual: it runs its year, then you can stop. You can also pause your deals, or close your account in Settings."),
    ]),
]
HELP_HEAD = {"diners": ("Eating out with FIG", "Claiming, codes, paying and takeout."), "restaurants": ("Running deals on FIG", "Cost, scanning, deals and takeout.")}
# a real app screen under each section's title: the diner's QR, the restaurant's dashboard (tablet)
SHOT_SIZE = {"qr": (780, 1688), "tdash": (1600, 1112)}  # the screenshots' own sizes, so the page doesn't shift as they load (FIX-LIST #107)
HELP_SHOT = {"diners": ('qr', "The QR a diner shows at the counter", "phone"), "restaurants": ('tdash', "A restaurant's FIG dashboard", "wide")}
help_html = hero("How can we help?", "Short answers to the questions people ask most. Still stuck? A real person replies within 24 hours.",
                 '<nav class="pg-pills" aria-label="Jump to">' + "".join(f'<a href="#{a}">{t}</a>' for a, t, _ in HELP) + "</nav>"
                 # search the questions as you type (28's research: search is the main way into help); js/help.js
                 + '<div class="hs-search"><input type="search" id="help-q" placeholder="Search the help center" aria-label="Search the help center" autocomplete="off">'
                 + '<p class="hs-none" id="help-none" hidden>No match. <a href="/contact">Message us</a> and a real person replies within 24 hours.</p></div>', cls="pg-hero-line")
for k, (anchor, title, qs) in enumerate(HELP):
    head, sub = HELP_HEAD[anchor]
    help_html += (f'<section class="section{" ice" if k else ""}" id="{anchor}"><div class="wrap faq"><div class="faq-head">'
                  f'<h2 class="h2">{head}</h2><p class="side">{sub}</p><figure class="help-shot {HELP_SHOT[anchor][2]}"><img src="/assets/screens/{HELP_SHOT[anchor][0]}.webp" alt="{HELP_SHOT[anchor][1]}" width="{SHOT_SIZE[HELP_SHOT[anchor][0]][0]}" height="{SHOT_SIZE[HELP_SHOT[anchor][0]][1]}"></figure></div>{qa_list(qs, 1 if k else 2)}</div></section>')
help_html += '''<section class="section pg-tight"><div class="wrap"><div class="pg-dark">
<div><h2>Still stuck?</h2><p>Message us and a real person replies within 24 hours. Or watch the quick tutorial videos for diners and restaurants.</p></div>
<div class="pg-dark-btns"><a class="btn btn-lg" href="/contact">Contact us</a><a class="btn btn-lg btn-line" href="/#catch">Watch the tutorials</a></div>
</div></div></section>'''
page("help", "Help center", "Answers for diners and restaurants using FIG: claiming deals, QR codes, takeout, accounts and running deals.", help_html, group="Main", wide=True, extra_head=faq_ld([qa for _, _, qs in HELP for qa in qs]) + '\n  <script src="/js/help.js" defer></script>')



def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%B} {d.day}, {d.year}"


def tables(html_):
    """A table in a post scrolls sideways on a phone, inside a frame that fades at its edge, instead of squeezing."""
    return re.sub(r"<table\b(.*?)</table>", lambda m: f'<div class="ps-table" tabindex="0" role="region" aria-label="Table"><table{m.group(1)}</table></div>', html_, flags=re.S)


def read_min(post):
    words = len(re.sub(r"<[^>]+>", " ", " ".join(h for _, h in post["sections"])).split())
    return max(2, round(words / 220))


# the clock, the overrides and `live` are at the top; queued = not live yet and not taken down
QUEUED = sorted((x for x in POSTS if not live(x) and x["slug"] not in TAKEN_DOWN), key=lambda x: x["publish_at"])
POSTS[:] = [x for x in POSTS if live(x)]
# a page of a post that isn't live (queued, moved later, or taken out of the list) goes, with its cover
_live = {x["slug"] for x in POSTS}
for f in [*(SITE / "blog").glob("*.html"), *(SITE / "assets" / "blog").glob("*.jpg")]:
    if f.stem not in _live:
        f.unlink()
POSTS.sort(key=lambda x: (x["date"], x.get("publish_at", "")), reverse=True)
# a live post's link to one still queued is plain text until that one goes live (fig-promo-28: it appears by itself then)
if NOT_LIVE:
    for x in POSTS:
        x["sections"] = [(h, _unlink(t)) for h, t in x["sections"]]
        x["faq"] = [(q, _unlink(ans)) for q, ans in x["faq"]]


def cover(post):
    """1200x630 cover + social image: topic colour, the title, a real app screen. Rebuilt every run (fast, deterministic)."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    W, H = 1200, 630
    top, bot, ink = {"For diners": ((58, 115, 255), (21, 70, 201), (255, 255, 255)),
                     "For restaurants": ((217, 250, 106), (156, 200, 26), (10, 16, 32))}.get(post["topic"], ((29, 36, 56), (10, 16, 32), (255, 255, 255)))
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bot)))
    font = lambda size, weight="ExtraBold": (lambda f: (f.set_variation_by_name(weight), f)[1])(ImageFont.truetype(str(SITE / "assets/PlusJakartaSans.ttf"), size))

    shot = Image.open(SITE / f"assets/screens/{post.get('screen', 'map')}.webp").convert("RGB")
    tablet = shot.width > shot.height
    sw = 600 if tablet else 330
    shot = shot.resize((sw, round(sw * shot.height / shot.width)), Image.LANCZOS)
    pad, rad = (14, 30) if tablet else (12, 46)
    fw, fh = shot.width + pad * 2, shot.height + pad * 2
    x0, y0 = (W - fw + 70, H - fh + 150) if tablet else (W - fw - 70, 150)
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle([x0 + 10, y0 + 24, x0 + fw + 10, y0 + fh + 24], rad, fill=120)
    img.paste((5, 10, 30), mask=shadow.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + fw, y0 + fh], rad, fill=(10, 16, 32))
    m = Image.new("L", shot.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, shot.width, shot.height], rad - pad + 2, fill=255)
    img.paste(shot, (x0 + pad, y0 + pad), m)

    maxw = x0 - 64 - 48
    for size in range(76, 38, -4):
        f, lines = font(size), [""]
        for word in post["title"].split():
            trial = (lines[-1] + " " + word).strip()
            if f.getlength(trial) <= maxw: lines[-1] = trial
            else: lines.append(word)
        if len(lines) <= 4: break
    k = font(22, "Bold")
    tw = k.getlength(post["topic"].upper())
    d.rounded_rectangle([64, 64, 64 + tw + 36, 104], 20, fill=ink)
    d.text((82, 84), post["topic"].upper(), font=k, fill=bot, anchor="lm")
    y = 140
    for line in lines:
        d.text((64, y), line, font=f, fill=ink)
        y += round(size * 1.1)
    d.text((64, H - 64), "FIG", font=font(40), fill=ink, anchor="ls")
    d.text((64 + font(40).getlength("FIG") + 14, H - 70), "Restaurant deals in Markham", font=font(22, "SemiBold"), fill=ink, anchor="ls")
    out = SITE / "assets/blog" / f"{post['slug']}.jpg"
    out.parent.mkdir(exist_ok=True)
    img.save(out, quality=84, optimize=True, progressive=True)
    return f"/assets/blog/{post['slug']}.jpg"


SHARE = '<button class="share" type="button" data-share><svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M16 6l-4-4-4 4M12 2v13"/></svg><span>Share</span></button>'


def end_cta(post):
    """The cobalt block at the end of a post: restaurants get listed, diners open FIG (the web app, 2026-10-13)."""
    if post["topic"] == "For restaurants":
        words, btns = ("<h2>Get your restaurant on FIG.</h2><p>Deals and scans in one flat plan, with no commission on dine-in. Founding prices before launch.</p>",
                       '<a class="btn btn-lg btn-volt" href="/app/welcome">Sign up</a><a class="btn btn-lg btn-line" href="/#owners">See how pricing works</a>')
    else:
        words, btns = ("<h2>Find a deal near you.</h2><p>FIG is free for diners. Opens in Markham on January 1, 2027.</p>",
                       '<a class="btn btn-lg btn-volt" href="/app/">Open FIG on the web</a><a class="btn btn-lg btn-line" href="/#how">How it works</a>')
    return f'<section class="section pg-tight"><div class="wrap"><div class="pg-cta"><div>{words}</div><div class="pg-cta-btns">{btns}</div></div></div></section>'


STORE_BTNS = re.search(r'<div class="badges small">(.*)</div>', STORES, re.S).group(1)
# the food photo on each post's card and page (the Paper design); the generated cover stays the social image
PHOTO = {"how-fig-makes-money": "alt-hotpot", "restaurant-deals-markham": "sakura-house", "delivery-app-commissions-vs-fig": "burger-co",
         "fill-slow-hours-restaurant": "noodle-bar", "student-food-deals-markham": "alt-banhmi", "flash-deals-explained": "alt-tacos",
         "takeout-without-delivery-fees": "bowl-lab", "why-we-built-fig": "wok-bar"}
BLOG_PICS = SITE / "assets" / "blog" / "photos"


def blog_pic(name):
    """The post's photo at blog size (the food photos in assets/food are 160px map pins): made once from the 1600px
    Unsplash originals in Media Assets (credits in assets/food/CREDITS.txt)."""
    out = BLOG_PICS / f"{name}.webp"
    if not out.exists():
        from PIL import Image
        BLOG_PICS.mkdir(parents=True, exist_ok=True)
        im = Image.open(ROOT / "Media Assets" / "Assets" / "website" / "food" / f"{name}.jpg").convert("RGB")
        im.thumbnail((1600, 1600), Image.LANCZOS)
        im.save(out, quality=78, method=6)
    small = BLOG_PICS / f"{name}-480.webp"
    if not small.exists():
        from PIL import Image
        im = Image.open(out)
        im.thumbnail((480, 4000), Image.LANCZOS)  # 480 wide, whatever its shape
        im.save(small, quality=76, method=6)
    return f"/assets/blog/photos/{name}.webp"


def thumb(pic):
    """A row's photo: the 480 px copy, the full one for big screens with sharp displays."""
    return f'src="{pic[:-5]}-480.webp" srcset="{pic[:-5]}-480.webp 480w, {pic} 1600w" sizes="(min-width: 720px) 240px, 112px"' if pic.startswith("/assets/blog/photos/") else f'src="{pic}"'


photo_of = lambda post, img: blog_pic(PHOTO[post["slug"]]) if post["slug"] in PHOTO else img
# laid out by group (FIX-LIST #145): a plain section per group (its anchor the slug, so /blog#fill-quiet-hours opens it), its
# published posts newest first; the pills are links to them, and sub.js shows one group at a time. A group with nothing live yet
# is left out, pill and all.
LIVE_GROUPS = [(g, t, d) for g, t, d in GROUPS if any(x["group"] == g for x in POSTS)]
chips = '<a href="/blog" data-group="all" aria-current="true">All</a>' + "".join(f'<a href="#{g}" data-group="{g}">{e(t)}</a>' for g, t, _ in LIVE_GROUPS)
blog = hero("Eat out for less.<br>Fill the quiet hours.", "", f'<nav class="pg-pills blog-filter" aria-label="Blog groups">{chips}</nav>')
rows = {g: [] for g, _, _ in GROUPS}
items = []
for k, post in enumerate(POSTS):
    url = f"/blog/{post['slug']}"
    img = cover(post)
    pic = photo_of(post, img)
    meta = f"{post['topic']} · {nice_date(post['date'])} · {read_min(post)} min read"
    if k == 0:
        blog += (f'<section class="section ice bl-feature-band"><div class="wrap"><a class="post-card bl-feature" href="{url}" data-topic="{post["topic"]}" data-post-card="{post["slug"]}">'
                 f'<span class="bl-pic"><img src="{pic}" alt="" width="720" height="480"><i>Newest</i></span>'
                 f'<span class="bl-text"><b>{e(post["title"])}</b><span class="bl-meta">{e(meta)}</span><p>{e(post["dek"])}</p><em>Read the post</em></span></a></div></section>')
    # every post in its group's list (the newest too, under its band)
    rows[post["group"]].append(f'<a class="post-card bl-row" href="{url}" data-topic="{post["topic"]}" data-post-card="{post["slug"]}"><img {thumb(pic)} alt="" width="240" height="168" loading="lazy">'
                    f'<span><b>{e(post["title"])}</b><span class="bl-meta">{e(meta)}</span><p>{e(post["dek"])}</p></span></a>')
    # three to read next: the same topic first, then the newest others (published ones only: POSTS is already the live list)
    related = ([x for x in POSTS if x is not post and x["topic"] == post["topic"]] + [x for x in POSTS if x is not post and x["topic"] != post["topic"]])[:3]
    toc = "".join(f'<li><a href="#{slug_id(h)}">{e(h)}</a></li>' for h, _ in post["sections"])
    updated = post.get("updated", post["date"])
    byline = f"By the FIG team · {post['topic']} · {'Updated ' if updated != post['date'] else ''}{nice_date(updated)} · {read_min(post)} min read"
    body = (f'''<section class="ps-head"><div class="wrap"><a class="ps-back" href="/blog">← The FIG blog</a>
<h1 class="ps-h1">{e(post["title"])}</h1><p class="ps-dek">{e(post["dek"])}</p><div class="post-by"><span>{e(byline)}</span>{SHARE}</div></div></section>
<div class="wrap"><img class="ps-cover" src="{pic}" alt="{e(post["title"])}" width="1200" height="560"></div>'''
            # the article, with what's in it beside it on a computer (pinned) and at its top on a phone
            + f'<div class="ps-grid"><nav class="ps-toc" aria-label="In this post"><details open><summary>In this post</summary><ol>{toc}<li><a href="#questions">Questions</a></li></ol></details></nav>'
            + '<article class="ps-body"><div class="pg-short"><h2>Key takeaways</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in post.get("takeaways", post["points"])) + "</ul></div>"
            + "".join(f'<h2 id="{slug_id(h)}">{e(h)}</h2>{tables(t)}' for h, t in post["sections"])
            + '<h2 id="questions">Questions</h2>' + qa_list(post["faq"])
            + '<aside class="ps-author"><img src="/assets/favicon.svg" alt="" width="44" height="44"><div><b>The FIG team</b><p>We build FIG in Markham, Ontario: live deals from local restaurants, free for diners. Questions or a correction? <a href="/contact">Write to us</a>.</p></div></aside>'
            + "</article><div></div></div>" + end_cta(post)
            + '<section class="section ps-more"><div class="wrap"><h2 class="h2 pg-sub">Keep reading</h2><div class="bl-list">'
            + "".join(f'<a class="post-card bl-row" href="/blog/{x["slug"]}" data-topic="{x["topic"]}" data-post-card="{x["slug"]}"><img {thumb(photo_of(x, cover(x)))} alt="" width="240" height="168" loading="lazy"><span><b>{e(x["title"])}</b><span class="bl-meta">{e(x["topic"])} · {nice_date(x["date"])} · {read_min(x)} min read</span><p>{e(x["dek"])}</p></span></a>' for x in related)
            + "</div></div></section>")
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"], "description": post.get("desc", post["dek"]), "keywords": post["keywords"],
               "datePublished": post["date"], "dateModified": post.get("updated", post["date"]), "articleSection": post["topic"], "inLanguage": "en-CA",
               "image": SITE_URL + img, "mainEntityOfPage": SITE_URL + url, "wordCount": len(re.sub(r"<[^>]+>", " ", " ".join(t for _, t in post["sections"])).split()),
               "author": {"@type": "Organization", "name": "FIG", "url": SITE_URL},
               "publisher": {"@type": "Organization", "name": "FIG", "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/icons/icon-512.png"}}}
    page(url[1:], post["title"], post.get("desc", post["dek"]), body, group="Blog", wide=True, keywords=post["keywords"], og_type="article", trail=[("Blog", "/blog")], image=img, seo=post.get("seo"),
         extra_head=ld(article) + faq_ld(post["faq"]))
    items.append(f"""  <item><title>{e(post['title'])}</title><link>{SITE_URL}{url}</link><guid>{SITE_URL}{url}</guid>
    <pubDate>{datetime.date.fromisoformat(post['date']):%a, %d %b %Y} 12:00:00 -0400</pubDate><category>{e(post['topic'])}</category><description>{e(post['dek'])}</description></item>
""")
page("blog", "Blog", "Guides to restaurant deals in Markham and ideas for independent restaurants, from the FIG team.",
     blog + "".join(f'<section class="section bl-group" id="{g}"><div class="wrap"><h2 class="h2 bl-gh">{e(t)}</h2><p class="bl-gd">{e(d)}</p>'
                    f'<div class="bl-list">{"".join(rows[g])}</div></div></section>' for g, t, d in LIVE_GROUPS), group="Blog", wide=True,
     keywords=BASE_KW + ", Markham food blog, restaurant marketing blog",
     extra_head=ld({"@context": "https://schema.org", "@type": "Blog", "name": "The FIG blog", "url": SITE_URL + "/blog",
                    "blogPost": [{"@type": "BlogPosting", "headline": x["title"], "url": f"{SITE_URL}/blog/{x['slug']}", "datePublished": x["date"]} for x in POSTS]}))
(SITE / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>The FIG blog</title><link>{SITE_URL}/blog</link><language>en-ca</language>
  <description>Restaurant deals in Markham, Ontario, and ideas for independent restaurants.</description>
{"".join(items)}</channel></rss>
""", encoding="utf-8")


# =====================================================================  404, site map, sitemap.xml, robots, manifest
page("404", "Page not found", "This page doesn't exist.", body='''<p class="lost-num" aria-hidden="true">404</p><h1>This page wandered off.</h1>
<p class="lead-p">It may have moved, or the link has a typo.</p>
<div class="cards"><a class="card-l" href="/"><b>Home</b><span>Local deals, one tap away.</span></a><a class="card-l" href="/#how"><b>How it works</b><span>Find, claim, show, save.</span></a>
<a class="card-l" href="/#owners"><b>For restaurants</b><span>Post deals diners can find.</span></a><a class="card-l" href="/help"><b>Help center</b><span>Answers to common questions.</span></a></div>''')

# a restaurant shared from the app (/r/<id>?n=<name>&from=<first name>, rewritten to /r.html in vercel.json)
page("r", "Shared with you", "A restaurant someone shared with you on FIG.", body='''<div class="r-bubble" aria-hidden="true"><b id="r-from">A friend</b><span>dinner here?</span></div>
<h1 id="r-title">Someone sent you a spot on FIG</h1>
<p class="lead-p" id="r-line">Live deals from restaurants near you. Claim one, show your QR at the counter. Free for diners.</p>
<div class="r-actions"><a class="btn btn-lg" id="r-web" href="/app/">See it on FIG</a><a class="btn btn-lg btn-ghost" href="/#how">How FIG works</a></div>
<p class="r-app"><a id="r-open" href="/" hidden>Have the FIG app? Open it there</a></p>
<script src="/js/config.js" defer></script><script src="/js/r.js" defer></script>''')


# Stripe sends people back here (takeout orders paid in the app, 2026-10-08): after paying for an order, after setting up payouts,
# and after FIG Premium (2026-10-09)
page("paid", "Back to FIG", "Your takeout payment.", wide=True, body=back_to_fig("You’re all set. Head back to FIG.",
     "Your card is held now and charged only when the restaurant accepts your order. If they decline it, you’re not charged.",
     "Didn’t finish paying? Open your order in FIG and tap Pay.", '<a class="btn btn-lg" href="/app/">Open FIG</a><a class="btn btn-lg btn-soft" href="/help">Help center</a>'))
page("stripe", "Back to FIG", "Setting up payouts with Stripe.", wide=True, body=back_to_fig("Back to FIG to finish up.",
     "Stripe has your details. Open FIG, go to Settings → Get paid, and you’ll see whether payouts are ready.",
     "If Stripe still needs something, tap the button there again to pick up where you left off.",
     '<a class="btn btn-lg" href="/app/">Open FIG</a><a class="btn btn-lg btn-soft" href="/business-terms">Business terms</a>', icon="→", cls="go"))
page("premium-on", "Back to FIG", "FIG Premium.", wide=True, body=back_to_fig("Thanks. Head back to FIG.",
     "If you finished paying, FIG Premium turns on in a moment, for your whole account. Open FIG and go to Settings → FIG Premium to see it, or to cancel or change your card later.",
     "Changed your mind before paying? Nothing was charged.", '<a class="btn btn-lg" href="/app/">Open FIG</a><a class="btn btn-lg btn-soft" href="/business-terms">Business terms</a>'))

# the sitemap's dates are the posts' own: the same posts give the same file, so the hourly job commits real changes only
POST_DATE = {f"/blog/{x['slug']}": x.get("updated", x["date"]) for x in POSTS}
if POSTS:
    POST_DATE["/blog"] = max(POST_DATE.values())
# every other page (FIX-LIST #107): the legal pages from their own "Last updated" line; the rest from the date their words last changed
# ponytail: hand-kept dates for 4 pages; bump the one you edit (a generated date would change the file every hourly run)
POST_DATE.update({"/": "2026-10-19", "/about": "2026-10-19", "/contact": "2026-10-19", "/help": "2026-10-19"})
POST_DATE.update(LEGAL_DATES)
lastmod = lambda p: f"<lastmod>{POST_DATE[p]}</lastmod>" if p in POST_DATE else ""
prio = lambda p: "1.0" if p == "/" else "0.8" if p in ("/about", "/blog", "/help") else "0.4" if p in ("/terms", "/privacy", "/business-terms", "/cookies") else "0.6"
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}{'' if p == '/' else p}</loc>{lastmod(p)}<priority>{prio(p)}</priority></url>\n" for p, _, _ in PAGES) + "</urlset>\n"
(SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
# no /admin line: it would only point at it; the admin pages carry noindex instead (FIX-LIST #83)
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
LLMS = f"""# FIG

> FIG is a restaurant deals app for Markham, Ontario, Canada. Restaurants post their own deals; diners find them on a map, claim one in a tap and show a rotating QR code at the counter. Free for diners. Restaurants pay one plan covering all their restaurants ($29.99 a month or $299.99 a year from launch; founding restaurants $9.99 a month for the first 12 months, or $59.99 for the first year then $299.99 a year), with no commission on dine-in. FIG also keeps 5% of the food on takeout orders diners pay for in the app.

## Facts
- Based in: Markham, Ontario
- Platforms: iPhone and Android
- Launch area: Markham first, expanding to Richmond Hill and Vaughan Mills
- Diners: free; no loyalty points, rewards or AI features
- Restaurants: one plan covering all an owner's restaurants, $29.99 a month or $299.99 a year from the day FIG opens to diners, before tax; with no plan 30 days after that, pages and deals pause until one is taken (nothing deleted); founding prices before launch: $9.99 a month for the first 12 months, or $59.99 for the first year then $299.99 a year (listing, unlimited everyday and flash deals, scans, dashboard and insights included); takeout orders paid in the app: FIG keeps 5% of the food before tax, and Stripe's card fee comes off the same payment; no ads
- How a deal works: claim (it stays good until the deal ends), show the QR code (refreshes every 5 minutes), pay the restaurant directly
- Takeout: with a deal that allows it, or at full price where the restaurant takes plain takeout orders; pay in the app and pick up at the counter; no delivery, and no fees for diners
- Privacy: restaurants never see a diner's phone number

## Pages
- [Home]({SITE_URL}/): what FIG is, features, pricing
- [About]({SITE_URL}/about): the full story and FAQ
- [Help center]({SITE_URL}/help): answers for diners and restaurants
""" + "".join(f"- [{x['title']}]({SITE_URL}/blog/{x['slug']}): {x['dek']}\n" for x in POSTS) + f"""
## Legal
- [Terms]({SITE_URL}/terms), [Privacy]({SITE_URL}/privacy), [Business terms]({SITE_URL}/business-terms)
"""
(SITE / "llms.txt").write_text(LLMS, encoding="utf-8")
(SITE / "site.webmanifest").write_text(json.dumps({
    "name": "FIG · Local deals", "short_name": "FIG", "start_url": "/", "display": "standalone", "background_color": "#FFFFFF", "theme_color": "#1E5EFF",
    "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=1), encoding="utf-8")

icons = SITE / "assets" / "icons"
if not (icons / "icon-512.png").exists():
    from PIL import Image
    icons.mkdir(exist_ok=True)
    src = Image.open(ROOT / "Media Assets" / "Assets" / "brand" / "fig-logo-profile-cobalt-1080.png").convert("RGB")
    for name, size in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
        src.resize((size, size), Image.LANCZOS).save(icons / name, optimize=True)
# every page asks for the site's own /css and /js files by their content (?v=<hash>), so a browser keeps them for a year
# (vercel.json: immutable when ?v= is there) and a new deploy's pages ask for the new files (FIX-LIST #124). /app has its own.
_ver = {}
def _stamp(m):
    path = m.group(2)
    if path not in _ver:
        f = SITE / path.lstrip("/")
        _ver[path] = hashlib.sha256(f.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:10] if f.is_file() else ""  # the same on a Windows (CRLF) and a Linux checkout
    return m.group(1) + path + (f"?v={_ver[path]}" if _ver[path] else "") + m.group(3)
_ASSET = re.compile(r'((?:src|href)=")(/(?:css|js)/[^"?#]+\.(?:css|js))(?:\?v=[0-9a-f]+)?(")')
for _f in SITE.rglob("*.html"):
    if _f.relative_to(SITE).parts[0] == "app":
        continue
    _t = _f.read_text(encoding="utf-8")
    _n = _ASSET.sub(_stamp, _t)
    if _n != _t:
        _f.write_text(_n, encoding="utf-8")
print(len(PAGES), "pages; sitemap.xml, robots.txt, site.webmanifest written")
print(f"blog: published {len(POSTS)}, queued {len(QUEUED)}, taken down {len(TAKEN_DOWN & {x['slug'] for x in _manifest['posts']})}" + "".join(f"\n  {x['publish_at']}  {x['slug']}" for x in QUEUED))
