"""
Design revisions applied on top of the client's drop by scripts/port-drop.py.

The drop is the source of truth for the design, but these changes cannot wait
for the next one. Like client_revisions.py, every revision asserts the shape it
expects, so a drop that moves the markup or the script underneath one stops the
port instead of losing it. They run after the drop's comments are stripped, so
they match the comment-free text.

When a drop arrives that already carries a revision, delete it from here.

Revisions, October 2026:

  1. The bar is one glass island of fixed width, almost square at the
     corners, floating over the page: the lockup on the left, the section
     links and the action on the right, the action last. It never changes
     shape. Its ink is white; its glass is 10% white over the photographs and
     the dark sections, and the hero photograph's night blue over the white
     page. Below 900px the menu button sits inside the island.
  2. The hero photograph fills the whole first screen, edge to edge: no inset,
     no rounded corners, no white margin, with the island floating over it.
  3. Every corner on the site follows the bar's: almost square. Controls
     (buttons, chips, tags, inputs, badges) take 6px and surfaces (cards,
     panels, the form, the figures) 12px. True circles, the status dots and
     the avatars, stay round.
  4. The drop's unused accent ramps are removed, and the three uses of one of
     them move onto the brand tones (night blue, since revision 16).
  5. The type scale is new: a fixed 16px root, and headings that scale with
     the viewport through clamp(), with their own leading and tracking.
  6. The menu button below 900px is two lines that cross into an X when the
     menu opens.
  7. Every solid button is the brand moss, the bar's action included: one
     colour for one kind of button.
  8. The dark gradient footer the drop superseded is removed: its rules, every
     one overridden by the white footer that replaced it, and the two empty
     elements it painted, the media layer and the divider, both hidden.
  9. What you get is an index of rows, not a grid of tall panels: each
     feature is one row, its number, title and description on the left and
     its figure in a landscape panel on the right, the rows ruled off by
     hairlines. The title is the larger of the two, the description at
     reading size. The numbers are drawn by a CSS counter, so no copy is
     added to the markup.
 10. Secondary actions on the dark grounds (the hero, the membership band
     and its cards) are text links, not buttons: white text, no fill, no
     outline and no blur, underlined on hover.
 11. No action carries an arrow. The trailing arrow glyph goes from every
     link and button label, and the drawn arrow from the form's submit and
     the menu's action. The words of every label are untouched.
 12. The close of the page is a statement on the white ground, not copy laid
     over a photograph: the heading, the line beneath it and the action
     centred, and the photograph below them as a wide, low panorama inside
     the content column. The footer still sits beneath it.
 13. The two chips on dark grounds (the membership band, the access card)
     are solid tones a step off their ground, not translucent glass.
 14. From 901px, What you get is a stack: the figures stick under the bar
     one after another at the same top, each rising over the last, which
     shrinks behind it as it comes, while the copy on the left hands over at
     the midpoint of the same travel. Both run off one progress per hand-over. It is laid on by script (.feat-grid.is-stacked), so
     without it, and on phones, the rows of revision 9 stand.
 15. The hero carries a new photograph, public/images/hero-portrait.webp, in
     place of the drop's. The drop's own stays in public/images/hero.webp,
     because the port matches each embedded photograph to its file there by
     checksum; only the page's reference to it moves.
 16. The warm tones go. Rust, umber, bronze, taupe, olive and sand are
     removed from the palette and every use moves onto the two cool families:
     the accent, its tint and its deeper steps onto moss, the secondary warm
     tones onto night blue, which gains tokens of its own. The four feature
     panels drawn from warm tones take cool ones under new class names, and
     the port stops if any warm tone survives.
 17. Every figure is a field: one flat tone with its content set straight on
     the colour in white. The gradient, the blurred light and the white card
     floating on it are gone, from the feature figures and the disciplines
     panel alike. The figures share one set of atoms on colour (quiet labels,
     white values, square segments, white rules, a solid white chip), which
     each figure composes from.
 18. The Healthspan score is a field of its own: the score at display size on
     the left, its three counts stacked on the right under rules, each keyed
     to its block, and the bar beneath as three square blocks divided by the
     counts themselves. Biological age stays as a quiet row at the foot.
 19. ApoB is a field of its own: the marker's name at display size, the white
     Optimal chip beside it, and the chart as one heavy white line over a
     square band for the range, with every point dropped but the last, which
     is drawn larger as the reading that matters.
 20. Your protocol is a field of its own: each item a large row under a rule,
     its category a small label above it rather than a chip. The photograph
     behind it stays until its replacement arrives; the layer that darkens it
     turns night blue, so the type reads on it in the palette's own shade.
 21. Your care team is a field: each discipline at headline size, keyed by a
     square, how it is delivered as a quiet label at the line's end.
 22. Your clinical record is a ledger on the field: each source's name as a
     label in a left column, what it holds at headline size beside it, the
     access line a quiet row at the foot.
 23. The concierge thread is set as type, not bubbles: the member's question
     quiet and to the right, the team's answer at headline size under a rule,
     the team keyed by three squares.
 24. The disciplines panel is a field too: its three devices (the team bar,
     the coverage ring, the gate) lose the light card and are drawn in white
     on the panel's tone, with square segments and keys.
 25. The disciplines panel moves as one choreography. The panes cross rather
     than swap: the outgoing one leaves quickly while the panel's colour turns
     slowly, and the incoming one builds in order on one long decelerating
     curve. The team bar grows as one bar, the coverage ring is revealed as
     one sweep with its count tied to it, the foot lines wipe in. Nothing
     loops and nothing fades out before a switch: once built, a pane holds.
"""

import re
import sys
import textwrap

APPLIED = []


def _once(text, needle, label):
    i = text.find(needle)
    if i < 0 or text.find(needle, i + 1) >= 0:
        sys.exit(f'design revision "{label}": expected exactly one {needle!r}. '
                 'The drop has changed underneath this revision; re-read '
                 'scripts/design_revisions.py before porting.')
    return i


# ── 1. The bar ──────────────────────────────────────────────────────────

def apply_to_chrome(chrome):
    """Lockup first in the island, the menu button last inside it."""
    label = 'bar: lockup moved to the left of the island'
    start = _once(chrome, '<a href={base || "#top"} class="nav-logo"', label)
    end = chrome.index('</a>', start) + len('</a>')
    line_start = chrome.rfind('\n', 0, start) + 1
    logo = chrome[start:end]
    chrome = chrome[:line_start] + chrome[end:].lstrip(' ').lstrip('\n')
    links = _once(chrome, '<div class="nav-links">', label)
    indent = chrome[chrome.rfind('\n', 0, links) + 1:links]
    chrome = chrome[:links] + logo + '\n' + indent + chrome[links:]
    APPLIED.append(label)

    label = 'bar: menu button moved inside the island'
    start = _once(chrome, '<button class="hamburger"', label)
    line_start = chrome.rfind('\n', 0, start) + 1
    end = chrome.index('</button>', start) + len('</button>')
    button = textwrap.dedent(chrome[line_start:end])
    chrome = chrome[:line_start] + chrome[end:].lstrip('\n')
    # The bar's own </nav> is the first one after the button (the mobile menu
    # carries a second), and the island closes on the last </div> before it.
    nav_end = chrome.find('</nav>', line_start)
    inner_end = chrome.rfind('</div>', 0, nav_end)
    pad = chrome[chrome.rfind('\n', 0, inner_end) + 1:inner_end] + '  '
    chrome = (chrome[:inner_end].rstrip(' ') + textwrap.indent(button, pad) + '\n'
              + chrome[chrome.rfind('\n', 0, inner_end) + 1:])
    APPLIED.append(label)

    label = 'bar: the menu button drawn as two lines'
    start = _once(chrome, '<svg class="hamburger-dots"', label)
    line_start = chrome.rfind('\n', 0, start) + 1
    end = chrome.index('</svg>', start) + len('</svg>')
    chrome = chrome[:line_start] + chrome[end:].lstrip(' ').lstrip('\n')
    APPLIED.append(label)

    label = 'actions: the menu action\'s arrow removed'
    start = _once(chrome, 'class="mobile-nav-cta"', label)
    end = chrome.index('</a>', start)
    action, k = re.subn(ARROW_SVG, '', chrome[start:end])
    if k != 1:
        sys.exit(f'design revision "{label}": the arrow was not found')
    chrome = chrome[:start] + action + chrome[end:]
    APPLIED.append(label)
    return chrome


NAV_SCRIPT = """\
(function () {
  const nav = document.querySelector('.main-nav');
  if (!nav) return;

  const measureNav = () => document.documentElement.style.setProperty('--nav-h', nav.offsetHeight + 'px');
  measureNav();
  window.addEventListener('resize', measureNav, { passive: true });
  if ('ResizeObserver' in window) new ResizeObserver(measureNav).observe(nav);

  // The island takes the opposite tone to whatever is under it: light glass
  // over a photograph or a dark section, dark glass over the white page. The
  // ground is read off the page itself, at seven points along the island's
  // middle, so no list of sections has to be kept in step with the markup.
  // A photograph counts as dark; a gradient by its first colour stop. The ink
  // is white in both tones, so the brightest point decides: one light card
  // under the links, a white tier in a dark band, turns the island dark.
  const inner = nav.querySelector('.nav-inner');
  if (!inner) return;
  const channel = (v) => (v /= 255) <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  const lum = (rgb) => 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2]);
  const rgba = (text) => {
    const m = text && text.match(/rgba?\(([^)]*)\)/);
    return m ? m[1].split(/[\s,/]+/).filter(Boolean).map(Number) : null;
  };
  const groundAt = (x, y) => {
    const hit = document.elementsFromPoint(x, y).find((el) => !el.closest('.main-nav, .mobile-menu'));
    for (let n = hit; n && n !== document.documentElement; n = n.parentElement) {
      if (n.tagName === 'IMG' || n.tagName === 'VIDEO') return 0;
      const s = getComputedStyle(n);
      if (s.backgroundImage !== 'none') {
        if (s.backgroundImage.includes('url(')) return 0;
        const stop = rgba(s.backgroundImage);
        if (stop) return lum(stop);
      }
      const c = rgba(s.backgroundColor);
      if (c && (c.length < 4 || c[3] > 0.5)) return lum(c);
    }
    return 1;
  };

  let dark = false;
  let queued = false;
  const update = () => {
    queued = false;
    const r = inner.getBoundingClientRect();
    const y = r.top + r.height / 2;
    let ground = 0;
    for (let i = 0; i < 7; i++) ground = Math.max(ground, groundAt(r.left + 24 + (r.width - 48) * i / 6, y));
    // Two thresholds, so a ground near the boundary cannot make it flicker.
    if (!dark && ground > 0.5) dark = true;
    else if (dark && ground < 0.35) dark = false;
    else return;
    nav.classList.toggle('is-dark', dark);
  };
  const queue = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };
  update();
  window.addEventListener('scroll', queue, { passive: true });
  window.addEventListener('resize', queue, { passive: true });
  window.addEventListener('load', queue);
})();"""


STACK_SCRIPT = """\
(function () {
  // What you get as a stack (design revision 14). From 901px the script lays
  // the stack on with .is-stacked; on phones, and without it, the rows stand.
  // On every frame that scrolls it marks the figure on top as .is-current
  // (its copy shows) and those under it as .is-covered, sets each figure's
  // --recede from how far the next has risen over it, and it starts each
  // figure's mock-up as it comes up the screen, which the page's own observer
  // cannot do once the articles have no box.
  const grid = document.querySelector('.feat-grid');
  if (!grid) return;
  const cards = Array.from(grid.children).filter((el) => el.classList.contains('feat-card'));
  if (cards.length < 2) return;
  const wide = window.matchMedia('(min-width: 901px)');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  const countUp = (el) => {
    const target = Number(el.dataset.count);
    if (!target) return;
    if (reduce.matches) { el.textContent = String(target); return; }
    const start = performance.now() + 450;
    const tick = (now) => {
      const t = Math.max(0, Math.min(1, (now - start) / 1100));
      el.textContent = String(Math.round((1 - Math.pow(1 - t, 3)) * target));
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const enter = (card) => {
    if (card.classList.contains('is-in')) return;
    card.classList.add('is-in');
    card.querySelectorAll('[data-count]').forEach(countUp);
  };

  // One progress per hand-over: how far figure i + 1 has travelled from the
  // foot of the screen to the top figure i is stuck at, 0 to 1. Everything is
  // derived from it, so the figures and the copy can never drift apart.
  const ease = (x) => x * x * (3 - 2 * x);
  const band = (p, a, b) => ease(Math.min(1, Math.max(0, (p - a) / (b - a))));
  // A figure's top as laid out, before its own shrink: the shrink is about
  // the centre, so half the height it has lost is added back. Measuring the
  // drawn top instead would let a shrinking figure uncover the one beneath.
  const topOf = (fig) => {
    const r = fig.getBoundingClientRect();
    return r.top - (fig.offsetHeight - r.height) / 2;
  };

  let queued = false;
  const update = () => {
    queued = false;
    if (!grid.classList.contains('is-stacked')) return;
    const figs = cards.map((card) => card.querySelector('.feat-visual'));
    const copies = cards.map((card) => card.querySelector('.feat-copy'));
    if (figs.some((f) => !f)) return;
    const vh = window.innerHeight;
    const stuck = parseFloat(getComputedStyle(figs[0]).top) || 0;
    const progress = figs.slice(1).map((fig) =>
      Math.min(1, Math.max(0, (vh - topOf(fig)) / Math.max(1, vh - stuck))));
    let current = 0;
    cards.forEach((card, i) => {
      const before = i > 0 ? progress[i - 1] : 1;
      const after = i < progress.length ? progress[i] : 0;
      if (before >= 0.5) current = i;
      figs[i].style.setProperty('--recede', ease(after).toFixed(4));
      // The outgoing copy is gone by the midpoint and the incoming one starts
      // there, so the two are never on screen together.
      copies[i]?.style.setProperty('--in', (i === 0 ? 1 : band(before, 0.5, 0.75)).toFixed(4));
      copies[i]?.style.setProperty('--out', band(after, 0.25, 0.5).toFixed(4));
      if (topOf(figs[i]) < vh * 0.85) enter(card);
    });
    cards.forEach((card, i) => {
      card.classList.toggle('is-current', i === current);
      card.classList.toggle('is-covered', i < current);
    });
  };
  const queue = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };
  const mode = () => {
    grid.classList.toggle('is-stacked', wide.matches);
    if (!wide.matches) cards.forEach((card) => {
      card.classList.remove('is-current', 'is-covered');
      card.querySelector('.feat-visual')?.style.removeProperty('--recede');
      card.querySelector('.feat-copy')?.style.removeProperty('--in');
      card.querySelector('.feat-copy')?.style.removeProperty('--out');
    });
    update();
  };
  mode();
  wide.addEventListener('change', mode);
  window.addEventListener('scroll', queue, { passive: true });
  window.addEventListener('resize', queue, { passive: true });
})();"""


def apply_to_layout_js(js):
    """Replace the bar's reshaping tween with the island's tone switch."""
    label = 'bar: the scroll tween replaced by a tone switch'
    start_marker = "(function () {\n  const nav = document.querySelector('.main-nav');\n  const inner"
    js = textwrap.dedent(js)
    start = _once(js, start_marker, label)
    end_marker = '\n})();\n'
    end = js.find(end_marker, start)
    if end < 0:
        sys.exit(f'design revision "{label}": the bar script never closes')
    js = js[:start] + NAV_SCRIPT + js[end + len(end_marker) - 1:]
    APPLIED.append(label)
    js = js.rstrip('\n') + '\n\n' + STACK_SCRIPT + '\n'
    APPLIED.append('what you get: the stack script added')
    return js


# ── the stylesheet ──────────────────────────────────────────────────────

CSS = """
/* ══════════════════════════════════════════════════════════════════════
   DESIGN REVISIONS, OCTOBER 2026 (scripts/design_revisions.py)
   Appended after the drop's own rules, so they win at equal specificity.
   ══════════════════════════════════════════════════════════════════════ */

/* The bar. .main-nav is only a frame that centres the island and lets clicks
   through around it; .nav-inner is the island: 960px wide wherever it fits,
   and it never changes shape. Its corners are almost square, 12px, and the
   action's are 6px: the island's radius less its padding, so they nest. No
   outline and no shadow (the drop sets every box-shadow to none, site-wide).

   The ink is white in both of the island's tones; only the glass changes.
   Over a photograph or a dark section it is the hero's own glass button:
   10% white over a 32px blur. Over the white page it is deep blue glass,
   the night blue of the hero photograph (#0a1a26) at 88% over a 24px blur:
   at less, the white page lifts it to a slate grey. White ink on it measures
   over 11:1 on plain white. The script in the
   layout reads which ground is under the island and sets .is-dark. The mark
   is white throughout, as the drop sets it on its dark grounds. */
.main-nav, .main-nav.is-scrolled {
  top: 0; left: 0; right: 0;
  display: flex; justify-content: center; align-items: flex-start;
  padding: 1rem 1rem 0; pointer-events: none;
  background: none; border: 0; -webkit-backdrop-filter: none; backdrop-filter: none;
}
.main-nav .nav-inner {
  pointer-events: auto;
  flex: 0 1 960px; width: 960px; max-width: 100%;
  display: flex; align-items: center; justify-content: flex-start; gap: 0.125rem;
  padding: 0.375rem 0.375rem 0.375rem 1.5rem;
  border-radius: 12px; border: 0;
  background: rgba(255, 255, 255, 0.1);
  -webkit-backdrop-filter: blur(32px);
  backdrop-filter: blur(32px);
  transition: background-color 0.35s ease;
  will-change: auto;
}
.main-nav.is-dark .nav-inner {
  background-color: rgba(10, 26, 38, 0.88);
  -webkit-backdrop-filter: blur(24px); backdrop-filter: blur(24px);
}
.main-nav .nav-inner .nav-logo {
  position: static; transform: none; margin-right: auto;
  color: #fff; --logo-icon: #fff; font-size: 18px; gap: 8px;
}
.main-nav .nav-links { margin-left: 0; gap: 0.125rem; }
/* Hover changes the ink alone, to a pale night blue, with no fill behind it. */
.main-nav .nav-links a {
  height: 2.5rem; padding: 0 0.875rem; border-radius: 6px;
  color: #fff; transition: color 0.2s ease;
}
.main-nav .nav-links a:hover { background: transparent; color: var(--tone-blue-pale); }
.main-nav .nav-actions { margin-left: 0.375rem; }
.main-nav .nav-cta {
  height: 2.5rem; padding: 0 1.25rem !important; border-radius: 6px !important;
  background: var(--tone-moss-light) !important; color: #fff !important;
}
/* The drop's shared button hover sets a dark border-color !important; it has
   to be cleared here, or it draws an outline round the action on hover. */
.main-nav .nav-cta, .main-nav .nav-cta:hover { border-color: transparent !important; }
.main-nav .nav-cta:hover {
  background: var(--tone-moss) !important;
  filter: none;
}
.main-nav .hamburger { display: none; }

/* One colour for one kind of button: every solid button is the brand moss,
   over the photographs as on the white page, with a deeper moss on hover. */
.btn-solid, .mobile-nav-cta, .plan-btn.is-solid, .wf-submit,
.hero .btn-solid, .closer .btn-solid, .plan.featured .plan-btn.is-solid {
  background: var(--tone-moss-light) !important; border-color: var(--tone-moss-light) !important; color: #fff !important;
}
.btn-solid:hover, .mobile-nav-cta:hover, .plan-btn.is-solid:hover, .wf-submit:hover,
.hero .btn-solid:hover, .closer .btn-solid:hover, .plan.featured .plan-btn.is-solid:hover {
  background: var(--tone-moss) !important;
  border-color: var(--tone-moss) !important; color: #fff !important;
}

/* What you get, as an index of rows. One feature per row, ruled off above
   and below: on the left its number (a CSS counter, so the markup carries no
   new copy), its title at h4 and its description at reading size; on the
   right its figure, in a landscape panel. The DOM keeps the figure first, as
   the drop has it; the grid places it. Every row is the same shape, the two
   the drop ran wide included. */
.feat-grid {
  display: block; counter-reset: feat;
  border-top: 1px solid var(--zinc-200);
}
.feat-card, .feat-card.is-wide {
  display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
  column-gap: 4rem; align-items: start;
  padding: 2.5rem 0; border-bottom: 1px solid var(--zinc-200);
}
.feat-card .feat-copy, .feat-card.is-wide .feat-copy {
  grid-column: 1; grid-row: 1; max-width: 26rem; gap: 0.75rem;
}
.feat-copy { counter-increment: feat; }
.feat-copy::before {
  content: counter(feat, decimal-leading-zero);
  margin-bottom: 0.5rem;
  font-size: var(--fs-small); line-height: var(--lh-small); letter-spacing: 0.04em;
  font-variant-numeric: tabular-nums; color: var(--tone-moss-light);
}
.feat-name {
  font-size: var(--fs-h4); line-height: var(--lh-h4); letter-spacing: var(--ls-h4);
}
.feat-desc {
  font-size: var(--fs-body); line-height: var(--lh-body); letter-spacing: var(--ls-body);
  color: var(--zinc-600);
}
/* The figure keeps its own mock-up at the width it was drawn for: the side
   padding grows with the panel so the cards inside never stretch past 26rem. */
.feat-card .feat-visual, .feat-card.is-wide .feat-visual {
  grid-column: 2; grid-row: 1; flex: none;
  aspect-ratio: 16 / 10;
  padding: 6% max(8%, calc(50% - 13rem));
}

@media (max-width: 900px) {
  .feat-card, .feat-card.is-wide {
    grid-template-columns: minmax(0, 1fr); row-gap: 1.5rem; padding: 2rem 0;
  }
  .feat-card .feat-copy, .feat-card.is-wide .feat-copy { grid-row: 1; max-width: none; }
  .feat-card .feat-visual, .feat-card.is-wide .feat-visual {
    grid-column: 1; grid-row: 2;
    aspect-ratio: auto; min-height: 17rem; padding: 1.75rem 1.25rem;
  }
}

/* Secondary actions on a dark ground are text links: white text, no fill, no
   outline, no blur, with just enough padding to keep the hit area and the
   baseline of the button beside them, and an underline on hover. Primary
   stays solid moss. */
.hero .btn-outline, .closer .btn-outline,
.plans .btn-pill, .plans .plan-btn:not(.is-solid) {
  display: inline-block; text-align: center;
  background: transparent; color: #fff; border: 0;
  padding-left: 0.25rem !important; padding-right: 0.25rem !important;
  -webkit-backdrop-filter: none; backdrop-filter: none;
  text-decoration: underline; text-decoration-color: transparent;
  text-decoration-thickness: 1px; text-underline-offset: 0.35em;
  transition: text-decoration-color 0.2s ease;
}
.hero .btn-outline:hover, .closer .btn-outline:hover,
.plans .btn-pill:hover, .plans .plan-btn:not(.is-solid):hover {
  background: transparent; color: #fff; border: 0;
  text-decoration-color: currentColor;
}

/* The close of the page: a statement on the white ground. The heading, the
   line under it and the action are centred in a reading measure; the
   photograph sits beneath them as a 21:9 panorama in the content column,
   framed on the face. Nothing is laid over the photograph. The DOM keeps the
   photograph first, as the drop has it; order places it. */
.closer { padding: 7rem 1.5rem 5rem; }
.closer .closer-card {
  max-width: 1120px; margin: 0 auto; min-height: 0; padding: 0;
  background: none; color: var(--charcoal); border-radius: 0; overflow: visible;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  gap: 4rem;
}
.closer .closer-inner {
  order: 0; max-width: 40rem; align-items: center; text-align: center; gap: 0.75rem;
}
.closer .closer-inner h2 { color: var(--charcoal); font-size: var(--fs-h2l); }
.closer .closer-sub { color: var(--zinc-600); max-width: 34rem; margin: 0 auto; }
.closer .closer-btns { justify-content: center; }
.closer .closer-media {
  order: 1; position: relative; inset: auto; width: 100%;
  aspect-ratio: 21 / 9; border-radius: 12px; overflow: hidden;
}
.closer .closer-media::after { display: none; }
.closer .closer-img { object-position: 50% 15%; }

@media (max-width: 900px) {
  .closer { padding: 4.5rem 1.25rem 3rem; }
  .closer .closer-card { gap: 2.5rem; }
  .closer .closer-media { aspect-ratio: 4 / 3; }
  .closer .closer-img { object-position: 62% 12%; }
}

/* What you get, as a stack, from 901px and only once the script has laid it
   on (.is-stacked); without the script the rows above stand. The articles
   give up their boxes (display: contents) so that every copy shares the left
   cell and every figure the right one: one grid row, so the sticky figures
   all share one containing block. Each figure sits a screen lower than the
   last in the flow and sticks at the same top, so each one rises over its
   predecessor, which recedes behind it and is gone when it settles. The
   copies overlap in their cell, sticky beside the stack, and crossfade to
   whichever figure is on top. */
@media (min-width: 901px) {
  .features {
    --stack-top: calc(var(--nav-h, 5rem) + 2.5rem);
    --stack-h: min(24rem, 58vh);
    /* Each figure enters the screen only once the one before it has settled,
       then holds for 12vh before the next appears: the gap is whatever is
       left of the screen below a settled figure, plus that hold. */
    --stack-gap: calc(100vh - var(--stack-top) - var(--stack-h) + 12vh);
  }
  .feat-grid.is-stacked {
    display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
    column-gap: 4rem; align-items: start; border-top: 0;
  }
  .feat-grid.is-stacked .feat-card, .feat-grid.is-stacked .feat-card.is-wide { display: contents; }
  /* The copy follows the same progress as the figures. --in and --out (0 to
     1, already eased by the script) say how far this feature's figure has
     arrived and how far the next one has: a copy rises in from below as its
     figure comes up and lifts away as the next one does, the two changing
     places at the midpoint of the figure's travel. */
  .feat-grid.is-stacked .feat-card .feat-copy {
    grid-column: 1; grid-row: 1; align-self: start;
    position: sticky; top: calc(var(--stack-top) + 2.5rem);
    opacity: calc(var(--in, 0) * (1 - var(--out, 0)));
    transform: translateY(calc((1 - var(--in, 0)) * 1.5rem - var(--out, 0) * 1.5rem));
    pointer-events: none; transition: none;
  }
  .feat-grid.is-stacked .feat-card.is-current .feat-copy { pointer-events: auto; }
  /* Every figure sticks at the same top, so none shows an edge above the one
     on top. --recede (0 to 1, eased by the script) is how far the next figure
     has risen over this one: it only shrinks, about its centre, to 90%, so by
     the time the next settles it lies wholly behind it and is gone without
     fading. */
  .feat-grid.is-stacked .feat-card .feat-visual {
    grid-column: 2; grid-row: 1; align-self: start;
    position: sticky; top: var(--stack-top); aspect-ratio: auto; height: var(--stack-h);
    transform-origin: 50% 50%;
    transform: scale(calc(1 - var(--recede, 0) * 0.1));
    transition: none;
  }
  .feat-grid.is-stacked .feat-card:nth-child(1) .feat-visual { margin-top: calc(0 * (var(--stack-h) + var(--stack-gap))); }
  .feat-grid.is-stacked .feat-card:nth-child(2) .feat-visual { margin-top: calc(1 * (var(--stack-h) + var(--stack-gap))); }
  .feat-grid.is-stacked .feat-card:nth-child(3) .feat-visual { margin-top: calc(2 * (var(--stack-h) + var(--stack-gap))); }
  .feat-grid.is-stacked .feat-card:nth-child(4) .feat-visual { margin-top: calc(3 * (var(--stack-h) + var(--stack-gap))); }
  .feat-grid.is-stacked .feat-card:nth-child(5) .feat-visual { margin-top: calc(4 * (var(--stack-h) + var(--stack-gap))); }
  .feat-grid.is-stacked .feat-card:nth-child(6) .feat-visual { margin-top: calc(5 * (var(--stack-h) + var(--stack-gap))); }
  /* The row has to run on past the last figure, or the last has no room to
     stick: its own margin would count inside its sticky range. An empty
     spacer in the same cell sets the row's length instead, holding the full
     stack for 30vh before it scrolls away as one. */
  .feat-grid.is-stacked::after {
    content: ''; grid-column: 2; grid-row: 1; visibility: hidden; pointer-events: none;
    height: calc(5 * (var(--stack-h) + var(--stack-gap)) + var(--stack-h) + 30vh);
  }
}
/* With reduced motion nothing moves with the scroll: the figures do not
   shrink (each still covers the last exactly), and the copy swaps outright. */
@media (min-width: 901px) and (prefers-reduced-motion: reduce) {
  .feat-grid.is-stacked .feat-card .feat-visual { transform: none; }
  .feat-grid.is-stacked .feat-card .feat-copy { opacity: 0; transform: none; }
  .feat-grid.is-stacked .feat-card.is-current .feat-copy { opacity: 1; }
}

/* The two chips on dark grounds are solid, not glass: no translucent fill
   and no backdrop blur, just a tone a step off their ground, the way the
   chips on the white page are a solid zinc-100. On the membership band
   (#130f13) the chip is a step lighter; on the blue access card (#1b4561,
   lightest at the chip's corner) a step darker, so it reads against the
   gradient rather than dissolving into it. */
.plans .s-chip {
  background: #2b272b; color: #e9e7e9;
  -webkit-backdrop-filter: none; backdrop-filter: none;
}
.cta-card .s-chip, .footer-cta .s-chip {
  background: #10293a; color: #e6edf2;
  -webkit-backdrop-filter: none; backdrop-filter: none;
}

/* Revision 16: the membership band glows night blue from its lower left, where
   the drop had rust, under the moss it already carries at the upper right. */
.plans::before {
  background:
    radial-gradient(ellipse 55% 60% at 8% 100%, rgba(42,95,131,0.7) 0%, rgba(42,95,131,0) 65%),
    radial-gradient(ellipse 50% 45% at 95% 0%, rgba(33,72,51,0.45) 0%, rgba(33,72,51,0) 65%);
}

/* The hero fills the first screen, edge to edge. The card keeps its own top
   padding so the copy clears the island floating over it. */
.hero { padding: 0; }
.hero-card {
  border-radius: 0;
  height: 100vh; height: 100svh; min-height: 600px;
  padding: 6.5rem 4rem 4rem;
}
/* Revision 15: she sits right of centre and the left of the photograph is its
   darkest ground, so the frame holds her right and the copy sits on the dark. */
.hero-img { object-position: 0% 30%; }

@media (max-width: 900px) {
  .main-nav, .main-nav.is-scrolled { padding: 0.75rem 0.75rem 0; }
  .main-nav .nav-inner, .main-nav.is-scrolled .nav-inner {
    flex: 1 1 auto; width: 100%; max-width: none !important;
    justify-content: flex-start;
    padding: 0.3125rem 0.3125rem 0.3125rem 1.25rem !important;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.1) !important;
    -webkit-backdrop-filter: blur(32px) !important;
    backdrop-filter: blur(32px) !important;
  }
  .main-nav.is-dark .nav-inner {
    background: rgba(10, 26, 38, 0.88) !important;
    -webkit-backdrop-filter: blur(24px) !important; backdrop-filter: blur(24px) !important;
  }
  .main-nav .nav-inner .nav-logo, .main-nav.is-scrolled .nav-inner .nav-logo {
    color: #fff !important; font-size: 17px;
  }
  .main-nav .hamburger, .main-nav.is-scrolled .hamburger {
    display: flex; width: 2.5rem; height: 2.5rem; border-radius: 7px;
    background: transparent !important; color: #fff !important;
    -webkit-backdrop-filter: none !important; backdrop-filter: none !important;
  }
  /* The menu button: two lines, 8px apart, that cross into an X when the menu
     opens. The middle line of the three the menu script expects stays hidden. */
  .main-nav .hamburger .hamburger-line {
    display: block; position: absolute; left: 50%; top: 50%;
    width: 18px; height: 1.5px; margin: -0.75px 0 0 -9px !important;
    background: currentColor !important; border-radius: 1px;
    opacity: 1 !important; transform: none;
    transition: transform 0.3s ease, opacity 0.2s ease;
  }
  .main-nav .hamburger .hamburger-line:nth-of-type(1) { transform: translateY(-4px) !important; }
  .main-nav .hamburger .hamburger-line:nth-of-type(2) { opacity: 0 !important; }
  .main-nav .hamburger .hamburger-line:nth-of-type(3) { transform: translateY(4px) !important; }
  .main-nav .hamburger.is-open .hamburger-line:nth-of-type(1) { transform: rotate(45deg) !important; }
  .main-nav .hamburger.is-open .hamburger-line:nth-of-type(3) { transform: rotate(-45deg) !important; }

  .hero { padding: 0; }
  .hero-card {
    height: auto; min-height: 100vh; min-height: 100svh;
    padding: 5.5rem 1.25rem 1.25rem; border-radius: 0;
  }
  .hero-img { object-position: 45% 20%; }
  /* Both hero actions run the full width of the column on a phone: the
     drop's own width: 100% did nothing while .hero-actions shrank to fit its
     content, so the column stretches and the actions stack. */
  .hero .hero-actions { align-items: stretch; width: 100%; }
  .hero .hero-btns { flex-direction: column; align-items: stretch; width: 100%; }
  .hero .hero-btns > * { width: 100%; justify-content: center; text-align: center; }
}

/* Revision 17: every figure is a field. The panel is one flat tone, with no
   gradient, no blurred light and no card floating on it: the figure's content
   is set straight on the colour in white, its heading at the top as a quiet
   label and its data anchored to the foot. The atoms below are the shared
   language every figure composes from: labels at 72% white, values in white,
   square segments, rules at 22% white, a solid white chip carrying the
   panel's own colour as its ink. */
.feat-card .feat-visual, .feat-card.is-wide .feat-visual {
  justify-content: flex-start; padding: 2rem 2.25rem; color: #fff;
}
.feat-visual::before, .prod-panel::before { display: none; }
.feat-visual.tone-ink { --fv-bg: var(--tone-night); }
.prod-panel { --fv-bg: var(--tone-night); }
.prod-panel .stack-card { box-shadow: none; }

.fm-card {
  display: flex; flex-direction: column; flex: 1 1 auto;
  background: none; border-radius: 0; padding: 0; box-shadow: none; color: #fff;
}
.fm-card + .fm-card {
  flex: 0 0 auto; margin-top: 1.25rem; padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.22);
}
.fm-card > :nth-child(2) { margin-top: auto; }
.fm-card + .fm-card > :nth-child(2) { margin-top: 0.75rem; }
.fm-title {
  font-size: var(--fs-small); line-height: var(--lh-small); letter-spacing: 0.01em;
  font-weight: 400; color: rgba(255,255,255,0.72);
}
.fm-big { font-size: var(--fs-h1); line-height: 0.9; letter-spacing: -0.04em; font-weight: 500; color: #fff; }
.fm-big small { color: rgba(255,255,255,0.72); letter-spacing: 0; }
.fm-muted, .fm-legend { color: rgba(255,255,255,0.72); }
.fm-legend b { color: #fff; font-weight: 500; }
.fm-track { gap: 3px; height: 0.625rem; }
.fm-track.fm-thin { height: 3px; background: rgba(255,255,255,0.22); border-radius: 0; }
.fm-seg { border-radius: 0; }
.fm-seg.is-moss, .fm-dot.is-moss { background: #fff; }
.fm-seg.is-bronze, .fm-dot.is-bronze { background: var(--tone-blue-pale); }
.fm-seg.is-rust { background: rgba(255,255,255,0.4); }
.fm-marker { border-top-color: #fff; }
.fm-chip, .fm-chip.is-moss, .fm-chip.is-rust { background: #fff; color: var(--fv-bg); font-weight: 500; }
.fm-list { margin: 0; }
.fm-list li { border-top: 1px solid rgba(255,255,255,0.22); color: #fff; }
.fm-band { fill: rgba(255,255,255,0.09); stroke: none; }
.fm-line { stroke: #fff; }
.fm-pts { fill: #fff; }
.fm-thread { margin-top: auto; max-width: 30rem; }
.fm-bubble { box-shadow: none; }
.fm-bubble.is-me { background: #fff; color: var(--fv-bg); }
.fm-bubble.is-team { background: rgba(255,255,255,0.12); color: #fff; }
.fm-avatars i { border-color: var(--fv-bg); }

@media (max-width: 900px) {
  .feat-card .feat-visual, .feat-card.is-wide .feat-visual { padding: 1.5rem 1.25rem; }
}

/* Revision 18: the Healthspan score. The header row gives up its box so the
   label and the score become cells of the card's own grid: the label across
   the top, the score at display size on the left, the counts stacked on the
   right, the bar across the foot. The score scales with the panel, not the
   window, so it holds its proportion in the stack and in a phone's row. */
.feat-visual:has(.fm-score) { container-type: inline-size; }
.fm-score {
  display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;
  grid-template-areas: "title title" "big legend" "track track";
  column-gap: 1.5rem; row-gap: 1.25rem;
}
.fm-score > .fm-row:first-child { display: contents; }
.fm-score .fm-title { grid-area: title; }
.fm-score .fm-big {
  grid-area: big; align-self: end;
  font-size: clamp(4rem, 24cqi, 8.5rem); line-height: 0.78; letter-spacing: -0.06em;
  font-variant-numeric: tabular-nums;
}
.fm-score .fm-big small { font-size: var(--fs-body); letter-spacing: 0; margin-left: 0.15em; }
.fm-score .fm-legend {
  grid-area: legend; align-self: end; margin: 0;
  display: flex; flex-direction: column; align-items: stretch; gap: 0.625rem;
  font-size: var(--fs-small); line-height: var(--lh-small);
}
.fm-score .fm-legend > span {
  display: flex; align-items: baseline; gap: 0.625rem;
  padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.22);
}
.fm-score .fm-legend > span::before {
  content: ''; flex: none; width: 0.5rem; height: 0.5rem; align-self: center;
}
.fm-score .fm-legend b {
  margin: 0 auto 0 0;
  font-size: clamp(1.375rem, 6cqi, 2.25rem); line-height: 1; letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}
.fm-score .fm-track { grid-area: track; margin: 0; height: 0.75rem; gap: 4px; }
/* The drop sizes the segments inline; the field divides the bar by the counts. */
.fm-score .fm-seg { width: auto !important; }
.fm-score .fm-seg { flex-basis: 0; flex-shrink: 1; }
.fm-score .fm-seg:nth-child(1) { flex-grow: 76; }
.fm-score .fm-seg:nth-child(2) { flex-grow: 22; }
.fm-score .fm-seg:nth-child(3) { flex-grow: 4; }
.fm-score .fm-seg:nth-child(1), .fm-score .fm-legend > span:nth-child(1)::before { background: var(--tone-moss-bright); }
.fm-score .fm-seg:nth-child(2), .fm-score .fm-legend > span:nth-child(2)::before { background: var(--tone-blue-pale); }
.fm-score .fm-seg:nth-child(3), .fm-score .fm-legend > span:nth-child(3)::before { background: #fff; }

/* Revision 19: ApoB. The marker's name is the figure's headline, at display
   size against the chip; the chart is one heavy line over a square band, and
   of its points only the latest reading is drawn, larger, ringed in white. */
.feat-visual:has(.fm-apob) { container-type: inline-size; }
.fm-apob > .fm-row:first-child { align-items: flex-start; }
.fm-apob .fm-title {
  font-size: clamp(2.25rem, 9cqi, 4rem); line-height: 0.9; letter-spacing: -0.04em;
  font-weight: 500; color: #fff;
}
.fm-apob .fm-chart { overflow: visible; }
.fm-apob .fm-band { rx: 0; }
.fm-apob .fm-line { stroke-width: 2.6; stroke-linejoin: round; stroke-linecap: round; }
.fm-apob .fm-pts circle { display: none; }
.fm-apob .fm-pts circle.fm-end {
  display: inline; fill: var(--tone-moss-bright); stroke: #fff; stroke-width: 2.2;
}

/* Revision 20: Your protocol. Each item is a row under a rule: its category a
   small label above, the instruction itself at headline size. */
.feat-visual:has(.fm-plan) { container-type: inline-size; }
.feat-visual:has(.fm-plan)::after {
  background: linear-gradient(180deg, rgba(10,26,38,0.2) 0%, rgba(10,26,38,0.72) 100%);
}
.fm-plan li {
  flex-direction: column; align-items: flex-start; gap: 0.3rem;
  padding: 0.875rem 0 0;
}
.fm-plan li + li { margin-top: 0.875rem; }
.fm-plan .fm-chip, .fm-plan .fm-chip.is-moss, .fm-plan .fm-chip.is-rust {
  background: none; color: var(--tone-blue-pale); padding: 0; border-radius: 0;
  font-size: var(--fs-tiny); line-height: var(--lh-tiny); letter-spacing: 0.08em;
  text-transform: uppercase; font-weight: 500;
}
.fm-plan li > span:nth-child(2) {
  font-size: clamp(1.125rem, 4.6cqi, 1.75rem); line-height: 1.15; letter-spacing: -0.02em;
  font-weight: 500; color: #fff;
}

/* Revisions 21 to 23 size their headline rows against the panel. */
.feat-visual.tone-night, .feat-visual.tone-ink, .feat-visual.tone-blue { container-type: inline-size; }

/* Revision 21: Your care team. */
.tone-night .fm-list li { align-items: baseline; gap: 0.75rem; padding: 0.75rem 0 0; }
.tone-night .fm-list li + li { margin-top: 0.75rem; }
.tone-night .fm-list li > span:nth-child(2) {
  font-size: clamp(1.125rem, 4.6cqi, 1.75rem); line-height: 1.15; letter-spacing: -0.02em; font-weight: 500;
}
.tone-night .fm-list .fm-muted { font-size: var(--fs-small); }
.tone-night .fm-dot { width: 0.5rem; height: 0.5rem; border-radius: 0; align-self: center; }

/* Revision 22: Your clinical record, as a ledger. */
.tone-ink .fm-list li {
  display: grid; grid-template-columns: minmax(5.5rem, 26%) minmax(0, 1fr);
  align-items: baseline; gap: 1rem; padding: 0.75rem 0 0;
}
.tone-ink .fm-list li + li { margin-top: 0.75rem; }
.tone-ink .fm-list .fm-chip, .tone-ink .fm-list .fm-chip.is-moss, .tone-ink .fm-list .fm-chip.is-rust {
  background: none; color: var(--tone-blue-pale); padding: 0; border-radius: 0;
  font-size: var(--fs-tiny); line-height: var(--lh-tiny); letter-spacing: 0.08em;
  text-transform: uppercase; font-weight: 500;
}
.tone-ink .fm-list li > span:nth-child(2) {
  font-size: clamp(1.125rem, 4.6cqi, 1.75rem); line-height: 1.15; letter-spacing: -0.02em; font-weight: 500;
}
.tone-ink .fm-card > .fm-row:last-child {
  margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.22);
  font-size: var(--fs-small);
}

/* Revision 23: the concierge thread, set as type. */
.fm-thread { width: 100%; max-width: none; gap: 1rem; align-items: stretch; }
.fm-bubble, .fm-bubble.is-me, .fm-bubble.is-team {
  background: none; border-radius: 0; padding: 0; box-shadow: none;
}
.fm-bubble.is-me {
  align-self: flex-end; max-width: 75%; text-align: right;
  color: rgba(255,255,255,0.72); font-size: var(--fs-body); line-height: var(--lh-body);
}
.fm-bubble.is-team {
  display: flex; flex-direction: column; gap: 0.75rem; padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.22); color: #fff;
  font-size: clamp(1.125rem, 4.6cqi, 1.75rem); line-height: 1.2; letter-spacing: -0.02em; font-weight: 500;
}
.fm-avatars { gap: 4px; margin: 0; }
.fm-avatars i, .fm-avatars i:first-child, .fm-avatars i:last-child {
  width: 0.625rem; height: 0.625rem; border: 0; border-radius: 0; margin: 0;
}
.fm-avatars i { background: var(--tone-blue-pale); }
.fm-avatars i:first-child { background: #fff; }
.fm-avatars i:last-child { background: var(--tone-moss-bright); }

/* Revision 24: the disciplines panel. The card gives up its fill, border, blur
   and padding; each device is drawn in white and the palette's pale tones on
   the panel's own colour, with square segments, arcs and keys. */
.prod-panel .stack-card, .prod-panel .stack-card.is-feature {
  background: none; border: 0; border-radius: 0; padding: 0;
  -webkit-backdrop-filter: none; backdrop-filter: none; color: #fff;
}
.prod-panel .stack-card-head, .prod-panel .stack-card.is-feature .stack-card-head {
  text-transform: none; letter-spacing: 0.01em; font-size: var(--fs-small); line-height: var(--lh-small);
  color: rgba(255,255,255,0.72);
}
.prod-panel .team-bar { gap: 4px; height: 0.75rem; }
.prod-panel .team-seg { border-radius: 0; }
.prod-panel .team-row::before { border-radius: 0; top: 0.45em; }
.prod-panel .team-seg:nth-child(1), .prod-panel .team-row:nth-child(1)::before { background: #fff; }
.prod-panel .team-seg:nth-child(2), .prod-panel .team-row:nth-child(2)::before { background: var(--tone-blue-pale); }
.prod-panel .team-seg:nth-child(3), .prod-panel .team-row:nth-child(3)::before { background: var(--tone-moss-bright); }
.prod-panel .team-seg:nth-child(4), .prod-panel .team-row:nth-child(4)::before { background: rgba(255,255,255,0.4); }
.prod-panel .team-role { color: #fff; font-size: var(--fs-large); line-height: 1.2; font-weight: 500; letter-spacing: -0.01em; }
.prod-panel .team-note { color: rgba(255,255,255,0.72); }
.prod-panel .team-foot { border-top: 1px solid rgba(255,255,255,0.22); color: rgba(255,255,255,0.72); }
.prod-panel .team-pulse span { background: #fff; border-radius: 0; }

.prod-panel .cov-arc { stroke-linecap: butt; }
.prod-panel .cov-arc:nth-child(1), .prod-panel .cov-legend li:nth-child(1)::before { stroke: #fff; background: #fff; }
.prod-panel .cov-arc:nth-child(2), .prod-panel .cov-legend li:nth-child(2)::before { stroke: var(--tone-blue-pale); background: var(--tone-blue-pale); }
.prod-panel .cov-arc:nth-child(3), .prod-panel .cov-legend li:nth-child(3)::before { stroke: rgba(255,255,255,0.7); background: rgba(255,255,255,0.7); }
.prod-panel .cov-arc:nth-child(4), .prod-panel .cov-legend li:nth-child(4)::before { stroke: rgba(255,255,255,0.5); background: rgba(255,255,255,0.5); }
.prod-panel .cov-arc:nth-child(5), .prod-panel .cov-legend li:nth-child(5)::before { stroke: rgba(255,255,255,0.35); background: rgba(255,255,255,0.35); }
.prod-panel .cov-arc:nth-child(6), .prod-panel .cov-legend li:nth-child(6)::before { stroke: rgba(255,255,255,0.2); background: rgba(255,255,255,0.2); }
.prod-panel .cov-legend li { color: #fff; font-size: var(--fs-small); }
.prod-panel .cov-legend li::before { border-radius: 0; }
.prod-panel .cov-num, .prod-panel .cov-plus { color: #fff; }
.prod-panel .cov-label { color: rgba(255,255,255,0.72); }
.prod-panel .cov-body { padding-bottom: 1.25rem; }
.prod-panel .cov-foot { color: #fff; border-top: 1px solid rgba(255,255,255,0.22); }

.prod-panel .gate-flow { background: none; padding: 0; border-radius: 0; }
.prod-panel .gate-step {
  color: #fff; padding: 1rem 0; font-size: var(--fs-large); line-height: 1.2; font-weight: 500; letter-spacing: -0.01em;
}
.prod-panel .gate-step + .gate-step { border-top-color: rgba(255,255,255,0.22); }
.prod-panel .gate-step .gate-dot { background: #fff !important; border-color: #fff !important; color: var(--fv-bg) !important; }
.prod-panel .gate-dot svg path, .prod-panel .gate-step .gate-dot svg path { stroke: var(--fv-bg) !important; }

/* Revision 25: motion in the disciplines panel. Three curves and no others:
   a long deceleration for everything that arrives, a quick acceleration for
   what leaves, and an even in-out for the panel's colour. Every element rests
   in its final state; the entries are one-shot animations keyed on
   .is-active, so they replay on each switch and never loop. */
:root {
  --ease-arrive: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-leave: cubic-bezier(0.4, 0, 1, 1);
  --ease-turn: cubic-bezier(0.65, 0, 0.35, 1);
}
@property --cov-sweep { syntax: '<angle>'; inherits: false; initial-value: 360deg; }
@property --cov-n { syntax: '<integer>'; inherits: false; initial-value: 500; }
@keyframes fieldRise { from { opacity: 0; transform: translateY(0.75rem); } to { opacity: 1; transform: none; } }
@keyframes fieldFade { from { opacity: 0; } to { opacity: 1; } }
@keyframes fieldGrow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes fieldWipe { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes fieldSweep { from { --cov-sweep: 0deg; } to { --cov-sweep: 360deg; } }
@keyframes fieldCount { from { --cov-n: 0; } to { --cov-n: 500; } }
@keyframes fieldDrawShield { from { stroke-dashoffset: 51; } to { stroke-dashoffset: 0; } }
@keyframes fieldDrawTick { from { stroke-dashoffset: 10; } to { stroke-dashoffset: 0; } }
@keyframes fieldBreathe { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }

.prod-panel {
  transition: --fv-bg 0.9s var(--ease-turn), --fv-light 0.9s var(--ease-turn), --fv-shade 0.9s var(--ease-turn);
}
/* The panes share one cell, so the outgoing one can leave while the next
   arrives, and the panel takes the height of the tallest. */
.prod-panes { display: grid; }
.prod-pane, .prod-pane.is-active { display: flex; grid-area: 1 / 1; height: 100%; animation: none; }
.prod-pane {
  opacity: 0; visibility: hidden; transform: translateY(-0.5rem); pointer-events: none;
  transition: opacity 0.3s var(--ease-leave), transform 0.3s var(--ease-leave), visibility 0s linear 0.3s;
}
.prod-pane.is-active { opacity: 1; visibility: visible; transform: none; pointer-events: auto; transition: none; }

/* At rest, every element is in its final state. */
.prod-panel .team-seg, .prod-panel .team-row, .prod-panel .cov-num, .prod-panel .cov-plus,
.prod-panel .cov-label, .prod-panel .cov-legend li, .prod-panel .cov-foot {
  animation: none; opacity: 1; transform: none;
}
.prod-panel .cov-arc, .prod-panel .cov-foot svg path { animation: none; stroke-dashoffset: 0; }

.prod-pane.is-active .stack-card-head { animation: fieldRise 0.7s var(--ease-arrive) 0.15s both; }

/* The team: one bar growing from the left, then the rows in order. */
.prod-panel .team-seg { transform-origin: left center; }
.prod-pane.is-active .team-seg { animation: fieldGrow 1.1s var(--ease-arrive) both; }
.prod-pane.is-active .team-seg:nth-child(1) { animation-delay: 0.25s; }
.prod-pane.is-active .team-seg:nth-child(2) { animation-delay: 0.33s; }
.prod-pane.is-active .team-seg:nth-child(3) { animation-delay: 0.41s; }
.prod-pane.is-active .team-seg:nth-child(4) { animation-delay: 0.49s; }
.prod-pane.is-active .team-row { animation: fieldRise 0.8s var(--ease-arrive) both; }
.prod-pane.is-active .team-row:nth-child(1) { animation-delay: 0.45s; }
.prod-pane.is-active .team-row:nth-child(2) { animation-delay: 0.53s; }
.prod-pane.is-active .team-row:nth-child(3) { animation-delay: 0.61s; }
.prod-pane.is-active .team-row:nth-child(4) { animation-delay: 0.69s; }
.prod-pane.is-active .team-foot { animation: fieldWipe 1.2s var(--ease-arrive) 0.7s both; }
.prod-panel .team-pulse span { animation: fieldBreathe 2.4s var(--ease-turn) infinite; }
.prod-panel .team-pulse span:nth-child(2) { animation-delay: 0.3s; }
.prod-panel .team-pulse span:nth-child(3) { animation-delay: 0.6s; }
.prod-panel .team-pulse span:nth-child(4) { animation-delay: 0.9s; }

/* Coverage: the ring revealed as one sweep from twelve o'clock, the count
   running on the same curve, so the two cannot drift apart. The ring's svg is
   turned a quarter back, so the sweep starts a quarter on in its own frame. */
.prod-panel .cov-ring svg {
  -webkit-mask: conic-gradient(from 90deg, #000 var(--cov-sweep), transparent 0);
  mask: conic-gradient(from 90deg, #000 var(--cov-sweep), transparent 0);
}
.prod-pane.is-active .cov-ring svg { animation: fieldSweep 1.6s var(--ease-arrive) 0.25s both; }
.prod-panel .cov-num { font-size: 0; counter-reset: cov-n var(--cov-n); }
.prod-panel .cov-num::after {
  content: counter(cov-n); display: inline-block; min-width: 3ch; text-align: right;
  font-size: var(--fs-h3); line-height: var(--lh-h3); letter-spacing: var(--ls-h3);
  font-variant-numeric: tabular-nums;
}
.prod-pane.is-active .cov-num { animation: fieldCount 1.6s var(--ease-arrive) 0.25s both, fieldFade 0.6s var(--ease-arrive) 0.25s both; }
.prod-pane.is-active .cov-plus, .prod-pane.is-active .cov-label { animation: fieldFade 0.8s var(--ease-arrive) 0.5s both; }
.prod-pane.is-active .cov-legend li { animation: fieldRise 0.8s var(--ease-arrive) both; }
.prod-pane.is-active .cov-legend li:nth-child(1) { animation-delay: 0.35s; }
.prod-pane.is-active .cov-legend li:nth-child(2) { animation-delay: 0.47s; }
.prod-pane.is-active .cov-legend li:nth-child(3) { animation-delay: 0.59s; }
.prod-pane.is-active .cov-legend li:nth-child(4) { animation-delay: 0.71s; }
.prod-pane.is-active .cov-legend li:nth-child(5) { animation-delay: 0.83s; }
.prod-pane.is-active .cov-legend li:nth-child(6) { animation-delay: 0.95s; }
.prod-pane.is-active .cov-foot { animation: fieldWipe 1.2s var(--ease-arrive) 0.8s both; }
.prod-pane.is-active .cov-foot svg path:first-of-type { animation: fieldDrawShield 0.9s var(--ease-arrive) 1.1s both; }
.prod-pane.is-active .cov-foot svg path:last-of-type { animation: fieldDrawTick 0.5s var(--ease-arrive) 1.5s both; }

@media (prefers-reduced-motion: reduce) {
  .prod-panel, .prod-pane { transition: none; }
  .prod-pane { transform: none; }
  .prod-panel *, .prod-panel *::before, .prod-panel *::after { animation: none !important; }
}
"""


# ── 11. No arrows on actions ────────────────────────────────────────────

ARROW_SVG = r'\s*<svg\b[^>]*>\s*<path d="M\d+ \d+h10M\d+ \d+l5 5-5 5"[^>]*/>\s*</svg>'


def apply_to_page(content):
    """Strip the trailing arrow from every action on the page.

    The glyph goes from the end of each outlined, pill and plan button's
    label, and the drawn arrow from the form's submit. The words stay exactly
    as the drop has them.
    """
    label = 'actions: the arrows removed'
    pattern = re.compile(
        r'(<a\b[^>]*class="(?:btn-outline|btn-pill|plan-btn)(?: is-solid)?"[^>]*>[^<]*?)'
        r'\s*(?:&#8594;|&rarr;|\u2192)(</a>)')
    content, n = pattern.subn(r'\1\2', content)
    if n != 7:
        sys.exit(f'design revision "{label}": expected seven arrowed actions, found {n}')
    submit = _once(content, '<button class="wf-submit"', label)
    end = content.index('</button>', submit)
    button, k = re.subn(ARROW_SVG, '', content[submit:end])
    if k != 1:
        sys.exit(f'design revision "{label}": the submit button\'s arrow was not found')
    content = content[:submit] + button + content[end:]
    APPLIED.append(f'{label} ({n} labels, the submit)')
    return _apob_page(_score_page(_cool_page(_hero_photo(content))))


# ── 15. The hero photograph ─────────────────────────────────────────────

HERO_PHOTO = {'src': '/images/hero-portrait.webp', 'width': '2560', 'height': '1089'}
DROP_PHOTO = {'src': '/images/hero.webp', 'width': '1600', 'height': '800'}


def _hero_photo(content):
    label = 'hero: the new photograph'
    start = _once(content, 'class="hero-img"', label)
    end = content.index('/>', start)
    img = content[start:end]
    for attr, value in HERO_PHOTO.items():
        img, n = re.subn(f'{attr}="{re.escape(DROP_PHOTO[attr])}"', f'{attr}="{value}"', img)
        if n != 1:
            sys.exit(f'design revision "{label}": expected the hero image\'s '
                     f'{attr}="{DROP_PHOTO[attr]}", which the drop no longer has')
    APPLIED.append(label)
    return content[:start] + img + content[end:]


# ── 8. The superseded footer ────────────────────────────────────────────

def apply_to_footer(footer):
    label = 'footer: the empty media layer and divider removed'
    for el in ('<div class="footer-media" aria-hidden="true"></div>',
               '<div class="footer-divider"></div>'):
        i = _once(footer, el, label)
        line_start = footer.rfind('\n', 0, i) + 1
        footer = footer[:line_start] + footer[i + len(el):].lstrip(' ').lstrip('\n')
    footer = re.sub(r'\n[ \t]*\n([ \t]*\n)+', '\n\n', footer)
    APPLIED.append(label)
    return footer


# The dark footer as the drop declares it, rule for rule. Every property here is
# overridden later in the drop by the white footer that replaced it, or paints
# an element that is hidden; matched exactly, so a drop that revives any of it
# stops the port rather than losing it silently.
DARK_FOOTER = re.compile(
    r'\.site-footer \{ background: #08090b; color: #fff; \}\n'
    r'\.footer-media \{ background: #08090b; \}\n'
    r'\.footer-media::before \{[^}]*\}\n'
    r'\.footer-media::after \{ display: none; \}\n'
    r'\.footer-divider \{ background: rgba\(255,255,255,0\.14\); \}\n'
    r'\.footer-logo, \.footer-col-title \{ color: #fff; \}\n'
    r'\.footer-tagline, \.footer-col a \{ color: rgba\(255,255,255,0\.62\); \}\n'
    r'\.footer-col a:hover \{ color: #fff; \}\n'
    r'\.footer-copy, \.footer-legal a \{ color: rgba\(255,255,255,0\.62\); \}\n'
    r'\.footer-legal a:hover \{ color: #fff; \}\n')

GONE = r'\.footer-(?:media|img|divider)\b'


def _footer(css):
    label = 'footer: the superseded dark footer removed from the stylesheet'
    css, n = DARK_FOOTER.subn('', css)
    if n != 1:
        sys.exit(f'design revision "{label}": expected the dark footer block once, found {n}')
    # Rules for the two removed elements, and for the photograph the first
    # footer carried, wherever they sit: only rules whose every selector names
    # one of them, so no shared rule is touched.
    def drop(m):
        sels = [s.strip() for s in m.group(1).split(',')]
        return '' if all(re.search(GONE, s) for s in sels) else m.group(0)
    css = re.sub(r'(?m)^[ \t]*([^{}@\n][^{}]*)\{[^{}]*\}[ \t]*\n', drop, css)
    left = re.findall(r'[^{}]*' + GONE + r'[^{}]*\{', css)
    if left:
        sys.exit(f'design revision "{label}": still referenced: {left}')
    APPLIED.append(label)
    return css


# ── 3. Almost-square corners everywhere ─────────────────────────────────

CONTROL = '6px'   # buttons, chips, tags, inputs, badges: the bar's action
SURFACE = '12px'  # cards, panels, the form, the figures: the bar's island


def _corner(part):
    """One radius, mapped onto the two-step scale by the size it had.

    A pill (anything 40px or more) was a control, and goes to CONTROL. A large
    radius (14px to 40px) was a surface, and goes to SURFACE. 7px to 10px was a
    small control, an input or a dropdown option, and joins the buttons at
    CONTROL. Circles in % and corners already this small or smaller are left.
    rem is read at 16px, which is near enough to sort a radius into its band.
    """
    m = re.fullmatch(r'(\d*\.?\d+)(px|rem|em)', part)
    if not m:
        return part
    px = float(m.group(1)) * (1 if m.group(2) == 'px' else 16)
    if px >= 40:
        return CONTROL
    if px >= 14:
        return SURFACE
    if 7 <= px <= 10:
        return CONTROL
    return part


def _boxy(css):
    count = 0

    def sub(m):
        nonlocal count
        value, important = m.group(2), m.group(3) or ''
        new = ' '.join(_corner(p) for p in value.split())
        if new != value:
            count += 1
        return m.group(1) + new + important

    css = re.sub(r'(border-radius\s*:\s*)([^;}!]+?)(\s*!important)?(?=\s*[;}])', sub, css)
    APPLIED.append(f'corners: {count} radii moved onto the 6px and 12px scale')
    return css


# ── 4. The unused accent ramps ──────────────────────────────────────────

RAMPS = r'(?:vermillion|green|yellow|pink)-\d+'


def _palette(css):
    label = 'palette: the unused accent ramps removed'
    for old, new in (('var(--yellow-700)', 'var(--tone-blue-light)'),
                     ('var(--yellow-50)', 'var(--tone-blue-tint)'),
                     ('var(--yellow-100)', 'var(--tone-blue-tint)')):
        css = css.replace(old, new)
    css, n = re.subn(r'[ \t]*(?:--' + RAMPS + r':\s*#[0-9a-fA-F]{3,8};\s*)+\n', '', css)
    if n == 0:
        sys.exit(f'design revision "{label}": the ramp declarations were not found')
    left = re.findall(r'--' + RAMPS, css)
    if left:
        sys.exit(f'design revision "{label}": still referenced: {sorted(set(left))}')
    APPLIED.append(label)
    return css


# ── 16. Moss and night blue ─────────────────────────────────────────────

# The warm tones as the drop declares them, matched exactly so a drop that
# changes them stops the port rather than half-converting.
WARM_DECLS = (
    '  --tone-rust: #83392c; --tone-rust-deep: #5e2d24; --tone-rust-soft: #854937;\n'
    '  --tone-umber: #623f30; --tone-umber-deep: #351f1c;\n'
    '  --tone-bronze: #917e64; --tone-taupe: #736050; --tone-olive: #5e503a;\n'
    '  --tone-sand: #bd9f82; --tone-sand-pale: #b0ab9a;\n')
WARM_TINTS = '  --tone-rust-tint: #f3e6e1; --tone-sand-tint: #f1ebe3; --tone-moss-tint: #e4ebe5;\n'

# The two families that replace them. Moss keeps the drop's three steps and
# tint and gains the light stop its panel already used; night blue is the
# hero photograph's sky, until now written into each rule by hand.
COOL_TONES = (
    '  --tone-moss-bright: #4a7a5c; --tone-moss-tint: #e4ebe5;\n'
    '  --tone-night: #0a1a26; --tone-blue-deep: #10293a; --tone-blue: #1b4561;\n'
    '  --tone-blue-light: #2a5f83; --tone-blue-pale: #9fbbd0; --tone-blue-tint: #e6edf2;\n')

# Every warm tone, by role, onto its cool counterpart. The accent (rust) becomes
# the light moss: white on it holds 6.5:1, and it still separates from the
# night-blue island the bar's action sits in. Its tint and its deeper steps go
# to moss with it; the secondary warm tones (umber, bronze, taupe, olive, sand)
# go to night blue, so the two families divide the page between them.
WARM_TO_COOL = {
    'rust': 'moss-light', 'rust-deep': 'moss-deep', 'rust-soft': 'moss',
    'rust-tint': 'moss-tint',
    'umber': 'blue', 'umber-deep': 'blue-deep',
    'bronze': 'blue-light', 'taupe': 'blue', 'olive': 'night',
    'sand': 'blue-pale', 'sand-pale': 'blue-pale', 'sand-tint': 'blue-tint',
}
WARM_TOKEN = re.compile(r'--tone-(rust|umber|bronze|taupe|olive|sand)(-deep|-soft|-tint|-pale)?\b')
ACCENT_RGB = '59,101,75'  # --tone-moss-light, for the drop's translucent rust
RUST_RGBA = re.compile(r'rgba\(\s*131\s*,\s*57\s*,\s*44\s*,')

# The four feature panels drawn from warm tones take cool ones, under new names
# so no class says rust where the colour is moss.
WARM_PANELS = {'tone-sand': 'tone-night', 'tone-rust': 'tone-pine', 'tone-umber': 'tone-tide'}
WARM_PANEL_RULES = (
    '.feat-visual.tone-sand  { --fv-bg: var(--tone-taupe); --fv-light: #d9bfa1; --fv-shade: var(--tone-olive); }\n'
    '.feat-visual.tone-rust  { --fv-bg: var(--tone-rust);  --fv-light: #b0634a; --fv-shade: var(--tone-rust-deep); }\n'
    '.feat-visual.tone-umber { --fv-bg: var(--tone-umber); --fv-light: var(--tone-bronze); --fv-shade: var(--tone-umber-deep); }\n')
COOL_PANEL_RULES = (
    '.feat-visual.tone-night { --fv-bg: var(--tone-blue-deep);  --fv-light: var(--tone-blue-light);  --fv-shade: var(--tone-night); }\n'
    '.feat-visual.tone-pine  { --fv-bg: var(--tone-moss-deep);  --fv-light: var(--tone-moss-light);  --fv-shade: var(--tone-night); }\n'
    '.feat-visual.tone-tide  { --fv-bg: var(--tone-blue);       --fv-light: var(--tone-moss-bright); --fv-shade: var(--tone-moss-deep); }\n')

WARM_LEFT = re.compile(
    r'--tone-(?:rust|umber|bronze|taupe|olive|sand)\b|rgba\(\s*131\s*,\s*57\s*,\s*44\b|'
    r'#(?:83392c|5e2d24|854937|623f30|351f1c|917e64|736050|5e503a|bd9f82|b0ab9a|f3e6e1|f1ebe3|b0634a|d9bfa1)\b',
    re.I)


def _warm_token(m):
    return '--tone-' + WARM_TO_COOL[m.group(1) + (m.group(2) or '')]


def _cool(css):
    label = 'palette: the warm tones replaced by moss and night blue'
    i = _once(css, WARM_DECLS, label)
    css = css[:i] + css[i + len(WARM_DECLS):]
    i = _once(css, WARM_TINTS, label)
    css = css[:i] + COOL_TONES + css[i + len(WARM_TINTS):]
    i = _once(css, WARM_PANEL_RULES, label)
    css = css[:i] + COOL_PANEL_RULES + css[i + len(WARM_PANEL_RULES):]
    css, n = WARM_TOKEN.subn(_warm_token, css)
    # A typed custom property's initial value has to be a literal colour.
    i = _once(css, '--fv-light { syntax: \'<color>\'; inherits: true; initial-value: #83392c; }', label)
    css = css.replace('initial-value: #83392c;', 'initial-value: #3b654b;', 1)
    css, k = RUST_RGBA.subn(f'rgba({ACCENT_RGB},', css)
    APPLIED.append(f'{label} ({n} references, {k} translucent)')
    return css


def _cool_page(content):
    label = 'palette: the warm panels and chart marks moved to moss and night blue'
    for old, new in WARM_PANELS.items():
        content, n = re.subn(rf'class="feat-visual {old}"', f'class="feat-visual {new}"', content)
        if n != 1:
            sys.exit(f'design revision "{label}": expected one {old} panel, found {n}')
    content, n = WARM_TOKEN.subn(_warm_token, content)
    if n != 3:
        sys.exit(f'design revision "{label}": expected three warm chart marks, found {n}')
    APPLIED.append(label)
    return content


# ── 18. The Healthspan score ────────────────────────────────────────────

def _score_page(content):
    label = 'healthspan: the score card marked for its own layout'
    content, n = re.subn(r'(<div class="feat-visual tone-moss" aria-hidden="true">\s*<div class="fm-card)(">)',
                         r'\1 fm-score\2', content)
    if n != 1:
        sys.exit(f'design revision "{label}": expected one score card in the moss panel, found {n}')
    APPLIED.append(label)
    return content


# ── 19. ApoB ────────────────────────────────────────────────────────────

def _apob_page(content):
    label = 'apob: the chart card marked, its latest reading drawn larger'
    content, n = re.subn(r'(<div class="feat-visual tone-pine" aria-hidden="true">\s*<div class="fm-card)(">)',
                         r'\1 fm-apob\2', content)
    if n != 1:
        sys.exit(f'design revision "{label}": expected one chart card in the pine panel, found {n}')
    content, n = re.subn(r'<circle cx="304" cy="86" r="3.5"/>',
                         '<circle class="fm-end" cx="304" cy="86" r="6"/>', content)
    if n != 1:
        sys.exit(f'design revision "{label}": expected the latest reading at 304,86 once, found {n}')
    APPLIED.append(label)
    return content


# ── 5. The type scale ───────────────────────────────────────────────────

TYPE = """html { font-size: 100%; }

/* The type scale. The root is a fixed 16px, so spacing in rem does not move
   with the window; the headings scale instead, each between a phone and a
   1440px desktop through clamp(), and hold there. Display sizes tighten as
   they grow: the larger the tier, the closer its leading and its tracking. */
:root {
  --fs-h1: clamp(2.25rem, 1.5rem + 2.3vw, 3.5rem);        --lh-h1: 1.02;  --ls-h1: -0.032em;
  --fs-h2l: clamp(2rem, 1.45rem + 1.6vw, 2.875rem);
  --fs-h2: clamp(1.75rem, 1.35rem + 1.2vw, 2.375rem);     --lh-h2: 1.1;   --ls-h2: -0.024em;
  --fs-h3: clamp(1.375rem, 1.15rem + 0.7vw, 1.875rem);    --lh-h3: 1.2;   --ls-h3: -0.018em;
  --fs-h4: clamp(1.1875rem, 1.05rem + 0.4vw, 1.4375rem);  --lh-h4: 1.3;   --ls-h4: -0.012em;
  --fs-large: clamp(1.0625rem, 0.98rem + 0.3vw, 1.25rem); --lh-large: 1.45; --ls-large: -0.008em;
  --fs-medium: 1.0625rem; --lh-medium: 1.5;  --ls-medium: -0.004em;
  --fs-body: 1rem;        --lh-body: 1.55;   --ls-body: 0;
  --fs-ui: 0.9375rem;     --lh-ui: 1.4;      --ls-ui: 0;
  --fs-small: 0.8125rem;  --lh-small: 1.5;   --ls-small: 0.003em;
  --fs-tiny: 0.6875rem;   --lh-tiny: 1.45;   --ls-tiny: 0.02em;
}"""


def _type(css):
    label = 'type: a new scale on a fixed root'
    m = re.search(r'html \{ font-size: [^}]*\}\n(?:@media[^\n]*html \{ font-size:[^\n]*\n)*\n?'
                  r':root \{\n  --fs-h1:[\s\S]*?\n\}\n'
                  r'(?:@media \(max-width: \d+px\) \{\n  :root \{ --fs-[^\n]*\n\}\n)*', css)
    if not m:
        sys.exit(f'design revision "{label}": the drop\'s type block was not found')
    css = css[:m.start()] + TYPE + '\n' + css[m.end():]
    # The phone breakpoint resets three tiers to fixed sizes; clamp() covers it.
    css, n = re.subn(r'[ \t]*:root \{ --fs-h1: [^}]*\}\n', '', css)
    if n != 1:
        sys.exit(f'design revision "{label}": expected one phone reset of the tiers, found {n}')
    if re.search(r'html \{ font-size: calc', css):
        sys.exit(f'design revision "{label}": a fluid root survived')
    APPLIED.append(label)
    return css


def apply_to_css(css):
    css = _footer(css)
    css = _palette(css)
    css = _cool(css)
    css = _type(css)
    css = _boxy(css)
    APPLIED.append('bar: one light island of fixed width')
    APPLIED.append('hero: the photograph fills the first screen, edge to edge')
    APPLIED.append('what you get: an index of rows, not a grid of tall panels')
    APPLIED.append('buttons: secondaries on dark grounds are text links')
    APPLIED.append('close: a centred statement over a panorama, not copy on a photograph')
    APPLIED.append('chips: the two on dark grounds solid, not glass')
    APPLIED.append('figures: flat fields, no card, no blur')
    APPLIED.append('healthspan: the score as a field')
    APPLIED.append('apob: the marker as a field')
    APPLIED.append('protocol: the items as rows on the field')
    APPLIED.append('care team: the disciplines as rows on the field')
    APPLIED.append('clinical record: a ledger on the field')
    APPLIED.append('concierge: the thread set as type, not bubbles')
    APPLIED.append('disciplines: the three devices drawn on the field')
    APPLIED.append('disciplines: one choreography, panes that cross, nothing that loops')
    css = css.rstrip('\n') + '\n' + CSS
    left = sorted(set(m.group(0) for m in WARM_LEFT.finditer(css)))
    if left:
        sys.exit(f'design revision "palette": warm tones survived: {left}')
    return css
