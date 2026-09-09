# The National Days of Prayer Movement in Europe

Static website for the movement encouraging the establishment of a National Day of
Prayer at the state level in every European country.

**Live demo:** https://newhope77.github.io/ndop-europe/

---

## What is here

| Page | File | Contents |
|---|---|---|
| Home | `index.html` | Hero, mission, benefits (society / state / churches), history preview, the Ukrainian precedent, call to action |
| About Us | `about.html` | Who the movement is, its principles, what it does, coordinator |
| History | `history.html` | 13-moment timeline, 1571 → 2026, with a lightbox for every image |
| Resources & Legal Base | `resources.html` | US precedents and Public Law 100-307, Ukraine's 2025 resolution, the seven practical steps, downloads |
| FAQ | `faq.html` | 10-question accordion |
| Prayer Marathon 28/30 | `marathon.html` | Interactive map of 30 nations over 28 days, with filters, search and a detail panel |
| Contact | `contact.html` | Coordinator details, audience-specific notes, enquiry form |

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

## The interactive map

`assets/js/marathon.js` plots each nation from its real latitude/longitude onto a
Mercator projection. The brochure's Europe map sits behind it as an `<image>`
whose placement was derived by measuring the brochure map's own projection
(Iceland and the Iberian peninsula as control points), so the markers land on the
correct country without shipping a country-outline dataset.

If you change the projection bounds in `marathon.js`, update the `<image>`
geometry in `src/pages/marathon.html` to match.

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

- **Prayer Marathon 28/30** — the day assignments, per-country prayer focuses and
  initiative statuses in `assets/js/marathon.js` are illustrative placeholders
  built to the right shape. Replace the `DATA` array with the real schedule.
- **Contact form** — it currently opens the visitor's email client (`mailto:`), so
  the site needs no backend. Point it at Formspree, Netlify Forms or a small
  endpoint when server-side delivery is wanted.
- Higher-resolution originals of the brochure photographs, if available; the
  images here were extracted from the PDF and are limited to its print resolution.
