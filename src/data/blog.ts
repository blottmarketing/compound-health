// ─────────────────────────────────────────────────────────────────────────────
// Compound Health — blog data
//
// Single source of truth for authors, categories and posts. Imported by
// /blog, /blog/[slug], /blog/category/[category] and /authors/[author].
//
// All routes are currently noindex (see BlogLayout). Content here is dummy
// placeholder copy for layout review only.
// ─────────────────────────────────────────────────────────────────────────────

export interface Author {
  /** URL slug, e.g. "imogen-asher" → /authors/imogen-asher */
  slug: string;
  name: string;
  role: string;
  /** Two-letter monogram for the avatar bubble (e.g. "IA"). */
  initials: string;
  bio: string;
}

export interface Category {
  /** URL slug, e.g. "research" → /blog/category/research */
  slug: string;
  name: string;
  description: string;
}

export interface Post {
  /** URL slug, e.g. "biomarkers-that-matter" → /blog/biomarkers-that-matter */
  slug: string;
  title: string;
  /** Short summary used on cards and OG description. */
  excerpt: string;
  /** ISO date string, e.g. "2026-05-28". */
  date: string;
  /** Estimated read time in minutes. */
  readTime: number;
  /** Eyebrow shown above the title on the post page. */
  eyebrow: string;
  /** Slugs of one or more authors. First author is treated as lead. */
  authorSlugs: string[];
  /** Slug of the primary category. */
  categorySlug: string;
  /** Free-form tags (in addition to the category). */
  tags: string[];
  /** Article body rendered as raw HTML. */
  bodyHtml: string;
  /** If true, surfaced as the hero card on the parent /blog page. */
  featured?: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// Authors
// ─────────────────────────────────────────────────────────────────────────────

export const authors: Author[] = [
  {
    slug: 'imogen-asher',
    name: 'Imogen Asher',
    role: 'Chief Medical Officer, Compound Health',
    initials: 'IA',
    bio: 'Dr Imogen Asher leads clinical strategy at Compound Health. Previously a consultant in preventive cardiology at a London teaching hospital, she has spent the last decade building longevity programs for private clients and family offices across Europe and the Middle East.',
  },
  {
    slug: 'henry-cavendish',
    name: 'Henry Cavendish',
    role: 'Head of Longevity Research, Compound Health',
    initials: 'HC',
    bio: 'Henry Cavendish heads research at Compound Health, where he translates the latest evidence in biomarker science and preventive medicine into usable protocols for members. He writes regularly on biological age, metabolic health and the practical limits of what data can tell us.',
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// Categories
// ─────────────────────────────────────────────────────────────────────────────

export const categories: Category[] = [
  {
    slug: 'research',
    name: 'Research',
    description:
      'New evidence, recent studies and the science our clinical team is watching, summarized for a non-clinical reader.',
  },
  {
    slug: 'insights',
    name: 'Insights',
    description:
      'How our members and partner advisors are thinking about healthspan, prevention and the practicalities of building a longevity program.',
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// Posts
// ─────────────────────────────────────────────────────────────────────────────

export const posts: Post[] = [
  {
    slug: 'biomarkers-that-matter-after-fifty',
    title: 'The biomarkers that actually matter after fifty',
    excerpt:
      'A working list of the panels and metrics our clinical team prioritizes for members in their sixth decade, and the ones we have learned to ignore.',
    date: '2026-05-28',
    readTime: 7,
    eyebrow: 'Clinical perspective',
    authorSlugs: ['imogen-asher', 'henry-cavendish'],
    categorySlug: 'research',
    tags: ['Biomarkers', 'Preventive medicine', 'Cardiometabolic'],
    featured: true,
    bodyHtml: `
      <p>Most of our new members arrive with a folder of bloodwork that runs to dozens of pages. Some of it is genuinely useful. Much of it is noise dressed up as data. Over the last two years our clinical team has refined a short list of biomarkers we treat as foundational for any member over fifty, and a longer list we order only when the foundational picture justifies it.</p>
      <h2>What we test first</h2>
      <p>Cardiovascular risk remains the single largest determinant of healthspan in this cohort, and our first-line panel reflects that. We start with apolipoprotein B rather than LDL cholesterol, lipoprotein(a) once in a member's lifetime, and a high-sensitivity C-reactive protein to capture systemic inflammation. Insulin resistance is screened with fasting insulin and HOMA-IR, not fasting glucose alone.</p>
      <p>For metabolic and hormonal health we order a comprehensive thyroid panel, sex hormones with SHBG, and IGF-1. Vitamin D, ferritin and a homocysteine reading round out the foundation.</p>
      <h2>What we order selectively</h2>
      <p>Coronary artery calcium scoring, advanced lipoprotein subfractions, continuous glucose monitoring and DEXA-derived visceral fat estimates are all useful, but only once the first-line panel raises a specific question. Ordering them upfront tends to produce findings without context.</p>
      <h2>What we have stopped ordering</h2>
      <p>Broad food-sensitivity panels, untargeted heavy-metal screens and most "wellness" hormone panels have been quietly retired from our protocols. The evidence base is thin and the false-positive rate is high enough that they generate more anxiety than insight.</p>
      <p>None of this is a substitute for a conversation with your clinician. It is, however, a reasonable starting point for the conversation itself.</p>
    `,
  },
  {
    slug: 'what-vo2-max-really-tells-you',
    title: 'What VO2 max really tells you, and what it does not',
    excerpt:
      'VO2 max has become the single most cited number in longevity. Here is how we use it with members, and the three caveats we always attach to the result.',
    date: '2026-05-21',
    readTime: 6,
    eyebrow: 'Performance',
    authorSlugs: ['henry-cavendish'],
    categorySlug: 'research',
    tags: ['VO2 max', 'Cardiorespiratory fitness', 'Testing'],
    bodyHtml: `
      <p>VO2 max is having a moment. It is also one of the most reliable predictors of all-cause mortality we have. Both can be true.</p>
      <h2>What the number is</h2>
      <p>VO2 max measures the maximum volume of oxygen your body can use during intense exercise. It is reported in millilitres of oxygen per kilogram of body mass per minute. For a member in their fifties, anything in the top quintile for their age and sex is associated with substantially lower long-term mortality than the bottom quintile.</p>
      <h2>The three caveats we attach</h2>
      <p>First, the test you took matters. A treadmill ramp protocol with gas exchange is the reference standard. A wrist-based estimate from a consumer wearable is a useful trend line, but not a diagnostic figure.</p>
      <p>Second, VO2 max is highly trainable. A member who improves from the 30th to the 60th percentile over twelve months has done something substantive, regardless of where they started.</p>
      <p>Third, no single biomarker captures fitness. Resting heart rate, heart-rate recovery and grip strength all add information that VO2 max alone does not provide.</p>
      <h2>How we use it</h2>
      <p>We test on intake, then again at month six and month twelve. The trajectory is more useful than the absolute number, particularly when paired with the member's training data over the same period.</p>
    `,
  },
  {
    slug: 'longevity-and-the-family-balance-sheet',
    title: 'Longevity and the family balance sheet',
    excerpt:
      'Why a growing number of family offices are now treating healthspan as a line item on the annual client review, sitting alongside net worth.',
    date: '2026-05-14',
    readTime: 5,
    eyebrow: 'Advisor briefing',
    authorSlugs: ['imogen-asher'],
    categorySlug: 'insights',
    tags: ['Family office', 'Wealth advisory', 'Healthspan'],
    bodyHtml: `
      <p>For most of the families we work with, the annual client review covers portfolio performance, tax position, succession structure and philanthropy. Health, until recently, sat outside the conversation. That is changing.</p>
      <h2>The shift</h2>
      <p>Several of our advisor partners now report a single healthspan score alongside net worth on the annual review. The score is composed from a member's diagnostics, biomarker trends and lifestyle data, normalised to their age and sex. It is updated quarterly.</p>
      <p>The point is not to clinicalise the relationship between principal and advisor. It is to give the principal one number they can act on, and one number their advisor can reference without overstepping.</p>
      <h2>Why advisors are leaning in</h2>
      <p>Three reasons come up consistently in our conversations. The first is retention: principals who feel their advisor is concerned with the years they have, not only the assets, refer more and switch less. The second is succession: a healthspan trajectory shapes the timing of generational transfer in a way the family is rarely prepared to discuss without a structured prompt. The third is differentiation: the firms moving fastest on this are setting an expectation the rest of the channel will need to meet.</p>
      <h2>What it does not replace</h2>
      <p>A healthspan score is not a substitute for a clinical relationship, and we are careful that our advisor partners do not present it as one. Members still see clinicians; advisors still see assets. The score sits between the two as a shared reference point, no more and no less.</p>
    `,
  },
  {
    slug: 'continuous-glucose-monitoring-for-non-diabetics',
    title: 'Continuous glucose monitoring for non-diabetics: useful, with conditions',
    excerpt:
      'CGMs have moved from a diabetes management tool to a mainstream longevity device. We outline where the evidence supports their use, and where it does not.',
    date: '2026-05-07',
    readTime: 6,
    eyebrow: 'Devices',
    authorSlugs: ['henry-cavendish'],
    categorySlug: 'research',
    tags: ['CGM', 'Metabolic health', 'Wearables'],
    bodyHtml: `
      <p>The continuous glucose monitor is now a fixture of any serious longevity program. It is also one of the most over-interpreted data sources we work with. Both observations matter.</p>
      <h2>Where the evidence is strong</h2>
      <p>For members with pre-diabetes, established insulin resistance or a family history of type 2 diabetes, two-week CGM cycles produce genuinely useful behavioral insight. Members see, in real time, how their breakfast choices, sleep quality and training timing interact with their glucose curves. The behavior change tends to stick.</p>
      <h2>Where it is overstated</h2>
      <p>For metabolically healthy members, the marginal information from a CGM is small. Glucose excursions after a meal are a normal physiological response, not a pathology. We have seen members worry themselves into eliminating foods that were not contributing to any meaningful metabolic risk.</p>
      <h2>How we deploy CGMs</h2>
      <p>Two two-week cycles per year is our default for members who have a clinical indication. For everyone else, we treat it as an optional educational tool rather than a recurring metric.</p>
    `,
  },
  {
    slug: 'sleep-the-biomarker-we-undervalue',
    title: 'Sleep, the biomarker we have systematically undervalued',
    excerpt:
      'A primer on why our clinical team treats sleep architecture, not sleep duration, as one of the most consequential signals in a member’s profile.',
    date: '2026-04-30',
    readTime: 5,
    eyebrow: 'Foundations',
    authorSlugs: ['imogen-asher'],
    categorySlug: 'research',
    tags: ['Sleep', 'Recovery', 'Cognitive health'],
    bodyHtml: `
      <p>The single most consistent observation across our member base is that sleep is the input most members under-deliver on, and the one that compounds fastest when they get it right.</p>
      <h2>Duration is the easy part</h2>
      <p>Seven to nine hours is the population-level recommendation, and it remains a reasonable starting point. But the members who see the largest gains are not the ones lengthening their time in bed. They are the ones whose sleep architecture is improving: more time in deep and REM stages, fewer awakenings, more stable heart-rate variability through the night.</p>
      <h2>What we measure</h2>
      <p>We use a combination of wearable data and, for members with persistent symptoms, a home polysomnography study. We are looking for stage distribution, sleep efficiency and, increasingly, for signs of undiagnosed sleep-disordered breathing, which is materially under-detected in high-functioning adults.</p>
      <h2>What we intervene on</h2>
      <p>Light exposure, alcohol, evening training schedule and core body temperature account for the majority of the wins we see in the first ninety days. Pharmacological intervention is reserved for cases where the underlying drivers have already been addressed.</p>
    `,
  },
  {
    slug: 'a-note-on-biological-age-tests',
    title: 'A note on biological age tests, and why we are still cautious',
    excerpt:
      'Biological age tests are a useful concept, an interesting research tool, and a marketing category that has gotten ahead of the evidence. We explain the distinction.',
    date: '2026-04-23',
    readTime: 6,
    eyebrow: 'Critical view',
    authorSlugs: ['henry-cavendish', 'imogen-asher'],
    categorySlug: 'insights',
    tags: ['Biological age', 'Epigenetics', 'Methodology'],
    bodyHtml: `
      <p>Biological age tests are now a fixture of the longevity market. The pitch is intuitive: a single number, derived from your epigenetic or proteomic profile, that tells you how old your body actually is. We use them ourselves, with members who are interested. We are also careful about how much weight we put on the result.</p>
      <h2>The concept is sound</h2>
      <p>The underlying science, particularly around DNA methylation clocks, is genuinely interesting. Several second-generation clocks correlate meaningfully with all-cause mortality, and the field is moving quickly.</p>
      <h2>The test you took is the question</h2>
      <p>Not every biological age test is equivalent. First-generation clocks were trained to predict chronological age. Second-generation clocks were trained to predict mortality. Third-generation clocks are trained to predict the pace of aging. They are different tools answering different questions, and they should not be compared like-for-like.</p>
      <h2>Variability is high</h2>
      <p>A single biological age reading from one provider, taken once, is a snapshot with meaningful test-to-test variability. Trends across several readings, from the same provider, using the same methodology, are far more informative.</p>
      <h2>How we use them</h2>
      <p>We order biological age testing for members who are specifically interested in tracking it, on an annual cadence, with the caveats above made explicit. We do not use the result to drive protocol changes that the foundational biomarker panel does not already support.</p>
    `,
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// Lookup helpers
// ─────────────────────────────────────────────────────────────────────────────

export function getAuthor(slug: string): Author | undefined {
  return authors.find((a) => a.slug === slug);
}

export function getCategory(slug: string): Category | undefined {
  return categories.find((c) => c.slug === slug);
}

export function getPost(slug: string): Post | undefined {
  return posts.find((p) => p.slug === slug);
}

export function postsByAuthor(slug: string): Post[] {
  return posts.filter((p) => p.authorSlugs.includes(slug));
}

export function postsByCategory(slug: string): Post[] {
  return posts.filter((p) => p.categorySlug === slug);
}

/** Posts sorted newest first. */
export function sortedPosts(list: Post[] = posts): Post[] {
  return [...list].sort((a, b) => (a.date < b.date ? 1 : -1));
}

/** Format an ISO date as e.g. "28 May 2026". */
export function formatDate(iso: string): string {
  const d = new Date(iso + 'T00:00:00Z');
  return d.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  });
}
