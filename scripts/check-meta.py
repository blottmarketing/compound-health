#!/usr/bin/env python3
"""
Check the built pages' head metadata against the launch checklist.

    npm run build && python3 scripts/check-meta.py

Reports title and description length against the ~60 and ~160 guidelines, plus
duplicates, missing fields, and images with no alt attribute. Exits non-zero if
anything fails, so it can go in CI later.

These are guidelines, not hard rules: a search engine truncates rather than
penalises. The point of the check is that a new drop cannot quietly reintroduce
a 200-character description without anyone noticing.

An image with alt="" is not a failure. It is the correct treatment for a
decorative photograph, and every photograph on this site sits inside an
aria-hidden="true" wrapper, so its whole subtree is out of the accessibility
tree regardless. Only a missing alt attribute is reported.
"""

import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

TITLE_MAX = 60
DESC_MAX = 160
DESC_MIN = 50


def pages():
    """Every built page except the redirect stubs.

    A route in astro.config.mjs's `redirects` is emitted as a meta-refresh
    document with a canonical at the target and nothing else. It has no
    description and no title of its own by design, so checking one reports a
    fault that is not there.
    """
    for dirpath, _dirs, files in os.walk(DIST):
        for name in files:
            if not name.endswith('.html'):
                continue
            full = os.path.join(dirpath, name)
            head = open(full, encoding='utf-8').read(400)
            if 'http-equiv="refresh"' in head:
                continue
            yield '/' + os.path.relpath(full, DIST), full


def main():
    seen = defaultdict(list)
    problems = []
    rows = []

    for route, path in sorted(pages()):
        s = open(path, encoding='utf-8').read()
        t = re.search(r'<title>(.*?)</title>', s, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        title = t.group(1).strip() if t else ''
        desc = d.group(1).strip() if d else ''

        if not title:
            problems.append(f'{route}: no <title>')
        if not desc:
            problems.append(f'{route}: no meta description')
        if len(title) > TITLE_MAX:
            problems.append(f'{route}: title is {len(title)}, over {TITLE_MAX}')
        if desc and len(desc) > DESC_MAX:
            problems.append(f'{route}: description is {len(desc)}, over {DESC_MAX}')
        if desc and len(desc) < DESC_MIN:
            problems.append(f'{route}: description is only {len(desc)}, under {DESC_MIN}')

        seen[title].append(route)
        seen[desc].append(route)

        imgs = re.findall(r'<img\b[^>]*>', s)
        no_alt = [i for i in imgs if not re.search(r'\salt=', i)]
        for i in no_alt:
            src = re.search(r'src="([^"]*)"', i)
            problems.append(f'{route}: <img> with no alt attribute: {src.group(1) if src else i[:60]}')

        empty_alt = sum(1 for i in imgs if re.search(r'\salt=""', i))
        rows.append((route, len(title), len(desc), len(imgs), empty_alt))

    for value, routes in seen.items():
        if value and len(routes) > 1:
            problems.append(f'duplicated across {", ".join(sorted(set(routes)))}: {value[:60]!r}')

    w = max(len(r[0]) for r in rows)
    print(f'{"route".ljust(w)}  title  desc  imgs  alt=""')
    for route, tl, dl, n, ea in rows:
        flag = ' <-' if tl > TITLE_MAX or dl > DESC_MAX else ''
        print(f'{route.ljust(w)}  {tl:5d}  {dl:4d}  {n:4d}  {ea:5d}{flag}')

    print()
    if problems:
        print(f'{len(problems)} problem(s):')
        for p in problems:
            print(f'  - {p}')
        return 1
    print(f'all clear: titles <= {TITLE_MAX}, descriptions {DESC_MIN}-{DESC_MAX}, '
          'every image has an alt attribute, no duplicates')
    return 0


if __name__ == '__main__':
    sys.exit(main())
