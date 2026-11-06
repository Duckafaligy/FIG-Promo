# The blog's words (28, content lead, 2026-10-14). pages.py builds /blog from POSTS (via content.py); e9 owns the layout.
# Every fact about FIG here is true of the app today (src/content/help.ts, Settings → Get paid, the business terms).
# Every outside fact has its source URL in a comment next to it. No invented numbers, customers, quotes or restaurants:
# worked examples say they're examples, with round numbers anyone can redo with their own.
# Fields: slug, screen (the share image), title, date (first published), updated, topic, group (one of GROUPS), dek, desc (optional), keywords,
# points (the "Key takeaways" box), sections [(h2, html)], faq [(q, a)] (also the FAQPage data), publish_at (queued posts:
# ISO with its offset; pages.py leaves a post out until then). Inside sections: plain <table>, and
# <div class="callout tip|example|math"><b>Title</b>…</div>.
# pages.py refuses to build a post that says what FIG has retired (Premium, announcements, diner messages, the Counter code, stamps, deposits,
# paying at the counter for takeout, Toronto/GTA) or that the app works for diners before DINERS_OPEN: see blog_claims.py. A post that has to
# mention one on purpose lists the rule in claims_ok=["premium"].

# Sources used across several posts
# Stripe Canada, domestic cards 2.9% + CA$0.30: https://stripe.com/en-ca/pricing
# Uber Eats Canada plans (Lite 20% / Plus 25% / Premium 30% delivery, 10% pickup, 15% if in-store prices aren't validated;
#   self-delivery 15%): https://merchants.ubereats.com/ca/en/pricing
# DoorDash Canada plans (Basic 20% delivery / 10% pickup, Plus 25% / 8%, Premier 29% / 8%): https://merchants.doordash.com/en-ca/pricing
# Statistics Canada, food services and drinking places 2023: operating profit margin 3.6% (lowest since 2003); cost of goods
#   sold 35.7% of operating expenses: https://www150.statcan.gc.ca/n1/daily-quotidien/250218/dq250218d-eng.htm
# Food cost 28-32% of revenue on average (US Foods, quoted by Resy): https://resy.com/join/resources/restaurant-menu-pricing/
# CRA small supplier, $30,000 over four consecutive calendar quarters or in a single quarter:
#   https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/when-register-charge.html
# CRA: a store coupon reduces the price before GST/HST is calculated (RC4022, "Coupons"):
#   https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/rc4022/general-information-gst-hst-registrants.html
# Ontario HST 13%, and the point-of-sale rebate of the 8% provincial part on prepared food and drinks of $4 or less (GI-064):
#   https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/gi-064/harmonized-sales-tax-ontario-point-sale-rebate-on-prepared-food-beverages.html

UPDATED = "2026-10-14"

# The blog's four groups (FIX-LIST #145): /blog is laid out by them (a section each, its anchor the slug) and Home's
# "Good to know" cards link to them. Every post has a `group`, one of these slugs (pages.py stops the build otherwise).
# The descriptions are true today.
GROUPS = [
    ("eat-out-for-less", "Eat out for less", "How deals work, and how to spot a good one."),
    ("fill-quiet-hours", "Fill your quiet hours", "Deal ideas for slow hours, the math behind them, and how to get your team ready."),
    ("takeout-and-money", "Takeout & money", "What a takeout order leaves you, with the fees and HST in plain numbers."),
    ("fig-in-markham", "FIG in Markham", "Local guides, and why FIG starts here."),
]

POSTS = [
    dict(slug="why-we-built-fig", screen="map", title="Why we built FIG", date="2026-10-02", updated="2026-11-05", topic="News", group="fig-in-markham",
         dek="Markham is full of great independent restaurants, and most of them run on thin margins. FIG is a deals app built around that: free for diners and for restaurants, with no cut of a dine-in bill.",
         desc="Why FIG exists: Markham restaurants run on thin margins, so FIG is free for them and for diners, and takes no cut of a dine-in bill.",
         keywords="FIG app, Markham restaurants, independent restaurants, restaurant deals app, why FIG",
         points=["FIG is a restaurant deals app starting in Markham, Ontario. It opened to diners on November 4, 2026.",
                 "Restaurants post their own deals, for the hours they choose, with their own daily cap. Posting deals and scanning diners are free, with no fee per diner.",
                 "Diners find deals on a map, claim one in a tap and show a code at the counter. It's free for diners, with no ads for now.",
                 "FIG earns only 5% of the food on takeout orders paid in the app. Never from a dine-in bill.",
                 "Markham first, expanding to Richmond Hill and Vaughan Mills."],
         sections=[
             ("The short answer", """<p>We built FIG because the restaurants that make a city worth eating in are mostly small and independent, and the tools that promise them customers usually charge a share of every order. FIG turns that around: a restaurant posts a deal for the hours it wants to fill, nearby diners find it on a map, and the diner pays the restaurant at the counter. FIG takes nothing from that bill.</p>
<p>This post explains the thinking behind that model, what FIG does and doesn't do, and how it pays for itself without ads (for now) or commissions on dine-in.</p>"""),
             # StatCan 2023: operating profit margin 3.6%, lowest since 2003 (see sources at the top)
             ("Restaurants run on thin margins", """<p>Running a restaurant is a hard way to make money. Statistics Canada reported that in 2023 the operating profit margin for food services and drinking places in Canada fell to 3.6%, the lowest since 2003. Food and drink bought for resale was the largest expense, at 35.7% of operating costs, with wages close behind.</p>
<p>On a 3.6% margin, a $40 dinner leaves about $1.44 of profit. Anything that takes a percentage of the bill comes straight out of that, and usually more than all of it.</p>
<div class="callout math"><b>What a commission does to a thin margin</b><ul><li>A $40 order at a 3.6% margin: about $1.44 of profit.</li><li>The same order on a 25% commission plan: $10.00 to the platform.</li><li>The commission is about seven times the profit the order would have made on its own.</li></ul><p>Every restaurant's numbers are different, but the shape is the same: a percentage of the bill is paid before the restaurant has made a cent.</p></div>"""),
             # Uber Eats Canada 20/25/30% delivery, DoorDash Canada 20/25/29% (sources at the top)
             ("What delivery apps charge, and why that's a different job", """<p>Delivery platforms publish their Canadian rates. Uber Eats lists marketplace plans at 20%, 25% and 30% of each delivery order, and 10% on pickup orders. DoorDash lists 20%, 25% and 29% on delivery, and 10% or 8% on pickup, depending on the plan. Those rates pay for real work: drivers, the app, the marketplace and the customers it brings.</p>
<p>FIG isn't trying to replace delivery. It does a narrower job: getting people <em>into</em> a restaurant, or to the counter for a pickup, during the hours the owner chooses. For that job, a percentage of every bill isn't needed, so FIG doesn't charge one. <a href="/blog/delivery-app-commissions-vs-fig">Delivery app commissions vs FIG, with the numbers</a>.</p>"""),
             ("So we flipped the model", """<p>On FIG, a deal is a decision the owner made. The restaurant picks:</p>
<ul><li><strong>What</strong> the deal is: a percentage off, a dollar amount off, 2-for-1, or something free with an order, on the whole bill or on specific dishes from its menu.</li><li><strong>When</strong> it runs: which days and hours, every week, once, or until a date. Or a <a href="/blog/flash-deals-explained">flash deal</a> right now, for a quiet hour.</li><li><strong>How many</strong>: a daily cap, so a deal never gives away more than planned. It stops on its own when the cap is reached.</li><li><strong>Where</strong>: dine-in only, or also as takeout.</li></ul>
<p>A diner finds the deal on Home or on the map, taps Claim, and the deal waits on their Deals page. At the restaurant, staff scan the diner's code with the restaurant side of FIG (on any phone, tablet or computer). The deal comes off the bill, and the diner pays the restaurant the way they always do.</p>"""),
             ("What FIG is for diners", """<ul><li><strong>Free.</strong> No subscription, no fees, no ads for now.</li><li><strong>Deals you can actually use.</strong> Live deals near you, nearest first, filtered by what you crave, your budget and your diet.</li><li><strong>No pressure.</strong> A claim doesn't time out. It works for as long as the deal runs, and it only ends when the restaurant ends the deal, or a flash or dated deal is over.</li><li><strong>Private.</strong> Restaurants see your first name and last initial, never your phone number or email.</li><li><strong>Honest reviews.</strong> Only diners whose visit was scanned can review a restaurant, so every review comes from a real meal. Deals get likes; restaurants get stars.</li></ul>"""),
             ("How FIG pays for itself", """<p>Restaurants use FIG <strong>for free</strong>. FIG earns in one way: on <strong>takeout paid in the app</strong>, it keeps 5% of the food (before tax), and Stripe's card fee comes off the same payment. The rest, tax included, goes to the restaurant.</p>
<p>That's it. No ads for now, no fee per diner, no commission on a dine-in bill, and nothing for sale that changes search order or reviews. <a href="/blog/how-fig-makes-money">How FIG makes money, in full</a>.</p>"""),
             # Main Street Unionville and Markham Village: https://en.wikipedia.org/wiki/Main_Street_Unionville ,
             #   https://en.wikipedia.org/wiki/Markham_Village ; Pacific Mall, NE corner of Steeles and Kennedy: https://en.wikipedia.org/wiki/Pacific_Mall
             ("Why Markham first", """<p>Because it's home, and because it has exactly the mix FIG is built for: hundreds of independent restaurants spread across plazas and main streets, from Pacific Mall at Steeles and Kennedy to Main Street Unionville and the old Main Street of Markham Village, and a lot of people who love finding somewhere new to eat.</p>
<p>FIG is in Markham first, expanding to Richmond Hill and Vaughan Mills. It is open to diners and restaurants now: diners can check out deals at www.figpromo.ca/app with no account needed to look around, and restaurants set up their page, menu and deals there too.</p>"""),
             ("What's next", """<p>We're signing Markham restaurants now. If you own one, building your page, your menu and your first deal takes a few minutes, and it is free. To publish them, you finish Stripe's identity and bank checks. <a href="/#owners">See how it works for restaurants</a> or read the <a href="/help">Help center</a>.</p>"""),
         ],
         faq=[("What is FIG?", "FIG is a restaurant deals app. Restaurants post their own deals; diners find them on a map, claim one and show a code at the counter. It's free for diners."),
              ("Is FIG open yet?", "Yes. FIG opened to diners on November 4, 2026, in Markham first, expanding to Richmond Hill and Vaughan Mills."),
              ("Does FIG take a commission?", "Not on dine-in. Posting deals and scanning diners are free, with no fee per diner. On takeout orders diners pay for in the app, FIG keeps 5% of the food before tax."),
              ("Does FIG show ads?", "No, not for now. FIG has no ads, and paying FIG never moves a restaurant up in search or on the map."),
              ("Does FIG deliver?", "No. Diners eat in, or order takeout with a deal and pick it up."),
              ("Do I need the app to use FIG?", "No. FIG runs in your web browser at www.figpromo.ca/app. Diners can check out deals there today, with no account needed to look around, and restaurants set up there too. The App Store and Google Play apps are coming soon.")]),

    dict(slug="how-fig-makes-money", screen="tdash", title="How FIG makes money: 5% of in-app takeout", date="2026-10-07", updated="2026-10-25", topic="For restaurants", group="takeout-and-money",
         dek="FIG is free for restaurants, with no commission on dine-in and no fee per diner. FIG earns only on takeout orders diners pay for in the app: it keeps 5% of the food.",
         desc="FIG is free for restaurants, with no commission on dine-in. It earns only 5% of the food on takeout orders paid in the app.",
         keywords="free restaurant app, FIG for restaurants, no commission restaurant app, restaurant deals app Markham",
         points=["Free for restaurants: your page, unlimited deals, every scan and insights cost nothing, for up to 2 locations for now.",
                 "There's no upfront payment, no monthly or yearly fee and nothing to choose or cancel.",
                 "No commission and no fee per diner on dine-in. On takeout paid in the app, FIG keeps 5% of the food, and Stripe's card fee comes off the same payment.",
                 "On a $30 takeout order, FIG's 5% is $1.50 and Stripe's card fee is about $1.28. You keep about $27.22 of the $30, plus the HST you remit.",
                 "Paying FIG never changes your search position, your reviews or your deal."],
         sections=[
             ("The short answer", """<p>FIG is free for restaurants. Everything a restaurant needs to bring diners in costs nothing: your page, your menu, unlimited everyday and flash deals, scanning diners at the counter and the insights that show what's working, for up to 2 locations for now. A diner who walks in with your deal pays you directly, and FIG takes nothing from that bill.</p>
<p>FIG earns in one way: it keeps 5% of the food on takeout orders that diners pay for in the app. This post goes through it, with the arithmetic.</p>"""),
             ("What you get, and what it costs", """<table><thead><tr><th>On FIG</th><th>What it costs you</th></tr></thead><tbody>
<tr><td>Your restaurant page, menu and photos</td><td>Free</td></tr>
<tr><td>Everyday deals and flash deals, as many as you like</td><td>Free</td></tr>
<tr><td>Scanning diners at the counter (any phone, tablet or computer)</td><td>Free, no fee per diner</td></tr>
<tr><td>Insights: views, claims, diners who came in and came back, per deal, day by day</td><td>Free</td></tr>
<tr><td>Your locations, under one sign-in</td><td>Free: up to 2 locations for now</td></tr>
<tr><td>Takeout paid in the app</td><td>5% of the food before tax, plus Stripe's card fee</td></tr>
</tbody></table>
<p>Everything above is free: no upfront payment and no monthly or yearly fee.</p>"""),
             ("No contract, nothing to cancel", """<p>There is no contract. You can pause your deals or close your account whenever you like, and takeout orders already paid are paid out as usual. The full rules are in the <a href="/business-terms">business terms</a>.</p>"""),
             # Stripe 2.9% + CA$0.30 domestic cards (source at the top); HST 13% Ontario
             ("Takeout paid in the app: 5% of the food", """<p>When a diner orders takeout and pays in the app, the payment goes through Stripe. FIG keeps 5% of the food before tax, Stripe's card fee comes off the same payment, and the rest, including the HST, is paid out to you. The HST is yours to remit, as with any sale. FIG isn't registered for HST yet; once it is, it will add 13% HST to its 5% fee and tell restaurants at least 30 days before that starts.</p>
<div class="callout math"><b>A $30 takeout order in Markham</b><table><thead><tr><th></th><th>Amount</th></tr></thead><tbody>
<tr><td>Food</td><td>$30.00</td></tr>
<tr><td>HST at 13%</td><td>$3.90</td></tr>
<tr><td>The diner pays</td><td>$33.90</td></tr>
<tr><td>Stripe: 2.9% of $33.90 + $0.30</td><td>&minus;$1.28</td></tr>
<tr><td>FIG: 5% of the $30.00 food</td><td>&minus;$1.50</td></tr>
<tr><td>Paid out to you</td><td>$31.12</td></tr>
<tr><td>Of which HST you remit</td><td>$3.90</td></tr>
<tr><td><strong>You keep from the food</strong></td><td><strong>$27.22 (90.7%)</strong></td></tr>
</tbody></table><p>Stripe's rate is its published price for Canadian domestic cards. Its fee is charged on the full payment, tax included.</p></div>
<p>Takeout on FIG is paid in the app, so it needs two things in Settings → Get paid: your HST number (it goes on every takeout receipt, with your restaurant as the seller) and Stripe payouts. Dine-in deals need neither. Each month's takeout statement shows sales, HST, fees and what you kept.</p>"""),
             ("Why not charge per diner, like other apps?", """<p>Because the restaurant already gave something up: the deal itself. A 2-for-1 or 20% off is the price of the visit. Charging again for the same diner would push owners to make deals smaller and rarer, which is worse for everyone, diners included. FIG wins when deals are good enough to post, so it doesn't tax them: there is no fee per diner, however many come.</p>"""),
             ("What paying FIG never does", """<ul><li>Change your deal or its price.</li><li>Move you up in search or on the map.</li><li>Hide, remove or reorder reviews. Only diners whose visit was scanned can review, and you can reply in public.</li><li>Share a diner's phone number or email with you. Orders and reviews show their first name and last initial.</li></ul>
<p>The full rules are in the <a href="/business-terms">business terms</a>.</p>"""),
             ("How this compares", """<p>If you're weighing FIG against a delivery app, compare the job, not just the rate. Delivery apps bring the food to the door and charge for it: Uber Eats and DoorDash publish Canadian delivery plans between 20% and 30% per order. FIG brings the diner to your door for free, with nothing per diner. For pickup, the big apps charge 8% to 10% of an order (Uber Eats charges 15% if your in-store prices aren't validated), which is close to what FIG's 5% plus the card fee comes to. <a href="/blog/delivery-app-commissions-vs-fig">The full comparison, with worked examples</a>.</p>"""),
             ("Getting started", """<p>Sign up as a business, add your menu and draft your first deal. Setting up is free, and everything stays a draft until you finish Stripe's identity, business and bank checks to publish. When you're ready for takeout paid in the app, add your HST number and connect Stripe in Settings → Get paid. Questions? <a href="/help">Restaurant help</a> or <a href="/contact">message us</a>.</p>"""),
         ],
         faq=[("How much does FIG cost a restaurant?", "Nothing. Signing up, building your page, menu and deals, publishing them, scanning and your dashboard are free, for up to 2 locations for now. On takeout orders diners pay for in the app, FIG keeps 5% of the food before tax, and Stripe's card fee comes off the same payment."),
              ("Is there a commission on dine-in?", "No. A diner who uses your deal pays you at the counter, and FIG takes nothing from that bill. There's no fee per diner."),
              ("Who pays Stripe's fee on takeout?", "It comes off the same in-app payment, before the payout: 2.9% + $0.30 on Canadian cards, Stripe's published rate. On a $33.90 payment that's about $1.28."),
              ("Does FIG collect HST for me?", "The diner pays the HST with the order and it's paid out to you with the rest. It's yours to remit. Your HST number goes on every takeout receipt, with your restaurant as the seller."),
              ("Is there a contract?", "No. There's no contract and nothing to cancel. You can pause your deals or close your account whenever you like, and takeout orders already paid are paid out as usual."),
              ("Can I pay to rank higher?", "No. Nothing you pay FIG changes where you appear in search or on the map, or what your reviews say.")]),

    # Places: Main Street Unionville https://en.wikipedia.org/wiki/Main_Street_Unionville ; Markham Village and its Main Street,
    #   two Main Streets over 4 km apart, both crossing Highway 7: https://en.wikipedia.org/wiki/Markham_Village ;
    #   Pacific Mall (NE corner of Steeles and Kennedy, Heritage Town food court and market): https://en.wikipedia.org/wiki/Pacific_Mall ;
    #   York University Markham Campus in Markham Centre, opened Fall 2024: https://presidentsreport2023.yorku.ca/opening-the-doors-to-innovation/ ;
    #   Toogood Pond steps from Main Street Unionville: https://www.blogto.com/travel/2023/03/unionville-ontario/ ;
    #   communities (Unionville, Markham Village, Cornell, Milliken, Cathedraltown): https://en.wikipedia.org/wiki/History_of_Markham,_Ontario
    dict(slug="restaurant-deals-markham", screen="map", title="How to find the best restaurant deals in Markham", date="2026-10-04", updated="2026-11-05", topic="For diners", group="fig-in-markham",
         dek="A practical guide to eating out for less in Markham, Ontario: when restaurants post deals, where to look across the city, and how to use FIG to find and use them.",
         desc="How to eat out for less in Markham, Ontario: when restaurants post deals, where to look, and how to find and use them on FIG.",
         keywords="restaurant deals Markham, Markham food deals, cheap eats Markham, Markham restaurants, Unionville restaurants, Pacific Mall food",
         points=["The best deals show up when restaurants are quiet: weekday afternoons, early dinners and late evenings.",
                 "Markham's food is spread across plazas and main streets: Highway 7, Steeles and Kennedy, Main Street Unionville, Markham Village and more.",
                 "FIG shows live deals on a map, nearest first, filtered by craving, budget and diet. It is open to diners in Markham now.",
                 "Claim in one tap, show your code at the counter, pay the restaurant as usual. Claims don't time out while the deal runs.",
                 "Reviews on FIG come only from scanned visits, so you can trust what you read."],
         sections=[
             ("The short answer", """<p>The best restaurant deals in Markham are posted for the hours restaurants are quiet, by the restaurants themselves. Look on weekday afternoons and early evenings, check the areas with lots of independent places close together, and use one map of live deals instead of ten Instagram accounts. That's what FIG is for: every live deal near you, nearest first, filtered to what you actually want to eat.</p>"""),
             ("1. Go when restaurants are quiet", """<p>Restaurants are busiest at weekend lunch and dinner. The rest of the week, most have hours with empty tables, and an empty table earns nothing. That's when owners are most willing to offer something.</p>
<table><thead><tr><th>When</th><th>Why it's good for deals</th></tr></thead><tbody>
<tr><td>Weekdays, about 2 to 5 pm</td><td>Between lunch and dinner: the slowest stretch for many kitchens</td></tr>
<tr><td>Early dinner, Monday to Thursday</td><td>Before the evening rush, and weeknights are quieter than weekends</td></tr>
<tr><td>Late evening</td><td>After the dinner rush, for dessert, bubble tea and late snacks</td></tr>
<tr><td>Bad weather</td><td>Rain and snow empty dining rooms fast: a good time for <a href="/blog/flash-deals-explained">flash deals</a></td></tr>
</tbody></table>
<p>Every restaurant is different, so treat this as a pattern, not a rule. On FIG, each deal shows its own days and hours.</p>"""),
             ("2. Know where the food is", """<p>Markham doesn't have one food street. It has dozens of plazas and a few main streets, each with a different feel:</p>
<ul><li><strong>Highway 7.</strong> The long east-west spine, lined with plazas, and home to Markham Centre, the city's new downtown, where York University's Markham Campus opened in 2024.</li><li><strong>Steeles and Kennedy.</strong> Around Pacific Mall, on the northeast corner, which has its own food court and market, Heritage Town.</li><li><strong>Main Street Unionville.</strong> The historic village street, with restaurants, pubs and cafés, steps from Toogood Pond.</li><li><strong>Markham Village.</strong> The city's other Main Street, in the old town centre, a few kilometres east of Unionville's.</li><li><strong>Neighbourhood plazas</strong> in Milliken, Cornell, Cathedraltown and beyond, where many of the places locals love are tucked away.</li></ul>
<p>Because so many restaurants share a plaza, a deal nearby often means a short walk, not a drive.</p>"""),
             ("3. Let the map do the searching", """<p>Open FIG and you see live deals around you, nearest first, on Home and on the map. Tell FIG once what you crave, your budget and any diet (halal, vegetarian, vegan, gluten-free and more), and the list becomes the places that actually fit you.</p>
<p>On the map, pick how far you're willing to go: 1, 2, 5 or 10 km. If nothing's live that close, FIG widens the search to the nearest places rather than showing an empty map. Search has a start screen too: your recent searches, popular cravings and the places on FIG.</p>
<div class="callout tip"><b>No location? No problem.</b><p>FIG works without your location. It shows Markham by default, and deals are never locked to where you are. Turn location on when you want "nearest first" to mean nearest to you.</p></div>"""),
             ("4. Claim, go, show your code", """<ol><li>Open a restaurant and tap Claim on the deal you want.</li><li>It waits on your Deals page. A claim has no time limit: it works for as long as the deal runs.</li><li>At the restaurant, open your Deals page and tap Show QR. Staff scan it.</li><li>The deal comes off the bill. You pay the restaurant as usual.</li></ol>
<p>A code works once, so a screenshot of a used code just says already used. <a href="/blog/how-restaurant-deals-work">How deals work, step by step</a>.</p>"""),
             ("5. Read the deal properly", """<p>A good deal is one that fits what you were going to do anyway. Before you claim, check:</p>
<ul><li><strong>Days and hours.</strong> Many deals run only in quiet hours.</li><li><strong>Dine in or takeout.</strong> Some deals are for eating in only; others also work as <a href="/blog/takeout-without-delivery-fees">takeout you pick up</a>.</li><li><strong>Which dishes.</strong> Some deals are on the whole order, some on specific dishes from the menu, which you can see on the restaurant's page.</li><li><strong>The daily cap.</strong> Popular deals can run out for the day.</li></ul>"""),
             ("6. Trust real reviews", """<p>Only diners whose visit was scanned can review a restaurant on FIG, so every review comes from a real meal. Restaurants get stars; deals get likes. Restaurants can reply in public, and paying FIG never hides or changes a review. <a href="/blog/how-to-read-restaurant-reviews">Reading reviews on FIG, in a minute</a>.</p>"""),
             ("7. Bring friends", """<p>Group plans fall apart over "where should we go?". Share the restaurant's link from FIG to your group chat: everyone sees the same place and its live deals. <a href="/blog/group-dining-deals">Eating out as a group, with deals</a>.</p>"""),
             ('Five mistakes that cost you the deal', "<ul><li><strong>Showing up outside the hours.</strong> Check the deal's days and times before you go.</li><li><strong>Ordering takeout on a dine-in deal.</strong> Look for Dine in or takeout.</li><li><strong>Waiting until the evening on a popular deal.</strong> Daily caps run out; claim early.</li><li><strong>Showing a screenshot.</strong> A screenshot of a code that was already scanned just says already used: open your Deals page at the counter.</li><li><strong>Forgetting the extras.</strong> The deal covers what it says; drinks and sides are usually full price.</li></ul>"),
         ],
         faq=[("What's the best app for restaurant deals in Markham?", "FIG is built for Markham restaurant deals: live deals on a map, set by the restaurants themselves, free for diners, with no ads for now. Check out deals at www.figpromo.ca/app."),
              ("When do Markham restaurants post the most deals?", "During their quiet hours: typically weekday afternoons, early weeknight dinners and late evenings. Each deal on FIG shows its own days and hours."),
              ("Do I pay through the app?", "For dine-in, no: you pay the restaurant at the counter as usual. Takeout is paid in the app when you order."),
              ("Does FIG need my location?", "No. FIG shows Markham by default and deals are never locked to where you are. Location just makes 'nearest first' mean nearest to you."),
              ("Do claimed deals expire?", "Not on their own. A claim works for as long as the deal runs. It ends only when the restaurant ends the deal, or a flash or dated deal is over."),
              ("Is FIG only in Markham?", "Markham first, expanding to Richmond Hill and Vaughan Mills.")]),

    dict(slug="delivery-app-commissions-vs-fig", screen="tscanner", title="Delivery app commissions vs FIG: what restaurants keep", date="2026-10-04", updated="2026-10-24", topic="For restaurants", group="takeout-and-money",
         dek="Delivery apps charge restaurants a percentage of every order. FIG is free for restaurants on dine-in, with nothing per diner, and keeps 5% of the food on in-app takeout. Here are the published Canadian rates and what a restaurant keeps from the same order.",
         desc="Delivery apps take a share of every order. FIG takes nothing per dine-in diner and 5% of the food on in-app takeout. The published Canadian rates, side by side.",
         keywords="delivery app commission Canada, Uber Eats commission, DoorDash commission, restaurant commission fees Ontario, commission-free restaurant app",
         points=["Uber Eats lists Canadian delivery plans at 20%, 25% and 30% of each order; DoorDash at 20%, 25% and 29%.",
                 "For pickup, Uber Eats lists 10% (15% if in-store prices aren't validated) and DoorDash 8% to 10%.",
                 "On FIG, a dine-in diner costs nothing; the only cost per visit is the deal you chose. In-app takeout costs 5% of the food plus Stripe's card fee: about 9.3% of a $30 order.",
                 "On a $30 delivery order at 25%, a restaurant keeps $22.50 of the food. On a $30 FIG takeout paid in the app, it keeps about $27.22.",
                 "Different jobs: delivery apps bring food to the door; FIG brings diners in and to the counter. Many restaurants will use both."],
         sections=[
             ("The short answer", """<p>Delivery apps charge restaurants a percentage of each order, and in Canada the published delivery rates run from 20% to 30%. FIG is free to use, charges nothing for a diner who eats in with your deal, and keeps 5% of the food (plus Stripe's card fee) on takeout paid in the app. FIG doesn't deliver, so it isn't a like-for-like replacement: it's a cheaper way to fill the tables and the pickup counter you already have.</p>"""),
             ("The published rates", """<p>Both big platforms publish their Canadian plans. Rates as listed in October 2026; your own agreement may differ.</p>
<table><thead><tr><th>Plan</th><th>Delivery</th><th>Pickup</th></tr></thead><tbody>
<tr><td>Uber Eats Lite</td><td>20%</td><td>10%</td></tr>
<tr><td>Uber Eats Plus</td><td>25%</td><td>10%</td></tr>
<tr><td>Uber Eats Premium</td><td>30%</td><td>10%</td></tr>
<tr><td>Uber Eats, your own drivers</td><td>15%</td><td>10%</td></tr>
<tr><td>DoorDash Basic</td><td>20%</td><td>10%</td></tr>
<tr><td>DoorDash Plus</td><td>25%</td><td>8%</td></tr>
<tr><td>DoorDash Premier</td><td>29%</td><td>8%</td></tr>
<tr><td>FIG, dine-in with a deal</td><td>n/a</td><td>No fee per diner (free)</td></tr>
<tr><td>FIG, takeout paid in the app</td><td>n/a</td><td>5% of the food + Stripe's 2.9% + $0.30</td></tr>
</tbody></table>
<p>Uber Eats notes its pickup fee rises to 15% if your in-store prices aren't validated. Higher plans buy more visibility, a wider delivery area and member programs, which is real value for some restaurants.</p>"""),
             ("Worked example: one $30 order", """<div class="callout math"><b>What the restaurant keeps from $30 of food</b><table><thead><tr><th>How the order came in</th><th>Platform takes</th><th>You keep from the food</th></tr></thead><tbody>
<tr><td>Delivery, 30% plan</td><td>$9.00</td><td>$21.00</td></tr>
<tr><td>Delivery, 25% plan</td><td>$7.50</td><td>$22.50</td></tr>
<tr><td>Delivery, 20% plan</td><td>$6.00</td><td>$24.00</td></tr>
<tr><td>Pickup, 10% plan</td><td>$3.00</td><td>$27.00</td></tr>
<tr><td>Pickup, 8% plan</td><td>$2.40</td><td>$27.60</td></tr>
<tr><td>FIG takeout paid in the app</td><td>$1.50 FIG + $1.28 Stripe</td><td>$27.22</td></tr>
<tr><td>FIG dine-in with a deal</td><td>$0.00</td><td>$30.00, minus the deal you chose</td></tr>
</tbody></table><p>The FIG card fee is Stripe's 2.9% + $0.30 on the $33.90 the diner pays with 13% HST. The platform rows use the published plan rates; card processing and any marketing you buy are set by each platform's own terms. On dine-in, FIG takes no cut of any order.</p></div>
<p>Be honest with yourself about pickup: an 8% to 10% pickup plan and FIG's in-app takeout land in the same range. FIG's real difference is everything around it: dine-in costs nothing per diner, there's no contract, and nothing you pay for changes where you show up.</p>"""),
             ("Worked example: a year of orders", """<div class="callout math"><b>Ten $40 orders a week</b><ul><li>At a 25% delivery commission: $10 an order, $100 a week, about $5,200 a year.</li><li>The same ten diners eating in with a FIG deal: $0 to FIG. Your cost is the deal itself, which you chose and capped.</li><li>As FIG takeout paid in the app: 5% of $40 is $2.00, and Stripe's fee on the $45.20 payment is about $1.61, so about $3.61 an order, or roughly $1,880 a year.</li></ul></div>"""),
             ("The cost you choose: the deal", """<p>A deal isn't free: if you offer 20% off, that 20% is a real cost. The difference is that you set it, for the hours you choose, with a daily cap, on the dishes you pick. A deal that fills a table at 3 pm, when it would otherwise be empty, can be worth it at a lower margin, as long as it covers its food cost and you're not giving it away at 7 pm on a Saturday. <a href="/blog/slow-hour-deal-math">How to run a slow-hour deal that makes money</a>.</p>"""),
             ("Different jobs, used together", """<p>Delivery apps are very good at one thing: getting food to someone's door. That has real costs (drivers, distance, support), and the commission pays for them. FIG does a different job:</p>
<ul><li>bringing people <em>into</em> your restaurant in hours you want to fill;</li><li>letting diners order takeout with your deal and pick it up, with no delivery fee for them;</li><li>keeping the relationship in your hands: you reply to their reviews and decide every deal.</li></ul>
<p>Plenty of restaurants will keep delivery for delivery and use FIG to fill the dining room and the counter.</p>"""),
             ("What you control on FIG", """<ul><li>The deal: what, on which dishes, which days and hours, dine-in only or takeout too.</li><li>A daily cap, so a deal never gives away more than planned.</li><li>Takeout: pause it for a rush, add prep time, or turn it off.</li><li>Whether to take takeout paid in the app, the only thing FIG earns on.</li></ul>
<p><a href="/blog/how-fig-makes-money">How FIG makes money</a> · <a href="/business-terms">Business terms</a></p>"""),
             ('Run your own numbers', "<p>Before you change anything, look at last month's statements and answer four questions:</p>\n<ol><li>What share of your sales came through each app, and at what rate?</li><li>How many of those orders were pickup, not delivery? Pickup on a delivery app still pays a commission.</li><li>Which hours are your dining room quiet? That's where FIG deals help most.</li><li>How many of your app customers have ever eaten in? Diners who come in are the ones who become regulars.</li></ol>\n<p>If a lot of your app orders are pickup from people who live nearby, a takeout deal on FIG is worth testing alongside.</p>"),
             ('If you already use delivery apps', '<ul><li><strong>Keep delivery for delivery.</strong> FIG doesn\'t replace a driver network.</li><li><strong>Add FIG for the room and the counter.</strong> Post deals for your quiet hours and let diners order takeout with them.</li><li><strong>Tell your regulars.</strong> A sign at the counter, "We\'re on FIG: deals Monday to Thursday afternoons", points app customers to the cheaper way to reach you.</li><li><strong>Compare after a month.</strong> FIG\'s free insights show views, claims, the diners who came in and who came back.</li></ul>'),
         ],
         faq=[("What commission do delivery apps charge in Canada?", "As published in October 2026: Uber Eats 20%, 25% or 30% on delivery and 10% on pickup; DoorDash 20%, 25% or 29% on delivery and 10% or 8% on pickup, depending on the plan."),
              ("Does FIG charge a commission?", "Not on dine-in: deals and scans are free, with no fee per diner. On takeout paid in the app, FIG keeps 5% of the food before tax, and Stripe's card fee comes off the same payment."),
              ("Is FIG cheaper than a delivery app's pickup plan?", "Close. On a $30 order, FIG's in-app takeout costs about $2.78 including the card fee; an 8% to 10% pickup plan costs $2.40 to $3.00. FIG's difference is that dine-in diners cost nothing."),
              ("Does FIG do delivery?", "No. Diners eat in, or order takeout and pick it up."),
              ("Can I use FIG and a delivery app together?", "Yes. Many restaurants will keep delivery for delivery and use FIG to fill quiet hours and the pickup counter."),
              ("Does paying FIG improve my ranking?", "No. Nothing you pay FIG moves a restaurant up in search or on the map.")]),

    # Food cost 28-32% (Resy/US Foods) and StatCan 3.6% margin: sources at the top
    dict(slug="fill-slow-hours-restaurant", screen="tdash", title="7 ways to fill slow hours at your restaurant", date="2026-10-04", updated="2026-10-24", topic="For restaurants", group="fill-quiet-hours",
         dek="Practical, low-cost ways for independent restaurants to bring in diners on quiet afternoons and weeknights, with the arithmetic to make sure a deal adds money instead of giving it away.",
         desc="Low-cost ways for independent restaurants to fill quiet afternoons and weeknights, with the math to make sure a deal adds money.",
         keywords="fill slow hours restaurant, restaurant marketing ideas, slow restaurant days, increase restaurant traffic, Markham restaurant marketing, happy hour ideas",
         points=["Find your real quiet hours from your own receipts, and aim deals only at those hours.",
                 "Make deals specific (a dish, a time, a price) and cap them per day so they can't cost more than planned.",
                 "Check the math: a deal in an empty hour only needs to cover its food cost to add money.",
                 "Use flash deals for surprise quiet spells, and takeout to fill the kitchen without filling tables.",
                 "Measure claims, scans and return visits per deal; keep what works and pause the rest."],
         sections=[
             ("The short answer", """<p>To fill slow hours without hurting your margins, aim a specific, capped deal at exactly the hours that are empty, put it where people are deciding where to eat, and measure whether it brings new diners back. A deal in a quiet hour only has to cover its own food cost to add money, because the alternative is an empty table that earns nothing.</p>
<p>Here are seven ways to do it, in the order we'd try them.</p>"""),
             ("1. Find your real quiet hours", """<p>Don't guess. Pull a few weeks of receipts (most point-of-sale systems can show sales by hour) and mark each hour of the week as busy, steady or quiet. For many restaurants the quiet hours are weekday afternoons, roughly 2 to 5 pm, and early weeknights. Yours might be different: a lunch spot near offices can be dead on Saturdays.</p>
<div class="callout tip"><b>A simple grid</b><p>Seven columns (days) by your opening hours (rows). Fill each cell with the average number of tables or orders. The cells with the lowest numbers are where a deal does the most good and the least harm.</p></div>"""),
             ("2. Make the deal specific", """<p>"2-for-1 dumplings, Monday to Thursday, 2 to 5 pm" beats "10% off". A specific deal is easier to share, easier for staff to honour and easier for a diner to decide on. On FIG a deal can be a percentage off, a dollar amount off, 2-for-1, or something free with an order, on the whole bill or on specific dishes from your menu, and it can run on chosen days and hours every week, once, or until a date. <a href="/blog/deal-types-percent-dollar-2-for-1">Which deal type to pick, with worked examples</a>.</p>"""),
             ("3. Do the math, then cap it", """<p>Restaurants in Canada run on thin margins: Statistics Canada put the 2023 operating profit margin for food services and drinking places at 3.6%. That's why the deal has to be right. The key idea: in an hour that would otherwise be empty, the deal only needs to cover its <em>food cost</em> to add money, because rent, wages and the lights are being paid either way.</p>
<div class="callout math"><b>Example: a $16 dish at 3 pm on a Tuesday</b><ul><li>Food cost at 30% (the industry average is 28% to 32%): $4.80 a plate.</li><li>20% off: the diner pays $12.80. Left after food cost: $8.00 a plate.</li><li>2-for-1: two plates for $16. Food cost $9.60. Left: $6.40 for two plates.</li><li>An empty table at 3 pm: $0.</li></ul><p>Both deals add money in an empty hour. At 7 pm on a Saturday, when the table would have sold at full price, the same 2-for-1 loses you about $16. That's why the hours matter more than the discount.</p></div>
<p>Then cap it. A daily cap on FIG stops the deal automatically once it's been used that many times, so a deal can never cost more than you planned. Start small (say 10 a day), watch it for two weeks, and raise it if it's working.</p>"""),
             ("4. Go where people are deciding", """<p>Most people decide where to eat on their phones, often in a group chat, a few minutes before they go. A poster in the window reaches people who are already there. A deal on a map of nearby deals reaches people who are deciding right now. On FIG, live deals show on Home and the map, nearest first, and diners can send a restaurant's link to their group chat, which opens its page with its live deals.</p>"""),
             ("5. Use flash deals for surprise quiet spells", """<p>Rain, a cancelled reservation, a slow lunch you didn't see coming. A flash deal is a short deal you post on the spot: pick the deal, how long it runs and an optional cap, and it's live near you within seconds, with a real timer. When the timer ends, it's gone. <a href="/blog/flash-deals-explained">How flash deals work</a>.</p>"""),
             ("6. Fill the kitchen, not just the tables", """<p>Some hours the dining room stays quiet but the kitchen has room. A deal diners can order as takeout and pick up fills that capacity without filling seats, and diners pay no delivery fee. On FIG you choose which deals work as takeout, and you can pause takeout or add prep time when the kitchen gets busy. Diners pay for takeout in the app; FIG keeps 5% of the food, plus Stripe's card fee. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a>.</p>"""),
             ("7. Measure, keep, pause", """<p>Give each deal two weeks, then look at three numbers:</p>
<table><thead><tr><th>Number</th><th>What it tells you</th></tr></thead><tbody>
<tr><td>Claims</td><td>Is the deal interesting? Low claims: the deal or its photo isn't pulling.</td></tr>
<tr><td>Scans</td><td>Are people actually coming in? Many claims but few scans: the hours or the distance may be wrong.</td></tr>
<tr><td>Return diners</td><td>Is it building regulars? This is the number that pays off long after the deal.</td></tr>
</tbody></table>
<p>FIG's insights show views, claims, the diners who came in and who came back, per deal, day by day. Keep the deals that bring new people back. Pause the rest with one tap.</p>"""),
             ("A one-week plan", """<ol><li><strong>Monday:</strong> mark your quiet hours from last month's receipts.</li><li><strong>Tuesday:</strong> pick one dish with a healthy margin and write one specific deal for one quiet window.</li><li><strong>Wednesday:</strong> post it on FIG with a cap of 10 a day. Take a good photo.</li><li><strong>Thursday to Sunday:</strong> make sure every staff member knows the deal and how to scan.</li><li><strong>Two weeks later:</strong> check claims, scans and return diners. Adjust the hours, the dish or the cap.</li></ol>
<p>Setting up on FIG takes about 15 minutes. <a href="/blog/set-up-fig-menu-takeout">A 15-minute setup guide for your menu and takeout</a>.</p>"""),
         ],
         faq=[("What's the cheapest way to market a small restaurant?", "Aim a specific, capped deal at your quiet hours and put it where diners are deciding. On FIG, posting deals and scanning diners are free, with no fee per diner."),
              ("Will a deal hurt my margins?", "Not if it runs only in hours that would otherwise be empty and covers its food cost. Cap it per day so it can't cost more than planned."),
              ("What are the slowest hours for restaurants?", "For many, weekday afternoons (about 2 to 5 pm) and early weeknights. Check your own receipts by hour: every restaurant is different."),
              ("Should I offer a percentage off or 2-for-1?", "2-for-1 pulls hardest but costs the most per plate; a percentage off is gentler on margin. Run the numbers on your food cost first."),
              ("How do I know if a deal is working?", "Watch claims, scans and return diners for two weeks. FIG's insights show all three per deal."),
              ("Can I stop a deal anytime?", "Yes. Pause or end it with one tap, and the daily cap stops it automatically each day.")]),

    # York University Markham Campus (Markham Centre, opened Fall 2024): https://presidentsreport2023.yorku.ca/opening-the-doors-to-innovation/
    # Pacific Mall Heritage Town food court: https://en.wikipedia.org/wiki/Pacific_Mall
    # Ontario $4 prepared food point-of-sale rebate (GI-064): source at the top
    dict(slug="student-food-deals-markham", screen="claim", title="Student food deals in Markham: eating out on a budget", date="2026-10-04", updated="2026-11-05", topic="For diners", group="fig-in-markham",
         dek="How high school and university students in Markham can eat out for less: when deals show up, how to set a real budget, how to decide as a group, and how FIG keeps it free.",
         desc="How Markham students can eat out for less: when deals show up, setting a real budget, deciding as a group, and why FIG is free.",
         keywords="student food deals Markham, cheap eats for students, after school food Markham, budget restaurants Markham, bubble tea deals Markham, York University Markham food",
         points=["After school (about 3 to 6 pm) is when many restaurants are quiet, so it's when deals show up.",
                 "Set a budget filter in FIG once and only see deals you can afford.",
                 "Snacks and drinks of $4 or less have a smaller tax in Ontario: only the 5% GST part, not the full 13%.",
                 "Send a restaurant's link to the group chat so everyone agrees faster, and split the bill fairly.",
                 "FIG is free: no subscription, no ads for now, no card needed to claim a deal."],
         sections=[
             ("The short answer", """<p>Eat when restaurants are quiet, decide with a budget instead of a craving, and let the deals come to you. In Markham that usually means after school and on weekday evenings, when many places post deals to fill empty tables. FIG puts every live deal near you on one map, filtered to your budget, and it's free.</p>"""),
             ("After school is deal time", """<p>Between lunch and dinner, many restaurants and bubble tea shops are at their quietest. That's exactly when owners post deals, and exactly when you get out of class. Late evenings are the other sweet spot for desserts and drinks.</p>
<p>For university students, Markham Centre on Highway 7 now has York University's Markham Campus, which opened in 2024, and Highway 7 is lined with plazas full of places to eat. High school students are rarely more than a short walk or bus ride from a plaza with a few options.</p>"""),
             ("Set a real budget", """<p>When you sign up, tell FIG what you crave and your budget. Home and the map then show deals that fit, nearest first, so you're not scrolling past $40 dinners. A few habits that stretch a budget further:</p>
<ul><li><strong>Pick the deal, then the place.</strong> Start from what's live and in budget, not from one restaurant you've already decided on.</li><li><strong>Share dishes.</strong> Two people sharing a 2-for-1 often eat more for less than two separate meals.</li><li><strong>Watch the add-ons.</strong> Drinks and extras are where a cheap meal stops being cheap.</li><li><strong>Look at takeout.</strong> Picking food up yourself means no delivery or service fees.</li></ul>
<div class="callout math"><b>A small tax tip for snacks</b><p>In Ontario, prepared food and drinks sold for $4 or less in total (before tax) get the 8% provincial part of the HST rebated at the till, so you pay only the 5% GST part. On a $3.80 drink, that's about $0.19 of tax instead of $0.49. It applies to the total of what you buy at one time, so it's for a single snack or drink, not a group order.</p></div>"""),
             ("Decide with your friends", """<p>Group plans fall apart over "where should we go?". Share a restaurant's link from FIG to your group chat: everyone sees the same place and its live deals. If the plan is six people at 5 pm, call the restaurant first to check there's room. <a href="/blog/group-dining-deals">How to eat out as a group, with deals</a>.</p>"""),
             ("Know your spots", """<p>A few areas worth knowing:</p>
<ul><li><strong>Pacific Mall</strong> at Steeles and Kennedy, with its own food court and market, Heritage Town.</li><li><strong>Highway 7</strong> and Markham Centre, near the York campus.</li><li><strong>Main Street Unionville</strong>, for a sit-down treat.</li><li><strong>Your local plaza.</strong> Many of the best cheap eats in Markham are in plazas you walk past every day.</li></ul>
<p>More in our <a href="/blog/restaurant-deals-markham">guide to restaurant deals in Markham</a>.</p>"""),
             ("How it works at the counter", """<ol><li>Claim the deal in FIG. It waits on your Deals page for as long as the deal runs.</li><li>At the restaurant, tap Show QR. Staff scan it.</li><li>The deal comes off your bill. You pay the restaurant like normal.</li></ol>
<p>You don't need a credit card to claim a deal. A code works once, so a screenshot from a friend won't help: everyone claims their own.</p>"""),
             ("Free is the point", """<p>FIG is free for every diner. There's nothing to subscribe to, no points to collect and no ads for now. Restaurants use FIG for free, and nothing is charged per diner. FIG is open to diners in Markham now.</p>"""),
             ('A week of eating out on $40', '<div class="callout math"><b>An example week (your prices will vary)</b><table><thead><tr><th>Day</th><th>Plan</th><th>Cost with 13% HST</th></tr></thead><tbody>\n<tr><td>Monday</td><td>A $3.50 drink after school (taxed at 5% under $4)</td><td>$3.68</td></tr>\n<tr><td>Tuesday</td><td>A $14 bowl with a $3-off deal</td><td>$12.43</td></tr>\n<tr><td>Thursday</td><td>2-for-1 with a friend: you each pay half of one $15 dish</td><td>$8.48</td></tr>\n<tr><td>Saturday</td><td>A $12 lunch with 15% off</td><td>$11.53</td></tr>\n<tr><td colspan="2"><strong>Total</strong></td><td><strong>$36.12</strong></td></tr>\n</tbody></table><p>Four meals out for under $40, by choosing the deal first. Without the deals, the same food would be about $50.</p></div>'),
             ('Diets and allergies', "<p>Set your diet in FIG (halal, vegetarian, vegan, gluten-free and more) and the places that don't fit drop out of your results. For allergies, filters are a starting point, not a guarantee: call the restaurant before you go, or tell staff when you order. Kitchens share equipment, and only they know exactly what's in a dish.</p>"),
             ('Staying safe and private', '<ul><li>Restaurants see your first name and last initial, never your phone number or email.</li><li>Your claimed deal only works on your phone, so nobody can use it for you.</li></ul>'),
         ],
         faq=[("Is FIG free for students?", "Yes. FIG is free for every diner, with no subscription and no ads for now."),
              ("Do I need a credit card?", "Not to claim a deal. You claim it in the app and pay the restaurant at the counter. Takeout paid in the app needs a card."),
              ("When are student food deals most common?", "In restaurants' quiet hours: after school, roughly 3 to 6 pm, and late evenings for desserts and drinks."),
              ("Can my friends use my code?", "No. Each code belongs to the person who claimed it and works once. Everyone claims their own deal."),
              ("Is food under $4 really taxed less?", "In Ontario, yes: qualifying prepared food and drinks sold for $4 or less in total get the 8% provincial part of the HST rebated at the till, so only the 5% GST applies."),
              ("When can I start using FIG deals?", "Now. FIG is open to diners in Markham: check out deals at www.figpromo.ca/app, with no account needed to look around.")]),

    dict(slug="flash-deals-explained", screen="qr", title="What are flash deals, and how do they work on FIG?", date="2026-10-04", updated="2026-10-24", topic="For diners", group="eat-out-for-less",
         dek="Flash deals are short, real-time restaurant deals posted during unexpected quiet spells. Here's how they work for diners and restaurants, how to catch them, and what happens to a claim when the timer ends.",
         desc="Flash deals are short restaurant deals posted during quiet spells. How they work, how to catch one, and what happens to a claim when the timer ends.",
         keywords="flash deals restaurants, last minute restaurant deals, happy hour Markham, real time food deals, flash deal app",
         points=["A flash deal is a short deal a restaurant posts right now, usually for an hour or two, because it has a quiet spell.",
                 "The timer is set by the restaurant and it's real: when it ends, the deal is gone.",
                 "Live flash deals stand out on the map and on Home, with their timer, and the Flash deals filter shows only them.",
                 "A claimed flash deal works until the timer ends, then it expires. Expired claims never count against you.",
                 "Restaurants post one in seconds, with an optional cap."],
         sections=[
             ("The short answer", """<p>A flash deal is a short restaurant deal posted on the spot, because the restaurant has empty tables right now. It runs for a set time, usually an hour or two, with a real countdown. Claim it while it's live, head over, and show your code before the timer ends.</p>"""),
             ("Everyday deals vs flash deals", """<table><thead><tr><th></th><th>Everyday deal</th><th>Flash deal</th></tr></thead><tbody>
<tr><td>When it's posted</td><td>In advance</td><td>Right now</td></tr>
<tr><td>When it runs</td><td>Chosen days and hours, every week, once, or until a date</td><td>From now until the timer ends</td></tr>
<tr><td>Why</td><td>Hours that are usually quiet</td><td>A surprise quiet spell: rain, a cancellation, a slow lunch</td></tr>
<tr><td>Your claim</td><td>Works whenever the deal runs</td><td>Works until the timer ends</td></tr>
<tr><td>Where you see it</td><td>Home, the map, the restaurant's page</td><td>Top of Search, the map, the restaurant's page</td></tr>
</tbody></table>"""),
             ("How to catch one", """<p>Live flash deals stand out on the map and on Home, with their timer, and the Flash deals filter shows only them. Because they're short, the best way to catch them is to check FIG when you're already thinking about food, the same moment you'd open a group chat to ask "where should we eat?".</p>"""),
             ("Claim it, then go", """<ol><li>Tap the flash deal and Claim it. It's on your Deals page with the time left.</li><li>Head over. A claim doesn't need you to be anywhere in particular: you can claim from home.</li><li>At the counter, tap Show QR and let staff scan it.</li></ol>
<p>A code works once, so a screenshot of a used code can't be reused. If the timer runs out before you get there, the claim expires. It shows as Expired on your Deals page for a day, and it never counts against you.</p>"""),
             ("Are flash deals real?", """<p>Yes, and it's worth saying why. On FIG, the timer is the restaurant's own: the owner chose the deal and how long it runs, because they actually have the space. FIG doesn't invent urgency, and a flash deal isn't a fake countdown that resets tomorrow.</p>"""),
             ("For restaurant owners", """<p>Posting a flash deal takes a few seconds: pick the deal (a percentage off, a dollar amount off, 2-for-1 or something free), the length and an optional cap. There's no fee per deal or per scan. Good flash deals are:</p>
<ul><li><strong>Simple.</strong> One dish or one clear discount, readable at a glance.</li><li><strong>Short.</strong> Long enough for someone nearby to get there, short enough to stay special.</li><li><strong>Capped.</strong> So a sudden rush can't overwhelm the kitchen.</li><li><strong>Real.</strong> Post one when you genuinely have room, and diners learn to trust them.</li></ul>
<p>Check the math before you post: in a quiet spell, a deal only has to cover its food cost to add money. <a href="/blog/slow-hour-deal-math">Slow-hour deal math</a> · <a href="/#owners">How FIG works for restaurants</a></p>"""),
             ('The life of a flash deal', '<table><thead><tr><th>When</th><th>What happens</th></tr></thead><tbody>\n<tr><td>2:40 pm</td><td>A restaurant has a quiet afternoon and posts "$4 off any noodle bowl, for 90 minutes, 15 available".</td></tr>\n<tr><td>2:41 pm</td><td>It stands out on the map and on Home, and shows on the restaurant\'s page, with the time left.</td></tr>\n<tr><td>2:45 to 4:10 pm</td><td>Diners nearby claim it and head over. Each claim waits on their Deals page.</td></tr>\n<tr><td>At the counter</td><td>Staff scan each diner\'s code. $4 comes off.</td></tr>\n<tr><td>4:10 pm</td><td>The timer ends. The deal disappears, and any unused claims expire. If all 15 had been used first, it would have ended then.</td></tr>\n</tbody></table>\n<p>An example timeline: every restaurant chooses its own deal, length and cap.</p>'),
             ('Why restaurants have surprise quiet spells', "<p>A dining room can go quiet for reasons nobody planned: a downpour, a cancelled group booking, a slow day after a holiday weekend, a road closure out front. The kitchen is staffed and the food is prepped either way. A flash deal turns that spare capacity into diners, and because it's short and capped, it doesn't train people to wait for discounts.</p>"),
             ('Flash deal etiquette for diners', '<ul><li><strong>Claim it when you mean to go.</strong> Caps are small, and an unused claim may keep someone else out.</li><li><strong>Go promptly.</strong> The deal ends with the timer, wherever you are.</li><li><strong>Check dine-in or takeout</strong> before you set off.</li><li><strong>Like the deal</strong> afterwards if it was good: it tells the restaurant, and other diners, that it worked.</li></ul>'),
             ('Everyday or flash? For owners', '<table><thead><tr><th>Use an everyday deal when</th><th>Use a flash deal when</th></tr></thead><tbody>\n<tr><td>The same hours are quiet every week</td><td>Today is unexpectedly quiet</td></tr>\n<tr><td>You want regulars to know when to come</td><td>You want diners who are nearby right now</td></tr>\n<tr><td>You can plan the dish and the staffing</td><td>You have food and staff ready but empty seats</td></tr>\n</tbody></table>\n<div class="callout math"><b>Is a flash deal worth it?</b><p>A $15 bowl with a food cost of $4.50 still leaves $6.50 with $4 off. In an hour where those seats would sit empty, fifteen of them add up to $97.50 toward the shift\'s wages and rent, before any drinks. Use your own numbers. <a href="/blog/slow-hour-deal-math">The full slow-hour math</a>.</p></div>'),
         ],
         faq=[("How long do flash deals last?", "The restaurant sets the length, usually an hour or two. The timer you see in the app is the real one."),
              ("What happens if my flash deal runs out before I arrive?", "The claim expires when the timer ends. It shows as Expired on your Deals page for a day, then leaves the list, and it never counts against you."),
              ("Will FIG message me about flash deals?", "Not on its own. Check the map or Home, or turn on the Flash deals filter to see only them."),
              ("Do I have to be nearby to claim a flash deal?", "No. Deals are never locked to your location. Just make sure you can get there before the timer ends."),
              ("Can a restaurant post a flash deal for takeout?", "A restaurant chooses whether each deal is dine-in only or also takeout."),
              ("Do flash deals cost restaurants anything?", "No. Posting deals and scanning diners are free, with no fee per deal or per diner.")]),

    dict(slug="takeout-without-delivery-fees", screen="qr", title="Takeout with a deal, pick up, skip the delivery fees", date="2026-10-04", updated=UPDATED, topic="For diners", group="takeout-and-money",
         dek="Some FIG deals let you order takeout from a Markham restaurant's menu and pick it up yourself, with no delivery or service fees. Here's how it works, what it costs, and what happens if you're late.",
         desc="Some FIG deals let you order takeout from a Markham restaurant and pick it up yourself, with no delivery or service fees. How it works and what it costs.",
         keywords="takeout deals Markham, pickup deals, no delivery fees, takeout pickup Markham",
         points=["Tap Takeout on a deal that allows it, add what you want from the menu, and pick it up when it's ready.",
                 "No delivery fee and no service fee from FIG. You pay the menu price, minus the deal, plus tax.",
                 "Some restaurants also take takeout at full price: tap Order takeout on their page.",
                 "Tap I'm here when you arrive and show your pickup code. Orders close as Not picked up two hours after the pickup time.",
                 "FIG doesn't deliver. Restaurants never see your phone number."],
         sections=[
             ("The short answer", """<p>On FIG, takeout means you order from the restaurant's own menu, with a deal taken off, and pick it up yourself. There's no driver, so there's no delivery fee, and FIG doesn't add a service fee. You pay the menu price minus the deal, plus tax. The restaurant sees your order, you see when it's ready, and you collect it with a code.</p>"""),
             ("How it works", """<ol><li>Find a deal marked Dine in or takeout and tap Takeout. The menu opens with the deal applied. Some restaurants also take takeout at full price: tap Order takeout on their page.</li><li>Add the dishes you want. The deal comes off your order, and you can add other dishes too.</li><li>Send it. The restaurant accepts it, and you can follow your order until it's ready.</li><li>Head over and tap I'm here when you arrive.</li><li>Show your pickup code so staff can scan it. That's it.</li></ol>"""),
             ("What you pay, and what you don't", """<div class="callout math"><b>Example: a $24 order with a $4-off deal</b><ul><li>Food: $24.00, minus the $4.00 deal: $20.00.</li><li>HST at 13%: $2.60.</li><li>You pay: $22.60.</li><li>Delivery fee: none. Service fee from FIG: none.</li></ul><p>Tax is charged on the price after the restaurant's own discount, the way a store coupon works.</p></div>
<p>You pay in the app when you order. The payment goes to the restaurant through Stripe, and the receipt names the restaurant as the seller, with its HST number.</p>"""),
             ("Why pickup is cheaper", """<p>Delivery has real costs (a driver, the distance, the platform), and somebody pays them: usually the diner through fees and the restaurant through a commission. Uber Eats and DoorDash publish Canadian delivery commissions of 20% to 30% for restaurants. When you pick up, none of that applies. <a href="/blog/delivery-app-commissions-vs-fig">What restaurants keep on each</a>.</p>"""),
             ("It starts with a deal", """<p>Only deals the restaurant allows as takeout have the button; dine-in only deals are for eating in. Restaurants can also limit how many deals one order can use, and some offer takeout at full price with no deal needed. If the kitchen gets busy, a restaurant can pause takeout or add prep time, and you'll see it before you order.</p>"""),
             ("If something changes", """<ul><li><strong>The restaurant needs you.</strong> They can mark that they're waiting. You'll see it on your order.</li><li><strong>You need to change something.</strong> Call the restaurant.</li><li><strong>You're running late.</strong> Tap I'm here when you arrive so it never counts as missed.</li><li><strong>You can't make it.</strong> Two hours after the pickup time, the order closes as Not picked up. Nothing gets switched off, but a missed pickup shows on your takeout record, and restaurants see it.</li></ul>"""),
             ("Private by default", """<p>The restaurant sees your first name and last initial, never your phone number or email.</p>"""),
             ('Your first takeout order, step by step', "<ol><li><strong>Pick the deal.</strong> On Home or the map, look for deals marked Dine in or takeout. Open one and check the days, hours and which dishes it's on.</li><li><strong>Tap Takeout.</strong> The restaurant's menu opens in sections, with the deal already applied to the dishes it covers.</li><li><strong>Build your order.</strong> Add the deal dish and anything else you want. The deal comes off; other dishes are full price.</li><li><strong>Check the pickup time.</strong> If the restaurant has added prep time because it's busy, you'll see it here, before you pay.</li><li><strong>Pay in the app.</strong> Your card is charged for the food after the deal, plus tax. The receipt names the restaurant as the seller.</li><li><strong>Follow the order.</strong> You'll see when the restaurant accepts it and when it's ready.</li><li><strong>Arrive and tap I'm here.</strong> Then show your pickup code at the counter so staff can scan it.</li><li><strong>Check the bag</strong> before you leave, and enjoy it while it's hot.</li></ol>"),
             ('Takeout, delivery or dine-in?', "<table><thead><tr><th></th><th>Takeout on FIG</th><th>Delivery app</th><th>Dine-in with a FIG deal</th></tr></thead><tbody>\n<tr><td>Who brings the food</td><td>You pick it up</td><td>A driver</td><td>Your server</td></tr>\n<tr><td>Delivery or service fee</td><td>None from FIG</td><td>Set by the app</td><td>None from FIG</td></tr>\n<tr><td>How you pay</td><td>In the app</td><td>In the app</td><td>At the counter, as usual</td></tr>\n<tr><td>Deal</td><td>If the deal allows takeout</td><td>The app's own promotions</td><td>Any live deal</td></tr>\n<tr><td>Best when</td><td>You're nearby and want to eat at home</td><td>You can't go out</td><td>You want the full experience</td></tr>\n</tbody></table>"),
             ('Tips for great pickups', '<ul><li><strong>Order in quiet hours.</strong> That\'s when takeout deals run, and when kitchens are fastest.</li><li><strong>Order when you\'re ready to leave.</strong> Food is best right when it\'s made.</li><li><strong>Call for changes.</strong> Allergies, no onions, extra sauce: call the restaurant right after you order.</li><li><strong>Ordering for a group?</strong> One person orders and picks up, then everyone settles up. <a href="/blog/group-dining-deals">Splitting the bill fairly</a>.</li></ul>'),
             ('What restaurants see', "<p>Restaurants see your order, the pickup time, your first name and last initial, and whether you've tapped I'm here. They don't see your phone number, email or card details: payments go through Stripe. A record of missed pickups is the one thing that follows you, which is why tapping I'm here when you arrive matters.</p>"),
         ],
         faq=[("Does FIG deliver?", "No. You order takeout and pick the food up yourself."),
              ("Is there a fee for takeout on FIG?", "Not for diners: no delivery fee and no service fee. You pay the menu price, minus the deal, plus tax."),
              ("Do I pay in the app or at the counter?", "For takeout, in the app when you order: the payment goes to the restaurant through Stripe. For dine-in deals, you pay at the counter as usual."),
              ("What if I'm late for my pickup?", "Tap I'm here when you arrive. Two hours after the pickup time, an order that wasn't picked up closes as Not picked up and shows on your takeout record."),
              ("Can I order takeout without a deal?", "Some restaurants take takeout at full price: tap Order takeout on their page."),
              ("Does the restaurant get my phone number?", "Not from FIG. Restaurants see your first name and last initial on your order.")]),

    # ---------------------------------------------------------------- the first batch of new posts (user 2026-10-14: "just post it";
    # the review gate is gone: a post without publish_at is live, and the admin page can hide one later)

    dict(slug="how-restaurant-deals-work", screen="claim", title="How restaurant deals work on FIG, from claim to counter", date="2026-10-14", updated="2026-11-05", topic="For diners", group="eat-out-for-less",
         dek="Everything that happens between seeing a deal and paying the bill: claiming, your Deals page, the code at the counter, takeout, what happens when a deal ends, and rating the visit.",
         desc="From seeing a deal to paying the bill: claiming, your Deals page, the code at the counter, takeout, when a deal ends, and rating the visit.",
         keywords="how restaurant deals work, claim restaurant deal, restaurant deal app how to, FIG voucher, QR code restaurant deal",
         points=["Find a deal on Home, the map or a restaurant's page, and tap Claim. It waits on your Deals page.",
                 "A claim has no time limit: it works for as long as the deal runs.",
                 "At the counter, tap Show QR and staff scan it. The deal comes off your bill.",
                 "A code works once, so a screenshot of a used code just says already used and nobody can reuse your deal.",
                 "After a scanned visit you can rate the restaurant, and like the deal. FIG is free for diners."],
         sections=[
             ("The short answer", """<p>On FIG, a restaurant deal works in four steps: you find a deal, claim it in one tap, show your code at the restaurant, and the deal comes off your bill. You pay the restaurant the way you always do. There's no card to add for dine-in, no points to collect and no fee: FIG is free for diners.</p>"""),
             ("Step 1: Find a deal", """<p>Deals show up in three places:</p>
<ul><li><strong>Home</strong>, nearest first, filtered by what you crave, your budget and your diet.</li><li><strong>The map</strong>, where you choose how far you'll go: 1, 2, 5 or 10 km.</li><li><strong>A restaurant's page</strong>, alongside its menu, hours, photos and reviews.</li></ul>
<p>Every deal shows what it is, when it runs and whether it's dine-in only or also takeout. Some deals are on the whole order; others are on specific dishes, which you'll see on the menu.</p>"""),
             ("Step 2: Claim it", """<p>Tap Claim on the deal, then Claim deal. It waits on your Deals page. A claim doesn't time out: it works for as long as the deal runs. You don't need to be near the restaurant to claim, and you don't need to go right away.</p>
<div class="callout tip"><b>When does a claim end?</b><p>Only when the restaurant ends the deal, or when a flash deal's timer or a dated deal is over. Then it shows as Expired on your Deals page for a day and leaves the list. Expired claims never count against you.</p></div>"""),
             ("Step 3: At the restaurant", """<p>Order as usual and, when it's time to pay, open your Deals page and tap Show QR. Staff scan it with the restaurant side of FIG.</p>
<p>If a camera won't cooperate, there's a short code staff can type instead. Either way, the deal comes off the bill and you pay the restaurant directly.</p>
<p>A code works once. That's what makes deals safe: after staff scan it, it's used, and a screenshot of it just says already used. If the restaurant lets a deal be used more than once, your screen shows a new code after each scan.</p>"""),
             ("Step 4: Rate the visit", """<p>Once your visit is scanned, you can rate the restaurant: tap Rate this visit, or find it later under Past visits on your Deals page. Pick the stars and add a few words or a photo if you like. One review per visit, and it shows your first name and last initial.</p>
<p>Deals get likes, restaurants get stars. Only diners whose visit was scanned can review, so every review on FIG comes from a real meal. <a href="/blog/how-to-read-restaurant-reviews">How to read a restaurant's reviews</a>.</p>"""),
             ("Takeout works too", """<p>If a deal is marked Dine in or takeout, tap Takeout instead: the restaurant's menu opens with the deal applied, you add what you want, and you pick it up. Tap I'm here when you arrive and show your pickup code. No delivery or service fees. <a href="/blog/takeout-without-delivery-fees">How takeout works</a>.</p>"""),
             ("Questions before you go", """<p>Not sure if there's room for six, or whether the deal works with the lunch special? Call the restaurant before you go. <a href="/blog/group-dining-deals">Going as a group?</a></p>"""),
             ("What FIG doesn't do", """<ul><li>Charge you anything, or show you ads.</li><li>Lock deals to where you are. Use them wherever you happen to be.</li><li>Rush you. No fake countdowns: a flash deal's timer is the restaurant's real one.</li><li>Share your phone number with restaurants.</li></ul>"""),
         ],
         faq=[("Do I need to pay in the app?", "Not for dine-in. You show your code and pay the restaurant as usual. Takeout is paid in the app when you order."),
              ("How long is a claimed deal good for?", "As long as the deal runs. It ends only when the restaurant ends the deal, or a flash or dated deal is over."),
              ("Can I screenshot my code?", "It won't help. A code works once, so a screenshot of a used code just says already used."),
              ("Can I use a deal more than once?", "Once per person per day, whether you use it at the counter or order takeout with it. The restaurant also caps how many are used each day."),
              ("Who can review a restaurant?", "Only diners whose visit was scanned, so every review comes from a real visit."),
              ("Is FIG free?", "Yes, for every diner: no subscription, no fees and no ads for now.")]),

    # StatCan 2023 margin 3.6%; food cost 28-32% (Resy): sources at the top
    dict(slug="slow-hour-deal-math", screen="tdash", title="How to run a slow-hour deal that makes money (with the math)", date="2026-10-14", updated="2026-10-24", topic="For restaurants", group="fill-quiet-hours",
         dek="A slow-hour deal makes money when it fills seats that would otherwise be empty and covers its food cost. Here's the arithmetic: contribution per plate, the worst case, the cap, and how to tell new diners from regulars who'd have come anyway.",
         desc="A slow-hour deal makes money when it fills empty seats and covers its food cost. The math: contribution per plate, the worst case and the daily cap.",
         keywords="happy hour deal restaurant profit, slow hour promotion, restaurant deal math, restaurant discount profitability, off-peak restaurant deals",
         points=["In an hour that would be empty, a deal only needs to cover its food cost to add money: rent and wages are paid either way.",
                 "Contribution per plate = what the diner pays minus the food cost. Work it out before you post.",
                 "Worst case = cap × the discount on diners who'd have paid full price anyway. Size the cap to a worst case you're fine with.",
                 "Run deals only in your quiet windows; at peak hours the same deal just gives money away.",
                 "Judge a deal by new and returning diners, not just claims."],
         sections=[
             ("The short answer", """<p>A slow-hour deal makes money when two things are true: it fills seats that would otherwise be empty, and what the diner pays is more than the food on their plate costs you. Because rent, wages and the lights are paid whether the room is full or not, a deal in a genuinely empty hour adds money as long as it covers its food cost. The risk is the diner who would have come anyway at full price. A daily cap limits that risk to a number you choose.</p>"""),
             ("Why the empty hour changes the math", """<p>Restaurant margins in Canada are thin: Statistics Canada reported a 3.6% operating profit margin for food services and drinking places in 2023, the lowest since 2003. With margins like that, a discount at full-price hours is expensive. But most of a restaurant's costs are fixed for the shift. In a quiet hour, the question isn't "is this deal profitable on its own?" but "does this deal leave me better off than an empty table?".</p>"""),
             ("Contribution per plate", """<p>Contribution is what's left from a sale after the cost of the food on the plate. It's the money that goes toward wages, rent and profit.</p>
<div class="callout math"><b>A $15 noodle bowl</b><p>Food cost at 30% of the menu price (the industry average is 28% to 32%): $4.50.</p><table><thead><tr><th>Deal</th><th>Diner pays</th><th>Food cost</th><th>Contribution</th></tr></thead><tbody>
<tr><td>No deal</td><td>$15.00</td><td>$4.50</td><td>$10.50</td></tr>
<tr><td>15% off</td><td>$12.75</td><td>$4.50</td><td>$8.25</td></tr>
<tr><td>$4 off</td><td>$11.00</td><td>$4.50</td><td>$6.50</td></tr>
<tr><td>2-for-1 (two bowls)</td><td>$15.00</td><td>$9.00</td><td>$6.00 for two</td></tr>
<tr><td>Empty table</td><td>$0</td><td>$0</td><td>$0</td></tr>
</tbody></table><p>Every deal above beats the empty table. Use your own menu price and food cost: these are round example numbers.</p></div>"""),
             ("The worst case, and how a cap controls it", """<p>The real cost of a deal is the discount you give to diners who would have paid full price anyway. You can't know exactly who they are, so plan for the worst case:</p>
<div class="callout math"><b>Worst case = daily cap × discount</b><ul><li>A $4-off deal capped at 15 a day: at worst, $60 a day of discount to people who'd have come anyway.</li><li>The same deal with no cap on a busy day: no limit.</li></ul><p>Pick a cap whose worst case you'd shrug at. On FIG, the daily cap stops the deal automatically once it's been used that many times.</p></div>
<p>And the upside: if even a third of those 15 diners are new, and one or two become regulars, the deal is paying off long after it ends.</p>"""),
             ("Add-ons: where a deal earns", """<p>Diners who come in for a deal often order something else: a drink, a side, a dessert. That extra order is usually full price.</p>
<div class="callout example"><b>Example: a deal plus a drink</b><p>Take the 15%-off bowl above ($8.25 contribution) and suppose the diner adds a $5 drink that costs you $1.25 to make (use your own numbers). The table now contributes $8.25 + $3.75 = $12.00, more than a full-price bowl alone. A deal on the main dish with drinks at full price is a classic shape for this reason.</p></div>"""),
             ("Pick the window", """<ol><li>Look at sales by hour for the last four weeks.</li><li>Find the windows where you're under, say, a third full: often weekday afternoons and early weeknights.</li><li>Run the deal only there. On FIG, a deal can run on chosen days and hours, with different hours for different days.</li></ol>
<p>The same 2-for-1 that fills a Tuesday at 3 pm would give away a full bowl per table at 7 pm on a Saturday.</p>"""),
             ("New diners vs regulars", """<p>A deal that only discounts your regulars is a price cut, not marketing. Watch who it brings in:</p>
<ul><li><strong>Claims</strong> tell you if the deal is interesting.</li><li><strong>Scans</strong> tell you if people actually come.</li><li><strong>Return visits</strong> tell you if it's building regulars.</li></ul>
<p>FIG's insights show views, claims, the diners who came in and who came back, per deal, day by day. If most scans are your usual faces, change the dish, the hours or the deal.</p>"""),
             ("A checklist before you post", """<ul><li>Does the diner's price cover the food cost, with room to spare?</li><li>Is it only in hours you're actually quiet?</li><li>Is the cap's worst case a number you're fine with?</li><li>Is it specific: a dish, a time, a price?</li><li>Do all staff know it and how to scan?</li><li>Have you set a date to check claims, scans and return diners?</li></ul>
<p>On FIG, posting deals and scanning diners are free, with no fee per diner. <a href="/blog/deal-types-percent-dollar-2-for-1">Next: % off, $ off or 2-for-1?</a></p>"""),
         ],
         faq=[("Do restaurant discounts actually make money?", "They can, when they fill otherwise empty seats and the diner's price covers the food cost. At busy hours, the same discount mostly gives money to diners who'd have paid full price."),
              ("What food cost should I assume?", "Use your own. As a reference, the average food cost is often quoted at 28% to 32% of revenue."),
              ("How big should my daily cap be?", "Big enough to matter, small enough that the worst case (cap × discount) is a number you're comfortable with. Start small and raise it."),
              ("Should drinks be part of the deal?", "Often not: a deal on the main dish with drinks at full price lets add-ons do the earning."),
              ("How do I know if new people are coming?", "Watch scans and return visits per deal. FIG's insights show the diners who came in and who came back."),
              ("Does FIG take a cut of dine-in deals?", "No. Posting deals and scanning diners are free, with no fee per diner.")]),

    # CRA: a store coupon reduces the price before GST/HST (RC4022): source at the top
    dict(slug="deal-types-percent-dollar-2-for-1", screen="tdash", title="% off, $ off or 2-for-1? Pricing a restaurant deal", date="2026-10-14", topic="For restaurants", group="fill-quiet-hours",
         dek="The four kinds of restaurant deal, side by side: what each costs you, what it feels like to a diner, and when to use it. With worked examples on a $14 dish.",
         desc="The four kinds of restaurant deal side by side: what each costs you, how it feels to a diner and when to use it, worked on a $14 dish.",
         keywords="percent off vs dollar off, 2 for 1 deal restaurant, BOGO restaurant, restaurant promotion ideas, restaurant deal pricing",
         points=["% off scales with the bill: gentle on small orders, generous on big ones. Cap it for takeout.",
                 "$ off feels bigger on cheap items and costs you a fixed, predictable amount.",
                 "2-for-1 pulls hardest and costs the most per plate. Best for groups and quiet hours.",
                 "Something free with an order costs you its food cost, while the diner values it at its menu price.",
                 "Tax is charged on the price after your own discount, the way a store coupon works."],
         sections=[
             ("The short answer", """<p>There's no best deal type, only the best one for the job. A percentage off scales with the bill. A dollar amount off is predictable. 2-for-1 is the strongest pull and the most expensive per plate. Something free with an order often gives the most perceived value for the least cost. Pick by the hour you're filling and the dish, then check the numbers.</p>"""),
             ("The four types on FIG", """<p>On FIG a deal can be any of these, on the whole order or on specific dishes from your menu:</p>
<ul><li><strong>Percentage off</strong>, e.g. 20% off.</li><li><strong>Dollar amount off</strong>, e.g. $3 off.</li><li><strong>2-for-1</strong>: buy one, get one.</li><li><strong>Something free</strong> with an order, e.g. a free drink with any bowl.</li></ul>"""),
             ("Side by side on a $14 dish", """<div class="callout math"><b>A $14 ramen, food cost $4.20 (30%)</b><table><thead><tr><th>Deal</th><th>Diner saves</th><th>Diner pays</th><th>Your contribution</th></tr></thead><tbody>
<tr><td>Full price</td><td>$0</td><td>$14.00</td><td>$9.80</td></tr>
<tr><td>20% off</td><td>$2.80</td><td>$11.20</td><td>$7.00</td></tr>
<tr><td>$3 off</td><td>$3.00</td><td>$11.00</td><td>$6.80</td></tr>
<tr><td>2-for-1 (two bowls)</td><td>$14.00</td><td>$14.00 for two</td><td>$5.60 for two</td></tr>
<tr><td>Free $5 drink that costs you $1.25</td><td>$5.00</td><td>$14.00</td><td>$8.55</td></tr>
</tbody></table><p>Round example numbers: use your own menu prices and food costs. Contribution is what the diner pays minus the food cost.</p></div>
<p>Notice the last row: the diner saves the most money of the single-dish deals, and you keep the most. That's the quiet strength of "free with an order": the diner values the item at its menu price, and you pay its food cost.</p>"""),
             ("Percentage off", """<p><strong>Good for:</strong> deals on the whole order, groups and higher-priced menus. It feels fair at any size.</p>
<p><strong>Watch out for:</strong> large takeout orders, where 20% of a big order is a lot. On FIG you can set the most one takeout order can take off, so a percentage deal can't run away on a $150 order.</p>"""),
             ("Dollar amount off", """<p><strong>Good for:</strong> single dishes and lower prices. "$3 off any bowl" reads bigger than "20% off" on a $14 bowl, and it costs you exactly $3 every time.</p>
<p><strong>Watch out for:</strong> very cheap items, where $3 can be most of the margin. Put it on dishes with room.</p>"""),
             ("2-for-1", """<p><strong>Good for:</strong> bringing in pairs and groups in your quietest hours. It's the easiest deal to share in a group chat.</p>
<p><strong>Watch out for:</strong> peak hours (it halves the price of a table you'd have filled anyway) and dishes with a high food cost. Cap it daily.</p>"""),
             ("Something free with an order", """<p><strong>Good for:</strong> low-cost, high-value extras: a drink, a dessert, a side. It also introduces diners to something they'd never have ordered.</p>
<p><strong>Watch out for:</strong> extras with a high food cost, or a free item so big that it competes with the main dish.</p>"""),
             ("How tax works on a deal", """<p>In Ontario, HST is calculated on what the diner actually pays after your own discount, the same way a store's coupon reduces the price before tax. On a $14 dish with $3 off, HST at 13% is charged on $11.00: $1.43, not $1.82. If you're registered, the HST you remit follows the discounted price. (This is general information, not tax advice: ask your accountant about your situation.) <a href="/blog/hst-registration-small-restaurants-ontario">HST registration for small restaurants</a>.</p>"""),
             ("Which one should you pick?", """<table><thead><tr><th>Your goal</th><th>Try</th></tr></thead><tbody>
<tr><td>Fill a dead afternoon with pairs and groups</td><td>2-for-1, capped</td></tr>
<tr><td>Get people to try one dish</td><td>$ off that dish</td></tr>
<tr><td>Bigger orders, takeout</td><td>% off, with a most-off limit</td></tr>
<tr><td>Feel generous, protect margin</td><td>Something free with an order</td></tr>
<tr><td>A surprise quiet hour</td><td>A <a href="/blog/flash-deals-explained">flash deal</a> with any of the above</td></tr>
</tbody></table>
<p>Whatever you pick, run it in your quiet windows, cap it, and judge it by new and returning diners. <a href="/blog/slow-hour-deal-math">The slow-hour math</a>.</p>"""),
         ],
         faq=[("Is % off or $ off better?", "$ off reads bigger on cheaper dishes and costs a fixed amount; % off scales with the bill and suits whole orders. Run both on your own prices."),
              ("Is 2-for-1 a good idea for a restaurant?", "In quiet hours, for pairs and groups, it can be: it pulls hardest. It costs the most per plate, so cap it and keep it away from peak hours."),
              ("Why offer something free instead of a discount?", "The diner values the free item at its menu price; you pay only its food cost. It often feels generous while keeping more margin."),
              ("Is HST charged before or after the discount?", "After your own discount: HST is calculated on what the diner actually pays, the way a store coupon reduces the price before tax."),
              ("Can I put a deal on specific dishes?", "Yes. A FIG deal can apply to the whole order or to specific dishes from your menu."),
              ("Can I limit a percentage deal on big takeout orders?", "Yes. You can set the most one takeout order can take off.")]),

    # Stripe 2.9% + CA$0.30: source at the top. HST number format 123456789 RT 0001 (9-digit BN, RT = GST/HST program, 4-digit
    #   reference): https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/rc4022/general-information-gst-hst-registrants.html
    dict(slug="set-up-fig-menu-takeout", screen="tscanner", title="Set up your FIG menu and takeout in 15 minutes", date="2026-10-14", updated="2026-10-25", topic="For restaurants", group="fill-quiet-hours",
         dek="A step-by-step guide for restaurant owners: your page, your menu, your first deal, and in-app takeout with your HST number and Stripe payouts, explained simply.",
         desc="A step-by-step guide for owners: your page, your menu, your first deal, and in-app takeout with your HST number and Stripe payouts.",
         keywords="FIG restaurant setup, restaurant menu app, set up takeout restaurant, Stripe payouts restaurant, HST number restaurant app",
         points=["Sign up as a business, then follow the Get FIG ready checklist on your dashboard: it ticks itself as you go.",
                 "Build your menu in sections, then dishes and prices. Nothing changes for diners until you tap Publish changes.",
                 "Post one specific, capped deal for a quiet window. Posting deals and scanning diners are free.",
                 "In-app takeout needs your HST number and Stripe payouts, both in Settings → Get paid. Dine-in deals need neither.",
                 "During a rush, pause takeout or add prep time in one tap."],
         sections=[
             ("The short answer", """<p>Setting up on FIG takes about 15 minutes if you have your menu handy: sign up as a business, add your sections, dishes and prices, and draft one deal for a quiet window. Everything stays a draft until you connect Stripe, which checks your ID and bank account in about 5 minutes; then you publish. If you want diners to pay for takeout in the app, add your HST number and connect Stripe for payouts in Settings → Get paid. Everything is free, except that in-app takeout costs 5% of the food plus Stripe's card fee.</p>"""),
             ("Before you start: have these ready", """<ul><li>Your menu (paper, a PDF or a photo) with prices.</li><li>Two or three good photos of your food and room.</li><li>Your opening hours.</li><li>For in-app takeout only: your HST number (it looks like 123456789 RT 0001) and your bank details for Stripe.</li></ul>"""),
             ("Minutes 0 to 3: sign up and follow the checklist", """<p>Sign up as a business with your restaurant's name and address. Your dashboard shows a <strong>Get FIG ready</strong> checklist with one button per step. Each step ticks itself when it's done, from your real data, and you can hide the checklist for good once you're set. Quick tours point out the important buttons the first time you open a screen.</p>"""),
             ("Minutes 3 to 10: your menu", """<ol><li><strong>Sections first.</strong> Starters, Mains, Noodles, Drinks: however your paper menu is organised.</li><li><strong>Dishes and prices.</strong> Type prices the way you like: "15.50", "15,50" and "$15.50" all work.</li><li><strong>Publish.</strong> Your edits are kept while you work, and the button says Publish changes until you tap it. Nothing changes for diners before that, and if you close the tab with unpublished changes, FIG asks first.</li></ol>
<p>Publishing is all or nothing: if one line has a problem, nothing changes and FIG tells you which line. Dishes keep their place in your deals and open orders when you edit them.</p>
<p>Out of something tonight? Mark a dish sold out for today, and it's back tomorrow.</p>"""),
             ("Minutes 10 to 13: your first deal", """<p>Pick one dish with a healthy margin and one quiet window, and write it plainly: "$3 off any noodle bowl, Monday to Thursday, 2 to 5 pm". Set a daily cap (10 is a good start) and choose dine-in only or takeout too. That's it: it's live on the map for nearby diners. <a href="/blog/deal-types-percent-dollar-2-for-1">Which deal type to pick</a>.</p>"""),
             ("Minutes 13 to 15: how you'll scan", """<p>Diners show a QR code; staff scan it with the restaurant side of FIG on any phone, tablet or computer, or type the short code if a camera won't cooperate. There's no fee per scan or per diner.</p>"""),
             ("Takeout: two ways to run it", """<table><thead><tr><th></th><th>What you need</th><th>What it costs</th></tr></thead><tbody>
<tr><td>Dine-in deals only</td><td>Nothing more</td><td>Free</td></tr>
<tr><td>Takeout, paid in the app</td><td>Your HST number + Stripe payouts (Settings → Get paid)</td><td>5% of the food + Stripe's 2.9% + $0.30</td></tr>
</tbody></table>
<p>You decide which deals work as takeout and how many deals one order can use. Some restaurants also take takeout at full price, with no deal needed.</p>"""),
             ("In-app payments, explained simply", """<p><strong>Step 1: your HST number.</strong> It goes on every takeout receipt, with your restaurant as the seller. FIG checks its format as you type. Not registered for HST? You can still post deals and scan diners; takeout waits until you have a number. <a href="/blog/hst-registration-small-restaurants-ontario">HST registration for small restaurants</a>.</p>
<p><strong>Step 2: Stripe payouts.</strong> FIG uses Stripe, a payments company, to take diners' cards and pay you. Stripe asks for your business details and bank account in its own secure setup. When it's done, Get paid shows Ready.</p>
<div class="callout math"><b>What a $30 in-app takeout pays you</b><ul><li>The diner pays $33.90 ($30.00 + 13% HST).</li><li>Stripe's fee: 2.9% of $33.90 + $0.30 = $1.28.</li><li>FIG's fee: 5% of $30.00 = $1.50.</li><li>Paid out to you: $31.12, including the $3.90 HST you remit.</li></ul></div>
<p>Each month's takeout statement shows sales, HST, fees and what you kept.</p>"""),
             ("When it gets busy", """<p>Takeout is for your quiet hours, not your rush. In one tap you can <strong>pause takeout</strong> (for a set time, or until tomorrow) or <strong>add prep time</strong> so pickup times stay honest. Diners see it before they order. Turn takeout off entirely whenever you like.</p>"""),
             ("After setup", """<ul><li>Reply to reviews in public. Only diners whose visit was scanned can leave one.</li><li>Check your insights after two weeks: claims, scans, and who came back.</li></ul>
<p>Questions? <a href="/help">Restaurant help</a> or <a href="/contact">message us</a>.</p>"""),
         ],
         faq=[("How long does it take to set up FIG?", "About 15 minutes with your menu handy: sign up, add your menu and draft one deal. To publish, connect Stripe (about 5 minutes, with your ID and a bank account). In-app takeout adds your HST number."),
              ("Do I need an HST number to use FIG?", "Not for deals and scanning. You need one, with Stripe payouts, for takeout, which diners pay for in the app."),
              ("What does it cost?", "Nothing to set up, go live, post deals or scan, for all your restaurants (up to 2 for now). In-app takeout costs 5% of the food plus Stripe's card fee."),
              ("What if we're too busy for takeout?", "Pause takeout for a while or until tomorrow, or add prep time, in one tap.")]),

    # CRA small supplier ($30,000 over four consecutive quarters, or in a single quarter; register within 29 days):
    #   https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/when-register-charge.html
    # Voluntary registration (charge, collect and remit; file returns; claim ITCs; stay registered at least one year):
    #   https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/account-register-voluntarily.html
    # Ontario HST 13% and the $4 prepared food point-of-sale rebate (GI-064); coupons before tax (RC4022); BN format (RC4022):
    #   sources at the top
    dict(slug="hst-registration-small-restaurants-ontario", screen="tdash", title="HST registration for small restaurants in Ontario: the $30,000 rule explained", date="2026-10-14", topic="For restaurants", group="takeout-and-money",
         dek="When a small Ontario restaurant has to register for HST, what changes when it does, and how HST works on deals and takeout. Plain-language, with the Canada Revenue Agency's own rules linked.",
         desc="When a small Ontario restaurant must register for HST, what changes when it does, and how HST works on deals and takeout, with CRA's rules linked.",
         seo="HST registration for small Ontario restaurants: $30,000 rule",
         keywords="HST registration small business Ontario, small supplier $30,000, restaurant HST Ontario, GST/HST number restaurant, input tax credits restaurant",
         points=["You're a small supplier while your taxable sales stay at $30,000 or less over four consecutive calendar quarters. Above that, you must register.",
                 "If you pass $30,000 in a single quarter, you must start charging HST on the sale that takes you over.",
                 "You can register voluntarily before then: you'd charge HST, file returns and claim input tax credits, and stay registered at least a year.",
                 "Ontario HST is 13%. Prepared food and drinks of $4 or less in one sale get the 8% provincial part rebated at the till.",
                 "On FIG, deals and scans work without an HST number; takeout needs one, and it goes on every receipt."],
         sections=[
             ("The short answer", """<p>In Canada, a business must register for GST/HST once its taxable sales go over $30,000 in four consecutive calendar quarters, or in a single quarter. Below that, it's a "small supplier" and registration is optional. In Ontario, a registered restaurant charges 13% HST on most meals and remits it to the Canada Revenue Agency (CRA), and can claim back the HST it paid on business costs. This guide explains the rules in plain language. It's general information, not tax advice: your accountant knows your situation.</p>"""),
             ("Am I a small supplier?", """<p>The CRA's test looks at your taxable sales (worldwide, including those of associated businesses) over a rolling year:</p>
<table><thead><tr><th>Your sales</th><th>What it means</th></tr></thead><tbody>
<tr><td>$30,000 or less over the last four consecutive calendar quarters</td><td>You're a small supplier. Registering is optional.</td></tr>
<tr><td>Over $30,000 across four consecutive quarters, but not in one</td><td>You stop being a small supplier at the end of the following month. Charge HST from then, and register within 29 days of that date.</td></tr>
<tr><td>Over $30,000 in a single calendar quarter</td><td>You stop being a small supplier right away: charge HST on the sale that takes you over, and register within 29 days.</td></tr>
</tbody></table>
<p>Calendar quarters end March 31, June 30, September 30 and December 31. Most restaurants open to the public pass $30,000 quickly: that's about $580 of sales a week.</p>"""),
             ("Should I register before I have to?", """<p>You can register voluntarily. The CRA lists what that means:</p>
<ul><li><strong>You charge, collect and remit</strong> HST on your taxable sales.</li><li><strong>You file GST/HST returns</strong> regularly.</li><li><strong>You can claim input tax credits</strong> (ITCs): the HST you paid on purchases and operating costs, like equipment and supplies, comes back to you.</li><li><strong>You stay registered at least one year</strong> before you can cancel.</li></ul>
<p>For a new restaurant buying equipment and renovating, ITCs can be significant. For a tiny operation, collecting and filing may not be worth it yet. That's the conversation to have with an accountant.</p>"""),
             ("How HST works on restaurant food in Ontario", """<ul><li><strong>The rate is 13%</strong>: the 5% federal part and the 8% Ontario part.</li><li><strong>The $4 rule.</strong> When qualifying prepared food and drinks sold to someone at one time total $4 or less (before tax), the 8% provincial part is rebated at the till, so only the 5% applies. A $3.80 coffee or snack is taxed at 5%; a $12 lunch at 13%.</li><li><strong>Discounts reduce the taxable price.</strong> HST is calculated on what the diner pays after your own discount, the same way a store coupon reduces the price before tax.</li></ul>
<div class="callout math"><b>A deal, taxed</b><ul><li>A $16 dish with a $4-off deal: the diner pays $12.00 + 13% HST ($1.56) = $13.56.</li><li>Without the deal: $16.00 + $2.08 = $18.08.</li><li>If you're registered, you remit $1.56 on that sale, not $2.08.</li></ul></div>"""),
             ("Your HST number", """<p>When you register, the CRA gives you a 15-character account number: your 9-digit business number, the letters RT (the GST/HST program) and a 4-digit reference, for example 123456789 RT 0001. It goes on your receipts.</p>"""),
             ("HST on FIG", """<table><thead><tr><th>On FIG</th><th>HST number needed?</th></tr></thead><tbody>
<tr><td>Your page, menu and deals</td><td>No</td></tr>
<tr><td>Scanning diners for dine-in deals</td><td>No: you charge tax on your own bill as usual</td></tr>
<tr><td>Takeout (diners pay in the app)</td><td>Yes, plus Stripe payouts</td></tr>
</tbody></table>
<p>For in-app takeout, your HST number goes on every receipt, with your restaurant as the seller. The diner pays the HST with the order, it's paid out to you with the rest, and it's yours to remit. Each month's takeout statement shows sales, HST, fees and what you kept, ready for your bookkeeping. <a href="/blog/set-up-fig-menu-takeout">How to set up in-app takeout</a>.</p>"""),
             ("A simple checklist", """<ol><li>Add up your taxable sales for the last four calendar quarters, every quarter.</li><li>If you're near $30,000, plan to register before you pass it.</li><li>Once registered, set your till to charge 13% (with the $4 rebate where it applies), keep receipts for everything you buy, and file on time.</li><li>Add your HST number in FIG under Settings → Get paid if you want in-app takeout.</li></ol>
<p>The CRA's own pages are the final word: <a href="https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/when-register-charge.html">when to register and start charging the GST/HST</a>.</p>"""),
         ],
         faq=[("What is the small supplier limit in Canada?", "$30,000 of taxable sales over four consecutive calendar quarters, or in a single quarter. Above that, you must register for GST/HST."),
              ("How long do I have to register?", "Within 29 days of the day you stop being a small supplier, according to the CRA. You must start charging HST from that day."),
              ("Can I register for HST voluntarily?", "Yes. You'd charge and remit HST, file returns and claim input tax credits, and you'd stay registered at least one year."),
              ("What is the HST rate on restaurant meals in Ontario?", "13%. Qualifying prepared food and drinks of $4 or less in one sale get the 8% provincial part rebated at the till, leaving 5%."),
              ("Is HST charged on the price before or after a deal?", "After your own discount: HST is calculated on what the diner actually pays."),
              ("Do I need an HST number to use FIG?", "Only for takeout, which diners pay for in the app. Deals and scans work without one."),
              ("Is this tax advice?", "No. It's general information with links to the CRA. Talk to an accountant about your own situation.")]),

    dict(slug="group-dining-deals", screen="map", title="Eating out as a group: picking a place, deals and splitting the bill", date="2026-10-14", topic="For diners", group="eat-out-for-less",
         dek="How to get a group from 'where should we eat?' to a table: deciding fast, checking there's room, making deals work for everyone, and splitting the bill fairly, with the arithmetic.",
         desc="Getting a group from 'where should we eat?' to a table: deciding fast, making deals work for everyone and splitting the bill fairly.",
         seo="Eating out as a group: deals and splitting the bill",
         keywords="group dining deals, where to eat with friends, split the bill, group restaurant Markham, 2 for 1 group deal",
         points=["Share one deal to the group chat instead of asking an open question: a concrete option ends the debate.",
                 "Call the restaurant to check there's room for your group.",
                 "Everyone can claim their own deal. Each code works once, for the person who claimed it.",
                 "Split by what you ordered, and share a deal's saving fairly: the arithmetic is below.",
                 "Quiet hours are best for groups: more room, more deals, more patient kitchens."],
         sections=[
             ("The short answer", """<p>Groups get stuck on choosing, not eating. Share one concrete deal to the group chat, check with the restaurant that there's room, go in a quiet hour if you can, and agree up front how you'll split. FIG helps with the first: share a restaurant's link to your group chat, and everyone sees the same place and its live deals.</p>"""),
             ("1. Decide fast", """<p>"Where should we eat?" invites twenty answers. "2-for-1 noodles at this place, 10 minutes away, 6 pm?" invites a yes. On FIG, share the restaurant's link to your group chat: everyone sees the same place and its live deals. If the first one doesn't land, share the next one. Two or three options is plenty.</p>
<div class="callout tip"><b>Use filters for the picky one</b><p>Set the group's must-haves in FIG's filters (halal, vegetarian, vegan, gluten-free, a budget) before you look, so every option you share already works for everyone.</p></div>"""),
             ("2. Check there's room", """<p>Six people at 7 pm on a Friday is a different ask from six at 5 pm on a Tuesday. Call the restaurant and ask.</p>"""),
             ("3. Make the deal work for the table", """<ul><li><strong>Everyone can claim.</strong> If a deal suits everyone, each person claims their own on their own phone. Each code works once, so each person needs their own, and a screenshot of a used code just says already used.</li><li><strong>Check the details.</strong> Some deals are on specific dishes, some on the whole order, some for dine-in only. Read the deal before the group commits.</li><li><strong>Watch the daily cap.</strong> Popular deals can run out. Claim before you leave home.</li><li><strong>Ask if unsure.</strong> How the deal applies to a shared bill is the restaurant's call. A quick call before you go saves an awkward moment at the till.</li></ul>"""),
             ("4. Split fairly", """<p>Three common ways, from simplest to fairest:</p>
<table><thead><tr><th>Method</th><th>Good for</th></tr></thead><tbody>
<tr><td>Split evenly</td><td>Everyone ordered about the same</td></tr>
<tr><td>Pay for what you ordered</td><td>Very different orders</td></tr>
<tr><td>Pay for what you ordered, share the deal's saving</td><td>When one person's deal discounted dishes everyone shared</td></tr>
</tbody></table>
<div class="callout math"><b>Example: four friends, one 2-for-1</b><ul><li>Orders: two $15 bowls on a 2-for-1, plus a $12 bowl and a $14 bowl. Food total before the deal: $56.</li><li>The deal takes off one $15 bowl: food $41.00.</li><li>HST at 13%: $5.33. Bill: $46.33.</li><li>Evenly: $46.33 ÷ 4 = $11.58 each, with a cent left over.</li><li>By order: the two 2-for-1 eaters share the one paid $15 bowl, $7.50 each; the others pay $12 and $14. With tax: $8.48, $8.48, $13.56 and $15.82.</li></ul><p>Evenly, the two people who ordered more pay less than their share; by order, the 2-for-1 pair saves the most. Agree on the method before you order.</p></div>"""),
             ("5. Go when it's quiet", """<p>Groups are easier for a restaurant in quiet hours: there's room to push tables together and the kitchen isn't slammed. Those are also the hours when restaurants post deals. Early weeknight dinners are the sweet spot. <a href="/blog/restaurant-deals-markham">When Markham restaurants post deals</a>.</p>"""),
             ("6. After the meal", """<p>Each person whose visit was scanned can rate the restaurant. If the place handled your group well, say so: reviews on FIG come only from real visits, so they carry weight with the next group deciding.</p>"""),
         ],
         faq=[("How do I get my friends to agree on a restaurant?", "Share one concrete option, a deal with a place, time and distance, instead of an open question. Two or three options is plenty."),
              ("Can everyone in my group use the same deal?", "Each person can claim their own if the deal suits them. Codes are personal and work once, so one person's code can't be shared."),
              ("How should we split a bill with a deal?", "Agree first: evenly is simplest; paying for what you ordered, with any deal saving shared by the people it applied to, is fairest."),
              ("How do I check if a restaurant can fit our group?", "Call the restaurant and ask, especially for a big group at a busy hour."),
              ("When is the best time to eat out as a group?", "Quiet hours, like early weeknight dinners: more room, an easier kitchen, and more deals."),
              ("Do deals apply to the whole table?", "It depends on the deal: some are on specific dishes, some on the whole order. Check the deal, or call the restaurant before you go.")]),

    dict(slug="how-to-read-restaurant-reviews", screen="map", title="How to read a restaurant's reviews on FIG", date="2026-10-14", updated="2026-10-24", topic="For diners", group="eat-out-for-less",
         dek="Reviews on FIG come only from diners whose visit was scanned. Here's how ratings, likes and replies work, and how to read a restaurant's page to decide in a minute.",
         desc="Reviews on FIG come only from diners whose visit was scanned. How ratings, likes and replies work, and how to read a page in a minute.",
         keywords="restaurant reviews, trustworthy restaurant reviews, how to read restaurant reviews, verified reviews restaurant app, FIG reviews",
         points=["Only diners whose visit was scanned can review a restaurant, so every review comes from a real visit.",
                 "Restaurants get stars; deals get likes. They answer different questions.",
                 "Read the spread of ratings, not just the average, and sort by Newest to see how it's doing now.",
                 "A restaurant's public replies tell you how it treats people when something goes wrong.",
                 "Paying FIG never hides, changes or reorders a review."],
         sections=[
             ("The short answer", """<p>On FIG, a review can only come from a diner whose visit was scanned at the restaurant, so you're reading people who actually ate there. To decide quickly: look at the spread of ratings, sort by Newest to see recent visits, read a couple of the low ones and how the restaurant replied, and check the likes on the deal you're considering.</p>"""),
             ("Why FIG reviews are different", """<p>Most review sites let anyone write anything. On FIG, the review button appears only after a visit is scanned: staff scan the diner's code at the restaurant. That rules out reviews from people who never went, and it ties each review to one visit: one review per visit. Reviews show the diner's first name and last initial.</p>
<p>And nothing a restaurant pays FIG changes this: paying never hides, changes or reorders reviews.</p>"""),
             ("Stars for restaurants, likes for deals", """<table><thead><tr><th></th><th>Stars</th><th>Likes</th></tr></thead><tbody>
<tr><td>On</td><td>The restaurant</td><td>A deal</td></tr>
<tr><td>Answers</td><td>Was the visit good?</td><td>Was the deal worth it?</td></tr>
<tr><td>Who</td><td>Diners whose visit was scanned</td><td>Diners</td></tr>
</tbody></table>
<p>A restaurant can have great food and a so-so deal, or the other way round. Check both.</p>"""),
             ("Read the shape, not just the number", """<p>At the top of a restaurant's reviews you'll see the average, the number of reviews, and five bars from 5 stars down to 1, showing how many of each. The bars often tell you more than the average:</p>
<ul><li><strong>Mostly 5s and 4s:</strong> consistent. A safe bet.</li><li><strong>Lots of 5s and lots of 1s:</strong> divisive. Read the 1s: is it the food, the wait, or something that won't bother you?</li><li><strong>Few reviews:</strong> new on FIG. Don't over-read one or two ratings either way.</li></ul>"""),
             ("Sort to answer your question", """<ul><li><strong>Newest</strong>: how's it doing now? Kitchens change, and recent visits matter most.</li><li><strong>Lowest</strong>: what goes wrong when it goes wrong? Look for patterns, not one bad night.</li><li><strong>Highest</strong>: what are people ordering? Great reviews often name the dish.</li></ul>
<div class="callout example"><b>A one-minute read</b><ol><li>Glance at the bars.</li><li>Sort by Newest and read three.</li><li>Sort by Lowest and read two, plus the restaurant's replies.</li><li>Check the deal's likes.</li></ol><p>That's usually enough to decide.</p></div>"""),
             ("Replies matter", """<p>Restaurants can reply to reviews in public. A calm, specific reply to a bad review ("we've changed how we handle takeout at lunch") tells you more about a place than ten five-star ratings. No reply at all isn't a red flag on its own: small kitchens are busy.</p>"""),
             ("Write a useful review yourself", """<p>After your visit is scanned, tap Rate this visit, or find it later under Past visits on your Deals page. Pick the stars and, if you like, add a few words or a photo. The most helpful reviews say:</p>
<ul><li>what you ordered;</li><li>when you went (a Tuesday afternoon is a different restaurant from a Saturday night);</li><li>one thing that stood out, good or bad.</li></ul>
<p>Be fair: rate the visit, not the price of the deal. If the deal itself disappointed, that's what a deal's like (or lack of one) is for. <a href="/blog/how-restaurant-deals-work">How deals work, from claim to counter</a>.</p>"""),
         ],
         faq=[("Can anyone review a restaurant on FIG?", "No. Only diners whose visit was scanned can review, so every review comes from a real visit. One review per visit."),
              ("What's the difference between stars and likes?", "Stars rate a restaurant visit; likes are for deals. A great restaurant can have a so-so deal, and the other way round."),
              ("Can restaurants remove bad reviews?", "No. Restaurants can reply in public, but paying FIG never hides, changes or reorders a review."),
              ("How should I sort reviews?", "Newest to see how it's doing now, Lowest to see what goes wrong, Highest to see what people order."),
              ("Whose name shows on my review?", "Your first name and last initial."),
              ("When can I review?", "After your visit is scanned: tap Rate this visit, or find it later under Past visits on your Deals page.")]),

    # ---------------------------------------------------------------- batch of 4 queued posts (publish_at: hidden until then)

    # Stripe 2.9% + CA$0.30, Ontario HST 13%: sources at the top. All fee arithmetic below is on the food after any deal, tax added on top.
    dict(slug="takeout-order-math-what-you-keep", screen="tscanner", title="Takeout order math: what a restaurant keeps on a $12, $20, $40 or $60 order", date="2026-10-16", publish_at="2026-10-16T12:00:00-04:00", topic="For restaurants", group="takeout-and-money",
         dek="On FIG, takeout paid in the app costs 5% of the food plus Stripe's card fee. The $0.30 part of that fee is fixed, so small orders cost a bigger share. Here are the numbers on four order sizes, and what to do about them.",
         desc="In-app takeout on FIG costs 5% of the food plus Stripe's card fee. Its fixed $0.30 weighs more on small orders: the numbers on four order sizes.",
         seo="Takeout order math: what a restaurant keeps per order",
         keywords="takeout fees restaurant, restaurant takeout profit, Stripe fee restaurant Canada, takeout order math, in-app takeout fees, restaurant takeout Markham",
         points=["A takeout order paid in the app costs 5% of the food before tax, plus Stripe's 2.9% + $0.30 on the full payment, tax included.",
                 "The $0.30 is a flat charge, so fees take about 10.8% of a $12 order but about 8.8% of a $60 order.",
                 "On a $20 order, a restaurant keeps about $18.04 of the food. On $40, about $36.39. On $60, about $54.73.",
                 "Judge takeout by contribution (what you keep minus the food cost), not by the fee alone, and compare it with dine-in.",
                 "Bigger baskets, quiet-hour takeout, a pause button and a deals-per-order limit are the levers you control."],
         sections=[
             ("The short answer", """<p>When a diner pays for takeout in the FIG app, the restaurant pays two things out of that payment: FIG keeps 5% of the food before tax, and Stripe keeps 2.9% of the full payment plus $0.30. On a $20 order that comes to about $1.96, so the restaurant keeps about $18.04 of the food. The HST the diner paid is paid out too, and it is the restaurant's to remit.</p>
<p>Because $0.30 is a flat amount, small orders cost a larger share than big ones. This post works through four order sizes so you can see where takeout makes sense for your kitchen.</p>"""),
             ("How the fees are worked out", """<p>Three numbers matter, in this order:</p>
<ol><li><strong>The food.</strong> What the diner is charged for the dishes, after any deal, before tax.</li><li><strong>The payment.</strong> The food plus 13% Ontario HST. This is what the diner's card is charged.</li><li><strong>The two fees.</strong> FIG: 5% of the food. Stripe: 2.9% of the payment plus $0.30, which is Stripe's published price for Canadian domestic cards.</li></ol>
<p>Stripe's percentage is taken on the full payment, tax included, because that is the amount that goes through the card. FIG's 5% is on the food only. Everything left is paid out to you, including the HST, which you remit as you would on any sale. <a href="/blog/how-fig-makes-money">How FIG makes money, in full</a>.</p>"""),
             ("Four order sizes, side by side", """<div class="callout math"><b>Round example orders (your menu will differ)</b><table><thead><tr><th>Food</th><th>HST at 13%</th><th>Diner pays</th><th>Stripe fee</th><th>FIG 5%</th><th>You keep from the food</th></tr></thead><tbody>
<tr><td>$12.00</td><td>$1.56</td><td>$13.56</td><td>$0.69</td><td>$0.60</td><td>$10.71 (about 89.3%)</td></tr>
<tr><td>$20.00</td><td>$2.60</td><td>$22.60</td><td>$0.96</td><td>$1.00</td><td>$18.04 (90.2%)</td></tr>
<tr><td>$40.00</td><td>$5.20</td><td>$45.20</td><td>$1.61</td><td>$2.00</td><td>$36.39 (91.0%)</td></tr>
<tr><td>$60.00</td><td>$7.80</td><td>$67.80</td><td>$2.27</td><td>$3.00</td><td>$54.73 (91.2%)</td></tr>
</tbody></table><p>Check one: on the $40 order, Stripe takes 2.9% of $45.20, which is $1.31, plus $0.30, so $1.61. FIG takes 5% of $40, which is $2.00. $40.00 &minus; $1.61 &minus; $2.00 = $36.39. Fees are rounded to the cent.</p></div>
<p>Put another way, the two fees together are about 10.8% of a $12 order, 9.8% of a $20 order, 9.0% of a $40 order and 8.8% of a $60 order. The share falls as the order grows, but it stays above 7.9% (FIG's 5% plus Stripe's 2.9%) however big the order gets.</p>"""),
             ("Compare it with what the food costs you", """<p>The fee matters less than what is left after the ingredients. Contribution is what you keep minus the food cost. It is the money that goes toward wages, rent and profit. Take a $24 order of food where your food cost is 30% of menu price (the usual quoted range is 28% to 32%), so $7.20 on the plate:</p>
<div class="callout math"><b>The same $24 of food, three ways</b><table><thead><tr><th>How it is sold</th><th>Diner is charged for food</th><th>You keep</th><th>Food cost</th><th>Contribution</th></tr></thead><tbody>
<tr><td>Dine-in with a $4-off deal</td><td>$20.00</td><td>$20.00 (no per-order fee to FIG)</td><td>$7.20</td><td>$12.80</td></tr>
<tr><td>Takeout with the same $4-off deal</td><td>$20.00</td><td>$18.04</td><td>$7.20</td><td>$10.84</td></tr>
<tr><td>Takeout at full price (0 deals per order)</td><td>$24.00</td><td>$21.71</td><td>$7.20</td><td>$14.51</td></tr>
</tbody></table><p>For the last row: the diner pays $24.00 + $3.12 HST = $27.12. Stripe takes $1.09 and FIG takes $1.20, so you keep $24.00 &minus; $1.09 &minus; $1.20 = $21.71.</p></div>
<p>Two things stand out. First, takeout with a deal still contributes $10.84, far better than an idle kitchen. Second, a full-price takeout order contributes more than a dine-in deal, because there is no discount to pay for, even after the fees. Whether you want takeout at full price is your call: on FIG, you choose it by setting 0 deals per order.</p>"""),
             ("What the fixed $0.30 means for your menu", """<p>If most of your takeout orders are one drink or one small snack, the flat part of the fee is a real cost. If most are a main, a side and a drink, it is a rounding error. You cannot change Stripe's price, but you can change the shape of the order:</p>
<ul><li><strong>Build combinations.</strong> A main plus a drink and a side at a set price turns a $12 order into a $20 one. On the table above, that moves the fee share from 10.8% to 9.8%, and, more importantly, adds food you would have sold at full price.</li><li><strong>Keep deals on the main dish.</strong> A deal on the main, with drinks and sides at full price, lets add-ons earn. <a href="/blog/slow-hour-deal-math">The slow-hour math covers why</a>.</li><li><strong>Set a deals-per-order limit.</strong> You decide how many deals one order can use, so a large order cannot stack discounts. For percentage deals you can also set the most one takeout order can take off. <a href="/blog/deal-types-percent-dollar-2-for-1">Which deal type fits</a>.</li></ul>"""),
             ("A month of takeout, as an example", """<div class="callout example"><b>Forty $30 orders in a month</b><ul><li>Each order: Stripe about $1.28 and FIG $1.50, so $2.78 in fees.</li><li>Forty orders: $111.20 in fees, from $1,200 of food.</li><li>You keep $1,088.80 of the food (about 90.7%), plus you collect and remit the HST.</li></ul><p>These are example numbers. Your monthly takeout statement shows your real sales, HST, fees and what you kept.</p></div>
<p>If those forty orders came in hours that were otherwise quiet, the question to ask is whether each one contributed more than an empty kitchen did. At a 30% food cost, a $30 order leaves $27.22 &minus; $9.00 = $18.22 before your wages and rent. It usually does.</p>"""),
             ("When takeout is the wrong call", """<ul><li><strong>At your peak.</strong> If the dining room is full and the kitchen is stretched, takeout orders compete with tables that pay without a card fee. Use pause takeout, for a set time or until tomorrow, or add prep time so pickup times stay honest.</li><li><strong>When the dish does not travel.</strong> Some food is best eaten at the table. Leave it off the takeout deals.</li><li><strong>When margins on the dish are very thin.</strong> Run its numbers first. If the food cost is already 40% of the price, a deal plus fees may leave little.</li></ul>
<p>Diners tap I'm here when they arrive, and an order that is not picked up closes two hours after the pickup time. Restaurants see a diner's missed pickups, which helps you decide how much prep to start before they arrive.</p>"""),
             ("What you need before takeout works", """<p>Takeout paid in the app needs two things in Settings → Get paid: your HST number, which goes on every receipt with your restaurant as the seller, and Stripe payouts. Dine-in deals need neither. Not registered yet? Read <a href="/blog/hst-registration-small-restaurants-ontario">HST registration for small restaurants</a>, which is general information and not tax advice. When both are ready, <a href="/blog/set-up-fig-menu-takeout">setting up your menu and takeout</a> takes about 15 minutes.</p>"""),
             ("A simple way to decide", """<ol><li>Pick the dish you would sell most as takeout and write its menu price and food cost.</li><li>Work out what you keep using the table above, or the formula: food &minus; (2.9% of food&times;1.13 + $0.30) &minus; 5% of food.</li><li>Subtract the food cost. If the answer is comfortably above zero, post a takeout deal for a quiet window with a daily cap.</li><li>After two weeks, look at your takeout statement and your insights, and keep what works.</li></ol>"""),
         ],
         faq=[("What does it cost a restaurant to take takeout orders on FIG?", "Nothing to turn it on. On each order paid in the app, FIG keeps 5% of the food before tax, and Stripe's card fee of 2.9% + $0.30 comes off the same payment."),
              ("Is Stripe's fee charged on the tax too?", "Yes. Stripe's percentage applies to the full card payment, which includes the HST. FIG's 5% is on the food before tax."),
              ("Why do small takeout orders cost more in percentage terms?", "Stripe's $0.30 is a flat amount. On a $12 order the two fees are about 10.8% of the food; on a $60 order about 8.8%."),
              ("Can I offer takeout at full price?", "Yes. If you set 0 deals per order, diners can order takeout at full price. Otherwise takeout comes with a deal."),
              ("Who remits the HST on a takeout order?", "The restaurant. The diner pays HST with the order, it is paid out to you with the rest, and your HST number is on the receipt. This is general information, not tax advice."),
              ("Can I stop takeout when the kitchen is busy?", "Yes. Pause takeout for a set time or until tomorrow, or add prep time, in one tap."),
              ("Is dine-in with a deal charged the same way?", "No. A diner who uses your deal at the counter pays you directly and FIG takes nothing from that bill.")]),

    dict(slug="compare-restaurant-deals-worth-it", screen="claim", title="Is it a good deal? How to compare restaurant deals", date="2026-10-17", publish_at="2026-10-17T12:00:00-04:00", updated="2026-11-05", topic="For diners", group="eat-out-for-less",
         dek="2-for-1, 20% off, $3 off or a free drink: which one saves you the most? A plain method for comparing restaurant deals, with worked examples, so you pick the one that fits what you were going to eat anyway.",
         desc="2-for-1, 20% off, $3 off or a free drink: which saves the most? A plain way to compare restaurant deals, with worked examples.",
         keywords="is this restaurant deal worth it, compare restaurant deals, 2 for 1 vs percent off, how to save money eating out, restaurant discount math, Markham restaurant deals",
         points=["A deal is only good if it saves money on something you would have ordered anyway.",
                 "Compare deals by the price you pay at the end, not by the size of the number in the headline.",
                 "A cheaper place at full price can beat a pricier place with a deal: do the sum on the dish.",
                 "Check the fine print in the app: which dishes, which days and hours, dine-in or takeout, and the daily cap.",
                 "Tax is worked out after the deal, so a deal also lowers the HST you pay."],
         sections=[
             ("The short answer", """<p>A good deal lowers what you pay for a meal you were already planning to have. To compare two deals, work out the final price you would pay for the same food, not the headline: $3 off, 20% off and 2-for-1 sound different but only the end price tells you which one is cheaper. Then check when it runs, which dishes it covers and whether you can get there before it ends.</p>"""),
             ("Step 1: start with the food, not the deal", """<p>The biggest mistake with any deal is ordering something you did not want because it was discounted. A $6 saving on a $20 dish you would never choose is a $14 loss. Decide what you feel like eating, then look for the deal that fits it. On FIG you can set what you crave, your budget and your diet once, and Home and the map show live deals that fit, nearest first.</p>"""),
             ("Step 2: turn every deal into a final price", """<p>Take the dish you want and work out what you pay under each deal. Here is a $16 dish, using round example prices:</p>
<div class="callout math"><b>One $16 dish, four deals (example prices, before tax)</b><table><thead><tr><th>Deal</th><th>How it works out</th><th>You pay</th><th>You save</th></tr></thead><tbody>
<tr><td>20% off</td><td>$16.00 &minus; $3.20</td><td>$12.80</td><td>$3.20</td></tr>
<tr><td>$3 off</td><td>$16.00 &minus; $3.00</td><td>$13.00</td><td>$3.00</td></tr>
<tr><td>2-for-1, with a friend</td><td>$32.00 for two, pay $16.00, so $8.00 each</td><td>$8.00 each</td><td>$8.00 each</td></tr>
<tr><td>Free $5 drink with a main</td><td>$16.00 + a drink you would pay $5.00 for</td><td>$16.00 for both</td><td>$5.00, only if you wanted the drink</td></tr>
</tbody></table><p>On a single $16 dish, 20% off beats $3 off by 20 cents. On a $12 dish the order flips: 20% is $2.40, so $3 off wins. The break-even is $15, where 20% off and $3 off are the same.</p></div>
<p>The 2-for-1 saves the most per person, but only if you have someone to share it with and you each want the dish. Alone, it is just a full-price dish.</p>"""),
             ("Step 3: remember the tax moves with the price", """<p>In Ontario, HST is 13% and it is worked out on what you actually pay after the restaurant's own discount, the same way a store coupon lowers the price before tax. That means a deal also lowers your tax. On the $16 dish with 20% off, you pay $12.80 plus $1.66 of HST, so $14.46. At full price it would be $16.00 plus $2.08, so $18.08. The deal saved you $3.62 at the till, not just $3.20.</p>
<p>One small exception: prepared food and drinks that total $4 or less in one sale get the 8% provincial part rebated at the till, so only the 5% GST applies. That is general information, not tax advice. <a href="/blog/student-food-deals-markham">More on the $4 rule and eating out on a budget</a>.</p>"""),
             ("Step 4: compare the place, not just the deal", """<p>A deal at an expensive restaurant is not automatically cheaper than the regular price at a cheaper one. Do the sum on the dish you would actually order:</p>
<div class="callout math"><b>Two places, one craving (example prices, before tax)</b><ul><li>Place A sells the dish at $14.00, no deal.</li><li>Place B sells it at $18.00 and has 25% off: $18.00 &minus; $4.50 = $13.50.</li><li>Place B with $3 off instead: $15.00. Now Place A is cheaper by $1.00.</li></ul><p>A 25% deal on an $18 dish beats a $14 dish by 50 cents. A $3 deal on the same dish does not. The bigger the discount percentage, the more a pricier menu can still come out ahead.</p></div>"""),
             ("Step 5: read the fine print before you claim", """<p>A deal that does not apply to your order saves you nothing. Before you tap Claim, check:</p>
<ul><li><strong>Which dishes.</strong> Some deals apply to the whole order, others to specific dishes you will see on the restaurant's menu.</li><li><strong>Days and hours.</strong> Many deals run only in quiet hours, such as weekday afternoons and early evenings.</li><li><strong>Dine in or takeout.</strong> Some deals are for eating in only. Others also work as takeout, paid in the app, and you pick the food up.</li><li><strong>The daily cap.</strong> A popular deal can run out for the day, so claim before you leave.</li><li><strong>The end.</strong> A claim stays until the deal ends. A flash deal ends when its timer does.</li></ul>
<p>If you are unsure how it applies to your order, call the restaurant first. <a href="/blog/how-restaurant-deals-work">How a deal works from claim to counter</a>.</p>"""),
             ("Step 6: price in the extras", """<p>Drinks, sides and desserts are usually full price, and they are where a cheap meal stops being cheap. A deal on the main is still a good deal if you keep the extras modest. Here is the whole bill for two people on a 2-for-1, example prices:</p>
<div class="callout example"><b>Two people, one 2-for-1</b><ul><li>Two $16 dishes on a 2-for-1: you pay $16.00.</li><li>Two $4 drinks at full price: $8.00.</li><li>Food total $24.00, HST at 13% is $3.12, bill $27.12, so $13.56 each.</li><li>Without the deal: $32.00 + $8.00 = $40.00, HST $5.20, bill $45.20, so $22.60 each.</li></ul><p>The deal saved $18.08 on the bill, $9.04 each. Most of the saving is the dish. The drinks were never discounted.</p></div>"""),
             ("Takeout deals, with the same sums", """<p>When a deal allows takeout, you order from the menu in the app, the deal comes off, and you pick it up. There is no delivery fee, and FIG adds no service fee. You pay the menu price minus the deal, plus tax, so the same arithmetic as above applies. A $24 order with $4 off is $20.00 plus $2.60 of HST, $22.60 in total. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a>.</p>"""),
             ("Group deals: share the saving fairly", """<p>When a deal saves money for the table, agree how to share it before the bill arrives. The simple rule is that the people whose dishes the deal covered share the saving. Example prices: four friends order two $15 bowls on a 2-for-1, plus a $12 bowl and a $14 bowl. Food is $56 before the deal and $41 after it, so the deal saved $15. Whoever ate the 2-for-1 bowls splits that $15 between them: $7.50 each. That is fairer than splitting the bill evenly, where the two people who ordered the cheaper dishes quietly cover part of the saving. <a href="/blog/group-dining-deals">Splitting the bill fairly, with the arithmetic</a>.</p>"""),
             ("Know when to skip a deal", """<p>Some deals are not worth chasing. Skip it if you would have to travel far out of your way for a few dollars, if the dish is not one you like, or if the hours mean rushing a meal you wanted to enjoy. A deal is a bonus on a good plan, not a reason for a bad one. Because FIG shows every live deal near you, nearest first, there is usually another one close by, and a claim does not time out while the deal runs, so you can claim now and go when it suits you.</p>"""),
             ("A quick checklist", """<ol><li>Would I order this dish anyway?</li><li>What is my final price under this deal, and under the next best one?</li><li>Does it cover the dishes, the day and the hour I am going?</li><li>Can I get there before it ends, and is there room if I am going with a group?</li><li>Have I counted the drinks and sides?</li></ol>
<p>If you can answer yes to the first four and the fifth does not worry you, claim it. If not, the next deal is probably already live. FIG is free for diners, with no ads for now.</p>"""),
         ],
         faq=[("Is 2-for-1 better than 20% off?", "For two people who both want the dish, 2-for-1 saves more: 50% each. Alone, it saves nothing, and 20% off is better. Work out the final price for your order."),
              ("Is $3 off or 20% off better?", "On dishes over $15, 20% off saves more; under $15, $3 off does. At exactly $15 they are equal. These are round example numbers."),
              ("Does a restaurant deal lower the tax I pay?", "Yes. In Ontario, HST is calculated on the price after the restaurant's own discount, like a store coupon, so a smaller price means smaller tax. This is general information, not tax advice."),
              ("Do I pay FIG anything to use a deal?", "No. FIG is free for diners, with no ads for now. For dine-in deals you pay the restaurant at the counter as usual."),
              ("Can I use a deal on takeout?", "Only if the restaurant marked that deal as Dine in or takeout. Takeout is paid in the app, and there is no delivery or service fee from FIG."),
              ("What if a deal runs out before I get there?", "A daily cap can end a deal for the day, and a flash deal ends with its timer. An expired claim never counts against you."),
              ("How do I check that a deal fits my order?", "Open the deal and check the dishes, days, hours and whether it is dine in or takeout. You can also call the restaurant before you go.")]),

    dict(slug="train-staff-honour-fig-deal", screen="tscanner", title="Train your staff to honour a FIG deal in 10 minutes", date="2026-10-18", updated="2026-10-24", publish_at="2026-10-18T12:00:00-04:00", topic="For restaurants", group="fill-quiet-hours",
         dek="A deal only works if the person at the counter knows what to do with it. A ten-minute training plan for restaurant staff: how to scan, what to check, what to say when something looks off, and a one-page cheat sheet.",
         desc="A ten-minute training plan so counter staff know what to do with a FIG deal: how to scan, what to check, what to say, and a cheat sheet.",
         keywords="train restaurant staff, scan QR code restaurant deal, staff training restaurant promotion, FIG for restaurants, honour restaurant coupon",
         points=["Staff need to know how a deal gets applied: scan the diner's code, or type the short code if the camera fails.",
                 "A code works once, so a screenshot of a used code just says already used.",
                 "Each claim is used once. A daily cap stops the deal on its own, so staff do not have to count.",
                 "Put the deal on a card by the till: what it covers, which days and hours, dine-in or takeout.",
                 "Decide in advance what staff do when a scan fails, and tell them they can ask you instead of arguing at the counter."],
         sections=[
             ("The short answer", """<p>Staff need to know four things: what the deal is, how to scan it, what to do when it does not scan, and who to ask. That fits in ten minutes. To scan, staff open the restaurant side of FIG on any phone, tablet or computer and scan the diner's code. The deal comes off the bill, and the diner pays you as usual. There's no fee per scan or per diner.</p>"""),
             ("Why training matters more than the deal", """<p>A diner who claimed a deal and then waits while three staff members debate it will not be back, however good the deal was. A short routine fixes that. It also protects you: when everyone applies the deal the same way, you can trust the numbers in your insights, which show views, claims, the diners who came in and the ones who came back.</p>"""),
             ("The ten-minute plan", """<table><thead><tr><th>Minutes</th><th>What to cover</th><th>Who does it</th></tr></thead><tbody>
<tr><td>0 to 2</td><td>What today's deals are, in one sentence each, with days and hours</td><td>You, reading from the deal card</td></tr>
<tr><td>2 to 7</td><td>Scan the diner's code with the restaurant side of FIG, step by step</td><td>You, then each person tries once</td></tr>
<tr><td>7 to 9</td><td>When something looks off and what to say</td><td>Role-play two cases</td></tr>
<tr><td>9 to 10</td><td>Who to ask, and where the cheat sheet lives</td><td>You</td></tr>
</tbody></table>
<p>Run it at the start of a shift, before the doors open, and again for anyone new. Put the same card by every till.</p>"""),
             ("How staff scan the diner's code", """<ol><li>The diner orders as usual. When it is time to pay, they open their Deals page and tap Show QR.</li><li>A staff member opens the restaurant side of FIG on a phone, tablet or computer and scans the code on the diner's screen.</li><li>The deal comes off the bill. The diner pays you the way they always do: card, cash or whatever you take.</li></ol>
<p>If a camera will not read the screen, there is a short code staff can type instead. Teach that too, so a dirty lens never stops a sale. A code works once, so a screenshot or a photo sent by a friend just says already used after the first scan. Each diner claims and shows their own.</p>"""),
             ("What staff should check", """<p>Before applying any deal, the person at the counter should be able to answer these without looking anything up. Put the answers on the card:</p>
<ul><li><strong>What it covers.</strong> The whole order, or specific dishes from your menu?</li><li><strong>When it runs.</strong> Which days and hours? A deal for weekday afternoons does not apply on Saturday night.</li><li><strong>Dine in or takeout.</strong> Dine-in deals are for eating in. Takeout is paid in the app, and a takeout order arrives with its deal already applied.</li><li><strong>The cap.</strong> It stops the deal on its own once it has been used that many times today. Staff do not need to count.</li><li><strong>One use per claim.</strong> A scanned claim is used. The diner can claim again only if the deal allows it.</li></ul>"""),
             ("When something looks off", """<p>Settle the answers before the rush, so nobody invents them at the counter. These are suggestions to adapt, since your policy is yours:</p>
<table><thead><tr><th>What happens</th><th>A calm way to handle it</th></tr></thead><tbody>
<tr><td>The code will not scan</td><td>Try again, then type the short code. If it still fails, ask the manager.</td></tr>
<tr><td>The diner shows a screenshot</td><td>Kindly ask them to open their Deals page and tap Show QR. The code on their Deals page is the current one.</td></tr>
<tr><td>The deal is outside its hours</td><td>Explain the days and hours. You can still honour it as a courtesy if you choose. That is your decision, not the app's.</td></tr>
<tr><td>The deal has ended or hit its cap</td><td>Say so politely and mention what else is on today. A flash deal ends with its timer.</td></tr>
<tr><td>The diner asks about a dish the deal does not cover</td><td>Point to the card. The deal covers what it says; other items are full price.</td></tr>
</tbody></table>
<p>Give staff permission to ask you. A short pause is better than a wrong call in either direction.</p>"""),
             ("Tax and the bill", """<p>In Ontario, HST is worked out on what the diner pays after your own discount, the same way a store coupon lowers the price before tax. Your till should charge tax on the discounted amount. This is general information, not tax advice, so check with your accountant if you are unsure how your till handles a discount. <a href="/blog/deal-types-percent-dollar-2-for-1">How tax works on each deal type</a>.</p>
<div class="callout math"><b>Example: a $12 bowl with $3 off, eating in</b><ul><li>Bowl $12.00 &minus; $3.00 = $9.00.</li><li>HST at 13%: $1.17.</li><li>Diner pays $10.17.</li></ul><p>Staff tip: if the till total does not match what the diner expects, show them the line. A clear receipt prevents most disputes.</p></div>"""),
             ("Be kind about privacy", """<p>Restaurants never see a diner's phone number. On orders and reviews, you see their first name and last initial. Tell staff not to ask for contact details to apply a deal; the scan is all that is needed.</p>"""),
             ("Your one-page cheat sheet", """<ol><li>Today's deals, with days, hours and dishes.</li><li>Scan the diner's code with the restaurant side of FIG.</li><li>If the camera fails, type the short code.</li><li>A used code just says already used: ask for the current code on their Deals page.</li><li>If anything looks off, ask the manager. Do not argue at the counter.</li><li>Afterwards, tell the diner they can rate the visit. Only scanned visits can be reviewed.</li></ol>
<p>Print it, laminate it and tape it by each till. When you change a deal, change the card the same day. <a href="/blog/set-up-fig-menu-takeout">Setting up your menu, deals and scanning</a> covers the first-time setup.</p>"""),
         ],
         faq=[("How do staff apply a FIG deal?", "They scan the diner's code with the restaurant side of FIG on any phone, tablet or computer. The deal comes off the bill."),
              ("What if the camera cannot scan the code?", "There is a short code staff can type instead."),
              ("Can a diner use a screenshot of their code?", "No. A code works once, so a screenshot of a used code just says already used."),
              ("Does it cost anything to scan diners?", "No. There's no fee per scan or per diner; scanning is free."),
              ("Do staff need to count how many times a deal was used?", "No. The daily cap you set stops the deal automatically once it has been used that many times."),
              ("Do restaurants see diners' phone numbers?", "No. On orders and reviews you see a first name and last initial.")]),

    dict(slug="eating-out-dietary-needs-allergies-markham", screen="claim", title="Eating out with dietary needs or allergies: filters, calling ahead and what to ask", date="2026-10-19", updated="2026-11-05", publish_at="2026-10-19T12:00:00-04:00", topic="For diners", group="fig-in-markham",
         dek="Halal, vegetarian, vegan, gluten-free or an allergy: how to use diet filters as a starting point, and what to ask a restaurant before you go and when you order.",
         desc="Halal, vegetarian, vegan, gluten-free or an allergy: using diet filters as a start, and what to ask a restaurant before you go and when you order.",
         seo="Eating out with dietary needs or allergies in Markham",
         keywords="allergy friendly restaurants Markham, halal restaurants Markham, vegetarian vegan restaurants Markham, gluten-free eating out, ask restaurant about allergies, dietary filters restaurant app",
         points=["Set your diet in FIG once and places that do not fit drop out of your results. Filters are a starting point, not a guarantee.",
                 "For an allergy, always confirm with the restaurant itself, before you go and again when you order.",
                 "Call the restaurant before you go with a short, specific question.",
                 "Ask about ingredients, shared equipment and how the dish is made, not just 'is it safe?'.",
                 "This is general information, not medical advice. Follow your doctor's guidance for your own allergy."],
         sections=[
             ("The short answer", """<p>Use FIG's diet filters to narrow the list, then ask the restaurant about your exact need before you go. Filters tell you where to look. Only the kitchen knows what is in a dish, what it was cooked beside and who is working today. For an allergy, check twice: once on the phone before you go, and again when you order. This guide is general information, not medical advice.</p>"""),
             ("Step 1: set your diet once", """<p>When you set up FIG, you choose what you crave, your budget and your diet: halal, vegetarian, vegan, gluten-free and more. After that, Home and the map show live deals from places that fit, nearest first, and the others drop out.</p>
<p>It saves a lot of scrolling, and it helps groups too: set the group's must-haves before you share options, so everything you send already works for everyone. <a href="/blog/group-dining-deals">Eating out as a group</a>.</p>"""),
             ("Step 2: know what a filter can and cannot tell you", """<table><thead><tr><th>A filter can tell you</th><th>It cannot tell you</th></tr></thead><tbody>
<tr><td>This place has options for your diet</td><td>That every dish on the menu is suitable</td></tr>
<tr><td>Which restaurants to look at first</td><td>What was cooked on the same grill or fryer</td></tr>
<tr><td>That the restaurant chose to list that diet</td><td>Whether today's recipe or supplier changed</td></tr>
<tr><td>A good place to start</td><td>That an allergy is safe</td></tr>
</tbody></table>
<p>Words like halal, vegan and gluten-free can mean slightly different things in different kitchens. If the exact meaning matters to you, ask what it means at that restaurant.</p>"""),
             ("Step 3: call before you go", """<p>Call the restaurant before you go. A good question is short, specific and gives the kitchen something to answer. Some examples to adapt:</p>
<div class="callout example"><b>Questions you can copy and change</b><ul><li>"Hi, I'm vegetarian. Is the mushroom noodle bowl made without meat stock?"</li><li>"I have a peanut allergy. Does the kitchen use peanut oil or peanut sauces, and can the dish I'm planning be made without them?"</li><li>"Do you have a gluten-free option, and is it cooked on separate equipment?"</li><li>"I'd like to use the 2-for-1 on the dumplings. Are the vegetable ones vegan?"</li></ul></div>
<p>A busy kitchen at 6 pm may not have time to talk, so call earlier in the day, or choose a quieter hour when staff can give you attention.</p>"""),
             ("Step 4: ask the right questions", """<p>"Is it safe?" is a hard question to answer yes or no. Better questions let the kitchen tell you what it knows:</p>
<ul><li><strong>Ingredients.</strong> What is in the dish, the sauce and the broth?</li><li><strong>Hidden sources.</strong> Is there butter, fish sauce, soy, nuts, egg, wheat or dairy in the sauce, marinade or garnish?</li><li><strong>Shared equipment.</strong> Is it cooked on the same grill, fryer or board as other foods?</li><li><strong>Changes.</strong> Can the dish be made without the ingredient, and will the kitchen change how it is cooked, or only leave something off the plate?</li><li><strong>Who is cooking.</strong> Does the person taking your order know your need? Ask them to pass it to the cook.</li></ul>"""),
             ("Step 5: say it again when you order", """<p>Menus, recipes and staff change. Even if you called earlier, tell your server when you order: "I have a shellfish allergy, as I mentioned on the phone." Say it at the table and at the counter, and again if a different person brings the food. If you are not sure about something you are served, ask before you eat it. If the answer does not satisfy you, it is fine to say no thank you.</p>"""),
             ("Deals and dietary needs", """<p>A deal only helps if you can eat the dish. Check which dishes the deal covers: some are on specific dishes, others on the whole order. If the covered dish does not suit you, call the restaurant and ask whether the deal can apply to something that does. The answer is the restaurant's call. A 2-for-1 on a dish you cannot eat is not a deal. <a href="/blog/compare-restaurant-deals-worth-it">How to compare restaurant deals</a>.</p>"""),
             ("Takeout with a dietary need", """<p>When you order takeout with a deal, call the restaurant for changes: no onions, extra sauce on the side, or a note about an allergy. When you collect the food, check the bag against the order before you leave. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a>.</p>"""),
             ("If you are the restaurant", """<p>Owners reading this: the more precisely your page, menu and replies describe what you can do, the more trust you earn. Keep ingredient and allergen information current, answer questions promptly, and be honest when you cannot guarantee something. A diner who hears "we cannot guarantee a nut-free kitchen" and chooses to come anyway, or goes elsewhere, is a better outcome than a mistake. Only diners whose visit was scanned can review, and you can reply in public. <a href="/blog/how-to-read-restaurant-reviews">How reviews work on FIG</a>.</p>"""),
             ("Talking to staff kindly and clearly", """<p>Kitchens are busy, and the easiest way to get a good answer is to make it easy to give. Lead with the need, then the question: "I'm allergic to sesame. Can you tell me which dishes have it?" is clearer than "what's safe here?". Thank the person who checked for you, even if the answer is that the kitchen cannot do it. A restaurant that tells you honestly what it cannot promise is looking after you. If you eat out often with the same need, a short note saved on your phone, with your allergy and the foods to avoid, saves you typing it each time.</p>"""),
             ("Going with friends or family", """<p>If you are eating with a group, tell the person organising before the restaurant is chosen, not at the table. Share a deal that you have already checked, so nobody has to change plans on the day. If you are taking a child with an allergy, say the need first when you call so the restaurant hears it straight away. For a big group, call earlier and ask whether the kitchen can handle it in a quiet hour rather than at peak dinner. Quiet hours are often better for questions as well as for deals.</p>"""),
             ("A short checklist", """<ol><li>Set your diet in FIG and shortlist two or three places.</li><li>Call each with a specific question.</li><li>Pick the one that answered clearly.</li><li>Claim the deal and go in a quieter hour.</li><li>Tell your server your need when you order.</li><li>Afterwards, rate the visit and name the dish. Your review helps the next diner with the same need.</li></ol>"""),
         ],
         faq=[("Does FIG have diet filters?", "Yes. You can set your diet, such as halal, vegetarian, vegan or gluten-free, and Home and the map show places that fit."),
              ("Is a diet filter a guarantee for an allergy?", "No. A filter is a starting point. Always confirm with the restaurant, before you go and when you order."),
              ("Does the restaurant see my phone number?", "Not through FIG. The restaurant sees your first name and last initial on orders and reviews."),
              ("What should I ask a restaurant about an allergy?", "Ask about ingredients in the dish and sauce, shared equipment, whether it can be made without the ingredient, and whether the kitchen knows about your need."),
              ("Can I use a deal on a dish that suits my diet?", "That depends on what the deal covers. Check the deal, or call the restaurant to ask whether it can apply to a dish you can eat."),
              ("Can I add a note about my diet to a takeout order?", "Call the restaurant after you order to tell them. Check the bag against your order when you collect it."),
              ("Is this medical advice?", "No. It is general information. Follow your doctor's guidance for your own allergy.")]),

    # ---------------------------------------------------------------- batch of 4 queued posts (publish_at: hidden until then)

    dict(slug="deal-wont-scan-troubleshooting-diners", screen="qr", title="Deal not working at the counter? What to check and what to say", date="2026-10-20", updated="2026-11-05", publish_at="2026-10-20T12:00:00-04:00", topic="For diners", group="eat-out-for-less",
         dek="A code that will not scan, a deal that seems to be over, a pickup that went wrong: the usual reasons a FIG deal does not apply at the counter, what to try first, and how to ask politely.",
         desc="A FIG code that will not scan, a deal that seems over or a missed pickup: the usual reasons, what to try first and how to ask politely.",
         seo="Restaurant deal not working at the counter: what to check",
         keywords="QR code not scanning restaurant, restaurant deal not working, coupon not accepted restaurant, FIG deal troubleshooting, claim restaurant deal problem",
         points=["Most counter problems come from the same few things: a dim screen, a screenshot, the wrong hours or a deal that has reached its daily cap.",
                 "Open your Deals page and tap Show QR yourself. Staff can scan it, or type the short code if a camera will not read the screen.",
                 "A claim has no time limit of its own. It works for as long as the deal runs, so you can claim at home and go when it suits you.",
                 "Check the deal's days, hours, dishes and dine-in or takeout setting before you go. The restaurant sets all of them.",
                 "Stay friendly. The person at the counter wants to apply your deal, and a calm question gets the fastest answer."],
         sections=[
             ("The short answer", """<p>If a FIG deal will not apply at the counter, check three things in this order: that you are showing the current code from your Deals page (not an old screenshot), that the deal is running right now on those days and hours for those dishes, and that it has not reached its daily cap. If the code still will not scan, staff can type the short code.</p>
<p>This guide goes through what to check before you leave, what to try at the till, and how to ask in a way that gets a quick, kind answer.</p>"""),
             ("Before you leave: a 30-second check", """<p>Most problems are easier to fix on your couch than at a busy till. Before you head out:</p>
<ul><li><strong>Open the deal.</strong> Read the days and hours. Many deals run only in quiet hours, such as weekday afternoons and early evenings.</li><li><strong>Check the dishes.</strong> Some deals cover the whole order. Others cover specific dishes from the restaurant's menu.</li><li><strong>Check dine in or takeout.</strong> A dine-in deal is for eating at the restaurant. A deal that also allows takeout is ordered in the app.</li><li><strong>Look at your Deals page.</strong> Your claim should be there, with the deal's name. If it says Expired, the deal ended.</li><li><strong>Charge your phone and turn the screen brightness up.</strong> A dim screen is the most common reason a camera cannot read a code.</li></ul>
<p>A claim has no time limit of its own. It works for as long as the deal runs, so you can claim at home and go when it suits you. <a href="/blog/how-restaurant-deals-work">How a deal works, from claim to counter</a>.</p>"""),
             ("The code will not scan", """<p>Staff scan your code with the restaurant side of FIG on a phone, tablet or computer. If it does not work the first time, try these in order:</p>
<ol><li><strong>Show the current code.</strong> Open your Deals page and tap Show QR. A code works once, so a screenshot or a photo of a code that was already scanned says already used. If the deal can be used more than once, your screen shows a new code after each scan, and some deals ask you to wait a few minutes between uses.</li><li><strong>Raise the brightness</strong> and hold the phone steady, close to the scanner but not touching it. Take off a glare-heavy screen protector if you can.</li><li><strong>Let them try again.</strong> A scanner that is moving, or a lens with a fingerprint on it, often fails once and works the second time.</li><li><strong>Offer the short code.</strong> If a camera will not cooperate, there is a short code that staff can type in instead. Ask if they would like to try that.</li></ol>
<p>None of these steps needs you to be the expert. The staff member at the counter can try the same things, and a restaurant that has trained its team will know what to do. <a href="/blog/train-staff-honour-fig-deal">What restaurants are taught</a>.</p>"""),
             ("What you see, why it happens, and what to do", """<table><thead><tr><th>What you see</th><th>Likely reason</th><th>What to try</th></tr></thead><tbody>
<tr><td>The camera will not read your code</td><td>Dim screen, glare or a screenshot</td><td>Show the current QR from your Deals page, raise the brightness, or ask staff to type the short code</td></tr>
<tr><td>Staff say the deal is not running</td><td>You are outside its days or hours</td><td>Read the deal's days and hours together. Come back in the window, or ask whether the restaurant is willing to honour it as a courtesy</td></tr>
<tr><td>The deal shows as Expired</td><td>The restaurant ended it, or a flash or dated deal is over</td><td>Look for another live deal nearby. Expired claims never count against you</td></tr>
<tr><td>The deal has run out for the day</td><td>The restaurant's daily cap was reached</td><td>Try earlier next time. Popular deals can run out</td></tr>
<tr><td>The dish you want is not covered</td><td>The deal is on specific dishes</td><td>Check the menu on the restaurant's page, or order the covered dish</td></tr>
</tbody></table>
<p>One thing to know: a courtesy is the restaurant's decision. The app tells staff what the deal is, but the owner decides what to do in a gray area, and the answer can reasonably be no.</p>"""),
             ("Check your bill", """<p>A deal should be visible on the receipt. In Ontario, HST (13%) is worked out on the price after the restaurant's own discount, the same way a store coupon lowers the price before tax. So a deal also lowers your tax. This is general information, not tax advice.</p>
<div class="callout math"><b>Example: an $18 dish with $4 off</b><ul><li>$18.00 &minus; $4.00 = $14.00.</li><li>HST at 13% of $14.00 = $1.82.</li><li>You should pay $15.82 for the dish.</li><li>Without the deal it would be $18.00 + $2.34 = $20.34.</li></ul><p>These are round example prices. If your total is closer to $20.34 than $15.82, ask kindly to look at the line. A cleared mistake takes a minute at the till and much longer to fix later.</p></div>"""),
             ("Takeout and pickup problems", """<p>If you ordered takeout with a deal, the deal is already applied in the app, so there is nothing to scan for it. What you need is your pickup code. A few things that help:</p>
<ul><li><strong>Tap I'm here when you arrive.</strong> It tells the restaurant you are outside, and it keeps the order from counting as missed.</li><li><strong>Show your pickup code</strong> so staff can scan it.</li><li><strong>Check the bag</strong> against your order before you leave. Allergies and changes are worth confirming with a quick call. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a>.</li><li><strong>If you will be late</strong>, still tap I'm here when you reach the door. An order that is not picked up closes as Not picked up two hours after the pickup time, and restaurants can see a diner's missed pickups.</li><li><strong>Need to change something?</strong> Call the restaurant. They can also tell you if they are waiting on you.</li></ul>"""),
             ("What to say at the counter", """<p>Staff are juggling a line, a kitchen and a till, and a short, friendly sentence helps them help you. Some examples you can copy and change:</p>
<div class="callout example"><b>Things you can say</b><ul><li>"I claimed the 2-for-1 on FIG. Should I show the code now or when I pay?"</li><li>"The camera is not reading my screen. Could you try the short code?"</li><li>"Is this deal on all the dishes, or only on the noodles?"</li><li>"I think the deal is for weekday afternoons. Is today one of those?"</li></ul></div>
<p>If the answer is no, thank them anyway. Next time, you will know what to look for, and the next person in line will have a better afternoon.</p>"""),
             ("Still stuck? Two ways to follow up", """<p>You can call the restaurant, or contact FIG through the <a href="/contact">contact page</a>. When you call or write, say which deal it was, the day and the time, and what you saw on your screen. A short, factual message helps the restaurant fix its own settings if a deal was posted with the wrong hours.</p>
<p>After a scanned visit you can rate it. Only diners whose visit was scanned can review, so a rating describes a real visit. Rate the food and the visit, and mention the deal if it was handled well. <a href="/blog/how-to-read-restaurant-reviews">How reviews work on FIG</a>.</p>"""),
         ],
         faq=[("Why will my FIG QR code not scan?", "Usually a dim screen, glare or a screenshot. Open your Deals page, tap Show QR, raise the brightness and hold the phone steady. If it still fails, staff can type the short code."),
              ("Can I use a screenshot of my code?", "No. A code works once, so a screenshot of a used code just says already used."),
              ("Why did the restaurant say my deal is not running?", "Each deal has its own days, hours and dishes, set by the restaurant. Check them in the app, and remember a daily cap can end a deal for the day."),
              ("Does an expired claim count against me?", "No. An expired claim shows as Expired on your Deals page for a day and leaves the list. It never counts against you."),
              ("What happens if I miss a takeout pickup?", "An order that is not picked up closes as Not picked up two hours after the pickup time, and restaurants can see missed pickups. Tapping I'm here when you arrive keeps it from counting as missed."),
              ("Who can I ask about a deal that did not work?", "Call the restaurant, or write to FIG through the contact page at www.figpromo.ca/contact. Say which deal, the day and what you saw.")]),

    dict(slug="date-night-markham-deals-budget", screen="map", title="Date night in Markham for less: a plan, with the math", date="2026-10-22", updated="2026-11-05", publish_at="2026-10-22T12:00:00-04:00", topic="For diners", group="fig-in-markham",
         dek="A dinner out for two does not have to cost a lot. How to pick the hour, choose the deal that fits the two of you, check the sums with HST and plan a walk afterwards.",
         desc="A budget-friendly dinner for two in Markham: pick the hour, choose the deal, check the sums with HST and add a walk afterwards.",
         seo="Date night in Markham for less: a plan with deal math",
         keywords="date night Markham, cheap date ideas Markham, dinner for two deals, 2 for 1 dinner Markham, Main Street Unionville dinner, budget dinner for two",
         points=["Go early or midweek. Quiet hours are when restaurants post deals, and you get a calmer table.",
                 "Pick the deal that fits what you would both eat anyway. On the example dinner below, a 2-for-1 on mains beats 20% off the whole bill.",
                 "HST is worked out after the deal, so a deal also lowers the tax. The example dinner drops from $76.84 to $51.98.",
                 "Call ahead to check for a table and to ask about diets. Then claim your deal before you leave.",
                 "Plan something free to do afterwards, such as a walk. Main Street Unionville is a short walk from Toogood Pond."],
         sections=[
             ("The short answer", """<p>The cheapest good date night is an early dinner on a weeknight, with the deal chosen before the restaurant. Look for a deal that covers a main dish each, check the final price with tax, and keep the drinks modest. In the example below, the same dinner for two comes to $76.84 at full price and $51.98 with a 2-for-1 on the mains. FIG is free for diners and open now in Markham.</p>
<p>This is a plan, not a ranking of restaurants. We do not name places here, because the live deals change every day. FIG shows you what is on near you.</p>"""),
             ("Step 1: pick the hour", """<p>Restaurants are busiest at weekend dinner. The rest of the week, many have empty tables earlier in the evening, and an empty table earns nothing, which is why owners post deals then.</p>
<table><thead><tr><th>When</th><th>Why it suits a date</th></tr></thead><tbody>
<tr><td>Monday to Thursday, early dinner</td><td>Before the evening rush. Quieter room, easier conversation, more deals</td></tr>
<tr><td>Weekday late afternoon</td><td>If your schedule allows it, an early meal followed by a walk</td></tr>
<tr><td>Late evening</td><td>After the rush, for dessert and a drink, if the kitchen is still open</td></tr>
<tr><td>Weekend dinner</td><td>The busiest time. Book ahead, and expect fewer deals</td></tr>
</tbody></table>
<p>Every restaurant is different, so treat this as a pattern, not a rule. Each deal on FIG shows its own days and hours. <a href="/blog/restaurant-deals-markham">When Markham restaurants post deals</a>.</p>"""),
             ("Step 2: start from what you both want", """<p>On FIG, you set your cravings, budget and diet once. Home and the map then show live deals from places that fit, nearest first. If one of you is halal, vegetarian, vegan or gluten-free, set that before you look, so every option works for both of you. For allergies, filters are only a starting point, so call the restaurant. <a href="/blog/eating-out-dietary-needs-allergies-markham">What to ask when you call</a>.</p>
<p>Then choose by the dish, not the discount. A deal on something neither of you wanted is not a saving.</p>"""),
             ("Step 3: compare the dinner, not the headline", """<p>Here is a dinner for two with round example prices: one shared starter, one main each and a drink each. Three ways to pay for it:</p>
<div class="callout math"><b>Example dinner for two (before tip)</b><table><thead><tr><th>Plan</th><th>Food and drink</th><th>HST at 13%</th><th>You pay</th></tr></thead><tbody>
<tr><td>No deal: starter $12, two $22 mains, two $6 drinks</td><td>$68.00</td><td>$8.84</td><td>$76.84</td></tr>
<tr><td>20% off the whole bill</td><td>$54.40</td><td>$7.07</td><td>$61.47</td></tr>
<tr><td>2-for-1 on the mains (pay for one $22 main)</td><td>$46.00</td><td>$5.98</td><td>$51.98</td></tr>
</tbody></table><p>Check: 20% of $68.00 is $13.60, so $54.40; HST $7.072 rounds to $7.07. For the 2-for-1: $12 + $22 + $12 = $46; HST is $5.98. The 2-for-1 saves $24.86 against full price, and $9.49 more than 20% off. If you were having two cheap mains and an expensive bottle, the answer would change, so redo it with your order.</p></div>
<p>The tax moves with the price. HST is worked out on what you pay after the restaurant's own discount, the same way a store coupon lowers the price before tax. This is general information, not tax advice. <a href="/blog/compare-restaurant-deals-worth-it">More on comparing deals</a>.</p>"""),
             ("Step 4: check there is a table", """<p>Call the restaurant before you go, especially if you want a quiet corner. Ask whether the deal works for a table for two and whether it applies to the dishes you have in mind. How a deal applies to your order is the restaurant's call, and a thirty-second call is easier than a surprise at the till. If you are dining on a weeknight, a booking is often not needed, but a call costs nothing.</p>"""),
             ("Step 5: claim, go and show your code", """<ol><li>Claim the deal in FIG. Each of you can claim your own if the deal suits you both.</li><li>At the restaurant, order as usual. When it is time to pay, open your Deals page and tap Show QR for staff to scan.</li><li>The deal comes off the bill. You pay the restaurant the way you always do.</li></ol>
<p>A code works once, so a screenshot of a used code will just say already used. <a href="/blog/how-restaurant-deals-work">How deals work, from claim to counter</a>. If something does not scan, <a href="/blog/deal-wont-scan-troubleshooting-diners">here is what to check</a>.</p>"""),
             ("Step 6: keep the extras modest", """<p>Drinks, desserts and sides are usually full price, and they are where a budget evening gets away from you. A few ways to keep it enjoyable:</p>
<ul><li>Share a dessert. Two spoons, one price.</li><li>Pick one drink each, or one to share. Tap water is a fine second round.</li><li>Look at the whole bill before you order, and decide on a number you are comfortable with.</li><li>Tip is your choice. Many people tip on the price before the deal, because the service was the same. That is a personal call, not a rule.</li></ul>"""),
             ("If it is a first date or a special night", """<p>Choose a place where you can talk. Early weeknight dinners are quieter, and a table for two by the window usually helps more than a discount does. If you are unsure of a dish, read the restaurant's page and its reviews first. Only diners whose visit was scanned can review on FIG, so you are reading people who actually ate there. Sort by Newest to see how it is doing now. <a href="/blog/how-to-read-restaurant-reviews">How to read a restaurant's reviews</a>.</p>
<p>It also helps to agree on a rough budget before you leave, so neither of you is guessing at the till. A shared number, such as "about $60 for the dinner", is easier to keep to than a feeling. Then the deal is a pleasant surprise instead of a requirement.</p>"""),
             ("Step 7: add something free", """<p>A date does not end at dessert, and the rest of the evening costs nothing. Main Street Unionville is a historic village street lined with restaurants, pubs and cafés, and Toogood Pond is steps away, which makes it an easy place to walk off a meal. In Markham Village, the old Main Street offers another option, a few kilometres east. Both are free to stroll. If it is raining or cold, a short walk through a plaza or a coffee instead still keeps the evening cheap. <a href="/blog/student-food-deals-markham">Tips on eating out on a budget</a>.</p>"""),
             ("A date-night budget in one table", """<table><thead><tr><th>Item</th><th>Example, no deals</th><th>Example, with deals</th></tr></thead><tbody>
<tr><td>Dinner for two (from above)</td><td>$76.84</td><td>$51.98</td></tr>
<tr><td>Shared dessert, $10 plus HST</td><td>$11.30</td><td>$11.30</td></tr>
<tr><td>A walk</td><td>$0</td><td>$0</td></tr>
<tr><td><strong>Total before tip</strong></td><td><strong>$88.14</strong></td><td><strong>$63.28</strong></td></tr>
</tbody></table>
<p>The saving is $24.86, about 28% of the full-price evening. The dessert is not discounted in this example. Your prices will differ, so use your own.</p>"""),
         ],
         faq=[("What is the cheapest way to do date night in Markham?", "Go early on a weeknight, pick a deal that covers a main each, keep drinks modest and add something free afterwards, such as a walk. FIG shows live deals near you on a map."),
              ("Is a 2-for-1 better than 20% off for two people?", "If you both want a main, usually yes. In the example in this post, a 2-for-1 on $22 mains came to $51.98 against $61.47 for 20% off the whole bill. Redo it with your own order."),
              ("Does a restaurant deal lower the tax?", "Yes. In Ontario, HST is worked out after the restaurant's own discount, so a lower price means less tax. This is general information, not tax advice."),
              ("Do we each need our own deal?", "Each person can claim their own if the deal suits both of you. Codes are personal and work once, so one person's code cannot be used by someone else."),
              ("Should I call the restaurant first?", "A short call helps. Ask if there is a table, whether the deal works for two and whether it covers the dishes you want."),
              ("Can I use FIG in Markham now?", "Yes. FIG is open to diners in Markham, and it is free. Check out deals at www.figpromo.ca/app, with no account needed to look around."),
              ("Is FIG free?", "Yes, for diners. There are no ads for now.")]),

    dict(slug="takeout-rush-pause-prep-time-deals-per-order", screen="tscanner", title="Takeout during a rush: pause, prep time and deals per order", date="2026-10-23", publish_at="2026-10-23T12:00:00-04:00", topic="For restaurants", group="fill-quiet-hours",
         dek="Takeout should fill the kitchen in quiet hours, not hurt the dining room at your peak. How to use pause, prep time and deals per order on FIG, with a simple capacity sum.",
         desc="Keep takeout for your quiet hours: how to use pause, prep time and deals per order on FIG, with a simple capacity sum and fee example.",
         seo="Takeout during a rush: pause, prep time and deals per order",
         keywords="restaurant takeout rush, restaurant kitchen capacity, takeout prep time, pause takeout, takeout orders limit, restaurant takeout Markham, in-app takeout",
         points=["Takeout earns most when it fills spare kitchen time in a quiet hour. At your peak it competes with tables.",
                 "Pause takeout for a set time or until tomorrow, or add prep time, in one tap. Diners see it before they order.",
                 "Set deals per order: 0 means takeout at full price, and a limit stops a large order stacking discounts.",
                 "Work out spare capacity before you promote takeout: plates per hour minus what dine-in already uses.",
                 "An $18 order after the deal leaves about $16.21 after FIG's 5% and Stripe's fee. Run your own sum on your dishes."],
         sections=[
             ("The short answer", """<p>Use takeout to fill spare kitchen time, not to compete with your busiest tables. On FIG you control this with three settings: pause takeout (for a set time or until tomorrow), add prep time so pickup times stay honest, and choose how many deals one order can use. Before you promote takeout, work out how many extra plates your kitchen can make in a quiet hour, and set your limits to that number.</p>
<p>Takeout paid in the app needs your HST number and Stripe payouts. On each order FIG keeps 5% of the food before tax and Stripe's card fee comes off the same payment. This post focuses on keeping it manageable.</p>"""),
             ("Why a rush needs its own plan", """<p>A diner who sits down at 6 pm and a diner who orders takeout at 6 pm are both asking the same cooks for food. The seated diner may also order drinks and dessert, and pays you at the counter with no per-order fee to FIG. At a busy time, a takeout order can slow the room you would have filled anyway.</p>
<p>In a quiet hour the opposite holds. The cooks are standing there, the food is prepped and the tables are empty. Takeout lets that capacity earn. The settings below let you aim it at the second case and keep it away from the first.</p>"""),
             ("Know your spare capacity", """<p>You do not need software for this. Pick one quiet window and think about it in plates per hour.</p>
<div class="callout math"><b>Example: a 2 to 5 pm window</b><ul><li>Two cooks. A typical bowl takes about 6 minutes of one cook's time (an example, so time your own).</li><li>One cook can make 60 ÷ 6 = 10 bowls an hour, so two can make 20.</li><li>Dine-in in this window uses about 8 bowls an hour (count your own from receipts).</li><li>Spare capacity: 20 &minus; 8 = 12 bowls an hour.</li><li>Over the 3 hours: about 36 bowls of spare capacity.</li></ul><p>Keep a margin. If you plan to use only 8 or 9 of those 12 an hour, a sudden table of six will not sink the kitchen.</p></div>
<p>Compare that with a daily cap on the deal. If your cap is 15 a day, and some of those are dine-in claims, the takeout share is probably well within your spare capacity. If the cap is 60, check again. <a href="/blog/slow-hour-deal-math">How to size a cap</a>.</p>"""),
             ("Tool 1: pause takeout", """<p>When the dining room fills, stop new orders in one tap. You can pause for a set time or until tomorrow, and diners see that takeout is paused before they order. Orders already accepted still need to be made, so pause a little earlier than you think you need to.</p>
<p>A good rule: pause when the dining room is more than about two thirds full, or when two or more orders are waiting longer than you promised. Choose your own number and tell the team.</p>"""),
             ("Tool 2: add prep time", """<p>Prep time is the honest version of "we are busy". Instead of pausing, add minutes so diners see the real wait before they order. A diner who knows pickup is in 25 minutes will plan for it. A diner who expects 15 and waits 25 will be unhappy, whatever the food is like.</p>
<table><thead><tr><th>Situation</th><th>Try</th></tr></thead><tbody>
<tr><td>Quiet hour, kitchen idle</td><td>Takeout on, normal prep time</td></tr>
<tr><td>Getting busy, still coping</td><td>Add 10 minutes of prep time</td></tr>
<tr><td>Dining room full, kitchen stretched</td><td>Pause takeout for an hour, or until tomorrow</td></tr>
<tr><td>Short on one ingredient</td><td>Mark that dish sold out for today and leave the rest on</td></tr>
</tbody></table>
<p>The numbers here are suggestions to adapt: you know your kitchen best.</p>"""),
             ("Tool 3: deals per order", """<p>You choose how many deals one order can use. That setting does two jobs.</p>
<ul><li><strong>A limit.</strong> A low limit stops a large order stacking several discounts. For percentage deals you can also set the most one takeout order can take off, so 20% of a very large order cannot run away.</li><li><strong>0 deals per order</strong> means diners can order takeout at full price, with no deal needed. Otherwise takeout comes with a deal. Full-price takeout can suit your quiet hours too, since you are not giving anything away.</li></ul>
<div class="callout math"><b>Example: a worst case with a limit</b><p>If you allow one $4-off deal per order and cap the deal at 10 takeout orders in the window, the most you can give away to takeout is 10 &times; $4 = $40. With no limit, one large order could use four deals: $16 from a single pickup. Pick the number that makes the worst case a figure you shrug at.</p></div>"""),
             ("What an order leaves you", """<p>Here is one takeout order, after the deal, as a reminder of the fees. Round example numbers:</p>
<div class="callout math"><b>An $18 order after the deal</b><table><thead><tr><th></th><th>Amount</th></tr></thead><tbody>
<tr><td>Food after the deal</td><td>$18.00</td></tr>
<tr><td>HST at 13%</td><td>$2.34</td></tr>
<tr><td>The diner pays</td><td>$20.34</td></tr>
<tr><td>Stripe: 2.9% of $20.34 + $0.30</td><td>&minus;$0.89</td></tr>
<tr><td>FIG: 5% of $18.00</td><td>&minus;$0.90</td></tr>
<tr><td><strong>You keep from the food</strong></td><td><strong>$16.21</strong></td></tr>
</tbody></table><p>The HST ($2.34) is paid out to you and is yours to remit. Food cost comes off the $16.21, and the rest goes toward wages, rent and profit. This is general information, not tax advice.</p></div>
<p>More order sizes, side by side: <a href="/blog/takeout-order-math-what-you-keep">takeout order math on $12, $20, $40 and $60</a>.</p>"""),
             ("Missed pickups", """<p>Diners tap I'm here when they arrive and show a pickup code. An order that is not picked up closes as Not picked up two hours after the pickup time. You can see a diner's missed pickups, which helps you decide how much to cook ahead. For dishes that lose quality while they wait, such as fried food, start cooking when the diner taps I'm here if your pickup time allows. For soups and braises that hold well, cooking ahead is fine.</p>"""),
             ("A short example of a busy Friday", """<p>Suppose a restaurant has takeout on during a quiet afternoon, with normal prep time. At 5:15 pm the dining room starts to fill and two takeout orders are already waiting. The manager adds 10 minutes of prep time at once, so new orders show the longer wait. At 5:45 pm the room is nearly full, so the manager pauses takeout until 7:30 pm. The two orders that were accepted are still made. At 7:30 pm takeout comes back on. Nothing was lost: the afternoon was filled, the rush was protected, and every diner who ordered saw an honest pickup time. This is an example, not a rule. Choose your own times from your own receipts.</p>"""),
             ("Tell your team", """<p>Before the shift, make sure every person knows who can pause takeout, what number triggers adding prep time, and where the pickup shelf is. A card by the till with those three answers saves arguments. <a href="/blog/train-staff-honour-fig-deal">A ten-minute staff plan</a>. Not set up for takeout yet? You need your HST number and Stripe payouts in Settings → Get paid. <a href="/blog/set-up-fig-menu-takeout">Setup takes about 15 minutes</a>, and <a href="/blog/hst-registration-small-restaurants-ontario">HST registration for small restaurants</a> explains the number.</p>"""),
         ],
         faq=[("Can I stop takeout when my kitchen is busy?", "Yes. Pause takeout for a set time or until tomorrow, or add prep time, in one tap. Diners see it before they order."),
              ("What does prep time do?", "It adds minutes to the pickup time, so diners see an honest wait before they order."),
              ("Can I offer takeout without a deal?", "Yes. If you set 0 deals per order, diners can order takeout at full price. Otherwise takeout comes with a deal."),
              ("How do I stop a big order stacking discounts?", "Set how many deals one order can use. For percentage deals you can also set the most one takeout order can take off."),
              ("What does a takeout order cost me?", "FIG keeps 5% of the food before tax and Stripe's card fee of 2.9% + $0.30 comes off the same payment. The HST is paid out to you and is yours to remit."),
              ("What happens if a diner does not pick up?", "The order closes as Not picked up two hours after the pickup time. You can see a diner's missed pickups."),
              ("What do I need to take takeout orders?", "Your HST number and Stripe payouts, both in Settings → Get paid. Dine-in deals need neither.")]),
    # ---------------------------------------------------------------- batch of 4 queued posts (publish_at: hidden until then)

    dict(slug="family-dinner-out-markham-deals-budget", screen="claim", title="Family dinner out in Markham for less: a plan for four, with the math", date="2026-10-24", publish_at="2026-10-24T12:00:00-04:00", updated="2026-11-05", topic="For diners", group="fig-in-markham",
         dek="Eating out with kids does not have to cost a lot. How to pick an early table, choose the deal that fits a family of four, check the sums with HST and keep the extras in check.",
         desc="A budget plan for a family dinner in Markham: pick the hour, choose the deal, check the sums with HST and keep drinks and extras modest.",
         seo="Family dinner out in Markham for less: a plan with deal math",
         keywords="family dinner deals Markham, eating out with kids, cheap family restaurants Markham, restaurant deals for families, family meal budget, 2 for 1 dinner family",
         points=["Go early on a weeknight. Quiet hours are when restaurants post deals, and a calmer room is easier with children.",
                 "Choose the deal by the final price for your whole order. In the example below, a 2-for-1 on adult mains brings a family of four from $67.80 to $49.72.",
                 "HST is worked out after the restaurant's own discount, so a deal also lowers the tax you pay.",
                 "Call ahead to check for a table and to ask how the deal applies to a shared bill. That answer is the restaurant's call.",
                 "Keep drinks and extras modest, and decide on a rough total before you leave home."],
         sections=[
             ("The short answer", """<p>The cheapest good family dinner is an early weeknight meal, with the deal chosen before the restaurant. Look for a deal that covers the adult mains, work out the final price for the whole table including tax, and keep the drinks simple. In the example below, the same dinner for four comes to $67.80 at full price and $49.72 with a 2-for-1 on the two adult mains. FIG is free for diners and open now in Markham.</p>
<p>This is a plan, not a ranking of restaurants. We do not name places here, because live deals change every day. FIG shows what is on near you.</p>"""),
             ("Step 1: pick an early table", """<p>Restaurants are busiest at weekend dinner. The rest of the week, many have empty tables in the early evening, and an empty table earns nothing, which is why owners post deals then. For a family it helps twice: more deals, and a quieter room when children are hungry and tired.</p>
<table><thead><tr><th>When</th><th>Why it suits a family</th></tr></thead><tbody>
<tr><td>Monday to Thursday, early dinner</td><td>Before the evening rush. Quieter room, faster kitchen, more deals</td></tr>
<tr><td>Weekday late afternoon</td><td>An early meal on a day off school or work, with the evening left free</td></tr>
<tr><td>Weekend lunch</td><td>Busier than a weekday, but easier on small children than a late dinner</td></tr>
<tr><td>Weekend dinner</td><td>The busiest time. Call ahead, and expect fewer deals</td></tr>
</tbody></table>
<p>Every restaurant is different, so treat this as a pattern, not a rule. Each deal on FIG shows its own days and hours. <a href="/blog/restaurant-deals-markham">When Markham restaurants post deals</a>.</p>"""),
             ("Step 2: start from what everyone will eat", """<p>On FIG, you set your cravings, budget and diet once. Home and the map then show live deals from places that fit, nearest first. If one of you is halal, vegetarian, vegan or gluten-free, set that before you look. Then ask the picky eater to choose between two or three options, instead of an open question. Sharing one concrete restaurant to the family chat works better than "where should we eat?". <a href="/blog/group-dining-deals">More on deciding as a group</a>.</p>
<p>A deal on a dish nobody wanted is not a saving. Look for the deal that matches what the family would have ordered anyway.</p>"""),
             ("Step 3: compare the whole dinner", """<p>Here is a dinner for a family of four with round example prices: one shared starter at $10, two adult mains at $16 and two children's mains at $9, with water to drink. Four ways to pay for it:</p>
<div class="callout math"><b>Example dinner for four (before tip)</b><table><thead><tr><th>Plan</th><th>Food</th><th>HST at 13%</th><th>You pay</th></tr></thead><tbody>
<tr><td>No deal</td><td>$60.00</td><td>$7.80</td><td>$67.80</td></tr>
<tr><td>$3 off each adult main</td><td>$54.00</td><td>$7.02</td><td>$61.02</td></tr>
<tr><td>20% off the whole bill</td><td>$48.00</td><td>$6.24</td><td>$54.24</td></tr>
<tr><td>2-for-1 on the adult mains (pay for one $16 main)</td><td>$44.00</td><td>$5.72</td><td>$49.72</td></tr>
</tbody></table><p>Check: $10 + $32 + $18 = $60. 20% of $60 is $12, so $48. The 2-for-1 takes off one $16 main, leaving $44. The 2-for-1 saves $18.08 against full price, and $4.52 more than 20% off. At full price the dinner is $16.95 a person; with the 2-for-1 it is $12.43 a person. If the children ordered the expensive dishes and the adults the cheap ones, the answer would change, so redo it with your own order.</p></div>
<p>The tax moves with the price. HST is worked out on what you pay after the restaurant's own discount, the same way a store coupon lowers the price before tax. This is general information, not tax advice. <a href="/blog/compare-restaurant-deals-worth-it">More on comparing deals</a>.</p>"""),
             ("Step 4: who claims the deal?", """<p>A claim on FIG is used once, and each phone has its own code, so it only works for the person who claimed it. Children often do not have phones, so decide before you go. Two simple ways: each adult claims one deal, or you call the restaurant and ask how it applies to a table with children. How a deal applies to a shared bill is the restaurant's call, and a short call is easier than a surprise at the till. <a href="/blog/how-restaurant-deals-work">How a deal works, from claim to counter</a>.</p>"""),
             ("Step 5: call before you go", """<p>Phone the restaurant and ask three things: is there a table for four at that time, does the deal cover the dishes you have in mind, and is there anything for the children that suits them. If anyone has an allergy, say so on the call and again when you order. Filters are a starting point, not a guarantee. This is general information, not medical advice. <a href="/blog/eating-out-dietary-needs-allergies-markham">What to ask about diets and allergies</a>.</p>
<p>Call earlier in the day. A kitchen at 6 pm may not have time to talk, and a quieter hour is better for questions as well as for deals.</p>"""),
             ("Step 6: keep the extras modest", """<p>Drinks, desserts and sides are usually full price, and they are where a family dinner gets away from you. A few habits that help:</p>
<ul><li>Water for the table, and one drink each only if you would have bought it anyway.</li><li>One dessert to share, with a spoon each.</li><li>Order the starter once and see how hungry everyone is before adding more.</li><li>Agree a rough total before you leave home. "About $55" is easier to keep to than a feeling.</li></ul>
<div class="callout example"><b>Example: the same dinner with extras</b><p>Add one shared dessert at $10 to the 2-for-1 dinner. Food is $54.00, HST is $7.02 and the bill is $61.02. The dessert added $11.30 with tax, which is more than half of the $18.08 the deal saved you on the mains, so it is a choice worth making on purpose. Your prices will differ.</p></div>"""),
             ("Step 7: tipping and splitting", """<p>Tip is your choice. Many people tip on the price before the deal, because the service was the same. That is a personal call, not a rule. If two families are sharing a table, agree how to split before the food arrives: evenly is simplest, and paying for what you ordered is fairest. <a href="/blog/group-dining-deals">Splitting the bill fairly, with the arithmetic</a>.</p>"""),
             ("Step 8: take it home if the evening is too hard", """<p>Some nights the family is too tired for a restaurant. If a deal allows takeout, you can order from the menu in the app, pay there and pick it up. There is no delivery fee and FIG adds no service fee. You pay the menu price minus the deal, plus tax, and you can eat at home in pyjamas. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a>.</p>"""),
             ("Something free afterwards", """<p>Main Street Unionville is a historic village street with restaurants, pubs and cafés, and Toogood Pond is steps away, which makes it an easy place for children to stretch their legs after dinner. Markham Village has its own old Main Street, a few kilometres east. A short walk costs nothing and tires out small people before bedtime.</p>"""),
             ("A quick checklist", """<ol><li>Pick an early weeknight and two or three places.</li><li>Work out the final price for your whole order under each deal.</li><li>Decide who claims, and call to check how it applies to your table.</li><li>Agree a rough total, including drinks and dessert.</li><li>After a scanned visit, rate it. Only diners whose visit was scanned can review, so your review helps the next family. <a href="/blog/how-to-read-restaurant-reviews">How reviews work</a>.</li></ol>"""),
         ],
         faq=[("What is the cheapest way to eat out as a family in Markham?", "Go early on a weeknight, pick a deal that covers the adult mains, work out the final price with tax and keep drinks and extras modest. FIG shows live deals near you on a map, and it is free for diners."),
              ("Is a 2-for-1 better than 20% off for a family?", "It depends on the order. In the example in this post, a 2-for-1 on two $16 adult mains came to $49.72 against $54.24 for 20% off the whole bill. Redo the sum with your own order."),
              ("Do children need their own deal?", "A claim is used once and the code only works on the phone of the person who claimed it. Call the restaurant to ask how a deal applies to a table with children."),
              ("Does a restaurant deal lower the tax?", "Yes. In Ontario, HST is worked out after the restaurant's own discount, so a lower price means less tax. This is general information, not tax advice."),
              ("Can I order takeout instead?", "If the restaurant allows takeout with that deal, yes. You order from the menu in the app, pay there and pick it up, with no delivery or service fee from FIG."),
              ("What if someone in the family has an allergy?", "Use FIG's diet filters to shortlist places, then call the restaurant and tell the server again when you order. Filters are a starting point, not a guarantee."),
              ("Can I use FIG in Markham now?", "Yes. FIG is open to diners in Markham, and it is free. Check out deals at www.figpromo.ca/app, with no account needed to look around.")]),

    dict(slug="takeout-or-dine-in-with-a-deal-which-costs-less", screen="qr", title="Takeout or dine-in with a deal: which costs you less?", date="2026-10-26", publish_at="2026-10-26T12:00:00-04:00", updated="2026-11-05", topic="For diners", group="takeout-and-money",
         dek="The same dish can cost different amounts depending on how you eat it. A side-by-side of dine-in and takeout with a deal, with the HST, the drink, the tip and the trip worked out.",
         desc="Takeout or dine-in with a deal? The same dish compared with HST, drinks, tip and travel, so you can pick the cheaper night out or in.",
         seo="Takeout or dine-in with a deal: which costs less?",
         keywords="takeout vs dine-in cost, takeout deals Markham, is takeout cheaper than eating out, pickup vs dine in, restaurant deal takeout, no delivery fee",
         points=["On FIG, takeout means you order in the app, pay there and pick it up. There is no delivery fee and FIG adds no service fee.",
                 "For one $18 main with $4 off, takeout comes to $15.82. Dine-in with a drink and a 15% tip comes to $23.04 in the example below.",
                 "The deal itself is worth the same either way. The gap comes from drinks, tip, parking and what else you order.",
                 "Takeout is only available with a deal, unless the restaurant sets 0 deals per order. Then takeout is at full price.",
                 "Dine-in is a different thing, not just a dearer one: you get the room, the service and the time."],
         sections=[
             ("The short answer", """<p>For the same dish and the same deal, takeout is usually the cheaper way to eat, because you skip the drink, the tip and the table time. In the example below, one $18 main with $4 off costs $15.82 as takeout and $23.04 as a dine-in meal with a drink and a 15% tip. The deal is worth the same either way. What changes is everything around it. This post works out where the difference comes from, so you can decide with your own prices.</p>
<p>FIG is free for diners and open now in Markham. Check out deals at www.figpromo.ca/app.</p>"""),
             ("What each way means on FIG", """<table><thead><tr><th></th><th>Dine-in with a deal</th><th>Takeout with a deal</th></tr></thead><tbody>
<tr><td>How you use the deal</td><td>Show your QR code at the restaurant and staff scan it</td><td>Tap Takeout on the deal, add dishes from the menu and pay in the app</td></tr>
<tr><td>How you pay</td><td>The restaurant, the way you always do</td><td>In the app, by card</td></tr>
<tr><td>Fees from FIG</td><td>None</td><td>No delivery fee and no service fee</td></tr>
<tr><td>Which deals</td><td>Any live deal</td><td>Only deals the restaurant allows as takeout</td></tr>
<tr><td>Full price</td><td>You can order anything on the menu</td><td>Takeout needs a deal, unless the restaurant sets 0 deals per order. Then takeout is at full price</td></tr>
</tbody></table>
<p>FIG does not deliver. You pick the order up yourself. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a> and <a href="/blog/how-restaurant-deals-work">how a deal works from claim to counter</a>.</p>"""),
             ("One dish, three ways", """<p>Take an $18 main with a $4-off deal, and round example prices. Ontario HST is 13%, and it is worked out on the price after the restaurant's own discount, the same way a store coupon lowers the price before tax. This is general information, not tax advice.</p>
<div class="callout math"><b>One $18 main with $4 off (example)</b><table><thead><tr><th>Way</th><th>Food and drink</th><th>HST at 13%</th><th>Tip (your choice)</th><th>You pay</th></tr></thead><tbody>
<tr><td>Takeout with the deal</td><td>$14.00</td><td>$1.82</td><td>none</td><td>$15.82</td></tr>
<tr><td>Dine-in with the deal, plus a $4 drink</td><td>$18.00</td><td>$2.34</td><td>15% of $18.00 = $2.70</td><td>$23.04</td></tr>
<tr><td>Takeout at full price (0 deals per order)</td><td>$18.00</td><td>$2.34</td><td>none</td><td>$20.34</td></tr>
</tbody></table><p>Check: $18.00 &minus; $4.00 = $14.00; 13% of $14.00 is $1.82. Dine-in: $14.00 + $4.00 = $18.00; 13% is $2.34; $18.00 + $2.34 + $2.70 = $23.04. A tip is a personal decision, and the 15% on the after-deal subtotal is only an example.</p></div>
<p>The deal saved $4.00 plus $0.52 of tax in both of the first two rows. The $7.22 gap between them is the drink, the tax on the drink, and the tip.</p>"""),
             ("What dine-in gives you that takeout cannot", """<p>Cheaper is not always better. Dine-in gives you the food made and served at its best, the room, someone else doing the dishes, and time with the people you are with. A cold bowl of noodles carried home in a bag is not the same dish. If the meal is the point of your evening, such as a date or a family night, the extra cost is the price of the evening. <a href="/blog/date-night-markham-deals-budget">A date night plan, with the math</a> and <a href="/blog/family-dinner-out-markham-deals-budget">a family dinner plan</a> go through that kind of meal.</p>
<p>Takeout suits a different night: you are tired, you want to eat at home, or you only have twenty minutes.</p>"""),
             ("Count the trip too", """<p>The price on the menu is not the only cost of getting food. Both ways, you travel to the restaurant. For takeout, you also carry the food home, and some dishes lose quality on the way.</p>
<ul><li><strong>Parking or transit.</strong> If you pay for either, add it to both columns. It is the same trip, but for takeout it can feel like a lot for a quick pickup.</li><li><strong>Travel time.</strong> A 15-minute drive each way is 30 minutes. That matters more for a $14 pickup than for a long dinner out.</li><li><strong>Food that travels.</strong> Fried food and noodles in broth are best eaten fresh. Dumplings, curries and rice dishes usually travel well.</li><li><strong>Walking.</strong> A pickup from a restaurant in your own plaza is nearly free. A 20-minute drive for the same bag is not.</li></ul>"""),
             ("Which deals work for takeout", """<p>Only deals the restaurant has allowed as takeout show the Takeout button, usually marked Dine in or takeout. A deal that is dine-in only is for eating at the restaurant. Restaurants can also limit how many deals one order can use, so a big order may not stack discounts. If you are unsure, call before you go. <a href="/blog/compare-restaurant-deals-worth-it">How to compare restaurant deals</a>.</p>"""),
             ("Order for two or for a group", """<p>The comparison shifts when more people are involved. A pickup for four is one trip, one payment and one person doing the carrying, and the fixed costs spread out. A dine-in meal for four costs more in drinks and tip, but the people are together.</p>
<div class="callout math"><b>Example: two $16 mains on a 2-for-1</b><ul><li>Takeout: pay for one $16 main, $16.00. HST $2.08. Total $18.08, so $9.04 each.</li><li>Dine-in: $16.00, plus two $4 drinks, $24.00. HST $3.12. Tip at 15% of $24.00 is $3.60. Total $30.72, so $15.36 each.</li></ul><p>These are round example prices. Your own order, your own drinks and your own tip will give different totals. The gap is $12.64 for the two of you.</p></div>"""),
             ("Missed pickups and being on time", """<p>Takeout has one rule that dine-in does not. Tap I'm here when you arrive, and show your pickup code. An order that is not picked up closes as Not picked up two hours after the pickup time, and restaurants can see a diner's missed pickups. Order when you are ready to leave, and the food is best the moment it is made. If something goes wrong at the counter, <a href="/blog/deal-wont-scan-troubleshooting-diners">here is what to check and what to say</a>.</p>"""),
             ("Allergies and special requests", """<p>On takeout you cannot ask the server at the table, so call the restaurant right after you order to mention allergies or changes, and check the bag against your order before you leave. Filters are a starting point, not a guarantee. This is general information, not medical advice. <a href="/blog/eating-out-dietary-needs-allergies-markham">What to ask about diets and allergies</a>.</p>"""),
             ("A simple way to decide", """<ol><li>Is the meal the point of the evening? If yes, dine in.</li><li>Is it a quick feed at home? Takeout.</li><li>Work out both totals with your own prices, including drinks and tip.</li><li>Check that the deal allows takeout, and that the dish will survive the trip.</li><li>Claim the deal before you leave. A claim stays until the deal ends.</li></ol>"""),
         ],
         faq=[("Is takeout cheaper than dining in?", "Usually, for the same dish and deal, because you skip drinks, tip and table time. In this post's example, $15.82 for takeout against $23.04 for dine-in with a drink and a 15% tip. Your prices will differ."),
              ("Does FIG charge a delivery or service fee on takeout?", "No. FIG does not deliver, so there is no delivery fee, and FIG adds no service fee. You pay the menu price minus the deal, plus tax."),
              ("Can I order takeout without a deal?", "Only if the restaurant sets 0 deals per order. Then takeout is at full price. Otherwise takeout comes with a deal."),
              ("How do I pay for takeout on FIG?", "In the app, by card, when you order. Dine-in deals are paid at the restaurant as usual."),
              ("Is HST charged before or after the deal?", "After the restaurant's own discount, the same way a store coupon lowers the price before tax. This is general information, not tax advice."),
              ("What if I cannot pick up my order?", "An order not picked up closes as Not picked up two hours after the pickup time, and restaurants can see missed pickups. Tap I'm here when you arrive."),
              ("Can I use FIG in Markham now?", "Yes. FIG is open to diners in Markham, and it is free. Check out deals at www.figpromo.ca/app, with no account needed to look around.")]),

    dict(slug="reply-to-reviews-restaurants", screen="map", title="Replying to reviews: a short guide for restaurant owners", date="2026-10-27", publish_at="2026-10-27T12:00:00-04:00", updated="2026-11-05", topic="For restaurants", group="fill-quiet-hours",
         dek="How to answer a review in a few minutes a week: what to say to a good review, a bad one and a rating with no words, with templates you can adapt and a little arithmetic on what one low rating does.",
         desc="How restaurant owners can reply to reviews on FIG in minutes a week, with templates and the arithmetic of one low rating.",
         seo="Replying to restaurant reviews: a short guide for owners",
         keywords="reply to restaurant reviews, respond to bad review restaurant, review reply templates, restaurant reputation, review response examples, Markham restaurants, FIG reviews",
         points=["Reviews on FIG come only from diners whose visit was scanned, so each one is about a real visit. You can reply in public.",
                 "Reviews show the diner's first name and last initial. You never see a diner's phone number or email.",
                 "Answer in a few lines: thank, be specific, say what you will do, and keep it calm. Write for the next reader, not just the writer.",
                 "One low rating moves the average less than it feels like. Ten 5-star reviews and one 1-star give 4.64; thirty and one give 4.87.",
                 "Paying FIG never hides, changes or reorders a review. A fair reply is the only tool you have, and it is a good one."],
         sections=[
             ("The short answer", """<p>Reply to every review with the same four steps: thank the person, name something specific, say what you will do if there is something to fix, and stop. Keep it to a few lines and write it for the next person who reads it, because most readers are future diners deciding whether to come. On FIG, reviews come only from diners whose visit was scanned, and you can reply in public. Ten minutes a week is enough for most small restaurants.</p>
<p>The examples below are templates to adapt. They are not quotes from real diners or real restaurants.</p>"""),
             ("What you can and cannot see", """<table><thead><tr><th>On FIG</th><th>What it means for you</th></tr></thead><tbody>
<tr><td>Reviews come only from scanned visits</td><td>Each review is about a real visit, one per visit. You are not answering people who never came</td></tr>
<tr><td>Restaurants get stars, deals get likes</td><td>A low star rating is about the visit. A low-liked deal is about the offer. Reply to each on its own terms</td></tr>
<tr><td>You can reply in public</td><td>Everyone who reads the review reads your answer too</td></tr>
<tr><td>You see a first name and last initial</td><td>Never a phone number or email. Do not ask for contact details to resolve something</td></tr>
</tbody></table>
<p>Paying FIG never hides, changes or reorders a review. You cannot remove a review you dislike, which is exactly why diners can trust the ones they read. <a href="/blog/how-to-read-restaurant-reviews">How diners read a page</a>.</p>"""),
             ("Why replies matter more than the rating", """<p>A calm, specific reply to a bad review tells a future diner more about your restaurant than ten five-star ratings do. They are reading to find out two things: is the food good, and what happens when something goes wrong. A good answer to the second question can win a diner who would otherwise skip you.</p>
<p>The reader to write for is not the person who complained. That person has already decided. It is the stranger scrolling at 5 pm, deciding where to eat.</p>"""),
             ("What a diner sees next to your reply", """<p>At the top of your reviews a diner sees the average, the number of reviews and five bars from 5 stars down to 1. They can sort by Newest, to see how you are doing now, or by Lowest, to see what goes wrong when it goes wrong. Our guide for diners suggests reading a couple of the low ones and how the restaurant replied, so that is where your reply does the most work. Read yours as a stranger would. <a href="/blog/how-to-read-restaurant-reviews">How diners read a restaurant's reviews</a>.</p>"""),
             ("The arithmetic of one low rating", """<p>It helps to know how much a single low review moves your average, so a bad night does not feel bigger than it is.</p>
<div class="callout math"><b>One 1-star review among 5-star reviews (example)</b><table><thead><tr><th>Reviews so far</th><th>Total stars</th><th>Average before</th><th>Average after one 1-star</th></tr></thead><tbody>
<tr><td>4 reviews, all 5 stars</td><td>20</td><td>5.00</td><td>21 &divide; 5 = 4.20</td></tr>
<tr><td>10 reviews, all 5 stars</td><td>50</td><td>5.00</td><td>51 &divide; 11 = 4.64</td></tr>
<tr><td>30 reviews, all 5 stars</td><td>150</td><td>5.00</td><td>151 &divide; 31 = 4.87</td></tr>
</tbody></table><p>These are round example numbers. A new restaurant feels one bad review a lot. A restaurant with many reviews barely moves. Either way, the bars show the whole shape of your ratings, not just the average, and the reply shows what you do about it.</p></div>"""),
             ("Replying to a good review", """<p>A good review is easy to answer and easy to get wrong. Avoid a copy-and-paste "Thanks for your feedback!" every time. Three lines are enough.</p>
<div class="callout example"><b>Template</b><p>"Thank you, [first name]. We are glad you enjoyed the [dish you named]. We hope to see you again on a quiet afternoon."</p></div>
<p>Name the dish or the detail they mentioned. If they praised a team member, pass it on and say you did. Do not offer a discount in the reply: let the deal speak for itself.</p>"""),
             ("Replying to a bad review", """<p>Take a breath before you type. A reply written in anger lives on the page for years.</p>
<ol><li><strong>Thank and acknowledge.</strong> "Thank you for telling us, [first name]. We are sorry the wait was long."</li><li><strong>Be specific, not defensive.</strong> Say what you understand happened: "A tour group arrived at the same time as the lunch rush." One sentence of context is fine. A paragraph of excuses is not.</li><li><strong>Say what changes.</strong> "We now add prep time when the room fills, so wait times are honest." If nothing will change, do not promise it.</li><li><strong>Invite them back, once.</strong> "We would like another chance." Then stop.</li></ol>
<div class="callout example"><b>Template for a low rating about service</b><p>"Thank you for telling us, [first name]. We are sorry the service was slow on your visit. We were short-staffed that evening and should have said so at the door. We have since changed how we handle busy nights. We hope you will give us another try."</p></div>
<p>Do not argue facts in public, do not name staff, and do not share anything about the diner's order beyond what they wrote. If the review is unfair, one calm correction is enough, such as "Our kitchen is closed on Mondays, so we think this may be about another restaurant."</p>"""),
             ("Replying to a rating with no words", """<p>A diner on FIG picks the stars and can add a few words or a photo if they like, so some reviews are only a rating. One line is enough for a good one. For a low rating with no words, do not guess what went wrong: say you are sorry the visit fell short, say you would like to do better, and stop. A long reply to a silent one-star rating reads as defensive.</p>
<div class="callout example"><b>Template for a low rating with no words</b><p>"Thank you for rating your visit, [first name]. We are sorry it fell short, and we would like another chance to get it right."</p></div>
<p>If the review has a photo, thank them for it and talk about the dish, not the diner.</p>"""),
             ("When a review is really about the deal", """<p>Restaurants get stars and deals get likes, so a star rating is about the visit. Diners still sometimes use their words to talk about the offer: "the 2-for-1 only covered one dish." Each deal shows its days, hours and dishes, so your reply can say what the deal covers, once, in plain words. If it was unclear, say so, and fix the deal's wording, because the next diner will read it the same way.</p>
<div class="callout example"><b>Template for a review that misread the deal</b><p>"Thank you, [first name]. We are sorry the deal was not clear. It covers the [dish] on [days] between [hours], and we have made that easier to see."</p></div>"""),
             ("How much time it takes", """<div class="callout math"><b>Example: a weekly routine</b><ul><li>5 reviews a week, about 3 minutes each: 15 minutes.</li><li>15 minutes &times; 52 weeks = 780 minutes, or 13 hours a year.</li><li>If a dull week has none, you spend none.</li></ul><p>Use your own volume. Most small restaurants will have fewer, especially at first.</p></div>
<p>Set a time. Ten minutes at the end of a Tuesday shift is better than a hundred good intentions. Give one person ownership, and a second for holidays.</p>"""),
             ("A reply checklist", """<ol><li>Did I thank them by first name?</li><li>Did I mention something specific from their review?</li><li>Am I writing for the next reader as well as for them?</li><li>Did I avoid blaming the diner or the staff?</li><li>If there is something to fix, did I say what I will do, and will I do it?</li><li>Is it short enough to read in ten seconds?</li></ol>"""),
             ("Turn feedback into changes", """<p>Over a month, patterns show up. Three people say the wait was long on Thursdays? Look at your staffing, or add takeout prep time. Several diners ask about the same deal? Make the details clearer. A deal nobody likes after two weeks? Change the dish or the hours. Your insights show views, claims and the diners who came back, and your reviews tell you why. <a href="/blog/slow-hour-deal-math">How to judge a deal by new and returning diners</a>. <a href="/blog/train-staff-honour-fig-deal">A ten-minute staff plan</a> can fix a lot of counter problems before they become reviews.</p>
<p>FIG is open to diners in Markham, and reviews come only from scanned visits, so yours start with your first diners. If you are still setting up, add your page and menu first.</p>"""),
         ],
         faq=[("Can I reply to reviews on FIG?", "Yes. Restaurants can reply to reviews in public."),
              ("Can I delete a bad review?", "No. Paying FIG never hides, changes or reorders a review. Reviews come only from diners whose visit was scanned."),
              ("Who can leave a review?", "Only diners whose visit was scanned, one review per visit. Reviews show the diner's first name and last initial."),
              ("Can I reply to a rating that has no words?", "Yes. Restaurants can reply to reviews in public. For a rating with no words, keep it to a line or two and do not guess what went wrong."),
              ("How should I answer a bad review?", "Thank them, be specific, say what you will change and invite them back once. Keep it calm and short, and write for the next reader."),
              ("How much does one low rating change my average?", "Less than it feels like. In the example in this post, one 1-star among ten 5-star reviews gives 4.64, and among thirty gives 4.87."),
              ("Should I offer a discount in a reply?", "Usually not. Let the deal speak for itself, and focus on what you will fix.")]),

    dict(slug="fig-payments-page-csv-bookkeeping-takeout", screen="tdash", title="Reading your FIG Payments page: takeout, fees and your bookkeeping", date="2026-10-28", publish_at="2026-10-28T12:00:00-04:00", updated="2026-11-05", topic="For restaurants", group="takeout-and-money",
         dek="Every takeout payment, refund and fee is listed on one page and downloads as a CSV file. How to read it, what each line means, a worked month-end example with the sums checked, and how to hand it to your bookkeeper.",
         desc="How to read the FIG Payments page: takeout payments, refunds and fees, the CSV download, and a worked month-end example with the arithmetic.",
         seo="FIG Payments page: reading takeout fees and the CSV",
         keywords="restaurant takeout bookkeeping, restaurant payments CSV, Stripe fees restaurant Canada, reconcile takeout payments, restaurant month end, FIG Payments page, Markham restaurants",
         points=["The Payments page lists every takeout payment, refund and fee, and it downloads as a CSV file you can open in a spreadsheet.",
                 "On each takeout order the diner's card is charged the food plus HST. Stripe's fee of 2.9% + $0.30 for most Canadian cards comes off that payment, and FIG keeps 5% of the food after any deal and before tax.",
                 "The HST on an order is yours to remit. Treat it as a separate line in your books, not as sales you keep.",
                 "Dine-in deals do not appear as takeout payments: the diner pays you directly and FIG takes nothing from that bill.",
                 "Check the page against your own records once a month. A short routine beats a long scramble at tax time."],
         sections=[
             ("The short answer", """<p>The Payments page in FIG lists every takeout payment, every refund and every fee, and you can download it as a CSV file. Use it as the record of your takeout money: one line per event, with the amounts that came in and the fees that came off. Once a month, download it, add up the lines and compare the total with what reached your bank account.</p>
<p>This post is general information about reading your records, not accounting or tax advice. Your bookkeeper or accountant has the final word on how to record any of it.</p>"""),
             ("What the page lists", """<table><thead><tr><th>Line</th><th>What it is</th><th>How to treat it</th></tr></thead><tbody>
<tr><td>Takeout payment</td><td>What the diner paid in the app for a takeout order, food plus HST</td><td>Sales of food, plus HST you collected for the CRA</td></tr>
<tr><td>Stripe fee</td><td>Stripe's card fee, 2.9% + $0.30 for most Canadian cards, taken off the payment</td><td>A card processing cost</td></tr>
<tr><td>FIG fee</td><td>5% of the food after any deal and before tax, on takeout orders only</td><td>A fee for the order. Once FIG is registered for HST, HST is added to this fee</td></tr>
<tr><td>Refund</td><td>Money returned to a diner</td><td>Reduces that order's sales</td></tr>
</tbody></table>
<p>Dine-in is not on this list. When a diner shows a code and pays you at the table or the till, FIG takes no commission on the bill and nothing about that bill is a takeout payment. Your dine-in sales stay in your own till or point-of-sale records. <a href="/blog/how-fig-makes-money">How FIG makes money</a> covers why.</p>"""),
             ("How a payment is charged", """<p>When a diner checks out, the card is held. It is charged when you accept the order, and if you decline, nothing is charged. That matters for your records: an order you declined leaves no payment to match. An order you accepted and the diner collected is one payment line with its fees.</p>
<p>There is no paying at the counter for takeout. The pickup code only confirms that the order was collected, so the app payment is the one place the money for a takeout order appears.</p>"""),
             ("A worked month-end example", """<p>Here are three takeout orders, with the food amount after any deal and before tax. These are round example numbers, and your menu will differ. HST is 13%. Stripe's fee is 2.9% of the whole payment plus $0.30. FIG's is 5% of the food.</p>
<div class="callout math"><b>Three example orders (before any HST on FIG's fee)</b><table><thead><tr><th>Food after deal</th><th>HST at 13%</th><th>Diner paid</th><th>Stripe fee</th><th>FIG 5%</th><th>Left from the food</th></tr></thead><tbody>
<tr><td>$20.00</td><td>$2.60</td><td>$22.60</td><td>$0.96</td><td>$1.00</td><td>$18.04</td></tr>
<tr><td>$30.00</td><td>$3.90</td><td>$33.90</td><td>$1.28</td><td>$1.50</td><td>$27.22</td></tr>
<tr><td>$40.00</td><td>$5.20</td><td>$45.20</td><td>$1.61</td><td>$2.00</td><td>$36.39</td></tr>
<tr><td><b>Total</b></td><td><b>$11.70</b></td><td><b>$101.70</b></td><td><b>$3.85</b></td><td><b>$4.50</b></td><td><b>$81.65</b></td></tr>
</tbody></table><p>Check one row: on the $30 order, Stripe takes 2.9% of $33.90, which is $0.98, plus $0.30, so $1.28. FIG takes 5% of $30, which is $1.50. $30.00 &minus; $1.28 &minus; $1.50 = $27.22. Fees are rounded to the cent.</p></div>
<p>Now the same total two ways. Food of $90.00 plus HST of $11.70 is $101.70 paid by diners. Take off $3.85 and $4.50 in fees and $93.35 is left. Of that, $81.65 is food and $11.70 is HST you will remit. If your CSV for these three orders does not add up to the same figures, look for a refund or a fee line you have not counted.</p>"""),
             ("The monthly routine, in ten minutes", """<ol><li><strong>Download the CSV</strong> from the Payments page for the month.</li><li><strong>Open it in a spreadsheet</strong> and sum three things: payments, fees and refunds.</li><li><strong>Split each payment</strong> into food and HST. Divide the payment by 1.13 to get the food: $22.60 &divide; 1.13 = $20.00.</li><li><strong>Compare the net</strong> with the payouts that reached your bank account for the same period. A small gap can be timing, with an order near the month's end landing in the next one.</li><li><strong>Save the file</strong> with the month in its name, such as the year, the month and the word takeout.</li></ol>
<p>If something does not match after that, write down the order and ask us on the <a href="/contact">contact page</a> rather than guessing.</p>"""),
             ("HST: what is yours to remit", """<p>HST on a takeout order is the restaurant's to remit. The diner pays it with the order, it comes through to you with the rest, and your HST number is what lets takeout work in the first place: a restaurant can turn takeout on only after it has added its HST number and finished Stripe payouts. Keep HST out of your sales figure and in its own line, so the amount you owe is easy to see.</p>
<p>Not registered yet? <a href="/blog/hst-registration-small-restaurants-ontario">HST registration for small restaurants in Ontario</a> goes through the $30,000 rule. It is general information, not tax advice.</p>"""),
             ("Refunds in your records", """<p>A refund shows up as its own line on the page, so you can see which order it belongs to. In your books, a refund reduces the sales for that order. Refunds are a money step, so owners and managers need a stronger sign-in for them: an authenticator app or a code by email. That is also a good control for your own records, because it means refunds are made on purpose by someone you chose. <a href="/blog/fig-staff-roles-sign-in-security-owners-managers">Who should be an owner, manager or staff member</a>.</p>"""),
             ("Handing it to your bookkeeper", """<p>The CSV is the whole point. Send it as it is, one file a month, and say three things in the email: the month it covers, that the HST on each line is the restaurant's to remit, and that dine-in sales are in your own till records. A bookkeeper who gets the same layout every month spots a missing line quickly. Keep the downloaded files in one folder so the year's records are in order when you file.</p>
<div class="callout example"><b>A simple email to send (example)</b><p>"Attached is the takeout payments file for [month]. It lists each payment, refund and fee. HST is included in each payment. Dine-in sales are in our till report."</p></div>"""),
             ("What to look at besides the totals", """<p>Once the sums agree, use the page as a small business tool. Sort by amount to see which sizes of order you get. Count the lines to see how many takeout orders came in during a month. Compare it with your quiet hours: takeout is meant to fill a kitchen that would otherwise be idle. <a href="/blog/takeout-order-math-what-you-keep">Takeout order math</a> shows what a restaurant keeps on a $12, $20, $40 or $60 order, and the <a href="/blog/takeout-rush-pause-prep-time-deals-per-order">rush guide</a> covers pausing takeout and adding prep time when the kitchen is full.</p>
<p>The page fills in as takeout orders come in. If you have not had one yet, set up your menu, hours, payouts and HST number first.</p>"""),
         ],
         faq=[("Where do I see my takeout payments?", "On the Payments page. It lists every takeout payment, refund and fee."),
              ("Can I download my payments?", "Yes. The Payments page downloads as a CSV file, which opens in any spreadsheet."),
              ("What fees come off a takeout payment?", "Stripe's card fee of 2.9% + $0.30 for most Canadian cards comes off the payment, and FIG keeps 5% of the food after any deal and before tax, on takeout orders only."),
              ("Does dine-in show up on the Payments page?", "No. FIG takes no commission on the bill and nothing on dine-in, and the diner pays you directly."),
              ("Who remits the HST on a takeout order?", "The restaurant. This is general information, not tax advice, so ask your accountant how to record it."),
              ("When is the card charged?", "The card is held at checkout and charged when the restaurant accepts the order. If the restaurant declines, nothing is charged."),
              ("Does a refund need a stronger sign-in?", "Yes. Refunds are a money step, so owners and managers need a sign-in step such as an authenticator app or a code by email.")]),

    dict(slug="fig-staff-roles-sign-in-security-owners-managers", screen="tscanner", title="Owner, Manager or Staff: setting up your team and sign-in security on FIG", date="2026-10-29", publish_at="2026-10-29T12:00:00-04:00", updated="2026-11-05", topic="For restaurants", group="fill-quiet-hours",
         dek="Who should hold which role on FIG, how people join by invite, which steps need a stronger sign-in, and how to set it up so a busy shift runs smoothly and the money steps stay with the right people.",
         desc="How to set up your team on FIG: Owner, Manager and Staff roles, invites, and the sign-in security for the money steps.",
         seo="FIG roles and sign-in security for restaurant teams",
         keywords="restaurant staff accounts, restaurant app roles, two-step sign-in restaurant, authenticator app restaurant, add staff FIG, restaurant owner manager access, Markham restaurants",
         points=["FIG has three roles: Owner, Manager and Staff. People join by accepting an invite from the owner.",
                 "Money steps, which are payouts, taking takeout live and refunds, need a stronger sign-in from owners and managers.",
                 "Sign-in security can be an authenticator app or a code by email.",
                 "Give each person their own account. Shared logins make it impossible to tell who did what, and they are hard to take back.",
                 "Review who has access every few months, and take access away from people who have left. A short list is a safe list."],
         sections=[
             ("The short answer", """<p>Invite each person to FIG with the role that matches their job: Owner, Manager or Staff. They join by accepting your invite, so you never share a password. For anything involving money, namely payouts, taking takeout live and refunds, owners and managers confirm with a stronger sign-in step. Pick the authenticator app if you can, and keep a short list of people with access.</p>
<p>You must be 18 or older to hold a restaurant account. Diners must be 14 or older.</p>"""),
             ("The three roles", """<table><thead><tr><th>Role</th><th>Who it suits</th><th>Our suggestion</th></tr></thead><tbody>
<tr><td>Owner</td><td>The person who runs the business and answers for it</td><td>Keep this to one or two people. Owners and managers are the ones asked for the extra sign-in on money steps</td></tr>
<tr><td>Manager</td><td>A shift lead or general manager you trust with the day-to-day</td><td>Choose people you would trust with payouts and refunds, because those steps are theirs to confirm</td></tr>
<tr><td>Staff</td><td>Counter staff, servers and cooks who scan codes on a shift</td><td>Everyone else who needs the app for their job</td></tr>
</tbody></table>
<p>The suggestions are ours, not rules. Check in the app for exactly what each role can do, and start with the smaller role: you can always move someone up later.</p>"""),
             ("How people join", """<p>Nobody signs up themselves and appears on your team. The owner sends an invite, and the person joins by accepting it with their own account. That has two good effects. You decide who is on the team, and each person signs in as themselves, so you can tell who scanned what.</p>
<ol><li>In the app, where you manage your team, send an invite with the role you chose.</li><li>Ask the person to accept it, and to set up their own sign-in security.</li><li>Check the page that they appear with the right role.</li><li>If anyone leaves, take away their access the same day.</li></ol>"""),
             ("Sign-in security: the choices", """<p>For the steps that involve money, an owner or manager confirms with a sign-in step. Two common choices are:</p>
<table><thead><tr><th>Method</th><th>How it works</th><th>Worth knowing</th></tr></thead><tbody>
<tr><td>Authenticator app</td><td>An app on the phone shows a short code that changes</td><td>The code comes from the app on the phone itself. Our first choice</td></tr>
<tr><td>Code by email</td><td>A code arrives in the person's inbox</td><td>Only as safe as that email account, so protect it too</td></tr>
</tbody></table>
<p>Whatever you choose, set it up on each owner's and manager's own phone, not a shared device behind the till. A code on a phone that stays with the person is the point.</p>"""),
             ("Which steps ask for it", """<p>The extra step is for the actions that move money or open it up:</p>
<ul><li><strong>Payouts.</strong> Finishing Stripe payouts, which a restaurant needs before it can take takeout.</li><li><strong>Taking takeout live.</strong> A restaurant can turn takeout on only after it has added its HST number and finished Stripe payouts.</li><li><strong>Refunds.</strong> Returning money to a diner.</li></ul>
<p>Keep the list of people who can do these things short. The fewer the phones that hold a code, the easier it is to know who made a change, and the easier it is to ask questions when the numbers on the Payments page look different from what you expected.</p>"""),
             ("A worked example: a small restaurant", """<p>Here is how a small restaurant might set this up. The people and numbers are an example, not a real restaurant.</p>
<div class="callout example"><b>Example: a restaurant with eight people</b><ul><li>1 owner who holds the business and the bank details.</li><li>1 manager who runs the evening shift and can handle a refund.</li><li>6 people on staff who scan codes at the till.</li><li>Money steps involve 2 people, the owner and the manager, both with an authenticator app.</li></ul><p>Of the 8 people, 2 (25%) can confirm the money steps and 6 (75%) cannot. If one of the 6 leaves, you take away one account and nothing else changes. With a single shared login for all 8 people, you would have to change it for everyone, and you could not say who did what.</p></div>"""),
             ("What to do when someone leaves", """<p>The day someone leaves, take away their access. Do not wait for the end of the month. It closes the question of who can still act on your restaurant's page. If you cannot find how to do it, use the <a href="/contact">contact page</a> and say so. If that person was a manager, also think about what they could do with a code on their own phone, and ask for your own sign-in method to be set up again if you are unsure.</p>
<p>It also helps to have a second owner or manager who can step in. If the only person with a code is away or has lost a phone, payouts and refunds wait, and a restaurant should not find that out on a busy Saturday.</p>
<p>A habit that helps: put "take away their FIG access" on the same checklist you use to collect keys and uniforms. <a href="/blog/train-staff-honour-fig-deal">Train your staff to honour a deal</a> covers the day-to-day side.</p>"""),
             ("Two locations", """<p>FIG supports up to 2 locations for now. If you run two, decide who is responsible at each: a manager per location is a reasonable starting point. The owner keeps the view of both. Everyone still gets their own account, and the roles are the same.</p>"""),
             ("A security checklist for the owner", """<ol><li>Is everyone using their own account?</li><li>Do the owner and managers have an authenticator app, or a code by email, set up on their own phones?</li><li>Is the list of people short, and does it match who works for you today?</li><li>Do we know who to call if an owner loses a phone? Write that down now, and use the <a href="/contact">contact page</a> if you get stuck.</li><li>Do staff know which steps are theirs and which belong to owners and managers?</li></ol>
<p>A last habit worth having: once a quarter, open the list, read each name aloud, and ask whether that person still works for you and still needs that role. If a part-time cook has never opened the app, they probably do not need to be on it. A list that matches your payroll is easy to defend, and easy to show an accountant or a new partner.</p>
<p>Setting this up takes about ten minutes, and it is worth doing before the first busy night, not after. The <a href="/blog/set-up-fig-menu-takeout">menu and takeout setup guide</a> is the next step.</p>"""),
         ],
         faq=[("What roles are there on FIG?", "Owner, Manager and Staff."),
              ("How do my staff get an account?", "They join by accepting an invite from the owner. Nobody can add themselves to your team."),
              ("Which steps need a stronger sign-in?", "The money steps: payouts, taking takeout live and refunds. Owners and managers need it for those."),
              ("What sign-in security can I use?", "An authenticator app or a code by email."),
              ("Can I run two restaurants from one account?", "FIG supports up to 2 locations for now."),
              ("How old do I have to be?", "Restaurant accounts are for people 18 or older. Diners must be 14 or older."),
              ("Should my staff share one login?", "No. Give each person their own account, so you can tell who did what and take one person off without affecting the rest.")]),

    dict(slug="deals-used-more-than-once-uses-per-diner-wait-between-uses", screen="qr", title="Deals diners can use more than once: uses per diner and the wait between uses", date="2026-10-30", publish_at="2026-10-30T12:00:00-04:00", updated="2026-11-05", topic="For restaurants", group="fill-quiet-hours",
         dek="A deal does not have to be a one-time offer. How uses per diner and the wait between uses work on FIG, how the code changes after every scan, and the arithmetic of a repeat deal for a quiet weekday.",
         desc="How repeat deals work on FIG: up to 20 uses per diner, an optional wait between uses, a new code after each scan, and the math of a repeat deal.",
         seo="Repeat restaurant deals: uses per diner and the wait between uses",
         keywords="restaurant repeat customers, restaurant deal limits, how many times can a diner use a deal, uses per diner, restaurant weekday lunch deal, bring customers back, Markham restaurants",
         points=["You set how many times one diner can use a deal, up to 20, and an optional wait between uses.",
                 "A deal code works once. If the deal can be used more than once, the diner's screen shows a new code after each scan.",
                 "A diner can claim a deal once a day, so a repeat deal naturally spreads visits over many days.",
                 "Each use needs a fresh scan of the new code, so a repeat deal is a deal you let the same diner come back to.",
                 "Work out the cost per use first. A repeat deal is good when it brings visits you would not have had."],
         sections=[
             ("The short answer", """<p>When you post a deal on FIG you choose how many times one diner can use it, from 1 up to 20, and you can add a wait between uses. After each scan the diner's screen shows a new code, because a code works once. Use one use for a trial offer, a few uses for a weekday habit, and a wait between uses so the same diner does not use it three times in an afternoon.</p>"""),
             ("What you can set", """<table><thead><tr><th>Setting</th><th>What it does</th><th>Good to know</th></tr></thead><tbody>
<tr><td>Uses per diner</td><td>How many times one diner can use the deal, up to 20</td><td>Start at 1 for something new</td></tr>
<tr><td>Wait between uses</td><td>An optional pause before the same diner can use it again</td><td>Stops several uses in one visit or one afternoon</td></tr>
<tr><td>Live now or scheduled</td><td>Starts the deal when you post it, or at a time you choose</td><td>Set a lunch deal ahead the evening before</td></tr>
<tr><td>Deal type</td><td>2 for 1, percent off, dollar off, or free with a dish</td><td>Pick the type that suits your food cost. <a href="/blog/deal-types-percent-dollar-2-for-1">See the comparison</a></td></tr>
</tbody></table>"""),
             ("How the code behaves", """<p>A deal code works once. The diner shows the QR code on their phone, your staff scan it, and that code is spent. If the deal allows more than one use, the diner's screen then shows a new code for the next time. That is why a screenshot is no use: the old code has already worked.</p>
<p>One more rule shapes how often the deal is used: a diner can claim a deal once a day. So even with 20 uses, one diner cannot burn through them in a single day. Your staff still do the same thing every time, which is scan whatever code is on the screen. <a href="/blog/train-staff-honour-fig-deal">A ten-minute staff guide</a> shows how.</p>"""),
             ("When a single use is right", """<ul><li><strong>A new dish you want people to try.</strong> One use gets the first order. A second visit is up to the dish.</li><li><strong>A big discount.</strong> The deeper the cut, the fewer uses you want to give.</li><li><strong>A busy time.</strong> A deal that fills a weekday lunch is not a deal you want repeated on a Saturday night.</li></ul>"""),
             ("When more uses make sense", """<ul><li><strong>A small, steady offer.</strong> A dollar off a lunch special for the week brings a regular a few times.</li><li><strong>A quiet weekday window.</strong> Repeat visits between 2 and 4 pm cost you the least, because the table and the cook were idle.</li><li><strong>A drink or a side.</strong> A small offer on an add-on can bring a full order with it.</li></ul>
<p>Pair uses with a wait. A deal that allows 5 uses with a wait between them gives a diner a reason to come back across the week instead of five times on the same day. <a href="/blog/slow-hour-deal-math">The slow-hour math</a> goes through how to judge a deal by new and returning diners.</p>"""),
             ("The arithmetic of a repeat deal", """<p>Here is an example with round numbers, not a real restaurant. A weekday lunch bowl sells for $14.00, the ingredients cost about 30% of that, and the deal takes $2.00 off. This is a dine-in deal, so FIG takes nothing from the bill.</p>
<div class="callout math"><b>One lunch bowl with $2 off (example)</b><table><thead><tr><th>Item</th><th>Amount</th></tr></thead><tbody>
<tr><td>Menu price</td><td>$14.00</td></tr>
<tr><td>Deal</td><td>&minus; $2.00</td></tr>
<tr><td>Diner pays (before HST)</td><td>$12.00</td></tr>
<tr><td>Food cost, 30% of $14.00</td><td>&minus; $4.20</td></tr>
<tr><td>Left toward wages, rent and profit</td><td>$7.80</td></tr>
</tbody></table><p>A diner who uses the deal 5 times leaves you 5 &times; $7.80 = $39.00. Without the deal, if they would have come twice at full price, you would have had 2 &times; ($14.00 &minus; $4.20) = $19.60. So the deal is better when it brings at least 2 extra visits. If they would have come all 5 times anyway, the deal cost you 5 &times; $2.00 = $10.00.</p></div>
<p>That last line is the risk to keep in mind. A repeat deal gives the discount to regulars as well as to newcomers. It pays off when the quiet window is truly quiet, and your results will tell you whether the same faces keep coming back or new ones do.</p>"""),
             ("Choosing the wait between uses", """<p>The wait is optional, and it is the setting that shapes how the deal feels. With no wait, a diner can come back as soon as they have claimed the deal again, which is once a day at most. With a wait, you decide the rhythm: a lunch deal that makes sense once a week behaves differently from a coffee deal that suits most weekdays.</p>
<table><thead><tr><th>If your goal is</th><th>Try</th></tr></thead><tbody>
<tr><td>Bring newcomers in once</td><td>1 use per diner</td></tr>
<tr><td>Make a weekday lunch a habit</td><td>A few uses, with a wait between them</td></tr>
<tr><td>Fill a quiet window, nothing more</td><td>Several uses, a short wait and tight hours</td></tr>
</tbody></table>
<p>These are starting points, not rules. The setting is yours, and the right answer depends on how much the discount costs you per use.</p>"""),
             ("Add-ons carry the margin", """<p>Most diners add a drink or a side. Keep the deal on the main dish and sell the add-ons at full price. If the same diner adds a $4.00 drink that costs you $1.00, that is another $3.00 per visit. Over 5 visits, $15.00 more, on top of the $39.00 above.</p>"""),
             ("Reading the results", """<p>Your dashboard shows results deal by deal. After two weeks, compare the deal's scans with your quiet hours: did that window fill up, or did the same few diners use up their visits? Your own till tells you the rest. If tables in that window were busier than the week before, keep the deal and consider more uses. If your regulars used it and nobody new did, lower the uses or narrow the hours.</p>
<p>Change one thing at a time, so you know which change made the difference. Write the setting down with the date, so that in a month you remember what you tried.</p>"""),
             ("Getting started", """<p>Diners are on FIG now, so a repeat deal starts working the day you publish it. You can post it live now or schedule it for the days and hours you choose. Pick the quietest weekday window you have and start with a small offer. Our <a href="/blog/fill-slow-hours-restaurant">seven ways to fill slow hours</a> has more ideas.</p>"""),
         ],
         faq=[("How many times can a diner use one deal?", "You choose, from 1 up to 20 uses per diner, with an optional wait between uses."),
              ("Does the QR code change?", "A deal code works once. If the deal can be used more than once, the diner's screen shows a new code after each scan."),
              ("Can a diner use a deal several times in a day?", "No. A diner can claim a deal once a day."),
              ("Can I schedule a repeat deal?", "Yes. A deal can be live now or scheduled, with uses per diner and a wait between uses."),
              ("Do restaurants see a diner's phone number?", "No. Restaurants never see diners' phone numbers."),
              ("Do I need a different code for each use?", "No. Your staff just scan whatever code the diner shows. The diner's screen creates the new code."),
              ("Does a dine-in repeat deal cost anything to FIG?", "No. FIG takes no commission on the bill and nothing on dine-in.")]),

    dict(slug="restaurant-checklist-before-fig-opens-january-2027", screen="map", title="Restaurant checklist: get your FIG page ready before you go live", date="2026-10-31", updated="2026-11-05", publish_at="2026-10-31T12:00:00-04:00", topic="For restaurants", group="fill-quiet-hours",
         dek="Diners are on FIG now, so your page counts from the day you publish it. A step-by-step checklist: your page, menu, hours, team, first deals and takeout.",
         desc="A step-by-step checklist for Markham restaurants to get their FIG page, menu and first deals ready before they go live.",
         seo="Restaurant checklist before you go live on FIG",
         keywords="restaurant app setup checklist, new restaurant app launch Markham, get ready restaurant deals app, restaurant menu photos, set up restaurant deals, Markham restaurants, go live on FIG",
         points=["FIG is open to diners in Markham now, so diners see your page as soon as you publish it.",
                 "Signing up, setting up your page, going live, posting deals, scanning and the dashboard cost nothing.",
                 "Do the base first: page, hours, menu with photos and sections. Then the team, then the first deals.",
                 "Takeout is optional. You can turn it on only after you add your HST number and finish Stripe payouts.",
                 "Two hours a week for five weeks is enough to do all of this without rushing, and most small restaurants need less."],
         sections=[
             ("The short answer", """<p>Before you go live, build your page, your menu and your first deals, so that the first diners who find you see a complete restaurant. Signing up, setting up your page, going live, posting deals, scanning and the dashboard cost nothing. The order that works best is the page and hours, then the menu, then your team, then the first deals, and takeout last, if you want it at all.</p>"""),
             ("Who does what", """<table><thead><tr><th>Who</th><th>What they do on FIG today</th></tr></thead><tbody>
<tr><td>Restaurants</td><td>Set up your page, menu, hours and deals, then publish them</td></tr>
<tr><td>Diners</td><td>Browse places, menus, reviews and live deals at www.figpromo.ca/app, and claim a deal in one tap</td></tr>
</tbody></table>
<p>FIG starts in Markham, then expands to Richmond Hill and Vaughan Mills. You need to be 18 or older to hold a restaurant account.</p>"""),
             ("How much time it takes", """<div class="callout math"><b>Counting the hours</b><ul><li>Five steps below: the base, the menu, your team, your first deals and takeout.</li><li>One step a week at two hours a week is 5 &times; 2 = 10 hours in all.</li></ul><p>Most small restaurants need less, and you can skip takeout altogether.</p></div>"""),
             ("Step 1: the base", """<ol><li><strong>Create your account.</strong> It costs nothing.</li><li><strong>Fill in your page.</strong> Name, cuisine, address, a short description and a few good photos.</li><li><strong>Set your opening hours.</strong> Include holidays and any day you are closed, because diners decide where to go around them.</li><li><strong>Check your details twice.</strong> A wrong phone number or hour costs you more than a missing photo.</li></ol>
<p>Photos matter more than most owners expect. Use daylight, shoot the dish from slightly above, and avoid stock images: diners can tell.</p>"""),
             ("Step 2: the menu", """<p>A menu with photos and sections is the part diners read first. Group dishes the way you would on a printed menu, and add a photo for your most popular dishes before the rest. Write names the way a diner would say them, and put anything dietary in the description. <a href="/blog/set-up-fig-menu-takeout">Set up your FIG menu and takeout in 15 minutes</a> takes you through the screens.</p>
<p>Prices should match your dining room. A price that is wrong on your page costs you either a sale or an argument at the till, so check each one once.</p>"""),
             ("Step 3: your team", """<p>Invite the people who will work with FIG every day. They join by accepting an invite from the owner, as Owner, Manager or Staff. Give owners and managers a sign-in step for money, such as an authenticator app or a code by email. <a href="/blog/fig-staff-roles-sign-in-security-owners-managers">The roles guide</a> has a checklist, and <a href="/blog/train-staff-honour-fig-deal">the ten-minute staff session</a> gets everyone ready for the till.</p>"""),
             ("Step 4: your first deals", """<p>Pick one or two quiet windows. Look at your week and find the hours where tables sit empty, usually weekday afternoons or early evenings. Then write a deal for each.</p>
<ul><li>Choose a type: 2 for 1, percent off, dollar off, or free with a dish. <a href="/blog/deal-types-percent-dollar-2-for-1">Which one fits</a>.</li><li>Choose live now or scheduled for the hours you want to fill.</li><li>Set uses per diner and, if you like, a wait between uses.</li><li>Do the sum on the price before you post. <a href="/blog/slow-hour-deal-math">The slow-hour math</a> shows how.</li></ul>
<div class="callout math"><b>A 60-second check (example)</b><p>A $15.00 dish, with a 30% food cost of $4.50, and a $3.00-off deal: the diner pays $12.00 and you keep $12.00 &minus; $4.50 = $7.50. That is $7.50 toward wages, rent and profit from a table that was empty. These are round example numbers.</p></div>"""),
             ("Step 5: takeout, if you want it", """<p>Takeout is optional. Diners pay online in the app at checkout, and the kitchen starts when you accept. A restaurant can turn it on only after it has added its HST number and finished Stripe payouts, and those money steps ask owners and managers for a stronger sign-in. FIG keeps 5% of the food after any deal and before tax on takeout orders, plus Stripe's card fee of 2.9% + $0.30 for most Canadian cards, which comes off the payment. Dine-in has no such fee. Read <a href="/blog/takeout-order-math-what-you-keep">the order math</a> before you decide, and <a href="/blog/hst-registration-small-restaurants-ontario">the HST guide</a> if you are not registered. That guide is general information, not tax advice.</p>
<p>If you do turn takeout on, learn the pause button and prep time first. <a href="/blog/takeout-rush-pause-prep-time-deals-per-order">The rush guide</a> covers both.</p>"""),
             ("Writing your page so diners understand it", """<p>Diners will see your page on a map next to other restaurants, so the first lines matter. Say what you serve and what the place is like in plain words, such as "a small Hakka kitchen, open late" or "a family bakery with a few tables". Name your best dish. If you serve halal, vegetarian, vegan or gluten-free food, say so clearly, because many diners filter for it and a vague description can lose them.</p>
<p>Keep it honest. If your kitchen cannot guarantee an allergen-free dish, say that, and invite people to call. <a href="/blog/eating-out-dietary-needs-allergies-markham">What diners with dietary needs ask restaurants</a> shows the questions you will hear.</p>
<ul><li>Use the same name that is on your sign.</li><li>Put your phone number where it can be found.</li><li>Choose the photo diners see first with care: a dish, not a storefront in the dark.</li></ul>"""),
             ("The day before you go live", """<ol><li>Open your page as a diner would and read it line by line.</li><li>Check that your hours, menu and photos are right.</li><li>Check that the scheduled deals start when you intend.</li><li>Run one test scan with your team so everyone has seen the screen.</li><li>Tell your regulars. A sign at the till and a word at the door cost nothing.</li></ol>"""),
             ("Two things not to do", """<ul><li><strong>Do not post a deal you have not priced.</strong> Do the sum first, because a deal that loses money on every table is hard to take back.</li><li><strong>Do not wait for a perfect page.</strong> Go live with a clear page and a good first deal, then improve it using your results, which show how each deal does.</li></ul>
<p>Questions? The <a href="/contact">contact page</a> reaches us. FIG is run by Brendan Lau in Markham, Ontario.</p>"""),
         ],
         faq=[("Is FIG open to diners?", "Yes. FIG opened to diners on November 4, 2026, in Markham first, expanding to Richmond Hill and Vaughan Mills. Diners see your page as soon as you publish it."),
              ("What does it cost to set up my restaurant?", "Signing up, setting up the page, going live, posting deals, scanning and the dashboard cost nothing. FIG earns only on takeout orders paid in the app."),
              ("Do I have to offer takeout?", "No. You can turn it on only after you add your HST number and finish Stripe payouts, and you can leave it off."),
              ("How many locations can I add?", "Up to 2 for now."),
              ("Where does FIG start?", "In Markham, then Richmond Hill and Vaughan Mills."),
              ("How old do I have to be?", "Restaurant accounts are for people 18 or older."),
              ("Can I schedule a deal?", "Yes. Deals can be live now or scheduled for the days and hours you choose.")]),

    # ---------------------------------------------------------------- batch of 4 queued posts (publish_at: hidden until then)

    dict(slug="menu-photos-restaurant-phone-photography-fig", screen="map", title="Menu photos with a phone: how to photograph your dishes for your FIG menu", date="2026-11-01", publish_at="2026-11-01T12:00:00-05:00", updated="2026-11-05", topic="For restaurants", group="fill-quiet-hours",
         dek="Your FIG menu has photos and sections, and photos are what diners look at first. How to shoot your dishes with the phone you already own: light, angle, plating, which dishes to do first and how long it takes.",
         desc="A practical guide for restaurant owners to photograph dishes with a phone for a FIG menu: light, angle, plating, order of work and a time budget.",
         seo="How to photograph restaurant dishes with a phone for your menu",
         keywords="restaurant menu photos, food photography phone, photograph restaurant dishes, online menu photos, restaurant menu setup, Markham restaurants, FIG menu",
         points=["A FIG menu has photos and sections, and you add both yourself. You do not need a studio or a hired photographer.",
                 "Daylight from a window, a clean plate and a slightly raised angle do most of the work.",
                 "Photograph your best sellers first. A menu with eight good photos beats one with thirty rushed ones.",
                 "Shoot the dish you really serve, at the size you really serve it, so the plate that arrives matches the picture.",
                 "Budget about four minutes a dish. Twenty dishes is a little over an hour, which fits into one quiet afternoon."],
         sections=[
             ("The short answer", """<p>You can take good menu photos with the phone in your pocket. Put the plate by a window in daylight, wipe the rim, hold the phone a little above the dish and take three or four shots, then keep the best one. Start with your best sellers, because those are the dishes diners will look for first on your FIG menu.</p>"""),
             ("Why photos matter on a menu page", """<p>On FIG, diners will browse places, menus, reviews and live deals on a map. A menu with photos and sections is easier to read at a glance than a long list of names, and a photo answers the questions a diner would otherwise have to ask: how big is it, what is on it, does it look like what I want tonight?</p>
<p>A photo is also a promise. If the picture shows a full bowl and the bowl that arrives is half that, the diner remembers the gap, and so does the review. The best menu photo is an honest one.</p>"""),
             ("What you need", """<table><thead><tr><th>Item</th><th>Why</th><th>Cost</th></tr></thead><tbody>
<tr><td>Your phone</td><td>Current phones take a sharp photo in daylight</td><td>Nothing</td></tr>
<tr><td>A window with daylight</td><td>Soft light from the side makes food look like itself</td><td>Nothing</td></tr>
<tr><td>A plain table or board</td><td>Keeps attention on the dish</td><td>Whatever you already have</td></tr>
<tr><td>A clean cloth</td><td>For fingerprints on the lens and drips on the rim</td><td>Nothing</td></tr>
<tr><td>A second pair of hands</td><td>One person plates, one person shoots</td><td>A few minutes of a colleague's time</td></tr>
</tbody></table>
<p>That is all. Do not buy lights or props before you have tried a window.</p>"""),
             ("Light: the one thing worth getting right", """<p>Most bad food photos are bad because of light, not the phone. A few rules:</p>
<ul><li><strong>Use daylight.</strong> Stand the dish near a window, with the light coming from the side or slightly behind the plate.</li><li><strong>Turn off the overhead lights</strong> in that corner. Mixed light makes food look yellow or grey.</li><li><strong>Skip the flash.</strong> It flattens the dish and makes sauce look oily.</li><li><strong>Shoot at the right time of day.</strong> If your kitchen is busy at noon, shoot at mid-afternoon when the room is quiet and the light is still good.</li></ul>
<p>If your restaurant has no good window, a spot just inside the front door often works, before opening.</p>"""),
             ("Angle and framing", """<p>Different dishes want different angles:</p>
<table><thead><tr><th>Kind of dish</th><th>Try this angle</th></tr></thead><tbody>
<tr><td>Flat dishes: pizza, a platter, a bowl seen from the top</td><td>Straight down</td></tr>
<tr><td>Tall dishes: burgers, stacked sandwiches, layered desserts</td><td>From the side, at the height of the dish</td></tr>
<tr><td>Most plates and bowls</td><td>A slightly raised angle, about halfway between the two</td></tr>
<tr><td>Drinks</td><td>From the side, so the colour and the glass show</td></tr>
</tbody></table>
<p>Keep the dish in the middle with a little empty space around it, and use the same angle for dishes of the same kind. A menu where the burgers all share one angle looks tidy, and diners compare them more easily.</p>"""),
             ("Plating for the camera, without cheating", """<ul><li><strong>Wipe the rim</strong> of the plate or bowl. Sauce drips are the most common flaw.</li><li><strong>Use the real portion.</strong> Do not pile it higher than a customer would receive.</li><li><strong>Add fresh colour</strong> that you would really serve, such as a few chopped green onions or a lemon wedge.</li><li><strong>Shoot it fast.</strong> Fries wilt and sauces skin over, so have the camera ready before the plate comes out.</li><li><strong>Keep plates and bowls consistent</strong> across the menu if you can.</li></ul>"""),
             ("What to photograph first", """<p>Do not try to shoot the whole menu on day one. Work in this order:</p>
<ol><li>Your best sellers. If you know what moves most, start there.</li><li>The dishes you want to sell more of, especially any you will use in a deal.</li><li>One dish per section, so every part of the menu has at least one picture.</li><li>The rest, whenever you have time.</li></ol>
<p>If you are about to post a deal, photograph the dish it applies to first. A deal on a dish with a good photo is easier for a diner to say yes to.</p>"""),
             ("A time budget, with the sum", """<div class="callout math"><b>How long it takes (example)</b><ul><li>Four minutes a dish: a minute to plate, two to shoot three or four angles, a minute to pick the best.</li><li>Eight best sellers: 8 &times; 4 = 32 minutes.</li><li>Twenty dishes: 20 &times; 4 = 80 minutes, which is one hour and twenty minutes.</li></ul><p>These are example numbers. Your own pace may be faster, because the second and third dish go quicker than the first.</p></div>
<p>If you have a staff member who is good with a phone, ask them to run the session. People who photograph their own friends' dinners often take the best menu photos.</p>"""),
             ("Choosing the best shot", """<p>Take three or four photos of each dish and then compare them side by side. Choose the one where the food is sharp and the plate is clean. Delete the rest, so the wrong one never ends up on your menu by mistake. Crop if you need to, but leave the edit there: heavy filters change the colour of the food, and then the dish on the table does not match.</p>
<p>When a dish changes, whether the recipe, the garnish or the plate, take a new photo. A photo that is a year old and no longer true is worse than no photo at all.</p>"""),
             ("Putting the photos on your FIG menu", """<p>In your restaurant account, your menu is built from sections with dishes in them, and each dish can have a photo. Group dishes the way your printed menu does, add the photo to each dish and check that every price is right. Our guide to <a href="/blog/set-up-fig-menu-takeout">setting up your FIG menu and takeout in 15 minutes</a> goes through the screens. If you want the full list of what to do before you go live, see the <a href="/blog/restaurant-checklist-before-fig-opens-january-2027">restaurant checklist</a>.</p>
<p>Diners are on FIG now, so a photo starts working as soon as your menu is published. Do your most popular dishes first and the rest at a calm pace.</p>"""),
             ("Mistakes to avoid", """<ul><li><strong>Stock photos.</strong> They never match what you serve.</li><li><strong>Dark photos.</strong> If you cannot see the food on a phone screen in the sun, it is too dark.</li><li><strong>Hands and thumbs</strong> at the edge of the frame.</li><li><strong>A different look on every dish.</strong> Consistency reads as care.</li><li><strong>Leaving a dish without a photo</strong> because it is hard to shoot. Show the plate as it is, steam and all.</li></ul>"""),
         ],
         faq=[("Do I need a professional photographer for my FIG menu?", "No. A phone, a window with daylight and a clean plate are enough. Start with your best sellers."),
              ("Does my FIG menu need photos?", "A FIG menu has photos and sections. You add them yourself, and you can start with your best sellers and add the rest later."),
              ("What is the best light for food photos?", "Daylight from a window, coming from the side or slightly behind the plate. Turn off overhead lights and skip the flash."),
              ("How many photos should I take of each dish?", "Three or four from slightly different angles, then keep the best one and delete the rest."),
              ("Should the photo show the real portion?", "Yes. Show the dish as you serve it, so that the plate that reaches the table matches the picture."),
              ("How long does it take to photograph a menu?", "About four minutes a dish as an example, so twenty dishes take a little over an hour. Do the best sellers first."),
              ("Can diners see my menu now?", "Yes. FIG is open to diners in Markham, and they see your menu and photos as soon as they are published.")]),

    dict(slug="takeout-order-declined-or-refunded-what-happens-to-the-money", screen="tdash", title="Takeout order declined or refunded: what happens to the money on FIG", date="2026-11-02", publish_at="2026-11-02T12:00:00-05:00", updated="2026-11-05", topic="For restaurants", group="takeout-and-money",
         dek="A takeout order is held on the diner's card and charged when you accept. What that means if you decline, if you need to refund, who can do it, and where to see every refund and fee afterwards.",
         desc="What happens to the money when a restaurant declines or refunds a FIG takeout order: when the card is charged, who can refund, and the Payments page.",
         seo="Takeout order declined or refunded: what happens to the money",
         keywords="restaurant takeout refund, declined takeout order, takeout payment hold, restaurant refund Stripe, takeout order accept decline, Markham restaurants, FIG takeout",
         points=["On a takeout order the diner pays online at checkout. The card is held, and charged when the restaurant accepts.",
                 "If the restaurant declines, nothing is charged. The kitchen starts only when you accept.",
                 "Refunds are a money step, so owners and managers need their stronger sign-in to make one.",
                 "The Payments page lists every takeout payment, refund and fee, and downloads as a CSV file.",
                 "FIG keeps 5% of the food after any deal and before tax, on takeout orders only. Use your Payments page, not memory, to see what a refunded order did to your month."],
         sections=[
             ("The short answer", """<p>When a diner pays for takeout in the FIG app, the card is held and is charged when the restaurant accepts the order. If you decline, nothing is charged. If you need to give money back after accepting, that is a refund, and owners and managers need their stronger sign-in to do it. Every payment, refund and fee then shows on your Payments page.</p>"""),
             ("The life of a takeout order", """<table><thead><tr><th>Step</th><th>What happens</th><th>Money</th></tr></thead><tbody>
<tr><td>1. The diner checks out</td><td>They pay online in the app. There is no paying at the counter</td><td>The card is held</td></tr>
<tr><td>2a. You accept</td><td>The kitchen starts</td><td>The card is charged</td></tr>
<tr><td>2b. You decline</td><td>The order does not go ahead</td><td>Nothing is charged</td></tr>
<tr><td>3. The diner collects</td><td>Staff use the pickup code to confirm collection</td><td>No new money moves. The code only confirms collection</td></tr>
<tr><td>4. Something goes wrong later</td><td>You refund the order</td><td>Listed on your Payments page</td></tr>
</tbody></table>
<p>Two things in this table are worth remembering. The kitchen starts when you accept, so accept only when you can make the order. And the pickup code is not a payment step. By the time the diner arrives, the payment has already happened.</p>"""),
             ("Declining an order", """<p>You can decline an order that you cannot make: the kitchen is out of the main ingredient, the dish is sold out, or it is simply too busy. Because the card is only held until you accept, a declined order costs the diner nothing, and you have lost no fee.</p>
<p>It is far better to decline quickly than to accept and then fail to deliver. A diner who is told no can eat somewhere else. A diner whose order is accepted and then late or wrong is the one who leaves a poor review. If you decline often at the same hour, that is the sign to use pause or prep time. <a href="/blog/takeout-rush-pause-prep-time-deals-per-order">The rush guide</a> covers both.</p>"""),
             ("Refunding an order", """<p>Once you have accepted and the card has been charged, a refund is how money goes back. Reasons you might refund include a dish that could not be made after you accepted, a mistake in the kitchen, or a problem the diner raised at pickup.</p>
<p>Refunds are one of the money steps. Owners and managers need their stronger sign-in for them, which is an authenticator app or a code by email. Money steps stay with the people who answer for them. <a href="/blog/fig-staff-roles-sign-in-security-owners-managers">The roles and sign-in guide</a> shows how to choose who has which role.</p>"""),
             ("Where you see it afterwards", """<p>Your Payments page lists every takeout payment, refund and fee, and it downloads as a CSV file. When an order is refunded, it shows there as its own line. Use it to answer three questions at month end:</p>
<ol><li>How much did I take in takeout payments?</li><li>How much did I refund?</li><li>What did the fees come to?</li></ol>
<p>Our guide to <a href="/blog/fig-payments-page-csv-bookkeeping-takeout">reading the Payments page</a> goes through the lines in detail and shows how to hand the file to a bookkeeper.</p>"""),
             ("Keeping the refund count low", """<p>A refund is a symptom. These steps stop most of them before they start:</p>
<ul><li><strong>Keep your menu current.</strong> A dish that is not available should not be on the menu. Check photos and prices at the start of each week.</li><li><strong>Add prep time</strong> when the kitchen is slow, so pickup times are honest.</li><li><strong>Pause takeout</strong> when you cannot keep up.</li><li><strong>Set deals per order</strong> so one order cannot stack more discounts than you meant.</li><li><strong>Check each bag against the order</strong> before it leaves the counter.</li></ul>"""),
             ("What a refund can cost you: a worked example", """<p>This example uses round numbers, not a real restaurant. Suppose one month holds 40 takeout orders of $30 of food each, and 2 of them are refunded in full.</p>
<div class="callout math"><b>Two refunds in forty orders (example)</b><ul><li>Takeout food sold: 40 &times; $30 = $1,200.</li><li>Refunded: 2 &times; $30 = $60, which is 5% of the month's takeout food.</li><li>Food still sold: $1,200 &minus; $60 = $1,140.</li></ul><p>The Payments page shows what happened to the fees on each refunded order. Look there rather than guessing.</p></div>
<p>The point of the example is the rate. Two refunds in forty orders is one in twenty. If you see one in five, the problem is upstream, in the menu, the prep time or the staffing, and the fix is cheaper than the refunds.</p>"""),
             ("A busy-night routine that prevents most problems", """<p>Most declined and refunded orders come from the same few causes, and they are cheap to prevent. Before a busy service, run through this short list with whoever is on the pass:</p>
<ol><li><strong>Check what is sold out.</strong> Take it off the menu before the first order arrives, not after.</li><li><strong>Set the prep time.</strong> If the kitchen is running 25 minutes behind, say so in the prep time rather than promising a quick pickup.</li><li><strong>Decide who watches new orders.</strong> One person should own the accept and decline buttons, so an order never sits unseen.</li><li><strong>Know when you will pause.</strong> Agree a point, such as more tickets on the line than you can fire at once, at which takeout is paused until the line clears.</li></ol>
<p>None of this costs anything, and each step protects the one thing a refund cannot repair, which is the diner's trust.</p>"""),
             ("What the diner sees", """<p>From the diner's side, the order is simple. They pay online at checkout, they wait to hear whether the restaurant accepts, and they collect with a pickup code that confirms the handover. They are never asked to pay at the counter. That is why a decline is painless for them: nothing was taken. It is also why you should decline fast. The sooner the answer comes, the sooner they can order somewhere else.</p>"""),
             ("Talking to the diner", """<p>A refund goes better with a short, plain note. Say what went wrong, say what you did and say you are sorry. Do not argue about it. A diner who gets a quick refund and an apology will often order again. A diner who is made to prove a point rarely does.</p>
<p>If the problem was in the review, answer it. <a href="/blog/reply-to-reviews-restaurants">Replying to reviews</a> has templates that are easy to adapt.</p>"""),
             ("What to do before takeout is on", """<p>A restaurant can turn takeout on only after it has added its HST number and finished Stripe payouts, and those steps ask owners and managers for the stronger sign-in. Do them early, so that a refund on your first busy day is not the first time you meet the sign-in. Takeout is optional, and FIG earns only on takeout orders paid in the app. Dine-in has no such fee.</p>"""),
         ],
         faq=[("When is the diner's card charged for takeout?", "The card is held at checkout and charged when the restaurant accepts the order."),
              ("What if I decline a takeout order?", "Nothing is charged. The kitchen starts when the restaurant accepts."),
              ("Who can refund a takeout order?", "Refunds are a money step, so owners and managers need their stronger sign-in to make one."),
              ("Where do I see my refunds and fees?", "On the Payments page, which lists every takeout payment, refund and fee and downloads as a CSV file."),
              ("Can a diner pay at the counter for takeout?", "No. Diners pay online in the app at checkout. The pickup code only confirms collection."),
              ("What does FIG keep on a takeout order?", "5% of the food after any deal and before tax, plus HST on that fee once FIG is registered for HST. Stripe's card fee of 2.9% + $0.30 for most Canadian cards comes off the payment."),
              ("Do I pay anything on dine-in orders?", "No. There is no commission on the bill and nothing on dine-in.")]),

    dict(slug="monthly-eating-out-budget-markham-diners", screen="claim", title="A monthly eating-out budget that works: where FIG deals fit in Markham", date="2026-11-03", updated="2026-11-05", publish_at="2026-11-03T12:00:00-05:00", topic="For diners", group="eat-out-for-less",
         dek="Set one number for eating out, split it into a few kinds of meals, add HST and tip, and see where a deal fits. A worked example with round numbers, and what to expect from FIG in Markham.",
         desc="How to set a monthly eating-out budget with HST and tip counted in, plus where restaurant deals on FIG fit in Markham.",
         seo="Monthly eating-out budget: a worked example with HST and tip",
         keywords="eating out budget, monthly restaurant budget, restaurant bill with tax and tip Ontario, how much to spend eating out, restaurant deals Markham, FIG deals",
         points=["Pick one monthly number for eating out and split it into a few kinds of meals, so one big dinner does not use it all.",
                 "Count HST and tip: a $40 meal with 13% HST and a 15% tip is about $51.20 in your wallet.",
                 "A deal helps most on the meals you were going to have anyway, not on extra ones.",
                 "FIG is open to diners in Markham now, and free. A diner can claim a deal once a day.",
                 "Review the month in five minutes at the end, and move the number up or down."],
         sections=[
             ("The short answer", """<p>Choose one number for eating out each month, then divide it into three or four kinds of meal: quick lunches, relaxed dinners, treats and takeout. Work out each meal as it will appear on your card, with HST and tip, not as the menu price. On FIG, you can look for deals on the meals you were going to have anyway.</p>"""),
             ("Start with one number", """<p>Most people overspend on eating out because they have no number. Look at the last two or three months of card statements, add up what went to restaurants, cafes and takeout, and take the average. Then choose a figure for next month that you are comfortable with, even if it is a little lower. A number you can keep to is better than a perfect number you ignore.</p>
<p>Write it as a monthly figure and a weekly one. In an example, $240 a month is about $60 a week, which is easier to hold in your head on a Friday evening.</p>"""),
             ("What a menu price really costs", """<p>The price on the menu is not what you pay. Ontario's HST is 13%, and many people tip on top. Here is a round example, with a 15% tip on the pre-tax amount. The tip is an example, not a rule.</p>
<div class="callout math"><b>A $40 meal, all in (example)</b><table><thead><tr><th>Line</th><th>Amount</th></tr></thead><tbody>
<tr><td>Menu price</td><td>$40.00</td></tr>
<tr><td>HST at 13%</td><td>$5.20</td></tr>
<tr><td>Tip at 15% of $40</td><td>$6.00</td></tr>
<tr><td>Total</td><td>$51.20</td></tr>
</tbody></table><p>So a $40 meal costs about 28% more than the menu says: $51.20 &minus; $40.00 = $11.20, and $11.20 &divide; $40.00 = 0.28.</p></div>
<p>Do your budget with the all-in number. Otherwise a month of ten $40 meals is $400 on paper and $512 in real life.</p>"""),
             ("Split the number into kinds of meal", """<p>Here is an example split for $240 a month. Yours will differ, and the figures are round for easy checking.</p>
<table><thead><tr><th>Kind of meal</th><th>How many</th><th>All-in each</th><th>Total</th></tr></thead><tbody>
<tr><td>Quick lunch</td><td>6</td><td>$15</td><td>$90</td></tr>
<tr><td>Casual dinner</td><td>2</td><td>$35</td><td>$70</td></tr>
<tr><td>Takeout night</td><td>2</td><td>$25</td><td>$50</td></tr>
<tr><td>One treat</td><td>1</td><td>$30</td><td>$30</td></tr>
<tr><td><b>Total</b></td><td>11</td><td></td><td><b>$240</b></td></tr>
</tbody></table>
<p>Check the sum: $90 + $70 + $50 + $30 = $240. Eleven meals out in a month is a little under three a week.</p>"""),
             ("Where a deal fits", """<p>A deal is useful when it lowers the price of a meal you were already going to have. It is not useful when it talks you into an extra one. On FIG, you can browse places, menus, reviews and live deals on a map, and claim a deal in one tap. A diner can claim a deal once a day, so it suits regular meals better than a binge.</p>
<div class="callout math"><b>A 2 for 1 on a regular dinner (example)</b><ul><li>Two mains at $18 each, normally $36 before HST and tip.</li><li>With a 2 for 1, you pay for one: $18.</li><li>You saved $18 on that meal, which is half the bill.</li></ul><p>If your casual-dinner line has room for it, the saving could pay for another lunch. Check the real terms of each deal, because every restaurant sets its own.</p></div>
<p>Our guides on <a href="/blog/compare-restaurant-deals-worth-it">comparing restaurant deals</a> and <a href="/blog/date-night-markham-deals-budget">a date night for less</a> go through the arithmetic in more detail.</p>"""),
             ("Three habits that make the number stick", """<ol><li><strong>Choose the treat.</strong> A big dinner you looked forward to feels better than three small ones you forgot. Put it in the budget on purpose.</li><li><strong>Keep a running tally</strong> on your phone's notes, once a meal. It takes ten seconds.</li><li><strong>Check before you go.</strong> Look at the menu, the price and any deal first. It is easier to decide at home than at the table.</li></ol>
<p>Eating with a group? <a href="/blog/group-dining-deals">Group dining deals</a> covers how to split a bill fairly.</p>"""),
             ("What to expect from FIG", """<p>FIG is free for diners and open now in Markham. Check out deals at www.figpromo.ca/app.</p>
<ul><li>You can browse places, menus, reviews and live deals on a map.</li><li>You claim a deal in one tap and show a QR code that staff scan at the restaurant.</li><li>A deal code works once, and one diner can claim a deal once a day.</li><li>Location is optional and never limits a deal.</li><li>Guests can look around, but you need an account to claim, order, save or review. Diners must be 14 or older.</li></ul>
<p>FIG starts in Markham, then Richmond Hill and Vaughan Mills.</p>"""),
             ("Lunch, dinner and takeout: where the money goes", """<p>It helps to see which kind of meal costs you the most per dollar of enjoyment. A lunch out at $15 all-in is easy to repeat and easy to skip. A dinner at $35 is a bigger decision. A takeout night at $25 costs less than a dinner out but more than cooking.</p>
<p>On FIG, takeout is paid for online in the app at checkout, and it comes with a deal unless the restaurant sets takeout at full price. Whether or not a deal is on that night, check the price you see at checkout before you confirm, and put the total into your tally. There is no paying at the counter for takeout, so the amount in the app is the amount you spend.</p>
<div class="callout math"><b>Swapping one meal (example)</b><ul><li>Before: two takeout nights at $25 each is $50.</li><li>If one of them becomes a lunch at $15, you spend $25 + $15 = $40.</li><li>That leaves $10 spare, which is two-thirds of another lunch.</li></ul></div>"""),
             ("A five-minute month-end review", """<p>On the last day of the month, add up what you spent and compare it with the number. Ask two questions: which kind of meal went over, and which one gave you the most enjoyment for the money? Then move $10 or $20 from one line to the other. After two or three months, the budget fits how you actually eat.</p>
<p>If you eat out far less than your number, that is fine too. The point of the number is to choose, not to spend it.</p>"""),
             ("A note on tipping", """<p>Tipping is up to you and to the service you had. The 15% in the example is only there to make the arithmetic concrete. Use whatever you normally leave. Whatever it is, add it to your all-in figures, so your number stays honest.</p>"""),
         ],
         faq=[("How much should I budget for eating out each month?", "There is no right figure. Add up the last two or three months of card statements, take the average and choose a number you are comfortable with, even if it is a little lower."),
              ("Should I count HST and tip in my restaurant budget?", "Yes. Ontario's HST is 13%, and tips come on top. In the example, a $40 meal comes to about $51.20 with HST and a 15% tip."),
              ("When can I use FIG as a diner?", "Now. FIG is open to diners in Markham: check out deals at www.figpromo.ca/app, with no account needed to look around."),
              ("Is FIG free for diners?", "Yes. FIG is free for diners."),
              ("How often can I claim the same deal?", "A diner can claim a deal once a day."),
              ("Do I have to share my location?", "No. Location is optional and never limits a deal."),
              ("Which deals save the most?", "The ones on meals you would have had anyway. A 2 for 1 on two $18 mains saves $18, half of that bill, but only if you did not add a meal you would have skipped.")]),

    dict(slug="read-your-deal-results-keep-change-or-stop", screen="tdash", title="Reading your deal results: keep, change or stop a deal", date="2026-11-04", publish_at="2026-11-04T12:00:00-05:00", updated="2026-11-05", topic="For restaurants", group="fill-quiet-hours",
         dek="Your dashboard shows results deal by deal. How to review a deal after two weeks, three questions to ask, and a worked example of the arithmetic that tells you whether to keep it, change it or end it.",
         desc="How restaurant owners can read deal-by-deal results on FIG and decide whether to keep, change or stop a deal, with a worked example.",
         seo="How to read your restaurant deal results: keep, change or stop",
         keywords="restaurant deal results, measure a restaurant promotion, is my restaurant deal working, restaurant promotion math, quiet hours deal review, Markham restaurants, FIG dashboard",
         points=["Your FIG dashboard shows results deal by deal, so you can judge each deal on its own.",
                 "Give a deal at least two weeks and change one thing at a time.",
                 "Ask three questions: did the quiet window fill, who used the deal, and what did each use leave you?",
                 "Your own till tells you how many diners would have come anyway. The dashboard cannot know that for you.",
                 "At the end of a review, keep, change or stop the deal, and write down the date and the reason."],
         sections=[
             ("The short answer", """<p>After a deal has run for two weeks, open your dashboard, read the results for that one deal, and compare them with your own till for the same hours. Ask whether the quiet window filled, whether new faces came, and what each use left you after food cost. Then do one of three things: keep the deal, change one setting, or stop it.</p>"""),
             ("Why review a deal at all", """<p>A deal is a bet on your quiet hours. Some bets pay off, some break even and some cost money without anyone noticing. The difference is easy to see if you look, and easy to miss if you do not. Looking takes ten minutes every two weeks, which is less time than it takes to make one batch of dough.</p>"""),
             ("What you have to look at", """<table><thead><tr><th>Source</th><th>What it shows you</th></tr></thead><tbody>
<tr><td>FIG dashboard</td><td>Results deal by deal, including how many diners used each deal</td></tr>
<tr><td>Your till or sales report</td><td>How busy the same hours were before the deal, and during it</td></tr>
<tr><td>Your kitchen notes</td><td>Whether the rush was manageable or whether the deal swamped the line</td></tr>
<tr><td>Your reviews</td><td>What diners said about the visit. You can reply to them in the app</td></tr>
</tbody></table>
<p>The dashboard tells you what the deal did. Only your own records can tell you what would have happened without it.</p>"""),
             ("Give it two weeks", """<p>A single day proves nothing. A rainy Tuesday, a school holiday or a road closure can change a lunch hour more than any deal can. Two full weeks, with the same hours each week, gives you at least two samples of each weekday. If you can wait four weeks, better still.</p>
<p>During the test, do not change the deal, the hours or the price. If you change three things, you will not know which one made the difference.</p>"""),
             ("Three questions to ask", """<ol><li><strong>Did the quiet window fill?</strong> Compare the hours of the deal with the same hours before it. A deal can have many uses and still leave the room just as empty if the uses were all in an hour that was already busy.</li><li><strong>Who used it?</strong> Regulars who would have come at full price, or new diners? Staff will usually know. If your regulars are the ones using it, the deal is a discount, not a draw.</li><li><strong>What did each use leave you?</strong> This is the arithmetic, shown below.</li></ol>"""),
             ("A worked example", """<p>These are round example numbers, not a real restaurant. A $15.00 dish costs $4.50 to make (a food cost of 30%). A deal takes $3.00 off, and the deal is dine-in, so FIG takes nothing from the bill. Over two weeks the dashboard shows 40 uses. Your till and your staff tell you that about 25 of those diners would have come anyway, and 15 would not.</p>
<div class="callout math"><b>Two weeks of a $3 off deal (example)</b><table><thead><tr><th>Line</th><th>Working</th><th>Amount</th></tr></thead><tbody>
<tr><td>Left from a dish at the deal price</td><td>$15.00 &minus; $3.00 &minus; $4.50</td><td>$7.50</td></tr>
<tr><td>Left from the same dish at full price</td><td>$15.00 &minus; $4.50</td><td>$10.50</td></tr>
<tr><td>Cost of the 25 who would have come anyway</td><td>25 &times; $3.00</td><td>&minus; $75.00</td></tr>
<tr><td>Earned from the 15 new diners</td><td>15 &times; $7.50</td><td>+ $112.50</td></tr>
<tr><td><b>Net for the two weeks</b></td><td>$112.50 &minus; $75.00</td><td><b>+ $37.50</b></td></tr>
</tbody></table></div>
<p>The deal is positive here, but only by a little, and the result depends heavily on the 25-and-15 split. If 30 had come anyway and 10 were new, the cost is 30 &times; $3.00 = $90.00 and the gain is 10 &times; $7.50 = $75.00, a net of &minus; $15.00. The same deal flips from a gain to a loss. That is why the split matters more than the total.</p>"""),
             ("Keep, change or stop", """<table><thead><tr><th>What you see</th><th>Try</th></tr></thead><tbody>
<tr><td>Quiet window filled, net positive</td><td>Keep it. Consider more uses per diner, with a wait between uses</td></tr>
<tr><td>Many uses, window already busy</td><td>Move the deal to a quieter window</td></tr>
<tr><td>Mostly regulars</td><td>Narrow the hours, lower the discount or change the deal type</td></tr>
<tr><td>Few uses</td><td>Check the photo, the dish and the hours. Then try another dish before cutting the discount</td></tr>
<tr><td>Too many uses for the kitchen</td><td>Shorten the hours or add a limit. For takeout, use pause and prep time</td></tr>
<tr><td>Net negative after two weeks</td><td>Stop it, and write down what you learned</td></tr>
</tbody></table>
<p><a href="/blog/deals-used-more-than-once-uses-per-diner-wait-between-uses">Uses per diner and the wait between uses</a> explains the two settings, and <a href="/blog/deal-types-percent-dollar-2-for-1">the deal-type guide</a> helps when it is the type that needs to change.</p>"""),
             ("Change one thing at a time", """<p>If a deal needs fixing, change a single setting and run it for another two weeks. The settings you can change are the discount, the dish, the days and hours, the uses per diner and the wait between uses. Posting a deal live now or scheduled is also up to you, so a change can be set to start on a Monday.</p>
<p>Keep a notes page with a line for each change: the date, what you changed, why and what happened. In three months you will be glad of it.</p>"""),
             ("Share the numbers with your team", """<p>The people who work the quiet shift know things the dashboard does not: which regulars came, whether the new faces ordered a drink, whether the room felt busier. Ask them two questions at the end of the two weeks: who used the deal, and what did you notice? Write the answers next to your numbers. A thirty-second talk at the end of a shift is often the most useful part of the review, and it also shows the team that the deal is something they have a say in.</p>"""),
             ("Do not forget the reviews", """<p>Numbers do not show how a diner felt. Read what diners say about their visits, and reply. A review that says the line was too long tells you more than a use count can. Reviews come only from scanned visits, so each one is from someone who really came. <a href="/blog/reply-to-reviews-restaurants">Replying to reviews</a> shows how.</p>"""),
             ("Your first weeks", """<p>Results build up as diners find your deals, so the first numbers are small. Set up each deal so you can judge it later: choose a quiet window, do the arithmetic from <a href="/blog/slow-hour-deal-math">the slow-hour math</a> and write down your guess for how many new diners it will bring. After a few weeks, you will have something to compare it with.</p>"""),
         ],
         faq=[("Where do I see how a deal is doing?", "Your dashboard shows results deal by deal."),
              ("How long should I run a deal before judging it?", "At least two weeks, with the same hours each week, and without changing the deal while you wait."),
              ("Can the dashboard tell me whether a diner would have come anyway?", "No. Only your own till, your staff and your regulars can tell you that, which is why the arithmetic uses your own numbers."),
              ("What should I change first if a deal is not working?", "Change one thing at a time: the hours, the dish, the discount, the uses per diner or the wait between uses."),
              ("How do I know whether a deal pays?", "Compare its results on your dashboard with your own till, then do the arithmetic on what each use leaves you after food cost."),
              ("Do restaurants see diners' phone numbers?", "No. Restaurants never see diners' phone numbers."),
              ("How soon can I read results?", "As soon as diners start viewing and claiming your deal. Give a new deal a few weeks before you judge it, since the first numbers are small.")]),

    dict(slug="browse-fig-as-a-guest-or-make-an-account-markham-diners", screen="map", title="Browsing FIG as a guest: what you can do before you make an account", date="2026-11-05", publish_at="2026-11-05T12:00:00-05:00", updated="2026-11-05", topic="For diners", group="eat-out-for-less",
         dek="You can look around FIG without signing up. What a guest can see, what needs an account, how to use the map to choose a place, and a short routine for deciding where to eat.",
         desc="What you can do on FIG as a guest in Markham, what needs an account (claiming, ordering, saving, reviewing), and how to choose a restaurant from the map.",
         seo="Browse FIG as a guest: what you can do without an account",
         keywords="browse restaurant deals Markham, FIG guest, restaurant deals app no account, find restaurants on a map, Markham restaurants, FIG web app",
         points=["FIG is free for diners and open on the web at www.figpromo.ca/app. Home works as a guest, so browsing needs no account.",
                 "A guest can look at places, menus, reviews and live deals on a map.",
                 "You need an account to claim a deal, order, save a place or write a review.",
                 "Location is optional and never limits a deal, so you can look at any part of Markham.",
                 "A short routine helps: pick a meal, scan the map, read the menu and the reviews, then claim only when you are ready to go."],
         sections=[
             ("The short answer", """<p>Yes, you can use FIG without an account. Open www.figpromo.ca/app and Home works as a guest: you can browse places, menus, reviews and live deals on a map. You only need an account when you want to claim a deal, order, save a place or write a review. FIG is free for diners.</p>"""),
             ("What a guest can do", """<p>Think of guest mode as window shopping. You can walk down the street, read the menus in the windows and see which places have a deal on right now, before you commit to anything. That is useful on its own, because choosing where to eat is often the longest part of going out.</p>
<table><thead><tr><th>You want to</th><th>As a guest</th><th>With an account</th></tr></thead><tbody>
<tr><td>See places and live deals on the map</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Read menus and reviews</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Claim a deal</td><td>No</td><td>Yes, in one tap</td></tr>
<tr><td>Order takeout</td><td>No</td><td>Yes</td></tr>
<tr><td>Save a place</td><td>No</td><td>Yes</td></tr>
<tr><td>Write a review</td><td>No</td><td>Yes, after a scanned visit</td></tr>
</tbody></table>
<p>Diners must be 14 or older to have an account.</p>"""),
             ("Why browsing first is a good habit", """<p>Most bad meals out come from deciding in a hurry. You are hungry, you are standing on a plaza and you pick the first place with a short line. Looking first, even for two minutes, changes that. You find out what is open, what a main costs and what other people thought of it.</p>
<p>Because location is optional and never limits a deal, you can also look ahead. If you work in one part of Markham and live in another, you can look at both and decide which suits tonight.</p>"""),
             ("A five-step routine for choosing a place", """<ol><li><strong>Pick the kind of meal.</strong> A quick lunch, a family dinner and a snack with a friend are different jobs. Decide first, so you are not comparing a coffee shop with a sit-down restaurant.</li><li><strong>Scan the map.</strong> Look for places near where you will be, and notice which ones have a live deal right now.</li><li><strong>Open the menu.</strong> Check that there is something you want at a price you are happy with. A deal on a dish you do not like is not a deal.</li><li><strong>Read the reviews.</strong> Reviews come only from scanned visits, so each one is from someone who actually went. <a href="/blog/how-to-read-restaurant-reviews">How to read a restaurant's reviews on FIG</a> shows what to look for.</li><li><strong>Decide how you will pay.</strong> For a dine-in deal, you show the code and pay the restaurant as usual. For takeout, you pay in the app at checkout.</li></ol>"""),
             ("What the map shows, and what it does not", """<p>The map is a good way to see what is nearby and what is on offer now. It does not tell you how busy a place is, whether a table is available or whether the kitchen has run out of a dish. For a larger group, or if you have dietary needs, a quick call to the restaurant is still the best step. <a href="/blog/eating-out-dietary-needs-allergies-markham">Eating out with dietary needs or allergies</a> covers what to ask.</p>"""),
             ("When it is worth making an account", """<p>Make an account when you find a deal you want to use. Claiming is one tap, and then you show a QR code that staff scan at the restaurant. A few things are worth knowing before you do:</p>
<ul><li>A deal code works once.</li><li>If the restaurant lets a deal be used more than once (up to 20 times, with an optional wait between uses), your screen shows a new code after each scan.</li><li>You can claim a deal once a day.</li><li>Restaurants never see your phone number.</li></ul>
<p>The value of a deal is the saving on the meal itself.</p>"""),
             ("A worked example: two minutes of looking", """<div class="callout example"><b>Choosing lunch (example)</b><ul><li>You have about $15 to spend on lunch, all in, and you can walk ten minutes.</li><li>On the map you see six places nearby, and two of them have a deal on right now.</li><li>You open the menus. One deal is on a dish you like. The other is on something you would not order.</li><li>You read three reviews for the first place, and they match what you want: a quick lunch.</li></ul><p>Total time: about two minutes. You walk over knowing what you will order, and you claim the deal on the way.</p></div>
<p>The numbers are only an example. The point is the order of steps: look, read, then claim.</p>"""),
             ("If you are not sure about a deal", """<p>Read the terms on the deal before you go. If anything is unclear, such as the hours it is live or whether it applies to your dish, ask the staff when you arrive. Everyone does better when the deal is understood on both sides of the counter. If a code will not scan, <a href="/blog/deal-wont-scan-troubleshooting-diners">what to check and what to say</a> has a short checklist.</p>"""),
             ("Using FIG with friends or family", """<p>Browsing as a guest is also a good way to settle a group decision. Open the map together, look at two or three places and read the menus out loud. Everyone can see the same thing without anyone needing to sign up first. Once the group has chosen, one person makes an account and claims the deal, or each person claims their own, since a diner can claim a deal once a day. If the group is large, call ahead as well. <a href="/blog/group-dining-deals">Group dining deals</a> has more on choosing a place and splitting the bill.</p>"""),
             ("Privacy, in plain words", """<p>Looking around as a guest asks nothing of you. When you do make an account, you are in control of what you do with it: you claim, order, save and review by choice. Restaurants never see diners' phone numbers, and location is optional. If you have a question about your account or about FIG, you can reach FIG on the contact page at www.figpromo.ca/contact.</p>"""),
             ("What is coming", """<p>FIG is on the web today. The iPhone and Android apps are coming. FIG starts in Markham, then Richmond Hill and Vaughan Mills. To start looking, check out deals at www.figpromo.ca/app.</p>"""),
         ],
         faq=[("Do I need an account to look at deals on FIG?", "No. Home works as a guest, so you can browse places, menus, reviews and live deals on a map without an account."),
              ("What do I need an account for?", "Claiming a deal, ordering, saving a place and writing a review."),
              ("Is FIG free for diners?", "Yes. FIG is free for diners."),
              ("Where do I use FIG?", "On the web at www.figpromo.ca/app. The iPhone and Android apps are coming."),
              ("Do I have to share my location?", "No. Location is optional and never limits a deal."),
              ("How old do I have to be?", "Diners must be 14 or older."),
              ("Can restaurants see my phone number?", "No. Restaurants never see diners' phone numbers.")]),

    dict(slug="free-with-a-dish-deal-pricing-restaurant-math", screen="tdash", title="A 'free with a dish' deal: what it costs you, with the math", date="2026-11-06", publish_at="2026-11-06T12:00:00-05:00", updated="2026-11-06", topic="For restaurants", group="fill-quiet-hours",
         dek="Give a drink, a side or a dessert with a main, and the real cost is your food cost, not your menu price. A worked example, how to choose the item, and how it compares with a dollar off.",
         desc="How to price a 'free with a dish' restaurant deal on FIG: what the free item really costs, a worked example and when it beats a dollar-off deal.",
         seo="Free with a dish: pricing a restaurant deal, with the math",
         keywords="free with a dish deal, restaurant combo deal math, restaurant promotion cost, free drink with a meal, food cost, Markham restaurants, FIG deal types",
         points=["On FIG a deal can be 2 for 1, percent off, dollar off, or free with a dish.",
                 "With a free item, the cost to you is what the item costs to make, not what it sells for.",
                 "Choose an item with a high menu price and a low food cost, such as a drink or a side, and one that fits the main.",
                 "Compare it with a dollar-off deal using the same arithmetic: what does one use leave you?",
                 "Start with a quiet window, a limit on uses per diner and two weeks of results on your dashboard."],
         sections=[
             ("The short answer", """<p>A free-with-a-dish deal gives the diner an extra item when they order a dish. It costs you what that item costs to make, not the price on your menu, so a drink or a side can be a cheap way to bring people in. Work out the food cost of the item, add it to the cost of the main, and check what each use leaves you.</p>"""),
             ("What the deal is", """<p>On FIG, a restaurant can post a deal as 2 for 1, percent off, dollar off, or free with a dish. The last one is a pairing: the diner orders a dish and gets another item with it. You choose the dish, the extra item, the hours, how many times one diner can use it and how long they wait between uses. You can post it live now or scheduled. <a href="/blog/deal-types-percent-dollar-2-for-1">Which type suits which restaurant</a> compares all four.</p>"""),
             ("Why the cost is not the menu price", """<p>If a drink sells for $3.50, giving it away does not cost you $3.50. It costs the ingredients, the cup and the few seconds of staff time. A dollar-off deal is different: $3.00 off is $3.00 gone from the till, every time. That is why a free item can look generous to the diner while costing you much less than the same amount taken off the bill.</p>
<p>The catch is that this only works for items with a low food cost. A steak and a soda are very different things to give away.</p>"""),
             ("A worked example", """<p>These are round example numbers, not a real restaurant. A main sells for $16.00 and costs $4.80 to make. A drink sells for $3.50 and costs $0.70 to make. The deal is dine-in, so FIG takes nothing from the bill.</p>
<div class="callout math"><b>One use of a free drink with a $16 main (example)</b><table><thead><tr><th>Line</th><th>Working</th><th>Amount</th></tr></thead><tbody>
<tr><td>Main at full price</td><td>$16.00 &minus; $4.80</td><td>$11.20 left</td></tr>
<tr><td>Main with a free drink</td><td>$16.00 &minus; $4.80 &minus; $0.70</td><td>$10.50 left</td></tr>
<tr><td>Main with $3.50 off instead</td><td>$16.00 &minus; $3.50 &minus; $4.80</td><td>$7.70 left</td></tr>
<tr><td><b>Difference, free drink vs $3.50 off</b></td><td>$10.50 &minus; $7.70</td><td><b>$2.80 more for you</b></td></tr>
</tbody></table></div>
<p>The diner sees a $3.50 drink for nothing, and you give up $0.70. The $3.50 off deal costs you the full $3.50. If the diner would have bought the drink anyway, the picture changes: the drink was a sale at $3.50 with $2.80 left after its cost, and now you earn nothing from it. That is the same question as in <a href="/blog/read-your-deal-results-keep-change-or-stop">reading your deal results</a>: who would have come, and what would they have bought, anyway?</p>"""),
             ("Choosing the item", """<table><thead><tr><th>Good choice</th><th>Why</th></tr></thead><tbody>
<tr><td>A fountain drink, tea or coffee</td><td>Low food cost, quick to serve</td></tr>
<tr><td>A small side or a soup</td><td>Easy to prepare in batches</td></tr>
<tr><td>A small dessert</td><td>Gives the diner a reason to stay and tells them what else you make</td></tr>
<tr><td>A topping or an upgrade</td><td>Low cost, and diners remember it</td></tr>
</tbody></table>
<p>Avoid items that are expensive to make, slow to prepare or that you often run short of. If the free item is out, the deal is out, and a diner who was promised a dessert and told it is gone is not a happy diner.</p>"""),
             ("Choosing the main", """<p>Pair the free item with a main that you want to sell more of, one with a good margin that is easy for the kitchen. A deal on your slowest, least profitable dish is hard to justify. A deal on a popular dish that is already in the kitchen's rhythm is easy to serve and easy to repeat.</p>
<p>Name the pairing clearly, so the diner and the staff both know what it is. A short description is enough.</p>"""),
             ("When it beats the other types", """<ul><li><strong>Against dollar off:</strong> better when the extra item has a low food cost, as in the example above.</li><li><strong>Against percent off:</strong> better when you want to protect the price of the main. The menu price stays the same.</li><li><strong>Against 2 for 1:</strong> better when you want to bring in one diner rather than two.</li></ul>
<p>It is worse when the item costs a lot to make, or when most diners would have ordered it anyway.</p>"""),
             ("Watch for the common mistakes", """<ul><li><strong>Choosing an item the kitchen cannot spare.</strong> If the free item is the one that is always running out, pick another.</li><li><strong>Forgetting the main's cost.</strong> The deal is only worth running if the main still leaves you something. In the example, $10.50 is left after the main and the free drink. If a main only leaves $3.00 after its cost, a free item of any size can wipe it out.</li><li><strong>Giving the same item to everyone all day.</strong> A deal for a quiet window brings people in when you need them. The same deal at the lunch rush only gives away items to people who were already coming.</li><li><strong>Not telling the team.</strong> A free item that the server did not know about is a free item argued about at the counter.</li></ul>"""),
             ("A second example: a free dessert", """<p>Here is another round-number example, to show that the same steps work for a different item. A main sells for $18.00 and costs $5.40 to make. A dessert sells for $7.00 and costs $1.40 to make. With the dessert free, what is left from the main is $18.00 &minus; $5.40 &minus; $1.40 = $11.20. Without the deal and without the dessert it is $12.60. So a diner who would have ordered only the main costs you $1.40 for that use. A diner who was never going to come at all brings you $11.20. If the deal brings in even a few diners like that on a quiet afternoon, it can pay for the cost of the free desserts given to others.</p>"""),
             ("Setting it up", """<ol><li>Choose a quiet window, using <a href="/blog/slow-hour-deal-math">the slow-hour math</a>.</li><li>Do the arithmetic above with your own food costs.</li><li>Set the uses per diner. One is a good start. If you want regulars to come back, <a href="/blog/deals-used-more-than-once-uses-per-diner-wait-between-uses">uses per diner and the wait between uses</a> shows how.</li><li>Brief your team, so everyone knows what the free item is and how to scan the code. <a href="/blog/train-staff-honour-fig-deal">Train your staff in 10 minutes</a>.</li><li>Check the results after two weeks.</li></ol>
<p>If the deal comes with takeout, remember the takeout fees: FIG keeps 5% of the food after any deal and before tax, on takeout orders only, and Stripe's card fee comes off the payment. <a href="/blog/takeout-order-math-what-you-keep">Takeout order math</a> has the arithmetic.</p>"""),
         ],
         faq=[("What does 'free with a dish' mean on FIG?", "It is one of four deal types, alongside 2 for 1, percent off and dollar off. The diner orders a dish and gets another item with it."),
              ("What does a free item cost me?", "What it costs to make, not its menu price. In the example, a $3.50 drink that costs $0.70 to make costs you $0.70."),
              ("Which items work best as the free item?", "Items with a low food cost that are quick to serve, such as drinks, small sides, soup or a small dessert."),
              ("Can I limit how often a diner uses it?", "Yes. You set uses per diner, and an optional wait between uses. A diner can claim a deal once a day."),
              ("Does FIG take a cut of a dine-in deal?", "No. FIG takes nothing on dine-in. It earns only on takeout orders paid in the app."),
              ("How do I know whether the deal is paying off?", "Read the results for that deal on your dashboard and compare them with your own till and your food costs, after at least two weeks."),
              ("Does it cost anything to post a deal?", "No. Posting deals costs restaurants nothing.")]),

    dict(slug="weekday-lunch-markham-for-less-deals-math", screen="claim", title="Weekday lunch in Markham for less: a work-week guide, with the math", date="2026-11-07", publish_at="2026-11-07T12:00:00-05:00", updated="2026-11-07", topic="For diners", group="eat-out-for-less",
         dek="Five lunches out is a real number once HST and tip are in. A way to look at a work week of lunches, where a deal helps, and the arithmetic for a dollar-off deal and a 2 for 1 with a colleague.",
         desc="A work-week lunch budget for Markham diners, with HST and tip in the math, and how a dollar-off deal or a 2 for 1 with a colleague changes it.",
         seo="Weekday lunch in Markham for less: the math",
         keywords="cheap lunch Markham, weekday lunch deals Markham, lunch budget, 2 for 1 lunch, eating out on a budget, restaurant deals Markham, FIG",
         points=["A $12 lunch comes to about $15.36 once HST and a 15% tip are added, so five lunches a week is about $76.80 in the example.",
                 "A dollar-off deal reduces the price before HST, so it saves a little more than its face value.",
                 "A 2 for 1 with a colleague cuts each person's lunch to about $8.58 in the example.",
                 "A diner can claim a deal once a day, so a deal fits best on the days you were going out anyway.",
                 "Browse live deals on the FIG map as a guest, and make an account when you want to claim one."],
         sections=[
             ("The short answer", """<p>Count a weekday lunch at its full price: the menu price, HST and a tip. In the example below, a $12 lunch costs $15.36, so five a week is $76.80. A $3 off deal on one of them saves about $3.39, and a 2 for 1 with a colleague saves about $6.78 each. Deals help most on the lunches you were already going to buy.</p>"""),
             ("Start with the real price", """<p>The number on the menu is not what leaves your account. In Ontario, HST is 13% on most restaurant meals, and a tip goes on top. This post uses 15% for the tip only to make the arithmetic concrete. Use whatever you normally leave.</p>
<div class="callout math"><b>One $12 lunch, all in (example)</b><ul><li>Menu price: $12.00.</li><li>HST at 13%: $12.00 &times; 0.13 = $1.56.</li><li>Tip at 15% of the menu price: $12.00 &times; 0.15 = $1.80.</li><li>Total: $12.00 + $1.56 + $1.80 = <b>$15.36</b>.</li></ul><p>Five of these in a work week: 5 &times; $15.36 = <b>$76.80</b>. Four weeks: $307.20.</p></div>
<p>If you are used to thinking of lunch as "twelve bucks", that is a surprise. It is also a reason to look for a saving, even a small one.</p>"""),
             ("Where a deal fits in a work week", """<p>A deal is worth the most on a lunch you would have bought anyway. A saving on a meal you did not need is not a saving. Here is a simple way to sort a week:</p>
<table><thead><tr><th>Day</th><th>Type of lunch</th><th>Deal to look for</th></tr></thead><tbody>
<tr><td>Monday</td><td>Packed lunch from home</td><td>None needed</td></tr>
<tr><td>Tuesday</td><td>Out, on your own</td><td>Dollar off or percent off</td></tr>
<tr><td>Wednesday</td><td>Out with a colleague</td><td>2 for 1</td></tr>
<tr><td>Thursday</td><td>Packed lunch or leftovers</td><td>None needed</td></tr>
<tr><td>Friday</td><td>Out, a treat</td><td>Whichever is live near you</td></tr>
</tbody></table>
<p>This is only an example of a week. Yours will look different, and that is fine. The point is to choose the days, rather than let the week choose them for you.</p>"""),
             ("A dollar-off deal on your own lunch", """<p>A $3 off deal takes $3.00 off the menu price, and the HST is worked out on the lower price. That means the saving is a little more than $3.00.</p>
<div class="callout math"><b>The same lunch with $3 off (example)</b><ul><li>Price after the deal: $12.00 &minus; $3.00 = $9.00.</li><li>HST at 13%: $9.00 &times; 0.13 = $1.17.</li><li>Tip, still on the $12.00 menu price: $1.80.</li><li>Total: $9.00 + $1.17 + $1.80 = <b>$11.97</b>.</li><li>Saving: $15.36 &minus; $11.97 = <b>$3.39</b>.</li></ul></div>
<p>The extra $0.39 is the HST on the $3.00. If you tip on the lower price instead, you save a bit more, because the tip is smaller too. Either way, the saving is real but modest, so it is best on days when you are going out regardless.</p>
<p>The tax rule behind this is that a store's own coupon or discount lowers the price before tax is worked out. The Canada Revenue Agency sets this out in its guide for GST/HST registrants (RC4022, "Coupons").</p>"""),
             ("A 2 for 1 with a colleague", """<p>A 2 for 1 is the bigger saving, and it needs two people. Two colleagues each order a $12 lunch, and the second lunch costs nothing.</p>
<div class="callout math"><b>Two $12 lunches on a 2 for 1 (example)</b><ul><li>Price after the deal: $12.00 for the two of you.</li><li>HST at 13%: $12.00 &times; 0.13 = $1.56.</li><li>Tip, on the $24.00 menu value: $24.00 &times; 0.15 = $3.60.</li><li>Total: $12.00 + $1.56 + $3.60 = <b>$17.16</b>, or <b>$8.58</b> each.</li><li>Without the deal: $15.36 each. Saving: $15.36 &minus; $8.58 = <b>$6.78</b> each.</li></ul></div>
<p>If you split the bill, <a href="/blog/group-dining-deals">group dining deals</a> shows how to do it fairly, including how to handle a tip.</p>"""),
             ("What about tipping and the staff?", """<p>It is fair to tip on the value of the meal you would have paid for, and many diners do, since the server does the same work. This post tips on the menu price in the examples. If you tip on the lower price, your saving is a little larger, and you can decide what feels right. Whatever you decide, put it into your tally so the number stays honest.</p>"""),
             ("What a month looks like", """<div class="callout example"><b>Four weeks, three lunches out a week (example)</b><ul><li>Without any deal: 12 lunches &times; $15.36 = <b>$184.32</b>.</li><li>With a $3 off deal on 4 of them: 4 &times; $3.39 = $13.56 saved.</li><li>With a 2 for 1 on 4 of them: 4 &times; $6.78 = $27.12 saved.</li><li>Both together, on 8 of the 12 lunches: $13.56 + $27.12 = $40.68 saved, leaving <b>$143.64</b>.</li></ul></div>
<p>These are example numbers. Your lunches, your prices and your tip will differ, but you can redo the sums in two minutes. <a href="/blog/monthly-eating-out-budget-markham-diners">A monthly eating-out budget</a> shows how to fit lunches into a bigger number.</p>"""),
             ("How to find a lunch deal on FIG", """<p>FIG is free for diners. You can browse places, menus, reviews and live deals on a map without an account. When you find one you want, make an account, claim it in one tap and show the QR code that staff scan at the restaurant. A few rules help to know:</p>
<ul><li>A diner can claim a deal once a day.</li><li>A deal code works once. If the restaurant lets a deal be used more than once, your screen shows a new code after each scan.</li><li>Location is optional and never limits a deal.</li></ul>
<p>Check the hours of the deal. A lunch deal that ends at 2 pm is no use at 2:15. If you are not sure, <a href="/blog/compare-restaurant-deals-worth-it">how to compare restaurant deals</a> helps you decide whether it is worth it.</p>"""),
             ("Takeout at lunch", """<p>If you would rather pick lunch up, takeout on FIG is paid for online in the app at checkout. The card is held and charged when the restaurant accepts, and nothing is charged if the restaurant declines. There is no paying at the counter, and the pickup code only confirms collection. Takeout comes with a deal unless the restaurant has set takeout at full price, so check the total at checkout. <a href="/blog/takeout-or-dine-in-with-a-deal-which-costs-less">Takeout or dine-in with a deal</a> compares the two.</p>"""),
             ("Small habits that add up", """<ul><li>Look at the map on the morning of a lunch out, not at noon when you are hungry.</li><li>Ask a colleague on the days you want a 2 for 1.</li><li>Keep one lunch a week as a treat, with no deal at all. A budget you enjoy is a budget you keep.</li></ul>
<p>To start looking, check out deals at www.figpromo.ca/app. FIG is open in Markham now, and it is expanding to Richmond Hill and Vaughan Mills.</p>"""),
         ],
         faq=[("How much does a weekday lunch really cost?", "More than the menu price. In the example, a $12 lunch comes to $15.36 with 13% HST and a 15% tip."),
              ("Does a dollar-off deal reduce the HST?", "Yes. A store's own discount lowers the price before HST is worked out, so $3 off a $12 lunch saves $3.39 with HST in the example."),
              ("How much does a 2 for 1 save two colleagues?", "In the example, about $6.78 each, bringing a $15.36 lunch to $8.58."),
              ("How often can I claim the same deal?", "A diner can claim a deal once a day."),
              ("Do I need an account to look for lunch deals?", "No. You can browse places, menus, reviews and live deals on the map as a guest. You need an account to claim a deal."),
              ("Is FIG free for diners?", "Yes. FIG is free for diners."),
              ("Where can I use FIG?", "In Markham, on the web at www.figpromo.ca/app. FIG is expanding to Richmond Hill and Vaughan Mills.")]),

    dict(slug="keep-your-fig-page-current-hours-menu-prices", screen="tscanner", title="Keep your FIG page current: hours, menu and prices", date="2026-11-08", publish_at="2026-11-08T12:00:00-05:00", updated="2026-11-08", topic="For restaurants", group="fill-quiet-hours",
         dek="A page that is out of date costs you trust the first time a diner arrives at a closed door. A short routine for your opening hours, menu sections, photos and prices, and who on your team should look after each.",
         desc="A simple routine for Markham restaurants to keep their FIG opening hours, menu, photos and prices up to date, with a checklist and a table of when to update.",
         seo="Keep your restaurant page current: hours, menu and prices",
         keywords="restaurant opening hours online, update restaurant menu, restaurant listing accuracy, restaurant holiday hours, menu prices, Markham restaurants, FIG restaurant page",
         points=["Diners on FIG see your opening hours, menu with photos and sections, reviews and live deals, so each needs to be right.",
                 "Check your page on a fixed day each week. Five minutes is enough.",
                 "Update hours before holidays and before any closure, not after.",
                 "When a price changes in the kitchen or on the till, change it on your FIG menu the same day.",
                 "Owners and managers can look after the page. Decide who does it, so it is never nobody's job."],
         sections=[
             ("The short answer", """<p>Choose one day a week, open your FIG page as a diner would, and check three things: your opening hours, your menu and your prices. Fix anything that is wrong that day. Update your hours before a holiday or a closure rather than after, and give one person the job, so it is not left to chance.</p>"""),
             ("Why it matters", """<p>When a diner finds your deal on the map, they are making a trip: they will walk or drive to you. If the page says you are open and the door is locked, the diner is annoyed with you, not with the page. If the menu shows a dish you stopped making, or a price that is lower than the till, the conversation at the counter starts badly.</p>
<p>Reviews on FIG come only from scanned visits, so every review is from a diner who really came. A visit that begins with a surprise is more likely to end with a lower rating. Keeping the page right is one of the cheapest ways to protect your stars.</p>"""),
             ("What diners see", """<table><thead><tr><th>Part of your page</th><th>What it is for</th><th>How often to check</th></tr></thead><tbody>
<tr><td>Opening hours</td><td>Tells diners when to come</td><td>Weekly, and before every holiday</td></tr>
<tr><td>Menu sections and dishes</td><td>Lets diners choose before they arrive</td><td>Weekly, and whenever the menu changes</td></tr>
<tr><td>Prices</td><td>Sets what diners expect to pay</td><td>Whenever a price changes</td></tr>
<tr><td>Photos</td><td>Is the first thing diners look at</td><td>When a dish changes, or each season</td></tr>
<tr><td>Live deals</td><td>Brings in diners for your quiet hours</td><td>Weekly, with your results</td></tr>
<tr><td>Reviews and replies</td><td>Shows how visits went</td><td>A few times a week</td></tr>
</tbody></table>"""),
             ("Opening hours", """<p>Your opening hours are the most important line on the page. Set them to match the real days and times you serve, including any day you are closed. Then think ahead:</p>
<ul><li>Update the hours before a holiday, not on the morning of it.</li><li>If you will close early for a private event or a staff day, change it as soon as you know.</li><li>If a deal is scheduled for a time you are going to be closed, change or end the deal too.</li></ul>
<p>It helps to keep a short list of the dates you are closed each year, so you can check the page against it. <a href="/blog/restaurant-checklist-before-fig-opens-january-2027">The go-live checklist</a> covers hours as part of the first setup.</p>"""),
             ("Menu, sections and photos", """<p>Your menu on FIG has sections and photos. Keep the sections in the order a diner would read them, with your best-known dishes near the top. When you add or remove a dish on the printed menu, do the same online the same day.</p>
<p>A photo that no longer matches the plate is worse than no photo. Retake it when the dish changes. <a href="/blog/menu-photos-restaurant-phone-photography-fig">How to photograph your dishes with a phone</a> shows how, and it takes about as long as it does to plate the dish.</p>"""),
             ("Prices", """<p>Prices are where the page and the till most often drift apart. Food costs go up, a supplier changes, and the till is updated but the page is not. The result is a diner who expects $14.00 and is asked for $15.50.</p>
<div class="callout math"><b>A small price change, checked (example)</b><ul><li>A dish on the page costs $14.00. In the kitchen it costs $4.20 to make, which is 30% of the price.</li><li>Your supplier's costs rise, and the dish now costs $4.90 to make.</li><li>At $14.00, the food cost is now $4.90 &divide; $14.00 = 35%.</li><li>To get back to 30%, the price would be $4.90 &divide; 0.30 = about $16.33, so you might choose $16.00 and accept a food cost of about 30.6%.</li></ul></div>
<p>These are round example numbers. The point is to change the price on the till and on the page together, and to think about any deal that sits on top of it. A deal that was fine at $14.00 may need a second look at a new price. <a href="/blog/slow-hour-deal-math">The slow-hour math</a> shows how.</p>"""),
             ("Who looks after the page", """<p>On FIG, staff join by accepting an invite from the owner, with the roles Owner, Manager and Staff. Decide who on the team keeps the page current. It is often a manager who knows the menu well. Put the weekly check in the same place as other recurring jobs, such as ordering or the cash-up.</p>
<p>Owners and managers also need a stronger sign-in for the money steps. <a href="/blog/fig-staff-roles-sign-in-security-owners-managers">Setting up your team and sign-in security</a> has the details.</p>"""),
             ("A five-minute weekly check", """<ol><li>Open your page as a diner would see it.</li><li>Read your opening hours for the coming week, and check them against holidays and events.</li><li>Scan the menu for dishes you no longer have, and for prices that have changed.</li><li>Look at your live deals, and end or change any that no longer suit.</li><li>Read new reviews, and reply to any that need it. <a href="/blog/reply-to-reviews-restaurants">Replying to reviews</a> has a short guide.</li></ol>
<p>Keep a note of what you changed and the date. If a diner says the page was wrong, you will know when it was last checked.</p>"""),
             ("What to do when something is wrong", """<p>Mistakes happen. If a diner tells you the page was wrong, thank them, fix it and note the date. If you find the error yourself, fix it at once and look at the other lines for the same kind of slip. It is worth replying to a review that mentions it, in a calm, short way. You do not need to explain at length: say what was wrong and that it is fixed.</p>
<p>A quick tip: the next time you print a new menu, update the page first and print second. The page then never falls behind the paper.</p>"""),
             ("A routine your team will keep", """<p>A routine only works if it is short. Put the five-minute check in your weekly schedule next to a task you already do. Hold it at the same time each week, so nobody has to remember. If the person who does it is away, name a backup. When the check is quick and has an owner, the page stays right without anyone thinking about it.</p>"""),
             ("If you have two locations", """<p>A restaurant can have up to 2 locations on FIG for now. Check each one separately, since hours and menus often differ between them. A short list with a line per location keeps the check quick.</p>"""),
         ],
         faq=[("How often should I check my FIG page?", "Once a week is a good habit, and again before any holiday or closure. Change prices the same day they change on your till."),
              ("What do diners see on my page?", "Your opening hours, your menu with photos and sections, reviews and your live deals."),
              ("Who can update the page?", "Your team, with the roles Owner, Manager and Staff. Staff join by accepting an invite from the owner."),
              ("What if I will be closed on a day a deal is scheduled?", "Change or end the deal, and update your opening hours, so diners do not arrive to a closed door."),
              ("Where do reviews come from?", "Reviews come only from scanned visits, so each one is from a diner who came to your restaurant."),
              ("Does it cost anything to keep my page up to date?", "No. Setting up the page, posting deals, scanning and the dashboard cost nothing for restaurants."),
              ("How many locations can I add?", "Up to 2 locations for now.")]),

]
