# Generated from fig-promo-e9's mocks (Direction A and B). Run: python site/preview/make.py
"""Static mocks for the web app redesign (user 2026-10-13): two directions x Home, Map, Restaurant page. Same brand
(webTokens: cobalt, ice, Plus Jakarta, volt sparingly), different formats. Example restaurants, like the website."""
import pathlib
OUT = pathlib.Path("C:/Promo Business/FIG-Promo/site/preview")
SITE = "/assets"
PHOTO = "/preview/img"

R = [  # name, cuisine, price, km, rating, deal, photo
    ("Golden Lantern", "Dim sum", "$$", "0.8 km", "4.7", "2 for 1 dim sum", "golden-lantern"),
    ("Seoul House", "Korean BBQ", "$$$", "1.2 km", "4.6", "20% off lunch sets", "seoul-house"),
    ("Noodle Bar", "Ramen", "$$", "1.5 km", "4.5", "Free egg with any bowl", "kinton-ramen"),
    ("Pearl Tea House", "Bubble tea", "$", "0.4 km", "4.4", "Buy 1, get 1 half price", "chatime"),
    ("Pho Corner", "Pho", "$", "2.1 km", "4.6", "$3 off a large bowl", "pho-hung"),
    ("Dumpling House", "Dumplings", "$", "1.9 km", "4.8", "Free egg tarts", "dumpling-house"),
    ("Sakura House", "Sushi", "$$", "2.4 km", "4.5", "15% off after 8 pm", "sakura-house"),
    ("Wok Bar", "Noodles", "$", "3.0 km", "4.3", "Free drink with a combo", "wok-bar"),
]
CHIPS = ["All", "Dim sum", "Ramen", "Bubble tea", "Pho", "Sushi", "Korean", "Open now", "Under $15"]
LOGO = f"{SITE}/favicon.svg"

CSS = f"""
@font-face {{ font-family: "FIG Jakarta"; src: url("{SITE}/PlusJakartaSans.woff2") format("woff2"); font-weight: 200 800; }}
:root {{ --bg:#FFFFFF; --ice:#EEF3FF; --line:#DCE4F7; --ink:#0A1020; --muted:#4B5568; --dim:#66718A; --cobalt:#1E5EFF; --volt:#C8F135; --leaf:#14C86B; --leaft:#087A42; --soft:#F6F8FD; --night:#0A1020; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "FIG Jakarta", system-ui, sans-serif; color: var(--ink); background: var(--bg); -webkit-font-smoothing: antialiased; }}
img {{ display: block; }}
.h1 {{ font-weight: 800; letter-spacing: -0.05em; line-height: 1.02; }}
.h2 {{ font-weight: 800; letter-spacing: -0.04em; line-height: 1.08; }}
.muted {{ color: var(--muted); }} .dim {{ color: var(--dim); }}
.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 48px; padding: 0 22px; border-radius: 999px; background: var(--cobalt); color: #fff; font-weight: 800; font-size: 15px; border: 0; box-shadow: 0 12px 28px rgba(30,94,255,.28); white-space: nowrap; }}
.btn.sm {{ height: 38px; padding: 0 16px; font-size: 14px; box-shadow: none; }}
.btn.ghost {{ background: #fff; color: var(--ink); border: 1px solid var(--line); box-shadow: none; }}
.chip {{ display: inline-flex; align-items: center; height: 38px; padding: 0 16px; border-radius: 999px; border: 1px solid var(--line); background: #fff; font-weight: 700; font-size: 14px; white-space: nowrap; }}
.chip.on {{ background: var(--ink); color: #fff; border-color: var(--ink); }}
.chips {{ display: flex; gap: 8px; overflow: hidden; }}
.deal {{ display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 999px; background: var(--volt); color: var(--ink); font-weight: 800; font-size: 13px; }}
.tag {{ display: inline-flex; padding: 4px 10px; border-radius: 999px; background: var(--ice); color: var(--cobalt); font-weight: 700; font-size: 12px; }}
.map {{ background: url("{SITE}/map-fallback.webp") center/cover; position: relative; overflow: hidden; }}
.pin {{ position: absolute; width: 46px; height: 46px; border-radius: 50%; border: 3px solid #fff; box-shadow: 0 8px 18px rgba(10,16,32,.28); background-size: cover; background-position: center; }}
.pin.deal-on {{ border-color: var(--volt); }} .pin.pick {{ width: 60px; height: 60px; border-color: var(--cobalt); z-index: 2; }}
.search {{ display: flex; align-items: center; gap: 10px; height: 48px; padding: 0 18px; border-radius: 999px; background: var(--soft); border: 1px solid var(--line); color: var(--dim); font-weight: 600; font-size: 15px; }}
.label {{ font-size: 13px; font-weight: 700; color: var(--dim); }}
.note {{ position: fixed; right: 12px; bottom: 10px; font-size: 11px; color: var(--dim); background: rgba(255,255,255,.9); padding: 4px 8px; border-radius: 6px; z-index: 99; }}
"""

pins_xy = [(18, 30), (34, 52), (52, 28), (64, 60), (44, 74), (76, 36), (26, 70), (84, 66)]
def pins(pick=0):
    return "".join(f'<div class="pin{" pick" if i == pick else " deal-on"}" style="left:{x}%;top:{y}%;background-image:url({PHOTO}/{r[6]}.webp)"></div>' for i, ((x, y), r) in enumerate(zip(pins_xy, R)))

def card(r, big=False):
    n, cu, pr, km, st, deal, ph = r
    return f'''<a class="card" href="rest.html"><div class="ph" style="background-image:url({PHOTO}/{ph}.webp)"><span class="deal">{deal}</span></div>
<div class="cb"><b>{n}</b><span class="dim">{cu} · {pr} · {km} · ★ {st}</span></div></a>'''

def row(r, i=0):
    n, cu, pr, km, st, deal, ph = r
    return f'''<a class="lrow{" sel" if i == 0 else ""}" href="rest.html"><div class="lph" style="background-image:url({PHOTO}/{ph}.webp)"></div>
<div class="lt"><b>{n}</b><span class="dim">{cu} · {km} · ★ {st}</span><span class="deal sm">{deal}</span></div></a>'''

FILES = {"home": "index.html", "map": "map.html", "rest": "rest.html", "owner": "owner.html"}
CRAVE = [("Dim sum", "dumpling-house"), ("Korean BBQ", "seoul-house"), ("Ramen", "kinton-ramen"), ("Bubble tea", "chatime"), ("Pho", "pho-hung"), ("Sushi", "sakura-house")]
def crave():
    return '<div class="crave">' + "".join(f'<a class="cv" href="map.html" style="background-image:url({PHOTO}/{ph}.webp)"><span>{n}</span></a>' for n, ph in CRAVE) + "</div>"
NEWP = [("Bowl Lab", "Poke bowls", "bowl-lab", "Joined this week"), ("Brew Lab", "Coffee", "brew-lab", "Joined 3 days ago"), ("Burger Co", "Burgers", "burger-co", "Joined 5 days ago"), ("Taco Stand", "Tacos", "alt-tacos", "Joined last week")]
def newp():
    return "".join(f'<a class="np" href="rest.html"><span class="lph" style="background-image:url({PHOTO}/{ph}.webp)"></span><span class="lt"><b>{n}</b><span class="dim">{c} · {w}</span></span><span class="tag">New</span></a>' for n, c, ph, w in NEWP)
def saved():
    return "".join(f'<a class="np" href="rest.html"><span class="lph" style="background-image:url({PHOTO}/{r[6]}.webp)"></span><span class="lt"><b>{r[0]}</b><span class="dim">{r[5]}</span></span><span class="heart">♥</span></a>' for r in (R[0], R[2], R[5]))
REV = [("Mia", 5, "2 days ago", "Came for the 2-for-1 and stayed for the egg tarts. They scanned my code in a second."), ("Daniel", 5, "Last week", "Best xiao long bao in Markham. Lunch for two came in under $20 with the deal."), ("Priya", 4, "2 weeks ago", "Busy on weekends, but worth it. I messaged ahead about a table for four.")]
def reviews():
    bars = "".join(f'<div class="bar"><span>{s}</span><i><em style="width:{w}%"></em></i></div>' for s, w in [(5, 78), (4, 15), (3, 5), (2, 1), (1, 1)])
    cards = "".join(f'<div class="rv"><div class="rvh"><span class="avs">{n[0]}</span><b>{n}</b><span class="stars">{"★" * s}</span><span class="dim">{d}</span></div><p class="muted">{x}</p><span class="vf">✓ Visit scanned with FIG</span></div>' for n, s, d, x in REV)
    return f'<div class="revs"><div class="rsum"><b class="big">4.7</b><span class="stars">★★★★★</span><span class="dim">128 reviews from scanned visits</span>{bars}</div><div class="rvs">{cards}</div></div>'
HOURS = [("Mon", "10 am – 9 pm"), ("Tue", "10 am – 9 pm"), ("Wed", "10 am – 9 pm"), ("Thu", "10 am – 9 pm"), ("Fri", "10 am – 10 pm"), ("Sat", "9 am – 10 pm"), ("Sun", "9 am – 9 pm")]
def hours():
    return '<div class="hrs">' + "".join(f'<div class="{"today" if d == "Tue" else ""}"><span>{d}</span><span>{h}</span></div>' for d, h in HOURS) + "</div>"
def similar():
    return f'<div class="grid">{"".join(card(r) for r in (R[5], R[3], R[6], R[7]))}</div>'
def activity():
    return '<div class="act"><div><i>🎟</i><span><b>3 deals claimed</b><br><span class="dim">You saved $24</span></span></div><div><i>★</i><span><b>2 reviews written</b><br><span class="dim">Thanks for helping others</span></span></div><div><i>💬</i><span><b>1 open chat</b><br><span class="dim">Golden Lantern replied</span></span></div></div>'
FULL_CSS = """
.crave { display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; }
.cv { height: 150px; border-radius: 20px; background-size: cover; background-position: center; position: relative; overflow: hidden; display: flex; align-items: flex-end; padding: 14px; color: #fff; font-weight: 800; font-size: 17px; transition: transform .3s; }
.cv::before { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,16,32,0) 40%, rgba(10,16,32,.75)); }
.cv span { position: relative; } .cv:hover { transform: translateY(-3px); }
.np { display: flex; align-items: center; gap: 14px; padding: 12px 0; border-bottom: 1px solid var(--line); }
.np:last-child { border-bottom: 0; }
.np .lph { width: 56px; height: 56px; border-radius: 14px; } .np .lt { flex: 1; } .np .tag { flex-shrink: 0; }
.heart { color: #E5484D; font-size: 18px; }
.box { padding: 22px; border-radius: 24px; border: 1px solid var(--line); background: #fff; }
.box h3 { font-size: 20px; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 4px; }
.three { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
.act { display: grid; gap: 14px; font-size: 14px; margin-top: 12px; } .act div { display: flex; gap: 12px; align-items: center; } .act i { width: 36px; height: 36px; border-radius: 12px; background: var(--ice); display: grid; place-items: center; font-style: normal; flex-shrink: 0; }
.revs { display: grid; grid-template-columns: 240px 1fr; gap: 24px; align-items: start; }
.rsum { display: grid; gap: 6px; padding: 20px; border-radius: 22px; background: var(--soft); border: 1px solid var(--line); }
.rsum .big { font-size: 52px; letter-spacing: -0.05em; line-height: 1; }
.bar { display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 700; } .bar i { flex: 1; height: 8px; border-radius: 99px; background: var(--line); overflow: hidden; } .bar em { display: block; height: 100%; background: var(--cobalt); }
.rvs { display: grid; gap: 14px; }
.rv { padding: 18px 20px; border-radius: 20px; border: 1px solid var(--line); display: grid; gap: 8px; background: #fff; }
.rvh { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; font-size: 14px; } .avs { width: 32px; height: 32px; border-radius: 50%; background: var(--ice); color: var(--cobalt); display: grid; place-items: center; font-weight: 800; }
.rv p { line-height: 1.6; font-size: 15px; } .vf { font-size: 12px; color: var(--leaft); font-weight: 700; }
.stars { color: #E89A00; letter-spacing: 1px; }
.hrs { display: grid; gap: 2px; font-size: 14px; margin-top: 8px; } .hrs div { display: flex; justify-content: space-between; padding: 6px 10px; border-radius: 10px; } .hrs .today { background: var(--ice); font-weight: 800; }
.pick { display: block; border-radius: 28px; overflow: hidden; background: #fff; box-shadow: 0 24px 50px rgba(10,16,32,.14); }
.pick .ph { height: 220px; background-size: cover; background-position: center; position: relative; }
.pick .ph .deal { position: absolute; left: 16px; top: 16px; }
.pick .pb { padding: 20px 22px 22px; display: grid; gap: 8px; } .pick .pb b { font-size: 22px; letter-spacing: -0.03em; }
.pick .row { display: flex; gap: 10px; margin-top: 6px; } .pick .row .btn { flex: 1; }
.hgrid { display: grid; grid-template-columns: 1fr 420px; gap: 56px; align-items: center; }
.tabp { display: none; } .tabp.on { display: block; }
.tab { cursor: pointer; user-select: none; }
@media (max-width: 700px) {
  .crave { grid-template-columns: repeat(3, 1fr); gap: 10px; } .cv { height: 100px; font-size: 14px; padding: 10px; }
  .three, .revs { grid-template-columns: 1fr; } .hgrid { grid-template-columns: 1fr; gap: 24px; } .pick .ph { height: 170px; }
}
"""
TABS_JS = '<script>document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>{document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("on",x===t));document.querySelectorAll(".tabp").forEach(p=>p.classList.toggle("on",p.dataset.t===t.dataset.t));scrollTo({top:0,behavior:"smooth"});}));</script>'

def page(name, body, extra_css):
    d, kind = name.split("-"); folder = OUT / d.lower(); folder.mkdir(parents=True, exist_ok=True)
    title = {"home": "Home", "map": "Map", "rest": "Golden Lantern", "owner": "For owners"}[kind]
    (folder / FILES[kind]).write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{title} · Direction {d} · FIG preview</title><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/preview/preview.css"><style>{CSS}{extra_css}{FULL_CSS} a {{ color: inherit; text-decoration: none; }} .cols > *, .rcols > *, .two > *, .split > * {{ min-width: 0; }} .chips {{ max-width: 100%; overflow-x: auto; scrollbar-width: none; }}</style></head><body>{body}<div class="note">Preview · example restaurants</div><script src="/preview/preview.js" defer></script></body></html>""", encoding="utf-8")

# ======================================================== Direction A: like the website (top nav, split views)
A_CSS = """
.nav { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; gap: 28px; height: 68px; padding: 0 32px; background: rgba(255,255,255,.96); border-bottom: 1px solid var(--line); }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 21px; letter-spacing: -0.03em; }
.brand img { width: 30px; height: 30px; }
.nav .search { flex: 1; max-width: 520px; height: 44px; }
.nav .links { display: flex; gap: 22px; font-weight: 700; font-size: 15px; color: var(--muted); }
.nav .links .on { color: var(--ink); }
.av { width: 40px; height: 40px; border-radius: 50%; background: var(--ice); display: grid; place-items: center; font-weight: 800; color: var(--cobalt); }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 32px; }
.hero { background: var(--ice); padding: 48px 0 40px; }
.hero .h1 { font-size: 56px; }
.hero .h1 span { color: var(--cobalt); }
.hero .chips { margin-top: 22px; flex-wrap: wrap; }
.sec { padding: 44px 0 0; }
.sech { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 18px; }
.sech .h2 { font-size: 30px; }
.sech a { color: var(--cobalt); font-weight: 800; font-size: 15px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.card { border-radius: 22px; overflow: hidden; border: 1px solid var(--line); background: #fff; }
.card .ph { height: 170px; background-size: cover; background-position: center; position: relative; }
.card .deal { position: absolute; left: 12px; bottom: 12px; }
.card .cb { padding: 14px 16px 18px; display: grid; gap: 4px; font-size: 14px; }
.card .cb b { font-size: 17px; }
.mapband { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: center; margin-top: 44px; padding: 28px; border-radius: 28px; background: var(--night); color: #fff; }
.mapband .map { height: 240px; border-radius: 20px; }
.mapband .h2 { font-size: 32px; }
.mapband p { color: #A3ADBF; margin: 10px 0 18px; line-height: 1.6; }
.launch { display: flex; gap: 12px; align-items: center; padding: 16px 20px; border-radius: 18px; background: #fff; border: 1px solid var(--line); margin-top: 22px; font-weight: 700; }
/* map: list + map split */
.split { display: grid; grid-template-columns: 440px 1fr; height: calc(100vh - 68px); }
.list { border-right: 1px solid var(--line); overflow: hidden; display: flex; flex-direction: column; }
.list .top { padding: 20px 22px 14px; display: grid; gap: 14px; border-bottom: 1px solid var(--line); }
.list .top .h2 { font-size: 26px; }
.lrow { display: flex; gap: 14px; padding: 14px 22px; border-bottom: 1px solid var(--line); }
.lrow.sel { background: var(--ice); box-shadow: inset 4px 0 0 var(--cobalt); }
.lph { width: 92px; height: 92px; border-radius: 16px; background-size: cover; background-position: center; flex-shrink: 0; }
.lt { display: grid; gap: 4px; align-content: center; font-size: 14px; }
.lt b { font-size: 17px; }
.deal.sm { padding: 4px 10px; font-size: 12px; justify-self: start; }
.split .map { height: 100%; }
.mapctl { position: absolute; right: 20px; top: 20px; display: grid; gap: 10px; z-index: 3; }
.mapctl .btn { box-shadow: 0 12px 28px rgba(30,94,255,.3); }
.zoom { display: grid; background: #fff; border-radius: 14px; border: 1px solid var(--line); overflow: hidden; justify-self: end; }
.zoom b { width: 44px; height: 44px; display: grid; place-items: center; font-size: 20px; border-bottom: 1px solid var(--line); }
.peek { position: absolute; left: 50%; bottom: 24px; transform: translateX(-50%); width: 420px; display: flex; gap: 14px; padding: 14px; border-radius: 22px; background: #fff; box-shadow: 0 24px 50px rgba(10,16,32,.18); z-index: 3; }
.peek .lph { width: 96px; height: 96px; }
.credit { position: absolute; left: 10px; bottom: 8px; font-size: 11px; color: var(--dim); background: rgba(255,255,255,.85); padding: 2px 6px; border-radius: 4px; }
/* restaurant: two columns */
.gal { display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 200px 200px; gap: 12px; margin-top: 28px; }
.gal div { border-radius: 22px; background-size: cover; background-position: center; }
.gal div:first-child { grid-row: span 2; }
.cols { display: grid; grid-template-columns: 1fr 400px; gap: 48px; padding: 32px 0 60px; }
.rname .h1 { font-size: 48px; }
.meta { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.menu { margin-top: 34px; }
.menu h3 { font-size: 22px; font-weight: 800; letter-spacing: -0.03em; margin: 26px 0 8px; }
.dish { display: flex; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: 15px; }
.dish small { display: block; color: var(--dim); font-size: 13px; margin-top: 2px; }
.side { position: sticky; top: 88px; align-self: start; display: grid; gap: 16px; }
.dcard { padding: 22px; border-radius: 24px; border: 1px solid var(--line); background: #fff; box-shadow: 0 14px 34px rgba(10,16,32,.08); display: grid; gap: 12px; }
.dcard.hot { border: 2px solid var(--cobalt); }
.dcard b { font-size: 19px; }
.mini { height: 160px; border-radius: 20px; }
/* phone width */
@media (max-width: 700px) {
  .nav { gap: 12px; padding: 0 16px; height: 60px; } .nav .links, .nav .search { display: none; } .nav .grow { flex: 1; }
  .wrap { padding: 0 16px; } .hero { padding: 28px 0 24px; } .hero .h1 { font-size: 38px; }
  .grid { grid-template-columns: 1fr 1fr; gap: 12px; } .card .ph { height: 120px; } .card .cb b { font-size: 15px; }
  .mapband { grid-template-columns: 1fr; padding: 20px; } .mapband .map { height: 180px; }
  .split { grid-template-columns: 1fr; grid-template-rows: 46vh 1fr; height: calc(100vh - 60px); } .split .map { order: -1; } .list .top .h2 { font-size: 22px; }
  .peek { display: none; } .lph { width: 76px; height: 76px; }
  .gal { grid-template-columns: 1fr; grid-template-rows: 220px; } .gal div:not(:first-child) { display: none; } .gal div:first-child { grid-row: auto; }
  .cols { grid-template-columns: 1fr; gap: 24px; } .side { position: static; order: -1; } .rname .h1 { font-size: 34px; }
  .bottombar { display: flex !important; }
}
.bottombar { display: none; position: fixed; left: 0; right: 0; bottom: 0; height: 64px; background: #fff; border-top: 1px solid var(--line); justify-content: space-around; align-items: center; font-weight: 700; font-size: 12px; color: var(--dim); z-index: 20; }
.bottombar .on { color: var(--cobalt); }
"""
def a_nav(on):
    links = "".join(f'<a {"href=\"./\"" if x == "Home" else "href=\"map.html\"" if x in ("Map", "Search") else ""} class="{"on" if x == on else ""}">{x}</a>' for x in ["Home", "Map", "Deals", "Saved", "Chats"])
    return f'''<div class="nav"><a class="brand" href="/preview/"><img src="{LOGO}" alt="">FIG</a><div class="search">⌕&nbsp; Search dishes, restaurants…</div><div class="grow"></div><div class="links">{links}</div><div class="av">A</div></div>
<div class="bottombar">{"".join(f'<a {"href=\"./\"" if x == "Home" else "href=\"map.html\"" if x in ("Map", "Search") else ""} class="{"on" if x == on else ""}">{x}</a>' for x in ["Home", "Map", "Deals", "Saved", "Account"])}</div>'''

chips = lambda on="All": '<div class="chips">' + "".join(f'<span class="chip{" on" if c == on else ""}">{c}</span>' for c in CHIPS) + "</div>"
page("A-home", a_nav("Home") + f'''
<div class="hero"><div class="wrap hgrid"><div><div class="h1">Good evening, Alex.<br><span>Where are we eating?</span></div>
<div class="search" style="margin-top:22px;max-width:640px;background:#fff">⌕&nbsp; Dim sum, ramen, bubble tea…</div>{chips()}</div><a class="pick" href="rest.html"><div class="ph" style="background-image:url({PHOTO}/golden-lantern.webp)"><span class="deal">Tonight's pick</span></div><div class="pb"><span class="label">Golden Lantern · Dim sum · 0.8 km</span><b>2 for 1 dim sum</b><span class="muted">Any two steamed baskets, the second free. Until 9 pm.</span><div class="row"><span class="btn">Claim</span><span class="btn ghost">See the menu</span></div></div></a></div></div>
<div class="wrap"><div class="sec"><div class="sech"><span class="h2">Live now near you</span><a href="map.html">See all deals →</a></div>
<div class="grid">{"".join(card(r) for r in R[:4])}</div></div>
<div class="sec"><div class="sech"><span class="h2">What are you craving?</span><a href="map.html">All cuisines →</a></div>{crave()}</div>
<div class="mapband"><div><span class="h2">8 places on the map</span><p>See every deal around Markham. Pins with a green ring have a deal on right now.</p><a class="btn" href="map.html">Open the map</a></div><div class="map">{pins(-1)}</div></div>
<div class="sec"><div class="sech"><span class="h2">On FIG in Markham</span><a href="map.html">See all →</a></div><div class="grid">{"".join(card(r) for r in R[4:8])}</div>
<div class="sec three"><div class="box"><h3>New on FIG</h3><p class="dim" style="font-size:14px">Places that just joined</p>{newp()}</div>
<div class="box"><h3>Your saved places</h3><p class="dim" style="font-size:14px">We'll tell you when they post a deal</p>{saved()}</div>
<div class="box"><h3>Your FIG</h3><p class="dim" style="font-size:14px">This month</p>{activity()}</div></div>
<div class="launch"><span class="deal">Jan 1, 2027</span>FIG opens in Markham. Save places now and you'll see their first deals here.</div></div><div style="height:80px"></div></div>''', A_CSS)

page("A-map", a_nav("Map") + f'''<div class="split"><div class="list"><div class="top"><span class="h2">8 places near Markham</span>{chips("All")}<span class="label">Nearest first · 5 with a deal now</span></div>
{"".join(row(r, i) for i, r in enumerate(R[:6]))}</div>
<div class="map">{pins(0)}<div class="mapctl"><span class="btn">◎&nbsp; Use my location</span><div class="zoom"><b>+</b><b style="border:0">−</b></div></div>
<div class="peek">{row(R[0]).replace('lrow sel', 'lt0')}<span class="btn sm" style="align-self:center">Claim</span></div><span class="credit">© OpenMapTiles © OpenStreetMap</span></div></div>''', A_CSS)

g = R[0]
page("A-rest", a_nav("Home") + f'''<div class="wrap"><div class="gal"><div style="background-image:url({PHOTO}/golden-lantern.webp)"></div><div style="background-image:url({PHOTO}/dumpling-house.webp)"></div><div style="background-image:url({PHOTO}/alt-hotpot.webp)"></div></div>
<div class="cols"><div><div class="rname"><span class="h1">Golden Lantern</span><div class="meta"><span class="tag">Dim sum</span><span class="tag">$$</span><span class="tag">★ 4.7 · 128 reviews</span><span class="tag" style="background:#E7F8EF;color:var(--leaft)">Open until 9 pm</span></div>
<p class="muted" style="margin-top:16px;line-height:1.6;max-width:620px">Cantonese dim sum, steamed to order. 4350 Steeles Ave E, Markham · 0.8 km away.</p></div>
<div class="menu"><span class="h2" style="font-size:28px">Menu</span><div class="chips" style="margin-top:14px"><span class="chip on">Steamed</span><span class="chip">Baked</span><span class="chip">Rice & noodles</span><span class="chip">Drinks</span></div>
<h3>Steamed</h3><div class="dish"><span>Har gow<small>4 pieces · shrimp</small></span><b>$7.50</b></div><div class="dish"><span>Siu mai<small>4 pieces · pork & shrimp</small></span><b>$6.95</b></div><div class="dish"><span>Cheung fun<small>Rice rolls, beef</small></span><b>$8.25</b></div>
<h3>Baked</h3><div class="dish"><span>Egg tarts<small>3 pieces</small></span><b>$6.50</b></div><div class="dish"><span>Char siu bao<small>3 pieces · BBQ pork</small></span><b>$6.25</b></div>
<h3>Rice & noodles</h3><div class="dish"><span>Sticky rice in lotus leaf<small>2 pieces</small></span><b>$7.95</b></div><div class="dish"><span>Beef chow fun<small>Wok-fried, bean sprouts</small></span><b>$14.50</b></div></div>
<div class="menu"><span class="h2" style="font-size:28px">Reviews</span><div style="margin-top:16px">{reviews()}</div></div></div>
<div class="side"><div class="dcard hot"><span class="deal" style="justify-self:start">Deal · today until 9 pm</span><b>2 for 1 dim sum</b><span class="muted" style="font-size:14px;line-height:1.5">Any two steamed baskets, the second free. Dine in or takeout.</span><span class="btn">Claim this deal</span><span class="btn ghost">Order takeout</span></div>
<div class="dcard"><b>Free egg tarts</b><span class="muted" style="font-size:14px">Mon–Thu · with any order</span><span class="btn ghost sm">Claim</span></div>
<div class="box"><h3>Hours</h3>{hours()}<p class="dim" style="font-size:13px;margin-top:10px">(905) 555-0142 · 4350 Steeles Ave E</p></div><div class="map mini">{pins(0)}</div><span class="btn ghost">💬 Message Golden Lantern</span></div></div>
<div class="sec" style="padding-bottom:70px"><div class="sech"><span class="h2">Similar places nearby</span><a href="map.html">See on the map →</a></div>{similar()}</div></div>''', A_CSS)

# ======================================================== Direction B: a web dashboard (sidebar, map-first, banner + tabs)
B_CSS = """
.app { display: grid; grid-template-columns: 248px 1fr; min-height: 100vh; }
.side { background: var(--night); color: #F4F6FB; padding: 22px 16px; display: flex; flex-direction: column; gap: 4px; position: sticky; top: 0; height: 100vh; }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 21px; padding: 0 10px 22px; }
.brand img { width: 30px; height: 30px; }
.navi { display: flex; align-items: center; gap: 12px; height: 46px; padding: 0 14px; border-radius: 14px; color: #A3ADBF; font-weight: 700; font-size: 15px; }
.navi.on { background: var(--cobalt); color: #fff; }
.navi i { width: 20px; text-align: center; font-style: normal; }
.side .grow { flex: 1; }
.qr { padding: 14px; border-radius: 16px; background: #141A2B; display: flex; gap: 12px; align-items: center; font-size: 12px; color: #A3ADBF; line-height: 1.4; }
.qr img { width: 56px; height: 56px; background: #fff; border-radius: 8px; padding: 4px; }
.main { min-width: 0; }
.topb { display: flex; align-items: center; gap: 16px; height: 72px; padding: 0 32px; border-bottom: 1px solid var(--line); background: #fff; position: sticky; top: 0; z-index: 5; }
.topb .search { flex: 1; max-width: 560px; }
.av { width: 40px; height: 40px; border-radius: 50%; background: var(--ice); display: grid; place-items: center; font-weight: 800; color: var(--cobalt); margin-left: auto; }
.body { padding: 28px 32px 60px; }
.greet .h1 { font-size: 40px; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 22px 0 28px; }
.stat { padding: 18px 20px; border-radius: 20px; background: var(--soft); border: 1px solid var(--line); display: grid; gap: 4px; }
.stat b { font-size: 28px; letter-spacing: -0.04em; }
.stat.c { background: var(--cobalt); color: #fff; border-color: var(--cobalt); } .stat.c .dim { color: #DDE7FF; }
.sech { display: flex; align-items: baseline; justify-content: space-between; margin: 26px 0 14px; } .sech .h2 { font-size: 24px; } .sech a { color: var(--cobalt); font-weight: 800; font-size: 14px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.card { border-radius: 18px; overflow: hidden; border: 1px solid var(--line); background: #fff; }
.card .ph { height: 130px; background-size: cover; background-position: center; position: relative; }
.card .deal { position: absolute; left: 10px; bottom: 10px; font-size: 12px; padding: 5px 10px; }
.card .cb { padding: 12px 14px 14px; display: grid; gap: 3px; font-size: 13px; } .card .cb b { font-size: 15px; }
.two { display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px; }
.panel { border-radius: 22px; border: 1px solid var(--line); overflow: hidden; background: #fff; }
.panel .map { height: 300px; }
.lrow { display: flex; gap: 12px; padding: 12px 16px; border-bottom: 1px solid var(--line); align-items: center; }
.lrow.sel { background: var(--ice); }
.lph { width: 64px; height: 64px; border-radius: 14px; background-size: cover; background-position: center; flex-shrink: 0; }
.lt { display: grid; gap: 3px; font-size: 13px; } .lt b { font-size: 15px; }
.deal.sm { padding: 3px 9px; font-size: 11px; justify-self: start; }
/* map-first */
.full { position: relative; height: calc(100vh - 72px); }
.full .map { position: absolute; inset: 0; }
.float { position: absolute; left: 24px; top: 24px; bottom: 24px; width: 380px; background: #fff; border-radius: 26px; box-shadow: 0 24px 50px rgba(10,16,32,.18); display: flex; flex-direction: column; overflow: hidden; z-index: 3; }
.float .top { padding: 18px 18px 12px; display: grid; gap: 12px; border-bottom: 1px solid var(--line); }
.float .top .h2 { font-size: 22px; }
.chipsf { position: absolute; left: 428px; right: 24px; top: 24px; z-index: 3; }
.chipsf .chip { box-shadow: 0 8px 20px rgba(10,16,32,.10); }
.mapctl { position: absolute; right: 24px; bottom: 24px; display: grid; gap: 10px; justify-items: end; z-index: 3; }
.zoom { display: grid; background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 20px rgba(10,16,32,.12); }
.zoom b { width: 44px; height: 44px; display: grid; place-items: center; font-size: 20px; border-bottom: 1px solid var(--line); }
.credit { position: absolute; left: 428px; bottom: 8px; font-size: 11px; color: var(--dim); background: rgba(255,255,255,.85); padding: 2px 6px; border-radius: 4px; z-index: 3; }
/* banner + tabs */
.banner { height: 300px; position: relative; background-size: cover; background-position: center; }
.banner::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,16,32,0) 30%, rgba(10,16,32,.78)); }
.btext { position: absolute; left: 32px; bottom: 26px; right: 32px; color: #fff; z-index: 2; display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; }
.btext .h1 { font-size: 46px; } .btext span { color: #DDE7FF; font-weight: 600; }
.tabs { display: flex; gap: 6px; padding: 0 32px; border-bottom: 1px solid var(--line); background: #fff; position: sticky; top: 72px; z-index: 4; }
.tab { padding: 16px 14px; font-weight: 800; font-size: 15px; color: var(--dim); border-bottom: 3px solid transparent; }
.tab.on { color: var(--ink); border-color: var(--cobalt); }
.rcols { display: grid; grid-template-columns: 1fr 360px; gap: 28px; }
.dgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.dcard { padding: 20px; border-radius: 22px; border: 1px solid var(--line); display: grid; gap: 10px; background: #fff; }
.dcard.hot { background: var(--night); color: #fff; border-color: var(--night); } .dcard.hot .muted { color: #A3ADBF; }
.dcard b { font-size: 18px; }
.info { padding: 20px; border-radius: 22px; background: var(--soft); border: 1px solid var(--line); display: grid; gap: 12px; font-size: 14px; }
.info .map { height: 150px; border-radius: 16px; }
.dish { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
/* phone width: the sidebar becomes a bottom bar */
.bottombar { display: none; }
@media (max-width: 700px) {
  .app { grid-template-columns: 1fr; } .side { display: none; }
  .bottombar { display: flex; position: fixed; left: 0; right: 0; bottom: 0; height: 66px; background: var(--night); justify-content: space-around; align-items: center; color: #A3ADBF; font-weight: 700; font-size: 12px; z-index: 20; }
  .bottombar .on { color: #fff; background: var(--cobalt); padding: 8px 14px; border-radius: 999px; }
  .topb { padding: 0 16px; height: 64px; } .body { padding: 20px 16px 90px; } .greet .h1 { font-size: 30px; }
  .stats { grid-template-columns: 1fr 1fr; } .grid { grid-template-columns: 1fr 1fr; } .two { grid-template-columns: 1fr; }
  .full { height: calc(100vh - 64px - 66px); } .float { left: 0; right: 0; top: auto; bottom: 0; width: auto; height: 44%; border-radius: 26px 26px 0 0; }
  .chipsf { left: 16px; right: 16px; top: 14px; } .credit { left: 8px; bottom: 46%; } .mapctl { bottom: calc(44% + 14px); right: 14px; }
  .banner { height: 220px; } .btext { left: 16px; right: 16px; flex-direction: column; align-items: flex-start; } .btext .h1 { font-size: 32px; }
  .tabs { padding: 0 8px; top: 64px; } .rcols, .dgrid { grid-template-columns: 1fr; }
}
"""
def b_shell(on, inner, top=True):
    nav = "".join(f'<a {"href=\"./\"" if x == "Home" else "href=\"map.html\"" if x in ("Map", "Search") else ""} class="navi{" on" if x == on else ""}"><i>{ic}</i>{x}</a>' for x, ic in [("Home", "⌂"), ("Search", "⌕"), ("Map", "◫"), ("Deals", "✦"), ("Saved", "♡"), ("Chats", "✉"), ("Account", "◯")])
    bar = "".join(f'<a {"href=\"./\"" if x == "Home" else "href=\"map.html\"" if x in ("Map", "Search") else ""} class="{"on" if x == on else ""}">{x}</a>' for x in ["Home", "Map", "Deals", "Chats", "Account"])
    tb = f'<div class="topb"><div class="search">⌕&nbsp; Search dishes, restaurants…</div><span class="btn sm ghost">Markham ▾</span><div class="av">A</div></div>' if top else ""
    return f'''<div class="app"><aside class="side"><a class="brand" href="/preview/"><img src="{LOGO}" alt="">FIG</a>{nav}<div class="grow"></div>
<div class="qr"><img src="{SITE}/qr-app.svg">Better on your phone. Scan to open FIG there.</div></aside><div class="main">{tb}{inner}</div></div><div class="bottombar">{bar}</div>'''

page("B-home", b_shell("Home", f'''<div class="body"><div class="greet"><span class="h1">Good evening, Alex</span><p class="muted" style="margin-top:6px">Markham · Tuesday 6:42 pm</p></div>
<div class="stats"><div class="stat c"><span class="dim">Live deals near you</span><b>5</b></div><div class="stat"><span class="dim">Places on FIG</span><b>8</b></div><div class="stat"><span class="dim">Saved</span><b>3</b></div><div class="stat"><span class="dim">You've saved</span><b>$24</b></div></div>
<div class="chips">{"".join(f'<span class="chip{" on" if c == "All" else ""}">{c}</span>' for c in CHIPS)}</div>
<div class="sech"><span class="h2">Live now</span><a href="map.html">All deals →</a></div><div class="grid">{"".join(card(r) for r in R[:4])}</div>
<div class="sech"><span class="h2">Around you</span><a href="map.html">Open the map →</a></div>
<div class="two"><div class="panel"><div class="map">{pins(0)}</div></div><div class="panel">{"".join(row(r, i) for i, r in enumerate(R[:4]))}</div></div>
<div class="sech"><span class="h2">What are you craving?</span><a href="map.html">All cuisines →</a></div>{crave()}
<div class="three" style="margin-top:26px"><div class="box"><h3>New on FIG</h3><p class="dim" style="font-size:14px">Places that just joined</p>{newp()}</div><div class="box"><h3>Saved</h3><p class="dim" style="font-size:14px">We'll tell you when they post a deal</p>{saved()}</div><div class="box"><h3>Your FIG</h3><p class="dim" style="font-size:14px">This month</p>{activity()}</div></div></div>'''), B_CSS)

page("B-map", b_shell("Map", f'''<div class="full"><div class="map">{pins(0)}</div>
<div class="chipsf"><div class="chips">{"".join(f'<span class="chip{" on" if c == "All" else ""}">{c}</span>' for c in CHIPS)}</div></div>
<div class="float"><div class="top"><span class="h2">8 places near you</span><span class="dim" style="font-size:13px">5 with a deal now · nearest first</span></div>{"".join(row(r, i) for i, r in enumerate(R[:7]))}</div>
<div class="mapctl"><span class="btn">◎&nbsp; Use my location</span><div class="zoom"><b>+</b><b style="border:0">−</b></div></div><span class="credit">© OpenMapTiles © OpenStreetMap</span></div>'''), B_CSS)

page("B-rest", b_shell("Home", f'''<div class="banner" style="background-image:url({PHOTO}/golden-lantern.webp)"><div class="btext"><div><span class="h1">Golden Lantern</span><br><span>Dim sum · $$ · ★ 4.7 (128) · 0.8 km · Open until 9 pm</span></div><span class="btn">♡&nbsp; Save</span></div></div>
<div class="tabs"><span class="tab on" data-t="d">Deals</span><span class="tab" data-t="m">Menu</span><span class="tab" data-t="r">Reviews (128)</span><span class="tab" data-t="i">Info</span></div>
<div class="body"><div class="rcols"><div><div class="tabp on" data-t="d"><div class="dgrid"><div class="dcard hot"><span class="deal" style="justify-self:start">Today until 9 pm</span><b>2 for 1 dim sum</b><span class="muted" style="font-size:14px;line-height:1.5">Any two steamed baskets, the second free. Dine in or takeout.</span><span class="btn">Claim</span></div>
<div class="dcard"><span class="tag" style="justify-self:start">Mon–Thu</span><b>Free egg tarts</b><span class="muted" style="font-size:14px">With any order</span><span class="btn ghost">Claim</span></div></div>
<div class="sech"><span class="h2">Popular on the menu</span><a>Full menu →</a></div><div class="dish"><span>Har gow · 4 pieces</span><b>$7.50</b></div><div class="dish"><span>Siu mai · 4 pieces</span><b>$6.95</b></div><div class="dish"><span>Egg tarts · 3 pieces</span><b>$6.50</b></div>
<div class="sech"><span class="h2">What people say</span><a>All reviews →</a></div>{reviews()}</div>
<div class="tabp" data-t="m"><div class="sech" style="margin-top:0"><span class="h2">Steamed</span></div><div class="dish"><span>Har gow · 4 pieces</span><b>$7.50</b></div><div class="dish"><span>Siu mai · 4 pieces</span><b>$6.95</b></div><div class="dish"><span>Cheung fun · beef</span><b>$8.25</b></div><div class="dish"><span>Xiao long bao · 6 pieces</span><b>$8.95</b></div>
<div class="sech"><span class="h2">Baked</span></div><div class="dish"><span>Egg tarts · 3 pieces</span><b>$6.50</b></div><div class="dish"><span>Char siu bao · 3 pieces</span><b>$6.25</b></div>
<div class="sech"><span class="h2">Rice & noodles</span></div><div class="dish"><span>Sticky rice in lotus leaf</span><b>$7.95</b></div><div class="dish"><span>Beef chow fun</span><b>$14.50</b></div></div>
<div class="tabp" data-t="r">{reviews()}</div>
<div class="tabp" data-t="i"><div class="box"><h3>Hours</h3>{hours()}</div><div class="box" style="margin-top:14px"><h3>Good to know</h3><p class="muted" style="line-height:1.7">Halal options · Takeout · Groups welcome · Wheelchair access · Card and cash</p></div></div>
<div class="sech"><span class="h2">Similar places nearby</span><a href="map.html">See on the map →</a></div>{similar()}</div>
<div class="info"><b style="font-size:17px">Info</b><span class="muted">4350 Steeles Ave E, Markham</span><span class="muted">Daily 10 am – 9 pm · (905) 555-0142</span><div class="map">{pins(0)}</div><span class="btn ghost">Directions</span><span class="btn ghost">💬 Message</span></div></div></div>''' + TABS_JS, top=True), B_CSS)
print("6 mocks written to", OUT)
