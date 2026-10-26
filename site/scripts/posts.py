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
    dict(slug="why-we-built-fig", screen="map", title="Why we built FIG", date="2026-10-02", updated="2026-10-25", topic="News", group="fig-in-markham",
         dek="Markham is full of great independent restaurants, and most of them run on thin margins. FIG is a deals app built around that: free for diners and for restaurants, with no cut of a dine-in bill.",
         desc="Why FIG exists: Markham restaurants run on thin margins, so FIG is free for them and for diners, and takes no cut of a dine-in bill.",
         keywords="FIG app, Markham restaurants, independent restaurants, restaurant deals app, why FIG",
         points=["FIG is a restaurant deals app starting in Markham, Ontario. Deals start January 1, 2027.",
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
<p>FIG opens in Markham first, expanding to Richmond Hill and Vaughan Mills. Deals start January 1, 2027. Until then, restaurants can set up their page, menu and first deals, and diners can join the waitlist at www.figpromo.ca.</p>"""),
             ("What's next", """<p>We're signing Markham restaurants now. If you own one, building your page, your menu and your first deal takes a few minutes, and it is free. To publish them, you finish Stripe's identity and bank checks. <a href="/#owners">See how it works for restaurants</a> or read the <a href="/help">Help center</a>.</p>"""),
         ],
         faq=[("What is FIG?", "FIG is a restaurant deals app. Restaurants post their own deals; diners find them on a map, claim one and show a code at the counter. It's free for diners."),
              ("When does FIG launch?", "FIG opens in Markham first, expanding to Richmond Hill and Vaughan Mills. Deals start January 1, 2027."),
              ("Does FIG take a commission?", "Not on dine-in. Posting deals and scanning diners are free, with no fee per diner. On takeout orders diners pay for in the app, FIG keeps 5% of the food before tax."),
              ("Does FIG show ads?", "No, not for now. FIG has no ads, and paying FIG never moves a restaurant up in search or on the map."),
              ("Does FIG deliver?", "No. Diners eat in, or order takeout with a deal and pick it up."),
              ("Do I need the app to use FIG?", "No. FIG runs in your web browser at www.figpromo.ca/app. Restaurants can set up there today; diners can join the waitlist on the site, and FIG opens to diners on January 1, 2027. The App Store and Google Play apps are coming soon.")]),

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
    dict(slug="restaurant-deals-markham", screen="map", title="How to find the best restaurant deals in Markham", date="2026-10-04", updated="2026-10-24", topic="For diners", group="fig-in-markham",
         dek="A practical guide to eating out for less in Markham, Ontario: when restaurants post deals, where to look across the city, and how to use FIG to find and use them.",
         desc="How to eat out for less in Markham, Ontario: when restaurants post deals, where to look, and how to find and use them on FIG.",
         keywords="restaurant deals Markham, Markham food deals, cheap eats Markham, Markham restaurants, Unionville restaurants, Pacific Mall food",
         points=["The best deals show up when restaurants are quiet: weekday afternoons, early dinners and late evenings.",
                 "Markham's food is spread across plazas and main streets: Highway 7, Steeles and Kennedy, Main Street Unionville, Markham Village and more.",
                 "FIG shows live deals on a map, nearest first, filtered by craving, budget and diet. Deals start January 1, 2027.",
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
         faq=[("What's the best app for restaurant deals in Markham?", "FIG is built for Markham restaurant deals: live deals on a map, set by the restaurants themselves, free for diners, with no ads for now. Deals start January 1, 2027."),
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
    dict(slug="student-food-deals-markham", screen="claim", title="Student food deals in Markham: eating out on a budget", date="2026-10-04", updated="2026-10-24", topic="For diners", group="fig-in-markham",
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
             ("Free is the point", """<p>FIG is free for every diner. There's nothing to subscribe to, no points to collect and no ads for now. Restaurants use FIG for free, and nothing is charged per diner. Deals start in Markham on January 1, 2027.</p>"""),
             ('A week of eating out on $40', '<div class="callout math"><b>An example week (your prices will vary)</b><table><thead><tr><th>Day</th><th>Plan</th><th>Cost with 13% HST</th></tr></thead><tbody>\n<tr><td>Monday</td><td>A $3.50 drink after school (taxed at 5% under $4)</td><td>$3.68</td></tr>\n<tr><td>Tuesday</td><td>A $14 bowl with a $3-off deal</td><td>$12.43</td></tr>\n<tr><td>Thursday</td><td>2-for-1 with a friend: you each pay half of one $15 dish</td><td>$8.48</td></tr>\n<tr><td>Saturday</td><td>A $12 lunch with 15% off</td><td>$11.53</td></tr>\n<tr><td colspan="2"><strong>Total</strong></td><td><strong>$36.12</strong></td></tr>\n</tbody></table><p>Four meals out for under $40, by choosing the deal first. Without the deals, the same food would be about $50.</p></div>'),
             ('Diets and allergies', "<p>Set your diet in FIG (halal, vegetarian, vegan, gluten-free and more) and the places that don't fit drop out of your results. For allergies, filters are a starting point, not a guarantee: call the restaurant before you go, or tell staff when you order. Kitchens share equipment, and only they know exactly what's in a dish.</p>"),
             ('Staying safe and private', '<ul><li>Restaurants see your first name and last initial, never your phone number or email.</li><li>Your claimed deal only works on your phone, so nobody can use it for you.</li></ul>'),
         ],
         faq=[("Is FIG free for students?", "Yes. FIG is free for every diner, with no subscription and no ads for now."),
              ("Do I need a credit card?", "Not to claim a deal. You claim it in the app and pay the restaurant at the counter. Takeout paid in the app needs a card."),
              ("When are student food deals most common?", "In restaurants' quiet hours: after school, roughly 3 to 6 pm, and late evenings for desserts and drinks."),
              ("Can my friends use my code?", "No. Each code belongs to the person who claimed it and works once. Everyone claims their own deal."),
              ("Is food under $4 really taxed less?", "In Ontario, yes: qualifying prepared food and drinks sold for $4 or less in total get the 8% provincial part of the HST rebated at the till, so only the 5% GST applies."),
              ("When can I start using FIG deals?", "FIG opens to diners in Markham on January 1, 2027, and deals start then. Until then, diners can join the waitlist at www.figpromo.ca.")]),

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
         keywords="takeout deals Markham, pickup deals, no delivery fees, takeout pickup Markham, order ahead Markham",
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

    dict(slug="how-restaurant-deals-work", screen="claim", title="How restaurant deals work on FIG, from claim to counter", date="2026-10-14", updated="2026-10-24", topic="For diners", group="eat-out-for-less",
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
<p>Every deal shows what it is, when it runs and whether it's dine-in only or also takeout. Some deals are on the whole order; others are on specific dishes, which you'll see on the menu. Deals in Markham start January 1, 2027.</p>"""),
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

    dict(slug="compare-restaurant-deals-worth-it", screen="claim", title="Is it a good deal? How to compare restaurant deals", date="2026-10-17", publish_at="2026-10-17T12:00:00-04:00", topic="For diners", group="eat-out-for-less",
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
             ("Step 1: start with the food, not the deal", """<p>The biggest mistake with any deal is ordering something you did not want because it was discounted. A $6 saving on a $20 dish you would never choose is a $14 loss. Decide what you feel like eating, then look for the deal that fits it. On FIG you can set what you crave, your budget and your diet once, and Home and the map show live deals that fit, nearest first. Deals start in Markham on January 1, 2027.</p>"""),
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

    dict(slug="eating-out-dietary-needs-allergies-markham", screen="claim", title="Eating out with dietary needs or allergies: filters, calling ahead and what to ask", date="2026-10-19", updated="2026-10-24", publish_at="2026-10-19T12:00:00-04:00", topic="For diners", group="fig-in-markham",
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
             ("Step 1: set your diet once", """<p>When you set up FIG, you choose what you crave, your budget and your diet: halal, vegetarian, vegan, gluten-free and more. After that, Home and the map show live deals from places that fit, nearest first, and the others drop out. FIG opens to diners in Markham on January 1, 2027, and deals start then. Until then, diners can join the waitlist at www.figpromo.ca.</p>
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

    dict(slug="deal-wont-scan-troubleshooting-diners", screen="qr", title="Deal not working at the counter? What to check and what to say", date="2026-10-20", updated="2026-10-24", publish_at="2026-10-20T12:00:00-04:00", topic="For diners", group="eat-out-for-less",
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
<p>This guide goes through what to check before you leave, what to try at the till, and how to ask in a way that gets a quick, kind answer. FIG opens to diners in Markham on January 1, 2027. Until then, diners can join the waitlist at www.figpromo.ca.</p>"""),
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

    dict(slug="date-night-markham-deals-budget", screen="map", title="Date night in Markham for less: a plan, with the math", date="2026-10-22", updated="2026-10-24", publish_at="2026-10-22T12:00:00-04:00", topic="For diners", group="fig-in-markham",
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
             ("The short answer", """<p>The cheapest good date night is an early dinner on a weeknight, with the deal chosen before the restaurant. Look for a deal that covers a main dish each, check the final price with tax, and keep the drinks modest. In the example below, the same dinner for two comes to $76.84 at full price and $51.98 with a 2-for-1 on the mains. FIG is free for diners and opens to them in Markham on January 1, 2027. Until then, diners can join the waitlist at www.figpromo.ca.</p>
<p>This is a plan, not a ranking of restaurants. We do not name places here, because the live deals change every day. Once FIG opens, it will show you what is on near you.</p>"""),
             ("Step 1: pick the hour", """<p>Restaurants are busiest at weekend dinner. The rest of the week, many have empty tables earlier in the evening, and an empty table earns nothing, which is why owners post deals then.</p>
<table><thead><tr><th>When</th><th>Why it suits a date</th></tr></thead><tbody>
<tr><td>Monday to Thursday, early dinner</td><td>Before the evening rush. Quieter room, easier conversation, more deals</td></tr>
<tr><td>Weekday late afternoon</td><td>If your schedule allows it, an early meal followed by a walk</td></tr>
<tr><td>Late evening</td><td>After the rush, for dessert and a drink, if the kitchen is still open</td></tr>
<tr><td>Weekend dinner</td><td>The busiest time. Book ahead, and expect fewer deals</td></tr>
</tbody></table>
<p>Every restaurant is different, so treat this as a pattern, not a rule. Each deal on FIG shows its own days and hours. <a href="/blog/restaurant-deals-markham">When Markham restaurants post deals</a>.</p>"""),
             ("Step 2: start from what you both want", """<p>When FIG opens, you will set your cravings, budget and diet once. Home and the map then show live deals from places that fit, nearest first. If one of you is halal, vegetarian, vegan or gluten-free, set that before you look, so every option works for both of you. For allergies, filters are only a starting point, so call the restaurant. <a href="/blog/eating-out-dietary-needs-allergies-markham">What to ask when you call</a>.</p>
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
         faq=[("What is the cheapest way to do date night in Markham?", "Go early on a weeknight, pick a deal that covers a main each, keep drinks modest and add something free afterwards, such as a walk. When FIG opens to diners on January 1, 2027, it will show live deals near you on a map."),
              ("Is a 2-for-1 better than 20% off for two people?", "If you both want a main, usually yes. In the example in this post, a 2-for-1 on $22 mains came to $51.98 against $61.47 for 20% off the whole bill. Redo it with your own order."),
              ("Does a restaurant deal lower the tax?", "Yes. In Ontario, HST is worked out after the restaurant's own discount, so a lower price means less tax. This is general information, not tax advice."),
              ("Do we each need our own deal?", "Each person can claim their own if the deal suits both of you. Codes are personal and work once, so one person's code cannot be used by someone else."),
              ("Should I call the restaurant first?", "A short call helps. Ask if there is a table, whether the deal works for two and whether it covers the dishes you want."),
              ("When do deals start in Markham?", "FIG opens to diners in Markham on January 1, 2027, and deals start then. Until then, diners can join the waitlist at www.figpromo.ca."),
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

    dict(slug="family-dinner-out-markham-deals-budget", screen="claim", title="Family dinner out in Markham for less: a plan for four, with the math", date="2026-10-24", publish_at="2026-10-24T12:00:00-04:00", topic="For diners", group="fig-in-markham",
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
             ("The short answer", """<p>The cheapest good family dinner is an early weeknight meal, with the deal chosen before the restaurant. Look for a deal that covers the adult mains, work out the final price for the whole table including tax, and keep the drinks simple. In the example below, the same dinner for four comes to $67.80 at full price and $49.72 with a 2-for-1 on the two adult mains. FIG is free for diners and opens to them in Markham on January 1, 2027. Until then, diners can join the waitlist at www.figpromo.ca.</p>
<p>This is a plan, not a ranking of restaurants. We do not name places here, because live deals change every day. Once FIG opens, it will show what is on near you.</p>"""),
             ("Step 1: pick an early table", """<p>Restaurants are busiest at weekend dinner. The rest of the week, many have empty tables in the early evening, and an empty table earns nothing, which is why owners post deals then. For a family it helps twice: more deals, and a quieter room when children are hungry and tired.</p>
<table><thead><tr><th>When</th><th>Why it suits a family</th></tr></thead><tbody>
<tr><td>Monday to Thursday, early dinner</td><td>Before the evening rush. Quieter room, faster kitchen, more deals</td></tr>
<tr><td>Weekday late afternoon</td><td>An early meal on a day off school or work, with the evening left free</td></tr>
<tr><td>Weekend lunch</td><td>Busier than a weekday, but easier on small children than a late dinner</td></tr>
<tr><td>Weekend dinner</td><td>The busiest time. Call ahead, and expect fewer deals</td></tr>
</tbody></table>
<p>Every restaurant is different, so treat this as a pattern, not a rule. Each deal on FIG shows its own days and hours. <a href="/blog/restaurant-deals-markham">When Markham restaurants post deals</a>.</p>"""),
             ("Step 2: start from what everyone will eat", """<p>When FIG opens, you will set your cravings, budget and diet once. Home and the map then show live deals from places that fit, nearest first. If one of you is halal, vegetarian, vegan or gluten-free, set that before you look. Then ask the picky eater to choose between two or three options, instead of an open question. Sharing one concrete restaurant to the family chat works better than "where should we eat?". <a href="/blog/group-dining-deals">More on deciding as a group</a>.</p>
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
         faq=[("What is the cheapest way to eat out as a family in Markham?", "Go early on a weeknight, pick a deal that covers the adult mains, work out the final price with tax and keep drinks and extras modest. When FIG opens to diners on January 1, 2027, it will show live deals near you on a map, and it is free for diners."),
              ("Is a 2-for-1 better than 20% off for a family?", "It depends on the order. In the example in this post, a 2-for-1 on two $16 adult mains came to $49.72 against $54.24 for 20% off the whole bill. Redo the sum with your own order."),
              ("Do children need their own deal?", "A claim is used once and the code only works on the phone of the person who claimed it. Call the restaurant to ask how a deal applies to a table with children."),
              ("Does a restaurant deal lower the tax?", "Yes. In Ontario, HST is worked out after the restaurant's own discount, so a lower price means less tax. This is general information, not tax advice."),
              ("Can I order takeout instead?", "If the restaurant allows takeout with that deal, yes. You order from the menu in the app, pay there and pick it up, with no delivery or service fee from FIG."),
              ("What if someone in the family has an allergy?", "Use FIG's diet filters to shortlist places, then call the restaurant and tell the server again when you order. Filters are a starting point, not a guarantee."),
              ("When do deals start in Markham?", "FIG opens to diners in Markham on January 1, 2027, and deals start then. Until then, diners can join the waitlist at www.figpromo.ca.")]),

    dict(slug="takeout-or-dine-in-with-a-deal-which-costs-less", screen="qr", title="Takeout or dine-in with a deal: which costs you less?", date="2026-10-26", publish_at="2026-10-26T12:00:00-04:00", topic="For diners", group="takeout-and-money",
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
<p>FIG is free for diners and opens to them in Markham on January 1, 2027. Until then, diners can join the waitlist at www.figpromo.ca.</p>"""),
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
              ("When do deals start in Markham?", "FIG opens to diners in Markham on January 1, 2027, and deals start then. Until then, diners can join the waitlist at www.figpromo.ca.")]),

    dict(slug="reply-to-reviews-restaurants", screen="map", title="Replying to reviews: a short guide for restaurant owners", date="2026-10-27", publish_at="2026-10-27T12:00:00-04:00", topic="For restaurants", group="fill-quiet-hours",
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
<p>FIG opens to diners in Markham on January 1, 2027, and reviews come from scanned visits, so yours start after that. Restaurants set up first: you can add your page and menu before then.</p>"""),
         ],
         faq=[("Can I reply to reviews on FIG?", "Yes. Restaurants can reply to reviews in public."),
              ("Can I delete a bad review?", "No. Paying FIG never hides, changes or reorders a review. Reviews come only from diners whose visit was scanned."),
              ("Who can leave a review?", "Only diners whose visit was scanned, one review per visit. Reviews show the diner's first name and last initial."),
              ("Can I reply to a rating that has no words?", "Yes. Restaurants can reply to reviews in public. For a rating with no words, keep it to a line or two and do not guess what went wrong."),
              ("How should I answer a bad review?", "Thank them, be specific, say what you will change and invite them back once. Keep it calm and short, and write for the next reader."),
              ("How much does one low rating change my average?", "Less than it feels like. In the example in this post, one 1-star among ten 5-star reviews gives 4.64, and among thirty gives 4.87."),
              ("Should I offer a discount in a reply?", "Usually not. Let the deal speak for itself, and focus on what you will fix.")]),

]
