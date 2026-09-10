# v3 artwork brief

v3 is the [lassie.ai](https://www.lassie.ai/) idiom. Lassie is a photography-led site: the page ground
is one flat bone, the type is a serif and a grotesk, the interface is drawn as flat vector cards, and
every moment of colour, warmth and depth in the page comes from a photograph. Take the photographs
away and there is almost nothing left. So the images are not decoration in v3, they are the design.

Every photo slot ships as a styled placeholder until a render exists. The renders are generated
outside the repo, in ChatGPT, from the prompts below, then dropped into `public/images/v3/`.

**Status, 2026-09-10.** Brief written, no renders yet. Four slots are wired and rendering their
placeholders: `hero-cover`, `quad-photo-a`, `quad-photo-b`, `closing-frame`. The three `step-*`
slots are not used by the build, because those three frames are drawn rather than photographed.

## The register

Lassie's product is medical admin, and their answer to it was a wild spring meadow at midday: yellow
poppies against blue sky, shot close and low, plus defocused fragments of a working clinic. Loud,
warm, and deliberately not medical.

Ours is a private longevity membership for UHNW clients, introduced through their wealth advisor.
The equivalent register is not wildness but **tended ground at first light, and the private rooms
that serve it**: an olive grove, clipped grass under dew, still water, cut stone, linen, a hand on a
desk. Photographed close, at a wide aperture, in the cold blue light of very early morning warming
into low gold. Nothing is loud and nothing is wild. It should read the way a very good private house
reads: quiet, expensive, cared for, and obviously alive.

Two families run through every slot, and they alternate:

1. **Ground truth.** Close, mostly defocused living detail: olive leaves, dew on clipped grass, a
   single stem, the surface of water. This is our poppy. It is where the colour and the warmth come
   from, and it is what sits behind the interface cards.
2. **Rooms and hands.** Quiet architectural interiors and human fragments: a forearm on linen, a
   hand at a desk, a figure through glass, light crossing a stone floor. This is where the human and
   the clinical live, and it is always implied by material, never by props.

## How the reference uses imagery

Worth knowing before writing a prompt, because the layout assumes these qualities.

**Photography.** Their ground is `#F9F8F5`. Photographs appear in five treatments. The hero is
full-bleed and full-viewport (`object-fit: cover`, no radius), shot through a glass partition so the
whole frame is optically softened, cool blue-green, and mid-dark through the middle so white serif
type reads on it with no scrim. The three big feature panels are 782x492 at a 64px radius,
16:10, and are intentional-camera-movement frames: a meadow dragged into vertical or diagonal
streaks of yellow, green and pink, with no recognisable subject at all, carrying one white interface
card floating at the centre. The four-quadrant block uses small near-square tiles, 236x261 and
273x277 and 238x228, at a 16px radius, each one a single simple subject legible at 240px. The
careers portrait is 283x373 at 16px with `object-position: 50% 0%`. The closing frame is 1376x724 at
a 64px radius, inset 32px from both page edges, with the brand mark in white over its centre.

Everything is `object-fit: cover`. Nothing has a border. Nothing has a shadow. Nothing has a
gradient laid over it. Where an image meets the ground it meets it on a hard edge, rounded at the
corners, and that is the whole transition.

**Iconography.** Stroke only, never filled. 18px, 20px and 24px viewBoxes, stroke-width 1.25 to 1.5,
round line caps, drawn in `currentColor` so they invert white over the hero and near-black over the
ground. In running copy they sit bare, with no disc and no square behind them. The only boxed icon
is inside a data card: a 36x36 tile at an 8px radius filled near-black `#1A1613`, carrying a small
mark in their accent green `#99D538`.

**Illustration.** All synthetic, all flat vector, no chrome and no device frames. The data cards are
340px wide at a 12px radius on a bone fill `#F3F0E9`, with mono digits for money and identifiers,
small green ticks for state, and one row per fact. The three "how it works" tiles are 441x441
squares of pure drawn interface on a bone tile, not photographs at all. The map is a dotted-grid
United States with weighted dots.

Note that last point: on the reference the "how it works" step tiles are drawn, not shot. We are
using photographs there instead, which is a deliberate departure. If the drawn route is preferred
later, the three prompts below are simply unused.

## Rules for every image

1. **No faces, no props, no brands.** Human presence is a forearm, a wrist, a shoulder, a back, a
   hand. Never a face, never eye contact, never a person posed for camera. Clinical presence is
   carried by material (stainless, glass, a plain white cuff, cut stone), never by a stethoscope, a
   lab coat, scrubs, a hospital bed, a scanner, a test tube or a smiling doctor. No legible text, no
   logos, no watch dials, no screens.
2. **One light, one hour.** Every image in the set is the same morning: cold blue-grey before the
   sun, warming to a low, raking gold. Never midday, never overhead, never a lamp, never night. That
   single decision is what makes seven unrelated frames look like one commission.
3. **Mostly empty, one plane sharp.** Wide aperture, one subject in focus and the rest of the frame
   falling away. At least half of every frame is quiet, because a card, a headline or a mark is
   going to sit on it.

**On edges, and this is not negotiable.** Do not write "fades into white", "dissolves", "soft
gradient", "mist" or "haze" into a prompt. Generators turn all five into fog, and it has been
rejected twice. Where an image meets the page ground it stops on a hard edge, rounded at the corners
by CSS. If an edge in a delivered render does not sit right against the ground, fix it in the image
file, the way the v1.1 footer render was fixed (see `docs/v1-1-art-brief.md`). Never put a CSS fade,
scrim or blur over an image to hide a bad edge.

Because every edge is hard, the page ground colour never has to appear inside a render. The ground
for v3 is the orchestrator's to set; nothing in this brief depends on it.

## The slots

Seven images. All land in `public/images/v3/`, as WebP, named by their id.

Generate at the largest size the tool offers (ChatGPT returns 1536x1024 for a 3:2 landscape request,
1024x1024 for a square) and always ask for the frame shape explicitly, or you will get a square back
regardless. Then crop to the ratio below and downscale to the target. Convert with
`cwebp -q 82 in.png -o out.webp`.

---

### 1. `hero-cover` — the first thing seen

`public/images/v3/hero-cover.webp` · **2880x1620, 16:9**

Full-bleed, full-viewport, `object-fit: cover`, no radius. On a 1440x900 desktop that crops to
roughly the middle 16:10 of the frame, and on a phone it crops hard to a centre column, so the
subject must survive both: nothing that matters may sit in the outer sixth on either side.

Keep clear: the centre of the frame carries the headline in white serif, the nav pill sits top
centre, and the email field sits bottom centre. The middle band has to be quiet and mid-dark on its
own, dark enough that white type reads without a scrim laid over it. That darkness is asked for in
the prompt and must be in the render, not added in CSS.

> Photograph, cinematic wide shot, shot through a pane of old hand-rolled glass so the whole frame is
> optically softened and slightly distorted. A still consulting room in a converted stone house at
> first light: a pale stone floor, a linen curtain moving slightly, one steel-framed window, an olive
> tree outside well out of focus behind the glass. A single person seen at a distance and far out of
> focus at the left edge, walking away from camera, only a shoulder and a back, no face. Cold
> blue-grey morning light from the right, low and raking, long quiet shadows, no direct sunbeam.
> Restrained palette: deep forest green, slate grey, wet stone, bone white, one thread of low gold.
> The middle of the frame is calm and mid-dark, uncluttered, nothing bright in the centre. Shot on
> medium format, 80mm, wide aperture, shallow depth of field, fine natural film grain. 16:9 landscape
> frame. No faces, no eye contact, no medical props, no stethoscope, no lab coat, no scrubs, no
> hospital equipment, no furniture logos, no text, no watermark, no lens flare, no fog, no mist, no
> vignette.

---

### 2, 3, 4. `step-01`, `step-02`, `step-03` — the "how it works" thumbnails

`public/images/v3/step-01.webp` (and `-02`, `-03`) · **1200x1200, 1:1**

Square tiles at roughly 440px on a 1440 desktop, `object-fit: cover`, 24px radius. Squares crop
safely to 4:3 or 16:10 if the layout changes, which is why they are square. Ids are deliberately
numeric, not named after the copy, so a copy change never orphans a file.

Keep clear: nothing overlays these, but the step number and the step title sit directly beneath, so
the bottom edge should be the quiet part of the frame.

They are one human triptych, three fragments of the same morning, and they read in order: the
assessment, the tracking, the protocol.

> **step-01.** Photograph, close and intimate. A bare forearm resting on unbleached linen laid over a
> pale limestone table, seen from above and slightly to the side. Skin sharp and warm, every other
> plane falling away. Cold blue-grey morning light raking from the left, a low warm reflection off
> the stone. Palette: bone, oat linen, warm skin, wet grey stone. Medium format, 100mm macro, wide
> aperture, very shallow depth of field, fine natural grain. Square 1:1 frame, quiet and empty along
> the bottom edge. No face, no jewellery, no watch, no medical props, no needles, no tubes, no
> gloves, no text, no logo, no watermark, no fog, no mist.

> **step-02.** Photograph, close and intimate. A wrist and the back of a hand resting on the edge of
> a bone-coloured stone worktop, a plain matte black strap on the wrist with the dial turned away
> from camera and no screen and no branding visible. Cold blue-grey morning light from the left,
> warming as it crosses the stone. Palette: bone, wet grey stone, matte black, warm skin, a single
> deep green leaf far out of focus behind. Medium format, 100mm, wide aperture, very shallow depth
> of field, fine natural grain. Square 1:1 frame, quiet and empty along the bottom edge. No face, no
> screen, no dial, no numbers, no logo, no medical props, no text, no watermark, no fog, no mist.

> **step-03.** Photograph, close and intimate. Two hands over a plain cream card on a dark walnut
> desk, one hand passing it to the other, the card completely blank with no printing on it at all.
> Low warm morning light from a window off to the right, deep quiet shadow on the left of the frame.
> Palette: cream paper, dark walnut, warm skin, deep forest green far out of focus behind. Medium
> format, 85mm, wide aperture, very shallow depth of field, fine natural grain. Square 1:1 frame,
> quiet and empty along the bottom edge. No faces, no writing, no printed text, no letterhead, no
> pen, no logo, no watermark, no fog, no mist.

---

### 5, 6. `quad-photo-a`, `quad-photo-b` — inside the four-quadrant block

`public/images/v3/quad-photo-a.webp` and `quad-photo-b.webp` · **1000x1100, 10:11**

Small near-square tiles, around 240x260 on a 1440 desktop, `object-fit: cover`, 16px radius. They
sit diagonally opposite the two data cards, around a centred statement, and each is partly
overlapped by a card. Legibility at 240px is the whole constraint: one subject, one colour idea, no
detail that needs looking into. Assume the inner corner of each tile is covered by a card, so put
nothing important there.

One is ground truth, one is rooms and hands, so the block carries both families at once.

> **quad-photo-a.** Photograph, very close. Dew on clipped lawn grass at dawn, shot almost at ground
> level, a few blades sharp in the near foreground and the rest of the frame falling into soft deep
> green. Cold blue-grey light before sunrise, single water droplets catching a tiny cold highlight.
> Palette: deep forest green, blue-grey, silver. Macro, wide aperture, very shallow depth of field,
> fine natural grain. Portrait 10:11 frame. One simple subject, readable as a small thumbnail. No
> flowers, no insects, no people, no text, no watermark, no fog, no mist.

> **quad-photo-b.** Photograph. A hand resting beside a closed notebook on a pale stone desk in a
> quiet private office at first light, seen from above and to the side, the hand sharp and the room
> behind well out of focus. Low warm light from a tall window on the right. Palette: bone, pale
> stone, warm skin, one dark green plant far out of focus. Medium format, 85mm, wide aperture, very
> shallow depth of field, fine natural grain. Portrait 10:11 frame. One simple subject, readable as
> a small thumbnail. No face, no screen, no laptop, no phone, no printed text, no logo, no watermark,
> no fog, no mist.

---

### 7. `closing-frame` — the note the page ends on

`public/images/v3/closing-frame.webp` · **2752x1448, 1.9:1**

The full-width card at the foot of the page: inset 32px from both page edges, 64px radius,
`object-fit: cover`. The brand mark sits over it in white, centred. Its top edge is a hard rounded
edge against the ground, and the footer block overlays its upper portion, so the top eighth of the
frame is never fully seen. Its bottom runs off the page.

Keep clear: the centre, for the white mark. Mid-toned and uncluttered there, with no bright highlight
behind where the mark lands.

This is the one frame allowed to be generous with colour. It is the equivalent of Lassie's poppies
against blue sky, and it is what the reader leaves with.

> Photograph, cinematic wide shot from inside an olive grove at sunrise, camera low and close among
> the trees looking along the rows. The nearest silver-green leaves are large and well out of focus
> across the left and right of the frame, one branch sharp in the middle distance, pale sky visible
> through the canopy above. Low gold sun raking from behind the trees on the right, long shadows
> across dry pale earth. Palette: silver-green, deep forest green, warm bone, dry pale earth, low
> gold. The centre of the frame is calm and mid-toned with no bright highlight in it. Shot on medium
> format, 50mm, wide aperture, shallow depth of field, fine natural film grain. Wide 1.9:1 landscape
> frame. No people, no buildings, no animals, no farm machinery, no fences, no text, no watermark,
> no lens flare, no fog, no mist, no vignette.

---

### Optional: `panel-drift-a`, `-b`, `-c` — motion behind the interface cards

`public/images/v3/panel-drift-a.webp` (and `-b`, `-c`) · **2400x1500, 16:10**

Only needed if v3 adopts the reference's wide feature panels: 782x492 at a 64px radius, one white
interface card floating at the centre of each. On the reference these are the most distinctive images
on the site, and they are the cheapest to reproduce well, because there is no subject to get wrong.
Listed here so the slot exists if the layout wants it.

Keep clear: everything. A card covers the middle 55% of the frame, and the image only has to be
beautiful at its edges.

> Photograph made with intentional camera movement, a long exposure dragged in a straight line so the
> subject is pulled into continuous vertical streaks and nothing is recognisable. The subject is an
> olive grove at dawn, streaked into bands of silver-green, deep forest green, bone and low gold.
> Painterly, continuous, no hard shapes, no discernible objects, even across the whole frame. Fine
> natural film grain. 16:10 landscape frame. No people, no flowers, no text, no watermark, no fog,
> no mist, no vignette.

For `-b` and `-c`, run the same prompt with the movement diagonal instead of vertical, and shift the
subject: `-b` is wet clipped grass at dawn (deep green, blue-grey, silver), `-c` is still water under
a pale sky (slate, bone, one thread of gold). Three frames, one hour, three colour weights.

## How to drop them in

1. Save each as WebP into `public/images/v3/`, named exactly by its id. Convert whatever the
   generator returns with `cwebp -q 82 <in>.png -o <id>.webp`, after cropping to the ratio above.
2. In `src/pages/v3/index.astro`, set the constants at the top of the file. Each is `string | null`,
   and a `null` slot renders as its styled placeholder, so images can go in one at a time:

```ts
const HERO_ART: string | null = '/images/v3/hero-cover.webp';
const QUAD_ART: (string | null)[] = [
  '/images/v3/quad-photo-a.webp',
  '/images/v3/quad-photo-b.webp',
];
const CLOSING_ART: string | null = '/images/v3/closing-frame.webp';
```

Those three constants are already in the page, all set to `null`. There is no `STEP_ART`: the
three process steps are drawn interface panels, not photographs, so slots 2, 3 and 4 below are
unused as the page stands. Their prompts are kept in case that decision is reversed.

3. `npm run build`, and check the page at three widths: 1440, 900 and 390. Every slot is
   `object-fit: cover`, so the only thing that can go wrong is the crop moving the subject out of
   frame on a narrow viewport. Fix that by changing `object-position` on that one slot, or by
   recropping the file. Do not fix it by changing the layout.
4. If a delivered render is close but the subject lands on the wrong side, mirror it in CSS
   (`transform: scaleX(-1)`), the way the v1.1 hero is mirrored. That is cheaper than a regeneration
   and nothing in these frames reads as handed.

Every image meets the page ground on a hard rounded edge. Do not add a CSS fade, scrim, blur or
gradient overlay to any of them. If the hero comes back too bright for white type, regenerate it
darker rather than laying a scrim over it, and if an edge is wrong, fix the pixels in the file.
