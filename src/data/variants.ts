/**
 * Home page design variations.
 *
 * `/` is the live design. Everything under a variant path is a candidate redesign,
 * kept side by side so they can be compared in one sitting. Every variant route is
 * noindex and stays out of public/sitemap.xml.
 *
 * Adding a variation: add a row here, create src/pages/<path>/index.astro, and give it
 * its own stylesheet under src/styles/variants/ plus its own layout under
 * src/layouts/variants/. Variations never share a stylesheet, so one can be changed
 * without touching another.
 */

export interface Variant {
  /** Short id, also the folder name under src/pages. */
  id: string;
  /** Label in the switcher. */
  label: string;
  /** Route, no trailing slash. */
  path: string;
  /** One line on what this variation is. */
  note: string;
  /** 'ready' has a real page, 'planned' is a placeholder. */
  status: 'ready' | 'planned';
}

export const LIVE: Variant = {
  id: 'live',
  label: 'Live',
  path: '/',
  note: 'The design currently in production.',
  status: 'ready',
};

export const VARIANTS: Variant[] = [
  {
    id: 'v1',
    label: 'v1',
    path: '/v1',
    note: "The client's final v1: superpower.com's type scale and zinc palette over the brand's "
      + 'rust, umber, bronze and moss, Aeonik, a nav that collapses into a blurred pill, a photographic '
      + 'hero card, and a fixed footer the closing card uncovers.',
    status: 'ready',
  },
  {
    id: 'v2',
    label: 'v2',
    path: '/v2',
    note: 'The joindawn.com idiom: a dark ground that a sunrise gradient carries into cream, one great circle drawn by scroll, serif display type, gradient pills.',
    status: 'ready',
  },
  {
    id: 'v3',
    label: 'v3',
    path: '/v3',
    note: 'The lassie.ai idiom: one cream ground and no bands, a light serif at 350, a floating glass nav pill, and scroll used as a mechanism — the hero window closes, a deck of panels deals itself, six tiles orbit a line that changes under them.',
    status: 'ready',
  },
];

/** Everything the switcher shows, live design first. */
export const SWITCHER: Variant[] = [LIVE, ...VARIANTS];

export function getVariant(id: string): Variant {
  const found = SWITCHER.find(v => v.id === id);
  if (!found) throw new Error(`Unknown variant: ${id}`);
  return found;
}
