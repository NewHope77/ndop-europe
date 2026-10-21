"""Resources & Legal Base."""

from blocks import (
    group, heading, para, image, raw, button, button_row, link_arrow, SECTION_LOCK,
)
from pages_common import page_hero, cta_band, section_head


def build(c, url):
    hero = page_hero("Resources &amp; Legal Base", c["heroTitle"], c["heroLede"], url)

    # The five American dates. The pairing of a date with its line is tighter
    # than a list block expresses, so the markup is kept as it was.
    dates = raw(
        '<ul class="dates">'
        + "".join(
            f'<li><b>{d["date"]}</b><span>{d["text"]}</span></li>' for d in c["usDates"]
        )
        + "</ul>"
    )

    united_states = group(
        [
            group(
                [
                    group(
                        [
                            group([image(c["usImage"], c["usAlt"])], cls="feature__media reveal"),
                            group(
                                [
                                    para(c["usEyebrow"], "eyebrow"),
                                    heading(c["usTitle"], 2),
                                    *[para(p) for p in c["usParagraphs"]],
                                    dates,
                                ],
                                cls="feature__body prose reveal",
                            ),
                        ],
                        cls="feature",
                    )
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    law = group(
        [
            group(
                [
                    group(
                        [
                            group(
                                [
                                    image(c["lawImage"], c["lawAlt"]),
                                    raw(
                                        '<div class="feature__badge">'
                                        f'<strong>{c["lawBadgeDate"]}</strong>'
                                        f'<span>{c["lawBadgeText"]}</span></div>'
                                    ),
                                ],
                                cls="feature__media reveal",
                                template_lock="all",
                            ),
                            group(
                                [
                                    para(c["lawEyebrow"], "eyebrow"),
                                    heading(c["lawTitle"], 2),
                                    *[para(p) for p in c["lawParagraphs"]],
                                    group(
                                        [
                                            image(c["lawScanImage"], c["lawScanAlt"])
                                        ],
                                        cls="feature__media feature__media--frame feature__media--inset is-zoomable",
                                        template_lock="all",
                                    ),
                                ],
                                cls="feature__body prose reveal",
                            ),
                        ],
                        cls="feature feature--flip",
                    )
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--tight section--paper2",
        lock=SECTION_LOCK,
    )

    ukraine = group(
        [
            group(
                [
                    group(
                        [
                            group(
                                [
                                    image(c["uaImage"], c["uaAlt"]),
                                    raw(
                                        '<div class="feature__badge">'
                                        f'<strong>{c["uaBadgeDate"]}</strong>'
                                        f'<span>{c["uaBadgeText"]}</span></div>'
                                    ),
                                ],
                                cls="feature__media feature__media--frame reveal is-zoomable",
                                template_lock="all",
                            ),
                            group(
                                [
                                    para(c["uaEyebrow"], "eyebrow"),
                                    heading(c["uaTitle"], 2),
                                    para(c["uaLead"], "lead"),
                                    *[para(p) for p in c["uaParagraphs"]],
                                    button_row([
                                        button(c["uaButton"], url("history") + "#kyiv-2026", "btn--outline")
                                    ]),
                                ],
                                cls="feature__body prose reveal",
                            ),
                        ],
                        cls="feature",
                    )
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    # A numbered sequence where the number is drawn by the stylesheet.
    steps_list = raw(
        '<ol class="steps reveal">'
        + "".join(f'<li class="step"><h3>{s}</h3></li>' for s in c["steps"])
        + "</ol>"
    )

    steps = group(
        [
            group(
                [
                    section_head(c["stepsEyebrow"], c["stepsTitle"], c["stepsLede"], center=True),
                    steps_list,
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--paper2",
        lock=SECTION_LOCK,
        extra={"anchor": "steps"},
    )

    def download(d):
        return group(
            [
                group(
                    [
                        raw(f'<span class="tl-year">{d["tag"]}</span>'),
                        heading(d["title"], 3),
                        para(d["text"]),
                        raw(link_arrow(d["linkLabel"], url(d["link"]))),
                    ],
                    cls="card__body",
                )
            ],
            tag="article",
            cls="card reveal",
            template_lock="all",
        )

    downloads = group(
        [
            group(
                [
                    section_head(c["downloadsEyebrow"], c["downloadsTitle"], c["downloadsLede"]),
                    group([download(d) for d in c["downloads"]], cls="card-grid", template_lock="all"),
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    cta = cta_band(
        c["ctaEyebrow"], c["ctaTitle"], c["ctaText"],
        [button(c["ctaButton"], url("contact") + "#join")],
    )

    return "\n\n".join([hero, united_states, law, ukraine, steps, downloads, cta])
