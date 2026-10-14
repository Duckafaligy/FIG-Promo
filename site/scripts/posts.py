# The blog's words (28, content lead, 2026-10-14). pages.py builds /blog from POSTS (via content.py); e9 owns the layout.
# Every fact about FIG here is true of the app today (src/content/help.ts, Settings → Get paid, the business terms).
# Every outside fact has its source URL in a comment next to it. No invented numbers, customers, quotes or restaurants:
# worked examples say they're examples, with round numbers anyone can redo with their own.
# Fields: slug, screen (the share image), title, date (first published), updated, topic, dek, desc (optional), keywords,
# points (the "Key takeaways" box), sections [(h2, html)], faq [(q, a)] (also the FAQPage data), publish_at (queued posts:
# ISO with its offset; pages.py leaves a post out until then). Inside sections: plain <table>, and
# <div class="callout tip|example|math"><b>Title</b>…</div>.

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

POSTS = [
    dict(slug="why-we-built-fig", screen="map", title="Why we built FIG", date="2026-10-02", updated=UPDATED, topic="News",
         dek="Markham is full of great independent restaurants, and most of them run on thin margins. FIG is a deals app built around that: free for diners, free for restaurants to post deals, and no cut of a dine-in bill.",
         desc="Why FIG exists: a restaurant deals app for Markham that's free for diners, free for restaurants to post deals and takes no cut of a dine-in bill.",
         keywords="FIG app, Markham restaurants, independent restaurants, restaurant deals app, why FIG",
         points=["FIG is a restaurant deals app starting in Markham, Ontario. Deals start January 1, 2027.",
                 "Restaurants post their own deals, for the hours they choose, with their own daily cap. Posting deals and scanning diners is free.",
                 "Diners find deals on a map, claim one in a tap and show a code at the counter. It's free for diners, with no ads.",
                 "FIG earns from an optional $50-a-year Premium plan and 5% of the food on takeout orders paid in the app. Never from a dine-in bill.",
                 "Markham first, expanding to Richmond Hill and Vaughan Mills."],
         sections=[
             ("The short answer", """<p>We built FIG because the restaurants that make a city worth eating in are mostly small and independent, and the tools that promise them customers usually charge a share of every order. FIG turns that around: a restaurant posts a deal for the hours it wants to fill, nearby diners find it on a map, and the diner pays the restaurant at the counter. FIG takes nothing from that bill.</p>
<p>This post explains the thinking behind that model, what FIG does and doesn't do, and how it pays for itself without ads or commissions on dine-in.</p>"""),
             # StatCan 2023: operating profit margin 3.6%, lowest since 2003 (see sources at the top)
             ("Restaurants run on thin margins", """<p>Running a restaurant is a hard way to make money. Statistics Canada reported that in 2023 the operating profit margin for food services and drinking places in Canada fell to 3.6%, the lowest since 2003. Food and drink bought for resale was the largest expense, at 35.7% of operating costs, with wages close behind.</p>
<p>On a 3.6% margin, a $40 dinner leaves about $1.44 of profit. Anything that takes a percentage of the bill comes straight out of that, and usually more than all of it.</p>
<div class="callout math"><b>What a commission does to a thin margin</b><ul><li>A $40 order at a 3.6% margin: about $1.44 of profit.</li><li>The same order on a 25% commission plan: $10.00 to the platform.</li><li>The commission is about seven times the profit the order would have made on its own.</li></ul><p>Every restaurant's numbers are different, but the shape is the same: a percentage of the bill is paid before the restaurant has made a cent.</p></div>"""),
             # Uber Eats Canada 20/25/30% delivery, DoorDash Canada 20/25/29% (sources at the top)
             ("What delivery apps charge, and why that's a different job", """<p>Delivery platforms publish their Canadian rates. Uber Eats lists marketplace plans at 20%, 25% and 30% of each delivery order, and 10% on pickup orders. DoorDash lists 20%, 25% and 29% on delivery, and 10% or 8% on pickup, depending on the plan. Those rates pay for real work: drivers, the app, the marketplace and the customers it brings.</p>
<p>FIG isn't trying to replace delivery. It does a narrower job: getting people <em>into</em> a restaurant, or to the counter for a pickup, during the hours the owner chooses. For that job, a percentage of every bill isn't needed, so FIG doesn't charge one. <a href="/blog/delivery-app-commissions-vs-fig">Delivery app commissions vs FIG, with the numbers</a>.</p>"""),
             ("So we flipped the model", """<p>On FIG, a deal is a decision the owner made. The restaurant picks:</p>
<ul><li><strong>What</strong> the deal is: a percentage off, a dollar amount off, 2-for-1, or something free with an order, on the whole bill or on specific dishes from its menu.</li><li><strong>When</strong> it runs: which days and hours, every week, once, or until a date. Or a <a href="/blog/flash-deals-explained">flash deal</a> right now, for a quiet hour.</li><li><strong>How many</strong>: a daily cap, so a deal never gives away more than planned. It stops on its own when the cap is reached.</li><li><strong>Where</strong>: dine-in only, or also as takeout.</li></ul>
<p>A diner finds the deal on Home or on the map, taps Claim, and the deal waits in their Voucher tab. At the restaurant, staff scan the diner's code with the FIG business app (on any phone, tablet or computer), or the diner scans the restaurant's own counter code. The deal comes off the bill, and the diner pays the restaurant the way they always do.</p>"""),
             ("What FIG is for diners", """<ul><li><strong>Free.</strong> No subscription, no fees, no ads.</li><li><strong>Deals you can actually use.</strong> Live deals near you, nearest first, filtered by what you crave, your budget and your diet.</li><li><strong>No pressure.</strong> A claim doesn't time out. It works for as long as the deal runs, and it only ends when the restaurant ends the deal, or a flash or dated deal is over.</li><li><strong>Private.</strong> When you message a restaurant in FIG, it sees your first name and last initial, never your phone number or email.</li><li><strong>Honest reviews.</strong> Only diners whose visit was scanned can review a restaurant, so every review comes from a real meal. Deals get likes; restaurants get stars.</li></ul>"""),
             ("How FIG pays for itself", """<p>Two ways, and both are optional for restaurants:</p>
<ol><li><strong>FIG Premium</strong>, $50 a year for a restaurant's whole account: unlimited locations (free accounts have up to 2), a deal announcement every 2 hours to diners in its area and everyone who saved it, area insights, a menu typed up from a photo, and a Premium badge. The badge never moves anyone up in search or on the map.</li><li><strong>Takeout paid in the app</strong>: FIG keeps 5% of the food (before tax), and Stripe's card fee comes off the same payment. The rest, tax included, goes to the restaurant.</li></ol>
<p>That's it. No ads, no fee per diner, no commission on a dine-in bill, and nothing for sale that changes search order or reviews. <a href="/blog/how-fig-makes-money">How FIG makes money, in full</a>.</p>"""),
             # Main Street Unionville and Markham Village: https://en.wikipedia.org/wiki/Main_Street_Unionville ,
             #   https://en.wikipedia.org/wiki/Markham_Village ; Pacific Mall, NE corner of Steeles and Kennedy: https://en.wikipedia.org/wiki/Pacific_Mall
             ("Why Markham first", """<p>Because it's home, and because it has exactly the mix FIG is built for: hundreds of independent restaurants spread across plazas and main streets, from Pacific Mall at Steeles and Kennedy to Main Street Unionville and the old Main Street of Markham Village, and a lot of people who love finding somewhere new to eat.</p>
<p>FIG opens in Markham first, expanding to Richmond Hill and Vaughan Mills. Deals start January 1, 2027. Until then, restaurants can set up their page, menu and first deals, and diners can explore the map.</p>"""),
             ("What's next", """<p>We're signing Markham restaurants now. If you own one, setting up is free and takes a few minutes: your page, your menu, your first deal. <a href="/#owners">See how it works for restaurants</a> or read the <a href="/help">Help center</a>.</p>"""),
         ],
         faq=[("What is FIG?", "FIG is a restaurant deals app. Restaurants post their own deals; diners find them on a map, claim one and show a code at the counter. It's free for diners."),
              ("When does FIG launch?", "FIG opens in Markham first, expanding to Richmond Hill and Vaughan Mills. Deals start January 1, 2027."),
              ("Does FIG take a commission?", "Not on dine-in. Posting deals and scanning diners is free, with no fee per diner. On takeout orders diners pay for in the app, FIG keeps 5% of the food before tax. FIG Premium is optional at $50 a year."),
              ("Does FIG show ads?", "No. FIG has no ads, and paying FIG never moves a restaurant up in search or on the map."),
              ("Does FIG deliver?", "No. Diners eat in, or order takeout with a deal and pick it up."),
              ("Do I need the app to use FIG?", "You can use FIG on the web at fig-promo.vercel.app/app today. The App Store and Google Play apps are coming soon.")]),

    dict(slug="how-fig-makes-money", screen="tdash", title="FIG is free for restaurants. Here's how we make money", date="2026-10-07", updated=UPDATED, topic="For restaurants",
         dek="Listing, deals, scans and chats are free on FIG, with no commission on dine-in. FIG is paid by the optional FIG Premium ($50 a year) and 5% of the food on takeout orders diners pay for in the app.",
         desc="Free for restaurants: listing, deals, scans and chats, no commission on dine-in. FIG earns from optional Premium and 5% of in-app takeout.",
         keywords="FIG pricing, free restaurant app, no commission restaurant app, restaurant deals app Markham, FIG Premium",
         points=["Free on FIG: your page, unlimited deals, every scan, chats, insights and up to 2 locations. No commission and no fee per diner on dine-in.",
                 "FIG makes money two ways: the optional FIG Premium ($50 a year) and 5% of the food on takeout orders diners pay for in the app.",
                 "On a $30 takeout order, FIG's 5% is $1.50 and Stripe's card fee is about $1.28. You keep about $27.22 of the $30, plus the HST you remit.",
                 "Premium adds unlimited locations, a deal announcement every 2 hours, area insights, your menu typed up from a photo and a badge.",
                 "Paying FIG never changes your search position, your reviews or your deal."],
         sections=[
             ("The short answer", """<p>Everything a restaurant needs to bring diners in is free on FIG: your page, your menu, unlimited everyday and flash deals, scanning diners at the counter, chats and the insights that show what's working. A diner who walks in with your deal pays you directly, and FIG takes nothing from that bill.</p>
<p>FIG earns money in exactly two places: an optional FIG Premium plan at $50 a year, and 5% of the food on takeout orders that diners pay for in the app. This post goes through both, with the arithmetic.</p>"""),
             ("What's free, with no catch", """<table><thead><tr><th>On FIG</th><th>What it costs you</th></tr></thead><tbody>
<tr><td>Your restaurant page, menu and photos</td><td>Free</td></tr>
<tr><td>Everyday deals and flash deals, as many as you like</td><td>Free</td></tr>
<tr><td>Scanning diners at the counter (any phone, tablet or computer)</td><td>Free, no fee per diner</td></tr>
<tr><td>Chats with diners</td><td>Free</td></tr>
<tr><td>Insights: views, claims, diners who came in and came back, per deal, day by day</td><td>Free</td></tr>
<tr><td>Up to 2 locations</td><td>Free</td></tr>
<tr><td>Takeout paid in the app</td><td>5% of the food before tax, plus Stripe's card fee</td></tr>
<tr><td>FIG Premium</td><td>Optional, $50 a year for your whole account</td></tr>
</tbody></table>
<p>No contract, no monthly fee, no setup fee.</p>"""),
             ("1. FIG Premium: $50 a year", """<p>One plan covers every location on your account. It adds:</p>
<ul><li><strong>Unlimited locations.</strong> Free accounts have up to 2.</li><li><strong>Deal announcements.</strong> At most every 2 hours, a short note about your deal to diners in your restaurant's area, and to everyone who saved your restaurant. Diners can turn these off, so they stay welcome.</li><li><strong>Area insights.</strong> When diners near you claim deals, what they crave, what's trending, and the restaurants and deals around you.</li><li><strong>Menu from a photo.</strong> Snap your menu or paste its link and FIG types up every dish and price for you to check.</li><li><strong>A FIG Premium badge</strong> on your page.</li></ul>
<p>What Premium never buys: a higher spot in search or on the map, or any say over reviews. Find it in Settings → FIG Premium. It renews yearly, and you can cancel anytime; it stays on until the end of the year you paid for.</p>
<div class="callout example"><b>Is Premium worth $50?</b><p>Spread over a year, $50 is under $1 a week. If announcements bring in one extra table a month, that's twelve tables a year for $50. If you have one location and don't need announcements yet, stay on the free plan: nothing you need to post deals, scan diners or take takeout is held back.</p></div>"""),
             # Stripe 2.9% + CA$0.30 domestic cards (source at the top); HST 13% Ontario
             ("2. Takeout paid in the app: 5% of the food", """<p>When a diner orders takeout and pays in the app, the payment goes through Stripe. FIG keeps 5% of the food before tax, Stripe's card fee comes off the same payment, and the rest, including the HST, is paid out to you. The HST is yours to remit, as with any sale.</p>
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
             ("Why not charge per diner, like other apps?", """<p>Because the restaurant already gave something up: the deal itself. A 2-for-1 or 20% off is the price of the visit. Charging again for the same diner would push owners to make deals smaller and rarer, which is worse for everyone, diners included. FIG wins when deals are good enough to post, so it doesn't tax them.</p>"""),
             ("What paying FIG never does", """<ul><li>Change your deal or its price.</li><li>Move you up in search or on the map. The Premium badge is a badge, not a ranking.</li><li>Hide, remove or reorder reviews. Only diners whose visit was scanned can review, and you can reply in public.</li><li>Share a diner's phone number or email with you. Chats show their first name and last initial.</li></ul>
<p>The full rules are in the <a href="/business-terms">business terms</a>.</p>"""),
             ("How this compares", """<p>If you're weighing FIG against a delivery app, compare the job, not just the rate. Delivery apps bring the food to the door and charge for it: Uber Eats and DoorDash publish Canadian delivery plans between 20% and 30% per order. FIG brings the diner to your door, and charges nothing for that. For pickup, the big apps charge 8% to 10% of an order (Uber Eats charges 15% if your in-store prices aren't validated), which is close to what FIG's 5% plus the card fee comes to. <a href="/blog/delivery-app-commissions-vs-fig">The full comparison, with worked examples</a>.</p>"""),
             ("Getting started", """<p>Sign up as a business, add your menu and post your first deal. It's free. When you're ready for takeout paid in the app, add your HST number and connect Stripe in Settings → Get paid. Questions? <a href="/help">Restaurant help</a> or <a href="/contact">message us</a>.</p>"""),
         ],
         faq=[("How much does FIG cost a restaurant?", "Nothing for your page, deals, scans, chats, insights and up to 2 locations. FIG Premium is optional at $50 a year. On takeout orders diners pay for in the app, FIG keeps 5% of the food before tax."),
              ("Is there a commission on dine-in?", "No. A diner who uses your deal pays you at the counter, and FIG takes nothing from that bill. There's no fee per diner."),
              ("Who pays Stripe's fee on takeout?", "It comes off the same in-app payment, before the payout: 2.9% + $0.30 on Canadian cards, Stripe's published rate. On a $33.90 payment that's about $1.28."),
              ("Does FIG collect HST for me?", "The diner pays the HST with the order and it's paid out to you with the rest. It's yours to remit. Your HST number goes on every takeout receipt, with your restaurant as the seller."),
              ("Is there a contract?", "No. Premium renews yearly; cancel anytime in Settings and it stays on until the end of the year you paid for."),
              ("Can I pay to rank higher?", "No. Nothing you pay FIG changes where you appear in search or on the map, or what your reviews say."),
              ("What do free accounts miss?", "More than 2 locations, deal announcements, area insights, menu from a photo and the badge. Everything needed to post deals, scan diners and take takeout is free.")]),

    # Places: Main Street Unionville https://en.wikipedia.org/wiki/Main_Street_Unionville ; Markham Village and its Main Street,
    #   two Main Streets over 4 km apart, both crossing Highway 7: https://en.wikipedia.org/wiki/Markham_Village ;
    #   Pacific Mall (NE corner of Steeles and Kennedy, Heritage Town food court and market): https://en.wikipedia.org/wiki/Pacific_Mall ;
    #   York University Markham Campus in Markham Centre, opened Fall 2024: https://presidentsreport2023.yorku.ca/opening-the-doors-to-innovation/ ;
    #   Toogood Pond steps from Main Street Unionville: https://www.blogto.com/travel/2023/03/unionville-ontario/ ;
    #   communities (Unionville, Markham Village, Cornell, Milliken, Cathedraltown): https://en.wikipedia.org/wiki/History_of_Markham,_Ontario
    dict(slug="restaurant-deals-markham", screen="map", title="How to find the best restaurant deals in Markham", date="2026-10-04", updated=UPDATED, topic="For diners",
         dek="A practical guide to eating out for less in Markham, Ontario: when restaurants post deals, where to look across the city, and how to use FIG to find and use them.",
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
             ("4. Claim, go, show your code", """<ol><li>Open a restaurant and tap Claim on the deal you want.</li><li>It waits in your Voucher tab. A claim has no time limit: it works for as long as the deal runs.</li><li>At the restaurant, open Voucher and tap Show QR. Staff scan it, or, if the restaurant uses a counter code, you scan theirs.</li><li>The deal comes off the bill. You pay the restaurant as usual.</li></ol>
<p>The code on your screen keeps changing, so a screenshot can't be reused. <a href="/blog/how-restaurant-deals-work">How deals work, step by step</a>.</p>"""),
             ("5. Read the deal properly", """<p>A good deal is one that fits what you were going to do anyway. Before you claim, check:</p>
<ul><li><strong>Days and hours.</strong> Many deals run only in quiet hours.</li><li><strong>Dine in or takeout.</strong> Some deals are for eating in only; others also work as <a href="/blog/takeout-without-delivery-fees">takeout you pick up</a>.</li><li><strong>Which dishes.</strong> Some deals are on the whole order, some on specific dishes from the menu, which you can see on the restaurant's page.</li><li><strong>The daily cap.</strong> Popular deals can run out for the day.</li></ul>"""),
             ("6. Trust real reviews", """<p>Only diners whose visit was scanned can review a restaurant on FIG, so every review comes from a real meal. Restaurants get stars; deals get likes. Restaurants can reply in public, and paying FIG never hides or changes a review. <a href="/blog/how-to-read-restaurant-reviews">Reading reviews on FIG, in a minute</a>.</p>"""),
             ("7. Bring friends", """<p>Group plans fall apart over "where should we go?". Share a deal straight to your group chat: everyone sees the same place, the same deal and how far it is. <a href="/blog/group-dining-deals">Eating out as a group, with deals</a>.</p>"""),
             ('Five mistakes that cost you the deal', "<ul><li><strong>Showing up outside the hours.</strong> Check the deal's days and times before you go.</li><li><strong>Ordering takeout on a dine-in deal.</strong> Look for Dine in or takeout.</li><li><strong>Waiting until the evening on a popular deal.</strong> Daily caps run out; claim early.</li><li><strong>Showing a screenshot.</strong> Codes keep changing: open your Voucher tab at the counter.</li><li><strong>Forgetting the extras.</strong> The deal covers what it says; drinks and sides are usually full price.</li></ul>"),
         ],
         faq=[("What's the best app for restaurant deals in Markham?", "FIG is built for Markham restaurant deals: live deals on a map, set by the restaurants themselves, free for diners, with no ads. Deals start January 1, 2027."),
              ("When do Markham restaurants post the most deals?", "During their quiet hours: typically weekday afternoons, early weeknight dinners and late evenings. Each deal on FIG shows its own days and hours."),
              ("Do I pay through the app?", "For dine-in, no: you pay the restaurant at the counter as usual. Takeout is paid in the app when you order."),
              ("Does FIG need my location?", "No. FIG shows Markham by default and deals are never locked to where you are. Location just makes 'nearest first' mean nearest to you."),
              ("Do claimed deals expire?", "Not on their own. A claim works for as long as the deal runs. It ends only when the restaurant ends the deal, or a flash or dated deal is over."),
              ("Is FIG only in Markham?", "Markham first, expanding to Richmond Hill and Vaughan Mills.")]),

    dict(slug="delivery-app-commissions-vs-fig", screen="tscanner", title="Delivery app commissions vs FIG: what restaurants keep", date="2026-10-04", updated=UPDATED, topic="For restaurants",
         dek="Delivery apps charge restaurants a percentage of every order. FIG charges nothing per dine-in diner and 5% of the food on in-app takeout. Here are the published Canadian rates and what a restaurant keeps from the same order.",
         keywords="delivery app commission Canada, Uber Eats commission, DoorDash commission, restaurant commission fees Ontario, commission-free restaurant app",
         points=["Uber Eats lists Canadian delivery plans at 20%, 25% and 30% of each order; DoorDash at 20%, 25% and 29%.",
                 "For pickup, Uber Eats lists 10% (15% if in-store prices aren't validated) and DoorDash 8% to 10%.",
                 "On FIG, a dine-in diner costs nothing; the only cost is the deal you chose. In-app takeout costs 5% of the food plus Stripe's card fee: about 9.3% of a $30 order.",
                 "On a $30 delivery order at 25%, a restaurant keeps $22.50 of the food. On a $30 FIG takeout paid in the app, it keeps about $27.22.",
                 "Different jobs: delivery apps bring food to the door; FIG brings diners in and to the counter. Many restaurants will use both."],
         sections=[
             ("The short answer", """<p>Delivery apps charge restaurants a percentage of each order, and in Canada the published delivery rates run from 20% to 30%. FIG charges nothing for a diner who eats in with your deal, and 5% of the food (plus Stripe's card fee) on takeout paid in the app. FIG doesn't deliver, so it isn't a like-for-like replacement: it's a cheaper way to fill the tables and the pickup counter you already have.</p>"""),
             ("The published rates", """<p>Both big platforms publish their Canadian plans. Rates as listed in October 2026; your own agreement may differ.</p>
<table><thead><tr><th>Plan</th><th>Delivery</th><th>Pickup</th></tr></thead><tbody>
<tr><td>Uber Eats Lite</td><td>20%</td><td>10%</td></tr>
<tr><td>Uber Eats Plus</td><td>25%</td><td>10%</td></tr>
<tr><td>Uber Eats Premium</td><td>30%</td><td>10%</td></tr>
<tr><td>Uber Eats, your own drivers</td><td>15%</td><td>10%</td></tr>
<tr><td>DoorDash Basic</td><td>20%</td><td>10%</td></tr>
<tr><td>DoorDash Plus</td><td>25%</td><td>8%</td></tr>
<tr><td>DoorDash Premier</td><td>29%</td><td>8%</td></tr>
<tr><td>FIG, dine-in with a deal</td><td>n/a</td><td>No fee</td></tr>
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
</tbody></table><p>The FIG card fee is Stripe's 2.9% + $0.30 on the $33.90 the diner pays with 13% HST. The platform rows use the published plan rates; card processing and any marketing you buy are set by each platform's own terms.</p></div>
<p>Be honest with yourself about pickup: an 8% to 10% pickup plan and FIG's in-app takeout land in the same range. FIG's real difference is everything around it: dine-in costs nothing per diner, there's no monthly fee or contract, and no plan you pay for changes where you show up.</p>"""),
             ("Worked example: a year of orders", """<div class="callout math"><b>Ten $40 orders a week</b><ul><li>At a 25% delivery commission: $10 an order, $100 a week, about $5,200 a year.</li><li>The same ten diners eating in with a FIG deal: $0 to FIG. Your cost is the deal itself, which you chose and capped.</li><li>As FIG takeout paid in the app: 5% of $40 is $2.00, and Stripe's fee on the $45.20 payment is about $1.61, so about $3.61 an order, or roughly $1,880 a year.</li></ul></div>"""),
             ("The cost you choose: the deal", """<p>A deal isn't free: if you offer 20% off, that 20% is a real cost. The difference is that you set it, for the hours you choose, with a daily cap, on the dishes you pick. A deal that fills a table at 3 pm, when it would otherwise be empty, can be worth it at a lower margin, as long as it covers its food cost and you're not giving it away at 7 pm on a Saturday. <a href="/blog/slow-hour-deal-math">How to run a slow-hour deal that makes money</a>.</p>"""),
             ("Different jobs, used together", """<p>Delivery apps are very good at one thing: getting food to someone's door. That has real costs (drivers, distance, support), and the commission pays for them. FIG does a different job:</p>
<ul><li>bringing people <em>into</em> your restaurant in hours you want to fill;</li><li>letting diners order takeout with your deal and pick it up, with no delivery fee for them;</li><li>keeping the relationship in your hands: you answer their messages, reply to their reviews and decide every deal.</li></ul>
<p>Plenty of restaurants will keep delivery for delivery and use FIG to fill the dining room and the counter.</p>"""),
             ("What you control on FIG", """<ul><li>The deal: what, on which dishes, which days and hours, dine-in only or takeout too.</li><li>A daily cap, so a deal never gives away more than planned.</li><li>Takeout: pause it for a rush, add prep time, or turn it off.</li><li>Whether to pay FIG for anything at all.</li></ul>
<p><a href="/blog/how-fig-makes-money">How FIG makes money</a> · <a href="/business-terms">Business terms</a></p>"""),
             ('Run your own numbers', "<p>Before you change anything, look at last month's statements and answer four questions:</p>\n<ol><li>What share of your sales came through each app, and at what rate?</li><li>How many of those orders were pickup, not delivery? Pickup on a delivery app still pays a commission.</li><li>Which hours are your dining room quiet? That's where FIG deals help most.</li><li>How many of your app customers have ever eaten in? Diners who come in are the ones who become regulars.</li></ol>\n<p>If a lot of your app orders are pickup from people who live nearby, a takeout deal on FIG is worth testing alongside.</p>"),
             ('If you already use delivery apps', '<ul><li><strong>Keep delivery for delivery.</strong> FIG doesn\'t replace a driver network.</li><li><strong>Add FIG for the room and the counter.</strong> Post deals for your quiet hours and let diners order takeout with them.</li><li><strong>Tell your regulars.</strong> A sign at the counter, "We\'re on FIG: deals Monday to Thursday afternoons", points app customers to the cheaper way to reach you.</li><li><strong>Compare after a month.</strong> FIG\'s free insights show views, claims, the diners who came in and who came back.</li></ul>'),
         ],
         faq=[("What commission do delivery apps charge in Canada?", "As published in October 2026: Uber Eats 20%, 25% or 30% on delivery and 10% on pickup; DoorDash 20%, 25% or 29% on delivery and 10% or 8% on pickup, depending on the plan."),
              ("Does FIG charge a commission?", "Not on dine-in: deals and scans are free, with no fee per diner. On takeout paid in the app, FIG keeps 5% of the food before tax, and Stripe's card fee comes off the same payment."),
              ("Is FIG cheaper than a delivery app's pickup plan?", "Close. On a $30 order, FIG's in-app takeout costs about $2.78 including the card fee; an 8% to 10% pickup plan costs $2.40 to $3.00. FIG's difference is that dine-in diners cost nothing."),
              ("Does FIG do delivery?", "No. Diners eat in, or order takeout and pick it up."),
              ("Can I use FIG and a delivery app together?", "Yes. Many restaurants will keep delivery for delivery and use FIG to fill quiet hours and the pickup counter."),
              ("Does paying FIG improve my ranking?", "No. FIG Premium never moves a restaurant up in search or on the map.")]),

    # Food cost 28-32% (Resy/US Foods) and StatCan 3.6% margin: sources at the top
    dict(slug="fill-slow-hours-restaurant", screen="tdash", title="7 ways to fill slow hours at your restaurant", date="2026-10-04", updated=UPDATED, topic="For restaurants",
         dek="Practical, low-cost ways for independent restaurants to bring in diners on quiet afternoons and weeknights, with the arithmetic to make sure a deal adds money instead of giving it away.",
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
             ("4. Go where people are deciding", """<p>Most people decide where to eat on their phones, often in a group chat, a few minutes before they go. A poster in the window reaches people who are already there. A deal on a map of nearby deals reaches people who are deciding right now. On FIG, live deals show on Home and the map, nearest first, and diners can share a deal straight to a group chat.</p>
<p>With FIG Premium ($50 a year), you can also announce a deal, at most every 2 hours, to diners in your area and to everyone who saved your restaurant.</p>"""),
             ("5. Use flash deals for surprise quiet spells", """<p>Rain, a cancelled reservation, a slow lunch you didn't see coming. A flash deal is a short deal you post on the spot: pick the deal, how long it runs and an optional cap, and it's live near you within seconds, with a real timer. When the timer ends, it's gone. <a href="/blog/flash-deals-explained">How flash deals work</a>.</p>"""),
             ("6. Fill the kitchen, not just the tables", """<p>Some hours the dining room stays quiet but the kitchen has room. A deal diners can order as takeout and pick up fills that capacity without filling seats, and diners pay no delivery fee. On FIG you choose which deals work as takeout, and you can pause takeout or add prep time when the kitchen gets busy. Diners pay for takeout in the app; FIG keeps 5% of the food, plus Stripe's card fee. <a href="/blog/takeout-without-delivery-fees">How takeout with a deal works</a>.</p>"""),
             ("7. Measure, keep, pause", """<p>Give each deal two weeks, then look at three numbers:</p>
<table><thead><tr><th>Number</th><th>What it tells you</th></tr></thead><tbody>
<tr><td>Claims</td><td>Is the deal interesting? Low claims: the deal or its photo isn't pulling.</td></tr>
<tr><td>Scans</td><td>Are people actually coming in? Many claims but few scans: the hours or the distance may be wrong.</td></tr>
<tr><td>Return diners</td><td>Is it building regulars? This is the number that pays off long after the deal.</td></tr>
</tbody></table>
<p>FIG's free insights show views, claims, the diners who came in and who came back, per deal, day by day. Keep the deals that bring new people back. Pause the rest with one tap.</p>"""),
             ("A one-week plan", """<ol><li><strong>Monday:</strong> mark your quiet hours from last month's receipts.</li><li><strong>Tuesday:</strong> pick one dish with a healthy margin and write one specific deal for one quiet window.</li><li><strong>Wednesday:</strong> post it on FIG with a cap of 10 a day. Take a good photo.</li><li><strong>Thursday to Sunday:</strong> make sure every staff member knows the deal and how to scan.</li><li><strong>Two weeks later:</strong> check claims, scans and return diners. Adjust the hours, the dish or the cap.</li></ol>
<p>Setting up on FIG is free. <a href="/blog/set-up-fig-menu-takeout">A 15-minute setup guide for your menu and takeout</a>.</p>"""),
         ],
         faq=[("What's the cheapest way to market a small restaurant?", "Aim a specific, capped deal at your quiet hours and put it where diners are deciding. Posting deals and scanning diners on FIG is free."),
              ("Will a deal hurt my margins?", "Not if it runs only in hours that would otherwise be empty and covers its food cost. Cap it per day so it can't cost more than planned."),
              ("What are the slowest hours for restaurants?", "For many, weekday afternoons (about 2 to 5 pm) and early weeknights. Check your own receipts by hour: every restaurant is different."),
              ("Should I offer a percentage off or 2-for-1?", "2-for-1 pulls hardest but costs the most per plate; a percentage off is gentler on margin. Run the numbers on your food cost first."),
              ("How do I know if a deal is working?", "Watch claims, scans and return diners for two weeks. FIG's free insights show all three per deal."),
              ("Can I stop a deal anytime?", "Yes. Pause or end it with one tap, and the daily cap stops it automatically each day.")]),

    # York University Markham Campus (Markham Centre, opened Fall 2024): https://presidentsreport2023.yorku.ca/opening-the-doors-to-innovation/
    # Pacific Mall Heritage Town food court: https://en.wikipedia.org/wiki/Pacific_Mall
    # Ontario $4 prepared food point-of-sale rebate (GI-064): source at the top
    dict(slug="student-food-deals-markham", screen="claim", title="Student food deals in Markham: eating out on a budget", date="2026-10-04", updated=UPDATED, topic="For diners",
         dek="How high school and university students in Markham can eat out for less: when deals show up, how to set a real budget, how to decide as a group, and how FIG keeps it free.",
         keywords="student food deals Markham, cheap eats for students, after school food Markham, budget restaurants Markham, bubble tea deals Markham, York University Markham food",
         points=["After school (about 3 to 6 pm) is when many restaurants are quiet, so it's when deals show up.",
                 "Set a budget filter in FIG once and only see deals you can afford.",
                 "Snacks and drinks of $4 or less have a smaller tax in Ontario: only the 5% GST part, not the full 13%.",
                 "Share a deal to the group chat so everyone agrees faster, and split the bill fairly.",
                 "FIG is free: no subscription, no ads, no card needed to claim a deal."],
         sections=[
             ("The short answer", """<p>Eat when restaurants are quiet, decide with a budget instead of a craving, and let the deals come to you. In Markham that usually means after school and on weekday evenings, when many places post deals to fill empty tables. FIG puts every live deal near you on one map, filtered to your budget, and it's free.</p>"""),
             ("After school is deal time", """<p>Between lunch and dinner, many restaurants and bubble tea shops are at their quietest. That's exactly when owners post deals, and exactly when you get out of class. Late evenings are the other sweet spot for desserts and drinks.</p>
<p>For university students, Markham Centre on Highway 7 now has York University's Markham Campus, which opened in 2024, and Highway 7 is lined with plazas full of places to eat. High school students are rarely more than a short walk or bus ride from a plaza with a few options.</p>"""),
             ("Set a real budget", """<p>When you sign up, tell FIG what you crave and your budget. Home and the map then show deals that fit, nearest first, so you're not scrolling past $40 dinners. A few habits that stretch a budget further:</p>
<ul><li><strong>Pick the deal, then the place.</strong> Start from what's live and in budget, not from one restaurant you've already decided on.</li><li><strong>Share dishes.</strong> Two people sharing a 2-for-1 often eat more for less than two separate meals.</li><li><strong>Watch the add-ons.</strong> Drinks and extras are where a cheap meal stops being cheap.</li><li><strong>Look at takeout.</strong> Picking food up yourself means no delivery or service fees.</li></ul>
<div class="callout math"><b>A small tax tip for snacks</b><p>In Ontario, prepared food and drinks sold for $4 or less in total (before tax) get the 8% provincial part of the HST rebated at the till, so you pay only the 5% GST part. On a $3.80 drink, that's about $0.19 of tax instead of $0.49. It applies to the total of what you buy at one time, so it's for a single snack or drink, not a group order.</p></div>"""),
             ("Decide with your friends", """<p>Group plans fall apart over "where should we go?". Share a deal from FIG straight to your group chat: everyone sees the same place, the same deal and how far it is. If the plan is six people at 5 pm, message the restaurant from FIG first to check there's room. Your phone number stays private. <a href="/blog/group-dining-deals">How to eat out as a group, with deals</a>.</p>"""),
             ("Know your spots", """<p>A few areas worth knowing:</p>
<ul><li><strong>Pacific Mall</strong> at Steeles and Kennedy, with its own food court and market, Heritage Town.</li><li><strong>Highway 7</strong> and Markham Centre, near the York campus.</li><li><strong>Main Street Unionville</strong>, for a sit-down treat.</li><li><strong>Your local plaza.</strong> Many of the best cheap eats in Markham are in plazas you walk past every day.</li></ul>
<p>More in our <a href="/blog/restaurant-deals-markham">guide to restaurant deals in Markham</a>.</p>"""),
             ("How it works at the counter", """<ol><li>Claim the deal in FIG. It waits in your Voucher tab for as long as the deal runs.</li><li>At the restaurant, tap Show QR. Staff scan it, or you scan the restaurant's counter code.</li><li>The deal comes off your bill. You pay the restaurant like normal.</li></ol>
<p>You don't need a credit card to claim a deal. The code keeps changing, so a screenshot from a friend won't work: everyone claims their own.</p>"""),
             ("Free is the point", """<p>FIG is free for every diner. There's nothing to subscribe to, no points to collect and no ads. Restaurants pay for FIG only if they choose Premium or take takeout payments in the app, never per diner. Deals start in Markham on January 1, 2027.</p>"""),
             ('A week of eating out on $40', '<div class="callout math"><b>An example week (your prices will vary)</b><table><thead><tr><th>Day</th><th>Plan</th><th>Cost with 13% HST</th></tr></thead><tbody>\n<tr><td>Monday</td><td>A $3.50 drink after school (taxed at 5% under $4)</td><td>$3.68</td></tr>\n<tr><td>Tuesday</td><td>A $14 bowl with a $3-off deal</td><td>$12.43</td></tr>\n<tr><td>Thursday</td><td>2-for-1 with a friend: you each pay half of one $15 dish</td><td>$8.48</td></tr>\n<tr><td>Saturday</td><td>A $12 lunch with 15% off</td><td>$11.53</td></tr>\n<tr><td colspan="2"><strong>Total</strong></td><td><strong>$36.12</strong></td></tr>\n</tbody></table><p>Four meals out for under $40, by choosing the deal first. Without the deals, the same food would be about $50.</p></div>'),
             ('Diets and allergies', "<p>Set your diet in FIG (halal, vegetarian, vegan, gluten-free and more) and the places that don't fit drop out of your results. For allergies, filters are a starting point, not a guarantee: message the restaurant from FIG before you go, or tell staff when you order. Kitchens share equipment, and only they know exactly what's in a dish.</p>"),
             ('Staying safe and private', '<ul><li>Restaurants see your first name and last initial, never your phone number or email.</li><li>Any phone number typed into a chat is hidden.</li><li>You can block or report a chat from the ⋯ menu.</li><li>Your claimed deal only works on your phone, so nobody can use it for you.</li></ul>'),
         ],
         faq=[("Is FIG free for students?", "Yes. FIG is free for every diner, with no subscription and no ads."),
              ("Do I need a credit card?", "Not to claim a deal. You claim it in the app and pay the restaurant at the counter. Takeout paid in the app needs a card."),
              ("When are student food deals most common?", "In restaurants' quiet hours: after school, roughly 3 to 6 pm, and late evenings for desserts and drinks."),
              ("Can my friends use my code?", "No. Each code keeps changing and belongs to the person who claimed it. Everyone claims their own deal."),
              ("Is food under $4 really taxed less?", "In Ontario, yes: qualifying prepared food and drinks sold for $4 or less in total get the 8% provincial part of the HST rebated at the till, so only the 5% GST applies."),
              ("When can I start using FIG deals?", "Deals start in Markham on January 1, 2027. You can explore the map and restaurants now.")]),

    dict(slug="flash-deals-explained", screen="qr", title="What are flash deals, and how do they work on FIG?", date="2026-10-04", updated=UPDATED, topic="For diners",
         dek="Flash deals are short, real-time restaurant deals posted during unexpected quiet spells. Here's how they work for diners and restaurants, how to catch them, and what happens to a claim when the timer ends.",
         keywords="flash deals restaurants, last minute restaurant deals, happy hour Markham, real time food deals, flash deal app",
         points=["A flash deal is a short deal a restaurant posts right now, usually for an hour or two, because it has a quiet spell.",
                 "The timer is set by the restaurant and it's real: when it ends, the deal is gone.",
                 "Live flash deals show at the top of Search under Live now near you, and stand out on the map.",
                 "A claimed flash deal works until the timer ends, then it expires. Expired claims never count against you.",
                 "Restaurants post one in seconds, free, with an optional cap."],
         sections=[
             ("The short answer", """<p>A flash deal is a short restaurant deal posted on the spot, because the restaurant has empty tables right now. It runs for a set time, usually an hour or two, with a real countdown. Claim it while it's live, head over, and show your code before the timer ends.</p>"""),
             ("Everyday deals vs flash deals", """<table><thead><tr><th></th><th>Everyday deal</th><th>Flash deal</th></tr></thead><tbody>
<tr><td>When it's posted</td><td>In advance</td><td>Right now</td></tr>
<tr><td>When it runs</td><td>Chosen days and hours, every week, once, or until a date</td><td>From now until the timer ends</td></tr>
<tr><td>Why</td><td>Hours that are usually quiet</td><td>A surprise quiet spell: rain, a cancellation, a slow lunch</td></tr>
<tr><td>Your claim</td><td>Works whenever the deal runs</td><td>Works until the timer ends</td></tr>
<tr><td>Where you see it</td><td>Home, the map, the restaurant's page</td><td>Top of Search, the map, the restaurant's page</td></tr>
</tbody></table>"""),
             ("How to catch one", """<p>Open Search: flash deals that are live near you sit at the top under Live now near you, with the time left. They also stand out on the map. Because they're short, the best way to catch them is to check FIG when you're already thinking about food, the same moment you'd open a group chat to ask "where should we eat?".</p>
<p>If a restaurant you saved has FIG Premium, it can send a short announcement about a deal, at most every 2 hours. You can turn those off anytime in Deal alerts.</p>"""),
             ("Claim it, then go", """<ol><li>Tap the flash deal and Claim it. It's in your Voucher tab with the time left.</li><li>Head over. A claim doesn't need you to be anywhere in particular: you can claim from home.</li><li>At the counter, tap Show QR and let staff scan it, or scan the restaurant's counter code.</li></ol>
<p>Your code keeps changing on screen, so a screenshot can't be reused. If the timer runs out before you get there, the claim expires. It shows as Expired in your Voucher tab for a day, and it never counts against you.</p>"""),
             ("Are flash deals real?", """<p>Yes, and it's worth saying why. On FIG, the timer is the restaurant's own: the owner chose the deal and how long it runs, because they actually have the space. FIG doesn't invent urgency, and a flash deal isn't a fake countdown that resets tomorrow.</p>"""),
             ("For restaurant owners", """<p>Posting a flash deal takes a few seconds: pick the deal (a percentage off, a dollar amount off, 2-for-1 or something free), the length and an optional cap. It's free, like every scan. Good flash deals are:</p>
<ul><li><strong>Simple.</strong> One dish or one clear discount, readable at a glance.</li><li><strong>Short.</strong> Long enough for someone nearby to get there, short enough to stay special.</li><li><strong>Capped.</strong> So a sudden rush can't overwhelm the kitchen.</li><li><strong>Real.</strong> Post one when you genuinely have room, and diners learn to trust them.</li></ul>
<p>Check the math before you post: in a quiet spell, a deal only has to cover its food cost to add money. <a href="/blog/slow-hour-deal-math">Slow-hour deal math</a> · <a href="/#owners">How FIG works for restaurants</a></p>"""),
             ('The life of a flash deal', '<table><thead><tr><th>When</th><th>What happens</th></tr></thead><tbody>\n<tr><td>2:40 pm</td><td>A restaurant has a quiet afternoon and posts "$4 off any noodle bowl, for 90 minutes, 15 available".</td></tr>\n<tr><td>2:41 pm</td><td>It appears at the top of Search under Live now near you, on the map and on the restaurant\'s page, with the time left.</td></tr>\n<tr><td>2:45 to 4:10 pm</td><td>Diners nearby claim it and head over. Each claim waits in their Voucher tab.</td></tr>\n<tr><td>At the counter</td><td>Staff scan each diner\'s code, or diners scan the restaurant\'s counter code. $4 comes off.</td></tr>\n<tr><td>4:10 pm</td><td>The timer ends. The deal disappears, and any unused claims expire. If all 15 had been used first, it would have ended then.</td></tr>\n</tbody></table>\n<p>An example timeline: every restaurant chooses its own deal, length and cap.</p>'),
             ('Why restaurants have surprise quiet spells', "<p>A dining room can go quiet for reasons nobody planned: a downpour, a cancelled group booking, a slow day after a holiday weekend, a road closure out front. The kitchen is staffed and the food is prepped either way. A flash deal turns that spare capacity into diners, and because it's short and capped, it doesn't train people to wait for discounts.</p>"),
             ('Flash deal etiquette for diners', '<ul><li><strong>Claim it when you mean to go.</strong> Caps are small, and an unused claim may keep someone else out.</li><li><strong>Go promptly.</strong> The deal ends with the timer, wherever you are.</li><li><strong>Check dine-in or takeout</strong> before you set off.</li><li><strong>Like the deal</strong> afterwards if it was good: it tells the restaurant, and other diners, that it worked.</li></ul>'),
             ('Everyday or flash? For owners', '<table><thead><tr><th>Use an everyday deal when</th><th>Use a flash deal when</th></tr></thead><tbody>\n<tr><td>The same hours are quiet every week</td><td>Today is unexpectedly quiet</td></tr>\n<tr><td>You want regulars to know when to come</td><td>You want diners who are nearby right now</td></tr>\n<tr><td>You can plan the dish and the staffing</td><td>You have food and staff ready but empty seats</td></tr>\n</tbody></table>\n<div class="callout math"><b>Is a flash deal worth it?</b><p>A $15 bowl with a food cost of $4.50 still leaves $6.50 with $4 off. In an hour where those seats would sit empty, fifteen of them add up to $97.50 toward the shift\'s wages and rent, before any drinks. Use your own numbers. <a href="/blog/slow-hour-deal-math">The full slow-hour math</a>.</p></div>'),
         ],
         faq=[("How long do flash deals last?", "The restaurant sets the length, usually an hour or two. The timer you see in the app is the real one."),
              ("What happens if my flash deal runs out before I arrive?", "The claim expires when the timer ends. It shows as Expired in your Voucher tab for a day, then leaves the list, and it never counts against you."),
              ("Will FIG message me about flash deals?", "Not on its own. Restaurants with FIG Premium can announce a deal to diners in their area and people who saved them, at most every 2 hours, and you can turn those off in Deal alerts."),
              ("Do I have to be nearby to claim a flash deal?", "No. Deals are never locked to your location. Just make sure you can get there before the timer ends."),
              ("Can a restaurant post a flash deal for takeout?", "A restaurant chooses whether each deal is dine-in only or also takeout."),
              ("Do flash deals cost restaurants anything?", "No. Posting deals and scanning diners on FIG is free.")]),

    dict(slug="takeout-without-delivery-fees", screen="chat", title="Takeout with a deal, pick up, skip the delivery fees", date="2026-10-04", updated=UPDATED, topic="For diners",
         dek="Some FIG deals let you order takeout from a Markham restaurant's menu and pick it up yourself, with no delivery or service fees. Here's how it works, what it costs, and what happens if you're late.",
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
             ("If something changes", """<ul><li><strong>The restaurant needs you.</strong> They'll message you in FIG or mark that they're waiting. You'll see it in Chats and on your order.</li><li><strong>You need to change something.</strong> Message them from the order.</li><li><strong>You're running late.</strong> Tap I'm here when you arrive so it never counts as missed.</li><li><strong>You can't make it.</strong> Two hours after the pickup time, the order closes as Not picked up. Nothing gets switched off, but a missed pickup shows on your takeout record, and restaurants see it.</li></ul>"""),
             ("Private by default", """<p>The restaurant sees your first name and last initial, never your phone number or email. Any phone number typed into a chat is hidden. The FIG team reads a chat only if it's reported.</p>"""),
             ('Your first takeout order, step by step', "<ol><li><strong>Pick the deal.</strong> On Home or the map, look for deals marked Dine in or takeout. Open one and check the days, hours and which dishes it's on.</li><li><strong>Tap Takeout.</strong> The restaurant's menu opens in sections, with the deal already applied to the dishes it covers.</li><li><strong>Build your order.</strong> Add the deal dish and anything else you want. The deal comes off; other dishes are full price.</li><li><strong>Check the pickup time.</strong> If the restaurant has added prep time because it's busy, you'll see it here, before you pay.</li><li><strong>Pay in the app.</strong> Your card is charged for the food after the deal, plus tax. The receipt names the restaurant as the seller.</li><li><strong>Follow the order.</strong> You'll see when the restaurant accepts it and when it's ready. If they need you, they'll message you in FIG.</li><li><strong>Arrive and tap I'm here.</strong> Then show your pickup code at the counter so staff can scan it.</li><li><strong>Check the bag</strong> before you leave, and enjoy it while it's hot.</li></ol>"),
             ('Takeout, delivery or dine-in?', "<table><thead><tr><th></th><th>Takeout on FIG</th><th>Delivery app</th><th>Dine-in with a FIG deal</th></tr></thead><tbody>\n<tr><td>Who brings the food</td><td>You pick it up</td><td>A driver</td><td>Your server</td></tr>\n<tr><td>Delivery or service fee</td><td>None from FIG</td><td>Set by the app</td><td>None from FIG</td></tr>\n<tr><td>How you pay</td><td>In the app</td><td>In the app</td><td>At the counter, as usual</td></tr>\n<tr><td>Deal</td><td>If the deal allows takeout</td><td>The app's own promotions</td><td>Any live deal</td></tr>\n<tr><td>Best when</td><td>You're nearby and want to eat at home</td><td>You can't go out</td><td>You want the full experience</td></tr>\n</tbody></table>"),
             ('Tips for great pickups', '<ul><li><strong>Order in quiet hours.</strong> That\'s when takeout deals run, and when kitchens are fastest.</li><li><strong>Order when you\'re ready to leave.</strong> Food is best right when it\'s made.</li><li><strong>Use the chat for changes.</strong> Allergies, no onions, extra sauce: message from the order rather than calling.</li><li><strong>Ordering for a group?</strong> One person orders and picks up, then everyone settles up. <a href="/blog/group-dining-deals">Splitting the bill fairly</a>.</li></ul>'),
             ('What restaurants see', "<p>Restaurants see your order, the pickup time, your first name and last initial, and whether you've tapped I'm here. They don't see your phone number, email or card details: payments go through Stripe. A record of missed pickups is the one thing that follows you, which is why tapping I'm here when you arrive matters.</p>"),
         ],
         faq=[("Does FIG deliver?", "No. You order takeout and pick the food up yourself."),
              ("Is there a fee for takeout on FIG?", "Not for diners: no delivery fee and no service fee. You pay the menu price, minus the deal, plus tax."),
              ("Do I pay in the app or at the counter?", "For takeout, in the app when you order: the payment goes to the restaurant through Stripe. For dine-in deals, you pay at the counter as usual."),
              ("What if I'm late for my pickup?", "Tap I'm here when you arrive. Two hours after the pickup time, an order that wasn't picked up closes as Not picked up and shows on your takeout record."),
              ("Can I order takeout without a deal?", "Some restaurants take takeout at full price: tap Order takeout on their page."),
              ("Does the restaurant get my phone number?", "No. Restaurants see your first name and last initial, and talk to you through FIG's chat.")]),

    # ---------------------------------------------------------------- new posts, queued for the user's review (one a day at
    # 12:00 Toronto time; EDT is -04:00 until November 1). Each publishes on its own when pages.py runs after publish_at.

    dict(slug="how-restaurant-deals-work", screen="claim", title="How restaurant deals work on FIG, from claim to counter", date="2026-10-16", publish_at="2026-10-16T12:00:00-04:00", topic="For diners",
         dek="Everything that happens between seeing a deal and paying the bill: claiming, the Voucher tab, the code at the counter, takeout, what happens when a deal ends, and rating the visit.",
         keywords="how restaurant deals work, claim restaurant deal, restaurant deal app how to, FIG voucher, QR code restaurant deal",
         points=["Find a deal on Home, the map or a restaurant's page, and tap Claim. It waits in your Voucher tab.",
                 "A claim has no time limit: it works for as long as the deal runs.",
                 "At the counter, tap Show QR and staff scan it, or scan the restaurant's own counter code. The deal comes off your bill.",
                 "The code keeps changing, so screenshots don't work and nobody can reuse your deal.",
                 "After a scanned visit you can rate the restaurant, and like the deal. FIG is free for diners."],
         sections=[
             ("The short answer", """<p>On FIG, a restaurant deal works in four steps: you find a deal, claim it in one tap, show your code at the restaurant, and the deal comes off your bill. You pay the restaurant the way you always do. There's no card to add for dine-in, no points to collect and no fee: FIG is free for diners.</p>"""),
             ("Step 1: Find a deal", """<p>Deals show up in three places:</p>
<ul><li><strong>Home</strong>, nearest first, filtered by what you crave, your budget and your diet.</li><li><strong>The map</strong>, where you choose how far you'll go: 1, 2, 5 or 10 km.</li><li><strong>A restaurant's page</strong>, alongside its menu, hours, photos and reviews.</li></ul>
<p>Every deal shows what it is, when it runs and whether it's dine-in only or also takeout. Some deals are on the whole order; others are on specific dishes, which you'll see on the menu. Deals in Markham start January 1, 2027.</p>"""),
             ("Step 2: Claim it", """<p>Tap Claim on the deal, then Claim deal. It waits in your Voucher tab. A claim doesn't time out: it works for as long as the deal runs. You don't need to be near the restaurant to claim, and you don't need to go right away.</p>
<div class="callout tip"><b>When does a claim end?</b><p>Only when the restaurant ends the deal, or when a flash deal's timer or a dated deal is over. Then it shows as Expired in your Voucher tab for a day and leaves the list. Expired claims never count against you.</p></div>"""),
             ("Step 3: At the restaurant", """<p>Order as usual and, when it's time to pay, open your Voucher tab. There are two ways the deal gets applied, depending on the restaurant:</p>
<table><thead><tr><th>Way</th><th>What you do</th><th>What staff do</th></tr></thead><tbody>
<tr><td>Your QR code</td><td>Tap Show QR</td><td>Scan it with the FIG business app</td></tr>
<tr><td>The counter code</td><td>Tap Scan the counter and point your camera at the restaurant's code</td><td>Nothing: the code on their screen does it</td></tr>
</tbody></table>
<p>If a camera won't cooperate, there's a short code staff can type instead. Either way, the deal comes off the bill and you pay the restaurant directly.</p>
<p>The QR code on your screen keeps changing, and the restaurant's counter code changes every 30 seconds. That's what makes deals safe: a screenshot can't be reused, and nobody can use your claim but you.</p>"""),
             ("Step 4: Rate the visit", """<p>Once your visit is scanned, you can rate the restaurant: tap Rate this visit, or find it later under Past visits in your Voucher tab. Pick the stars and add a few words or a photo if you like. One review per visit, and it shows your first name and last initial.</p>
<p>Deals get likes, restaurants get stars. Only diners whose visit was scanned can review, so every review on FIG comes from a real meal. <a href="/blog/how-to-read-restaurant-reviews">How to read a restaurant's reviews</a>.</p>"""),
             ("Takeout works too", """<p>If a deal is marked Dine in or takeout, tap Takeout instead: the restaurant's menu opens with the deal applied, you add what you want, and you pick it up. Tap I'm here when you arrive and show your pickup code. No delivery or service fees. <a href="/blog/takeout-without-delivery-fees">How takeout works</a>.</p>"""),
             ("Questions before you go", """<p>Not sure if there's room for six, or whether the deal works with the lunch special? Tap Message on the restaurant's page or your claimed deal. The restaurant sees your first name and last initial, never your phone number or email. <a href="/blog/group-dining-deals">Going as a group?</a></p>"""),
             ("What FIG doesn't do", """<ul><li>Charge you anything, or show you ads.</li><li>Lock deals to where you are. Use them wherever you happen to be.</li><li>Rush you. No fake countdowns: a flash deal's timer is the restaurant's real one.</li><li>Share your phone number with restaurants.</li></ul>"""),
         ],
         faq=[("Do I need to pay in the app?", "Not for dine-in. You show your code and pay the restaurant as usual. Takeout is paid in the app when you order."),
              ("How long is a claimed deal good for?", "As long as the deal runs. It ends only when the restaurant ends the deal, or a flash or dated deal is over."),
              ("Can I screenshot my code?", "It won't work. The code keeps changing, so only the live code in your app can be scanned."),
              ("What's the counter code?", "Some restaurants show their own QR code at the counter that changes every 30 seconds. Tap Scan the counter on your claimed deal and point your camera at it."),
              ("Can I use a deal more than once?", "Each claim is one use. The restaurant decides how often a deal can be claimed, and caps how many are used per day."),
              ("Who can review a restaurant?", "Only diners whose visit was scanned, so every review comes from a real visit."),
              ("Is FIG free?", "Yes, for every diner: no subscription, no fees and no ads.")]),

    # StatCan 2023 margin 3.6%; food cost 28-32% (Resy): sources at the top
    dict(slug="slow-hour-deal-math", screen="tdash", title="How to run a slow-hour deal that makes money (with the math)", date="2026-10-17", publish_at="2026-10-17T12:00:00-04:00", topic="For restaurants",
         dek="A slow-hour deal makes money when it fills seats that would otherwise be empty and covers its food cost. Here's the arithmetic: contribution per plate, the worst case, the cap, and how to tell new diners from regulars who'd have come anyway.",
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
<p>FIG's free insights show views, claims, the diners who came in and who came back, per deal, day by day. If most scans are your usual faces, change the dish, the hours or the deal.</p>"""),
             ("A checklist before you post", """<ul><li>Does the diner's price cover the food cost, with room to spare?</li><li>Is it only in hours you're actually quiet?</li><li>Is the cap's worst case a number you're fine with?</li><li>Is it specific: a dish, a time, a price?</li><li>Do all staff know it and how to scan?</li><li>Have you set a date to check claims, scans and return diners?</li></ul>
<p>Posting deals and scanning diners on FIG is free. <a href="/blog/deal-types-percent-dollar-2-for-1">Next: % off, $ off or 2-for-1?</a></p>"""),
         ],
         faq=[("Do restaurant discounts actually make money?", "They can, when they fill otherwise empty seats and the diner's price covers the food cost. At busy hours, the same discount mostly gives money to diners who'd have paid full price."),
              ("What food cost should I assume?", "Use your own. As a reference, the average food cost is often quoted at 28% to 32% of revenue."),
              ("How big should my daily cap be?", "Big enough to matter, small enough that the worst case (cap × discount) is a number you're comfortable with. Start small and raise it."),
              ("Should drinks be part of the deal?", "Often not: a deal on the main dish with drinks at full price lets add-ons do the earning."),
              ("How do I know if new people are coming?", "Watch scans and return visits per deal. FIG's free insights show the diners who came in and who came back."),
              ("Does FIG take a cut of dine-in deals?", "No. Posting deals and scanning diners is free, with no fee per diner.")]),

    # CRA: a store coupon reduces the price before GST/HST (RC4022): source at the top
    dict(slug="deal-types-percent-dollar-2-for-1", screen="tdash", title="% off, $ off or 2-for-1? Pricing a restaurant deal", date="2026-10-18", publish_at="2026-10-18T12:00:00-04:00", topic="For restaurants",
         dek="The four kinds of restaurant deal, side by side: what each costs you, what it feels like to a diner, and when to use it. With worked examples on a $14 dish.",
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
    dict(slug="set-up-fig-menu-takeout", screen="tscanner", title="Set up your FIG menu and takeout in 15 minutes", date="2026-10-19", publish_at="2026-10-19T12:00:00-04:00", topic="For restaurants",
         dek="A step-by-step guide for restaurant owners: your page, your menu, your first deal, and in-app takeout with your HST number and Stripe payouts, explained simply.",
         keywords="FIG restaurant setup, restaurant menu app, set up takeout restaurant, Stripe payouts restaurant, HST number restaurant app",
         points=["Sign up as a business, then follow the Get FIG ready checklist on your dashboard: it ticks itself as you go.",
                 "Build your menu in sections, then dishes and prices. Nothing changes for diners until you tap Publish changes.",
                 "Post one specific, capped deal for a quiet window. Posting deals and scanning diners is free.",
                 "In-app takeout needs your HST number and Stripe payouts, both in Settings → Get paid. Dine-in deals need neither.",
                 "During a rush, pause takeout or add prep time in one tap."],
         sections=[
             ("The short answer", """<p>Setting up on FIG takes about 15 minutes if you have your menu handy: sign up as a business, add your sections, dishes and prices, publish, and post one deal for a quiet window. If you want diners to pay for takeout in the app, add your HST number and connect Stripe for payouts in Settings → Get paid. Everything except in-app takeout is free, and in-app takeout costs 5% of the food plus Stripe's card fee.</p>"""),
             ("Before you start: have these ready", """<ul><li>Your menu (paper, a PDF or a photo) with prices.</li><li>Two or three good photos of your food and room.</li><li>Your opening hours.</li><li>For in-app takeout only: your HST number (it looks like 123456789 RT 0001) and your bank details for Stripe.</li></ul>"""),
             ("Minutes 0 to 3: sign up and follow the checklist", """<p>Sign up as a business with your restaurant's name and address. Your dashboard shows a <strong>Get FIG ready</strong> checklist with one button per step. Each step ticks itself when it's done, from your real data, and you can hide the checklist for good once you're set. Quick tours point out the important buttons the first time you open a screen.</p>"""),
             ("Minutes 3 to 10: your menu", """<ol><li><strong>Sections first.</strong> Starters, Mains, Noodles, Drinks: however your paper menu is organised.</li><li><strong>Dishes and prices.</strong> Type prices the way you like: "15.50", "15,50" and "$15.50" all work.</li><li><strong>Publish.</strong> Your edits are kept while you work, and the button says Publish changes until you tap it. Nothing changes for diners before that, and if you close the tab with unpublished changes, FIG asks first.</li></ol>
<p>Publishing is all or nothing: if one line has a problem, nothing changes and FIG tells you which line. Dishes keep their place in your deals and open orders when you edit them.</p>
<div class="callout tip"><b>Long menu?</b><p>With FIG Premium ($50 a year), snap a photo of your menu or paste its link and FIG types up every dish and price for you to check before you publish.</p></div>
<p>Out of something tonight? Mark a dish sold out for today, and it's back tomorrow.</p>"""),
             ("Minutes 10 to 13: your first deal", """<p>Pick one dish with a healthy margin and one quiet window, and write it plainly: "$3 off any noodle bowl, Monday to Thursday, 2 to 5 pm". Set a daily cap (10 is a good start) and choose dine-in only or takeout too. That's it: it's live on the map for nearby diners. <a href="/blog/deal-types-percent-dollar-2-for-1">Which deal type to pick</a>.</p>"""),
             ("Minutes 13 to 15: how you'll scan", """<p>Diners show a QR code; staff scan it with the FIG business app on any phone, tablet or computer, or type the short code if a camera won't cooperate. You can also turn on a <strong>counter code</strong> in Settings: your screen shows a code that changes every 30 seconds, and diners scan it themselves. Both are free, with no fee per diner.</p>"""),
             ("Takeout: three ways to run it", """<table><thead><tr><th></th><th>What you need</th><th>What it costs</th></tr></thead><tbody>
<tr><td>Dine-in deals only</td><td>Nothing more</td><td>Free</td></tr>
<tr><td>Takeout, paid in the app</td><td>Your HST number + Stripe payouts (Settings → Get paid)</td><td>5% of the food + Stripe's 2.9% + $0.30</td></tr>
</tbody></table>
<p>You decide which deals work as takeout and how many deals one order can use. Some restaurants also take takeout at full price, with no deal needed.</p>"""),
             ("In-app payments, explained simply", """<p><strong>Step 1: your HST number.</strong> It goes on every takeout receipt, with your restaurant as the seller. FIG checks its format as you type. Not registered for HST? You can still post deals and scan diners; takeout waits until you have a number. <a href="/blog/hst-registration-small-restaurants-ontario">HST registration for small restaurants</a>.</p>
<p><strong>Step 2: Stripe payouts.</strong> FIG uses Stripe, a payments company, to take diners' cards and pay you. Stripe asks for your business details and bank account in its own secure setup. When it's done, Get paid shows Ready.</p>
<div class="callout math"><b>What a $30 in-app takeout pays you</b><ul><li>The diner pays $33.90 ($30.00 + 13% HST).</li><li>Stripe's fee: 2.9% of $33.90 + $0.30 = $1.28.</li><li>FIG's fee: 5% of $30.00 = $1.50.</li><li>Paid out to you: $31.12, including the $3.90 HST you remit.</li></ul></div>
<p>Each month's takeout statement shows sales, HST, fees and what you kept.</p>"""),
             ("When it gets busy", """<p>Takeout is for your quiet hours, not your rush. In one tap you can <strong>pause takeout</strong> (for a set time, or until tomorrow) or <strong>add prep time</strong> so pickup times stay honest. Diners see it before they order. Turn takeout off entirely whenever you like.</p>"""),
             ("After setup", """<ul><li>Answer messages from diners in Chats. They see your restaurant's name; you see their first name and last initial.</li><li>Reply to reviews in public. Only diners whose visit was scanned can leave one.</li><li>Check your free insights after two weeks: claims, scans, and who came back.</li></ul>
<p>Questions? <a href="/help">Restaurant help</a> or <a href="/contact">message us</a>.</p>"""),
         ],
         faq=[("How long does it take to set up FIG?", "About 15 minutes with your menu handy: sign up, add your menu, publish and post one deal. In-app takeout adds your HST number and Stripe setup."),
              ("Do I need an HST number to use FIG?", "Not for deals and scanning. You need one, with Stripe payouts, for takeout, which diners pay for in the app."),
              ("What does it cost?", "Your page, menu, deals, scans, chats, insights and up to 2 locations are free. In-app takeout costs 5% of the food plus Stripe's card fee. FIG Premium is optional at $50 a year."),
              ("Can FIG type my menu for me?", "With FIG Premium, yes: snap a photo or paste a link and FIG types up every dish and price for you to check."),
              ("What if we're too busy for takeout?", "Pause takeout for a while or until tomorrow, or add prep time, in one tap."),
              ("Can diners scan us instead of us scanning them?", "Yes. Turn on the counter code in Settings: your screen shows a code that changes every 30 seconds, and diners scan it.")]),

    # CRA small supplier ($30,000 over four consecutive quarters, or in a single quarter; register within 29 days):
    #   https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/when-register-charge.html
    # Voluntary registration (charge, collect and remit; file returns; claim ITCs; stay registered at least one year):
    #   https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/account-register-voluntarily.html
    # Ontario HST 13% and the $4 prepared food point-of-sale rebate (GI-064); coupons before tax (RC4022); BN format (RC4022):
    #   sources at the top
    dict(slug="hst-registration-small-restaurants-ontario", screen="tdash", title="HST registration for small restaurants in Ontario: the $30,000 rule explained", date="2026-10-20", publish_at="2026-10-20T12:00:00-04:00", topic="For restaurants",
         dek="When a small Ontario restaurant has to register for HST, what changes when it does, and how HST works on deals and takeout. Plain-language, with the Canada Revenue Agency's own rules linked.",
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

    dict(slug="group-dining-deals", screen="chat", title="Eating out as a group: picking a place, deals and splitting the bill", date="2026-10-21", publish_at="2026-10-21T12:00:00-04:00", topic="For diners",
         dek="How to get a group from 'where should we eat?' to a table: deciding fast, checking there's room, making deals work for everyone, and splitting the bill fairly, with the arithmetic.",
         keywords="group dining deals, where to eat with friends, split the bill, group restaurant Markham, 2 for 1 group deal",
         points=["Share one deal to the group chat instead of asking an open question: a concrete option ends the debate.",
                 "Message the restaurant from FIG to check there's room for your group. Your number stays private.",
                 "Everyone can claim their own deal. Each code keeps changing, so it only works on its owner's phone.",
                 "Split by what you ordered, and share a deal's saving fairly: the arithmetic is below.",
                 "Quiet hours are best for groups: more room, more deals, more patient kitchens."],
         sections=[
             ("The short answer", """<p>Groups get stuck on choosing, not eating. Share one concrete deal to the group chat, check with the restaurant that there's room, go in a quiet hour if you can, and agree up front how you'll split. FIG helps with the first two: share any deal straight to a chat, and message the restaurant without giving out your number.</p>"""),
             ("1. Decide fast", """<p>"Where should we eat?" invites twenty answers. "2-for-1 noodles at this place, 10 minutes away, 6 pm?" invites a yes. On FIG, share a deal to your group chat: everyone sees the same place, the same deal and how far it is. If the first one doesn't land, share the next one. Two or three options is plenty.</p>
<div class="callout tip"><b>Use filters for the picky one</b><p>Set the group's must-haves in FIG's filters (halal, vegetarian, vegan, gluten-free, a budget) before you look, so every option you share already works for everyone.</p></div>"""),
             ("2. Check there's room", """<p>Six people at 7 pm on a Friday is a different ask from six at 5 pm on a Tuesday. Tap Message on the restaurant's page and ask. FIG even suggests a first message, like "Table for 4 tonight?", which fills in for you to edit before you send. The restaurant sees your first name and last initial, never your phone number.</p>"""),
             ("3. Make the deal work for the table", """<ul><li><strong>Everyone can claim.</strong> If a deal suits everyone, each person claims their own on their own phone. Codes keep changing, so each one only works on its owner's phone, and screenshots don't scan.</li><li><strong>Check the details.</strong> Some deals are on specific dishes, some on the whole order, some for dine-in only. Read the deal before the group commits.</li><li><strong>Watch the daily cap.</strong> Popular deals can run out. Claim before you leave home.</li><li><strong>Ask if unsure.</strong> How the deal applies to a shared bill is the restaurant's call. A quick message before you go saves an awkward moment at the till.</li></ul>"""),
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
              ("Can everyone in my group use the same deal?", "Each person can claim their own if the deal suits them. Codes are personal and keep changing, so one person's code can't be shared."),
              ("How should we split a bill with a deal?", "Agree first: evenly is simplest; paying for what you ordered, with any deal saving shared by the people it applied to, is fairest."),
              ("How do I check if a restaurant can fit our group?", "Tap Message on the restaurant's page in FIG. The restaurant never sees your phone number."),
              ("When is the best time to eat out as a group?", "Quiet hours, like early weeknight dinners: more room, an easier kitchen, and more deals."),
              ("Do deals apply to the whole table?", "It depends on the deal: some are on specific dishes, some on the whole order. Check the deal, or message the restaurant before you go.")]),

    dict(slug="how-to-read-restaurant-reviews", screen="map", title="How to read a restaurant's reviews on FIG", date="2026-10-22", publish_at="2026-10-22T12:00:00-04:00", topic="For diners",
         dek="Reviews on FIG come only from diners whose visit was scanned. Here's how ratings, likes and replies work, and how to read a restaurant's page to decide in a minute.",
         keywords="restaurant reviews, trustworthy restaurant reviews, how to read restaurant reviews, verified reviews restaurant app, FIG reviews",
         points=["Only diners whose visit was scanned can review a restaurant, so every review comes from a real visit.",
                 "Restaurants get stars; deals get likes. They answer different questions.",
                 "Read the spread of ratings, not just the average, and sort by Newest to see how it's doing now.",
                 "A restaurant's public replies tell you how it treats people when something goes wrong.",
                 "Paying FIG never hides, changes or reorders a review."],
         sections=[
             ("The short answer", """<p>On FIG, a review can only come from a diner whose visit was scanned at the restaurant, so you're reading people who actually ate there. To decide quickly: look at the spread of ratings, sort by Newest to see recent visits, read a couple of the low ones and how the restaurant replied, and check the likes on the deal you're considering.</p>"""),
             ("Why FIG reviews are different", """<p>Most review sites let anyone write anything. On FIG, the review button appears only after a visit is scanned, whether staff scanned the diner's code or the diner scanned the restaurant's counter code. That rules out reviews from people who never went, and it ties each review to one visit: one review per visit. Reviews show the diner's first name and last initial.</p>
<p>And nothing a restaurant pays FIG changes this. Premium doesn't hide, change or reorder reviews.</p>"""),
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
             ("Write a useful review yourself", """<p>After your visit is scanned, tap Rate this visit, or find it later under Past visits in your Voucher tab. Pick the stars and, if you like, add a few words or a photo. The most helpful reviews say:</p>
<ul><li>what you ordered;</li><li>when you went (a Tuesday afternoon is a different restaurant from a Saturday night);</li><li>one thing that stood out, good or bad.</li></ul>
<p>Be fair: rate the visit, not the price of the deal. If the deal itself disappointed, that's what a deal's like (or lack of one) is for. <a href="/blog/how-restaurant-deals-work">How deals work, from claim to counter</a>.</p>"""),
         ],
         faq=[("Can anyone review a restaurant on FIG?", "No. Only diners whose visit was scanned can review, so every review comes from a real visit. One review per visit."),
              ("What's the difference between stars and likes?", "Stars rate a restaurant visit; likes are for deals. A great restaurant can have a so-so deal, and the other way round."),
              ("Can restaurants remove bad reviews?", "No. Restaurants can reply in public, but paying FIG never hides, changes or reorders a review."),
              ("How should I sort reviews?", "Newest to see how it's doing now, Lowest to see what goes wrong, Highest to see what people order."),
              ("Whose name shows on my review?", "Your first name and last initial."),
              ("When can I review?", "After your visit is scanned: tap Rate this visit, or find it later under Past visits in your Voucher tab.")]),
]
