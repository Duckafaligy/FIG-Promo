"""About page and blog posts. Plain facts, written so people, search engines and AI answer engines can quote them.

Each post: slug, title, ISO date, topic, dek (meta description), keywords, key points (the quotable summary),
sections [(h2, html)], faq [(q, a)]. Keep every number in line with the app: $50/year plan, Premium $6.99/month,
codes refresh every 5 minutes, claims held 24 hours, stamps 25/50/100.
"""

ABOUT_FAQ = [
    ("What is FIG?", "FIG is a restaurant deals app for Markham, Ontario. Restaurants post their own deals, diners find them on a map, claim one in a tap and show a code at the counter to save."),
    ("Is FIG free?", "Yes, for diners. Restaurants pay one plan of $50 CAD a year, with no commission and no fee per diner. FIG Premium for diners ($6.99 a month) is optional and can be earned free with stamps."),
    ("Where is FIG available?", "FIG is launching in Markham, Ontario first, then Richmond Hill, then the rest of York Region and the Greater Toronto Area."),
    ("Who makes FIG?", "FIG Technologies Inc., a small team based in Markham, Ontario."),
    ("Is FIG a delivery app?", "No. FIG brings diners into the restaurant. You eat in, or order takeout ahead and pick it up. You pay the restaurant directly, and FIG never takes a cut of the bill."),
]

ABOUT = '''<p class="doc-kicker">About FIG</p>
<h1>FIG is the restaurant deals app for Markham.</h1>
<p class="lead-p">Live deals from local restaurants, on a map. Diners claim a deal in one tap and show a code at the counter. Restaurants pay one flat plan, $50 a year, and keep every dollar of every bill.</p>

<div class="doc-short"><h2>FIG at a glance</h2><ul>
<li><b>What:</b> a mobile app (iPhone and Android) for finding and using deals at local restaurants.</li>
<li><b>Where:</b> launching in Markham, Ontario. Richmond Hill next, then the rest of York Region and the GTA.</li>
<li><b>For diners:</b> free. Optional FIG Premium is $6.99 a month, or free with Passport stamps.</li>
<li><b>For restaurants:</b> one plan, $50 CAD a year. No commission, no fee per diner, every scan included.</li>
<li><b>Company:</b> FIG Technologies Inc., Markham, Ontario.</li>
</ul></div>

<h2>Why FIG exists</h2>
<p>Markham is one of the best places in Canada to eat. Dim sum, ramen, Hakka, Hong Kong cafés, Korean fried chicken, Indian sweets, bubble tea on every plaza. Most of the places that make it great are small and independent.</p>
<p>Those owners all have the same problem: quiet hours. A full room at 7 pm, then a slow Tuesday afternoon. The usual answer is a delivery app, but delivery platforms take a percentage of every order, and a lot of owners decided long ago it doesn't add up.</p>
<p>FIG is built the other way around. The restaurant decides the deal, the days, the hours and how many a day. Diners walk in and pay the restaurant like normal. The restaurant pays FIG one flat plan for the year, whether one diner shows up or a thousand.</p>

<h2>How FIG works for diners</h2>
<ol>
<li><b>Find</b> a live deal near you on the home feed or the map. Filter by craving, budget and diet (halal, vegetarian, vegan, gluten-free and more).</li>
<li><b>Claim</b> it in one tap. We hold it for 24 hours.</li>
<li><b>Show</b> your code at the counter. It refreshes every 5 minutes, so a screenshot can't be reused.</li>
<li><b>Earn</b> a stamp in your Passport. Spend 25, 50 or 100 stamps on free FIG Premium.</li>
</ol>
<p>You can also order takeout ahead and pay at pickup, message a restaurant before you go, and share a deal with your group chat so everyone can agree on where to eat.</p>

<h2>How FIG works for restaurants</h2>
<ol>
<li><b>Set up</b> your page: photos, address, hours, cuisine and dietary options.</li>
<li><b>Start</b> the $50 a year plan. Your page goes live.</li>
<li><b>Post</b> a deal for the hours you want to fill, with an optional daily cap. Pause it anytime.</li>
<li><b>Scan</b> diners at the counter with any phone or tablet. Every scan is included.</li>
</ol>
<p>The dashboard shows scans, new diners and which deals work, so you can keep what fills seats and drop what doesn't.</p>

<h2>What makes FIG different</h2>
<ul>
<li><b>No commission.</b> One flat plan. A diner who uses your deal pays you, at your counter.</li>
<li><b>Honest deals.</b> Every deal, timer and opening hour is set by the restaurant itself.</li>
<li><b>Codes that can't be copied.</b> Rotating QR codes stop screenshots and resold deals.</li>
<li><b>Private by default.</b> Restaurants never see a diner's phone number, even for takeout. Chats go through the app.</li>
<li><b>Real reviews.</b> Only diners whose visit was scanned can review, and paying never removes a review.</li>
</ul>

<h2>Local first</h2>
<p>We're starting with the neighbourhoods we know: Unionville, Markham Village, Cornell, Milliken, Cathedraltown and the Highway 7 corridor. Once Markham is running well, Richmond Hill is next, then Vaughan, Toronto and the rest of the GTA.</p>

<h2>Questions people ask about FIG</h2>
{faq}

<h2>Get in touch</h2>
<p>Restaurant owners: <a href="/#owners">see the $50 a year plan</a>. Diners: <a href="/#how">see how it works</a>. Everyone else: <a href="/contact">say hello</a>, or read the <a href="/blog">blog</a>.</p>'''

POSTS = [
    dict(slug="why-we-built-fig", title="Why we built FIG", date="2026-10-02", topic="News",
         dek="Markham has incredible independent restaurants. We wanted a way to find them that's fair to the owners too.",
         keywords="FIG app, Markham restaurants, independent restaurants, restaurant deals app",
         points=["FIG is a restaurant deals app starting in Markham, Ontario.",
                 "Restaurants post their own deals and pay one flat plan of $50 a year, with no commission.",
                 "Diners find deals on a map, claim one and show a code at the counter. It's free for diners."],
         sections=[
             ("Markham deserves better than a cut of every bill", "<p>Markham is one of the best places in Canada to eat. Dim sum on Kennedy, ramen on Highway 7, Hong Kong cafés in every plaza, bubble tea on every corner. But the places that make it great are mostly small and independent, and they compete for attention with apps that take a percentage of every order.</p><p>Owners told us the same thing again and again: they have quiet hours they'd love to fill, but giving away a large share of each bill doesn't add up.</p>"),
             ("So we flipped the model", "<p>On FIG, a restaurant posts its own deal, for the hours it wants, with its own daily cap. Diners find it on a map, claim it, and show a code at the counter. The diner pays the restaurant directly. The restaurant pays FIG one plan, $50 a year, no matter how many diners walk in.</p><p>That means a deal on FIG is a decision the owner made, not a discount a platform forced on them. It also means the deals are real: the timer on a flash deal is the owner's timer.</p>"),
             ("Why Markham first", "<p>Because it's home, and because it has exactly the mix FIG is built for: hundreds of independent restaurants, busy plazas, and a lot of people who love finding a new place to eat. Richmond Hill is next.</p><p>If you own a restaurant in Markham, we'd love to set you up before launch. <a href=\"/#owners\">See the plan</a>.</p>"),
         ],
         faq=[("When does FIG launch?", "FIG is launching in Markham first. Download the app or join the waitlist on the home page to hear the moment it opens near you."),
              ("Does FIG take a commission?", "No. Restaurants pay one flat plan of $50 a year. FIG never takes a percentage of the bill.")]),

    dict(slug="one-plan-50-a-year", title="One plan, $50 a year: how FIG pricing works", date="2026-10-03", topic="For restaurants",
         dek="No commission, no fee per diner, every location included. Here's what FIG's $50 a year plan means for a restaurant.",
         keywords="FIG pricing, restaurant marketing cost, no commission restaurant app, $50 a year",
         points=["Restaurants pay $50 CAD a year for FIG. That's the only fee.",
                 "No commission on the bill, no fee per scan, no fee per diner.",
                 "Unlimited deals, unlimited scans, takeout, chats and a dashboard are all included."],
         sections=[
             ("What you pay", "<p>One plan: $50 CAD a year. It covers every location you run and every diner who walks in from FIG. That works out to about 14 cents a day.</p><p>There's no commission on the bill and no fee per scan. A diner who uses your deal pays you, at your counter, the way they always do.</p>"),
             ("What's included", "<ul><li>Unlimited deals, everyday and flash</li><li>Unlimited scans on any phone or tablet, for every staff member</li><li>Takeout ordering, with diners paying you at pickup</li><li>Chats with diners (their phone number stays private)</li><li>A dashboard with scans, new diners and what's working</li></ul>"),
             ("You control the cost of your deals", "<p>The only other cost is the deal itself, and you set it. Choose the days and hours, who it's for, and an optional daily cap. Pause anytime. Most owners start with one deal for their slowest hours.</p>"),
             ("Cancelling", "<p>Cancel the plan whenever you like in the app, under Your FIG plan. It runs to the end of the year you paid for. Read the full <a href=\"/business-terms\">business terms</a>.</p>"),
         ],
         faq=[("How much does FIG cost a restaurant?", "$50 CAD a year for all locations, with no commission and no per-diner fees."),
              ("Is there a contract?", "No long contract. The plan is yearly and you can cancel anytime; it runs to the end of the year you paid for.")]),

    dict(slug="how-the-passport-works", title="Your Passport: how stamps turn into free Premium", date="2026-10-03", topic="For diners",
         dek="Every meal on FIG earns a stamp. Spend 25, 50 or 100 stamps on free FIG Premium. Here's how it works.",
         keywords="FIG Passport, restaurant stamps, food rewards Markham, FIG Premium",
         points=["Every deal you use and every takeout pickup earns one stamp.",
                 "Stamps are a balance: 25 = a free week of Premium, 50 = three weeks, 100 = a month.",
                 "Your first stamp unlocks 3 days of Premium straight away."],
         sections=[
             ("Earning stamps", "<p>Every time you use a deal on FIG, staff scan your code and a stamp lands in your Passport, with the place, the date and what you saved. Takeout pickups earn stamps too.</p>"),
             ("Spending stamps", "<p>Stamps are a balance you spend, not a punch card that resets. 25 stamps buys a free week of FIG Premium, 50 buys three weeks and 100 buys a month. Claim a reward and keep collecting for the next one.</p>"),
             ("What Premium adds", "<p>Premium ($6.99 a month if you pay for it) adds unlimited AI picks: tell FIG what you feel like and it picks your three best deals nearby, with a reason for each. Without Premium you get 3 picks a day.</p>"),
             ("A food diary you didn't have to write", "<p>Your Passport doubles as a history of every place you've tried in Markham, and how much you saved there.</p>"),
         ],
         faq=[("Do stamps expire?", "Stamps stay in your Passport as a balance you can spend on Premium rewards."),
              ("Do takeout orders earn stamps?", "Yes. A scanned takeout pickup earns a stamp, just like a dine-in deal.")]),

    dict(slug="restaurant-deals-markham", title="How to find the best restaurant deals in Markham", date="2026-10-04", topic="For diners",
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
             ("Make it count", "<p>Every deal you use earns a Passport stamp, and stamps turn into free Premium. Eat out more, save more. <a href=\"/blog/how-the-passport-works\">How the Passport works</a>.</p>"),
         ],
         faq=[("What's the best app for restaurant deals in Markham?", "FIG is built specifically for Markham restaurant deals: live deals on a map, set by the restaurants themselves, free for diners."),
              ("Do I pay through the app?", "No. You pay the restaurant at the counter, like normal. FIG never handles payment for food.")]),

    dict(slug="delivery-app-commissions-vs-fig", title="Delivery app commissions vs a flat $50 plan: what restaurants keep", date="2026-10-04", topic="For restaurants",
         dek="Delivery apps charge restaurants a percentage of every order. FIG charges $50 a year. Here's how the two compare for a Markham restaurant.",
         keywords="delivery app commission, UberEats commission, DoorDash commission, restaurant commission fees Ontario, commission-free restaurant app",
         points=["Delivery platforms commonly charge restaurants a commission on every order, often reported in the 15% to 30% range depending on the plan.",
                 "FIG charges a flat $50 CAD a year with no commission, because diners come to the restaurant and pay it directly.",
                 "FIG isn't a delivery replacement: it fills dine-in and pickup during the hours a restaurant chooses."],
         sections=[
             ("How commission pricing works", "<p>Delivery platforms usually charge the restaurant a percentage of each order, plus sometimes marketing or promotion fees. The exact rate depends on the plan, but commissions in the 15% to 30% range are commonly reported. The more a restaurant sells through the app, the more it pays.</p>"),
             ("A simple example", "<p>Take a $40 dinner order. At a 25% commission, the platform keeps $10 of it. Ten orders like that a week is $100 a week, or about $5,200 a year, in commission alone.</p><p>On FIG, that same restaurant pays $50 for the whole year. The diner walks in, shows a code, and pays the restaurant directly. The only extra cost is the deal the owner chose to offer.</p>"),
             ("Different jobs", "<p>Delivery apps are good at getting food to someone's door. FIG does a different job: it brings people into the restaurant, or to the counter for takeout pickup, during the hours the owner wants to fill. Many restaurants will use both.</p>"),
             ("What you control on FIG", "<ul><li>The deal itself: what, when and for whom</li><li>A daily cap, so a deal never costs more than you planned</li><li>Pausing anytime, with one tap</li></ul><p><a href=\"/#owners\">See the $50 a year plan</a>.</p>"),
         ],
         faq=[("Does FIG charge a commission?", "No. FIG is a flat $50 CAD a year per restaurant, with every location and scan included."),
              ("Does FIG do delivery?", "No. Diners eat in or order takeout ahead and pick it up, paying the restaurant at the counter.")]),

    dict(slug="fill-slow-hours-restaurant", title="7 ways to fill slow hours at your restaurant", date="2026-10-04", topic="For restaurants",
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
         faq=[("What's the cheapest way to market a small restaurant?", "Target your slow hours with a specific, capped deal where diners are already looking. FIG does this for a flat $50 a year."),
              ("Will a deal hurt my margins?", "Not if you cap it and only run it in hours that would otherwise be empty.")]),

    dict(slug="student-food-deals-markham", title="Student food deals in Markham: eating out on a budget", date="2026-10-04", topic="For diners",
         dek="How high school and university students in Markham can eat out for less: after-school deals, group plans and free Premium with stamps.",
         keywords="student food deals Markham, cheap eats for students, after school food Markham, budget restaurants Markham, bubble tea deals Markham",
         points=["After-school hours are exactly when many restaurants are quiet, so that's when deals show up.",
                 "Set a budget filter in FIG once and only see deals you can afford.",
                 "Share a deal to your group chat so everyone can agree on where to go."],
         sections=[
             ("After school is deal time", "<p>Between 3 and 6 pm, a lot of Markham restaurants and bubble tea shops are quiet. That's when owners post deals, and when you're most likely to be hungry.</p>"),
             ("Set your budget once", "<p>When you sign up, tell FIG your budget and what you crave. The home feed and map then show deals that fit, nearest first, so you're not scrolling past $40 dinners.</p>"),
             ("Decide with your friends", "<p>Can't agree where to eat? Share a deal from FIG straight to your group chat. Everyone sees the same place, the same deal and how far it is.</p>"),
             ("Free is better", "<p>FIG is free for diners. Every deal you use earns a stamp, and your first stamp unlocks 3 days of Premium. Collect 25 stamps for a free week. <a href=\"/blog/how-the-passport-works\">How stamps work</a>.</p>"),
             ("Ask before you go", "<p>Not sure if there's space for six, or if the deal works for takeout? Message the restaurant from the deal. Your phone number stays private.</p>"),
         ],
         faq=[("Is FIG free for students?", "Yes. FIG is free for every diner. Premium is optional and can be earned free with stamps."),
              ("Do I need a credit card?", "No. You claim deals in the app and pay the restaurant directly at the counter.")]),

    dict(slug="flash-deals-explained", title="What are flash deals, and how do they work on FIG?", date="2026-10-04", topic="For diners",
         dek="Flash deals are short, real-time restaurant deals posted during quiet hours. Here's how to catch them in Markham.",
         keywords="flash deals restaurants, last minute restaurant deals, happy hour Markham, real time food deals",
         points=["A flash deal is a short deal a restaurant posts right now, for a quiet hour.",
                 "The timer is set by the restaurant and it's real: when it ends, the deal is gone.",
                 "Turn on flash alerts to hear about the ones near you."],
         sections=[
             ("What a flash deal is", "<p>Everyday deals run on a schedule, like every weekday afternoon. A flash deal is different: a restaurant posts it on the spot, because it has empty tables right now. It usually lasts an hour or two.</p>"),
             ("How to catch one", "<p>Turn on flash alerts in FIG and you'll get a notification when a flash deal drops near you. Flash deals also show at the top of your home feed and glow on the map.</p>"),
             ("Claim it, then go", "<p>Claim the flash deal in one tap and head over. Show your code at the counter. Like every FIG code, it refreshes every 5 minutes so it can't be screenshotted and reused.</p>"),
             ("For restaurant owners", "<p>Posting a flash deal takes a few seconds: pick the deal, the length and an optional cap. It's included in the <a href=\"/#owners\">$50 a year plan</a>.</p>"),
         ],
         faq=[("How long do flash deals last?", "The restaurant sets the length, usually an hour or two. The timer you see in the app is the real one."),
              ("Can I turn flash alerts off?", "Yes. Every alert in FIG can be turned off, and quiet hours at night are on by default.")]),

    dict(slug="takeout-without-delivery-fees", title="Order ahead, pick up, skip the delivery fees", date="2026-10-04", topic="For diners",
         dek="FIG takeout lets you order from a Markham restaurant's menu, watch it get made and pay at pickup, with no delivery or service fees.",
         keywords="takeout without delivery fees, order ahead pickup Markham, takeout deals Markham, pickup orders",
         points=["Order from the restaurant's menu in FIG and pay at the counter when you pick up.",
                 "No delivery fee and no service fee from FIG.",
                 "Deals apply to takeout unless the restaurant marks a deal dine-in only."],
         sections=[
             ("How it works", "<p>Open a restaurant in FIG, tap the menu and build your order. The restaurant accepts it and you can watch its status: new, cooking, ready. Head over, show your pickup code, pay at the counter and go.</p>"),
             ("Why pickup is cheaper", "<p>There's no driver, so there's no delivery fee, and FIG doesn't add a service fee. You pay the menu price, minus any deal, straight to the restaurant.</p>"),
             ("Deals and stamps still count", "<p>Deals work on takeout unless the restaurant says dine-in only, and every scanned pickup earns a Passport stamp.</p>"),
             ("Private by default", "<p>The restaurant never sees your phone number. If you need to change something, message them from the order in the app.</p>"),
         ],
         faq=[("Does FIG deliver?", "No. FIG takeout is order-ahead pickup. You collect the food and pay the restaurant at the counter."),
              ("Is there a fee for ordering takeout on FIG?", "No. FIG doesn't charge diners delivery or service fees.")]),
]
