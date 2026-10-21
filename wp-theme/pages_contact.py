"""Contact."""

from blocks import group, heading, para, raw, link_arrow, SECTION_LOCK
from pages_common import page_hero, pullquote

MAIL_ICON = (
    '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true">'
    '<rect x="2.5" y="4.5" width="15" height="11" rx="1.5" stroke="currentColor" stroke-width="1.4"/>'
    '<path d="M3 5.5l7 5 7-5" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'
)
GLOBE_ICON = (
    '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true">'
    '<circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.4"/>'
    '<path d="M2.5 10h15M10 2.5c2.3 2.5 2.3 12.5 0 15M10 2.5c-2.3 2.5-2.3 12.5 0 15" '
    'stroke="currentColor" stroke-width="1.2"/></svg>'
)

EMAIL = "info@nationaldayofprayer.eu"


def build(c, url):
    hero = page_hero("Contact", c["heroTitle"], c["heroLede"], url)

    contact_lines = raw(
        '<ul class="contact-lines" style="flex-direction:column;gap:14px">'
        f'<li>{MAIL_ICON}<a href="mailto:{EMAIL}">{EMAIL}</a></li>'
        f'<li>{GLOBE_ICON}<a href="{url("about")}#board">{c["cardBoardLink"]}</a></li>'
        "</ul>"
    )

    card = group(
        [
            group(
                [
                    para(c["cardEyebrow"], "eyebrow"),
                    heading(c["cardTitle"], 3),
                    para(c["cardRole"], "coordinator__role"),
                    contact_lines,
                    para(c["cardNote"], "coordinator__note"),
                ],
            )
        ],
        cls="coordinator coordinator--single",
        template_lock="all",
    )

    blocks = [
        group([heading(b["title"], 3), para(b["text"], "contact-block__text")], cls="contact-block")
        for b in c["blocks"]
    ]

    media = group(
        [
            heading(c["mediaTitle"], 3),
            para(c["mediaText"], "contact-block__text"),
            raw(
                "<p>"
                + link_arrow(c["mediaDownload"], url("assets/docs/ndop-in-europe-brochure.pdf"))
                + "</p>"
            ),
        ],
        cls="contact-block",
    )

    left = group([card, *blocks, media], cls="reveal")

    # The form is a control, not prose: its fields, their order and their names
    # are what the script reads when it hands the message to the mail client.
    options = "".join(f"<option>{o}</option>" for o in c["roleOptions"])
    form = raw(
        '<form class="form" id="contactForm" novalidate>'
        f'<p class="eyebrow">{c["formEyebrow"]}</p>'
        f'<h2 style="font-size:1.7rem;margin-bottom:22px">{c["formTitle"]}</h2>'
        f'<div class="field"><label for="cf-name">{c["labelName"]}</label>'
        '<input id="cf-name" name="name" type="text" required autocomplete="name"></div>'
        f'<div class="field"><label for="cf-email">{c["labelEmail"]}</label>'
        '<input id="cf-email" name="email" type="email" required autocomplete="email"></div>'
        f'<div class="field"><label for="cf-country">{c["labelCountry"]}</label>'
        '<input id="cf-country" name="country" type="text" autocomplete="country-name"></div>'
        f'<div class="field"><label for="cf-role">{c["labelRole"]}</label>'
        f'<select id="cf-role" name="role">{options}</select></div>'
        f'<div class="field"><label for="cf-message">{c["labelMessage"]}</label>'
        '<textarea id="cf-message" name="message" required></textarea></div>'
        f'<button class="btn btn--primary" type="submit">{c["formButton"]}</button>'
        f'<p class="form__note">{c["formNote"]}</p>'
        '<p class="form__status" id="formStatus"></p>'
        "</form>"
    )

    right = group([form], cls="reveal", extra={"anchor": "join"})

    body = group(
        [group([group([left, right], cls="contact-grid")], cls="wrap")],
        tag="section",
        cls="section",
        lock=SECTION_LOCK,
    )

    quote = pullquote(c["pullQuote"], c["pullQuoteCite"])

    return "\n\n".join([hero, body, quote])
