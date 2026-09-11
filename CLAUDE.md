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
│   │   ├── blog.ts             # authors, categories, posts — single source of truth for blog content
│   │   └── variants.ts         # home page design variations — single source of truth for the switcher
│   ├── components/
│   │   └── variants/                     # used by the variations only, never by the live site
│   │       ├── Logo.astro                # mark + wordmark lockup, takes a `base` route
│   │       ├── Footer.astro              # three-column footer with landscape art, takes a `base` route
│   │       ├── VariantSwitcher.astro     # the fixed pill for moving between variations
│   │       └── V2ThemeSwitcher.astro     # v2 only: the pill for its three colour themes
│   ├── layouts/
│   │   ├── MainLayout.astro          # live marketing pages; supports `noindex` prop
│   │   ├── LegalLayout.astro         # privacy/terms; always indexed
│   │   ├── BlogLayout.astro          # blog/author/category; defaults to noindex (pre-launch)
│   │   ├── DesignSystemLayout.astro  # /design-system/*; always noindex
│   │   └── variants/
│   │       ├── V1Layout.astro           # variation v1; loads styles/variants/v1.css, always noindex
│   │       ├── V11Layout.astro          # variation v1.1; loads styles/variants/v1-1.css, always noindex
│   │       ├── V2Layout.astro           # variation v2; loads styles/variants/v2.css, own dark footer, always noindex
│   │       ├── V3Layout.astro           # variation v3; loads styles/variants/v3.css, glass nav pill, own footer, always noindex
│   │       └── VariantStubLayout.astro  # placeholder for a variation not started yet
│   ├── pages/                  # one .astro file per route
│   │   ├── index.astro                      # the live home page
│   │   ├── privacy-policy.astro
│   │   ├── website-terms.astro
│   │   ├── for-advisors.astro
│   │   ├── overview-deck-june/index.astro   # private RIA deck, noindex
│   │   ├── v1/index.astro                   # design variation v1, noindex
│   │   ├── v1-1/index.astro                 # design variation v1.1, forked from v1, noindex
│   │   ├── v2/index.astro                   # design variation v2, the joindawn.com idiom, noindex
│   │   ├── v3/index.astro                   # design variation v3, the lassie.ai idiom, noindex
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
│       ├── design-system.css                # documentation chrome for /design-system/*
│       └── variants/
│           ├── v1.css                       # the v1 system, loaded by /v1 only
│           ├── v1-1.css                     # the v1.1 system, Bayshore-influenced, loaded by /v1-1 only
│           ├── v2.css                       # the v2 system, the joindawn.com idiom, loaded by /v2 only
│           └── v3.css                       # the v3 system, the lassie.ai idiom, loaded by /v3 only
├── docs/
│   ├── v1-1-art-brief.md   # the brief for the two v1.1 renders, and how to drop them in
│   └── v3-art-brief.md     # the seven v3 photography slots, their prompts, and how to drop them in
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
| Design v1 | https://compoundhealth.io/v1 | Live | Noindex | V1Layout |
| Design v1.1 | https://compoundhealth.io/v1-1 | Live | Noindex | V11Layout |
| Design v2 | https://compoundhealth.io/v2 | Live | Noindex | V2Layout |
| Design v3 | https://compoundhealth.io/v3 | Live | Noindex | V3Layout |

## Design variations

`/` is the design that ships. Candidate redesigns of the home page live on their own routes, so the live site and every candidate can be opened side by side. This was set up on 2026-09-07, when the Duna-idiom redesign moved off `/` and onto `/v1`.

- **`src/data/variants.ts` is the source of truth.** It lists the live design plus every variation, with a label, a route, a one-line note and a status of `ready` or `planned`. The switcher reads it; so do the placeholder pages. Add a row here first.
- **Nothing is shared between a variation and the live site except content and public assets.** Each variation has its own stylesheet under `src/styles/variants/` and its own layout under `src/layouts/variants/`. `src/styles/global.css`, `src/layouts/MainLayout.astro` and the live `src/pages/index.astro` belong to production and are not to be touched while working on a variation. That separation is the point: a variation must be changeable without any risk to `/`. The live page's only departure from `main` is the switcher at its foot, and that is temporary.
- **Variations are noindex, always.** Their layouts hard-code `<meta name="robots" content="noindex, nofollow" />`, they are excluded from `public/sitemap.xml`, and each route is listed under `Disallow:` in `public/robots.txt`. No canonical tag either, so a stray crawl cannot fold a variation into `/`.
- **The switcher.** `src/components/variants/VariantSwitcher.astro` is a fixed pill at the foot of the live page and every variation, listing Live plus each variation. It carries its own scoped styles and uses no design tokens, so it renders identically on top of any design and can never be the reason two variations differ. It rides along on `/` because the whole set lives on the `redesign` branch for review; that is the one non-production thing on the live page, and it comes off before anything ships (delete the import and the `<VariantSwitcher current="live" />` at the foot of `src/pages/index.astro`).
- **In-page links inside a variation take a `base`.** `V1Layout`, `Logo` and `Footer` accept a `base` prop (`/v1`), and every anchor is built from it, so navigating inside a variation never drops the reviewer onto the live page. Links that genuinely leave the variation (legal, `for-advisors`, mail) stay absolute.
- **Starting a new variation.** Set the row in `variants.ts` to `ready`, add `src/styles/variants/<v>.css` and `src/layouts/variants/<V>Layout.astro` (copy the closest existing pair), then replace `src/pages/<v>/index.astro`. Never point two variations at one stylesheet. v1.1 was forked from v1 this way on 2026-09-07: an exact copy of the page, the layout and the stylesheet, iterated from there. Two variations with identical stylesheets are served one shared CSS asset because Vite hashes by content; the moment one changes it gets its own. The source files are separate regardless, which is what matters.
- **Copy is the client's, in every variation.** A variation changes layout and visual system, not words. See rule 7 below.

## Design system

Each design has one source of truth for visual style. Use it. Do not invent new tokens, sizes or button variants inline.

- **Live system lives in `src/styles/global.css`.** All tokens (colour, type, spacing), atoms (buttons, eyebrows, badges, inputs, avatars, dividers, links) and molecules (step card, plan card, feature card, metric row, post card, author chip, form field, mobile menu link, case stat, case quote card, testimonial, breadcrumb, author panel) are defined there. It is the system behind `/`, the legal pages, the blog, `for-advisors` and the deck, and it is what `/design-system` documents.
- **The v1 system lives in `src/styles/variants/v1.css`,** loaded by `/v1` alone. Rules 3 to 7 below describe that system, not the live one. It is not documented under `/design-system` yet; when v1 is chosen, its documentation moves there in the same pass.
- **The v1.1 system lives in `src/styles/variants/v1-1.css`,** loaded by `/v1-1` alone. It answers the client's feedback of 2026-09-07, that v1 did not feel premium, by blending v1's structure with [bayshore.ai](https://www.bayshore.ai/). Same sections, same copy, same layout skeleton as v1; everything else differs:
  1. **Bayshore's palette, lifted from their own swatches.** Ground bone `#F2EFEB`, ink `#1B1B1A`, warm greys down to `#6F6D69`, accent chestnut `#6D464C`, and the environment colours dusk blue `#2E558B`, sand `#EACBA6`, beige `#D4C1AB`, lavender `#EFEBF1`, deep stone `#2E2124`. The brand green is gone from this variation entirely. The primary action is near-black, as theirs is; chestnut is for links, marks and hovers.
  2. **Gradient environments, not flat bands.** `--hero-grad` is dusk sky into sand, resolving to the ground at its last stop so the section below joins with no seam. `--cta-grad` runs the same sky into chestnut and sand. `--panel-grad` is quarried stone. Those three, plus `--footer-grad`, are the only places the blue and the sand appear.
  3. **Square, not rounded.** Every radius is 0 except circles (dots, avatars, rings). No pills anywhere: buttons, chips, cards and panels are rectangles.
  4. **Labels are Roman caps.** `.s-chip` and `.step-n` are Cinzel, letterspaced, uppercase, no fill and no box, which is Bayshore's own secondary face. Display type is one weight at line-height 1.0 and -0.045em; there is no italic anywhere, so emphasis in a heading carries in sand instead.
  5. **The bento is a divided plane.** Cells touch on a 1px ground gap, and one cell (`.tone-stone`) is a deep panel carrying cream copy. Three pastels of equal value is what made v1 read flat. The other two tones are `.tone-sand` and `.tone-lavender`.
  6. **The nav inverts over the hero.** Cream logo, mark and links while the bar is transparent; ink on bone once scrolled.
  7. **Both renders are in,** from the prompts in `docs/v1-1-art-brief.md`: one marble-and-sand world at one hour. `public/images/v1-1/hero-monolith.webp` is a marble tree under a dusk sky, mirrored in CSS (`.hero-img { transform: scaleX(-1) }`) because the render puts the tree left of centre and the copy needs that side. `public/images/v1-1/footer-stone.webp` is the same world on a low horizon, its near-white sky carrying the link columns and its marble foreground under the `.footer-media::after` vignette, where the legal row is cream. Its top 20% was flattened to the ground colour `#F2EFEB` in the asset, ramping back to the render by 42%, so the join with the section above holds at any viewport even though `object-position: center bottom` crops the top on wide screens. Fix an edge like that in the image, never with a CSS fade over it.
  8. **The hero copy is anchored high and left, not centred.** It has to clear the tree canopy and the bright sand band, where cream type disappears. The quiet link at the foot of the block always lands on the sand, so it is ink on desktop and cream only under 900px, where the art moves below the copy and the hero shortens its gradient to meet the top of the render. The image meets the page ground on a hard edge, which is Bayshore's own move; it is not a fade, and it is not the Duna rule that the transition into white lives in the artwork. That rule belongs to v1.
- **The v2 system lives in `src/styles/variants/v2.css`,** loaded by `/v2` alone, built 2026-09-07. It follows [joindawn.com](https://joindawn.com): their layouts, palette, type, motion and interactions, with the client's copy unchanged. Nothing is shared with v1 or v1.1 beyond the `Logo` component and the switcher.
  1. **Dawn's warm scale.** Cream `#FBF3EB`, sand `#F8E7D5`, peach `#FACE9F`, orange `#FF9C31`, amber, gold, yellow `#FBC81C`, burnt `#C36500`, cocoa `#5B3205`, ink `#321C04` (which is also the dark ground), plus a sky blue pair for the closing card. Text is ink or cream; muted text is ink at 70%.
  2. **Type.** Source Serif 4 (regular, with italic for `em`) for every heading and figure; Figtree for reading, labels and buttons; Lato only in the wordmark. Eyebrows are 12px caps letterspaced 0.2em with no box.
  3. **The page opens dark and the sun comes up.** The hero is two rounded cards on the ink ground inside a 0.5rem inset: the warm gradient card carries the headline, the photo card carries the standfirst and actions, and one circle spans both, dotted on the left and solid on the right. Then `.scroller` (260vh) pins a stage in which a gradient arc draws itself around a dotted ring as the reader scrolls (GSAP ScrollTrigger, scrubbed) with the "process" head in burnt orange, and `.sunrise` (a fixed-height gradient from ink through orange and yellow to cream) hands the page to the light ground, with the three step cards sitting at its foot.
  4. **Stacked sections with rounded feet.** Every section from the sunrise on is `.stack`: a 5rem bottom radius, pulled up under the section above by the same amount, with descending z-index classes (`.z7` down to `.z1`) so each lies over the next. Grounds alternate cream, sand, the brown gradient (`.bg-brown.is-dark`), sand with a silk sheen (`.silk`), cream.
  5. **Cards, pills, discs.** `.card` is cream with a 1px white edge and a 1.25rem radius; `.is-lift` raises it on hover. Every primary action is `.btn-primary`, Dawn's radial orange-to-gold pill, and every button scales to 0.95 on hover. `.tag-brand` is the gradient chip. `.disc` is the peach icon circle. `.pill-past` (dim, dashed) and `.pill-glow` (gradient, glowing, blurred in by scroll) are Dawn's past-and-future contrast; on v2 they carry the "what you get" standfirst's own words.
  6. **Figures.** `.chat` in the wide feature card is a thread of gradient bubbles carrying the sentence's three verbs. `#disciplines` is a tablist of gradient pills driving one cream card with chips lifted from the discipline's sentence. `#audiences` is the coverflow carousel of the four audience cards (arrows, keys, swipe). The closing `.sky` card is a CSS sky with drifting clouds and a second scroll-drawn arc; the form sits beneath it on cream. The footer is Dawn's plain dark block, written in `V2Layout`.
  7. **Motion.** Arcs and the stage copy are scrubbed by scroll; everything else is a one-shot `.reveal`. The bar hides on the way down, returns on the way up, frosts once scrolled, and turns ink over the light ground via the `[data-nav-light]` sentinel. Reduced motion draws the arcs in full and disables the scrubs.
  8. **Three colour themes, one structure.** Every colour in `v2.css` is a token, including the rgb triplets for translucent uses (`--ink-rgb`, `--cream-rgb`, `--glow-rgb`, `--tint-rgb`) and the stops of the brown, deep and sunrise gradients (`--brown-*`, `--deep-*`, `--sun-*`); the SVG gradient stops in the page are coloured from CSS too. `html[data-theme="sage"]` (forest, moss, lime: the brand green) and `html[data-theme="dusk"]` (midnight, lavender, rose, champagne) override the colour tokens only, never a size or a layout; Dawn is the default. `V2ThemeSwitcher` is the fixed pill bottom-right that sets `data-theme`, remembers it in localStorage (`ch-v2-theme`) and honours `?theme=<id>` in the URL; `V2Layout` applies the saved theme in `<head>` before first paint. When adding a colour to v2, add it as a token and give every theme a value.
- **Documentation lives at `/design-system`.** Three routes, all noindex via `DesignSystemLayout`:
  - `/design-system` — overview and working rules.
  - `/design-system/atoms` — colour, typography, spacing, radii, buttons, badges, eyebrows, dots, avatars, dividers, inputs, links, motion.
  - `/design-system/molecules` — every reusable block on the site, with code snippets.
- **Methodology.** Atomic design (atoms → molecules → organisms → templates → pages) combined with [Finsweet Client-First](https://finsweet.com/client-first) naming. Class names are lowercase, hyphen-separated, with `is-active` / `is-open` for state and modifier classes like `.is-good`, `.is-warn`, `.tone-sage` for variants.
- **Rules.**
  1. Every visual change starts in the stylesheet of the design you are working in: `global.css` for the live site, `src/styles/variants/<v>.css` for a variation. If a token, atom or molecule does not exist for what you need, add it before using it. Never edit `global.css` to serve a variation.
  2. Do not inline colours, sizes or backgrounds on elements. Position values that come from data (e.g. `.metric-lead style="width:82%"` and `.metric-mark style="left:82%"`) are the only legitimate use of inline `style`. Colours always come from a class.
  3. **One ground (v1).** The v1 page runs on `--warm-white` end to end. `--panel` (#F1EFEA) is the neutral fill for cards; there is no `--panel` section band any more. The product panel (`.prod-panel`) is painted with `--panel-grad`, a pale sweep of the bento tints. Colour lives inside cells and cards only: the three tints (`--tint-green`, `--tint-orange`, `--tint-pink`, each with an `-ink` and a `-deep` partner) go on `.bento-cell` via `.tone-*`, and a tinted cell is monochrome. Yellow and violet were tried and dropped; do not reintroduce them. The closing section (`.cta`, id `joinwaitlist`) pairs the gradient card (`.cta-card`, a mesh of the three tints with white copy: the closing message at the top, the `Get access` invitation at the foot, no button because the form is the action) with the access form beside it on the ground. `.btn-dark` is the charcoal pill for the standalone card on the advisors page and the deck. `.footer-cta` is the same card standing alone on the advisors page and the deck. That card is the one gradient surface; do not add a background band to any section.
  4. **Fills and hairlines, never outlines (v1).** Group content with a fill or with `--hair` hairlines on the top and left of grid cells. Do not wrap a grid in a bordered, rounded box. Form controls sit on `--hair` too, as warm-white fields with no card around them. `--border`, the green-tinted line, is not used on the v1 page.
  5. **Section heads use `.s-head` (v1).** Chip, title, standfirst, and an optional `.s-head-action` pill that carries a real destination. `.s-label`, the older uppercase label, is what the live system uses on the home, legal, blog and deck pages.
  6. **Two section patterns, never the same one twice in a row (v1).** `.bento` is a six-column grid of tinted cells of unequal size, one row of a wide cell and a half, then a row of three halves (used by "what you get"). The health score card was pulled from it on 2026-09-04; `.bars` stays in the system. `.prod` is the interactive two-column pattern: a `role="tablist"` of choices on the left driving a card in a soft panel on the right (used by "how we choose"). Every label inside a panel or card is lifted verbatim from copy already in that section: a panel illustrates copy, it never introduces new copy.
  7. **Copy is the client's.** Do not rewrite, shorten, add or remove marketing copy, headings or CTA labels while doing visual work. If a layout needs different words, raise it rather than changing them.
  8. When you add a new atom or molecule to `global.css`, add a documentation block to the corresponding `/design-system` page in the same commit. A variation's stylesheet is not documented there until that variation is chosen.
  9. All `/design-system/*` routes must stay noindex and out of `public/sitemap.xml`.
- **Product cards are glass (v1).** `.stack-card` and `.bento-card` are `--glass-card` with a bright hairline edge, backdrop blur and an ambient shadow. The health score is `.bars`: gradient columns on one 0 to 100 plot, `.is-good` green (`--grad-cool`), `.is-warn` orange (`--grad-warm`), `.is-peak` glowing, and `--v` on `.bar` the only inline value. The panel figures are the team bar (`.team-bar` + `.team-legend`), the ring (`.cov-ring` of six `.cov-arc`) and the gradient card (`.stack-card.is-feature` with `.gate-chip` and `.gate-flow`). `.metric-*` and `.vault-*` no longer exist.
- **Visual reference (v1).** v1 follows [duna.com](https://duna.com). Its idiom: one ground, fills and hairlines instead of outlines, a chip-plus-title section head with a pill action, product panels alternating sides, generous air, and per-block scroll reveal.
- **Visual reference (v2).** v2 follows [joindawn.com](https://joindawn.com). Its idiom: a dark opening, a split hero of rounded cards, one great circle drawn by scroll, a sunrise gradient into cream, stacked sections with rounded feet, serif display type, gradient pills, a coverflow carousel and a sky card.
- **Visual reference (v3).** v3 follows [lassie.ai](https://www.lassie.ai/). Its idiom: one cream ground and no bands, no shadows and no hairlines, a light serif display at 350 with nothing above it, a floating glass nav pill, scroll used as a mechanism rather than as decoration, drawn product figures where other designs would put a photograph, DM Mono reserved for machine facts, and a giant wordmark on pale blue under a rounded-foot footer.

- **The v3 system lives in `src/styles/variants/v3.css`,** loaded by `/v3` alone, built 2026-09-10. It follows [lassie.ai](https://www.lassie.ai/): their layouts, palette, type, motion and interactions, with the client's copy unchanged. Nothing is shared with v1, v1.1 or v2 beyond the `Logo` component and the switcher.
  1. **One ground, no bands.** `--bg-primary` (`#F9F8F5`) runs the whole page. Sections are separated by air alone, 100px rising to 200px at desktop, never by a change of background. White is the surface of everything raised; `--stone-300` (`#F3F0E9`) is the one second ground and it is always a card, never a band. Warm-black `#1A1613` is the text, `#120C08` the dark fill, `#666666` the muted. The pale blue `#C3EAF4` appears only as sky (the wide panel, the footer band) and as focus. Colour otherwise comes only from photography and from the drawn figures.
  2. **`font-size: 62.5%` on `html`,** so 1rem is 10px and every value in the stylesheet is authored in whole tens of a pixel, as the reference does. Do not change it without rewriting the file.
  3. **Three faces.** Newsreader at weight 350 stands in for ABC Marist, the reference's commercial display serif: a variable axis so the display sits on 350 exactly, a low x-height against a generous cap, and a true italic. DM Sans reads, DM Mono is the machine voice and appears exactly twice, on a figure and on the colophon. Lato still carries the wordmark. Emphasis inside a heading is the serif italic, never a weight or a colour.
  4. **No shadows, no borders, no hairlines in the layout.** Elevation is radius and fill. Two shadow strings exist in the whole system and one of them is the focus ring. Form controls are fills rather than outlines. Focus is a design element: 2px `#42B5DC` plus a 3px halo, on everything.
  5. **No entrance animation anywhere.** There is no fade-up, no stagger and no per-block reveal; both the CSS study and the live interaction study of the reference confirmed it. Everything outside a pinned stage sits still at full opacity, and that is what makes the scrubbed set pieces read as events. The only one-shot entrances are the mark drawing itself and the figure counting, both of which the reference also plays once on enter.
  6. **Scroll is a mechanism, not an effect.** Three set pieces carry all the motion, driven by GSAP ScrollTrigger over Lenis (`lerp: 0.2`, on the GSAP ticker, `lagSmoothing(0)`, exposed as `window.__lenis` so a headless capture can jump): the hero window closes from `inset(0)` to `inset(32px round 64px)` over 1s `cubic-bezier(.22,1,.36,1)` while the picture stays still; `.car` pins a stage in which three panels deal like a deck, the front one leaving upward as the next arrives from below (dropped below 1024px, where the reference stacks them too); and `.orbit` pins a stage in which six tiles are parked on a scroll-scrubbed ellipse around a line that leaves as the next arrives, each photograph counter-scaling its own image 2 → 1 so the crop settles rather than pops.
  7. **The nav is a floating glass pill,** not a bar: `w-max`, centred, 16px down, `rgba(227,221,207,.4)` behind `blur(13px)`, never hiding and never changing colour. A white indicator follows the pointer; the wordmark collapses to the mark past `scrollY` 400 and comes back at 360. Below 1024px the four section links move into a small glass card that drops from under the pill, and below 760px the wordmark gives up its space to the mark. Four details the bar got wrong and that are worth not reintroducing: the indicator is white, so whatever it sits under goes ink, or the label is white on white over the hero; it appears and disappears by fading where it stands, never by growing or collapsing onto its own left edge; it is repositioned on every frame of the wordmark's collapse, or it keeps a stale width and leaves a white slab around a lone mark; and the wordmark's 0.9rem of space is its own `margin-left` rather than a flex `gap`, because a gap survives a zero-width child and leaves the collapsed lockup with 14px on one side and 23px on the other.
  7b. **One motion scale for the whole variation.** `--t-tint` (0.18s) for colour, opacity and fill; `--t-move` (0.32s) for position, size and transform; `--ease-out-quint` for both, which is the same curve GSAP calls `power4.out`, so the stylesheet and the scripts move together. Three curves and five durations across the same kinds of interaction is what makes motion feel unconsidered even when each piece is fine on its own. The deliberate outliers are the reference's own and are all on the same curve: the hero window at 1s, the hero ticker at 0.68s, and the mark drawing itself at 1.6s. Scrubbed timelines have no duration of their own; their numbers are timeline units.
  8. **The footer stands on a fixed panel.** A white block with 64px feet, and beneath it a fixed gradient panel carrying the wordmark in white serif at almost the full page width, uncovered by the footer's own `margin-bottom: 30vw` scrolling past it. No script.
  9. **The figures are drawn, never photographed.** `fig-`, `dcard-` and `disc-` are the three families: three product-interface panels for the process steps, four data cards for the orbit, three discipline squares, two wide panel figures, and one stroke-only icon set at 1.4. They scale by a container-query unit `--u` against a nominal design box, so a composition can never push its frame out of shape. Every word inside a figure is lifted verbatim from that section's copy and every number is a neutral illustrative reading.
  10. **Photography: all four renders are in** (2026-09-11), at `public/images/v3/`, wired through four nullable constants at the top of the page so a slot falls back to its placeholder if a file is ever removed. The register is tended ground at first light and the private rooms that serve it: no faces, no props, one light and one hour, mostly empty frames because a card or a headline sits on each. The hero and the closing frame carry white type, and the rule is that their darkness lives in the file: never a scrim, never a gradient over a picture. Both needed a highlight rolloff after delivery, done in linear light with the shadows untouched, and the closing frame also gave up its top 18% because the white mark was landing on sky. The slots, the prompts and the treatment each file received are in `docs/v3-art-brief.md`. The three `step-*` prompts in that brief are unused: those frames are drawn.
  11. **One deliberate departure from the reference.** It puts nothing above a heading, and the client's copy names every section. The label is `.sec-label`: the mono voice at 12px, no box, no caps, no letterspacing, which is the quietest thing this system can do with a word that has to be there.

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
