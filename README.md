# The National Days of Prayer Movement in Europe

Static website for the movement encouraging the establishment of a National Day of
Prayer at the country level in every European country.

**Live demo:** https://newhope77.github.io/ndop-europe/

---

## What is here

| Page | File | Contents |
|---|---|---|
| Home | `index.html` | Hero, mission, benefits (society / state / churches), history preview, the Ukrainian precedent, call to action |
| About Us | `about.html` | Who the movement is, its principles, what it does, the International Board |
| History | `history.html` | 12-moment timeline, 1571 → 2026, with a lightbox for every image |
| Resources & Legal Base | `resources.html` | US precedents and Public Law 100-307, Ukraine's 2025 resolution, the seven practical steps, downloads |
| FAQ | `faq.html` | 10-question accordion |
| Contact | `contact.html` | Board contact, audience-specific notes, enquiry form |

All content, imagery and the colour palette come from the movement's own brochure
(`assets/docs/ndop-in-europe-brochure.pdf`). Site language is **English only**.

## Design

Taken directly from the printed brochure:

- Navy `#0C335B`, accent blue `#0389C3`, warm paper `#FBFAF7`
- The brochure's dot–line–dot rule as a recurring motif
- Serif headings (EB Garamond, standing in for the brochure's Minion Pro) over a
  sans-serif body (Inter) for on-screen readability
- The Europe map from the brochure cover, extracted as a clean background plate

Fully responsive (mobile / tablet / desktop), keyboard accessible, with
`prefers-reduced-motion` respected.

## Frozen: Prayer Marathon 28/30

The Prayer Marathon page is **frozen at the client's request** (brief of
2026-09-24, item 4.1) and is not built or linked anywhere. Nothing was deleted:

- page source — `src/frozen/marathon.html`
- map module — `assets/js/marathon.js`
- styles — the `Prayer Marathon 28/30` block in `assets/css/style.css`

To bring it back: move the page to `src/pages/`, restore the nav and footer links
in `src/layout.html`, correct the figures in the `DATA` array, and rebuild. The
map plots each nation from its real latitude/longitude onto a Mercator
projection, with the brochure's Europe map behind it as an `<image>` placed by
measuring that map's own projection — so if you change the projection bounds in
`marathon.js`, update the `<image>` geometry in the page to match.

## Multilingual readiness

The site ships in English and English lives in the markup, so pages stay readable
and indexable without JavaScript. Every translatable node carries `data-i18n`, and
`assets/i18n/en.json` is the reference dictionary of those keys.

To add a language later:

1. Add `assets/i18n/<code>.json` with the same keys.
2. Add the code to `SUPPORTED` in `assets/js/i18n.js`.
3. Add a language switcher that calls `NDOP.i18n.setLocale('<code>')`.

Missing keys fall back to the English already in the HTML.

## Building

Pages are assembled from `src/layout.html` plus the fragments in `src/pages/`, so
the header, navigation and footer exist in one place only. No dependencies.

```bash
python3 build.py     # regenerates the *.html in the repo root, plus sitemap.xml and robots.txt
```

Edit `src/pages/*.html` — never the generated files in the root.

To preview locally:

```bash
python3 -m http.server 8811
```

## Deployment

GitHub Pages serves the repository root on every push to `main`. `.nojekyll` is
present so that Jekyll does not touch the assets.

## Content still to be supplied by the movement

- **Board members' names.** `about.html` lists six board seats by country and
  remit (United States, Poland, Germany, Austria, Ukraine, United Kingdom) with
  no personal names, since none were supplied. Add each name where its seat is
  described, once the member has agreed to be named.
- **Corporate email address.** `info@ndop-europe.org` is a placeholder used in
  the page copy, the footer, the JSON-LD block and `assets/js/main.js`. Register
  the movement's own domain and replace it in those four places.
- **Contact form** — it currently opens the visitor's email client (`mailto:`), so
  the site needs no backend. Point it at Formspree, Netlify Forms or a small
  endpoint when server-side delivery is wanted.
- Higher-resolution originals of the brochure photographs, if available; the
  images here were extracted from the PDF and are limited to its print resolution.

## Changes from the brief of 2026-09-24

1.1 circle of twelve stars added to the blue banner of every page · 2.1 the navy
figures strip after the mission removed · 2.2 "at the state level" replaced
throughout with "at the country level" · 3.1 the 1588 Spanish Armada story
removed in full · 3.2 every remaining history entry expanded, with the US
federal / individual-state distinction spelled out · 3.3 Ukraine's first
observance in 2025 noted alongside the first intergovernmental service in 2026 ·
4.1 Prayer Marathon frozen · 4.2 the principles block laid out 3 x 2 · 5.1 all
personal names and phone numbers removed · 5.2 International Board block added.
