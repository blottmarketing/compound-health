#!/usr/bin/env python3
"""
Port the client's flattened HTML drop into the Astro source tree.

The client delivers the finished site as self-contained HTML files, one per page,
each carrying the whole design system, the fonts and the photographs inline. This
script splits a drop back into the tree it came from:

    client_resources/final_version/compound-health-v1.html  -> src/pages/index.astro
    client_resources/final_version/privacy-policy.html      -> src/pages/privacy-policy.astro
    client_resources/final_version/website-terms.html       -> src/pages/website-terms.astro
                                the design system           -> src/styles/global.css
                                the chrome and its script   -> src/layouts/SiteLayout.astro
                                the lockup                  -> src/components/Logo.astro
                                the footer                  -> src/components/Footer.astro

Run it, do not hand-patch the output: a new drop is ported by regenerating every
file from it, so nothing can drift. Checksum the drop against the one in place
first, because a re-download arrives under a new name and is not a revision.

    python3 scripts/port-drop.py

Five changes are made in the port and no others:
  1. The two Aeonik faces are linked from /fonts/ rather than embedded as base64.
  2. The five photographs are linked from /images/ rather than embedded as base64.
  3. The favicon and the touch icon are linked from / rather than embedded.
  4. Links that leave a page are root-relative; the legal pages' section anchors
     take a `base` of '/' so they reach the home page. The drop's own footer keeps
     bare '#how' anchors on the legal pages, which go nowhere there.
  5. The drop's `noindex` is dropped and the canonical, og:url and og:image come
     from `site:` in astro.config.mjs. These three pages are the live site.
  6. The dead `--hero-image` token is removed. Nothing reads it, and the file it
     names is not in public/, so it warns on every build.
  7. Launch scaffolding the drop has no notion of is added to the layout: the
     full favicon set and the web manifest, a preload for Aeonik Regular, the
     Organization JSON-LD on the home page, a skip link, and the `id="main"`
     target it lands on (the hero section, and <main> on the legal pages). The
     canonical also drops its trailing slash so it agrees with sitemap.xml, and
     every unnamed inline <svg> is marked aria-hidden, which the drop does for
     its logo and its burger but missed on four icons. The footer's legal row
     gains a Sitemap link, and the bar's For advisors link is removed, that
     route now redirecting to the home page.
"""

import base64
import hashlib
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, 'client_resources', 'final_version')

HOME  = os.path.join(DROP, 'compound-health-v1.html')
PRIV  = os.path.join(DROP, 'privacy-policy.html')
TERMS = os.path.join(DROP, 'website-terms.html')

# The drop embeds every asset as base64. Each one is already in public/ byte for
# byte, so the port looks the payload up by digest and links the file instead.
# Nothing is written to public/: a payload with no match in it is an error.
PUBLIC = os.path.join(ROOT, 'public')


def public_index():
    index = {}
    for dirpath, _dirs, files in os.walk(PUBLIC):
        for name in files:
            if name == '.DS_Store':
                continue
            full = os.path.join(dirpath, name)
            with open(full, 'rb') as fh:
                index[hashlib.md5(fh.read()).hexdigest()] = '/' + os.path.relpath(full, PUBLIC)
    return index


ASSETS = None


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print(f'  wrote {rel}  ({len(text):,} bytes)')


def style_blocks(html):
    out = []
    for m in re.finditer(r'<style[^>]*>', html):
        end = html.find('</style>', m.end())
        out.append(html[m.end():end])
    return out


def script_blocks(html):
    out = []
    for m in re.finditer(r'<script>', html):
        end = html.find('</script>', m.end())
        out.append(html[m.end():end])
    return out


def body_of(html):
    head_end = html.find('</head>')
    m = re.search(r'<body[^>]*>', html[head_end:])
    return html[head_end + m.end():html.rfind('</body>')]


def resolve_assets(text, where):
    """Swap every data: URI for the public/ file holding the same bytes."""
    def sub(m):
        raw = base64.b64decode(re.sub(r'\s', '', m.group(2)))
        digest = hashlib.md5(raw).hexdigest()
        path = ASSETS.get(digest)
        if path is None:
            sys.exit(f'{where}: an embedded {m.group(1)} of {len(raw):,} bytes '
                     f'(md5 {digest}) has no match in public/. Save it there first.')
        return path
    return re.sub(r'data:([-\w.+/]+);base64,([A-Za-z0-9+/=\s]+?)(?=["\'])', sub, text)


def slice_lines(body, first, last):
    """Lines are 1-based and inclusive, as printed by the map in the header."""
    return '\n'.join(body.split('\n')[first - 1:last])


def reindent(block, spaces):
    """Re-indent a block lifted out of the drop to sit at `spaces` columns."""
    block = textwrap.dedent(block).strip('\n')
    pad = ' ' * spaces
    return '\n'.join(pad + l if l.strip() else '' for l in block.split('\n'))


def hide_decorative_svgs(markup, where):
    """Mark every unnamed inline <svg> as decorative.

    An <svg> with no aria-hidden, no role and no accessible name is exposed to a
    screen reader as an unnamed graphic. Chrome's accessibility tree confirmed
    four of them on the home page: the arrow in the mobile menu's action, the
    arrow in the submit button, and the error and success icons on the form.
    Every one is an icon standing beside its own label, so every one is
    decorative. The drop already marks its logo and its burger this way; these
    were simply missed.

    focusable="false" goes with it, matching the drop's own convention.
    """
    def sub(m):
        tag = m.group(0)
        if re.search(r'\b(aria-hidden|role|aria-label|aria-labelledby)=', tag):
            return tag
        sub.count += 1
        return tag[:-1].rstrip() + ' aria-hidden="true" focusable="false">'
    sub.count = 0
    out = re.sub(r'<svg\b[^>]*>', sub, markup)
    if sub.count:
        print(f'  marked {sub.count} unnamed svg(s) decorative in {where}')
    return out


def anchors(markup):
    """Section anchors in the chrome resolve against the home page: `base` is ''
    there, so they stay plain hashes, and '/' elsewhere, so they reach it."""
    def sub(m):
        if m.group(1) == 'top':
            return 'href={base || "#top"}'
        return 'href={`${base}#' + m.group(1) + '`}'
    return re.sub(r'href="#(top|how|features|membership|partners|joinwaitlist)"', sub, markup)


def balanced(body, start_marker, where):
    """The element opening at `start_marker`, through its own closing tag."""
    i = body.find(start_marker)
    if i < 0:
        sys.exit(f'{start_marker!r} not found in {where}')
    tag = re.match(r'<([a-zA-Z0-9]+)', body[i:]).group(1)
    depth = 0
    for m in re.finditer(rf'<(/?){tag}\b[^>]*?(/?)>', body[i:]):
        if m.group(2) == '/':
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            # Back up to the start of the line so the block keeps its own
            # indent and dedents cleanly.
            return body[body.rfind('\n', 0, i) + 1:i + m.end()]
    sys.exit(f'{start_marker!r} is never closed in {where}')


def find_block(body, start_marker, end_marker, where):
    i = body.find(start_marker)
    if i < 0:
        sys.exit(f'{start_marker!r} not found in {where}')
    j = body.find(end_marker, i)
    if j < 0:
        sys.exit(f'{end_marker!r} not found after {start_marker!r} in {where}')
    return body[i:j + len(end_marker)]


# Kept beside the templates they appear in, so the length check below reads the
# same strings the pages are written with.
new_title_text = 'Compound Health | A private longevity membership'
new_desc_text = ('A private longevity membership, introduced through the people who already '
                 'advise you. Clinical partners chosen against one standard. Your data stays yours.')


def main():
    global ASSETS
    ASSETS = public_index()
    home, priv, terms = read(HOME), read(PRIV), read(TERMS)

    # The design system and the layout script are one file shared by all three
    # pages. Prove that before splitting, or the pages would silently diverge.
    design = style_blocks(home)[-1]
    for name, html in (('privacy-policy', priv), ('website-terms', terms)):
        if style_blocks(html)[-2] != design:
            sys.exit(f'{name} carries a different design system from the home page')
    layout_js = script_blocks(home)[-1]
    for name, html in (('privacy-policy', priv), ('website-terms', terms)):
        if script_blocks(html)[-1] != layout_js:
            sys.exit(f'{name} carries a different layout script from the home page')
    legal_css = style_blocks(priv)[-1]
    if style_blocks(terms)[-1] != legal_css:
        sys.exit('the two legal pages carry different page styles')

    hb, pb, tb = body_of(home), body_of(priv), body_of(terms)

    # ── src/styles/global.css ────────────────────────────────────────────
    fonts = """/* Aeonik, the client's typeface: Regular for text, Medium for titles.
   Linked from public/fonts/ rather than embedded, which is the only change
   made to the drop's own @font-face rules. */
@font-face {
  font-family: 'Aeonik';
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  src: url('/fonts/Aeonik-Regular.woff2') format('woff2');
}
@font-face {
  font-family: 'Aeonik';
  font-weight: 500;
  font-style: normal;
  font-display: swap;
  src: url('/fonts/Aeonik-Medium.woff2') format('woff2');
}
"""
    header = """/*
 * Compound Health: the design system.
 *
 * Generated by scripts/port-drop.py from the client's final drop at
 * client_resources/final_version/. Do not edit by hand: a new drop is ported by
 * running that script again, so this file cannot drift from what was delivered.
 *
 * This is the drop's own <style> block verbatim. The system: superpower.com's
 * type scale and zinc palette, the client's brand tones (rust, umber, bronze,
 * moss, sand) carrying the accent, Aeonik at 400 and 500, one white ground, a
 * transparent bar that collapses into a blurred pill, photographic cards opening
 * and closing the page, and a fixed footer the closing card uncovers.
 */

"""
    css = textwrap.dedent(design).strip()
    # --hero-image is declared in :root and read by nothing: it is the last
    # trace of the design this one replaced, and the file it points at is not
    # in public/. Left in, it warns on every build. Dropped here rather than by
    # hand, so a new drop cannot bring it back unnoticed.
    css, dead = re.subn(r'[ \t]*--hero-image:[^;]*;\n', '', css)
    if dead:
        print(f'  dropped {dead} dead --hero-image declaration')
    write('src/styles/global.css', header + fonts + css + '\n')

    # ── src/components/Logo.astro ────────────────────────────────────────
    svg = find_block(hb, '<svg class="logo-svg"', '</svg>', 'home')
    logo = '''---
/**
 * The Compound Health lockup: mark and wordmark as one drawing on one viewBox,
 * so no proportion inside it can drift. Lifted verbatim from the client's drop
 * by scripts/port-drop.py.
 *
 * The wordmark is on `currentColor` so the bar can invert over the hero
 * photograph; the mark is on --logo-icon so it holds the brand rust while the
 * wordmark changes around it. Size it with a height on .logo-svg and nothing
 * else.
 */
---

''' + svg + '\n'
    write('src/components/Logo.astro', logo)

    # ── src/components/Footer.astro ──────────────────────────────────────
    footer = balanced(hb, '<footer class="site-footer">', 'home')
    footer = footer.replace(svg, '<Logo />')
    footer = footer.replace('href="https://compoundhealth.io/for-advisors"', 'href="/for-advisors"')
    footer = footer.replace('href="privacy-policy.html"', 'href="/privacy-policy"')
    footer = footer.replace('href="website-terms.html"', 'href="/website-terms"')
    # A Sitemap link in the legal row. It points at the XML itself, which is what
    # public/sitemap.xml is; there is no HTML sitemap on a four-page site.
    footer = footer.replace(
        '<a href="/website-terms">Website Terms</a>',
        '<a href="/website-terms">Website Terms</a>\n          '
        '<a href="/sitemap.xml">Sitemap</a>')
    # Section anchors resolve against the home page. On the home page `base` is
    # empty and they stay plain hashes, which neither reload it nor leave it.
    footer = anchors(footer)
    footer = hide_decorative_svgs(footer, 'the footer')
    footer_astro = '''---
/**
 * The site footer. Generated by scripts/port-drop.py from the client's drop
 * (which names it src/components/Footer.astro); the markup below is that file's.
 *
 * It is fixed at the foot of the window behind the page, and the closing card
 * travels over it and slides away to uncover it. The page reserves exactly its
 * height in --footer-h, measured by the script in SiteLayout. Changing the
 * footer's height therefore changes nothing else.
 *
 * `base` is '' on the home page, where a section anchor is a plain hash, and '/'
 * on the legal pages, where it has to reach the home page first. The drop itself
 * leaves bare hashes in the legal footer, which go nowhere there.
 */
import Logo from './Logo.astro';

interface Props {
  /** '' on the home page, '/' anywhere else. */
  base?: string;
}

const { base = '' } = Astro.props;
---

''' + textwrap.dedent(footer).strip() + '\n'
    write('src/components/Footer.astro', footer_astro)

    # ── src/layouts/SiteLayout.astro ─────────────────────────────────────
    nav = balanced(hb, '<nav class="main-nav">', 'home')
    menu = ('  <!-- Mobile menu overlay -->\n'
            + balanced(hb, '<div class="mobile-menu" id="mobileMenu"', 'home'))

    chrome = nav + '\n\n' + menu
    chrome = chrome.replace(svg, '<Logo />')
    # The bar's For advisors link is removed rather than rewritten: /for-advisors
    # redirects to the home page (astro.config.mjs), so the link went back to the
    # page the reader was already on. The footer's own "For advisors and firms"
    # is left as it is, which is a separate call.
    chrome, dropped = re.subn(
        r'\s*<a href="https://compoundhealth\.io/for-advisors" class="nav-text-link">'
        r'For advisors</a>', '', chrome)
    if dropped != 1:
        sys.exit('the bar\'s For advisors link was not found; the drop has changed shape')
    chrome = chrome.replace('href="https://compoundhealth.io/for-advisors"', 'href="/for-advisors"')
    chrome = anchors(chrome)
    chrome = hide_decorative_svgs(chrome, 'the bar and the menu')

    layout = '''---
/**
 * The site layout: the bar, the mobile menu and the footer, and the script that
 * drives all three. Generated by scripts/port-drop.py from the client's drop,
 * which names it SiteLayout.astro; the markup and the script below are that
 * file's.
 *
 * Canonical and og:url come from `site:` in astro.config.mjs. The drop's own
 * `noindex` is not carried over: these pages are the live site.
 */
import '../styles/global.css';
import Logo from '../components/Logo.astro';
import Footer from '../components/Footer.astro';

interface Props {
  title: string;
  description?: string;
  image?: string;
  /** '' on the home page, '/' anywhere else, so section anchors reach it. */
  base?: string;
  /** Class on <body>. The legal pages use 'legal-page'. */
  bodyClass?: string;
  /**
   * Run the hero intro. Only the home page has a hero, and .is-intro hides
   * pieces before first paint, so a page without one must not ask for it.
   */
  intro?: boolean;
  /** Emit the Organization JSON-LD. The home page alone, or it duplicates. */
  organizationSchema?: boolean;
  /**
   * Keep the page out of the index. It emits the robots meta and suppresses the
   * canonical: a noindex page pointing a canonical at itself is telling a
   * crawler to index the URL it was just told to ignore.
   */
  noindex?: boolean;
}

const SITE_NAME = 'Compound Health';
// 155 characters, so it is not truncated in a result. The drop's own is 200 and
// its <title> 103; both are the client's words, cut rather than rewritten, and
// both are metadata rather than copy that appears on the page. If the client
// wants the full sentences back, they belong in the drop, not here.
const DEFAULT_DESCRIPTION =
  'A private longevity membership, introduced through the people who already advise you. Clinical partners chosen against one standard. Your data stays yours.';
const DEFAULT_OG = '/og-image.png';

const {
  title,
  description = DEFAULT_DESCRIPTION,
  image = DEFAULT_OG,
  base = '',
  bodyClass = '',
  intro = false,
  organizationSchema = false,
  noindex = false,
} = Astro.props;

const siteOrigin = Astro.site ?? new URL('https://compoundhealth.io');
// The build emits directories, so Astro.url.pathname carries a trailing slash.
// Strip it: public/sitemap.xml and the URLs already indexed are slash-less, and
// a canonical that disagrees with the sitemap is a canonical pointing at a URL
// nobody indexed. The root keeps its own '/'. Which form the host actually
// serves is a hosting decision and still has to be made; this only stops the
// two files in the repo contradicting each other.
const canonical = new URL(Astro.url.pathname.replace(/(.)\/$/, '$1'), siteOrigin).toString();
const ogImage = new URL(image, siteOrigin).toString();

const organization = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: SITE_NAME,
  legalName: 'Compound Health, Inc.',
  url: siteOrigin.toString(),
  logo: new URL('/logo.png', siteOrigin).toString(),
  email: 'hello@compoundhealth.io',
  description: DEFAULT_DESCRIPTION,
  // sameAs is deliberately absent: no social profile has been given for this
  // organization. Add the real URLs here when there are any; an invented or
  // guessed profile is worse than none.
};
---

<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{title}</title>
    <meta name="description" content={description} />
    {noindex && <meta name="robots" content="noindex, follow" />}
    {!noindex && <link rel="canonical" href={canonical} />}

    <link rel="icon" type="image/svg+xml" href="/favicon-black.svg" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="icon" href="/favicon.ico" sizes="32x32" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <meta name="theme-color" content="#83392c" />

    <!-- Aeonik Regular sets the reading copy and the hero standfirst, so it is
         on the critical path. Medium is not preloaded: it sets the headline,
         which the intro holds hidden anyway. -->
    <link
      rel="preload"
      href="/fonts/Aeonik-Regular.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content={SITE_NAME} />
    <meta property="og:locale" content="en_US" />
    <meta property="og:url" content={canonical} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={ogImage} />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={ogImage} />

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" is:inline></script>
    {
      intro && (
        <!-- Intro: mark the document before first paint so the hero pieces start
             hidden and GSAP can bring them in. Skipped with reduced motion; the
             script at the foot of the body clears it if GSAP fails to load. -->
        <script is:inline>
          if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.classList.add('is-intro');
          }
        </script>
      )
    }

    <!-- Lenis smooth scrolling (1.3.26). Its stylesheet turns off the native
         smooth scroll-behavior so the two do not fight. -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.css" />
    <script src="https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js" is:inline></script>

    {
      organizationSchema && (
        <script
          type="application/ld+json"
          is:inline
          set:html={JSON.stringify(organization)}
        />
      )
    }

    <slot name="head" />
  </head>

  <body id="top" class={bodyClass}>
    <!-- Skip link. The bar is four section anchors and an action before any
         content, and the mobile menu adds five more, so a keyboard reader
         otherwise tabs through the whole of it on every page. It is off-screen
         until focused, and it sits above the bar's own z-index when it is. -->
    <a class="skip-link" href="#main">Skip to content</a>
CHROME

    <slot />

    <Footer base={base} />

    <style is:global>
      .skip-link {
        position: fixed;
        top: 0;
        left: 50%;
        transform: translate(-50%, -120%);
        z-index: 2000;
        padding: 12px 20px;
        border-radius: 0 0 10px 10px;
        background: #18181b;
        color: #ffffff;
        font-family: var(--font-sans);
        font-size: var(--fs-small);
        line-height: var(--lh-small);
        text-decoration: none;
        transition: transform 0.18s ease-out;
      }
      .skip-link:focus-visible {
        transform: translate(-50%, 0);
        outline: 2px solid #ffffff;
        outline-offset: -6px;
      }
      @media (prefers-reduced-motion: reduce) {
        .skip-link { transition: none; }
      }
      /* The target takes focus programmatically, so it must not draw a ring. */
      [id='main'][tabindex='-1'] { outline: none; }
    </style>

    <!-- Nav, scroll reveal and mobile menu. -->
    <script is:inline>
LAYOUTJS
    </script>
  </body>
</html>
'''
    layout = layout.replace('CHROME', reindent(chrome, 4))
    layout = layout.replace('LAYOUTJS', reindent(layout_js, 6))
    write('src/layouts/SiteLayout.astro', layout)

    # ── src/pages/index.astro ────────────────────────────────────────────
    start = hb.find('<!-- ==================================================================')
    end = hb.find('<!-- ==================================================================\n       THE FOOTER')
    content = hb[start:end].rstrip()
    content = resolve_assets(content, 'home')
    # The flattener rewrote the "Originally src" annotations into base64 too;
    # they now say the same thing as the src beside them.
    content = re.sub(r'[ \t]*<!-- Originally src="[^"]*" -->\n', '', content)
    content = content.replace('href="https://compoundhealth.io/for-advisors"', 'href="/for-advisors"')
    content = content.replace('href="privacy-policy.html"', 'href="/privacy-policy"')
    content = content.replace('href="website-terms.html"', 'href="/website-terms"')
    content = re.sub(r'<script>', '<script is:inline>', content)
    # The skip link in SiteLayout needs somewhere to land. The page has no <main>
    # (every section is a body child, which the stylesheet's ground rule depends
    # on), so the first section carries the id instead. tabindex=-1 so focus
    # actually moves there rather than only the scroll position.
    content, marked = re.subn(r'<section class="hero">',
                              '<section class="hero" id="main" tabindex="-1">',
                              content, count=1)
    if marked != 1:
        sys.exit('the hero section was not found, so the skip link has no target')
    content = hide_decorative_svgs(content, 'the home page')

    page = '''---
/**
 * The Compound Health home page.
 *
 * Generated by scripts/port-drop.py from client_resources/final_version/
 * compound-health-v1.html. Do not edit by hand: run the script against the new
 * drop instead. The bar, the mobile menu, the footer and the script that drives
 * them are in SiteLayout; everything below is this page's own.
 *
 * Copy is the client's. Do not rewrite, shorten, add or remove marketing copy,
 * headings or CTA labels. If a layout needs different words, raise it.
 */
import SiteLayout from '../layouts/SiteLayout.astro';
---

<SiteLayout
  title="Compound Health | A private longevity membership"
  intro={true}
  organizationSchema={true}
>
''' + reindent(content, 2) + '''
</SiteLayout>
'''
    write('src/pages/index.astro', page)

    # ── the two legal pages ──────────────────────────────────────────────
    for rel, body, html, title, desc in (
        ('src/pages/privacy-policy.astro', pb, priv, 'Privacy Policy | Compound Health',
         'How Compound Health collects, uses and safeguards your personal information.'),
        ('src/pages/website-terms.astro', tb, terms, 'Website Terms | Compound Health',
         'The terms governing your use of the Compound Health website.'),
    ):
        main = find_block(body, '<main class="legal">', '</main>', rel)
        main = main.replace('<main class="legal">',
                            '<main class="legal" id="main" tabindex="-1">', 1)
        main = hide_decorative_svgs(main, rel)
        main = main.replace('href="privacy-policy.html"', 'href="/privacy-policy"')
        main = main.replace('href="website-terms.html"', 'href="/website-terms"')
        main = main.replace('href="index.html"', 'href="/"')
        main = re.sub(r'href="index\.html#', 'href="/#', main)
        astro = f'''---
/**
 * {title.split(' |')[0]}. Copy is the client's, verbatim.
 *
 * Generated by scripts/port-drop.py from client_resources/final_version/.
 * Do not edit by hand.
 */
import SiteLayout from '../layouts/SiteLayout.astro';
---

<SiteLayout
  title="{title}"
  description="{desc}"
  base="/"
  bodyClass="legal-page"
>
''' + reindent(main, 2) + '''
</SiteLayout>

<style is:global>
''' + textwrap.dedent(legal_css).strip() + '''
</style>
'''
        write(rel, astro)

    # A soft check: these are guidelines, not errors, so it warns and carries on.
    # scripts/check-meta.py runs the same check over every built page.
    for label, value, limit in (
        ('home <title>', new_title_text, 60),
        ('shared description', new_desc_text, 160),
    ):
        if len(value) > limit:
            print(f'  ! {label} is {len(value)} characters, over the {limit} guideline')

    print('\nported.')


if __name__ == '__main__':
    main()
