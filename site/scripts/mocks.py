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


def screen(body, tabbar="", label="App screen", loop=""):
    return (f'<div class="phone mk-phone" role="img" aria-label="{e(label)}"><div class="mk-scr"{(' data-loop="' + loop + '"') if loop else ""}><div class="mk">{status()}{body}{tabbar}</div></div></div>')


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
    pins = "".join(f'<i class="mk-pin pulse {c}" style="left:{x}%;top:{y}%">{l}</i>' for l, c, x, y in [("D", "", 22, 24), ("B", "g", 62, 18), ("R", "", 40, 44), ("P", "g", 74, 52), ("N", "", 18, 62), ("K", "g", 52, 70)])
    b = f'''<div class="mk-map"><span class="r r1"></span><span class="r r2"></span><span class="r r3"></span>{pins}</div>
<div class="mk-search">Where are we eating?</div>'''
    return screen(b, tabs(DINER_TABS, "map"), "FIG for diners: the map with deal pins")


def diner_claim():
    b = f'''<div class="mk-hero">{tile("D")}</div><div class="mk-pad"><b class="mk-h">2 for 1 dim sum</b><small>Golden Lantern &middot; Weekdays 2 to 5 pm</small>
<div class="mk-line"><span>Time left</span><b>Ends in 54 min</b></div><div class="mk-line"><span>Uses</span><b>1</b></div><span class="mk-btn wide mk-press">Claim this deal</span></div>'''
    return screen(b, tabs(DINER_TABS, "home"), "FIG for diners: claiming a deal")


def diner_saved():
    b = f'''<div class="mk-pad center sv"><span class="mk-ok pop-in">&check;</span><b class="mk-h">Saved $8</b><small>at Golden Lantern</small>
<div class="mk-li slim">{tile("D")}<span><b>2 for 1 dim sum</b><small>Scanned by staff &middot; 3:12 pm</small></span></div>
<small>It came off your bill. You paid the restaurant as usual.</small></div>'''
    return screen(b, tabs(DINER_TABS, "ticket"), "FIG for diners: the deal came off the bill and saved $8")


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
    b = f'''<div class="mk-pad center"><b class="mk-h">Show your code</b><small>New code after every scan</small><div class="mk-qr">{qr_svg()}</div>
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


SCREENS = {"saved": diner_saved, "home": owner_home, "deals": owner_deals, "scan": owner_scan, "orders": owner_orders, "payments": owner_payments,
           "map": diner_map, "claim": diner_claim, "qr": diner_qr}
