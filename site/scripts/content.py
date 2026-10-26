"""About page and blog posts. Plain facts, written so people, search engines and AI answer engines can quote them.

Each post: slug, screen (an app screenshot in assets/screens for the cover), title, ISO date, topic, dek (meta description), keywords, key points (the quotable summary),
sections [(h2, html)], faq [(q, a)]. Keep every number in line with the app: free for diners; restaurants are completely free, with no upfront payment and no price list (the owner 2026-10-24; no commission on the bill; FIG keeps 5% of the food on takeout orders diners pay for in the app, and Stripe's card fee comes off the same payment), FIG Premium, chat and announcements are HIDDEN for launch (the CEO 2026-10-17: don't mention them), no ads for now (user 2026-10-09),
a code works once and changes after every scan (not with time), claims last until the restaurant ends the deal, no loyalty points or rewards.
"""

ABOUT_FAQ = [
    ("What is FIG?", "FIG is a deals app for Markham, Ontario. Restaurants post their own deals, diners find them on a map, claim one in a tap and show a code at the counter."),
    ("Is FIG free?", "Yes, for diners and for restaurants, with no commission on the bill and no fee per diner. FIG earns only by keeping 5% of the food on takeout orders paid in the app."),
    ("Where is FIG available?", "FIG is launching in Markham, Ontario. Markham first, expanding to Richmond Hill and Vaughan Mills."),
    ("Who makes FIG?", "FIG is run by Brendan Lau in Markham, Ontario. You can reach FIG on the contact page."),
    ("Is FIG a delivery app?", "No. FIG brings diners to your restaurant. They eat in or, when a deal allows it, order takeout and pick it up. FIG never delivers, and diners never pay FIG."),
]

ABOUT = '''<section class="ab-glance"><div class="wrap ab-glance-in">
<h2 class="h2">FIG at a glance</h2>
<dl class="ab-dl">
<div><dt>What</dt><dd>A deals app for local restaurants. Restaurants can set up on the web today. Diners open on January 1, 2027. iPhone and Android apps are coming.</dd></div>
<div><dt>Where</dt><dd>Markham first, expanding to Richmond Hill and Vaughan Mills.</dd></div>
<div><dt>For diners</dt><dd>Free. Nothing to upgrade.</dd></div>
<div><dt>For restaurants</dt><dd>Free to start and free to run. FIG keeps 5% of the food only on takeout paid in the app.</dd></div>
<div><dt>Who</dt><dd>Run by Brendan Lau in Markham, Ontario.</dd></div>
</dl></div></section>

<section class="section ab-why"><div class="wrap ab-why-in">
<div class="ab-why-side"><h2 class="h2">Why FIG exists</h2><blockquote>“A full room at 7 pm, then a slow Tuesday afternoon.”</blockquote>
<img src="/assets/about/noodle-bar.webp" srcset="/assets/about/noodle-bar-560.webp 560w, /assets/about/noodle-bar.webp 1040w" sizes="(min-width: 980px) 560px, 100vw" alt="Stir-fried noodles on a wooden plate" width="1040" height="600" loading="lazy"></div>
<div class="ab-why-text">
<p>Markham is one of the best places in Canada to eat. Dim sum, ramen, Hakka, Hong Kong cafés, Korean fried chicken, Indian sweets, bubble tea on every plaza. Most of the places that make it great are small and independent.</p>
<p>Those owners share one problem: quiet hours. The usual answer is a delivery app, but delivery apps take a cut of every order, and many owners decided long ago that it doesn't add up.</p>
<p class="ab-strong">FIG works the other way around. You choose the deal, the days, the hours and how many a day. Diners walk in and pay you like normal. FIG takes no commission on deals or on the bill.</p>
<p>FIG is free for restaurants. We earn only from 5% of the food on takeout orders that diners pay for in the app.</p>
</div></div></section>

<section class="section ab-how"><div class="wrap ab-how-in">
<article class="ab-col ab-diners"><h2>For diners</h2><ol>
<li><b>Find</b><span>A live deal near you, on the home feed or the map. Filter by craving, budget and diet.</span></li>
<li><b>Claim</b><span>In one tap. It’s yours for as long as the deal runs.</span></li>
<li><b>Show</b><span>Your code at the counter. It works once, so a screenshot can't be reused.</span></li>
<li><b>Rate</b><span>The visit afterwards, so reviews on FIG come from real visits.</span></li>
</ol><p>Some deals also let you order takeout and pick it up. You can send a restaurant's link to friends: it opens the place's page with its live deals, so everyone sees the same thing.</p></article>
<article class="ab-col ab-owners"><h2>For restaurants</h2><ol>
<li><b>Build</b><span>Your page, menu and first deal as drafts: photos, hours, cuisine and dietary options.</span></li>
<li><b>Publish</b><span>Connect Stripe so it can check your identity, business and bank account (about 5 minutes). FIG never sees your ID.</span></li>
<li><b>Post</b><span>A deal for the hours you want to fill, with an optional daily cap. Pause it any time.</span></li>
<li><b>Scan</b><span>Staff scan each diner's code with any phone or tablet. No fee per scan.</span></li>
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
