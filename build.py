#!/usr/bin/env python3
"""
DirectScribe static site generator — zero dependencies (Python 3 stdlib only).

Astro was the preferred stack, but node/npm are unavailable in this
environment, so the site is hand-authored static HTML/CSS. This script stamps
each page's content into one shared layout (guaranteeing an identical nav,
footer, and NOT-LEGAL-ADVICE disclaimer on every page) and emits clean-URL
static files that Cloudflare Pages serves directly with no build step.

Usage:  python3 build.py
Output: dist/  (commit it, or set it as the Cloudflare Pages output directory)
"""
import hashlib
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
SITE = "https://directscribe.ca"

FRONT_RE = re.compile(r"^\s*<!--(.*?)-->", re.DOTALL)


def parse_page(text):
    """Return (meta dict, content) splitting the leading HTML-comment front-matter."""
    meta = {}
    m = FRONT_RE.match(text)
    content = text
    if m:
        block = m.group(1)
        content = text[m.end():]
        for line in block.splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, _, val = line.partition(":")
            meta[key.strip().lower()] = val.strip()
    return meta, content.strip("\n")


def out_and_url(rel):
    """Map a src/pages path to (output path relative to dist, canonical URL path)."""
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return "index.html", "/"
    if rel == "404.html":
        return "404.html", None  # not a public URL; excluded from sitemap
    if rel.endswith("/index.html"):
        d = rel[: -len("/index.html")]
        return f"{d}/index.html", f"/{d}/"
    d = rel[: -len(".html")]
    return f"{d}/index.html", f"/{d}/"


def apply_active_nav(layout, nav):
    if not nav:
        return layout
    marker = f'data-nav="{nav}"'
    return layout.replace(marker, f'{marker} aria-current="page"', 1)


def main():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    styles_hash = hashlib.sha256((SRC / "styles.css").read_bytes()).hexdigest()[:10]

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    urls = []
    page_files = sorted(PAGES.rglob("*.html"))
    for pf in page_files:
        rel = pf.relative_to(PAGES).as_posix()
        meta, content = parse_page(pf.read_text(encoding="utf-8"))
        out_rel, url = out_and_url(rel)
        canonical = SITE + "/" if url == "/" else (SITE + url if url else SITE + "/404")

        html = layout
        html = apply_active_nav(html, meta.get("nav", ""))
        html = html.replace("{{STYLES_HASH}}", styles_hash)
        html = html.replace("{{TITLE}}", meta.get("title", "DirectScribe"))
        html = html.replace("{{DESCRIPTION}}", meta.get("description", ""))
        html = html.replace("{{CANONICAL}}", canonical)
        # content injected last so page copy can never collide with a placeholder token
        html = html.replace("{{CONTENT}}", content)

        dst = DIST / out_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(html, encoding="utf-8")
        if url:
            urls.append(url)

    # assets
    (DIST / "assets").mkdir(exist_ok=True)
    shutil.copy2(SRC / "styles.css", DIST / "assets" / "styles.css")

    # public/ copied verbatim to site root (version.json, favicon, screenshots, _headers)
    if PUBLIC.exists():
        for item in PUBLIC.rglob("*"):
            if item.is_file():
                target = DIST / item.relative_to(PUBLIC)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)

    # sitemap.xml + robots.txt
    loc = "\n".join(
        f"  <url><loc>{SITE}{u}</loc></url>" for u in sorted(set(urls))
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{loc}\n</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )

    print(f"Built {len(page_files)} pages -> {DIST.relative_to(ROOT)}/")
    for u in sorted(set(urls)):
        print(f"  {u}")


if __name__ == "__main__":
    main()
