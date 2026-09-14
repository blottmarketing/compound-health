#!/usr/bin/env python3
"""
Generate public/llms-full.txt from the built HTML.

Run it after `npm run build`, and re-run it after every client drop: the page
copy changes with the drop, and a stale llms-full.txt is worse than none.

    npm run build && python3 scripts/build-llms-full.py

public/llms.txt is the short index and is hand-written, not generated: it says
what the company is and what the pages are, which no extractor can infer. Edit
that one by hand.
"""

import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    ('Home', 'https://compoundhealth.io/', 'dist/index.html'),
    ('Privacy Policy', 'https://compoundhealth.io/privacy-policy', 'dist/privacy-policy/index.html'),
    ('Website Terms', 'https://compoundhealth.io/website-terms', 'dist/website-terms/index.html'),
]


def strip_subtrees(s, opener):
    """Remove every element whose opening tag matches `opener`, and its children."""
    out, i = [], 0
    for m in re.finditer(opener, s):
        if m.start() < i:
            continue
        tag = re.match(r'<([a-zA-Z0-9]+)', m.group(0)).group(1)
        depth, end = 0, None
        for t in re.finditer(rf'<(/?){tag}\b[^>]*?(/?)>', s[m.start():]):
            if t.group(2) == '/':
                continue
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end()
                break
        if end is None:
            continue
        out.append(s[i:m.start()])
        i = end
    out.append(s[i:])
    return ''.join(out)


def text_of(path):
    s = open(path, encoding='utf-8').read()
    body = s[s.index('<body'):s.rindex('</body>')]
    body = strip_subtrees(body, r'<(?:script|style|svg)\b[^>]*>')
    # The chrome repeats on every page and says nothing about the page itself.
    body = strip_subtrees(body, r'<nav class="main-nav"[^>]*>')
    body = strip_subtrees(body, r'<footer class="site-footer"[^>]*>')
    body = strip_subtrees(body, r'<div class="mobile-menu"[^>]*>')
    # Decorative figures. The drop marks every one aria-hidden, and their labels
    # are lifted verbatim from copy that appears elsewhere on the page anyway.
    body = strip_subtrees(body, r'<[a-zA-Z0-9]+[^>]*\baria-hidden="true"[^>]*>')

    out = []
    for m in re.finditer(r'<(h1|h2|h3|p|li)\b[^>]*>(.*?)</\1>', body, re.S):
        tag, inner = m.group(1), m.group(2)
        # A <br> is a line break in a heading, and adjacent inline elements are
        # separate words. Both become spaces, or the words run together.
        inner = re.sub(r'<br\s*/?>', ' ', inner)
        inner = re.sub(r'</(span|em|strong|b|i|a|div)>', r'</\1> ', inner)
        t = html.unescape(re.sub(r'<[^>]+>', '', inner))
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) < 3:
            continue
        prefix = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'li': '- '}.get(tag, '')
        line = prefix + t
        if line not in out[-3:]:
            out.append(line)
    return out


def main():
    parts = ['# Compound Health', '',
             '> The readable copy of every page on compoundhealth.io, generated from the '
             'built HTML. Navigation, forms and decorative figures are omitted.', '']
    for name, url, rel in PAGES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            sys.exit(f'{rel} is missing. Run `npm run build` first.')
        parts += [f'## {name}', '', f'Source: {url}', ''] + text_of(path) + ['']

    out = os.path.join(ROOT, 'public', 'llms-full.txt')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(parts) + '\n')
    print(f'wrote public/llms-full.txt  ({os.path.getsize(out):,} bytes)')


if __name__ == '__main__':
    main()
