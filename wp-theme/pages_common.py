"""Sections that appear on more than one page."""

from blocks import (
    group, heading, para, raw, button, button_row,
    RULE_CENTER, SECTION_LOCK,
)


def page_hero(crumb, title, lede, url):
    """The blue band at the top of every page but the home page."""
    return group(
        [
            raw('<div class="page-hero__map" aria-hidden="true"></div>'),
            group(
                [
                    raw(
                        '<p class="breadcrumb">'
                        f'<a href="{url("index")}">Home</a><span>/</span>{crumb}</p>'
                    ),
                    heading(title, 1),
                    para(lede, "lede"),
                ],
                cls="wrap page-hero__inner",
            ),
        ],
        tag="section",
        cls="page-hero",
        lock=SECTION_LOCK,
    )


def pullquote(text, cite):
    """A sentence set apart on navy."""
    return group(
        [
            group(
                [
                    group(
                        [raw(RULE_CENTER), para(text), raw(f"<cite>{cite}</cite>")],
                        cls="pullquote reveal",
                    )
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--navy",
        lock=SECTION_LOCK,
    )


def cta_band(eyebrow, title, text, buttons):
    """The closing invitation."""
    return group(
        [
            raw('<div class="cta-band__map" aria-hidden="true"></div>'),
            group(
                [
                    para(eyebrow, "eyebrow center"),
                    heading(title, 2),
                    para(text),
                    button_row(buttons),
                ],
                cls="wrap",
            ),
        ],
        tag="section",
        cls="section cta-band",
        lock=SECTION_LOCK,
    )


def section_head(eyebrow, title, lede=None, center=False):
    children = [para(eyebrow, "eyebrow"), heading(title, 2)]
    if lede:
        children.append(para(lede, "lede"))
    return group(children, cls="section-head center reveal" if center else "section-head reveal")
