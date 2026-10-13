# Direction C, "enhanced with images" (user via d7, 2026-10-13: "more enhanced like with images but make it look natural"):
# Home and the restaurant page with real food photography from the responsive pipeline (site/scripts/images.py:
# webp + jpg srcset, width/height, colour placeholders, lazy below the fold). Run after make_c.py.
import contextlib, io, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from images import picture  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import make_c as c  # noqa: E402  (rebuilds A, B, C)
m, nav, C_CSS, FLIP, chips = c.m, c.nav, c.C_CSS, c.FLIP, c.chips

PLUS_CSS = """
.ph { position: relative; overflow: hidden; border-radius: 24px; } .ph picture, .ph img { display: block; width: 100%; height: 100%; object-fit: cover; }
.ph img { transition: transform .6s cubic-bezier(.22,1,.36,1); } a:hover .ph img { transform: scale(1.04); }
.xhero { position: relative; padding: 44px 0 56px; background: linear-gradient(180deg, var(--ice), #fff); }
.xg { display: grid; grid-template-columns: 1fr 560px; gap: 48px; align-items: center; }
.xg .h1 { font-size: 54px; } .xg .h1 span { color: var(--cobalt); }
.xg .search { margin-top: 20px; background: #fff; height: 54px; max-width: 600px; box-shadow: 0 10px 30px rgba(10,16,32,.06); }
.xg .chips { margin-top: 16px; flex-wrap: wrap; }
.mosaic { position: relative; height: 470px; }
.mosaic .ph { position: absolute; box-shadow: 0 30px 60px rgba(10,16,32,.18); }
.mosaic .m1 { left: 0; top: 0; width: 330px; height: 300px; } .mosaic .m2 { right: 0; top: 50px; width: 240px; height: 200px; } .mosaic .m3 { right: 40px; bottom: 0; width: 300px; height: 200px; } .mosaic .m4 { left: 30px; bottom: 10px; width: 180px; height: 140px; }
.sticker { position: absolute; z-index: 3; display: grid; gap: 2px; padding: 12px 16px; border-radius: 18px; background: #fff; box-shadow: 0 18px 40px rgba(10,16,32,.16); font-size: 13px; }
.sticker b { font-size: 16px; } .sticker.s1 { left: 250px; top: 236px; } .sticker.s2 { right: 10px; top: 4px; background: var(--volt); }
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 34px; }
.pcard { display: grid; gap: 12px; } .pcard .ph { aspect-ratio: 4 / 3; } .pcard .ph .deal { position: absolute; left: 12px; top: 12px; z-index: 2; }
.pcard b { font-size: 17px; } .pcard .dim { font-size: 14px; }
.cgrid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }
.crav { display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; }
.crav a { display: grid; gap: 10px; justify-items: center; font-weight: 800; font-size: 15px; } .crav .ph { width: 100%; aspect-ratio: 1; border-radius: 50%; }
.band { position: relative; margin-top: 56px; border-radius: 32px; overflow: hidden; height: 360px; color: #fff; }
.band .ph { position: absolute; inset: 0; border-radius: 0; } .band::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(10,16,32,.82), rgba(10,16,32,.15) 70%); }
.band .bt { position: absolute; z-index: 2; left: 48px; top: 50%; transform: translateY(-50%); max-width: 460px; display: grid; gap: 14px; }
.band .bt .h2 { font-size: 40px; } .band .bt p { color: #DDE3EE; line-height: 1.6; }
.xrest-hero { position: relative; height: 460px; color: #fff; }
.xrest-hero .ph { position: absolute; inset: 0; border-radius: 0; } .xrest-hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,16,32,.05) 30%, rgba(10,16,32,.8)); }
.xrest-hero .wrap { position: relative; z-index: 2; height: 100%; padding-top: 28px; display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; padding-bottom: 36px; }
.xrest-hero .h1 { font-size: 60px; } .xrest-hero .meta2 { display: flex; flex-wrap: wrap; gap: 14px; color: #DDE3EE; font-weight: 600; margin-top: 8px; }
.strip { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: -40px; position: relative; z-index: 3; } .strip .ph { aspect-ratio: 4 / 3; border: 4px solid #fff; box-shadow: 0 14px 30px rgba(10,16,32,.14); border-radius: 20px; }
.xcols { display: grid; grid-template-columns: 1fr 380px; gap: 44px; padding: 36px 0 70px; }
.dishes { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.dishc { display: flex; gap: 14px; align-items: center; padding: 12px; border: 1px solid var(--line); border-radius: 20px; }
.dishc .ph { width: 96px; height: 96px; flex-shrink: 0; border-radius: 16px; } .dishc div { display: grid; gap: 4px; } .dishc small { color: var(--dim); }
.xclaim { position: sticky; top: 90px; display: grid; gap: 12px; padding: 22px; border-radius: 26px; border: 2px solid var(--cobalt); background: #fff; box-shadow: 0 24px 50px rgba(10,16,32,.10); }
.xclaim .ph { aspect-ratio: 16 / 9; } .xclaim b { font-size: 22px; letter-spacing: -0.03em; }
@media (max-width: 700px) {
  .xg { grid-template-columns: 1fr; gap: 26px; } .xg .h1 { font-size: 36px; } .mosaic { height: 300px; } .mosaic .m1 { width: 62%; height: 200px; } .mosaic .m2 { width: 42%; height: 140px; top: 30px; } .mosaic .m3 { width: 55%; height: 130px; right: 0; } .mosaic .m4 { display: none; } .sticker.s1 { left: 34%; top: 168px; }
  .stat-row { grid-template-columns: 1fr 1fr; } .cgrid { grid-template-columns: 1fr 1fr; gap: 14px; } .crav { grid-template-columns: repeat(3, 1fr); }
  .band { height: 300px; border-radius: 24px; } .band .bt { left: 22px; right: 22px; } .band .bt .h2 { font-size: 28px; }
  .xrest-hero { height: 340px; } .xrest-hero .h1 { font-size: 38px; } .xrest-hero .wrap { flex-direction: column; align-items: flex-start; }
  .strip { grid-template-columns: repeat(3, 1fr); margin-top: 14px; } .strip a:nth-child(n+4) { display: none; }
  .xcols { grid-template-columns: 1fr; gap: 26px; } .dishes { grid-template-columns: 1fr; } .xclaim { position: static; }
}
"""
P = lambda name, alt, sizes, eager=False: picture(name, alt, sizes, eager=eager)
PLACES = [("Golden Lantern", "Dim sum", "0.8 km", "4.7", "2 for 1 dim sum", "dim-sum"), ("Seoul House", "Korean BBQ", "1.2 km", "4.6", "20% off lunch sets", "korean-bbq"),
          ("Noodle Bar", "Ramen", "1.5 km", "4.5", "Free egg with any bowl", "ramen"), ("Pearl Tea House", "Bubble tea", "0.4 km", "4.4", "Buy 1, get 1 half price", "bubble-tea"),
          ("Pho Corner", "Pho", "2.1 km", "4.6", "$3 off a large bowl", "pho"), ("Dumpling House", "Dumplings", "1.9 km", "4.8", "Free egg tarts", "dumplings"),
          ("Sakura House", "Sushi", "2.4 km", "4.5", "15% off after 8 pm", "sushi"), ("Brew Lab", "Coffee", "1.0 km", "4.9", "2-for-1 lattes", "coffee")]
def pcard(p):
    n, cu, km, st, deal, img = p
    return f'<a class="pcard" href="rest-plus.html"><div class="ph">{P(img, n + ", " + cu, "(min-width: 1000px) 300px, 45vw")}<span class="deal">{deal}</span></div><div style="display:grid;gap:3px"><b>{n}</b><span class="dim">{cu} · {km} · ★ {st}</span></div></a>'

hero = f'''<div class="xhero"><div class="wrap xg"><div><div class="h1">Good evening, Alex.<br><span>Where are we eating?</span></div>
<div class="search">⌕&nbsp; Dim sum, ramen, bubble tea…</div>{chips()}</div>
<div class="mosaic"><a class="ph m1" href="rest-plus.html">{P("dim-sum", "Dim sum in a bamboo steamer", "330px", eager=True)}</a><div class="ph m2">{P("bubble-tea", "Bubble tea", "240px")}</div><div class="ph m3">{P("korean-bbq", "Korean BBQ on the grill", "300px")}</div><div class="ph m4">{P("ramen", "Ramen", "180px")}</div>
<div class="sticker s1"><span class="dim">Golden Lantern · 0.8 km</span><b>2 for 1 dim sum</b></div><div class="sticker s2"><b>5 deals live</b><span>near you tonight</span></div></div></div>
<div class="wrap"><div class="stat-row"><div class="tile c"><span class="dim">Live deals near you</span><b>5</b></div><div class="tile"><span class="dim">Places on FIG nearby</span><b>8</b></div><div class="tile"><span class="dim">Your saved places</span><b>3</b></div><div class="tile n"><span class="dim">You've saved with FIG</span><b>$24</b></div></div></div></div>'''
crav = "".join(f'<a href="map.html"><div class="ph">{P(img, n, "(min-width: 1000px) 180px, 30vw")}</div>{n}</a>' for n, img in [("Dim sum", "dim-sum"), ("Ramen", "ramen"), ("Bubble tea", "bubble-tea"), ("Pho", "pho"), ("Sushi", "sushi"), ("Korean BBQ", "korean-bbq")])
m.page("C-homeplus", FLIP + nav("Home") + hero + f'''<div class="wrap">
<div class="sec"><div class="sech"><span class="h2">Live now near you</span><a href="map.html">All deals →</a></div><div class="cgrid">{"".join(pcard(p) for p in PLACES[:4])}</div></div>
<div class="sec"><div class="sech"><span class="h2">What are you craving?</span><a href="map.html">All cuisines →</a></div><div class="crav">{crav}</div></div>
<div class="band"><div class="ph">{P("korean-bbq", "Korean BBQ on a shared grill", "(min-width: 1000px) 1220px, 100vw")}</div><div class="bt"><span class="h2">Dinner for four, sorted.</span><p>Send the group a few places, everyone taps a favourite, and FIG picks where you're going.</p><a class="btn" href="map.html" style="justify-self:start">Plan with friends</a></div></div>
<div class="sec"><div class="sech"><span class="h2">On FIG in Markham</span><a href="map.html">See the map →</a></div><div class="cgrid">{"".join(pcard(p) for p in PLACES[4:])}</div></div>
<div class="launch"><span class="deal">Jan 1, 2027</span>FIG opens in Markham. Save places now and their first deals show up here.</div><div style="height:70px"></div></div>''', C_CSS + PLUS_CSS)

strip = "".join(f'<a class="ph" href="#">{P(i, a, "(min-width: 1000px) 240px, 30vw")}</a>' for i, a in [("dumplings", "Dumplings"), ("dim-sum", "Xiao long bao"), ("noodles", "Noodles"), ("wok", "Wok-fried beef"), ("bowls", "A rice bowl")])
dishes = "".join(f'<div class="dishc"><div class="ph">{P(i, n, "96px")}</div><div><b>{n}</b><small>{d}</small><b style="color:var(--cobalt)">{pr}</b></div></div>' for n, d, pr, i in [("Xiao long bao", "6 pieces · pork soup dumplings", "$8.95", "dim-sum"), ("Har gow", "4 pieces · shrimp", "$7.50", "dumplings"), ("Beef chow fun", "Wok-fried, bean sprouts", "$14.50", "wok"), ("Dan dan noodles", "Sesame, chili, pork", "$12.95", "noodles")])
m.page("C-restplus", FLIP + nav("Home") + f'''<div class="xrest-hero"><div class="ph">{P("dim-sum", "Golden Lantern's dim sum", "100vw", eager=True)}</div><div class="wrap"><div><span class="deal">Deal today until 9 pm</span><div class="h1" style="margin-top:12px">Golden Lantern</div>
<div class="meta2"><span>Dim sum · $$</span><span>★ 4.7 (128)</span><span>0.8 km</span><span>Open until 9 pm</span></div></div><span class="btn ghost">♡ Save</span></div></div>
<div class="wrap"><div class="strip">{strip}</div><div class="xcols"><div>
<div class="sech"><span class="h2" style="font-size:28px">Popular dishes</span><a>Full menu →</a></div><div class="dishes">{dishes}</div>
<div class="sech" style="margin-top:36px"><span class="h2" style="font-size:28px">Reviews</span><a>All 128 →</a></div>{c.m.reviews() if hasattr(c.m, "reviews") else ""}
<div class="sech" style="margin-top:36px"><span class="h2" style="font-size:28px">Similar places</span></div><div class="cgrid" style="grid-template-columns:repeat(3,1fr)">{"".join(pcard(p) for p in [PLACES[5], PLACES[2], PLACES[4]])}</div></div>
<aside><div class="xclaim"><div class="ph">{P("dumplings", "Steamed baskets", "380px")}</div><span class="deal" style="justify-self:start">Today until 9 pm</span><b>2 for 1 dim sum</b><span class="muted" style="font-size:14px;line-height:1.5">Any two steamed baskets, the second free. Claim it, then show your code at the counter.</span><span class="btn">Claim this deal</span><span class="btn ghost">Order takeout</span>
<span class="dim" style="font-size:13px">Daily 10 am – 9 pm · 4350 Steeles Ave E, Markham</span></div></aside></div></div>''', C_CSS + PLUS_CSS)
print("C enhanced written")
