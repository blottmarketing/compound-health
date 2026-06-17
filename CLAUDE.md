# CLAUDE.md — Compound Health Website

Instructions for any agent (Claude or otherwise) working in this repository. Read this file at the start of every session before making changes.

## Project at a glance

- **Site name:** Compound Health
- **Production URL:** https://compoundhealth.io
- **Stack:** Astro 6 (static), vanilla CSS, GSAP for motion
- **Hosting:** static output from `npm run build` (`dist/`)
- **Folder location:** Google Drive shared folder (`Longevity Folder - G and A/Marketing & Presentations (external)/Website/compound-health`). Files saved here sync to Drive.

## Repo map

```
compound-health/
├── astro.config.mjs        # site: https://compoundhealth.io
├── package.json            # astro dev | build | preview
├── public/                 # static assets copied as-is to /
│   ├── favicon.* / og-image.*
│   ├── robots.txt          # references sitemap
│   └── sitemap.xml         # indexed pages only
├── src/
│   ├── data/
│   │   └── blog.ts             # authors, categories, posts — single source of truth for blog content
│   ├── layouts/
│   │   ├── MainLayout.astro          # marketing pages; supports `noindex` prop
│   │   ├── LegalLayout.astro         # privacy/terms; always indexed
│   │   ├── BlogLayout.astro          # blog/author/category; defaults to noindex (pre-launch)
│   │   └── DesignSystemLayout.astro  # /design-system/*; always noindex
│   ├── pages/                  # one .astro file per route
│   │   ├── index.astro
│   │   ├── privacy-policy.astro
│   │   ├── website-terms.astro
│   │   ├── overview-deck-june/index.astro   # private RIA deck, noindex
│   │   ├── design-system/                   # internal design system, all routes noindex
│   │   │   ├── index.astro                  # /design-system  overview
│   │   │   ├── atoms.astro                  # /design-system/atoms
│   │   │   └── molecules.astro              # /design-system/molecules
│   │   ├── blog/
│   │   │   ├── index.astro                  # /blog parent
│   │   │   ├── [slug].astro                 # /blog/<post-slug>
│   │   │   └── category/[category].astro    # /blog/category/<category-slug>
│   │   └── authors/
│   │       └── [author].astro               # /authors/<first-lastname>
│   └── styles/
│       ├── global.css                       # tokens + atoms + molecules — the live design system
│       └── design-system.css                # documentation chrome for /design-system/*
├── PAGES.xlsx              # source of truth for live page inventory
└── CLAUDE.md               # this file
```

## Standing operating instructions

1. **Always load full project context before doing work.** Before any edit, list `src/pages/`, open the relevant `.astro` files, and re-read this CLAUDE.md and `PAGES.xlsx`. Do not rely on assumed state from a prior session — the repo is the source of truth.
2. **`PAGES.xlsx` is the page inventory.** Every page on the site is listed there with its name, URL, status (Live / Draft / Archived), indexing (Indexed / Noindex), layout, and last updated. Update this file whenever a page is added, removed, renamed, or its indexing changes.
3. **`public/sitemap.xml` mirrors the indexed pages from `PAGES.xlsx`.** When a new indexed page ships, add it to the sitemap with today's `<lastmod>`. When a page is removed or switched to noindex, remove it from the sitemap. Never include noindex routes in the sitemap.
4. **Indexing rule.** A page is "indexed" by default. To make a page private, pass `noindex={true}` to `MainLayout` (or add a `<meta name="robots" content="noindex, nofollow" />` if using a different layout). Noindex pages must be excluded from `sitemap.xml` and listed as "Noindex" in `PAGES.xlsx`.
5. **Canonical URLs come from `astro.config.mjs` (`site:`).** Do not hardcode absolute URLs in templates.
6. **American English** in all prose. Compound Health is US-based and serves US clients, so the entire site uses American spelling (optimize, color, personalized, program, advisor). Legal copy already uses US spelling.
7. **No em dashes** in copy.

## Workflow when adding or changing a page

1. Create/modify the `.astro` file under `src/pages/`.
2. Confirm `noindex` is set correctly via the layout prop.
3. Update `PAGES.xlsx`: add the row or update status / indexing / last updated.
4. Update `public/sitemap.xml`:
   - If the page is indexed → add `<url>` entry with absolute URL and today's date in `<lastmod>` (YYYY-MM-DD).
   - If switching to noindex or removing the page → delete its `<url>` entry.
5. Run `npm run build` to confirm the site compiles.
6. Commit with a clear message referencing the page slug.

## Current page inventory (snapshot — `PAGES.xlsx` is the source of truth)

| Page | URL | Status | Indexing | Layout |
|---|---|---|---|---|
| Home | https://compoundhealth.io/ | Live | Indexed | MainLayout |
| Privacy Policy | https://compoundhealth.io/privacy-policy | Live | Indexed | LegalLayout |
| Website Terms | https://compoundhealth.io/website-terms | Live | Indexed | LegalLayout |
| RIA Overview Deck (June) | https://compoundhealth.io/overview-deck-june/ | Live | Noindex | MainLayout |
| Design System — Overview | https://compoundhealth.io/design-system | Live | Noindex | DesignSystemLayout |
| Design System — Atoms | https://compoundhealth.io/design-system/atoms | Live | Noindex | DesignSystemLayout |
| Design System — Molecules | https://compoundhealth.io/design-system/molecules | Live | Noindex | DesignSystemLayout |
| Blog — Index | https://compoundhealth.io/blog | Live | Noindex | BlogLayout |
| Blog Category — Research | https://compoundhealth.io/blog/category/research | Live | Noindex | BlogLayout |
| Blog Category — Insights | https://compoundhealth.io/blog/category/insights | Live | Noindex | BlogLayout |
| Blog Post — 6 dummy posts | https://compoundhealth.io/blog/<slug> | Live | Noindex | BlogLayout |
| Author — Imogen Asher | https://compoundhealth.io/authors/imogen-asher | Live | Noindex | BlogLayout |
| Author — Henry Cavendish | https://compoundhealth.io/authors/henry-cavendish | Live | Noindex | BlogLayout |

## Design system

The site has a single source of truth for visual style. Use it. Do not invent new tokens, sizes or button variants inline.

- **Live system lives in `src/styles/global.css`.** All tokens (colour, type, spacing), atoms (buttons, eyebrows, badges, inputs, avatars, dividers, links) and molecules (step card, plan card, feature card, metric row, post card, author chip, form field, mobile menu link, case stat, case quote card, testimonial, breadcrumb, author panel) are defined there.
- **Documentation lives at `/design-system`.** Three routes, all noindex via `DesignSystemLayout`:
  - `/design-system` — overview and working rules.
  - `/design-system/atoms` — colour, typography, spacing, radii, buttons, badges, eyebrows, dots, avatars, dividers, inputs, links, motion.
  - `/design-system/molecules` — every reusable block on the site, with code snippets.
- **Methodology.** Atomic design (atoms → molecules → organisms → templates → pages) combined with [Finsweet Client-First](https://finsweet.com/client-first) naming. Class names are lowercase, hyphen-separated, with `is-active` / `is-open` for state and modifier classes like `.is-good`, `.is-warn`, `.tone-sage` for variants.
- **Rules.**
  1. Every visual change starts in `global.css`. If a token, atom or molecule does not exist for what you need, add it before using it.
  2. Do not inline colours, sizes or backgrounds on elements. Width values that come from data (e.g. `.metric-fill style="width:82%"`) are the only legitimate use of inline `style`. Colours always come from a class.
  3. When you add a new atom or molecule to `global.css`, add a documentation block to the corresponding `/design-system` page in the same commit.
  4. All `/design-system/*` routes must stay noindex and out of `public/sitemap.xml`.
- **Status modifiers shipped with the system.** `.metric-fill.is-good` (sage) and `.metric-fill.is-warn` (gold) replace the previously inline metric colours in `index.astro`.

## Blog system

The blog is pre-launch. Every route under `/blog`, `/blog/category/*` and `/authors/*` is currently **Noindex** via `BlogLayout`'s default `noindex={true}`. None of these routes appear in `public/sitemap.xml`.

- **Content lives in `src/data/blog.ts`.** This file holds typed `Author`, `Category` and `Post` collections. To add or edit a post, author or category, edit this file. Do not introduce a separate CMS layer without a discussion.
- **Slugs are the URL.** Author slugs are `first-lastname`. Category slugs are short, lowercased nouns. Post slugs are kebab-case.
- **Authoring posts.** `bodyHtml` is raw HTML. Stick to `<h2>` and `<p>`. The post body inherits the `.prose` styles in `global.css`.
- **American English** in all blog copy, per project standing instructions.
- **When launching the blog publicly:** pass `noindex={false}` on the relevant `BlogLayout` instances (or change the layout default), add each newly-indexed route to `public/sitemap.xml`, and flip its row in `PAGES.xlsx` from `Noindex` to `Indexed`.

## Commands

- `npm run dev` — local preview at http://localhost:4321
- `npm run build` — static build to `dist/`
- `npm run preview` — preview the built output

## Things to leave alone unless asked

- `node_modules/`, `.astro/`, `dist/` — generated.
- GSAP version pinned via CDN in `MainLayout.astro`.
- Favicon set and `og-image.*` — fixed assets.
