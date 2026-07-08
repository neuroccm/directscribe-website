#!/usr/bin/env python3
"""
DirectScribe build validator — the node-free equivalent of `npm run build`
gate. Runs against dist/ (run build.py first). Exits non-zero on any failure.

Checks:
  * every internal href/src resolves to a real file in dist/ (clean-URL aware)
  * every in-page and cross-page #anchor target exists
  * one <h1>, a <title>, html lang, meta viewport, persistent nav + footer
  * no <script> tags anywhere (the site ships zero client JS)
  * every compliance page carries an in-body NOT-LEGAL-ADVICE callout
  * honest-copy denylist (blocks over-claims like "nothing retained anywhere",
    "100% local", "HIPAA compliant", "unrecoverable", ...)
  * required honest-copy phrases are present where mandated
  * version.json has exactly the app's manifest shape (no free-text notes field)
  * key palette pairs meet WCAG AA (>= 4.5:1)
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

errors = []
warnings = []
FILE_EXTS = (".css", ".json", ".svg", ".xml", ".png", ".jpg", ".webp", ".ico", ".txt", ".pdf")


def err(where, msg):
    errors.append(f"{where}: {msg}")


def norm(p):
    """Normalize a URL path for the id/page map: drop trailing slash except root."""
    p = p.split("?")[0]
    if p != "/" and p.endswith("/"):
        p = p[:-1]
    return p or "/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []      # (tag, href/src)
        self.ids = set()
        self.h1 = 0
        self.in_title = False
        self.title = ""
        self.lang = None
        self.has_viewport = False
        self.has_nav = False
        self.has_footer = False
        self.scripts = 0
        self.imgs_missing_alt = 0
        self.navmarks = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html" and "lang" in a:
            self.lang = a["lang"]
        if tag == "meta" and a.get("name") == "viewport":
            self.has_viewport = True
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "nav":
            self.has_nav = True
        if tag == "footer":
            self.has_footer = True
        if tag == "script":
            self.scripts += 1
        if tag == "a" and a.get("href"):
            self.links.append(("a", a["href"]))
            if "data-nav" in a:
                self.navmarks.add(a["data-nav"])
        if tag in ("link", "img") and a.get("href", a.get("src")):
            self.links.append((tag, a.get("href") or a.get("src")))
        if tag == "img":
            if not (a.get("alt") is not None):
                self.imgs_missing_alt += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


# honest-copy guardrails ------------------------------------------------------
DENY = [
    "nothing retained anywhere", "never leaves your mac", "nothing ever leaves",
    "nothing leaves your", "everything stays on your mac", "your data never leaves",
    "audio never leaves", "100% local", "fully local dictation",
    "fully local transcription", "completely local", "hipaa compliant",
    "hipaa-compliant", "hipaa compliance", "unrecoverable", "permanently delete",
    "cannot be recovered", "military-grade", "bank-grade", "zero risk",
]
# (page-url-substring, needle) — needle must be present
REQUIRE = [
    ("/index", "your dictation. your vendors. your mac."),
    ("/index", "backups you configure may retain copies"),
    ("/index", "only the physician's voice"),
    ("/security", "backups you configure may retain copies"),
    ("/security", "no telemetry"),
    ("/security", "update check"),
    ("/security", "s.10.1"),
    ("/security", "system of record"),
    ("/security", "only the physician's voice"),
    ("/pricing", "$39"),
    ("/pricing", "$399"),
    ("/compliance/index", "s.10.1"),
    ("/compliance/consent", "filevault"),
    ("/support", "month"),
]


def normalize_text(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"').lower())


# WCAG contrast ---------------------------------------------------------------
def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    h = h.lstrip("#")
    return 0.2126 * _lin(int(h[0:2], 16)) + 0.7152 * _lin(int(h[2:4], 16)) + 0.0722 * _lin(int(h[4:6], 16))


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


PAIRS = [
    ("ink/white", "#1b2733", "#ffffff"), ("navy/white", "#0a2540", "#ffffff"),
    ("muted/white", "#51616f", "#ffffff"), ("muted/surface", "#51616f", "#eef3f8"),
    ("link/white", "#0b5fa5", "#ffffff"), ("white/brand", "#ffffff", "#0b5fa5"),
    ("white/navy", "#ffffff", "#0a2540"), ("footer-muted/navy", "#b7c6d6", "#0a2540"),
    ("footer-link/navy", "#8fc1ea", "#0a2540"), ("warn/warn-bg", "#8a5a00", "#fbf3e2"),
    ("success/white", "#1e7a46", "#ffffff"),
]


def main():
    if not DIST.exists():
        print("dist/ not found — run: python3 build.py", file=sys.stderr)
        return 1

    html_files = sorted(DIST.rglob("*.html"))
    if not html_files:
        err("dist", "no HTML files built")

    # map every page URL -> its id set, for cross-page anchor checks
    pages = {}
    parsed = {}
    for f in html_files:
        rel = f.relative_to(DIST).as_posix()
        url = "/" if rel == "index.html" else (
            "/" + rel[: -len("/index.html")] if rel.endswith("/index.html") else "/" + rel)
        parsed[f] = parse(f)
        pages[norm(url)] = parsed[f].ids

    for f in html_files:
        rel = f.relative_to(DIST).as_posix()
        page = parsed[f]
        cur_url = "/" if rel == "index.html" else (
            "/" + rel[: -len("/index.html")] if rel.endswith("/index.html") else "/" + rel)
        where = rel
        raw = normalize_text(f.read_text(encoding="utf-8"))

        # structure / accessibility
        if page.h1 != 1:
            err(where, f"expected exactly one <h1>, found {page.h1}")
        if not page.title.strip():
            err(where, "empty <title>")
        if page.lang is None:
            err(where, "missing lang on <html>")
        if not page.has_viewport:
            err(where, "missing meta viewport")
        if not page.has_nav:
            err(where, "missing <nav>")
        if not page.has_footer:
            err(where, "missing <footer>")
        if page.scripts:
            err(where, f"found {page.scripts} <script> tag(s) — site must ship zero JS")
        src = f.read_text(encoding="utf-8")
        if "style=\"" in src or "style='" in src:
            err(where, "inline style attribute present — blocked by CSP style-src 'self'")
        if 'onclick=' in src.lower() or 'onload=' in src.lower():
            err(where, "inline event handler present — site ships no JS")
        if page.imgs_missing_alt:
            err(where, f"{page.imgs_missing_alt} <img> without alt")
        need_nav = {"product", "security", "pricing", "compliance", "support"}
        if not need_nav.issubset(page.navmarks):
            err(where, f"nav missing links: {need_nav - page.navmarks}")
        if "not legal advice" not in raw:
            err(where, "footer NOT-LEGAL-ADVICE text missing")

        # compliance pages need an in-body legal callout
        if rel.startswith("compliance/"):
            if "callout--legal" not in f.read_text(encoding="utf-8"):
                err(where, "compliance page missing in-body NOT-LEGAL-ADVICE callout")

        # honest-copy denylist
        for bad in DENY:
            if bad in raw:
                err(where, f"forbidden over-claim present: '{bad}'")

        # required phrases
        for frag, needle in REQUIRE:
            if ("/" + rel).startswith(frag) or ("/" + rel.replace("/index.html", "/index")).startswith(frag):
                if normalize_text(needle) not in raw:
                    err(where, f"required phrase missing: '{needle}'")

        # link resolution
        for tag, href in page.links:
            h = href.strip()
            if not h or h.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            if h.startswith("#"):
                if h[1:] and h[1:] not in page.ids:
                    err(where, f"missing in-page anchor {h}")
                continue
            path, _, frag = h.partition("#")
            path = path.split("?")[0]
            if not path.startswith("/"):
                err(where, f"non-absolute internal link '{h}' (author links as /...)")
                continue
            # resolve to a file in dist
            if path.endswith(FILE_EXTS):
                target = DIST / path.lstrip("/")
                ok = target.is_file()
            else:
                cand = DIST / path.lstrip("/") / "index.html" if path != "/" else DIST / "index.html"
                ok = cand.is_file()
            if not ok:
                err(where, f"broken internal link '{h}'")
                continue
            # cross-page anchor
            if frag:
                target_ids = pages.get(norm(path))
                if target_ids is not None and frag not in target_ids:
                    err(where, f"link '{h}' targets missing anchor #{frag}")

    # version.json ------------------------------------------------------------
    vj = DIST / "version.json"
    if not vj.is_file():
        err("version.json", "missing")
    else:
        try:
            data = json.loads(vj.read_text(encoding="utf-8"))
            expect_keys = {"version", "build", "url", "minMacOS"}
            if set(data.keys()) != expect_keys:
                err("version.json", f"keys must be exactly {sorted(expect_keys)}, got {sorted(data.keys())}")
            if "notes" in data:
                err("version.json", "must not contain a free-text 'notes' field")
            if data.get("url") != "https://directscribe.ca/download":
                err("version.json", f"url must be https://directscribe.ca/download, got {data.get('url')!r}")
            for k in expect_keys:
                if k in data and not isinstance(data[k], str):
                    err("version.json", f"{k} must be a string")
        except json.JSONDecodeError as e:
            err("version.json", f"invalid JSON: {e}")

    # contrast ----------------------------------------------------------------
    for name, fg, bg in PAIRS:
        r = contrast(fg, bg)
        if r < 4.5:
            err("contrast", f"{name} = {r:.2f}:1 < 4.5 (WCAG AA)")

    # report ------------------------------------------------------------------
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        print(f"\nFAILED — {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"OK — validated {len(html_files)} pages, links, anchors, copy, "
          f"version.json, and WCAG AA contrast. No errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
