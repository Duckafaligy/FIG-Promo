"""About page and blog posts. Plain facts, written so people, search engines and AI answer engines can quote them.

Each post: slug, screen (an app screenshot in assets/screens for the cover), title, ISO date, topic, dek (meta description), keywords, key points (the quotable summary),
sections [(h2, html)], faq [(q, a)]. Keep every number in line with the app: free for diners and restaurants (no fees, no commission), ads pay per tap (from $0.30, daily budget,
invoiced monthly), no AI features, codes refresh every 5 minutes, claims last until the restaurant ends the deal, no loyalty points or rewards.
"""

ABOUT_FAQ = [
    ("What is FIG?", "FIG is a restaurant deals app for Markham, Ontario. Restaurants post their own deals, diners find them on a map, claim one in a tap and show a code at the counter to save."),
    ("Is FIG free?", "Yes, for diners and restaurants. FIG makes money only from restaurants' ads, which cost only when a diner taps and are always labelled Sponsored. There's no commission and no fee per diner."),
    ("Where is FIG available?", "FIG is launching in Markham, Ontario first, then Richmond Hill, then the rest of York Region and the Greater Toronto Area."),
    ("Who makes FIG?", "FIG Technologies Inc., a small team based in Markham, Ontario."),
    ("Is FIG a delivery app?", "No. FIG brings diners into the restaurant. You eat in, or order takeout ahead and pick it up. You pay the restaurant directly, and FIG never takes a cut of the bill."),
]

ABOUT = '''<p class="doc-kicker">About FIG</p>
<h1>FIG is the restaurant deals app for Markham.</h1>
<p class="lead-p">Live deals from local restaurants, on a map. Diners claim a deal in one tap and show a code at the counter. Restaurants join free, post deals free and keep every dollar of every bill.</p>

<div class="doc-short"><h2>FIG at a glance</h2><ul>
<li><b>What:</b> a mobile app (iPhone and Android) for finding and using deals at local restaurants.</li>
<li><b>Where:</b> launching in Markham, Ontario. Richmond Hill next, then the rest of York Region and the GTA.</li>
<li><b>For diners:</b> free. Nothing to upgrade.</li>
<li><b>For restaurants:</b> free. No commission, no fees. Optional ads, paid per tap.</li>
<li><b>Company:</b> FIG Technologies Inc., Markham, Ontario.</li>
</ul></div>

<h2>Why FIG exists</h2>
<p>Markham is one of the best places in Canada to eat. Dim sum, ramen, Hakka, Hong Kong cafés, Korean fried chicken, Indian sweets, bubble tea on every plaza. Most of the places that make it great are small and independent.</p>
<p>Those owners all have the same problem: quiet hours. A full room at 7 pm, then a slow Tuesday afternoon. The usual answer is a delivery app, but delivery platforms take a percentage of every order, and a lot of owners decided long ago it doesn't add up.</p>
<p>FIG is built the other way around. The restaurant decides the deal, the days, the hours and how many a day. Diners walk in and pay the restaurant like normal. FIG charges the restaurant nothing for any of it. We make money only when a restaurant wants to be seen first and runs an ad, paying per tap.</p>

<h2>How FIG works for diners</h2>
<ol>
<li><b>Find</b> a live deal near you on the home feed or the map. Filter by craving, budget and diet (halal, vegetarian, vegan, gluten-free and more).</li>
<li><b>Claim</b> it in one tap. It’s yours for as long as the deal runs.</li>
<li><b>Show</b> your code at the counter. It refreshes every 5 minutes, so a screenshot can't be reused.</li>
<li><b>Rate</b> the visit afterwards, so reviews on FIG come from real visits.</li>
</ol>
<p>You can also order takeout ahead and pay at pickup, message a restaurant before you go, and share a deal with your group chat so everyone can agree on where to eat.</p>

<h2>How FIG works for restaurants</h2>
<ol>
<li><b>Set up</b> your page: photos, address, hours, cuisine and dietary options.</li>
<li><b>Go live</b> for free.</li>
<li><b>Post</b> a deal for the hours you want to fill, with an optional daily cap. Pause it anytime.</li>
<li><b>Scan</b> diners at the counter with any phone or tablet. Every scan is free.</li>
<li><b>Advertise</b> when you want more diners: an ad in the <a href=\"/ads\">Ads Manager</a>, paid per tap. Optional.</li>
</ol>
<p>The dashboard shows scans, new diners and which deals work, so you can keep what fills seats and drop what doesn't.</p>

<h2>What makes FIG different</h2>
<ul>
<li><b>No commission, no fees.</b> Diners pay you, at your counter. FIG is paid only by optional, clearly labelled ads.</li>
<li><b>Honest deals.</b> Every deal, timer and opening hour is set by the restaurant itself.</li>
<li><b>Codes that can't be copied.</b> Rotating QR codes stop screenshots and resold deals.</li>
<li><b>Private by default.</b> Restaurants never see a diner's phone number, even for takeout. Chats go through the app.</li>
<li><b>Real reviews.</b> Only diners whose visit was scanned can review, and an ad never changes or removes a review.</li>
</ul>

<h2>Local first</h2>
<p>We're starting with the neighbourhoods we know: Unionville, Markham Village, Cornell, Milliken, Cathedraltown and the Highway 7 corridor. Once Markham is running well, Richmond Hill is next, then Vaughan, Toronto and the rest of the GTA.</p>

<h2>Questions people ask about FIG</h2>
{faq}

<h2>Get in touch</h2>
<p>Restaurant owners: <a href="/#owners">see how pricing works</a>. Diners: <a href="/#how">see how it works</a>. Everyone else: <a href="/contact">say hello</a>, or read the <a href="/blog">blog</a>.</p>'''

POSTS = [
    dict(slug="why-we-built-fig", screen="map", title="Why we built FIG", date="2026-10-02", topic="News",
         dek="Markham has incredible independent restaurants. We wanted a way to find them that's fair to the owners too.",
         keywords="FIG app, Markham restaurants, independent restaurants, restaurant deals app",
         points=["FIG is a restaurant deals app starting in Markham, Ontario.",
                 "Restaurants post their own deals for free, with no commission and no fees.",
                 "Diners find deals on a map, claim one and show a code at the counter. It's free for diners."],
         sections=[
             ("Markham deserves better than a cut of every bill", "<p>Markham is one of the best places in Canada to eat. Dim sum on Kennedy, ramen on Highway 7, Hong Kong cafés in every plaza, bubble tea on every corner. But the places that make it great are mostly small and independent, and they compete for attention with apps that take a percentage of every order.</p><p>Owners told us the same thing again and again: they have quiet hours they'd love to fill, but giving away a large share of each bill doesn't add up.</p>"),
             ("So we flipped the model", "<p>On FIG, a restaurant posts its own deal, for the hours it wants, with its own daily cap. Diners find it on a map, claim it, and show a code at the counter. The diner pays the restaurant directly, and FIG takes nothing from the bill. Restaurants that want to be seen first can sponsor a spot for a week; that's how FIG is paid.</p><p>That means a deal on FIG is a decision the owner made, not a discount a platform forced on them. It also means the deals are real: the timer on a flash deal is the owner's timer.</p>"),
             ("Why Markham first", "<p>Because it's home, and because it has exactly the mix FIG is built for: hundreds of independent restaurants, busy plazas, and a lot of people who love finding a new place to eat. Richmond Hill is next.</p><p>If you own a restaurant in Markham, we'd love to set you up before launch. <a href=\"/#owners\">See how pricing works</a>.</p>"),
         ],
         faq=[("When does FIG launch?", "FIG is launching in Markham first. Download the app or join the waitlist on the home page to hear the moment it opens near you."),
              ("Does FIG take a commission?", "No. FIG is free for restaurants and never takes a percentage of the bill. Restaurants can choose to run ads, paid per tap.")]),

    dict(slug="how-fig-makes-money", screen="tdash", title="FIG is free for restaurants. Here's how we make money", date="2026-10-07", topic="For restaurants",
         dek="Listing, deals, scans, takeout and chats are free on FIG, with no commission. FIG is paid only by restaurants' ads, and only when a diner taps.",
         keywords="FIG pricing, free restaurant app, no commission restaurant app, restaurant advertising Markham, pay per click restaurant ads",
         points=["FIG is free for restaurants: listing, unlimited deals, every scan, takeout and chats. No commission, no fees.",
                 "FIG makes money from ads: a restaurant sets a daily budget and pays only when a diner taps, from about $0.30 a tap.",
                 "Ads run from the Ads Manager on the FIG website, are always labelled Sponsored, and show which diners actually came in."],
         sections=[
             ("What's free", "<p>Everything you need to bring diners in: your page, unlimited everyday and flash deals, scanning diners at the counter on any phone or tablet, takeout ordering, chats with diners and a dashboard of what's working. No commission on the bill, no fee per diner, no monthly fee.</p><p>A diner who uses your deal pays you, at your counter, the way they always do.</p>"),
             ("How FIG makes money", "<p>When you want more diners, you can run an ad from the <a href=\"/ads\">Ads Manager</a>. Pick a goal (more diners, promote a deal, or fill quiet hours), who should see it (distance, days and hours, the foods they crave, new or returning diners) and a daily budget. You pay only when a diner taps your ad.</p><p>Like Facebook ads, each sponsored spot goes to a quick auction: ads with a fair bid, photos diners tap and good ratings win, and the winner pays just enough to beat the next ad, never more than its budget. Every paid spot is labelled Sponsored.</p>"),
             ("You see what you get", "<p>Every ad shows its views, taps and the diners who came in within a week of tapping, day by day. Add up to three photos and FIG shows the one diners tap most. Before you spend a dollar, Insights shows when diners near you claim deals, what they crave, and how many places nearby advertise.</p>"),
             ("What an ad never does", "<ul><li>Change your deal or its price</li><li>Hide, remove or reorder reviews</li><li>Share any diner's details with you</li></ul><p>Read the full <a href=\"/business-terms\">business terms</a>.</p>"),
         ],
         faq=[("How much does FIG cost a restaurant?", "Nothing, unless you run ads. Ads cost only when a diner taps, from about $0.30 a tap, within a daily budget you set, invoiced monthly."),
              ("Is there a contract?", "No. Pause or end an ad anytime. You're invoiced only for taps.")]),

    dict(slug="restaurant-deals-markham", screen="map", title="How to find the best restaurant deals in Markham", date="2026-10-04", topic="For diners",
         dek="A practical guide to eating out for less in Markham, Ontario: when to go, where to look and how to use FIG.",
         keywords="restaurant deals Markham, Markham food deals, cheap eats Markham, Markham restaurants, Unionville restaurants",
         points=["The best restaurant deals in Markham are usually in off-peak hours: weekday afternoons and early evenings.",
                 "FIG shows live deals from Markham restaurants on a map, nearest first, filtered by craving, budget and diet.",
                 "Claim a deal in one tap, show the code at the counter and pay the restaurant as usual."],
         sections=[
             ("Go when restaurants are quiet", "<p>Restaurants are busiest at lunch and dinner on weekends. The rest of the week they have empty tables, and that's when owners are most willing to offer a deal. Think weekday afternoons from 2 to 5 pm, early dinners, and late-night snacks.</p>"),
             ("Know the food streets", "<p>Markham's restaurants cluster in plazas. The Highway 7 corridor, Kennedy Road, Warden Avenue, Main Street Unionville and Markham Village each have dozens of places within a few minutes of each other, which makes it easy to try somewhere new when a deal pops up nearby.</p>"),
             ("Let the app do the searching", "<p>Instead of checking ten Instagram accounts, open FIG. Home and the map show every live deal around you, nearest first. Tell FIG your cravings, budget and any dietary needs once (halal, vegetarian, vegan, gluten-free and more) and the list becomes the places that actually fit you.</p>"),
             ("Watch for flash deals", "<p>Flash deals are short deals a restaurant posts when it has a quiet hour. Turn on flash alerts and FIG tells you when one drops near you. The timer is real, set by the restaurant. <a href=\"/blog/flash-deals-explained\">How flash deals work</a>.</p>"),
             ("Rate where you went", "<p>After a visit, rate it in a tap. Only diners whose visit was scanned can review on FIG, so the ratings you read come from real meals.</p>"),
         ],
         faq=[("What's the best app for restaurant deals in Markham?", "FIG is built specifically for Markham restaurant deals: live deals on a map, set by the restaurants themselves, free for diners."),
              ("Do I pay through the app?", "No. You pay the restaurant at the counter, like normal. FIG never handles payment for food.")]),

    dict(slug="delivery-app-commissions-vs-fig", screen="tscanner", title="Delivery app commissions vs FIG: what restaurants keep", date="2026-10-04", topic="For restaurants",
         dek="Delivery apps charge restaurants a percentage of every order. FIG charges nothing per diner. Here's how the two compare for a Markham restaurant.",
         keywords="delivery app commission, UberEats commission, DoorDash commission, restaurant commission fees Ontario, commission-free restaurant app",
         points=["Delivery platforms commonly charge restaurants a commission on every order, often reported in the 15% to 30% range depending on the plan.",
                 "FIG charges no commission and no fee per diner: diners come to the restaurant and pay it directly.",
                 "FIG isn't a delivery replacement: it fills dine-in and pickup during the hours a restaurant chooses."],
         sections=[
             ("How commission pricing works", "<p>Delivery platforms usually charge the restaurant a percentage of each order, plus sometimes marketing or promotion fees. The exact rate depends on the plan, but commissions in the 15% to 30% range are commonly reported. The more a restaurant sells through the app, the more it pays.</p>"),
             ("A simple example", "<p>Take a $40 dinner order. At a 25% commission, the platform keeps $10 of it. Ten orders like that a week is $100 a week, or about $5,200 a year, in commission alone.</p><p>On FIG, those ten diners cost the restaurant nothing. They show a code and pay the restaurant directly. The only cost is the deal the owner chose to offer, and optional ads (paid per tap) if the owner wants to be seen first.</p>"),
             ("Different jobs", "<p>Delivery apps are good at getting food to someone's door. FIG does a different job: it brings people into the restaurant, or to the counter for takeout pickup, during the hours the owner wants to fill. Many restaurants will use both.</p>"),
             ("What you control on FIG", "<ul><li>The deal itself: what, when and for whom</li><li>A daily cap, so a deal never gives away more than you planned</li><li>Pausing anytime, with one tap</li><li>Whether to advertise at all</li></ul><p><a href=\"/blog/how-fig-makes-money\">How FIG makes money</a>.</p>"),
         ],
         faq=[("Does FIG charge a commission?", "No. FIG is free for restaurants, with no commission and no fee per diner. Ads are optional and paid per tap."),
              ("Does FIG do delivery?", "No. Diners eat in or order takeout ahead and pick it up, paying the restaurant at the counter.")]),

    dict(slug="fill-slow-hours-restaurant", screen="tdash", title="7 ways to fill slow hours at your restaurant", date="2026-10-04", topic="For restaurants",
         dek="Practical ideas for independent restaurants to bring in diners on quiet afternoons and weeknights, without giving away margin.",
         keywords="fill slow hours restaurant, restaurant marketing ideas, slow restaurant days, increase restaurant traffic, Markham restaurant marketing",
         points=["Target the exact hours that are slow, not the whole day.",
                 "Cap how many deals you give away so a promotion never costs more than planned.",
                 "Measure what brings new diners in, keep it, and drop what doesn't."],
         sections=[
             ("1. Find your real quiet hours", "<p>Look at a few weeks of receipts and mark the hours with empty tables. For most places it's weekday afternoons and early weeknights. That's where a deal does the most good.</p>"),
             ("2. Make the deal specific", "<p>\"2-for-1 dim sum, Monday to Thursday, 2 to 5 pm\" works better than \"10% off\". A clear, specific deal is easy to share and easy for staff to honour.</p>"),
             ("3. Cap it", "<p>Set a daily limit. On FIG, a daily cap stops a deal automatically once it's been used that many times.</p>"),
             ("4. Go where people are deciding", "<p>Most people decide where to eat on their phone, often in a group chat. Being on a map of nearby deals at the moment they're deciding matters more than a poster in the window.</p>"),
             ("5. Use flash deals for surprise quiet spells", "<p>Rain, a cancelled booking, a slow lunch. A short flash deal tells nearby diners right now. <a href=\"/blog/flash-deals-explained\">How flash deals work</a>.</p>"),
             ("6. Offer pickup", "<p>Takeout ordered ahead and picked up at the counter fills the kitchen without filling tables, and without delivery fees.</p>"),
             ("7. Measure and repeat", "<p>Track scans and new diners per deal. Keep the deals that bring new people in and pause the rest. FIG's dashboard shows this for every deal.</p>"),
         ],
         faq=[("What's the cheapest way to market a small restaurant?", "Target your slow hours with a specific, capped deal where diners are already looking. FIG does this for free."),
              ("Will a deal hurt my margins?", "Not if you cap it and only run it in hours that would otherwise be empty.")]),

    dict(slug="student-food-deals-markham", screen="claim", title="Student food deals in Markham: eating out on a budget", date="2026-10-04", topic="For diners",
         dek="How high school and university students in Markham can eat out for less: after-school deals, group plans and budget filters.",
         keywords="student food deals Markham, cheap eats for students, after school food Markham, budget restaurants Markham, bubble tea deals Markham",
         points=["After-school hours are exactly when many restaurants are quiet, so that's when deals show up.",
                 "Set a budget filter in FIG once and only see deals you can afford.",
                 "Share a deal to your group chat so everyone can agree on where to go."],
         sections=[
             ("After school is deal time", "<p>Between 3 and 6 pm, a lot of Markham restaurants and bubble tea shops are quiet. That's when owners post deals, and when you're most likely to be hungry.</p>"),
             ("Set your budget once", "<p>When you sign up, tell FIG your budget and what you crave. The home feed and map then show deals that fit, nearest first, so you're not scrolling past $40 dinners.</p>"),
             ("Decide with your friends", "<p>Can't agree where to eat? Share a deal from FIG straight to your group chat. Everyone sees the same place, the same deal and how far it is.</p>"),
             ("Free is better", "<p>FIG is free for diners. Nothing to collect, nothing to upgrade: just deals.</p>"),
             ("Ask before you go", "<p>Not sure if there's space for six, or if the deal works for takeout? Message the restaurant from the deal. Your phone number stays private.</p>"),
         ],
         faq=[("Is FIG free for students?", "Yes. FIG is free for every diner, with nothing to upgrade."),
              ("Do I need a credit card?", "No. You claim deals in the app and pay the restaurant directly at the counter.")]),

    dict(slug="flash-deals-explained", screen="qr", title="What are flash deals, and how do they work on FIG?", date="2026-10-04", topic="For diners",
         dek="Flash deals are short, real-time restaurant deals posted during quiet hours. Here's how to catch them in Markham.",
         keywords="flash deals restaurants, last minute restaurant deals, happy hour Markham, real time food deals",
         points=["A flash deal is a short deal a restaurant posts right now, for a quiet hour.",
                 "The timer is set by the restaurant and it's real: when it ends, the deal is gone.",
                 "Turn on flash alerts to hear about the ones near you."],
         sections=[
             ("What a flash deal is", "<p>Everyday deals run on a schedule, like every weekday afternoon. A flash deal is different: a restaurant posts it on the spot, because it has empty tables right now. It usually lasts an hour or two.</p>"),
             ("How to catch one", "<p>Turn on flash alerts in FIG and you'll get a notification when a flash deal drops near you. Flash deals also show at the top of your home feed and glow on the map.</p>"),
             ("Claim it, then go", "<p>Claim the flash deal in one tap and head over. Show your code at the counter. Like every FIG code, it refreshes every 5 minutes so it can't be screenshotted and reused.</p>"),
             ("For restaurant owners", "<p>Posting a flash deal takes a few seconds: pick the deal, the length and an optional cap. It's free, like every scan. <a href=\"/#owners\">How FIG works for restaurants</a>.</p>"),
         ],
         faq=[("How long do flash deals last?", "The restaurant sets the length, usually an hour or two. The timer you see in the app is the real one."),
              ("Can I turn flash alerts off?", "Yes. Every alert in FIG can be turned off, and quiet hours at night are on by default.")]),

    dict(slug="takeout-without-delivery-fees", screen="chat", title="Order ahead, pick up, skip the delivery fees", date="2026-10-04", topic="For diners",
         dek="FIG takeout lets you order from a Markham restaurant's menu, watch it get made and pay at pickup, with no delivery or service fees.",
         keywords="takeout without delivery fees, order ahead pickup Markham, takeout deals Markham, pickup orders",
         points=["Order from the restaurant's menu in FIG and pay at the counter when you pick up.",
                 "No delivery fee and no service fee from FIG.",
                 "Deals apply to takeout unless the restaurant marks a deal dine-in only."],
         sections=[
             ("How it works", "<p>Open a restaurant in FIG, tap the menu and build your order. The restaurant accepts it and you can watch its status: new, cooking, ready. Head over, show your pickup code, pay at the counter and go.</p>"),
             ("Why pickup is cheaper", "<p>There's no driver, so there's no delivery fee, and FIG doesn't add a service fee. You pay the menu price, minus any deal, straight to the restaurant.</p>"),
             ("Deals still count", "<p>Deals work on takeout unless the restaurant says dine-in only.</p>"),
             ("Private by default", "<p>The restaurant never sees your phone number. If you need to change something, message them from the order in the app.</p>"),
         ],
         faq=[("Does FIG deliver?", "No. FIG takeout is order-ahead pickup. You collect the food and pay the restaurant at the counter."),
              ("Is there a fee for ordering takeout on FIG?", "No. FIG doesn't charge diners delivery or service fees.")]),
]
