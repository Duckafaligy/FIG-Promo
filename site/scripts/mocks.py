"""Native mock screens for the website: real HTML and CSS built from the app's design tokens (cobalt, leaf green, ink, muted),
no screenshots and no photos. Every size is in cqw (a share of the screen's own width), so a mock scales with its frame and never stretches.
Decorative: the wrapper is one image to a screen reader. The words inside are real text (people can select it)."""
import html

COBALT, LEAF = "#1E5EFF", "#14C86B"
ICON = {  # the app's own tab icons (src/ui/icons.gen.ts), 24x24, drawn the same way
    "home": '<path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "ticket": '<path d="M3 9V6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v3a3 3 0 0 0 0 6v3a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-3a3 3 0 0 0 0-6z"/>',
    "scan": '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M4 12h16"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
    "map": '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}



def e(s):
    return html.escape(s, quote=False)


def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>'


def tabs(items, active):
    out = ""
    for key, label in items:
        if key == "scan":
            out += f'<span class="mk-tab big">{icon("scan")}<b>{label}</b></span>'
        else:
            out += f'<span class="mk-tab{" on" if key == active else ""}">{icon(key)}<b>{label}</b></span>'
    return f'<div class="mk-tabs">{out}</div>'


OWNER_TABS = [("home", "Home"), ("ticket", "Deals"), ("scan", "Scan"), ("gear", "Settings")]  # biz/(tabs)/_layout.tsx: Home, Deals, Scan, Settings (Chats is hidden)
DINER_TABS = [("home", "Home"), ("map", "Map"), ("ticket", "Deals"), ("user", "Profile")]  # (diner)/(tabs)/_layout.tsx without Chats


def tile(letter, cls=""):
    return f'<i class="mk-lt {cls}">{letter}</i>'


def status():
    return '<div class="mk-status"><span>9:41</span><span class="mk-dots"><i></i><i></i><i></i></span></div>'


def screen(body, tabbar="", label="App screen"):
    return (f'<div class="phone mk-phone" role="img" aria-label="{e(label)}"><div class="mk-scr"><div class="mk">{status()}{body}{tabbar}</div></div></div>')


def bars(vals):
    top = max(vals)
    return ('<div class="mk-bars">' + "".join(f'<i style="height:{round(v / top * 100)}%"></i>' for v in vals) + '</div>'
            '<div class="mk-days">' + "".join(f'<em>{d}</em>' for d in "MTWTFSS") + '</div>')


def owner_home():
    b = f'''<div class="mk-head"><div><b class="mk-h">Golden Lantern</b><small>Markham &middot; Open now</small></div><span class="mk-pill ok">Ready</span></div>
<div class="mk-card"><div class="mk-row"><b>This week</b><small>Scans</small></div><div class="mk-big">41 <em>+12%</em></div>{bars([4, 6, 5, 8, 9, 6, 3])}</div>
<div class="mk-sec"><b>Live deals</b><small>See all</small></div>
<div class="mk-li">{tile("D")}<span><b>2 for 1 dim sum</b><small>Weekdays 2 to 5 pm &middot; 12 left today</small></span><span class="mk-tag live">Live</span></div>
<div class="mk-li">{tile("B", "g")}<span><b>$3 off any bubble tea</b><small>Daily 3 to 5 pm &middot; 20 left today</small></span><span class="mk-tag live">Live</span></div>
<div class="mk-sec"><b>Recent scans</b><small>Today</small></div>
<div class="mk-li slim"><span class="mk-av">A</span><span><b>Alex C.</b><small>2 for 1 dim sum &middot; 3:12 pm</small></span></div>
<div class="mk-li slim"><span class="mk-av">S</span><span><b>Sam P.</b><small>$3 off any bubble tea &middot; 2:48 pm</small></span></div>'''
    return screen(b, tabs(OWNER_TABS, "home"), "FIG for restaurants: the Home screen with this week's scans and live deals")


def owner_deals():
    b = f'''<div class="mk-head"><b class="mk-h">Deals</b><span class="mk-btn sm">New deal</span></div>
<div class="mk-seg"><span class="on">Live 2</span><span>Scheduled</span><span>Drafts 1</span></div>
<div class="mk-li">{tile("D")}<span><b>2 for 1 dim sum</b><small>Weekdays 2 to 5 pm &middot; up to 1 use</small></span><span class="mk-tag live">Live</span></div>
<div class="mk-li">{tile("B", "g")}<span><b>$3 off any bubble tea</b><small>Daily 3 to 5 pm &middot; 20 a day</small></span><span class="mk-tag live">Live</span></div>
<div class="mk-li">{tile("N", "t")}<span><b>Free tea with noodles</b><small>Not visible to diners yet</small></span><span class="mk-tag">Draft</span></div>
<div class="mk-note"><b>Connect Stripe to publish</b><small>Your drafts are saved. It takes about 5 minutes.</small><span class="mk-btn">Connect Stripe</span></div>'''
    return screen(b, tabs(OWNER_TABS, "ticket"), "FIG for restaurants: the Deals screen with live deals and a draft")


def owner_scan():
    b = f'''<div class="mk-cam"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i><span>Point at the diner's code</span></div>
<div class="mk-sheet"><span class="mk-ok">&check;</span><b class="mk-h">Scan verified</b><small>Practice scan: nothing was used</small>
<div class="mk-li slim">{tile("D")}<span><b>2 for 1 dim sum</b><small>Alex C. &middot; 1 use, now used</small></span></div><span class="mk-btn">Scan next</span></div>'''
    return screen(b, tabs(OWNER_TABS, "scan"), "FIG for restaurants: a verified scan")


def owner_orders():
    b = f'''<div class="mk-head"><span class="mk-back">&lsaquo; Home</span><span class="mk-pill ok">Takeout: On</span></div><b class="mk-h">Orders</b>
<div class="mk-card order"><div class="mk-row"><span class="mk-tag new">New</span><small>#A27</small></div>
<b class="mk-h2">Alex C.</b><div class="mk-pick">Pickup 7:30 pm</div>
<div class="mk-line"><span>2 &times; Dim sum basket</span><span>$18.00</span></div><div class="mk-line"><span>1 &times; Jasmine tea</span><span>$3.00</span></div>
<div class="mk-line tot"><b>Food</b><b>$21.00</b></div>
<div class="mk-two"><span class="mk-btn ghost">Decline</span><span class="mk-btn">Accept for 7:30 pm</span></div></div>
<div class="mk-li slim"><span><b>#A24 &middot; Sam P.</b><small>Preparing &middot; pickup 6:45 pm</small></span><span class="mk-tag live">Preparing</span></div>'''
    return screen(b, tabs(OWNER_TABS, "home"), "FIG for restaurants: a new takeout order with a pickup time")


def owner_payments():
    b = f'''<div class="mk-head"><span class="mk-back">&lsaquo; Settings</span><span class="mk-btn sm ghost">CSV</span></div><b class="mk-h">Payments</b>
<div class="mk-card"><div class="mk-row"><b>October</b><small>Takeout</small></div><div class="mk-big">$412.60 <em>paid out</em></div>
<div class="mk-line"><span>Food sold</span><span>$468.00</span></div><div class="mk-line"><span>FIG keeps 5%</span><span>&minus;$23.40</span></div><div class="mk-line"><span>Stripe card fees</span><span>&minus;$32.00</span></div></div>
<div class="mk-sec"><b>Recent</b><small>Oct 24</small></div>
<div class="mk-li slim"><span><b>Order #A27</b><small>Food $21.00 &middot; FIG fee $1.05</small></span><span class="mk-amt">+$18.75</span></div>
<div class="mk-li slim"><span><b>Order #A24</b><small>Food $34.00 &middot; FIG fee $1.70</small></span><span class="mk-amt">+$30.34</span></div>'''
    return screen(b, tabs(OWNER_TABS, "gear"), "FIG for restaurants: Payments with the month's totals")


def diner_map():
    pins = "".join(f'<i class="mk-pin {c}" style="left:{x}%;top:{y}%">{l}</i>' for l, c, x, y in [("D", "", 22, 24), ("B", "g", 62, 18), ("R", "", 40, 44), ("P", "g", 74, 52), ("N", "", 18, 62), ("K", "g", 52, 70)])
    b = f'''<div class="mk-map"><span class="r r1"></span><span class="r r2"></span><span class="r r3"></span>{pins}</div>
<div class="mk-search">Where are we eating?</div>'''
    return screen(b, tabs(DINER_TABS, "map"), "FIG for diners: the map with deal pins")


def diner_claim():
    b = f'''<div class="mk-hero">{tile("D")}</div><div class="mk-pad"><b class="mk-h">2 for 1 dim sum</b><small>Golden Lantern &middot; Weekdays 2 to 5 pm</small>
<div class="mk-line"><span>Time left</span><b>Ends in 54 min</b></div><div class="mk-line"><span>Uses</span><b>1</b></div><span class="mk-btn wide">Claim this deal</span></div>'''
    return screen(b, tabs(DINER_TABS, "home"), "FIG for diners: claiming a deal")


def qr_svg():
    import random
    rnd = random.Random(7)
    n, cells = 21, ""
    def finder(ox, oy):
        return "".join(f'<rect x="{ox + x}" y="{oy + y}" width="1" height="1"/>' for x in range(7) for y in range(7) if x in (0, 6) or y in (0, 6) or (2 <= x <= 4 and 2 <= y <= 4))
    for x in range(n):
        for y in range(n):
            if (x < 8 and y < 8) or (x > 12 and y < 8) or (x < 8 and y > 12) or (8 <= x <= 12 and 8 <= y <= 12):
                continue
            if rnd.random() < 0.5:
                cells += f'<rect x="{x}" y="{y}" width="1" height="1"/>'
    return f'<svg viewBox="0 0 21 21" fill="#0E1116" shape-rendering="crispEdges">{finder(0, 0)}{finder(14, 0)}{finder(0, 14)}{cells}<rect x="8" y="8" width="5" height="5" fill="#fff"/><rect x="8.6" y="8.6" width="3.8" height="3.8" rx=".8" fill="{COBALT}"/></svg>'


def diner_qr():
    b = f'''<div class="mk-pad center"><b class="mk-h">Show your code</b><small>Staff scan it once, then it is used</small><div class="mk-qr">{qr_svg()}</div>
<b>2 for 1 dim sum</b><small>Golden Lantern &middot; code K7Q2 9XMD</small></div>'''
    return screen(b, tabs(DINER_TABS, "ticket"), "FIG for diners: the code to show at the counter")


def tablet(kind):
    """A wide restaurant screen for Home's tabs: dashboard, scanner, verified."""
    side = '<div class="mk-side"><b>FIG</b><span class="on">Home</span><span>Orders</span><span>Deals</span><span>Scan a code</span><span>Menu</span><span>Insights</span><span>Staff</span><span>Settings</span></div>'
    if kind == "dash":
        main = f'''<div class="mk-main"><div class="mk-head"><div><b class="mk-h">Golden Lantern</b><small>Markham</small></div><span class="mk-pill ok">Ready</span></div>
<div class="mk-cols"><div class="mk-card"><div class="mk-row"><b>This week</b><small>Scans</small></div><div class="mk-big">41 <em>+12%</em></div>{bars([4, 6, 5, 8, 9, 6, 3])}</div>
<div class="mk-card"><b>Live deals</b><div class="mk-li slim">{tile("D")}<span><b>2 for 1 dim sum</b><small>12 left today</small></span></div><div class="mk-li slim">{tile("B", "g")}<span><b>$3 off bubble tea</b><small>20 left today</small></span></div></div></div></div>'''
        label = "FIG for restaurants on a tablet: the dashboard"
    elif kind == "scan":
        main = '<div class="mk-main"><div class="mk-cam wide"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i><span>Point at the diner\'s code</span></div></div>'
        label = "FIG for restaurants on a tablet: the scanner"
    else:
        main = f'<div class="mk-main center"><span class="mk-ok">&check;</span><b class="mk-h">Scan verified</b><div class="mk-li slim">{tile("D")}<span><b>2 for 1 dim sum</b><small>Alex C. &middot; now used</small></span></div></div>'
        label = "FIG for restaurants on a tablet: a verified scan"
    return f'<div class="mk-tab-scr" role="img" aria-label="{e(label)}"><div class="mk-t">{side}{main}</div></div>'


SCREENS = {"home": owner_home, "deals": owner_deals, "scan": owner_scan, "orders": owner_orders, "payments": owner_payments,
           "map": diner_map, "claim": diner_claim, "qr": diner_qr}


# ---------- Home's "Good to know" cards: one small animated scene per blog group (replaces the 960x600 video loops) ----------
# Plain HTML + CSS (site.css "gs-"), every size in cqw of the card's picture, so it's sharp and never clips at any width. The
# moves are CSS keyframes on transform/opacity only; the static look (reduced motion, "Pause animations") is the finished state.
# The QR is a real code (qrcode, error correction H, 25x25) for the example claim code FIG-K7Q2-9XMD, the FIG tile on top.
QR_N, QR_D = 25, "M0 0h7v1h-7zM8 0h3v1h-3zM18 0h7v1h-7zM0 1h1v1h-1zM6 1h1v1h-1zM8 1h3v1h-3zM12 1h1v1h-1zM15 1h1v1h-1zM18 1h1v1h-1zM24 1h1v1h-1zM0 2h1v1h-1zM2 2h3v1h-3zM6 2h1v1h-1zM9 2h5v1h-5zM16 2h1v1h-1zM18 2h1v1h-1zM20 2h3v1h-3zM24 2h1v1h-1zM0 3h1v1h-1zM2 3h3v1h-3zM6 3h1v1h-1zM8 3h5v1h-5zM14 3h1v1h-1zM16 3h1v1h-1zM18 3h1v1h-1zM20 3h3v1h-3zM24 3h1v1h-1zM0 4h1v1h-1zM2 4h3v1h-3zM6 4h1v1h-1zM8 4h2v1h-2zM14 4h1v1h-1zM16 4h1v1h-1zM18 4h1v1h-1zM20 4h3v1h-3zM24 4h1v1h-1zM0 5h1v1h-1zM6 5h1v1h-1zM8 5h3v1h-3zM12 5h3v1h-3zM18 5h1v1h-1zM24 5h1v1h-1zM0 6h7v1h-7zM8 6h1v1h-1zM10 6h1v1h-1zM12 6h1v1h-1zM14 6h1v1h-1zM16 6h1v1h-1zM18 6h7v1h-7zM13 7h2v1h-2zM16 7h1v1h-1zM3 8h1v1h-1zM6 8h1v1h-1zM9 8h3v1h-3zM14 8h1v1h-1zM16 8h1v1h-1zM19 8h3v1h-3zM23 8h2v1h-2zM2 9h3v1h-3zM7 9h1v1h-1zM16 9h2v1h-2zM19 9h3v1h-3zM24 9h1v1h-1zM2 10h1v1h-1zM4 10h4v1h-4zM18 10h2v1h-2zM22 10h2v1h-2zM0 11h1v1h-1zM2 11h1v1h-1zM4 11h2v1h-2zM7 11h1v1h-1zM20 11h1v1h-1zM22 11h2v1h-2zM2 12h1v1h-1zM6 12h1v1h-1zM18 12h1v1h-1zM23 12h2v1h-2zM1 13h3v1h-3zM7 13h1v1h-1zM16 13h2v1h-2zM19 13h1v1h-1zM21 13h2v1h-2zM0 14h1v1h-1zM2 14h1v1h-1zM5 14h2v1h-2zM24 14h1v1h-1zM1 15h1v1h-1zM7 15h2v1h-2zM17 15h2v1h-2zM20 15h1v1h-1zM22 15h1v1h-1zM24 15h1v1h-1zM0 16h2v1h-2zM6 16h1v1h-1zM9 16h3v1h-3zM13 16h2v1h-2zM16 16h5v1h-5zM22 16h1v1h-1zM8 17h3v1h-3zM12 17h2v1h-2zM15 17h2v1h-2zM20 17h1v1h-1zM24 17h1v1h-1zM0 18h7v1h-7zM10 18h1v1h-1zM12 18h2v1h-2zM16 18h1v1h-1zM18 18h1v1h-1zM20 18h1v1h-1zM22 18h1v1h-1zM0 19h1v1h-1zM6 19h1v1h-1zM10 19h2v1h-2zM13 19h2v1h-2zM16 19h1v1h-1zM20 19h2v1h-2zM23 19h2v1h-2zM0 20h1v1h-1zM2 20h3v1h-3zM6 20h1v1h-1zM10 20h3v1h-3zM15 20h6v1h-6zM24 20h1v1h-1zM0 21h1v1h-1zM2 21h3v1h-3zM6 21h1v1h-1zM8 21h1v1h-1zM10 21h2v1h-2zM13 21h1v1h-1zM15 21h2v1h-2zM18 21h1v1h-1zM20 21h1v1h-1zM23 21h1v1h-1zM0 22h1v1h-1zM2 22h3v1h-3zM6 22h1v1h-1zM10 22h1v1h-1zM13 22h1v1h-1zM15 22h2v1h-2zM18 22h2v1h-2zM21 22h2v1h-2zM24 22h1v1h-1zM0 23h1v1h-1zM6 23h1v1h-1zM9 23h1v1h-1zM11 23h1v1h-1zM13 23h2v1h-2zM19 23h1v1h-1zM21 23h1v1h-1zM24 23h1v1h-1zM0 24h7v1h-7zM11 24h1v1h-1zM14 24h1v1h-1zM16 24h4v1h-4zM21 24h1v1h-1zM24 24h1v1h-1z"


def _qr():
    c, ring, t = QR_N / 2, 7.2, 6.0
    return (f'<svg class="gs-qr" viewBox="0 0 {QR_N} {QR_N}" shape-rendering="crispEdges"><path d="{QR_D}" fill="#0E1116"/>'
            f'<rect x="{c - ring / 2}" y="{c - ring / 2}" width="{ring}" height="{ring}" rx="1.6" fill="#fff" shape-rendering="auto"/>'
            f'<rect x="{c - t / 2}" y="{c - t / 2}" width="{t}" height="{t}" rx="1.5" fill="{COBALT}" shape-rendering="auto"/>'
            f'<svg x="{c - 2.2}" y="{c - 2.2}" width="4.4" height="4.4" viewBox="743 716 100 100" class="gs-lg"><use href="#logo"/></svg></svg>')


def _pin(x, y, i):
    return f'<i class="gs-pin p{i}" style="left:{x}%;top:{y}%"><svg viewBox="743 716 100 100"><use href="#logo"/></svg></i>'


GTK_SCENES = {
    "eat-out-for-less": f'''<div class="gs gs-eat">
<div class="gs-card gs-deal"><div class="gs-top">{tile("B")}<span class="gs-ex">Example</span></div><b class="gs-big">20% off</b><b class="gs-name">bubble tea</b><small>Today, 2 to 5 pm</small>
<span class="gs-btn"><span class="gs-b1">Claim</span><span class="gs-b2">Claimed &check;</span></span></div>
<div class="gs-card gs-ticket">{_qr()}<b>Show this to staff</b><small>K7Q2 9XMD</small></div></div>''',
    "fill-quiet-hours": f'''<div class="gs gs-quiet"><div class="gs-card gs-owner">
<div class="gs-row">{tile("D")}<span class="gs-tt"><b>2 for 1 dim sum</b><small><span class="gs-ex">Example</span> Weekdays</small></span><span class="gs-st"><span class="gs-draft">Draft</span><span class="gs-live">Live</span></span></div>
<div class="gs-day"><span class="gs-track"><i class="gs-seg"></i></span><span class="gs-h t1">11 am</span><span class="gs-h t2">2 pm</span><span class="gs-h t3">5 pm</span><span class="gs-h t4">10 pm</span></div>
<div class="gs-row gs-on"><span><b>Deal on</b> <small>2 to 5 pm</small></span><span class="gs-sw"><i></i></span></div></div></div>''',
    "takeout-and-money": '''<div class="gs gs-money"><div class="gs-card gs-rcpt">
<div class="gs-rh"><b>Takeout order</b><span class="gs-ex">Example</span></div>
<p class="gs-r r1"><span>Food</span><b>$20.00</b></p><p class="gs-r r2"><span>HST (13%)</span><b>$2.60</b></p>
<p class="gs-r r3"><span>FIG, 5% of the food</span><b>&minus;$1.00</b></p><p class="gs-r r4"><span>Stripe, 2.9% + $0.30</span><b>&minus;$0.96</b></p>
<p class="gs-r gs-keep"><span>You keep</span><b>$18.04</b></p><p class="gs-note">+ HST $2.60: yours to remit</p></div></div>''',
    "fig-in-markham": f'''<div class="gs gs-map"><svg class="gs-land" viewBox="0 0 160 100" preserveAspectRatio="none" aria-hidden="true">
<path d="M96 6c10 4 22 2 30 10s4 18 14 22 18 0 20 8v14H112c-8-6-20-4-24-12s4-18-2-26 2-14 10-16z" fill="#DCF3E6"/><path d="M8 70c10-6 22-2 30-8s14-14 26-12 14 12 6 18-24 6-34 8-22 4-28-6z" fill="#DCF3E6"/>
<g fill="none" stroke="#fff" stroke-linecap="round"><path d="M-4 58C40 52 90 50 164 44" stroke-width="2.6"/><path d="M92 -4C94 30 96 60 98 104" stroke-width="2.6"/><path d="M28 -4C29 30 30 66 31 104" stroke-width="2.6"/>
<path d="M-4 30C50 26 110 22 164 20M-4 86C60 82 110 80 164 76M60 -4C61 40 62 70 64 104M124 -4C126 40 128 70 130 104" stroke-width="1.2"/></g></svg>
<span class="gs-place gs-vm" style="left:19%;top:40%"><i></i>Vaughan Mills</span><span class="gs-place gs-rhill" style="left:44%;top:21%"><i></i>Richmond Hill</span>
<b class="gs-mk">Markham</b>{_pin(70, 34, 1)}{_pin(80, 27, 2)}{_pin(88, 40, 3)}{_pin(75, 50, 4)}{_pin(64, 47, 5)}
<p class="gs-cap"><b>Markham first,</b> expanding to Richmond Hill and Vaughan Mills</p></div>''',
}


def gtk_scene(slug):
    return GTK_SCENES.get(slug)
