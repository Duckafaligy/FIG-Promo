"""Tells Bing (and the other IndexNow engines) about every page in the sitemap, so new and changed pages get crawled fast.
usage: python site/scripts/indexnow.py   (after the site is deployed; the key file <key>.txt sits at the site root)"""
import json, pathlib, re, urllib.request

SITE = pathlib.Path(__file__).resolve().parents[1]
HOST = "www.figpromo.ca"
key = next(p.stem for p in SITE.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem))
urls = re.findall(r"<loc>([^<]+)</loc>", (SITE / "sitemap.xml").read_text(encoding="utf-8"))
body = {"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow: {r.status} for {len(urls)} pages")
