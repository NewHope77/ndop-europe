#!/usr/bin/env python3
"""
Static site builder for The National Days of Prayer Movement in Europe.

Every page in src/pages/ is a content fragment preceded by a short front-matter
block. The fragment is inserted into src/layout.html and written to the repo
root, where GitHub Pages serves it. No dependencies, no toolchain.

    python3 build.py
"""

import hashlib
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
SITE_URL = "https://newhope77.github.io/ndop-europe/"


def parse(text):
    """Split 'key: value' front matter from the page body (separated by '---')."""
    head, _, body = text.partition("\n---\n")
    meta = {}
    for line in head.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body.strip()


def fingerprint(layout):
    """Append a content hash to the CSS/JS URLs so a redeploy is never served
    from a stale browser cache."""
    for asset in ("assets/css/style.css", "assets/js/i18n.js", "assets/js/main.js"):
        digest = hashlib.md5((ROOT / asset).read_bytes()).hexdigest()[:8]
        layout = layout.replace('"%s"' % asset, '"%s?v=%s"' % (asset, digest))
    return layout


def main():
    layout = fingerprint((SRC / "layout.html").read_text(encoding="utf-8"))
    built = []

    for page in sorted(PAGES.glob("*.html")):
        meta, body = parse(page.read_text(encoding="utf-8"))
        html = (
            layout.replace("{{title}}", meta.get("title", ""))
            .replace("{{description}}", meta.get("description", ""))
            .replace("{{canonical}}", SITE_URL + ("" if page.stem == "index" else page.name))
            .replace("{{content}}", body)
            .replace("{{scripts}}", meta.get("scripts", ""))
            .replace("<body>", '<body data-page="%s">' % meta.get("nav", page.stem))
        )
        (ROOT / page.name).write_text(html, encoding="utf-8")
        built.append(page.name)

    # sitemap.xml
    urls = "".join(
        "\n  <url><loc>%s%s</loc></url>" % (SITE_URL, "" if n == "index.html" else n)
        for n in built
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls,
        encoding="utf-8",
    )

    # robots.txt
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % SITE_URL, encoding="utf-8"
    )

    print("Built %d pages: %s" % (len(built), ", ".join(built)))


if __name__ == "__main__":
    main()
