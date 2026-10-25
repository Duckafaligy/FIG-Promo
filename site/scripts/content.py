"""About page and blog posts. Plain facts, written so people, search engines and AI answer engines can quote them.

Each post: slug, screen (an app screenshot in assets/screens for the cover), title, ISO date, topic, dek (meta description), keywords, key points (the quotable summary),
sections [(h2, html)], faq [(q, a)]. Keep every number in line with the app: free for diners; restaurants are completely free, with no upfront payment and no price list (the owner 2026-10-24; no commission on the bill; FIG keeps 5% of the food on takeout orders diners pay for in the app, and Stripe's card fee comes off the same payment), FIG Premium, chat and announcements are HIDDEN for launch (the CEO 2026-10-17: don't mention them), no ads for now (user 2026-10-09),
a code works once and changes after every scan (not with time), claims last until the restaurant ends the deal, no loyalty points or rewards.
"""

ABOUT_FAQ = [
    ("What is FIG?", "FIG is a restaurant deals app for Markham, Ontario. Restaurants post their own deals, diners find them on a map, claim one in a tap and show a code at the counter to save."),
    ("Is FIG free?", "Yes for diners, always. Restaurants are free too, with no commission on the bill and no fee per diner. FIG earns only by keeping 5% of the food on takeout orders diners pay for in the app."),
    ("Where is FIG available?", "FIG is launching in Markham, Ontario. Markham first, expanding to Richmond Hill and Vaughan Mills."),
    ("Who makes FIG?", "A small team based in Markham, Ontario."),
    ("Is FIG a delivery app?", "No. FIG brings diners into the restaurant. It’s a live-deals app: you eat in, or, when a deal allows it, takeout and pick up. You never pay FIG anything."),
]

ABOUT = '''<section class="ab-glance"><div class="wrap ab-glance-in">
<h2 class="h2">FIG at a glance</h2>
<dl class="ab-dl">
<div><dt>What</dt><dd>An app for finding and using deals at local restaurants. Restaurants can set up on the web today; FIG opens to diners on January 1, 2027. iPhone and Android apps are coming soon.</dd></div>
<div><dt>Where</dt><dd>Markham first, expanding to Richmond Hill and Vaughan Mills.</dd></div>
<div><dt>For diners</dt><dd>Free. Nothing to upgrade.</dd></div>
<div><dt>For restaurants</dt><dd>Free: deals and scans, with no commission on the bill. FIG keeps 5% of the food only on takeout orders paid in the app.</dd></div>
<div><dt>Who</dt><dd>A small team in Markham, Ontario.</dd></div>
</dl></div></section>

<section class="section ab-why"><div class="wrap ab-why-in">
<div class="ab-why-side"><h2 class="h2">Why FIG exists</h2><blockquote>“A full room at 7 pm, then a slow Tuesday afternoon.”</blockquote>
<div class="ab-tile-wide" aria-hidden="true"><svg class="logo"><use href="#logo"/></svg></div></div>
<div class="ab-why-text">
<p>Markham is one of the best places in Canada to eat. Dim sum, ramen, Hakka, Hong Kong cafés, Korean fried chicken, Indian sweets, bubble tea on every plaza. Most of the places that make it great are small and independent.</p>
<p>Those owners all have the same problem: quiet hours. The usual answer is a delivery app, but delivery platforms take a percentage of every order, and a lot of owners decided long ago it doesn't add up.</p>
<p class="ab-strong">FIG is built the other way around. The restaurant decides the deal, the days, the hours and how many a day. Diners walk in and pay the restaurant like normal. FIG takes no commission on deals or on the bill.</p>
<p>Restaurants use FIG for free. We make money only from 5% of the food on takeout orders diners pay for in the app.</p>
</div></div></section>

<section class="section ab-how"><div class="wrap ab-how-in">
<article class="ab-col ab-diners"><h2>For diners</h2><ol>
<li><b>Find</b><span>A live deal near you on the home feed or the map. Filter by craving, budget and diet (halal, vegetarian, vegan, gluten-free and more).</span></li>
<li><b>Claim</b><span>In one tap. It’s yours for as long as the deal runs.</span></li>
<li><b>Show</b><span>Your code at the counter. It works once, so a screenshot can't be reused.</span></li>
<li><b>Rate</b><span>The visit afterwards, so reviews on FIG come from real visits.</span></li>
</ol><p>Some deals also let you order takeout and pick up. You can send a restaurant's link to your group chat: it opens the place's page on FIG with its live deals, so everyone agrees on where to eat.</p></article>
<article class="ab-col ab-owners"><h2>For restaurants</h2><ol>
<li><b>Set up</b><span>Your page: photos, address, hours, cuisine and dietary options.</span></li>
<li><b>Publish</b><span>After Stripe's quick identity and bank checks (about 5 minutes).</span></li>
<li><b>Post</b><span>A deal for the hours you want to fill, with an optional daily cap. Pause it anytime.</span></li>
<li><b>Scan</b><span>Diners at the counter with any phone or tablet. No fee per scan.</span></li>
</ol><p>The dashboard shows scans, new diners and which deals work, so you can keep what fills seats and drop what doesn't.</p></article>
</div></section>

<section class="section ab-diff"><div class="wrap">
<h2 class="h2">What makes FIG different.</h2>
<ul class="ab-diff-grid">
<li><b>No commission on the bill.</b><span>Diners pay you, at your counter. FIG is paid only from 5% of the food on takeout orders diners pay for in the app.</span></li>
<li><b>Honest deals.</b><span>Every deal, timer and opening hour is set by the restaurant itself.</span></li>
<li><b>Codes that can't be copied.</b><span>One-time QR codes stop screenshots and resold deals.</span></li>
<li><b>Private by default.</b><span>Restaurants never see a diner's phone number, even for a takeout order.</span></li>
<li><b>Real reviews.</b><span>Only diners whose visit was scanned can review, and paying FIG never changes or removes a review.</span></li>
<li><b>Local first.</b><span>Unionville, Markham Village, Cornell, Milliken, Cathedraltown and the Highway 7 corridor first. Then expanding to Richmond Hill and Vaughan Mills.</span></li>
</ul></div></section>

<section class="section ab-faq"><div class="wrap faq">
<div class="faq-head"><h2 class="h2">Questions people ask about FIG</h2><p class="side">Restaurant owners: <a href="/#owners">see why FIG is free for restaurants</a>. Everyone else: <a href="/contact">say hello</a>, or read the <a href="/blog">blog</a>.</p></div>
{faq}
</div></section>'''

# the blog's words live in posts.py (28, content lead, 2026-10-14)
from posts import POSTS  # noqa: E402,F401
