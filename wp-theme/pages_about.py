"""About Us."""

from blocks import group, heading, para, bullets, image, raw, button, button_row, SECTION_LOCK
from pages_common import page_hero, pullquote, section_head


def build(c, url):
    hero = page_hero("About Us", c["heroTitle"], c["heroLede"], url)

    intro = group(
        [
            group(
                [
                    group(
                        [
                            group([image(c["introImage"], c["introAlt"])], cls="feature__media reveal"),
                            group(
                                [
                                    para(c["introEyebrow"], "eyebrow"),
                                    heading(c["introTitle"], 2),
                                    para(c["introLead"], "lead"),
                                    *[para(p) for p in c["introParagraphs"]],
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

    def value(v):
        return group(
            [raw(v["icon"]), heading(v["title"], 3), para(v["text"])],
            tag="article",
            cls="value reveal",
            template_lock="all",
        )

    values = group(
        [
            group(
                [
                    section_head(c["valuesEyebrow"], c["valuesTitle"], center=True),
                    group([value(v) for v in c["values"]], cls="value-grid", template_lock="all"),
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--paper2",
        lock=SECTION_LOCK,
    )

    prose = []
    for s in c["doSections"]:
        prose.append(heading(s["title"], 3))
        prose.extend(para(p) for p in s["paragraphs"])
    prose.append(bullets(c["doBullets"]))
    prose.append(button_row([button(c["doButton"], url("resources"), "btn--outline")]))

    what_we_do = group(
        [
            group(
                [
                    section_head(c["doEyebrow"], c["doTitle"]),
                    group(prose, cls="prose reveal"),
                ],
                cls="wrap wrap--narrow",
            )
        ],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    def member(m):
        return group(
            [
                raw(f'<span class="board-member__country">{m["country"]}</span>'),
                heading(m["role"], 3),
                para(m["text"]),
            ],
            tag="article",
            cls="board-member reveal",
            template_lock="all",
        )

    board = group(
        [
            group(
                [
                    section_head(c["boardEyebrow"], c["boardTitle"], c["boardLede"]),
                    group([member(m) for m in c["board"]], cls="board-grid"),
                    para(c["boardNote"], "board-note reveal"),
                ],
                cls="wrap",
            )
        ],
        tag="section",
        cls="section section--paper2",
        lock=SECTION_LOCK,
        extra={"anchor": "board"},
    )

    quote = pullquote(c["pullQuote"], c["pullQuoteCite"])

    return "\n\n".join([hero, intro, values, what_we_do, board, quote])
