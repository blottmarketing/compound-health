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
    note: 'One warm ground, tinted bento cells, interactive product panels, the Duna idiom.',
    status: 'ready',
  },
  {
    id: 'v1-1',
    label: 'v1.1',
    path: '/v1-1',
    note: 'An iteration on v1.',
    status: 'planned',
  },
  {
    id: 'v2',
    label: 'v2',
    path: '/v2',
    note: 'A second direction.',
    status: 'planned',
  },
  {
    id: 'v3',
    label: 'v3',
    path: '/v3',
    note: 'A third direction.',
    status: 'planned',
  },
];

/** Everything the switcher shows, live design first. */
export const SWITCHER: Variant[] = [LIVE, ...VARIANTS];

export function getVariant(id: string): Variant {
  const found = SWITCHER.find(v => v.id === id);
  if (!found) throw new Error(`Unknown variant: ${id}`);
  return found;
}
