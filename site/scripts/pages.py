"""Builds the whole site around index.html: nav, footer, every extra page, sitemap.xml, robots.txt and the web manifest.

run: python site/scripts/pages.py
- Legal pages come from legal.json (exported from the app's src/content/legal.ts, so they match the app word for word).
- Nav and footer are written into index.html too, so every page shares them.
- Sections that also live on the home page (how it works, features, restaurants) are copied from index.html, so they never drift.
- SITE_URL is the address search engines see: change it once figpromo.com is connected.
"""
import datetime, html, json, pathlib, re

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
PAGES = []  # (path, title, group) for sitemap.xml and the site map page

NAV_LINKS = [("/how-it-works", "How it works"), ("/features", "Features"), ("/#owners", "Pricing"), ("/restaurants", "For restaurants"), ("/help", "Help")]


def nav(current=""):
    links = "".join(f'<a href="{h}"{" class=on aria-current=page" if h == current else ""}>{t}</a>' for h, t in NAV_LINKS)
    return f'''<header class="nav" id="nav">
  <a class="brand" href="/" aria-label="FIG home"><svg class="logo"><use href="#logo"/></svg><span>FIG</span></a>
  <nav class="nav-links" aria-label="Main">{links}</nav>
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
        <div><h3>Diners</h3><a href="/how-it-works">How it works</a><a href="/features">Features</a><a href="/passport">Passport</a><a href="/how-it-works#tutorial">Diner tutorial</a><a href="/#owners">Pricing</a><a href="/help">Help center</a></div>
        <div><h3>Restaurants</h3><a href="/restaurants">FIG for restaurants</a><a href="/#owners">Pricing</a><a href="/restaurants#tutorial">Restaurant tutorial</a><a href="/business-terms">Business terms</a><a href="/help#restaurants">Restaurant help</a></div>
        <div><h3>Company</h3><a href="/about">About</a><a href="/blog">Blog</a><a href="/press">Press kit</a><a href="/contact">Contact</a><a href="/sitemap">Site map</a></div>
        <div><h3>Legal</h3><a href="/terms">Terms of service</a><a href="/privacy">Privacy policy</a><a href="/business-terms">Business terms</a><a href="/cookies">Cookies</a></div>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 FIG Technologies Inc. · Markham, Ontario · <a class="admin-link" href="/admin">Are you the admin?</a></span>
      <span>App screens show example restaurants and deals. Map data © OpenStreetMap contributors, OpenFreeMap. App Store is a trademark of Apple Inc. Google Play is a trademark of Google LLC.</span>
    </div>
  </div>
</footer>'''


def head_meta(path, title, desc, extra=""):
    url = SITE_URL + ("" if path == "/" else path)
    return f'''  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
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
index = index.replace('  <meta name="theme-color"', '  <!-- seo -->\n' + head_meta("/", "FIG · Local deals in Markham", "Live deals from Markham restaurants, one tap away.",
                      f'\n  <script type="application/ld+json">{ORG}</script>') + '\n  <!-- /seo -->\n  <meta name="theme-color"', 1)
(SITE / "index.html").write_text(index, encoding="utf-8")
PAGES.append(("/", "Home", "Main"))


def page(slug, title, desc, body, group="More", wide=False, extra_head=""):
    path = "/" + slug
    current = path if path in dict(NAV_LINKS) else ""
    out = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)} · FIG</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{head_meta(path, title + " · FIG", desc, extra_head)}
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
<script src="/js/sub.js" defer></script>
</body>
</html>
'''
    p = SITE / (slug + ".html")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")
    if slug != "404":
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
<p>When you join the waitlist on this website we keep your email or mobile number, whether you're a diner or a restaurant, the area you picked, when you joined and which link brought you here. We use it only to tell you when FIG opens near you and to send FIG news, because you ticked the consent box. Every email has an unsubscribe link and you can reply STOP to any text. We never sell it or share it with restaurants or advertisers.</p>''')

page("cookies", "Cookies", "What this website stores on your device.", group="Legal", body='''<p class="doc-kicker">Last updated October 4, 2026</p>
<h1>Cookies</h1>
<p>This website doesn't use advertising or tracking cookies, and there's no analytics script following you around.</p>
<h2>What it does store</h2>
<ul><li><b>Nothing, for most visitors.</b> Browsing the site and joining the waitlist don't set cookies.</li>
<li><b>FIG team only:</b> signing in to the admin page sets one secure, HttpOnly cookie that keeps you signed in for 8 hours, and one that counts wrong password tries.</li></ul>
<h2>Things loaded from other services</h2>
<p>The map tiles come from OpenFreeMap, the animation library from cdnjs and the map library from jsDelivr. They see a normal web request (like any website you visit) but we don't send them anything about you.</p>''')

page("about", "About", "FIG puts live deals from local restaurants on a map.", '''<h1>Eat local. Save fast.</h1>
<p class="lead-p">FIG is a deals app for local restaurants, starting in Markham, Ontario.</p>
<h2>Why FIG</h2>
<p>Great independent restaurants are everywhere in Markham, but they're hard to find and harder to fill on a slow Tuesday afternoon. Delivery apps take a big cut of every order, so a lot of owners stay off them.</p>
<p>FIG flips that. Restaurants post their own deals and pay one plan, $50 a year, with no commission and no fee per diner. Diners find those deals on a map, claim one, show a code at the counter and earn stamps they can spend on free Premium.</p>
<h2>How we build it</h2>
<ul><li><b>Honest deals.</b> Every deal and its hours are set by the restaurant. Timers are real.</li>
<li><b>Private by default.</b> Restaurants never see a diner's phone number, even for takeout.</li>
<li><b>Local first.</b> Markham now, Richmond Hill next, then the rest of the GTA.</li></ul>
<h2>Get in touch</h2>
<p>Restaurant owners: <a href="/owners">see how FIG works for you</a>. Everyone else: <a href="/contact">say hello</a>.</p>''')

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
help_html += '<p>Want to see it step by step? Watch the <a href="/how-it-works#tutorial">diner tutorial</a> or the <a href="/restaurants#tutorial">restaurant tutorial</a>.</p>'
page("help", "Help center", "Answers for diners and restaurants using FIG.", help_html, group="Main", extra_head=faq_ld([qa for _, _, qs in HELP for qa in qs]))

page("press", "Press kit", "FIG logos, colours and facts.", '''<h1>Press kit</h1>
<p class="lead-p">Logos, colours and the facts about FIG. Please don't stretch or recolour the logo.</p>
<div class="kit">
<figure><div class="kit-logo light"><img src="/assets/favicon.svg" alt="FIG logo, cobalt"></div><figcaption>Logo on light · <a href="/assets/favicon.svg" download>SVG</a></figcaption></figure>
<figure><div class="kit-logo dark"><svg class="logo" style="width:96px;height:96px"><use href="#logo"/></svg></div><figcaption>Logo on dark and cobalt (white letters, green leaf)</figcaption></figure>
<figure><div class="kit-logo"><img src="/assets/og.png" alt="FIG cover image"></div><figcaption>Cover image · <a href="/assets/og.png" download>PNG</a></figcaption></figure>
</div>
<h2>Colours</h2>
<div class="swatches"><span style="--c:#1E5EFF">Cobalt<br>#1E5EFF</span><span style="--c:#C8F135;color:#0A1020">Volt<br>#C8F135</span><span style="--c:#14C86B">Leaf<br>#14C86B</span><span style="--c:#0A1020">Midnight<br>#0A1020</span></div>
<h2>Fast facts</h2>
<ul><li><b>What:</b> a deals app for local restaurants. Diners find live deals on a map, claim one and show a code at the counter.</li>
<li><b>Where:</b> launching in Markham, Ontario, then Richmond Hill.</li>
<li><b>For restaurants:</b> one plan, $50 CAD a year. No commission, no fee per diner.</li>
<li><b>For diners:</b> free. Optional FIG Premium is $6.99/month, or earned free with stamps.</li>
<li><b>Company:</b> FIG Technologies Inc., Markham, Ontario.</li></ul>
<p>Press questions: <a href="/contact">contact us</a>.</p>''')

POSTS = [
    ("why-we-built-fig", "Why we built FIG", "October 4, 2026", "Markham has incredible independent restaurants. We wanted a way to find them that's fair to the owners too.", [
        "Markham is one of the best places in Canada to eat. Dim sum on Kennedy, ramen on Hwy 7, bubble tea on every corner. But the places that make it great are mostly small and independent, and they're competing for attention with apps that take a big cut of every order.",
        "Owners told us the same thing again and again: they have quiet hours they'd love to fill, but giving away a large share of each bill doesn't add up.",
        "So FIG works differently. A restaurant posts its own deal, for the hours it wants, with its own daily cap. Diners find it on a map, claim it, and show a code at the counter. The restaurant pays one plan, $50 a year, no matter how many diners walk in.",
        "We're starting in Markham because that's home. If you own a restaurant here, we'd love to set you up before launch.",
    ]),
    ("one-plan-50-a-year", "One plan, $50 a year: how FIG pricing works", "October 3, 2026", "No commission, no fee per diner, every location included. Here's what that means in practice.", [
        "Restaurants on FIG pay one plan: $50 CAD a year. It covers every location you run and every diner who walks in from FIG.",
        "There's no commission on the bill and no fee per scan. A diner who uses your deal pays you, at your counter, the way they always do.",
        "Inside the plan you get unlimited deals (everyday and flash), unlimited scans on any phone or tablet, takeout ordering if you want it, chats with diners, and a dashboard that shows what's working.",
        "You control the cost of your own deals: set the days and hours, add a daily cap, and pause anytime. Cancel the plan whenever you like and it runs to the end of the year you paid for.",
    ]),
    ("how-the-passport-works", "Your Passport: how stamps turn into free Premium", "October 2, 2026", "Every meal earns a stamp. Here's how to spend them.", [
        "Every time you use a deal on FIG, staff scan your code and a stamp lands in your Passport. Takeout pickups earn stamps too.",
        "Stamps are a balance you spend. 25 stamps buys a free week of FIG Premium, 50 buys three weeks and 100 buys a month. Claim a reward and keep collecting for the next one.",
        "Premium adds AI picks: tell FIG what you feel like and it picks your three best deals nearby, with a reason for each. Without Premium you get 3 picks a day.",
        "Your Passport also doubles as a food diary: every place you've tried, when, and what you saved.",
    ]),
]
blog = '<h1>Blog</h1><p class="lead-p">News and notes from the FIG team.</p><div class="posts">'
for slug, title, date, dek, paras in POSTS:
    blog += f'<a class="post-card" href="/blog/{slug}"><span>{date}</span><b>{e(title)}</b><p>{e(dek)}</p></a>'
    page(f"blog/{slug}", title, dek, f'<p class="doc-kicker"><a href="/blog">Blog</a> · {date}</p><h1>{e(title)}</h1><p class="lead-p">{e(dek)}</p>' + "".join(f"<p>{e(p)}</p>" for p in paras))
page("blog", "Blog", "News and notes from the FIG team.", blog + "</div>")


# =====================================================================  product pages
def hero(title, lead, ctas=True):
    btns = f'<div class="page-cta">{STORES.replace("badges small", "badges")}</div>' if ctas else ""
    return f'<section class="page-hero"><div class="wrap"><h1 class="display-2">{title}</h1><p class="lead-p">{lead}</p>{btns}</div></section>'


ARROW = '<svg width="56" height="40" viewBox="0 0 56 40" aria-hidden="true"><path d="M4 6c14-2 30 2 40 14 3 4 5 8 6 12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M42 27l8 7 3-10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def tutorial(role, steps, title):
    lis = "".join(f'<li><span class="n">{k + 1}</span><div><b>{e(h)}</b><p>{e(d)}</p></div></li>' for k, (h, d) in enumerate(steps))
    return f'''<section class="section" id="tutorial"><div class="wrap split">
  <div><h2 class="h2">{title}</h2><ol class="tsteps">{lis}</ol></div>
  <div class="tutwrap"><p class="tut-label"><span>Quick tutorial video</span>{ARROW}</p>
  <div class="tutvid"><video data-src="/assets/clips/tut-{role}.mp4" data-rate="1.35" poster="/assets/clips/tut-{role}.jpg" muted loop playsinline preload="none" disablepictureinpicture disableremoteplayback controlslist="nodownload nofullscreen noremoteplayback"></video></div></div>
</div></section>'''


STORE_BTNS = re.search(r'<div class="badges small">(.*)</div>', STORES, re.S).group(1)


def cta(title, text):
    return f'<section class="section"><div class="wrap"><div class="get-app"><div><h3>{title}</h3><p>{text}</p></div><div class="badges">{STORE_BTNS}</div></div></div></section>'


def faq(qs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qs) + "</div>"


DINER_STEPS = [("Download FIG and sign up", "Free for diners. Tell FIG what you crave, your budget and any diet needs once."),
               ("Find a deal near you", "Home and the map show live deals from restaurants around you, nearest first."),
               ("Claim it in one tap", "We hold it for 24 hours. Read the fine print, then tap Claim deal."),
               ("Show your code at the counter", "Staff scan it, or type the 8 characters under the QR. It changes every 5 minutes."),
               ("Earn a stamp", "Every visit adds a stamp to your Passport. Spend 25, 50 or 100 on free Premium."),
               ("Order takeout or ask a question", "Order ahead and pay at pickup, or message the restaurant from your deal.")]
OWNER_STEPS = [("Download FIG and sign up as a business", "Choose \"I own a restaurant\", add your name, your restaurant and your location."),
               ("Set up your page", "Add 3 photos, your address, cuisine and dietary options. This is what diners see."),
               ("Set your hours", "Diners see them on your page. Deals only show while you're open."),
               ("Start your plan", "One plan, $50 a year. Every location and every scan included. Your page goes live."),
               ("Post a deal", "Pick the type, the days and hours, who it's for and a daily cap. Pause it anytime."),
               ("Scan diners at the counter", "Any phone or tablet. Can't read the QR? Type the code. Add staff and their devices.")]
HELP_QS = {a: qs for a, _, qs in HELP}
OWNER_QA = HELP_QS["restaurants"]

page("how-it-works", "How it works", "Find a deal, claim it, show your code, earn a stamp. How FIG works for diners, step by step.", wide=True, group="Main", body=
     hero("How FIG works", "Find a live deal near you, claim it in one tap, show your code at the counter and earn a stamp. Free for diners.")
     + SECTION("how") + tutorial("diner", DINER_STEPS, "Watch it, start to finish.")
     + '''<section class="section"><div class="wrap"><div class="cards three">
  <a class="card-l" href="/passport"><b>The Passport</b><span>Every meal earns a stamp. Spend them on free Premium.</span><em>How stamps work</em></a>
  <a class="card-l" href="/features"><b>Takeout and chats</b><span>Order ahead, pay at pickup, and message restaurants before you go.</span><em>See every feature</em></a>
  <a class="card-l" href="/#owners"><b>What it costs</b><span>Nothing for diners. Premium is optional, or free with stamps.</span><em>See pricing</em></a>
</div></div></section>''' + cta("Ready when you are.", "FIG opens in Markham first. Download it and you'll be first in line."))

page("features", "Features", "Map, filters, flash deals, sharing, AI picks, the Passport, chats and takeout: everything in the FIG app.", wide=True, group="Main", body=
     hero("Everything in FIG", "Hover any box to see how it works. Every video is the real app.")
     + SECTION("features")
     + '''<section class="section"><div class="wrap"><h2 class="h2">And the small things that matter.</h2><div class="cards three">
  <div class="card-l"><b>Private by default</b><span>Restaurants never see your phone number, even for takeout. Chats go through the app.</span></div>
  <div class="card-l"><b>Codes that can't be copied</b><span>Your QR changes every 5 minutes, so a screenshot is useless to anyone else.</span></div>
  <div class="card-l"><b>Real reviews</b><span>Only diners whose visit was scanned can review, and paying never removes a review.</span></div>
  <div class="card-l"><b>Alerts you control</b><span>Flash deals near you, reminders before a claim ends, quiet hours at night. Turn any of them off.</span></div>
  <div class="card-l"><b>Dietary filters</b><span>Halal, vegetarian, vegan, gluten-free and more. Always confirm allergies with staff.</span></div>
  <div class="card-l"><b>Food history</b><span>Every place you've tried, when, and how much you saved.</span></div>
</div></div></section>''' + cta("See it for yourself.", "Free for diners. Launching in Markham."))

page("restaurants", "FIG for restaurants", "One plan, $50 a year. No commission, no fee per diner. Fill your quiet hours with local diners in Markham.", wide=True, group="Main", extra_head=faq_ld(OWNER_QA), body=
     hero("Fill your quiet hours with local diners.", "Post a deal for the hours you want. Diners find it on the map, claim it and show a code at your counter. One plan, $50 a year.")
     + SECTION("owners") + tutorial("restaurant", OWNER_STEPS, "Set up in minutes.")
     + f'<section class="section"><div class="wrap narrow"><h2 class="h2">Owners ask.</h2>{faq(OWNER_QA)}<p class="more-link">More in the <a href="/help#restaurants">help center</a>, or read the <a href="/business-terms">business terms</a>.</p></div></section>'
     + cta("Get your restaurant on FIG", "Download FIG and choose \"I own a restaurant\". Your page goes live as soon as you finish setup."))

page("passport", "The Passport", "Every meal on FIG earns a stamp. Spend 25, 50 or 100 stamps on free FIG Premium.", wide=True, group="Main", body=
     hero("Every meal earns a stamp.", "The Passport is your food diary on FIG. Every deal you use and every takeout pickup adds a stamp you can spend on free Premium.")
     + '''<section class="section tight"><div class="wrap split">
  <div><div class="plans two">
    <div class="plan"><p class="price"><b>25</b><span>stamps</span></p><p class="plan-d">1 free week of Premium</p></div>
    <div class="plan prem"><p class="price"><b>50</b><span>stamps</span></p><p class="plan-d">3 free weeks of Premium</p></div>
    <div class="plan"><p class="price"><b>100</b><span>stamps</span></p><p class="plan-d">1 free month of Premium</p></div>
    <div class="plan"><p class="price"><b>1st</b><span>stamp</span></p><p class="plan-d">3 days of Premium, straight away</p></div>
  </div>
  <h2 class="h2" style="margin-top:56px">How it works</h2>
  <ol class="tsteps"><li><span class="n">1</span><div><b>Use a deal</b><p>Staff scan your code at the counter, or your takeout pickup code.</p></div></li>
  <li><span class="n">2</span><div><b>A stamp lands in your Passport</b><p>With the place, the date and what you saved.</p></div></li>
  <li><span class="n">3</span><div><b>Spend stamps on Premium</b><p>Stamps are a balance. Claim a reward and keep collecting for the next one.</p></div></li></ol></div>
  <div class="phone big"><img src="/assets/screens/stamp.webp" alt="Stamp earned screen in the FIG app" width="390" height="844" loading="lazy"></div>
</div></section>''' + cta("Start your Passport.", "Your first stamp unlocks 3 days of Premium."))

# =====================================================================  404, site map, sitemap.xml, robots, manifest
page("404", "Page not found", "This page doesn't exist.", body='''<p class="doc-kicker">404</p><h1>This page wandered off.</h1>
<p class="lead-p">It may have moved, or the link has a typo.</p>
<div class="cards"><a class="card-l" href="/"><b>Home</b><span>Local deals, one tap away.</span></a><a class="card-l" href="/how-it-works"><b>How it works</b><span>Find, claim, show, save.</span></a>
<a class="card-l" href="/restaurants"><b>For restaurants</b><span>One plan, $50 a year.</span></a><a class="card-l" href="/help"><b>Help center</b><span>Answers to common questions.</span></a></div>''')

GROUP_OF = lambda p, g: "Blog" if p.startswith("/blog") else "Company" if p in ("/about", "/contact", "/press") else g
groups = {}
for p, t, g in PAGES + [("/sitemap", "Site map", "Company")]:
    groups.setdefault(GROUP_OF(p, g), []).append((p, t))
sm = '<h1>Site map</h1><p class="lead-p">Every page on this site.</p><div class="sitemap">' + "".join(
    f'<div><h2>{g}</h2>' + "".join(f'<a href="{p}">{e(t)}</a>' for p, t in items) + "</div>" for g, items in groups.items()) + "</div>"
page("sitemap", "Site map", "Every page on the FIG website.", sm, group="Company")

today = datetime.date.today().isoformat()
prio = lambda p: "1.0" if p == "/" else "0.9" if p in dict(NAV_LINKS) or p == "/passport" else "0.4" if p in ("/terms", "/privacy", "/business-terms", "/cookies") else "0.6"
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}{'' if p == '/' else p}</loc><lastmod>{today}</lastmod><priority>{prio(p)}</priority></url>\n" for p, _, _ in PAGES) + "</urlset>\n"
(SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
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
