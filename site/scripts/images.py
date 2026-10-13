"""Responsive photos for the website and the web app: credited source photos -> site/assets/img/<name>-<w>.<hash>.webp/.jpg
at 480 / 800 / 1200 px wide, plus site/assets/img/manifest.json (sizes, the placeholder colour, the credit) for srcset,
width/height and a colour placeholder. Hashed names, so vercel.json caches /assets/img for a year.
Only photos with a credit line are built (CREDITS below); anything else is refused.
Run: python site/scripts/images.py   (re-run after adding a photo; old files are removed)"""
import hashlib, io, json, pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "Media Assets" / "Assets" / "website" / "food"
OUT = ROOT / "site" / "assets" / "img"
WIDTHS = (480, 800, 1200)
BUDGET = {480: 45_000, 800: 95_000, 1200: 180_000}  # bytes per webp; the build fails above this
RATIO = 4 / 3  # every photo is cropped to 4:3 so cards never shift

# name: (source file, credit). Unsplash License: free for commercial use, no attribution required.
U = "Unsplash License, https://unsplash.com/photos/"
CREDITS = {
    "dim-sum": ("golden-lantern.jpg", U + "1678026582164-24a5460c447a"),
    "bubble-tea": ("chatime.jpg", U + "1558857563-b371033873b8"),
    "ramen": ("kinton-ramen.jpg", U + "1569718212165-3a8278d5f624"),
    "korean-bbq": ("seoul-house.jpg", U + "1709433420601-6e473136571b"),
    "dumplings": ("dumpling-house.jpg", U + "1496116218417-1a781b1c416c"),
    "coffee": ("brew-lab.jpg", U + "1509042239860-f550ce710b93"),
    "sushi": ("sakura-house.jpg", U + "1579584425555-c3ce17fd4351"),
    "pho": ("pho-hung.jpg", U + "1631709497146-a239ef373cf1"),
    "bowls": ("bowl-lab.jpg", U + "1546069901-ba9599a7e63c"),
    "noodles": ("noodle-bar.jpg", U + "1585032226651-759b368d7246"),
    "wok": ("wok-bar.jpg", U + "1603133872878-684f208fb84b"),
    "burgers": ("burger-co.jpg", U + "1568901346375-23c9450c58cd"),
    "tacos": ("alt-tacos.jpg", U + "1599974579688-8dbdd335c77f"),
    "pizza": ("alt-pizza.jpg", U + "1513104890138-7c749659a591"),
    "hot-pot": ("alt-hotpot.jpg", U + "1611345158052-94149ce57507"),
    "banh-mi": ("alt-banhmi.jpg", U + "1600454309261-3dc9b7597637"),
}

def crop(im):
    w, h = im.size
    if w / h > RATIO:
        nw = round(h * RATIO); return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = round(w / RATIO); return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))

def encode(im, fmt, budget=None):
    for q in (78, 72, 66, 60, 54):
        b = io.BytesIO(); im.save(b, fmt, quality=q, **({"method": 6} if fmt == "WEBP" else {"optimize": True, "progressive": True}))
        if budget is None or b.tell() <= budget: return b.getvalue()
    sys.exit(f"over budget: {fmt} {im.size} is {b.tell()} bytes > {budget}")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.iterdir():
        if f.suffix in (".webp", ".jpg"): f.unlink()
    manifest = {}
    for name, (src, credit) in CREDITS.items():
        im = crop(Image.open(SRC / src).convert("RGB"))
        colour = "#%02x%02x%02x" % im.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        files = {}
        for w in WIDTHS:
            if im.width < w: continue
            r = im.resize((w, round(w / RATIO)), Image.LANCZOS)
            for fmt, ext in (("WEBP", "webp"), ("JPEG", "jpg")):
                data = encode(r, fmt, BUDGET[w] if fmt == "WEBP" else None)
                fn = f"{name}-{w}.{hashlib.sha1(data).hexdigest()[:8]}.{ext}"
                (OUT / fn).write_bytes(data)
                files.setdefault(ext, {})[w] = f"/assets/img/{fn}"
        manifest[name] = {"w": 1200, "h": 900, "colour": colour, "webp": files["webp"], "jpg": files["jpg"], "credit": credit}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    total = sum(f.stat().st_size for f in OUT.glob("*.webp"))
    print(f"{len(manifest)} photos, {len(list(OUT.glob('*.webp')))} webp ({total // 1024} KB) + jpg fallbacks -> {OUT}")

def picture(name, alt, sizes="(min-width: 1000px) 25vw, 50vw", cls="", eager=False):
    """<picture> markup for one photo: webp + jpg srcset, width/height, colour placeholder, lazy unless eager."""
    m = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))[name]
    ss = lambda ext: ", ".join(f"{u} {w}w" for w, u in m[ext].items())
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="{m["jpg"]["800"]}" srcset="{ss("jpg")}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{alt}" {load}'
            f' class="{cls}" style="background:{m["colour"]}"></picture>')

if __name__ == "__main__":
    main()
    assert picture("pho", "Pho").count("w,") >= 2, "srcset missing sizes"  # self-check
