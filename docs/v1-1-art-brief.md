# v1.1 artwork brief

The client's feedback on v1 was that it did not feel premium, and asked for a blend of the current
site with [bayshore.ai](https://www.bayshore.ai/): their colours, their gradient backgrounds, and
the tree and landscape redrawn in their style (3D, realistic, marble).

The palette and the gradients are done in `src/styles/variants/v1-1.css`. The renders have to be
generated outside the repo, and a slot with no render runs as a gradient environment, which is what
it is painted for.

**Status, 2026-09-07.** The hero render is in: `public/images/v1-1/hero-monolith.webp`, from the
first prompt below, generated at 1536x1024. It is mirrored in CSS because it puts the tree left of
centre and the copy needs that side, and its bottom edge meets the page ground on a hard edge
rather than resolving to bone, which is Bayshore's own move and needs no fade. The footer render is
still to do; prompt two below.

## What to generate

Two images, one world, same light, same palette. Both are backdrops: no text, no logos, nothing
important in the centre where copy sits.

### 1. Hero, `hero-monolith.webp`, 2400x1600

A single sculptural tree carved from veined marble, standing in a still, near-empty landscape of
pale stone and drifted sand. Photoreal 3D render, cinematic, physically-based materials: the marble
is warm white with grey and ochre veining and a soft polished sheen; the ground is fine pale sand
with long shadows. Low sun behind and to the left, raking light, deep soft shadows, faint haze on
the horizon.

The sky is a dusk gradient: deep desert blue `#2A4E82` at the top, cooling through grey-blue
`#6E7A93` at the middle, into warm sand `#EACBA6` near the horizon. The tree occupies the lower
third and sits left or right of centre, never dead centre. The upper half of the frame is quiet
sky, because the headline sits there.

The prompt asks for the bottom edge to resolve to bone as well, and the render that landed does
not: it ends on sand in shadow. That turned out not to matter, because v1.1 meets the page ground
on a hard edge rather than a dissolve. Keep the line in the prompt, but do not reject a render
over it.

Wide, calm, expensive. No people, no buildings, no wildlife, no lens flare, no text.

### 2. Footer, `footer-stone.webp`, 2048x1360

The same world at the same hour, seen wide and low: a horizon of pale marble outcrops and sand,
the tree small and distant or absent. The top half of the frame is near-empty sky in pale sand and
bone tones (`#EDE6DC` to `#E4D3BE`), light enough for small dark text to sit on it. The landscape
occupies the bottom half only. Same materials, same raking light, same haze.

## Prompt to paste

> Photoreal 3D render, cinematic wide shot. A single sculptural tree carved from veined warm-white
> marble, grey and ochre veining, softly polished, standing in a still empty landscape of pale
> stone outcrops and fine drifted sand. Low raking sun from behind left, long soft shadows, faint
> atmospheric haze on the horizon. Dusk gradient sky: deep desert blue at the top, grey-blue
> through the middle, warm sand near the horizon, fading to bone white at the very bottom edge of
> the frame. The tree sits in the lower third, off centre; the upper half is quiet, empty sky.
> Muted, expensive, restrained palette: deep blue #2A4E82, grey-blue #6E7A93, sand #EACBA6, bone
> #F2EFEB. Physically-based materials, high detail, 8k, no people, no buildings, no animals, no
> lens flare, no text, no watermark.

And for the footer:

> Photoreal 3D render, cinematic wide shot, low horizon. A still empty landscape of pale veined
> marble outcrops and fine drifted sand, seen wide, with a single sculptural marble tree small and
> distant on the horizon. Low raking sun from behind left, long soft shadows, faint atmospheric
> haze. The top half of the frame is near-empty sky in pale sand and bone tones, light and almost
> white, with nothing in it; the landscape occupies only the bottom half. Muted, expensive,
> restrained palette: bone #F2EFEB, pale sand #EDE6DC, sand #E4D3BE, warm marble white.
> Physically-based materials, high detail, 8k, no people, no buildings, no animals, no lens flare,
> no text, no watermark.

Ask for a 3:2 landscape frame in both cases, or the generator will hand back a square. Whatever it
returns as PNG, convert to WebP before it goes into `public/`.

## Dropping them in

1. Save both as WebP into `public/images/v1-1/`.
2. In `src/pages/v1-1/index.astro`, set the two constants at the top:

```ts
const HERO_ART: string | null = '/images/v1-1/hero-monolith.webp';
const FOOTER_ART: string | null = '/images/v1-1/footer-stone.webp';
```

3. `npm run build`. The hero gradient stays behind the render as its backdrop, and the footer
   switches from the sand gradient to the photograph.

If the ratio is not 3:2, update the `width` and `height` on the `<img>` in the same file (hero) and
in `src/components/variants/Footer.astro` (footer), so the browser reserves the right space.

In v1.1 the artwork meets the page ground on a hard horizontal edge, the way Bayshore's own image
blocks do. Do not add a CSS fade, scrim or blur to soften it. (The Duna rule that the transition
into white must live inside the artwork belongs to v1, whose hero dissolves into the page.)

What does need checking in a render is the copy side: the hero copy sits high and left over the
sky, so keep that region quiet, and expect to mirror the image in CSS if the subject lands on the
wrong side.
