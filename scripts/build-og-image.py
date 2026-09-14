#!/usr/bin/env python3
"""
Regenerates public/og-image.png and public/og-image.jpg.

The card is the home page's own hero photograph, full bleed, with the lockup
sitting on the left in one flat white. Nothing else is on it: no headline, no
URL, no copy. It is drawn as HTML at exactly 1200x630, the size SiteLayout
declares in og:image:width and og:image:height, and screenshotted.

Both source pieces are read out of the repo rather than kept as a second copy,
so the card cannot drift from the site:

  public/images/hero.webp    the photograph the hero card uses
  src/components/Logo.astro  the lockup, mark and wordmark on one viewBox

The mark is forced to white here. It holds the brand rust on the site, where it
sits on the bar, but on this photograph one flat colour reads better at the size
a feed actually shows.

Rendering needs a headless Chromium. Playwright's cached headless shell is what
this looks for, because full Chrome in headless mode hangs on this machine; set
CHROME to override the search. The page is drawn at twice the size and resampled
down, so the curves of the lockup come out clean.

    python3 scripts/build-og-image.py

Only /og-image.png is referenced, by SiteLayout and MainLayout. The .jpg is
written alongside it so the pair cannot disagree, and nothing links to it.
"""
import base64
import glob
import io
import os
import subprocess
import sys
import tempfile

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO = os.path.join(REPO, 'public/images/hero.webp')
LOGO_SRC = os.path.join(REPO, 'src/components/Logo.astro')
OUT_PNG = os.path.join(REPO, 'public/og-image.png')
OUT_JPG = os.path.join(REPO, 'public/og-image.jpg')

W, H = 1200, 630
SCALE = 2


def find_chrome():
    """Playwright's headless shell first, newest build wins."""
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    pattern = os.path.expanduser(
        '~/Library/Caches/ms-playwright/chromium_headless_shell-*/'
        'chrome-headless-shell-*/chrome-headless-shell')
    found = sorted(glob.glob(pattern))
    if found:
        return found[-1]
    sys.exit('No headless Chromium found. Install one with `npx playwright install '
             'chromium` or point CHROME at a binary.')


def build_html():
    logo_src = io.open(LOGO_SRC, encoding='utf-8').read()
    logo = logo_src[logo_src.index('<svg'):logo_src.rindex('</svg>') + 6]
    logo = logo.replace('class="logo-svg"',
                        'class="logo-svg" preserveAspectRatio="xMinYMid meet"')
    hero = 'data:image/webp;base64,' + base64.b64encode(open(HERO, 'rb').read()).decode()

    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><title>og</title><style>
  html, body { margin: 0; padding: 0; width: %(w)dpx; height: %(h)dpx; overflow: hidden; background: #18181b; }
  .frame { position: relative; width: %(w)dpx; height: %(h)dpx; overflow: hidden; }
  .photo { position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; object-position: 62%% 18%%; display: block; }
  /* The gradient the site already runs over the hero, .hero-media::after,
     carried at a little more weight so the lockup holds on a small card. */
  .scrim { position: absolute; inset: 0;
    background: linear-gradient(90deg, rgba(0,0,0,.46) 0%%, rgba(0,0,0,.16) 38%%, rgba(0,0,0,0) 60%%); }
  .lock { position: absolute; left: 84px; top: 50%%; transform: translateY(-50%%);
    height: 62px; color: #fff; --logo-icon: #fff; }
  .lock .logo-svg { display: block; height: 100%%; width: auto; }
</style></head>
<body><div class="frame">
  <img class="photo" src="%(hero)s" alt="" />
  <div class="scrim"></div>
  <div class="lock">%(logo)s</div>
</div></body></html>
""" % {'w': W, 'h': H, 'hero': hero, 'logo': logo}


def main():
    chrome = find_chrome()
    tmp = tempfile.mkdtemp(prefix='og-image-')
    page = os.path.join(tmp, 'og.html')
    shot = os.path.join(tmp, 'og.png')
    io.open(page, 'w', encoding='utf-8').write(build_html())

    subprocess.run([
        chrome, '--headless', '--disable-gpu', '--hide-scrollbars',
        '--force-device-scale-factor=%d' % SCALE,
        '--window-size=%d,%d' % (W, H),
        '--screenshot=' + shot,
        'file://' + page,
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    img = Image.open(shot).convert('RGB')
    if img.size != (W * SCALE, H * SCALE):
        sys.exit('Rendered %dx%d, expected %dx%d.' % (img.size + (W * SCALE, H * SCALE)))
    img = img.resize((W, H), Image.LANCZOS)

    img.save(OUT_PNG, 'PNG', optimize=True)
    img.save(OUT_JPG, 'JPEG', quality=88, optimize=True, progressive=True)
    for p in (OUT_PNG, OUT_JPG):
        print('%s  %dx%d  %d bytes' % (os.path.relpath(p, REPO), W, H, os.path.getsize(p)))


if __name__ == '__main__':
    main()
