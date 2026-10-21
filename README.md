# The National Days of Prayer Movement in Europe

Static website for the movement encouraging the establishment of a National Day of
Prayer at the country level in every European country.

**Live demo:** https://nationaldayofprayer.eu/

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

### Light and dark themes

The header carries a sun/moon toggle. **Light is the default** — it is the
brand look from the brochure — and a visitor's choice is remembered in
`localStorage` under `ndop.theme`. An inline script in `<head>` applies the
stored theme before the page paints, so a dark-theme visitor never sees a white
flash between pages.

Only design tokens change between themes; no component is restyled. The light
set lives on `:root` in `assets/css/style.css`, the dark set on
`:root[data-theme="dark"]` directly below it. Two rules matter when editing:

- `--navy` is a **surface** colour (hero, banners, footer). Heading *text* uses
  `--heading`, which flips to near-white in dark. Never colour text with
  `--navy`.
- Card and panel backgrounds use `--surface`, not a literal `#fff`. The only
  deliberate exceptions are the framed document scans, which stay on white
  paper in both themes so they remain readable.

To make the site follow the visitor's OS setting instead of defaulting to
light, add a `prefers-color-scheme` check to the inline script in
`src/layout.html`.

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

## The WordPress theme

The movement's owner asked for WordPress, so the same site is also a theme in
`wp-theme/`. It is not a port: the design system in `assets/css/style.css` is
shared **unchanged** between the two, and the words come from the same
`content/*.json`. Everything WordPress makes necessary lives in one extra file,
`wp-theme/ndop/assets/css/wp.css`.

| | |
|---|---|
| `wp-theme/ndop/` | the theme — templates, `functions.php`, `theme.json` |
| `wp-theme/blocks.py` | writes Gutenberg block markup |
| `wp-theme/pages_*.py` | one module per page |
| `wp-theme/build.py` | content -> `pages/*.html`, `inc/meta.php`, `inc/captions.php` |
| `wp-theme/pack.sh` | assembles the theme and zips it for upload |

```bash
cd wp-theme && ./pack.sh     # -> ndop.zip
```

Only sources are in git. The photographs, the brochure, `style.css`, `main.js`
and everything `build.py` writes are assembled by `pack.sh` from files that are
already in the repository, so there is never a second copy to drift.

Install the zip through **Appearance -> Themes -> Upload**. On activation the
theme imports the photographs into the media library and creates the six pages
itself (`inc/setup.php`), which is why the move can be repeated on the live
domain with the same result. **Tools -> NDOP content** runs it again; a second
button there rewrites the pages from the theme, discarding any editing.

### What the client can change

Page content is ordinary Gutenberg blocks, so a page is edited by clicking the
text on it. Every section carries `lock: {move, remove}`, and arrangements that
have to stay put — the three benefit columns, a card row, a timeline entry —
carry `templateLock: all`. Words and photographs can change; the layout cannot.
The footer verse sits in the Customizer, under **Footer**.

### Four things that will bite whoever edits this next

- **`theme.json` is not optional.** Without it WordPress wraps the contents of
  every group block in `.wp-block-group__inner-container`, that wrapper becomes
  the only child of each grid, and every row collapses into one column. The file
  also switches `blockGap` off, which otherwise adds 24px between everything.
- **A core image block is a `<figure>`.** Inside the fixed-height card plate the
  figure is removed from the box tree with `display:contents`, so the picture is
  the grid item again and `max-height` still means what it meant before.
- **Saved block markup must be exactly what the block would save.** An extra
  `loading` attribute, or an `anchor` attribute without the matching `id="…"`,
  and the client is shown "this block contains unexpected or invalid content".
  That is why `data-lightbox` is not stored in the page: a container asks for it
  with the class `is-zoomable` and `ndop_mark_zoomable_images()` adds it while
  the page renders, with the caption read from the media library.
- **LiteSpeed Cache serves the old page.** Purge it, or add a query string, or
  you will check a change that never reached you.

## Multilingual readiness

The site ships in English and English lives in the markup, so pages stay readable
and indexable without JavaScript. Every translatable node carries `data-i18n`, and
`assets/i18n/en.json` is the reference dictionary of those keys.

To add a language later:

1. Add `assets/i18n/<code>.json` with the same keys.
2. Add the code to `SUPPORTED` in `assets/js/i18n.js`.
3. Add a language switcher that calls `NDOP.i18n.setLocale('<code>')`.

Missing keys fall back to the English already in the HTML.

## How the site is put together

Three layers, so that words can be changed without touching markup:

| | | |
|---|---|---|
| `content/*.json` | the words and pictures | edited by the client through `/admin` |
| `src/pages/*.html` | the shape of each page | edited by a developer |
| `src/layout.html` | head, header, footer | edited by a developer |

`build.py` renders the templates with the content and writes the finished pages
to the repo root. It has no dependencies — a tiny substitution engine does the
work:

- `{{ field }}` — insert a value
- `{{#list}} … {{/list}}` — repeat for each item; a list of plain strings is
  addressed as `{{value}}` inside the block
- `{{?field}} … {{/?field}}` — include only when the field has a value

```bash
python3 build.py     # regenerates the *.html in the root, plus sitemap.xml and robots.txt
```

Never edit the generated `*.html` in the root — the next build overwrites it.

## Editing the content (for the client)

`/admin` is an editing interface ([Sveltia CMS](https://github.com/sveltia/sveltia-cms),
configured in `admin/config.yml`). The editor signs in with a GitHub account,
picks a page, changes text or uploads a photograph, and presses Save. That
commits to `main`, which rebuilds and republishes the site.

Only content is exposed there — no layout, no styling, no code. When adding a
field to `content/*.json`, add it to `admin/config.yml` too, or the client will
not see it.

Images uploaded through the CMS land in `assets/img`. Ask the client to keep
them under roughly 500 KB; nothing enforces it.

The admin page needs a GitHub OAuth endpoint to sign in. On Cloudflare that is
the `sveltia-cms-auth` worker; it is free and takes a few minutes to deploy.

To preview locally:

```bash
python3 -m http.server 8811
```

## Deployment

GitHub Pages serves the repository root on every push to `main`. `.nojekyll` is
present so that Jekyll does not touch the assets.

**Custom domain:** `nationaldayofprayer.eu`, set by the `CNAME` file at the repo
root. Keep that file — a rebuild does not recreate it. The domain is registered
through imena.ua, and the DNS records it needs are:

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `newhope77.github.io.` |

`prayforeurope.eu` is the movement's second domain and should be set to a 301
redirect to `nationaldayofprayer.eu` at the registrar, not pointed at Pages —
two domains serving the same pages would read as duplicates to search engines.

Once DNS resolves, turn on **Enforce HTTPS** in the repository's Pages settings;
GitHub issues the certificate itself, which takes a few minutes after the
records propagate. `SITE_URL` in `build.py` drives the canonical URLs, the
sitemap and robots.txt, so it must match the live domain.

## Content still to be supplied by the movement

- **Board members' names.** `about.html` lists six board seats by country and
  remit (United States, Poland, Germany, Austria, Ukraine, United Kingdom) with
  no personal names, since none were supplied. Add each name where its seat is
  described, once the member has agreed to be named.
- **A mailbox for `info@nationaldayofprayer.eu`.** The address is now used in the
  page copy, the footer, the JSON-LD block and `assets/js/main.js`. The domain's
  MX already points at `mail.imena.com.ua`, but the mailbox itself still has to
  be created in the imena.ua panel — until it exists, mail to it bounces.
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
