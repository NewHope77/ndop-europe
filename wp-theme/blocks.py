"""
Gutenberg block markup, written the way the design needs it.

The site's sections are expressed as core blocks — group, heading, paragraph,
list, image — each carrying the class the stylesheet already targets. Nothing
here invents a style: the classes come from assets/css/style.css unchanged.

Two attributes do the real work for the client:

  lock         stops a section being dragged elsewhere or deleted
  templateLock stops items being added to or removed from a fixed arrangement

Text inside stays editable in both cases, which is the whole point — the words
and the photographs can change, the layout cannot.
"""

import json

SECTION_LOCK = {"move": True, "remove": True}


def _attrs(d):
    """Block attributes as WordPress writes them: JSON, or nothing at all."""
    d = {k: v for k, v in d.items() if v not in (None, "", [], {})}
    return " " + json.dumps(d, separators=(",", ":"), ensure_ascii=False) if d else ""


def _classes(*names):
    out = []
    for n in names:
        if n:
            out.extend(str(n).split())
    return " ".join(dict.fromkeys(out))


def group(children, tag="div", cls="", lock=None, template_lock=None, extra=None):
    """A core/group. Sections of the page are groups with tagName 'section'."""
    attrs = {"tagName": tag} if tag != "div" else {}
    if cls:
        attrs["className"] = cls
    if lock:
        attrs["lock"] = lock
    if template_lock:
        attrs["templateLock"] = template_lock
    if extra:
        attrs.update(extra)

    inner = "\n".join(c for c in children if c)

    # An anchor is not only an attribute: core/group writes it into the markup
    # as id="…", and a block whose saved markup does not match what the block
    # would save is shown to the client as invalid content.
    anchor = f' id="{attrs["anchor"]}"' if attrs.get("anchor") else ""

    return (
        f"<!-- wp:group{_attrs(attrs)} -->\n"
        f'<{tag} class="{_classes("wp-block-group", cls)}"{anchor}>\n{inner}\n</{tag}>\n'
        f"<!-- /wp:group -->"
    )


def heading(text, level=2, cls=""):
    attrs = {}
    if level != 2:
        attrs["level"] = level
    if cls:
        attrs["className"] = cls
    return (
        f"<!-- wp:heading{_attrs(attrs)} -->\n"
        f'<h{level} class="{_classes("wp-block-heading", cls)}">{text}</h{level}>\n'
        f"<!-- /wp:heading -->"
    )


def para(text, cls=""):
    attrs = {"className": cls} if cls else {}
    open_tag = f'<p class="{cls}">' if cls else "<p>"
    return f"<!-- wp:paragraph{_attrs(attrs)} -->\n{open_tag}{text}</p>\n<!-- /wp:paragraph -->"


def bullets(items, cls=""):
    """A core/list. Each line stays separately editable."""
    attrs = {"className": cls} if cls else {}
    lis = "\n".join(
        f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items
    )
    open_tag = f'<ul class="wp-block-list {cls}">' if cls else '<ul class="wp-block-list">'
    return f"<!-- wp:list{_attrs(attrs)} -->\n{open_tag}\n{lis}\n</ul>\n<!-- /wp:list-->".replace(
        "<!-- /wp:list-->", "<!-- /wp:list -->"
    )


def image(src, alt, cls="", zoomable=False, lazy=None):
    """
    A core/image, so the client swaps a photograph through the media library.

    The markup is exactly what the block itself would save — no loading
    attribute, no data attributes of ours. Anything extra and WordPress marks
    the block as invalid content the moment the client opens the page.

    Enlarging on click is therefore not written here. The container asks for it
    with the class `is-zoomable`, and the theme adds the attribute when the page
    is rendered; see ndop_mark_zoomable_images().

    `src` is a file name from assets/img, written as a placeholder and resolved
    when the theme imports that file into the library.
    """
    name = src.split("/")[-1]
    ident = f"__IMG_ID:{name}__"

    attrs = {"id": ident, "sizeSlug": "full", "linkDestination": "none"}
    if cls:
        attrs["className"] = cls

    # The id belongs in the attributes as a number, not a quoted string.
    head = _attrs(attrs).replace(f'"{ident}"', ident)

    return (
        f"<!-- wp:image{head} -->\n"
        f'<figure class="{_classes("wp-block-image", "size-full", cls)}">'
        f'<img src="__IMG_URL:{name}__" alt="{alt}" class="wp-image-{ident}"/></figure>\n'
        f"<!-- /wp:image -->"
    )


def raw(markup):
    """Decoration and controls — rules, icons, buttons. Not meant to be edited."""
    return f"<!-- wp:html -->\n{markup}\n<!-- /wp:html -->"


# --- pieces of the design that recur -------------------------------------

RULE = '<div class="rule" aria-hidden="true"><i></i></div>'
RULE_CENTER = '<div class="rule rule--center" aria-hidden="true"><i></i></div>'
ARROW = (
    '<svg width="16" height="10" viewBox="0 0 16 10" fill="none">'
    '<path d="M1 5h13M10 1l4 4-4 4" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def button(label, href, style="btn--primary"):
    return f'<a class="{_classes("btn", style)}" href="{href}">{label}</a>'


def button_row(buttons, style=""):
    s = f' style="{style}"' if style else ""
    return raw(f'<div class="btn-row"{s}>' + "".join(buttons) + "</div>")


def link_arrow(label, href):
    return f'<a class="link-arrow" href="{href}">{label} {ARROW}</a>'
