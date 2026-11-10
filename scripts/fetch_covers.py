"""Fetch real cover-image URLs for the BookVerse seed catalog.

Data sources (both public, no API key required):
  1. Google Books API   - search by title+author, take imageLinks.thumbnail
  2. Open Library API   - fallback when Google has no cover

The URLs (not the images) are stored; the browser loads covers directly from
the provider CDN at runtime. Usage:

    python scripts/fetch_covers.py   # from repo root (or inside backend container)

Writes: backend/app/cover_urls.py  ->  COVER_URLS = {title: url}
Books with no public cover are simply omitted; the frontend then falls back
to the generated CSS cover.
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

_repo_backend = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_repo_backend if _repo_backend.exists() else Path("/app")))
from app.seed_data import BOOKS  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (BookVerse educational project)"}


def http_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def try_upgrade_zoom(url):
    """Try zoom=3 (larger image); keep it only if a real image comes back."""
    hi = re.sub(r"zoom=\d", "zoom=3", url)
    if hi == url:
        return url
    try:
        req = urllib.request.Request(hi, headers=UA)
        with urllib.request.urlopen(req, timeout=10) as r:
            ctype = (r.headers.get("Content-Type") or "").startswith("image")
            size = int(r.headers.get("Content-Length") or 0)
            if r.status == 200 and ctype and size > 8000:
                return hi
    except Exception:
        pass
    return url


def from_google(title, author):
    q = f'intitle:"{title}" inauthor:"{author.split()[-1]}"'
    url = ("https://www.googleapis.com/books/v1/volumes?q="
           + urllib.parse.quote(q) + "&maxResults=5&country=US")
    try:
        data = http_json(url)
    except Exception:
        return None
    for item in data.get("items", []):
        links = item.get("volumeInfo", {}).get("imageLinks") or {}
        thumb = links.get("thumbnail") or links.get("smallThumbnail")
        if thumb:
            thumb = thumb.replace("http://", "https://").replace("&edge=curl", "")
            return try_upgrade_zoom(thumb)
    return None


def from_openlibrary(title, author):
    url = ("https://openlibrary.org/search.json?"
           + urllib.parse.urlencode({"title": title, "author": author,
                                     "fields": "cover_i", "limit": 5}))
    try:
        data = http_json(url)
    except Exception:
        return None
    for doc in data.get("docs", []):
        if doc.get("cover_i"):
            return f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"
    return None


def main():
    covers, misses = {}, []
    for b in BOOKS:
        url = from_google(b["title"], b["author"]) or from_openlibrary(b["title"], b["author"])
        if url:
            covers[b["title"]] = url
            print(f"  OK   {b['title']}")
        else:
            misses.append(b["title"])
            print(f"  MISS {b['title']}")

    # second, looser pass: short title (strip subtitle) without the author
    still_missing = []
    for title in misses:
        b = next(x for x in BOOKS if x["title"] == title)
        short = title.split(":")[0].strip()
        url = None
        if short != title:
            url = from_google(short, b["author"]) or from_openlibrary(short, b["author"])
        if not url:
            url = from_openlibrary(title, "")
        if url:
            covers[title] = url
            print(f"  OK*  {title} (loose match)")
        else:
            still_missing.append(title)
    misses = still_missing

    out = Path(__file__).resolve().parents[1] / "backend" / "app" / "cover_urls.py"
    if not out.parent.exists():
        # running inside the backend container (non-root user): use /tmp
        out = Path("/tmp/cover_urls.py")
    lines = "\n".join(f'    "{t}": "{u}",' for t, u in sorted(covers.items()))
    out.write_text(
        '"""Real cover URLs (Google Books / Open Library CDNs), fetched once\n'
        'by scripts/fetch_covers.py - public data, no API key, no download.\n'
        'Titles missing here fall back to the generated CSS cover."""\n\n'
        "COVER_URLS = {\n" + lines + "\n}\n",
        encoding="utf-8",
    )
    print(f"\n{len(covers)}/{len(BOOKS)} covers found -> {out}")
    if misses:
        print("No public cover for:", ", ".join(misses))


if __name__ == "__main__":
    main()
