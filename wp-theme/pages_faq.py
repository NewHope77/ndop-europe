"""Frequently asked questions."""

import re

from blocks import group, para, raw, button, SECTION_LOCK
from pages_common import page_hero, cta_band


def paragraphs(answer):
    """
    The answer, as one block per paragraph.

    The stored answers already carry their own <p> tags. Wrapping that in a
    paragraph block would nest <p> inside <p>, which the browser repairs by
    closing the outer one early — leaving an empty paragraph above the answer
    and markup the editor cannot parse. Split it instead, so each paragraph is
    a block the client can edit on its own.
    """
    parts = re.findall(r"<p\b[^>]*>(.*?)</p>", answer, flags=re.S)
    return [para(p.strip()) for p in parts] if parts else [para(answer)]


def item(q, a):
    """
    One question.

    The question is the accordion's own control — a button the script opens and
    closes — so it stays as markup. The answer is ordinary paragraphs, which is
    what the client will actually want to reword.
    """
    return group(
        [
            raw(
                '<button class="faq__q" aria-expanded="false">'
                f'{q}<span class="faq__icon" aria-hidden="true"></span></button>'
            ),
            group(
                [group(paragraphs(a), cls="faq__a-inner")],
                cls="faq__a",
            ),
        ],
        cls="faq__item",
        template_lock="all",
    )


def build(c, url):
    hero = page_hero("FAQ", c["heroTitle"], c["heroLede"], url)

    faq = group(
        [
            group(
                [group([item(i["q"], i["a"]) for i in c["items"]], cls="faq", extra={"anchor": "faq"})],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    cta = cta_band(
        c["ctaEyebrow"], c["ctaTitle"], c["ctaText"],
        [button(c["ctaButton"], url("contact"))],
    )

    return "\n\n".join([hero, faq, cta])
