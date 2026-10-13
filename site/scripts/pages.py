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
MEGA = re.search(r'<div class="mega".*?Save fast\.</span>\s*</div>', index, re.S).group(0)
STORES = re.search(r'<div class="badges small">.*?</div>', index, re.S).group(0)
SECTION = lambda sid: re.search(rf'<section class="section[^"]*" id="{sid}">.*?</section>', index, re.S).group(0)
e = html.escape
BASE_KW = "FIG, FIG app, restaurant deals Markham, Markham restaurants, food deals Ontario, local restaurant deals app"
PAGES = []  # (path, title, group) for sitemap.xml and the site map page
HIDDEN = {"404", "r", "paid", "stripe", "premium-on"}  # not indexed, no breadcrumbs, not in the sitemap

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
        <p>Live deals from local restaurants, on a map. Starting in Markham, Ontario. Richmond Hill next.</p>
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
  <link rel="stylesheet" href="/css/pages.css">
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
    """Where Stripe sends people back (and Ads off): one card over the faded map, Open FIG and one more link."""
    return f'''<section class="st"><div class="st-card">
<div class="st-badge{" " + cls if cls else ""}" aria-hidden="true">{icon}</div>
<h1 class="st-h1">{title}</h1><p class="st-lead">{lead}</p>{f'<p class="st-note">{note}</p>' if note else ""}
<div class="st-btns">{second}</div>
</div></section>'''


def faq_ld(qs):
    return '\n  <script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}) + "</script>"


LEGAL_TABS = [("terms", "Terms of service"), ("privacy", "Privacy policy"), ("business-terms", "Business terms")]


def para(p):
    """A legal paragraph: lines that start with a bullet become a bullet."""
    return f'<p class="lg-bullet">{e(p[1:].strip())}</p>' if p.startswith("•") else f"<p>{e(p)}</p>"


def legal(slug, doc, extra=""):
    short = "".join(f"<li>{e(x)}</li>" for x in doc["short"])
    secs = [(s["heading"], "".join(para(p) for p in s["paragraphs"])) for s in doc["sections"]]
    if extra:  # (title, html) sections only this page has
        secs += [(h, t) for h, t in extra]
    tabs = '<nav class="pg-pills" aria-label="Legal documents">' + "".join(
        f'<a href="/{s}"{" aria-current=page" if s == slug else ""}>{t}</a>' for s, t in LEGAL_TABS) + "</nav>"
    rail = '<nav class="lg-rail" aria-label="On this page"><b>On this page</b>' + "".join(f'<a href="#{slug_id(h)}">{e(h)}</a>' for h, _ in secs) + "</nav>"
    doc_html = (f'<div class="pg-short"><h2>The short version</h2><ul>{short}</ul></div>'
                + "".join(f'<section class="lg-sec" id="{slug_id(h)}"><h2>{e(h)}</h2>{t}</section>' for h, t in secs)
                + f'<div class="lg-ask"><div><b>{e(doc["contactAsk"])}</b><span>{e(doc["contactLine"])}</span></div><a class="btn" href="/contact">Contact us</a></div>')
    body = (hero(e(doc["title"]), e(doc["updated"]), tabs if slug in dict(LEGAL_TABS) else "", cls="pg-hero-line")
            + f'<section class="section lg"><div class="wrap lg-grid">{rail}<article class="lg-doc">{doc_html}</article></div></section>')
    page(slug, doc["title"], doc["short"][0], body, group="Legal", wide=True)


L = json.loads((SITE / "scripts" / "legal.json").read_text(encoding="utf-8"))
legal("terms", L["terms"])
legal("business-terms", L["business-terms"])
legal("privacy", L["privacy"], [("The website waitlist", '''<p>When you join the waitlist on this website we keep your email or mobile number, whether you're a diner or a restaurant, the area you picked, when you joined and which link brought you here. We use it only to tell you when FIG opens near you and to send FIG news, because you asked for it when you signed up. Every email has an unsubscribe link and you can reply STOP to any text. We never sell it or share it with restaurants or advertisers.</p>''')])

page("cookies", "Cookies", "What this website stores on your device.", group="Legal", wide=True, body=hero("Cookies", "Last updated October 4, 2026", cls="pg-hero-line") + '''<section class="section lg"><div class="wrap"><article class="lg-doc lg-solo">
<p>This website doesn't use advertising or tracking cookies, and there's no analytics script following you around.</p>
<h2>What it does store</h2>
<ul><li><b>Nothing, for most visitors.</b> Browsing the site and joining the waitlist don't set cookies.</li>
<li><b>FIG team only:</b> signing in to the admin page sets one secure, HttpOnly cookie that keeps you signed in for 8 hours, and one that counts wrong password tries.</li></ul>
<h2>Things loaded from other services</h2>
<p>The map tiles come from OpenFreeMap, the animation library from cdnjs and the map library from jsDelivr. They see a normal web request (like any website you visit) but we don't send them anything about you.</p>
</article></div></section>''')

page("about", "About FIG", "FIG is the restaurant deals app for Markham, Ontario: live deals on a map, free for diners and free for restaurants.",
     hero('The restaurant deals app for <span class="accent">Markham.</span>',
          "Live deals from local restaurants, on a map. Diners claim a deal in one tap and show a code at the counter. Restaurants join free, post deals free and pay no commission on dine-in.",
          '<div class="ab-photos" aria-hidden="true"><img src="/assets/about/dumpling-house.webp" srcset="/assets/about/dumpling-house-360.webp 360w, /assets/about/dumpling-house.webp 720w" sizes="180px" alt="" width="720" height="1040"><img src="/assets/about/brew-lab.webp" srcset="/assets/about/brew-lab-360.webp 360w, /assets/about/brew-lab.webp 720w" sizes="180px" alt="" width="720" height="1360"></div>', "ab-hero")
     + ABOUT.replace("{faq}", qa_list(ABOUT_FAQ, 1)), wide=True,
     keywords=BASE_KW + ", about FIG, FIG Technologies, Markham startup", group="Company",
     extra_head=ld({"@context": "https://schema.org", "@type": "AboutPage", "name": "About FIG", "url": SITE_URL + "/about",
                    "mainEntity": {"@type": "Organization", "name": "FIG Technologies Inc.", "url": SITE_URL, "foundingLocation": "Markham, Ontario",
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
        ("How do I use a deal?", "Claim it in the app. It waits in your Voucher tab for as long as the deal runs. Show the QR code at the counter when you order, and staff scan it or type the 8 characters under it."),
        ("Can someone use my screenshot?", "No. Your code changes every 5 minutes, so only the live code on your phone works."),
        ("What do I pay?", "Just your bill, like normal, with the deal taken off. Some restaurants let you pay for takeout in the app; that money goes to the restaurant. FIG never charges diners anything."),
        ("How do reviews work?", "Only diners whose visit was scanned can review, so every review comes from a real visit. Rate a visit right after it, or later from Past visits in your Voucher tab."),
        ("Do restaurants see my phone number?", "Never. Chats and takeout orders go through the app and your number stays private."),
        ("Can I order takeout?", "Yes. Tap Takeout on a deal that allows it, add what you want, watch it get made, and pick it up. Some restaurants also take takeout at full price: tap Order takeout on their page. FIG doesn't deliver."),
        ("What if a restaurant won't honour a deal?", "Report the visit in the app. A real person looks at every report and replies within 24 hours."),
    ]),
    ("restaurants", "For restaurants", [
        ("What does FIG cost?", "Nothing for dine-in. Joining, your page, deals, scans and chats are free, with no commission on dine-in. On takeout orders diners pay for in the app, FIG keeps 5% of the food (before tax), and Stripe's card fee comes off the same payment. FIG Premium is optional, $50 a year."),
        ("Do I need new equipment?", "No. Any phone, tablet or computer can scan: open FIG on the web (the iPhone and Android apps are coming soon). Add staff and their devices in Settings."),
        ("What if a code won't scan?", "Tap Enter code and type the 8 characters under the diner's QR. It runs the same check as a scan."),
        ("How do I post a deal?", "In the app, open Deals and tap New. Pick the dishes (or the whole order, for dine-in), the offer, the days and hours, and check it the way diners will see it. You can pause it anytime, or post an ended deal again in one tap."),
        ("When does my page go live?", "As soon as you finish setup: photos, address, hours and cuisine. Nothing to pay first."),
        ("Can diners order takeout?", "Yes. Add your menu: first the sections, then the dishes in each. Turn on takeout and pick how many deals one order can use: 1, 2, 3, more or no limit, or 0 to take orders at full price. You scan their pickup code when they collect."),
        ("How do I stop?", "There's nothing to cancel. Pause your deals, or close your account in Settings anytime."),
    ]),
]
HELP_HEAD = {"diners": ("Eating out with FIG", "Claiming, codes, paying and takeout."), "restaurants": ("Running deals on FIG", "Cost, scanning, deals and takeout.")}
# a real app screen under each section's title: the diner's QR, the restaurant's dashboard (tablet)
HELP_SHOT = {"diners": ('qr', "The QR a diner shows at the counter", "phone"), "restaurants": ('tdash', "A restaurant's FIG dashboard", "wide")}
help_html = hero("How can we help?", "Short answers to the questions people ask most. Still stuck? A real person replies within 24 hours.",
                 '<nav class="pg-pills" aria-label="Jump to">' + "".join(f'<a href="#{a}">{t}</a>' for a, t, _ in HELP) + "</nav>", cls="pg-hero-line")
for k, (anchor, title, qs) in enumerate(HELP):
    head, sub = HELP_HEAD[anchor]
    help_html += (f'<section class="section{" ice" if k else ""}" id="{anchor}"><div class="wrap faq"><div class="faq-head">'
                  f'<h2 class="h2">{head}</h2><p class="side">{sub}</p><figure class="help-shot {HELP_SHOT[anchor][2]}"><img src="/assets/screens/{HELP_SHOT[anchor][0]}.webp" alt="{HELP_SHOT[anchor][1]}"></figure></div>{qa_list(qs, 1 if k else 2)}</div></section>')
help_html += '''<section class="section pg-tight"><div class="wrap"><div class="pg-dark">
<div><h2>Still stuck?</h2><p>Message us and a real person replies within 24 hours. Or watch the quick tutorial videos for diners and restaurants.</p></div>
<div class="pg-dark-btns"><a class="btn btn-lg" href="/contact">Contact us</a><a class="btn btn-lg btn-line" href="/#catch">Watch the tutorials</a></div>
</div></div></section>'''
page("help", "Help center", "Answers for diners and restaurants using FIG.", help_html, group="Main", wide=True, extra_head=faq_ld([qa for _, _, qs in HELP for qa in qs]))



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


SHARE = '<button class="share" type="button" data-share><svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M16 6l-4-4-4 4M12 2v13"/></svg><span>Share</span></button>'


def end_cta(post):
    """The cobalt block at the end of a post: restaurants get listed, diners open FIG (the web app, 2026-10-13)."""
    if post["topic"] == "For restaurants":
        words, btns = ("<h2>Get your restaurant on FIG.</h2><p>Free to join. Free deals and scans, with no commission on dine-in.</p>",
                       '<a class="btn btn-lg btn-volt" href="/app/sign-up-business">List your restaurant</a><a class="btn btn-lg btn-line" href="/#owners">See how pricing works</a>')
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
chips = "".join(f'<button role="tab" aria-selected="{str(t == "All").lower()}" data-topic="{t}">{t.replace("For ", "").capitalize()}</button>' for t in ["All"] + [t for t in TOPICS if any(x["topic"] == t for x in POSTS)])
blog = hero("Eat out for less.<br>Fill the quiet hours.", "", f'<div class="pg-pills blog-filter" role="tablist" aria-label="Filter posts">{chips}</div>')
rows = []
items = []
for k, post in enumerate(POSTS):
    url = f"/blog/{post['slug']}"
    img = cover(post)
    pic = photo_of(post, img)
    meta = f"{post['topic']} · {nice_date(post['date'])} · {read_min(post)} min read"
    kicker = f"{post['topic']} · {nice_date(post['date'])}"
    if k == 0:
        blog += (f'<section class="section ice bl-feature-band"><div class="wrap"><a class="post-card bl-feature" href="{url}" data-topic="{post["topic"]}">'
                 f'<span class="bl-pic"><img src="{pic}" alt="" width="720" height="480"><i>Newest</i></span>'
                 f'<span class="bl-text"><span class="pg-kick">{kicker}</span><b>{e(post["title"])}</b><p>{e(post["dek"])}</p><em>Read the post</em></span></a></div></section>')
    else:
        rows.append(f'<a class="post-card bl-row" href="{url}" data-topic="{post["topic"]}"><img {thumb(pic)} alt="" width="240" height="168" loading="lazy">'
                    f'<span><span class="pg-kick">{kicker}</span><b>{e(post["title"])}</b><p>{e(post["dek"])}</p></span></a>')
    related = [x for x in POSTS if x is not post and x["topic"] == post["topic"]][:2] or [x for x in POSTS if x is not post][:2]
    body = (f'''<section class="ps-head"><div class="wrap"><a class="ps-back" href="/blog">← The FIG blog</a><p class="pg-kick">{e(kicker)}</p>
<h1 class="ps-h1">{e(post["title"])}</h1><p class="ps-dek">{e(post["dek"])}</p><div class="post-by"><span>By the FIG team · Markham, Ontario · {read_min(post)} min read</span>{SHARE}</div></div></section>
<div class="wrap"><img class="ps-cover" src="{pic}" alt="{e(post["title"])}" width="1200" height="560"></div>'''
            + '<article class="ps-body"><div class="pg-short"><h2>Key points</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in post["points"]) + "</ul></div>"
            + "".join(f'<h2 id="{slug_id(h)}">{e(h)}</h2>{t}' for h, t in post["sections"])
            + '<h2>Questions</h2>' + qa_list(post["faq"])
            + "</article>" + end_cta(post)
            + '<section class="section ps-more"><div class="wrap"><h2 class="h2 pg-sub">Keep reading</h2><div class="bl-list">'
            + "".join(f'<a class="post-card bl-row" href="/blog/{x["slug"]}" data-topic="{x["topic"]}"><img {thumb(photo_of(x, ""))} alt="" width="240" height="168" loading="lazy"><span><span class="pg-kick">{x["topic"]} · {nice_date(x["date"])}</span><b>{e(x["title"])}</b><p>{e(x["dek"])}</p></span></a>' for x in related)
            + "</div></div></section>")
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"], "description": post["dek"], "keywords": post["keywords"],
               "datePublished": post["date"], "dateModified": post.get("updated", post["date"]), "articleSection": post["topic"], "inLanguage": "en-CA",
               "image": SITE_URL + img, "mainEntityOfPage": SITE_URL + url, "wordCount": len(re.sub(r"<[^>]+>", " ", " ".join(t for _, t in post["sections"])).split()),
               "author": {"@type": "Organization", "name": "FIG", "url": SITE_URL},
               "publisher": {"@type": "Organization", "name": "FIG Technologies Inc.", "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/icons/icon-512.png"}}}
    page(url[1:], post["title"], post["dek"], body, group="Blog", wide=True, keywords=post["keywords"], og_type="article", trail=[("Blog", "/blog")], image=img,
         extra_head=ld(article) + faq_ld(post["faq"]))
    items.append(f"""  <item><title>{e(post['title'])}</title><link>{SITE_URL}{url}</link><guid>{SITE_URL}{url}</guid>
    <pubDate>{datetime.date.fromisoformat(post['date']):%a, %d %b %Y} 12:00:00 -0400</pubDate><category>{e(post['topic'])}</category><description>{e(post['dek'])}</description></item>
""")
page("blog", "Blog", "Guides to restaurant deals in Markham and ideas for independent restaurants, from the FIG team.",
     blog + '<section class="section bl-rows"><div class="wrap bl-list">' + "".join(rows) + "</div></section>", group="Blog", wide=True,
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
<a class="card-l" href="/#owners"><b>For restaurants</b><span>Free to join and post deals.</span></a><a class="card-l" href="/help"><b>Help center</b><span>Answers to common questions.</span></a></div>''')

# a restaurant shared from the app (/r/<id>?n=<name>&from=<first name>, rewritten to /r.html in vercel.json)
page("r", "Shared with you", "A restaurant someone shared with you on FIG.", body='''<div class="r-bubble" aria-hidden="true"><b id="r-from">A friend</b><span>dinner here?</span></div>
<h1 id="r-title">Someone sent you a spot on FIG</h1>
<p class="lead-p" id="r-line">Live deals from restaurants near you. Claim one, show your QR at the counter. Free for diners.</p>
<div class="r-actions"><a class="btn btn-lg" id="r-web" href="/app/">See it on FIG</a><a class="btn btn-lg btn-ghost" href="/#how">How FIG works</a></div>
<p class="r-app"><a id="r-open" href="/" hidden>Have the FIG app? Open it there</a></p>
<script src="/js/r.js" defer></script>''')


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

today = datetime.date.today().isoformat()
prio = lambda p: "1.0" if p == "/" else "0.8" if p in ("/about", "/blog", "/help") else "0.4" if p in ("/terms", "/privacy", "/business-terms", "/cookies") else "0.6"
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}{'' if p == '/' else p}</loc><lastmod>{today}</lastmod><priority>{prio(p)}</priority></url>\n" for p, _, _ in PAGES) + "</urlset>\n"
(SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
LLMS = f"""# FIG

> FIG is a restaurant deals app for Markham, Ontario, Canada. Restaurants post their own deals; diners find them on a map, claim one in a tap and show a rotating QR code at the counter. Free for diners. Free for restaurants to list, post deals and scan, with no commission on dine-in. FIG is paid by the optional FIG Premium ($50 a year: unlimited locations, deal announcements every 2 hours, area insights, menu from a photo) and 5% of the food on takeout orders diners pay for in the app.

## Facts
- Company: FIG Technologies Inc., Markham, Ontario
- Platforms: iPhone and Android
- Launch area: Markham first, then Richmond Hill, then the rest of York Region and the GTA
- Diners: free; no loyalty points, rewards or AI features
- Restaurants: free (listing, unlimited everyday and flash deals, scans, chats, dashboard); takeout orders paid in the app: FIG keeps 5% of the food before tax, and Stripe's card fee comes off the same payment; free insights (views, claims, diners who came in and came back); no ads
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
print(len(PAGES), "pages; sitemap.xml, robots.txt, site.webmanifest written")
