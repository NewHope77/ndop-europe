"""History — the twelve moments, 1571 to today."""

from blocks import group, heading, para, image, raw, button, SECTION_LOCK
from pages_common import page_hero, pullquote, cta_band


def entry(e):
    """
    One moment on the timeline.

    The plate is marked is-zoomable, so the theme lets the picture open full
    size exactly as before; the caption comes from the media library. The plate
    keeps the hover overlay the design draws, and nothing is cropped.
    """
    body = [
        raw(f'<span class="tl-year">{e["year"]}</span>'),
        heading(e["title"], 3),
        *[para(p) for p in e["paragraphs"]],
    ]

    if e.get("quote"):
        body.append(
            raw(
                '<blockquote class="tl-quote">'
                f'{e["quote"]}<cite>{e["quoteCite"]}</cite></blockquote>'
            )
        )

    if e.get("extraImage"):
        # The second picture of an entry. Its spacing and its squared corners
        # were inline styles in the static build; as a block they belong to a
        # class, so the markup stays something the editor can parse.
        body.append(
            group(
                [
                    group(
                        [image(e["extraImage"], e["extraAlt"])],
                        cls="tl-card__media tl-card__media--extra is-zoomable",
                        template_lock=False,
                    )
                ],
                cls="tl-card__extra",
            )
        )

    return group(
        [
            raw('<span class="tl-item__dot" aria-hidden="true"></span>'),
            group(
                [
                    group(
                        [image(e["image"], e["alt"])],
                        cls="tl-card__media is-zoomable",
                        template_lock=False,
                    ),
                    group(body, cls="tl-card__body"),
                ],
                cls="tl-card",
            ),
        ],
        tag="article",
        cls="tl-item reveal",
        extra={"anchor": e["id"]},
    )


def build(c, url):
    hero = page_hero("History", c["heroTitle"], c["heroLede"], url)

    timeline = group(
        [
            group(
                [group([entry(e) for e in c["entries"]], cls="timeline")],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    quote = pullquote(c["pullQuote"], c["pullQuoteCite"])
    cta = cta_band(
        c["ctaEyebrow"], c["ctaTitle"], c["ctaText"],
        [button(c["ctaButton"], url("resources"))],
    )

    return "\n\n".join([hero, timeline, quote, cta])
