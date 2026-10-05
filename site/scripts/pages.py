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
HIDDEN = {"404", "r", "business"}  # not indexed, no breadcrumbs, not in the sitemap

NAV_LINKS = [("/#how", "How it works"), ("/#features", "Features"), ("/#passport", "Passport"), ("/#catch", "What's the catch?"), ("/#owners", "For restaurants")]


def nav(current=""):
    links = "".join(f'<a href="{h}"{" class=on aria-current=page" if h == current else ""}>{t}</a>' for h, t in NAV_LINKS)
    return f'''<header class="nav" id="nav">
  <a class="brand" href="/" aria-label="FIG home"><svg class="logo"><use href="#logo"/></svg><span>FIG</span></a>
  <nav class="nav-links" aria-label="Sections">{links}</nav>
  <div class="nav-end">{STORES_NAV}<a class="btn btn-sm nav-get" href="https://apps.apple.com/" target="_blank" rel="noopener" data-get-app>Get FIG</a><button class="nav-menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-sheet"><span></span><span></span></button></div>
  <div class="nav-sheet" id="nav-sheet">{links}{STORES}</div>
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
        <div><h3>Restaurants</h3><a href="/#owners">Pricing</a><a href="/#catch">Tutorial</a><a href="/blog/pay-per-scan-pricing">How pricing works</a><a href="/business">Top up your balance</a><a href="/business-terms">Business terms</a><a href="/help#restaurants">Restaurant help</a></div>
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
index = re.sub(r'<header class="nav".*?</header>', nav(), index, count=1, flags=re.S)
index = re.sub(r'<footer class="foot">.*?</footer>', FOOTER, index, count=1, flags=re.S)
index = re.sub(r'\n  <!-- seo -->.*?<!-- /seo -->', "", index, flags=re.S)
ORG = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "name": "FIG Technologies Inc.", "url": SITE_URL, "logo": SITE_URL + "/assets/icons/icon-512.png",
     "address": {"@type": "PostalAddress", "addressLocality": "Markham", "addressRegion": "ON", "addressCountry": "CA"}},
    {"@type": "WebSite", "name": "FIG", "url": SITE_URL},
    {"@type": "MobileApplication", "name": "FIG", "operatingSystem": "iOS, Android", "applicationCategory": "LifestyleApplication",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"}}]})
index = index.replace('  <meta name="theme-color"', '  <!-- seo -->\n' + head_meta("/", "FIG · Restaurant deals in Markham, Ontario", "Live deals from Markham restaurants, one tap away. Free for diners, free to join for restaurants.",
                      f'\n  <script type="application/ld+json">{ORG}</script>') + '\n  <!-- /seo -->\n  <meta name="theme-color"', 1)
(SITE / "index.html").write_text(index, encoding="utf-8")
PAGES.append(("/", "Home", "Main"))


def ld(obj):
    return '\n  <script type="application/ld+json">' + json.dumps(obj) + "</script>"


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, "item": SITE_URL + u} for k, (n, u) in enumerate(items)]}


def page(slug, title, desc, body, group="More", wide=False, extra_head="", keywords="", og_type="website", trail=None, image="/assets/og.png"):
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
{head_meta(path, title + " · FIG", desc, extra_head, og_type, image)}
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

page("about", "About FIG", "FIG is the restaurant deals app for Markham, Ontario: live deals on a map, free for diners, free to join for restaurants ($1.50 per diner scanned in).",
     ABOUT.replace("{faq}", '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in ABOUT_FAQ) + "</div>"),
     keywords=BASE_KW + ", about FIG, FIG Technologies, Markham startup", group="Company",
     extra_head=ld({"@context": "https://schema.org", "@type": "AboutPage", "name": "About FIG", "url": SITE_URL + "/about",
                    "mainEntity": {"@type": "Organization", "name": "FIG Technologies Inc.", "url": SITE_URL, "foundingLocation": "Markham, Ontario",
                                   "areaServed": ["Markham, Ontario", "Richmond Hill, Ontario"], "description": "FIG is a restaurant deals app for Markham, Ontario."}}) + faq_ld(ABOUT_FAQ))

page("contact", "Contact", "Get in touch with FIG.", '''<h1>Contact</h1>
<p class="lead-p">A real person reads every message.</p>
<div class="cards">
<a class="card-l" href="mailto:business@fig.app"><b>Restaurants</b><span>Getting set up, your balance, deals and scanning.</span><em>business@fig.app</em></a>
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
        ("What does FIG cost?", "Nothing to join or go live, and your first 10 scans are free. Then $1.50 CAD per verified scan from a prepaid balance. No commission, no monthly fee."),
        ("Do I need new equipment?", "No. Any phone or tablet with the FIG app can scan. Add staff and their devices in Settings."),
        ("What if a code won't scan?", "Tap Enter code and type the 8 characters under the diner's QR. It runs the same check as a scan."),
        ("How do I post a deal?", "In the app, open Deals and tap New. Pick the type, the days and hours, who it's for and an optional daily cap. You can pause it anytime."),
        ("When does my page go live?", "As soon as you finish setup: photos, address, hours and cuisine. Nothing to pay first."),
        ("Can I take takeout orders?", "Yes. Turn on takeout and add your menu (you can read it from a photo). Diners pay you at pickup and you scan their pickup code."),
        ("How do I stop?", "There's no subscription. Stop topping up, pause your deals, or close your account in Settings. Ask us within 30 days of closing for a refund of what's left on your balance."),
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
TOPICS = ["For diners", "For restaurants", "News"]


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


slug_id = lambda h: re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")
SHARE = '<button class="share" type="button" data-share><svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M16 6l-4-4-4 4M12 2v13"/></svg><span>Share</span></button>'


def end_cta(post):
    if post["topic"] == "For restaurants":
        return ('<div class="get-app post-cta"><div><h3>Get your restaurant on FIG</h3><p>Free to join. 10 free scans, then $1.50 per diner FIG brings in. No commission.</p></div>'
                f'<div class="badges">{STORE_BTNS}</div></div><p class="more-link"><a href="/#owners">See how pricing works</a></p>')
    return f'<div class="get-app post-cta"><div><h3>Find a deal near you</h3><p>FIG is free for diners. Launching in Markham.</p></div><div class="badges">{STORE_BTNS}</div></div>'


STORE_BTNS = re.search(r'<div class="badges small">(.*)</div>', STORES, re.S).group(1)
chips = "".join(f'<button role="tab" aria-selected="{str(t == "All").lower()}" data-topic="{t}">{t.replace("For ", "").capitalize()}</button>' for t in ["All"] + [t for t in TOPICS if any(x["topic"] == t for x in POSTS)])
blog = ('<h1>The FIG blog</h1><p class="lead-p">Eating out in Markham for less, and running a busier restaurant. Notes from the FIG team.</p>'
        f'<div class="seg blog-filter" role="tablist" aria-label="Filter posts">{chips}</div><div class="posts">')
items = []
for post in POSTS:
    url = f"/blog/{post['slug']}"
    img = cover(post)
    meta = f"{post['topic']} · {nice_date(post['date'])} · {read_min(post)} min read"
    blog += (f'<a class="post-card" href="{url}" data-topic="{post["topic"]}"><img src="{img}" alt="" width="1200" height="630" loading="lazy">'
             f'<div><span>{meta}</span><b>{e(post["title"])}</b><p>{e(post["dek"])}</p></div></a>')
    related = [x for x in POSTS if x is not post and x["topic"] == post["topic"]][:2] or [x for x in POSTS if x is not post][:2]
    toc = '<nav class="toc" aria-label="In this post"><b>In this post</b><ol>' + "".join(f'<li><a href="#{slug_id(h)}">{e(h)}</a></li>' for h, _ in post["sections"]) + "</ol></nav>"
    body = (f'<p class="doc-kicker"><a href="/blog">Blog</a> · {meta}</p><h1>{e(post["title"])}</h1><p class="lead-p">{e(post["dek"])}</p>'
            f'<div class="post-by"><span>By the FIG team · Markham, Ontario</span>{SHARE}</div>'
            f'<img class="post-cover" src="{img}" alt="{e(post["title"])}" width="1200" height="630">'
            + '<div class="doc-short"><h2>Key points</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in post["points"]) + "</ul></div>" + toc
            + "".join(f'<h2 id="{slug_id(h)}">{e(h)}</h2>{t}' for h, t in post["sections"])
            + end_cta(post)
            + "<h2>Questions</h2><div class=\"faq\">" + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in post["faq"]) + "</div>"
            + '<h2>Keep reading</h2><div class="cards">' + "".join(f'<a class="card-l" href="/blog/{x["slug"]}"><b>{e(x["title"])}</b><span>{e(x["dek"])}</span></a>' for x in related) + "</div>")
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"], "description": post["dek"], "keywords": post["keywords"],
               "datePublished": post["date"], "dateModified": post.get("updated", post["date"]), "articleSection": post["topic"], "inLanguage": "en-CA",
               "image": SITE_URL + img, "mainEntityOfPage": SITE_URL + url, "wordCount": len(re.sub(r"<[^>]+>", " ", " ".join(t for _, t in post["sections"])).split()),
               "author": {"@type": "Organization", "name": "FIG", "url": SITE_URL},
               "publisher": {"@type": "Organization", "name": "FIG Technologies Inc.", "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/icons/icon-512.png"}}}
    page(url[1:], post["title"], post["dek"], body, group="Blog", keywords=post["keywords"], og_type="article", trail=[("Blog", "/blog")], image=img,
         extra_head=ld(article) + faq_ld(post["faq"]))
    items.append(f"""  <item><title>{e(post['title'])}</title><link>{SITE_URL}{url}</link><guid>{SITE_URL}{url}</guid>
    <pubDate>{datetime.date.fromisoformat(post['date']):%a, %d %b %Y} 12:00:00 -0400</pubDate><category>{e(post['topic'])}</category><description>{e(post['dek'])}</description></item>
""")
page("blog", "Blog", "Guides to restaurant deals in Markham and ideas for independent restaurants, from the FIG team.", blog + "</div>", group="Blog",
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
page("404", "Page not found", "This page doesn't exist.", body='''<p class="doc-kicker">404</p><h1>This page wandered off.</h1>
<p class="lead-p">It may have moved, or the link has a typo.</p>
<div class="cards"><a class="card-l" href="/"><b>Home</b><span>Local deals, one tap away.</span></a><a class="card-l" href="/#how"><b>How it works</b><span>Find, claim, show, save.</span></a>
<a class="card-l" href="/#owners"><b>For restaurants</b><span>Free to join, $1.50 a scan.</span></a><a class="card-l" href="/help"><b>Help center</b><span>Answers to common questions.</span></a></div>''')

# a restaurant shared from the app (/r/<id>?n=<name>&from=<first name>, rewritten to /r.html in vercel.json)
page("r", "Shared with you", "A restaurant someone shared with you on FIG.", body='''<p class="doc-kicker">Shared with you</p><h1 id="r-title">Someone sent you a spot on FIG</h1>
<p class="lead-p" id="r-line">Live deals from restaurants near you. Claim one, show your QR at the counter. Free for diners.</p>
<div class="cards"><a class="card-l" id="r-open" href="/" hidden><b>Open in FIG</b><span>Already have the app? Open this restaurant there.</span></a><a class="card-l" href="/#join"><b>Join the waitlist</b><span>FIG opens in Markham on January 1, 2027.</span></a>
<a class="card-l" href="/#how"><b>How FIG works</b><span>Find, claim, show, save.</span></a></div>
<script src="/js/r.js" defer></script>''')


# ---- /business: restaurant owners top up their balance (js/business.js); not indexed
page("business", "Restaurant balance", "Top up your FIG restaurant balance: $1.50 per scan, $20, $50, $100 or any amount.", body='''<style>
.bal{max-width:560px;margin:0 auto}.bal .kick{color:var(--cobalt);font-weight:800;letter-spacing:.08em;font-size:12px;text-transform:uppercase}
.bal h1{margin:6px 0 4px}.bal .sub-l{color:var(--muted);margin:0 0 24px}
.bal-box{border:1.5px solid var(--line);border-radius:24px;padding:22px;margin:0 0 16px;background:var(--bg)}
.bal-box h2{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.bal-box label{display:block;font-weight:700;font-size:14px;margin:12px 0 6px}
.bal-box input[type=email],.bal-box input[type=password],.bal-box input[type=text],.bal-box select{width:100%;height:50px;border-radius:14px;border:1.5px solid var(--line);background:var(--card);padding:0 14px;font:inherit;font-size:16px;color:var(--text)}
.bal-box input:focus,.bal-box select:focus{outline:none;border-color:var(--cobalt);background:var(--ice)}
.bal-box .btn{width:100%;justify-content:center;margin-top:16px}.bal-or{text-align:center;color:var(--muted);font-size:13px;margin:14px 0 0}
.bal-hero{border-radius:28px;padding:24px;color:#fff;background:linear-gradient(135deg,#3B78FF,#1E5EFF 42%,#1239B8);box-shadow:0 18px 40px rgba(30,94,255,.3);margin:0 0 16px}
.bal-hero .row{display:flex;justify-content:space-between;align-items:center;gap:12px}.bal-hero small{opacity:.8;font-weight:800;letter-spacing:.08em;font-size:12px}
.bal-amount{font-size:60px;font-weight:800;letter-spacing:-.04em;line-height:1.05;margin:10px 0 4px}.bal-line{color:var(--volt);font-weight:700}
.bal-pill{border-radius:99px;padding:4px 12px;font-size:12px;font-weight:800}.bal-pill.volt{background:var(--volt);color:#0A1020}.bal-pill.red{background:#FDECEC;color:#C9353A}.bal-pill.amber{background:#FFE7A8;color:#0A1020}
.bal-warn{border:1.5px solid #E5484D;background:#FDECEC;color:#8A2A2E;border-radius:20px;padding:14px 16px;margin:0 0 16px;font-weight:600;font-size:14px}
.bal-note{border-radius:18px;padding:14px 16px;margin:0 0 16px;font-weight:700;font-size:14px}.bal-note.wait{background:var(--ice);color:var(--text)}.bal-note.done{background:#E3F7EF;color:#067A55}
.amts{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.amts button{height:44px;padding:0 18px;border-radius:99px;border:1.5px solid var(--line);background:var(--bg);font:inherit;font-weight:800;color:var(--text);cursor:pointer}
.amts button.on{background:#0A1020;border-color:#0A1020;color:#fff}.bal-meta{display:flex;justify-content:space-between;color:var(--muted);font-size:13px;font-weight:600}
.toggle{display:flex;justify-content:space-between;align-items:center;gap:12px;font-weight:800}.toggle input{width:22px;height:22px;accent-color:var(--cobalt)}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.three label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.acts{list-style:none;margin:8px 0 0;padding:0}.acts li{display:flex;justify-content:space-between;gap:12px;padding:12px 0;border-top:1px solid var(--line)}.acts li:first-child{border-top:0}
.acts small{display:block;color:var(--muted);font-size:12px}.acts em{font-style:normal;font-weight:800}.acts em.plus{color:#067A55}.acts .empty{color:var(--muted);justify-content:center}
.bal-foot{display:flex;justify-content:space-between;color:var(--muted);font-size:13px;margin:8px 0 0}.linkbtn{border:0;background:none;color:var(--cobalt);font:inherit;font-weight:800;cursor:pointer;padding:0}
@media (max-width:480px){.three{grid-template-columns:1fr}.bal-amount{font-size:48px}}
</style>
<div class="bal">
<p class="kick">FIG for restaurants</p>
<h1>Your balance</h1>
<p class="sub-l">$1.50 per scan, only when a FIG diner’s code is scanned. Top up here and the FIG app shows it within seconds.</p>

<section id="bal-out" hidden>
  <form class="bal-box" id="s-form">
    <h2>Sign in</h2>
    <p class="hint">Use the email and password of your FIG business account.</p>
    <label for="s-email">Email</label><input id="s-email" type="email" autocomplete="email" required>
    <label for="s-pass">Password</label><input id="s-pass" type="password" autocomplete="current-password" required>
    <p class="form-msg" id="s-msg" hidden></p>
    <button class="btn btn-ink" type="submit">Sign in</button>
    <button class="btn btn-ghost" type="button" id="s-google">Continue with Google</button>
    <p class="bal-or">Forgot your password? Reset it in the FIG app: Sign in, then Forgot?</p>
  </form>
</section>

<section id="bal-none" hidden>
  <div class="bal-box"><h2>No restaurant here</h2><p>This account isn’t the owner or a manager of a restaurant on FIG. Sign in with your business account, or <a href="/#owners">see how FIG works for restaurants</a>.</p>
  <button class="linkbtn" type="button" data-out>Sign out</button></div>
</section>

<section id="bal-in" hidden>
  <p class="bal-note" id="b-note" hidden></p>
  <div class="bal-hero">
    <div class="row"><small>YOUR BALANCE</small><span class="bal-pill" id="b-pill"></span></div>
    <div style="opacity:.85;font-weight:700;margin-top:10px" id="b-name"></div>
    <div class="bal-amount" id="b-amount">$0.00</div>
    <div class="bal-line" id="b-line"></div>
  </div>
  <p class="bal-warn" id="b-paused" hidden>Your deals are paused. Diners can still see your page, but can’t claim deals until you top up. Deals already claimed still work.</p>

  <div class="bal-box">
    <h2>Add to your balance</h2>
    <div class="amts"><button type="button" data-amt="20">$20</button><button type="button" data-amt="50">$50</button><button type="button" data-amt="100">$100</button><button type="button" data-amt="custom">Custom</button></div>
    <div id="t-custom" hidden><label for="t-amt">Amount (CAD)</label><input id="t-amt" type="text" inputmode="decimal" placeholder="$10 to $500"></div>
    <div class="bal-meta"><span id="t-scans"></span><span id="b-card"></span></div>
    <p class="form-msg" id="t-msg" hidden></p>
    <button class="btn btn-volt" type="button" id="t-go">Top up</button>
    <p class="bal-or">Paid securely through Stripe. Receipts come by email.</p>
  </div>

  <div class="bal-box">
    <div class="toggle"><span>Automatic top-up</span><input type="checkbox" id="a-on" aria-label="Automatic top-up"></div>
    <p class="hint">Never pause: FIG tops you up when you run low.</p>
    <div id="a-fields" hidden>
      <div class="three">
        <div><label for="a-below">When under</label><select id="a-below"><option value="5">$5</option><option value="10">$10</option><option value="20">$20</option></select></div>
        <div><label for="a-amount">Add</label><select id="a-amount"><option value="20">$20</option><option value="50">$50</option><option value="100">$100</option></select></div>
        <div><label for="a-limit">Max a month</label><select id="a-limit"><option value="100">$100</option><option value="200">$200</option><option value="500">$500</option></select></div>
      </div>
      <p class="hint" id="a-card"></p>
    </div>
    <p class="form-msg" id="a-msg" hidden></p>
  </div>

  <div class="bal-box"><h2>Activity</h2><ul class="acts" id="b-activity"></ul></div>
  <div class="bal-foot"><span>$1.50 per scan · <a href="/business-terms">Business terms</a></span><button class="linkbtn" type="button" data-out>Sign out</button></div>
</section>
</div>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.117.2/dist/umd/supabase.min.js"></script>
<script src="/js/business.js" defer></script>''')

today = datetime.date.today().isoformat()
prio = lambda p: "1.0" if p == "/" else "0.8" if p in ("/about", "/blog", "/help") else "0.4" if p in ("/terms", "/privacy", "/business-terms", "/cookies") else "0.6"
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}{'' if p == '/' else p}</loc><lastmod>{today}</lastmod><priority>{prio(p)}</priority></url>\n" for p, _, _ in PAGES) + "</urlset>\n"
(SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
LLMS = f"""# FIG

> FIG is a restaurant deals app for Markham, Ontario, Canada. Restaurants post their own deals; diners find them on a map, claim one in a tap and show a rotating QR code at the counter. Free for diners. Restaurants join free and pay $1.50 CAD only when a FIG diner's code is scanned, with no commission.

## Facts
- Company: FIG Technologies Inc., Markham, Ontario
- Platforms: iPhone and Android
- Launch area: Markham first, then Richmond Hill, then the rest of York Region and the GTA
- Diners: free; optional FIG Premium $6.99/month (AI picks), or earned free with Passport stamps (25 = 1 week, 50 = 3 weeks, 100 = 1 month)
- Restaurants: free to join and go live, 10 free scans, then $1.50 CAD per verified scan from a prepaid balance (top-ups $20/$50/$100 or custom, optional automatic top-up); unlimited everyday and flash deals, takeout ordering, chats, dashboard
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
