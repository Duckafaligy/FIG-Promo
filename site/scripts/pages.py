"""Builds the whole site around index.html: nav, footer, every extra page, sitemap.xml, robots.txt and the web manifest.

run: python site/scripts/pages.py
- Legal pages come from legal.json (exported from the app's src/content/legal.ts, so they match the app word for word).
- Nav and footer are written into index.html too, so every page shares them.
- Sections that also live on the home page (how it works, features, restaurants) are copied from index.html, so they never drift.
- SITE_URL is the address search engines see: change it once figpromo.com is connected.
"""
import datetime, html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import ABOUT, ABOUT_FAQ, POSTS

SITE_URL = "https://fig-promo.vercel.app"
SITE = pathlib.Path(__file__).resolve().parents[1]
ROOT = SITE.parent
index = (SITE / "index.html").read_text(encoding="utf-8")
SPRITE = re.search(r'<svg width="0" height="0".*?</svg>', index, re.S).group(0)
STORES_NAV = re.search(r'<div class="nav-stores">.*?</div>', index, re.S).group(0)
MEGA = re.search(r'<div class="mega".*?Save fast\.</span>\s*</div>', index, re.S).group(0)
STORES = re.search(r'<div class="badges small">.*?</div>', index, re.S).group(0)
SECTION = lambda sid: re.search(rf'<section class="section[^"]*" id="{sid}">.*?</section>', index, re.S).group(0)
e = html.escape
BASE_KW = "FIG, FIG app, restaurant deals Markham, Markham restaurants, food deals Ontario, local restaurant deals app"
PAGES = []  # (path, title, group) for sitemap.xml and the site map page
HIDDEN = {"404", "r"}  # not indexed, no breadcrumbs, not in the sitemap

NAV_LINKS = [("/#how", "How it works"), ("/#features", "Features"), ("/#passport", "Passport"), ("/#catch", "What's the catch?"), ("/#owners", "For restaurants")]


def nav(current=""):
    links = "".join(f'<a href="{h}"{" class=on aria-current=page" if h == current else ""}>{t}</a>' for h, t in NAV_LINKS)
    return f'''<header class="nav" id="nav">
  <a class="brand" href="/" aria-label="FIG home"><svg class="logo"><use href="#logo"/></svg><span>FIG</span></a>
  <nav class="nav-links" aria-label="Sections">{links}</nav>
  {STORES_NAV}
</header>'''


FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/"><svg class="logo"><use href="#logo"/></svg><span>FIG</span></a>
        <p>Live deals from local restaurants, on a map. Starting in Markham, Ontario. Richmond Hill next.</p>
        {STORES}
      </div>
      <div class="foot-cols">
        <div><h3>Diners</h3><a href="/#how">How it works</a><a href="/#features">Features</a><a href="/#passport">Passport</a><a href="/#catch">Tutorial</a><a href="/help">Help center</a></div>
        <div><h3>Restaurants</h3><a href="/#owners">Pricing</a><a href="/#catch">Tutorial</a><a href="/blog/one-plan-50-a-year">How the plan works</a><a href="/business-terms">Business terms</a><a href="/help#restaurants">Restaurant help</a></div>
        <div><h3>Company</h3><a href="/about">About</a><a href="/blog">Blog</a><a href="/contact">Contact</a></div>
        <div><h3>Legal</h3><a href="/terms">Terms of service</a><a href="/privacy">Privacy policy</a><a href="/business-terms">Business terms</a><a href="/cookies">Cookies</a></div>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 FIG Technologies Inc. · Markham, Ontario · <a class="admin-link" href="/admin">Are you the admin?</a></span>
      <span>App screens show example restaurants and deals. Map data © OpenStreetMap contributors, OpenFreeMap. App Store is a trademark of Apple Inc. Google Play is a trademark of Google LLC.</span>
    </div>
  </div>
</footer>'''


def head_meta(path, title, desc, extra="", og_type="website"):
    url = SITE_URL + ("" if path == "/" else path)
    return f'''  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="FIG">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE_URL}/assets/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">{extra}'''


# ---------- the home page gets the same nav, footer and head tags ----------
index = re.sub(r'<header class="nav".*?</header>', nav(), index, count=1, flags=re.S)
index = re.sub(r'<footer class="foot">.*?</footer>', FOOTER, index, count=1, flags=re.S)
index = re.sub(r'\n  <!-- seo -->.*?<!-- /seo -->', "", index, flags=re.S)
ORG = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "name": "FIG Technologies Inc.", "url": SITE_URL, "logo": SITE_URL + "/assets/icons/icon-512.png",
     "address": {"@type": "PostalAddress", "addressLocality": "Markham", "addressRegion": "ON", "addressCountry": "CA"}},
    {"@type": "WebSite", "name": "FIG", "url": SITE_URL},
    {"@type": "MobileApplication", "name": "FIG", "operatingSystem": "iOS, Android", "applicationCategory": "LifestyleApplication",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"}}]})
index = index.replace('  <meta name="theme-color"', '  <!-- seo -->\n' + head_meta("/", "FIG · Restaurant deals in Markham, Ontario", "Live deals from Markham restaurants, one tap away. Free for diners, $50 a year for restaurants.",
                      f'\n  <script type="application/ld+json">{ORG}</script>') + '\n  <!-- /seo -->\n  <meta name="theme-color"', 1)
(SITE / "index.html").write_text(index, encoding="utf-8")
PAGES.append(("/", "Home", "Main"))


def ld(obj):
    return '\n  <script type="application/ld+json">' + json.dumps(obj) + "</script>"


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, "item": SITE_URL + u} for k, (n, u) in enumerate(items)]}


def page(slug, title, desc, body, group="More", wide=False, extra_head="", keywords="", og_type="website", trail=None):
    path = "/" + slug
    if slug not in HIDDEN:
        extra_head = ld(crumbs([("Home", "/")] + (trail or []) + [(title, path)])) + extra_head
    current = path if path in dict(NAV_LINKS) else ""
    out = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)} · FIG</title>
  <meta name="description" content="{e(desc)}">
  <meta name="keywords" content="{e(keywords or BASE_KW)}">
  <meta name="robots" content="{'noindex' if slug in HIDDEN else 'index, follow, max-image-preview:large'}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{head_meta(path, title + " · FIG", desc, extra_head, og_type)}
  <link rel="stylesheet" href="/css/site.css">
</head>
<body class="sub">
{SPRITE}
<div class="bg" aria-hidden="true"><div class="bg-grid"></div></div>
{nav(current)}
<main{' class="page"' if wide else ' class="wrap doc"'}>
{body}
</main>
{FOOTER}
{MEGA}
<script src="/js/fx.js" defer></script>
<script src="/js/sub.js" defer></script>
</body>
</html>
'''
    p = SITE / (slug + ".html")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")
    if slug not in HIDDEN:
        PAGES.append((path, title, group))


def faq_ld(qs):
    return '\n  <script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}) + "</script>"


def legal(slug, doc, extra=""):
    short = "".join(f"<li>{e(x)}</li>" for x in doc["short"])
    secs = "".join(f"<h2>{e(s['heading'])}</h2>" + "".join(f"<p>{e(p)}</p>" for p in s["paragraphs"]) for s in doc["sections"])
    body = f'''<p class="doc-kicker">{e(doc["updated"])}</p>
<h1>{e(doc["title"])}</h1>
<div class="doc-short"><h2>The short version</h2><ul>{short}</ul></div>
{secs}{extra}
<p class="doc-contact">{e(doc["contactAsk"])} <a href="mailto:{e(doc["email"])}">{e(doc["email"])}</a><br><span>{e(doc["contactLine"])}</span></p>'''
    page(slug, doc["title"], doc["short"][0], body, group="Legal")


L = json.loads((SITE / "scripts" / "legal.json").read_text(encoding="utf-8"))
legal("terms", L["terms"])
legal("business-terms", L["business-terms"])
legal("privacy", L["privacy"], '''<h2>The website waitlist</h2>
<p>When you join the waitlist on this website we keep your email or mobile number, whether you're a diner or a restaurant, the area you picked, when you joined and which link brought you here. We use it only to tell you when FIG opens near you and to send FIG news, because you asked for it when you signed up. Every email has an unsubscribe link and you can reply STOP to any text. We never sell it or share it with restaurants or advertisers.</p>''')

page("cookies", "Cookies", "What this website stores on your device.", group="Legal", body='''<p class="doc-kicker">Last updated October 4, 2026</p>
<h1>Cookies</h1>
<p>This website doesn't use advertising or tracking cookies, and there's no analytics script following you around.</p>
<h2>What it does store</h2>
<ul><li><b>Nothing, for most visitors.</b> Browsing the site and joining the waitlist don't set cookies.</li>
<li><b>FIG team only:</b> signing in to the admin page sets one secure, HttpOnly cookie that keeps you signed in for 8 hours, and one that counts wrong password tries.</li></ul>
<h2>Things loaded from other services</h2>
<p>The map tiles come from OpenFreeMap, the animation library from cdnjs and the map library from jsDelivr. They see a normal web request (like any website you visit) but we don't send them anything about you.</p>''')

page("about", "About FIG", "FIG is the restaurant deals app for Markham, Ontario: live deals on a map, free for diners, one $50 a year plan for restaurants.",
     ABOUT.replace("{faq}", '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in ABOUT_FAQ) + "</div>"),
     keywords=BASE_KW + ", about FIG, FIG Technologies, Markham startup", group="Company",
     extra_head=ld({"@context": "https://schema.org", "@type": "AboutPage", "name": "About FIG", "url": SITE_URL + "/about",
                    "mainEntity": {"@type": "Organization", "name": "FIG Technologies Inc.", "url": SITE_URL, "foundingLocation": "Markham, Ontario",
                                   "areaServed": ["Markham, Ontario", "Richmond Hill, Ontario"], "description": "FIG is a restaurant deals app for Markham, Ontario."}}) + faq_ld(ABOUT_FAQ))

page("contact", "Contact", "Get in touch with FIG.", '''<h1>Contact</h1>
<p class="lead-p">A real person reads every message.</p>
<div class="cards">
<a class="card-l" href="mailto:business@fig.app"><b>Restaurants</b><span>Getting set up, your plan, deals and scanning.</span><em>business@fig.app</em></a>
<a class="card-l" href="mailto:privacy@fig.app"><b>Privacy</b><span>See or delete what we hold about you.</span><em>privacy@fig.app</em></a>
<a class="card-l" href="mailto:legal@fig.app"><b>Legal</b><span>Terms and anything official.</span><em>legal@fig.app</em></a>
<a class="card-l" href="/help"><b>Help center</b><span>Answers to the questions people ask most.</span><em>Read the help</em></a>
</div>
<p>In the app, you can also message us from Profile, then Help, then Message us. We reply within 24 hours.</p>''')

HELP = [
    ("diners", "For diners", [
        ("Is FIG free?", "Yes. Deals are free to claim and use. FIG Premium ($6.99/month) is optional and adds AI picks; you can also earn Premium free with stamps."),
        ("How do I use a deal?", "Claim it in the app (we hold it for 24 hours), then show the QR code at the counter when you order. Staff scan it, or type the 8 characters under it."),
        ("Can someone use my screenshot?", "No. Your code changes every 5 minutes, so only the live code on your phone works."),
        ("What do I pay?", "Just your bill, at the restaurant, like normal. FIG never takes payment for food."),
        ("How do stamps work?", "Every deal you use, and every takeout pickup, adds a stamp. Spend 25 for a free week of Premium, 50 for 3 weeks or 100 for a month, again and again."),
        ("Do restaurants see my phone number?", "Never. Chats and takeout go through the app and your number stays private."),
        ("Can I order takeout?", "Yes, where the restaurant offers it. Order from the menu, watch it get made, and pay at the counter when you pick it up. Deals can apply to takeout unless the deal is dine-in only."),
        ("What if a restaurant won't honour a deal?", "Report the visit in the app. A real person looks at every report and replies within 24 hours."),
    ]),
    ("restaurants", "For restaurants", [
        ("What does FIG cost?", "One plan: $50 CAD a year for all your locations. No commission, no fee per diner, no other fees."),
        ("Do I need new equipment?", "No. Any phone or tablet with the FIG app can scan. Add staff and their devices in Settings."),
        ("What if a code won't scan?", "Tap Enter code and type the 8 characters under the diner's QR. It runs the same check as a scan."),
        ("How do I post a deal?", "In the app, open Deals and tap New. Pick the type, the days and hours, who it's for and an optional daily cap. You can pause it anytime."),
        ("When does my page go live?", "As soon as you finish setup (photos, address, hours, cuisine) and start your plan."),
        ("Can I take takeout orders?", "Yes. Turn on takeout and add your menu (you can read it from a photo). Diners pay you at pickup and you scan their pickup code."),
        ("How do I cancel?", "Cancel anytime in the app under Your FIG plan. It runs to the end of the year you paid for."),
    ]),
]
help_html = '<h1>Help center</h1><p class="lead-p">Short answers to the questions people ask most. Still stuck? <a href="/contact">Contact us</a>.</p>'
for anchor, title, qs in HELP:
    help_html += f'<h2 id="{anchor}">{title}</h2><div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qs) + "</div>"
help_html += '<p>Want to see it step by step? Watch the <a href="/#catch">quick tutorial videos</a> for diners and restaurants.</p>'
page("help", "Help center", "Answers for diners and restaurants using FIG.", help_html, group="Main", extra_head=faq_ld([qa for _, _, qs in HELP for qa in qs]))



def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%B} {d.day}, {d.year}"


def read_min(post):
    words = len(re.sub(r"<[^>]+>", " ", " ".join(h for _, h in post["sections"])).split())
    return max(2, round(words / 220))


POSTS.sort(key=lambda x: x["date"], reverse=True)
blog = '<h1>The FIG blog</h1><p class="lead-p">Eating out in Markham for less, and running a busier restaurant. Notes from the FIG team.</p><div class="posts">'
for post in POSTS:
    url = f"/blog/{post['slug']}"
    meta = f"{post['topic']} · {nice_date(post['date'])} · {read_min(post)} min read"
    blog += f'<a class="post-card" href="{url}"><span>{meta}</span><b>{e(post["title"])}</b><p>{e(post["dek"])}</p></a>'
    related = [x for x in POSTS if x is not post and x["topic"] == post["topic"]][:2] or [x for x in POSTS if x is not post][:2]
    body = (f'<p class="doc-kicker"><a href="/blog">Blog</a> · {meta}</p><h1>{e(post["title"])}</h1><p class="lead-p">{e(post["dek"])}</p>'
            + '<div class="doc-short"><h2>Key points</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in post["points"]) + "</ul></div>"
            + "".join(f"<h2>{e(h)}</h2>{t}" for h, t in post["sections"])
            + "<h2>Questions</h2><div class=\"faq\">" + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in post["faq"]) + "</div>"
            + '<h2>Keep reading</h2><div class="cards">' + "".join(f'<a class="card-l" href="/blog/{x["slug"]}"><b>{e(x["title"])}</b><span>{e(x["dek"])}</span></a>' for x in related) + "</div>")
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"], "description": post["dek"], "keywords": post["keywords"],
               "datePublished": post["date"], "dateModified": post["date"], "articleSection": post["topic"], "inLanguage": "en-CA",
               "image": SITE_URL + "/assets/og.png", "mainEntityOfPage": SITE_URL + url,
               "author": {"@type": "Organization", "name": "FIG", "url": SITE_URL},
               "publisher": {"@type": "Organization", "name": "FIG Technologies Inc.", "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/icons/icon-512.png"}}}
    page(url[1:], post["title"], post["dek"], body, group="Blog", keywords=post["keywords"], og_type="article", trail=[("Blog", "/blog")],
         extra_head=ld(article) + faq_ld(post["faq"]))
page("blog", "Blog", "Guides to restaurant deals in Markham and ideas for independent restaurants, from the FIG team.", blog + "</div>", group="Blog",
     keywords=BASE_KW + ", Markham food blog, restaurant marketing blog",
     extra_head=ld({"@context": "https://schema.org", "@type": "Blog", "name": "The FIG blog", "url": SITE_URL + "/blog",
                    "blogPost": [{"@type": "BlogPosting", "headline": x["title"], "url": f"{SITE_URL}/blog/{x['slug']}", "datePublished": x["date"]} for x in POSTS]}))


# =====================================================================  404, site map, sitemap.xml, robots, manifest
page("404", "Page not found", "This page doesn't exist.", body='''<p class="doc-kicker">404</p><h1>This page wandered off.</h1>
<p class="lead-p">It may have moved, or the link has a typo.</p>
<div class="cards"><a class="card-l" href="/"><b>Home</b><span>Local deals, one tap away.</span></a><a class="card-l" href="/#how"><b>How it works</b><span>Find, claim, show, save.</span></a>
<a class="card-l" href="/#owners"><b>For restaurants</b><span>One plan, $50 a year.</span></a><a class="card-l" href="/help"><b>Help center</b><span>Answers to common questions.</span></a></div>''')

# a restaurant shared from the app (/r/<id>?n=<name>&from=<first name>, rewritten to /r.html in vercel.json)
page("r", "Shared with you", "A restaurant someone shared with you on FIG.", body='''<p class="doc-kicker">Shared with you</p><h1 id="r-title">Someone sent you a spot on FIG</h1>
<p class="lead-p" id="r-line">Live deals from restaurants near you. Claim one, show your QR at the counter. Free for diners.</p>
<div class="cards"><a class="card-l" id="r-open" href="/" hidden><b>Open in FIG</b><span>Already have the app? Open this restaurant there.</span></a><a class="card-l" href="/#join"><b>Join the waitlist</b><span>FIG opens in Markham on January 1, 2027.</span></a>
<a class="card-l" href="/#how"><b>How FIG works</b><span>Find, claim, show, save.</span></a></div>
<script src="/js/r.js" defer></script>''')

today = datetime.date.today().isoformat()
prio = lambda p: "1.0" if p == "/" else "0.8" if p in ("/about", "/blog", "/help") else "0.4" if p in ("/terms", "/privacy", "/business-terms", "/cookies") else "0.6"
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}{'' if p == '/' else p}</loc><lastmod>{today}</lastmod><priority>{prio(p)}</priority></url>\n" for p, _, _ in PAGES) + "</urlset>\n"
(SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
LLMS = f"""# FIG

> FIG is a restaurant deals app for Markham, Ontario, Canada. Restaurants post their own deals; diners find them on a map, claim one in a tap and show a rotating QR code at the counter. Free for diners. Restaurants pay one plan of $50 CAD a year with no commission and no fee per diner.

## Facts
- Company: FIG Technologies Inc., Markham, Ontario
- Platforms: iPhone and Android
- Launch area: Markham first, then Richmond Hill, then the rest of York Region and the GTA
- Diners: free; optional FIG Premium $6.99/month (AI picks), or earned free with Passport stamps (25 = 1 week, 50 = 3 weeks, 100 = 1 month)
- Restaurants: $50 CAD/year, every location and scan included, unlimited everyday and flash deals, takeout ordering, chats, dashboard
- How a deal works: claim (held 24 hours), show the QR code (refreshes every 5 minutes), pay the restaurant directly, earn a stamp
- Takeout: order ahead, pay at pickup, no delivery or service fees from FIG
- Privacy: restaurants never see a diner's phone number

## Pages
- [Home]({SITE_URL}/): what FIG is, features, the Passport, pricing
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
print(len(PAGES), "pages; sitemap.xml, robots.txt, site.webmanifest written")
