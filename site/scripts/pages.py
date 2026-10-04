"""Builds the footer and the site's extra pages (legal, help, about, blog, press, contact, cookies).

run: python site/scripts/pages.py
- Legal pages come from legal.json (exported from the app's src/content/legal.ts, so they match the app word for word).
- The footer is written into index.html between <footer class="foot"> and </footer>, and used on every page.
"""
import html, json, pathlib, re

SITE = pathlib.Path(__file__).resolve().parents[1]
index = (SITE / "index.html").read_text(encoding="utf-8")
SPRITE = re.search(r'<svg width="0" height="0".*?</svg>', index, re.S).group(0)
NAV = re.search(r'<header class="nav".*?</header>', index, re.S).group(0)
NAV = re.sub(r'<a ([^>]*)href="#', r'<a \1href="/#', NAV)   # section links go back to the home page (the logo's <use href="#logo"> stays)
MEGA = re.search(r'<div class="mega".*?Save fast\.</span>\s*</div>', index, re.S).group(0)
STORES = re.search(r'<div class="badges small">.*?</div>', index, re.S).group(0)
e = html.escape

FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/"><svg class="logo"><use href="#logo"/></svg><span>FIG</span></a>
        <p>Live deals from local restaurants, on a map. Starting in Markham, Ontario. Richmond Hill next.</p>
        {STORES}
      </div>
      <div class="foot-cols">
        <div><h3>Diners</h3><a href="/#how">How it works</a><a href="/#tut">Diner tutorial</a><a href="/#passport">Passport</a><a href="/#chats">Chats</a><a href="/#features">Takeout</a><a href="/help">Help center</a></div>
        <div><h3>Restaurants</h3><a href="/owners">Get on FIG</a><a href="/#owners">Pricing</a><a href="/owners#tut">Restaurant tutorial</a><a href="/business-terms">Business terms</a><a href="/help#restaurants">Restaurant help</a></div>
        <div><h3>Company</h3><a href="/about">About</a><a href="/blog">Blog</a><a href="/press">Press kit</a><a href="/contact">Contact</a></div>
        <div><h3>Legal</h3><a href="/terms">Terms of service</a><a href="/privacy">Privacy policy</a><a href="/business-terms">Business terms</a><a href="/cookies">Cookies</a></div>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 FIG Technologies Inc. · Markham, Ontario · <a class="admin-link" href="/admin">Are you the admin?</a></span>
      <span>App screens show example restaurants and deals. Map data © OpenStreetMap contributors, OpenFreeMap. App Store is a trademark of Apple Inc. Google Play is a trademark of Google LLC.</span>
    </div>
  </div>
</footer>'''

index = re.sub(r'<footer class="foot">.*?</footer>', FOOTER, index, count=1, flags=re.S)
(SITE / "index.html").write_text(index, encoding="utf-8")


def page(slug, title, desc, body):
    out = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)} · FIG</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#0A0D14">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/css/site.css">
</head>
<body class="sub">
{SPRITE}
<div class="bg" aria-hidden="true"><div class="bg-grid"></div></div>
{NAV}
<main class="wrap doc">
{body}
</main>
{FOOTER}
{MEGA}
</body>
</html>
'''
    path = SITE / (slug + ".html")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")


def legal(slug, doc, extra=""):
    short = "".join(f"<li>{e(x)}</li>" for x in doc["short"])
    secs = "".join(f"<h2>{e(s['heading'])}</h2>" + "".join(f"<p>{e(p)}</p>" for p in s["paragraphs"]) for s in doc["sections"])
    body = f'''<p class="doc-kicker">{e(doc["updated"])}</p>
<h1>{e(doc["title"])}</h1>
<div class="doc-short"><h2>The short version</h2><ul>{short}</ul></div>
{secs}{extra}
<p class="doc-contact">{e(doc["contactAsk"])} <a href="mailto:{e(doc["email"])}">{e(doc["email"])}</a><br><span>{e(doc["contactLine"])}</span></p>'''
    page(slug, doc["title"], doc["short"][0], body)


L = json.loads((SITE / "scripts" / "legal.json").read_text(encoding="utf-8"))
legal("terms", L["terms"])
legal("business-terms", L["business-terms"])
legal("privacy", L["privacy"], '''<h2>The website waitlist</h2>
<p>When you join the waitlist on this website we keep your email or mobile number, whether you're a diner or a restaurant, the area you picked, when you joined and which link brought you here. We use it only to tell you when FIG opens near you and to send FIG news, because you ticked the consent box. Every email has an unsubscribe link and you can reply STOP to any text. We never sell it or share it with restaurants or advertisers.</p>''')

page("cookies", "Cookies", "What this website stores on your device.", '''<p class="doc-kicker">Last updated October 4, 2026</p>
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
help_html += '<p>Want to see it step by step? <a href="/#tut">Watch the tutorial</a>.</p>'
page("help", "Help center", "Answers for diners and restaurants using FIG.", help_html)

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
print("pages written")
