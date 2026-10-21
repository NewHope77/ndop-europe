"""The home page, as Gutenberg blocks."""

from blocks import (
    group, heading, para, bullets, image, raw, button, button_row, link_arrow,
    RULE, RULE_CENTER, SECTION_LOCK,
)

# The three benefit icons, drawn in the brochure's line style.
ICON_SOCIETY = (
    '<svg class="benefit__icon" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
    '<circle cx="11" cy="11" r="4.6" stroke="currentColor" stroke-width="1.6"/>'
    '<circle cx="22" cy="13" r="3.6" stroke="currentColor" stroke-width="1.6" opacity=".55"/>'
    '<path d="M3 27c0-4.4 3.6-8 8-8s8 3.6 8 8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    '<path d="M21 19.4c4 .5 7 3.9 7 7.6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>'
    "</svg>"
)
ICON_STATE = (
    '<svg class="benefit__icon" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
    '<path d="M16 3l12 5.5v3H4v-3L16 3z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M7.5 12v11M13 12v11M19 12v11M24.5 12v11M3 27h26" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    "</svg>"
)
ICON_CHURCH = (
    '<svg class="benefit__icon" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
    '<path d="M16 3v9M11.5 7h9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    '<path d="M6 28V15l10-5 10 5v13" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M13 28v-6.5h6V28M3 28h26" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    "</svg>"
)


def benefit(icon, title, items):
    """One of the three columns. Its heading and lines stay editable; the icon
    and the arrangement do not, so the row cannot end up uneven."""
    return group(
        [raw(icon), heading(title, 3), bullets(items)],
        tag="article",
        cls="benefit reveal",
        template_lock="all",
    )


def build(c, url):
    """`c` is content/index.json; `url` resolves a page slug to its address."""

    hero = group(
        [
            raw('<div class="hero__map" aria-hidden="true"></div>'),
            group(
                [
                    para(c["heroEyebrow"], "hero__eyebrow"),
                    heading(c["heroTitle"], 1),
                    raw(RULE),
                    para(c["heroVerse"], "hero__verse"),
                    para(c["heroCite"], "hero__cite"),
                    button_row([
                        button(c["heroCta1"], url("about")),
                        button(c["heroCta2"], url("resources"), "btn--ghost"),
                    ]),
                ],
                cls="wrap hero__inner",
            ),
            raw('<div class="hero__scroll" aria-hidden="true"><i></i><span>Scroll</span></div>'),
        ],
        tag="section",
        cls="hero",
        lock=SECTION_LOCK,
    )

    mission = group(
        [
            image("map-light.png", "", "mission__map"),
            group(
                [
                    para(c["missionEyebrow"], "eyebrow"),
                    para(c["missionText"], "mission__text"),
                    raw(RULE),
                ],
                cls="wrap mission__inner reveal",
            ),
        ],
        tag="section",
        cls="section mission",
        lock=SECTION_LOCK,
        extra={"anchor": "mission"},
    )

    benefits = group(
        [
            group(
                [
                    group(
                        [
                            para(c["benefitsEyebrow"], "eyebrow"),
                            heading(c["benefitsTitle"], 2),
                            para(c["benefitsLede"], "lede"),
                        ],
                        cls="section-head center reveal",
                    ),
                    group(
                        [
                            benefit(ICON_SOCIETY, c["societyTitle"], c["societyItems"]),
                            benefit(ICON_STATE, c["stateTitle"], c["stateItems"]),
                            benefit(ICON_CHURCH, c["churchTitle"], c["churchItems"]),
                        ],
                        cls="benefits",
                        template_lock="all",
                    ),
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--paper2",
        lock=SECTION_LOCK,
    )

    def card(item):
        return group(
            [
                group([image(item["image"], item["alt"])],
                    cls="card__media",
                    template_lock=False),
                group(
                    [
                        raw(f'<span class="tl-year">{item["year"]}</span>'),
                        heading(item["title"], 3),
                        para(item["text"]),
                        raw(link_arrow(item["linkLabel"], url(item["link"].replace(".html", "")))),
                    ],
                    cls="card__body",
                ),
            ],
            tag="article",
            cls="card reveal",
            template_lock="all",
        )

    history = group(
        [
            group(
                [
                    group(
                        [
                            para(c["historyEyebrow"], "eyebrow"),
                            heading(c["historyTitle"], 2),
                            para(c["historyLede"], "lede"),
                        ],
                        cls="section-head reveal",
                    ),
                    group([card(i) for i in c["cards"]], cls="card-grid", template_lock="all"),
                    button_row(
                        [button(c["historyCta"], url("history"), "btn--outline")],
                        style="justify-content:center;margin-top:44px",
                    ),
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section",
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
                                    image(c["ukraineImage"], c["ukraineAlt"]),
                                    raw(
                                        '<div class="feature__badge">'
                                        f'<strong>{c["ukraineBadgeDate"]}</strong>'
                                        f'<span>{c["ukraineBadgeText"]}</span></div>'
                                    ),
                                ],
                                cls="feature__media feature__media--frame",
                                template_lock=False,
                            ),
                            group(
                                [
                                    para(c["ukraineEyebrow"], "eyebrow"),
                                    heading(c["ukraineTitle"], 2),
                                    para(c["ukraineP1"]),
                                    para(c["ukraineP2"]),
                                    button_row([
                                        button(c["ukraineButton"], url("resources"), "btn--outline")
                                    ]),
                                ],
                                cls="feature__body",
                            ),
                        ],
                        cls="feature reveal",
                    )
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--paper2",
        lock=SECTION_LOCK,
    )

    quote = group(
        [
            group(
                [
                    group(
                        [raw(RULE_CENTER), para(c["quoteText"]), raw(f'<cite>{c["quoteCite"]}</cite>')],
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

    cta = group(
        [
            raw('<div class="cta-band__map" aria-hidden="true"></div>'),
            group(
                [
                    para(c["ctaEyebrow"], "eyebrow center"),
                    heading(c["ctaTitle"], 2),
                    para(c["ctaLede"]),
                    button_row([
                        button(c["ctaB1"], url("contact") + "#join"),
                        button(c["ctaB2"], url("resources") + "#steps", "btn--ghost"),
                    ]),
                ],
                cls="wrap",
            ),
        ],
        tag="section",
        cls="section cta-band",
        lock=SECTION_LOCK,
    )

    return "\n\n".join([hero, mission, benefits, history, ukraine, quote, cta])
