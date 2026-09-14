import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://compoundhealth.io',

  /**
   * /for-advisors redirects to the home page. The page itself is kept at
   * src/pages/_for-advisors.astro: the leading underscore takes it out of
   * routing, so the draft stays in the tree without answering a request and
   * without colliding with the redirect below.
   *
   * A static build emits this as a meta-refresh document with a canonical at
   * the target, not a 301. The real 301 belongs at the host, alongside the
   * www and trailing-slash decisions that are still open.
   */
  redirects: {
    '/for-advisors': '/',
  },
});
