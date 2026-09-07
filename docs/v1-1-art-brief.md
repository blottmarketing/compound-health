# v1.1 artwork brief

The client's feedback on v1 was that it did not feel premium, and asked for a blend of the current
site with [bayshore.ai](https://www.bayshore.ai/): their colours, their gradient backgrounds, and
the tree and landscape redrawn in their style (3D, realistic, marble).

The palette and the gradients are done in `src/styles/variants/v1-1.css`. The two renders are not,
because they have to be generated outside the repo. Until they exist, both slots run as gradient
environments, which is what they are painted for. This file is the brief for generating them.

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
`#6E7A93` at the middle, into warm sand `#EACBA6` near the horizon, and the very bottom edge of
the frame resolves to bone `#F2EFEB` so the image joins the page ground with no seam. The tree
occupies the lower third and sits left or right of centre, never dead centre. The upper half of
the frame is quiet sky, because the headline sits there.

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

For the footer, swap the last part of the first sentence for a low wide horizon with the tree
distant or absent, and ask for the top half of the frame to be near-empty pale sand sky.

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

The transition into the page ground lives in the artwork, never in a CSS fade, scrim or blur. If
the bottom edge of the hero render is not bone, it will show a seam, and the fix is to regenerate
the image rather than to gradient over it.
