# Direction C, the mix: from fig-promo-e9's design. Run after make.py: python site/preview/make_c.py
"""Direction C, the mix (user 2026-10-13: "i like a mix but id still keep a navbar maybe"): A's top navbar on every page and
its airy Home and two-column restaurant page, with B's fuller modules (stat tiles, live-now row, map + list module,
floating results panel, tabs); a sidebar only for the owner area and a collapsible filters rail on the Map."""
import make as m  # same brand CSS, data, cards, rows, pins (also rewrites A and B, unchanged)
from make import CSS, R, CHIPS, LOGO, PHOTO, SITE, card, row, pins

C_CSS = """
html { scroll-behavior: smooth; } [id] { scroll-margin-top: 90px; }
html.side-nav body { padding-left: 240px; }
html.side-nav .nav { position: fixed; left: 0; top: 0; bottom: 0; width: 240px; height: auto; flex-direction: column; align-items: stretch; gap: 14px; padding: 22px 16px; border-bottom: 0; border-right: 1px solid var(--line); z-index: 30; }
html.side-nav .nav .search { flex: 0 0 44px; max-width: none; } html.side-nav .nav .grow { display: none; }
html.side-nav .nav .links { display: flex; flex-direction: column; align-items: stretch; gap: 4px; margin: 0; padding: 0; width: 100%; } html.side-nav .nav .links a { text-align: left; } html.side-nav .nav .search { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; } html.side-nav .nav .links a { padding: 10px 14px; border-radius: 12px; }
html.side-nav .nav .ic, html.side-nav .nav .av { align-self: flex-start; } html.side-nav .nav .av { margin-top: auto; }
html.side-nav .full { height: 100vh; } html.side-nav .oside { top: 0; }
@media (max-width: 700px) { html.side-nav body { padding-left: 0; } }

.nav { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; gap: 22px; height: 68px; padding: 0 28px; background: rgba(255,255,255,.97); border-bottom: 1px solid var(--line); }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 21px; letter-spacing: -0.03em; }
.brand img { width: 30px; height: 30px; }
.nav .search { flex: 1; max-width: 460px; height: 44px; }
.nav .grow { flex: 1; }
.area { display: inline-flex; align-items: center; gap: 6px; height: 40px; padding: 0 14px; border-radius: 999px; border: 1px solid var(--line); font-weight: 700; font-size: 14px; }
.links { display: flex; gap: 4px; margin-left: auto; }
.links span { padding: 10px 14px; border-radius: 999px; font-weight: 700; font-size: 15px; color: var(--muted); }
.links .on { background: var(--ice); color: var(--cobalt); }
.ic { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--line); display: grid; place-items: center; font-size: 16px; position: relative; }
.ic .dot { position: absolute; top: 8px; right: 9px; width: 8px; height: 8px; border-radius: 50%; background: #D92D3A; border: 2px solid #fff; }
.av { width: 40px; height: 40px; border-radius: 50%; background: var(--cobalt); color: #fff; display: grid; place-items: center; font-weight: 800; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 0 28px; }
/* home */
.hero { background: var(--ice); padding: 40px 0 36px; }
.herog { display: grid; grid-template-columns: 1fr 470px; gap: 36px; align-items: center; }
.hero .h1 { font-size: 52px; } .hero .h1 span { color: var(--cobalt); }
.hero .search { margin-top: 20px; background: #fff; height: 52px; max-width: 600px; }
.hero .chips { margin-top: 16px; flex-wrap: wrap; }
.tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.tile { padding: 18px 20px; border-radius: 20px; background: #fff; border: 1px solid var(--line); display: grid; gap: 4px; }
.tile b { font-size: 30px; letter-spacing: -0.04em; } .tile.c { background: var(--cobalt); border-color: var(--cobalt); color: #fff; } .tile.c .dim { color: #DDE7FF; }
.tile.n { background: var(--night); border-color: var(--night); color: #fff; } .tile.n .dim { color: #A3ADBF; }
.sec { padding-top: 36px; }
.sech { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 16px; } .sech .h2 { font-size: 28px; } .sech a { color: var(--cobalt); font-weight: 800; font-size: 14px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.card { border-radius: 20px; overflow: hidden; border: 1px solid var(--line); background: #fff; }
.card .ph { height: 160px; background-size: cover; background-position: center; position: relative; }
.card .deal { position: absolute; left: 12px; bottom: 12px; }
.card .cb { padding: 13px 15px 16px; display: grid; gap: 4px; font-size: 14px; } .card .cb b { font-size: 16px; }
.two { display: grid; grid-template-columns: 1.5fr 1fr; gap: 18px; }
.panel { border-radius: 24px; border: 1px solid var(--line); overflow: hidden; background: #fff; }
.panel .map { height: 340px; }
.panel h4 { padding: 16px 18px 6px; font-size: 17px; }
.lrow { display: flex; gap: 12px; padding: 12px 18px; border-bottom: 1px solid var(--line); align-items: center; }
.lrow.sel { background: var(--ice); box-shadow: inset 4px 0 0 var(--cobalt); }
.lph { width: 64px; height: 64px; border-radius: 14px; background-size: cover; background-position: center; flex-shrink: 0; }
.lt { display: grid; gap: 3px; font-size: 13px; } .lt b { font-size: 15px; }
.deal.sm { padding: 3px 9px; font-size: 11px; justify-self: start; }
.three { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.mini { display: flex; gap: 12px; align-items: center; padding: 12px; border-radius: 18px; border: 1px solid var(--line); }
.mini .lph { width: 56px; height: 56px; }
.launch { display: flex; gap: 12px; align-items: center; padding: 16px 20px; border-radius: 18px; background: var(--soft); border: 1px solid var(--line); margin-top: 24px; font-weight: 700; }
/* map: floating results panel + collapsible filters rail */
.full { position: relative; height: calc(100vh - 68px); }
.full .map { position: absolute; inset: 0; }
.rail { position: absolute; left: 20px; top: 20px; bottom: 20px; width: 72px; background: #fff; border-radius: 22px; box-shadow: 0 14px 34px rgba(10,16,32,.12); display: grid; align-content: start; gap: 6px; padding: 12px 8px; z-index: 3; justify-items: center; font-size: 11px; font-weight: 700; color: var(--dim); text-align: center; }
.rail i { width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center; font-style: normal; font-size: 18px; background: var(--soft); color: var(--ink); }
.rail i.on { background: var(--cobalt); color: #fff; }
.float { position: absolute; left: 106px; top: 20px; bottom: 20px; width: 390px; background: #fff; border-radius: 24px; box-shadow: 0 24px 50px rgba(10,16,32,.18); display: flex; flex-direction: column; overflow: hidden; z-index: 3; }
.float .top { padding: 18px 18px 12px; display: grid; gap: 12px; border-bottom: 1px solid var(--line); } .float .top .h2 { font-size: 22px; }
.float .chips { flex-wrap: wrap; }
.mapctl { position: absolute; right: 20px; top: 20px; display: grid; gap: 10px; justify-items: end; z-index: 3; }
.zoom { display: grid; background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 20px rgba(10,16,32,.12); }
.zoom b { width: 44px; height: 44px; display: grid; place-items: center; font-size: 20px; border-bottom: 1px solid var(--line); }
.peek { position: absolute; left: calc(106px + 390px + 24px); bottom: 24px; display: flex; gap: 14px; align-items: center; padding: 12px 14px; border-radius: 20px; background: #fff; box-shadow: 0 24px 50px rgba(10,16,32,.18); z-index: 3; }
.peek .lph { width: 60px; height: 60px; }
.credit { position: absolute; right: 10px; bottom: 8px; font-size: 11px; color: var(--dim); background: rgba(255,255,255,.85); padding: 2px 6px; border-radius: 4px; z-index: 3; }
/* restaurant: gallery + two columns, tabs on the left */
.gal { display: grid; grid-template-columns: 2fr 1fr 1fr; grid-template-rows: 190px 190px; gap: 10px; margin-top: 24px; }
.gal div { border-radius: 20px; background-size: cover; background-position: center; } .gal div:first-child { grid-row: span 2; }
.cols { display: grid; grid-template-columns: 1fr 380px; gap: 40px; padding: 26px 0 60px; }
.rname { display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; } .rname .h1 { font-size: 46px; }
.meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.tabs { display: flex; gap: 4px; margin-top: 26px; border-bottom: 1px solid var(--line); }
.tab { padding: 14px 14px; font-weight: 800; font-size: 15px; color: var(--dim); border-bottom: 3px solid transparent; } .tab.on { color: var(--ink); border-color: var(--cobalt); }
.dish { display: flex; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: 15px; } .dish small { display: block; color: var(--dim); font-size: 13px; margin-top: 2px; }
.dgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 18px; }
.dc { padding: 18px; border-radius: 20px; border: 1px solid var(--line); display: grid; gap: 8px; } .dc b { font-size: 17px; }
.rev { padding: 16px 0; border-bottom: 1px solid var(--line); display: grid; gap: 6px; font-size: 14px; } .rev .reply { margin-left: 16px; padding: 10px 14px; border-radius: 14px; background: var(--soft); color: var(--muted); }
.side { position: sticky; top: 88px; align-self: start; display: grid; gap: 14px; }
.claim { padding: 22px; border-radius: 24px; border: 2px solid var(--cobalt); background: #fff; box-shadow: 0 14px 34px rgba(10,16,32,.08); display: grid; gap: 12px; } .claim b { font-size: 20px; }
.box { padding: 18px; border-radius: 22px; background: var(--soft); border: 1px solid var(--line); display: grid; gap: 10px; font-size: 14px; } .box .map { height: 150px; border-radius: 16px; }
/* owner: top navbar + owner sidebar */
.owner { display: grid; grid-template-columns: 236px 1fr; min-height: calc(100vh - 68px); }
.oside { border-right: 1px solid var(--line); padding: 20px 14px; display: grid; align-content: start; gap: 2px; background: var(--soft); }
.oside .navi { display: flex; align-items: center; gap: 12px; height: 42px; padding: 0 12px; border-radius: 12px; font-weight: 700; font-size: 14px; color: var(--muted); }
.oside .navi.on { background: #fff; color: var(--cobalt); box-shadow: 0 2px 8px rgba(10,16,32,.06); }
.oside .navi .n { margin-left: auto; background: var(--cobalt); color: #fff; font-size: 11px; padding: 2px 7px; border-radius: 99px; }
.oside .lbl { font-size: 12px; font-weight: 700; color: var(--dim); padding: 14px 12px 6px; }
.obody { padding: 26px 30px 60px; min-width: 0; }
.otiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 18px 0 22px; }
.board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.col { padding: 14px; border-radius: 20px; background: var(--soft); border: 1px solid var(--line); display: grid; align-content: start; gap: 10px; }
.col h5 { font-size: 14px; display: flex; justify-content: space-between; }
.ord { padding: 12px 14px; border-radius: 16px; background: #fff; border: 1px solid var(--line); display: grid; gap: 4px; font-size: 13px; } .ord b { font-size: 15px; }
.chart { display: flex; align-items: flex-end; gap: 10px; height: 150px; padding: 10px 0 0; } .chart div { flex: 1; border-radius: 10px 10px 4px 4px; background: #DCE4F7; } .chart div.t { background: var(--cobalt); }
.days { display: flex; gap: 10px; font-size: 12px; color: var(--dim); } .days span { flex: 1; text-align: center; }
.drow { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--line); font-size: 14px; } .drow b { font-size: 15px; } .drow .bar { flex: 1; height: 8px; border-radius: 99px; background: var(--ice); overflow: hidden; } .drow .bar i { display: block; height: 100%; background: var(--cobalt); border-radius: 99px; }
.sw { width: 40px; height: 24px; border-radius: 99px; background: var(--leaf); position: relative; } .sw::after { content: ""; position: absolute; right: 3px; top: 3px; width: 18px; height: 18px; border-radius: 50%; background: #fff; }
/* phone: top bar + bottom bar */
.bottombar { display: none; position: fixed; left: 0; right: 0; bottom: 0; height: 64px; background: #fff; border-top: 1px solid var(--line); justify-content: space-around; align-items: center; font-weight: 700; font-size: 12px; color: var(--dim); z-index: 20; }
.bottombar .on { color: var(--cobalt); }
@media (max-width: 700px) {
  .nav { padding: 0 16px; gap: 10px; height: 60px; } .nav .search, .links, .area { display: none; } .nav .grow { flex: 1; }
  .bottombar { display: flex; } .wrap { padding: 0 16px; } body { padding-bottom: 70px; }
  .herog { grid-template-columns: 1fr; gap: 18px; } .hero { padding: 24px 0; } .hero .h1 { font-size: 36px; }
  .grid { grid-template-columns: 1fr 1fr; gap: 12px; } .card .ph { height: 120px; } .two, .three { grid-template-columns: 1fr; } .panel .map { height: 220px; }
  .full { height: calc(100vh - 60px - 64px); } .rail { display: none; } .float { left: 0; right: 0; top: auto; bottom: 0; width: auto; height: 46%; border-radius: 24px 24px 0 0; } .peek { display: none; } .mapctl { top: 14px; right: 14px; }
  .gal { grid-template-columns: 1fr; grid-template-rows: 220px; } .gal div:not(:first-child) { display: none; } .gal div:first-child { grid-row: auto; }
  .cols { grid-template-columns: 1fr; gap: 20px; } .side { position: static; } .rname .h1 { font-size: 32px; } .rname { flex-direction: column; align-items: flex-start; } .dgrid { grid-template-columns: 1fr; }
  .owner { grid-template-columns: 1fr; } .oside { display: none; } .obody { padding: 18px 16px 90px; } .otiles { grid-template-columns: 1fr 1fr; } .board { grid-template-columns: 1fr; }
}
"""

FLIP = '<script>document.body.dataset.flip = "1";</script>'

def nav(on, owner=False):
    if owner:
        links = ""
        mid = '<span class="area">Golden Lantern ▾</span><span class="tag" style="background:#E7F8EF;color:var(--leaft)">● Live</span>'
        bar = ["Home", "Orders", "Scan", "Deals", "Settings"]
    else:
        links = '<div class="links">' + "".join(f'<a {"href=\"./\"" if x == "Home" else "href=\"map.html\"" if x == "Map" else "href=\"owner.html\"" if x == "For owners" else ""} class="{"on" if x == on else ""}">{x}</a>' for x in ["Home", "Map", "Deals", "Saved", "Chats", "For owners"]) + "</div>"
        mid = '<div class="search">⌕&nbsp; Search dishes, restaurants…</div><span class="area">◎ Markham ▾</span>'
        bar = ["Home", "Map", "Deals", "Saved", "Account"]
    return f'''<div class="nav"><a class="brand" href="./"><img src="{LOGO}" alt="">FIG</a>{mid}<div class="grow"></div>{links}<span class="ic">🔔<span class="dot"></span></span><span class="av">A</span></div>
<div class="bottombar">{"".join(f'<a {"href=\"./\"" if x == "Home" else "href=\"map.html\"" if x == "Map" else "href=\"owner.html\"" if x == "For owners" else ""} class="{"on" if x == on else ""}">{x}</a>' for x in bar)}</div>'''

chips = lambda on="All", items=CHIPS: '<div class="chips">' + "".join(f'<span class="chip{" on" if c == on else ""}">{c}</span>' for c in items) + "</div>"
mini = lambda r: f'<a class="mini" href="rest.html"><div class="lph" style="background-image:url({PHOTO}/{r[6]}.webp)"></div><div class="lt"><b>{r[0]}</b><span class="dim">{r[1]} · {r[3]}</span></div></a>'

m.page("C-home", FLIP + nav("Home") + f'''
<div class="hero"><div class="wrap herog"><div><div class="h1">Good evening, Alex.<br><span>Where are we eating?</span></div>
<div class="search">⌕&nbsp; Dim sum, ramen, bubble tea…</div>{chips()}</div>
<div class="tiles"><div class="tile c"><span class="dim">Live deals near you</span><b>5</b></div><div class="tile"><span class="dim">Places on FIG nearby</span><b>8</b></div><div class="tile"><span class="dim">Your saved places</span><b>3</b></div><div class="tile n"><span class="dim">You've saved with FIG</span><b>$24</b></div></div></div></div>
<div class="wrap"><div class="sec"><div class="sech"><span class="h2">Live now near you</span><a href="map.html">All deals →</a></div><div class="grid">{"".join(card(r) for r in R[:4])}</div></div>
<div class="sec"><div class="sech"><span class="h2">Around you</span><a href="map.html">Open the map →</a></div><div class="two"><div class="panel"><div class="map">{pins(0)}</div></div><div class="panel"><h4>Nearest first</h4>{"".join(row(r, i) for i, r in enumerate(R[:4]))}</div></div></div>
<div class="sec three"><div><div class="sech"><span class="h2" style="font-size:22px">Saved</span><a href="map.html">See all</a></div><div style="display:grid;gap:10px">{"".join(mini(r) for r in R[4:7])}</div></div>
<div><div class="sech"><span class="h2" style="font-size:22px">Recently viewed</span><a href="map.html">See all</a></div><div style="display:grid;gap:10px">{"".join(mini(r) for r in [R[0], R[2], R[5]])}</div></div>
<div><div class="sech"><span class="h2" style="font-size:22px">New on FIG</span><a href="map.html">See all</a></div><div style="display:grid;gap:10px">{"".join(mini(r) for r in [R[7], R[6], R[1]])}</div></div></div>
<div class="launch"><span class="deal">Jan 1, 2027</span>FIG opens in Markham. Save places now and their first deals show up here.</div><div style="height:60px"></div></div>''', C_CSS)

rail = '<div class="rail"><i class="on">☰</i>Filters<i>◷</i>Open<i>$</i>Price<i>✦</i>Deals<i>♡</i>Diet</div>'
m.page("C-map", FLIP + nav("Map") + f'''<div class="full"><div class="map">{pins(0)}</div>{rail}
<div class="float"><div class="top"><span class="h2">8 places near Markham</span>{chips("All", CHIPS[:6])}<span class="label">5 with a deal now · nearest first</span></div>{"".join(row(r, i) for i, r in enumerate(R[:7]))}</div>
<div class="peek"><div class="lph" style="background-image:url({PHOTO}/golden-lantern.webp)"></div><div class="lt"><b>Golden Lantern</b><span class="deal sm">2 for 1 dim sum</span></div><span class="btn sm">Claim</span></div>
<div class="mapctl"><span class="btn">◎&nbsp; Use my location</span><div class="zoom"><b>+</b><b style="border:0">−</b></div></div><span class="credit">© OpenMapTiles © OpenStreetMap</span></div>''', C_CSS)

m.page("C-rest", FLIP + nav("Home") + f'''<div class="wrap"><div class="gal"><div style="background-image:url({PHOTO}/golden-lantern.webp)"></div><div style="background-image:url({PHOTO}/dumpling-house.webp)"></div><div style="background-image:url({PHOTO}/alt-hotpot.webp)"></div><div style="background-image:url({PHOTO}/chatime.webp)"></div><div style="background-image:url({PHOTO}/noodle-bar.webp)"></div></div>
<div class="cols"><div><div class="rname"><div><span class="h1">Golden Lantern</span><div class="meta"><span class="tag">Dim sum</span><span class="tag">$$</span><span class="tag">★ 4.7 · 128 reviews</span><span class="tag" style="background:#E7F8EF;color:var(--leaft)">Open until 9 pm</span><span class="tag">0.8 km</span></div></div><span class="btn ghost">♡ Save</span></div>
<div class="tabs"><a class="tab on" href="#deals">Deals</a><a class="tab" href="#menu">Menu</a><a class="tab" href="#reviews">Reviews</a><a class="tab" href="#info">Info</a></div>
<div class="dgrid" id="deals"><div class="dc" style="border:2px solid var(--cobalt)"><span class="deal" style="justify-self:start">Today until 9 pm</span><b>2 for 1 dim sum</b><span class="muted" style="font-size:14px">Any two steamed baskets, the second free.</span></div><div class="dc"><span class="tag" style="justify-self:start">Mon–Thu</span><b>Free egg tarts</b><span class="muted" style="font-size:14px">With any order</span></div></div>
<div class="sech" id="menu" style="margin-top:28px"><span class="h2" style="font-size:24px">Popular on the menu</span><a>Full menu →</a></div><div class="dish"><span>Har gow<small>4 pieces · shrimp</small></span><b>$7.50</b></div><div class="dish"><span>Siu mai<small>4 pieces · pork & shrimp</small></span><b>$6.95</b></div><div class="dish"><span>Egg tarts<small>3 pieces</small></span><b>$6.50</b></div>
<div class="sech" id="reviews" style="margin-top:28px"><span class="h2" style="font-size:24px">Reviews</span><a>All 128 →</a></div><div class="rev"><b>★★★★★ · Priya S.</b><span class="muted">The har gow were perfect and the deal came off at the counter in seconds.</span><span class="reply">Golden Lantern: Thanks Priya, see you soon!</span></div>
<div class="sech" style="margin-top:28px"><span class="h2" style="font-size:24px">Similar places</span></div><div class="grid" style="grid-template-columns:repeat(3,1fr)">{"".join(card(r) for r in [R[5], R[2], R[4]])}</div></div>
<div class="side"><div class="claim"><span class="deal" style="justify-self:start">Deal · today until 9 pm</span><b>2 for 1 dim sum</b><span class="muted" style="font-size:14px;line-height:1.5">Claim it, then show your code at the counter. It stays yours while the deal runs.</span><span class="btn">Claim this deal</span><span class="btn ghost">Order takeout</span></div>
<div class="box" id="info"><b style="font-size:16px">Hours & location</b><span class="muted">Daily 10 am – 9 pm · (905) 555-0142</span><span class="muted">4350 Steeles Ave E, Markham</span><div class="map">{pins(0)}</div></div></div></div></div>''', C_CSS)

bars = [38, 52, 44, 66, 58, 80, 100]
oside = '<aside class="oside">' + "".join(f'<div class="navi{" on" if x == "Dashboard" else ""}">{ic}&nbsp; {x}{f"<span class=n>{n}</span>" if n else ""}</div>' for x, ic, n in [("Dashboard", "⌂", ""), ("Orders", "▤", "2"), ("Scan a code", "⌗", ""), ("Deals", "✦", ""), ("Menu", "☰", ""), ("Hours", "◷", ""), ("Insights", "▥", ""), ("Reviews", "★", "1"), ("Chats", "✉", "")]) + '<div class="lbl">Business</div>' + "".join(f'<div class="navi">{ic}&nbsp; {x}</div>' for x, ic in [("Staff & devices", "◎"), ("Locations", "⌖"), ("FIG Premium", "◆"), ("Settings", "⚙")]) + "</aside>"
m.page("C-owner", FLIP + nav("Home", owner=True) + f'''<div class="owner">{oside}<div class="obody"><span class="h1" style="font-size:34px">Good evening, Mei</span><p class="muted" style="margin-top:4px">Golden Lantern · Tuesday · takeout is on</p>
<div class="otiles"><div class="tile c"><span class="dim">Scanned in today</span><b>14</b></div><div class="tile"><span class="dim">Takeout orders</span><b>3</b></div><div class="tile"><span class="dim">Live deals</span><b>2</b></div><div class="tile"><span class="dim">Page views this week</span><b>1,240</b></div></div>
<div class="sech"><span class="h2" style="font-size:22px">Takeout orders</span><a>All orders →</a></div>
<div class="board"><div class="col"><h5>New <span class="tag">2</span></h5><div class="ord"><b>#A27 · Dana D.</b><span class="dim">2× Har gow · pickup 6:54 pm</span><span class="btn sm">Accept</span></div><div class="ord"><b>#A28 · Ken W.</b><span class="dim">Siu mai, egg tarts · 7:10 pm</span><span class="btn sm">Accept</span></div></div>
<div class="col"><h5>Cooking <span class="tag">1</span></h5><div class="ord"><b>#A26 · Priya S.</b><span class="dim">Cheung fun · ready 6:40 pm</span><span class="btn sm ghost">Mark ready</span></div></div>
<div class="col"><h5>Ready <span class="tag">0</span></h5><span class="dim" style="font-size:13px;padding:8px 4px">Ready orders wait here for their pickup code.</span></div></div>
<div class="two" style="margin-top:22px"><div class="panel" style="padding:18px"><div class="sech" style="margin-bottom:6px"><span class="h2" style="font-size:20px">Diners this week</span><a>Insights →</a></div><div class="chart">{"".join(f'<div class="{"t" if i == 6 else ""}" style="height:{h}%"></div>' for i, h in enumerate(bars))}</div><div class="days">{"".join(f"<span>{d}</span>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"])}</div></div>
<div class="panel" style="padding:18px"><div class="sech" style="margin-bottom:4px"><span class="h2" style="font-size:20px">Live deals</span><a>Deals →</a></div>
<div class="drow"><div style="display:grid;gap:2px;width:150px"><b>2 for 1 dim sum</b><span class="dim">9 scans today</span></div><div class="bar"><i style="width:72%"></i></div><span class="sw"></span></div>
<div class="drow"><div style="display:grid;gap:2px;width:150px"><b>Free egg tarts</b><span class="dim">5 scans today</span></div><div class="bar"><i style="width:40%"></i></div><span class="sw"></span></div>
<div class="sech" style="margin:16px 0 4px"><span class="h2" style="font-size:20px">Newest review</span><a>Reply →</a></div><div class="rev" style="border:0"><b>★★★★★ · Priya S.</b><span class="muted">The har gow were perfect and the deal came off in seconds.</span></div></div></div></div></div>''', C_CSS)
print("C mocks written")
