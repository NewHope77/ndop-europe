#!/usr/bin/env python3
"""
Static site builder for The National Days of Prayer Movement in Europe.

Layout  : src/layout.html          — header, footer, <head>
Template: src/pages/<page>.html    — the shape of one page, with {{ }} markers
Content : content/<page>.json      — the words and pictures, edited through /admin

Running this writes the finished pages to the repo root, where the host serves
them. No dependencies, no toolchain.

    python3 build.py
"""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
CONTENT = ROOT / "content"

SECTION = re.compile(r"\{\{#\s*([\w.]+)\s*\}\}(.*?)\{\{/\s*\1\s*\}\}", re.S)
OPTIONAL = re.compile(r"\{\{\?\s*([\w.]+)\s*\}\}(.*?)\{\{/\?\s*\1\s*\}\}", re.S)
FIELD = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")


def lookup(ctx, path):
    """Resolve 'a.b.c' against a stack of dicts, innermost scope first."""
    for scope in reversed(ctx):
        if not isinstance(scope, dict):
            continue
        value = scope
        for part in path.split("."):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                value = None
                break
        if value is not None:
            return value
    return None


def render(template, ctx):
    """{{#list}}…{{/list}} repeats, {{?field}}…{{/?field}} is conditional,
    {{field}} substitutes. Values are inserted as-is: the content is ours."""

    def section(match):
        items = lookup(ctx, match.group(1)) or []
        # a list of plain strings is addressed as {{value}} inside the block
        items = [i if isinstance(i, dict) else {"value": i} for i in items]
        return "".join(render(match.group(2), ctx + [item]) for item in items)

    def optional(match):
        return render(match.group(2), ctx) if lookup(ctx, match.group(1)) else ""

    def field(match):
        value = lookup(ctx, match.group(1))
        return "" if value is None else str(value)

    template = SECTION.sub(section, template)
    template = OPTIONAL.sub(optional, template)
    return FIELD.sub(field, template)


def fingerprint(layout):
    """Append a content hash to the CSS/JS URLs so a redeploy is never served
    from a stale browser cache."""
    for asset in ("assets/css/style.css", "assets/js/i18n.js", "assets/js/main.js"):
        digest = hashlib.md5((ROOT / asset).read_bytes()).hexdigest()[:8]
        layout = layout.replace('"%s"' % asset, '"%s?v=%s"' % (asset, digest))
    return layout


def main():
    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    base = site["url"].rstrip("/") + "/"
    layout = fingerprint((SRC / "layout.html").read_text(encoding="utf-8"))
    built = []

    for template_file in sorted(PAGES.glob("*.html")):
        name = template_file.stem
        data = json.loads((CONTENT / (name + ".json")).read_text(encoding="utf-8"))
        ctx = [site, data]

        body = render(template_file.read_text(encoding="utf-8"), ctx)
        html = render(
            layout.replace("{{content}}", body)
                  .replace("{{canonical}}", base + ("" if name == "index" else name + ".html"))
                  .replace("<body>", '<body data-page="%s">' % name),
            ctx,
        )
        (ROOT / (name + ".html")).write_text(html, encoding="utf-8")
        built.append(name + ".html")

    urls = "".join(
        "\n  <url><loc>%s%s</loc></url>" % (base, "" if n == "index.html" else n)
        for n in built
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls,
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % base, encoding="utf-8"
    )

    print("Built %d pages: %s" % (len(built), ", ".join(built)))


if __name__ == "__main__":
    main()
