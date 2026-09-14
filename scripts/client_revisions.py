#!/usr/bin/env python3
"""
Client revisions, applied on top of a drop by scripts/port-drop.py.

The client reviews the ported site and sends changes. They are applied here
rather than edited into the generated files, which the next drop overwrites, and
rather than edited into the drop itself, which has to stay a faithful record of
what was delivered.

Every revision asserts its target. If a later drop changes the wording
underneath one, the port stops and names it rather than silently skipping it.
When a drop finally arrives with a change already applied, delete that entry;
the failing assertion is what tells you it is time.

--- Round of 14 September 2026 -------------------------------------------------

Mostly claim substantiation rather than design: a superiority claim, an efficacy
figure, a menu of regulated therapies, and a reach number that overstated what
happened. The wording is the client's and is exact.

Two judgement calls, both flagged back to the client:

  * The Healthspan stat was offered as "cut the stat, or cut the whole strip".
    The strip is kept, because the same round rewrites the 400 figure inside it,
    which would be pointless if the strip were going.

  * The biological-age figure was offered as "neutralise, or label the dashboard
    illustrative". It is neutralised. The figure is aria-hidden decoration, so a
    disclaimer inside it would never be read out, which makes it the weaker of
    the two options rather than the safer one.

One item in this round contradicts the live privacy policy and is NOT applied
here: see UNAPPLIED at the foot of this file.
"""

import re
import sys

APPLIED = []


def revise(text, old, new, label, expect=1):
    """Replace `old` with `new`, asserting it appears exactly `expect` times.

    Matching is whitespace-tolerant: every run of whitespace in `old` matches any
    run in the text. The drop and the ported page carry the same markup at
    different indentation (the port re-indents), and a client reflowing a
    paragraph should not silently drop a revision either. The replacement is
    re-indented to sit at the indentation of whatever it replaced.
    """
    pattern = r'\s+'.join(re.escape(tok) for tok in old.split())
    matches = list(re.finditer(pattern, text))
    if len(matches) != expect:
        sys.exit(
            f'client revision "{label}": expected {expect} occurrence(s) of\n'
            f'  {" ".join(old.split())[:140]!r}\n'
            f'but found {len(matches)}. The drop has changed underneath this revision.\n'
            f'Re-read scripts/client_revisions.py against the new wording before porting.')

    out, last = [], 0
    for m in matches:
        line_start = text.rfind('\n', 0, m.start()) + 1
        indent = text[line_start:m.start()]
        body = new
        if new and not indent.strip() and '\n' in new:
            lines = new.split('\n')
            body = lines[0] + ''.join('\n' + indent + l.lstrip() for l in lines[1:])
        out.append(text[last:m.start()])
        out.append(body)
        last = m.end()
    out.append(text[last:])

    APPLIED.append(label)
    return ''.join(out)


def apply_to_page(content):
    """The home page's own markup."""

    # The reach figure. "reached 400 clients" overstated it: the session was
    # delivered to one advisory team, and 400 is the size of that team's book.
    # The hero marquee lists the strip twice, so this one lands twice.
    content = revise(
        content,
        '<span class="cred-text">UHNW clients in the advisory book we delivered our first session to</span>',
        '<span class="cred-text">UHNW households covered by the advisory team we delivered to</span>',
        'hero stat: 400 reach figure', expect=2)

    content = revise(
        content,
        '<div class="case-stat-label">UHNW clients in the advisory team\'s book, reached through a single educational session.</div>',
        '<div class="case-stat-label">UHNW households covered by the advisory team we delivered a single educational session to.</div>',
        'partners stat: 400 reach figure')

    # "First of its kind": a superiority claim, unsubstantiated. The whole cell
    # goes; the two that remain still carry the engagement.
    content = revise(
        content,
        '            <div class="case-stat">\n'
        '              <div class="case-num"><em>First</em></div>\n'
        '              <div class="case-stat-label">Educational session of its kind delivered with a private bank advisory team.</div>\n'
        '          </div>\n',
        '',
        'partners stat: "First of its kind" removed')

    # The Healthspan score stat, and its divider, in both copies of the strip.
    for label, hidden in (('hero stat: Healthspan score removed', ''),
                          ('hero stat: Healthspan score removed (marquee copy)', ' aria-hidden="true"')):
        content = revise(
            content,
            '          <div class="cred-divider" aria-hidden="true"></div>\n'
            f'          <div class="cred-item"{hidden}>\n'
            '            <span class="cred-num">1</span>\n'
            '            <span class="cred-text">Healthspan score, owned by the client</span>\n'
            '          </div>\n',
            '',
            label)

    # The therapy menu. Naming hormones, peptides, regenerative therapies and
    # NAD IV as a list of options is the part that reads as a menu. The two
    # conditions under it stay, and so does the discipline's own sentence.
    content = revise(
        content,
        '                    <div class="gate-chips">\n'
        '                      <span class="gate-chip">Hormones</span>\n'
        '                      <span class="gate-chip">Peptides</span>\n'
        '                      <span class="gate-chip">Regenerative therapies</span>\n'
        '                      <span class="gate-chip">NAD</span>\n'
        '                      <span class="gate-chip">IV</span>\n'
        '                      <span class="gate-chip">CGM</span>\n'
        '                    </div>\n',
        '',
        'therapy menu removed from the disciplines panel')

    # The efficacy figure, neutralised.
    content = revise(
        content,
        '<span class="fm-title">Biological age</span><span class="fm-muted">2.5 years younger</span>',
        '<span class="fm-title">Biological age</span><span class="fm-muted">Tracked each panel</span>',
        'dashboard: biological-age claim neutralised')

    # Hero standfirst.
    content = revise(
        content,
        '            A private longevity membership, introduced through the people who already advise you, your\n'
        '            firm or your organization. Delivered by clinical partners chosen against one standard. Your\n'
        '            data stays yours.',
        '            A private longevity membership, through partner you trust. Clinical partners selected on\n'
        '            three things: published outcomes, clinical governance, and your ownership of your own\n'
        '            data.',
        'hero standfirst')

    # Section 2, the process.
    content = revise(
        content,
        '<h2 class="s-title">A new model for<br />human performance</h2>',
        '<h2 class="s-title">One record. The best clinicians<br />for what it says.</h2>',
        'section 2 headline')

    content = revise(
        content,
        '              We built the infrastructure that connects the people who advise you to world-class\n'
        '              preventive care.',
        '              We built the layer that sits between the people who advise you and the clinicians\n'
        '              worth sending you to.',
        'section 2 standfirst')

    # Section 3, what you get.
    content = revise(
        content,
        '<h2 class="s-title">Everything your health<br />has been missing</h2>',
        '<h2 class="s-title">The parts that usually do not<br />talk to each other.</h2>',
        'section 3 headline')

    content = revise(
        content,
        '              Compound Health is not a gym membership or a supplement subscription. It is a medical\n'
        '              relationship, sustained and personalized.',
        '              A medical relationship that is continuous, physician-led, and calibrated to your own\n'
        '              data. Your clinicians see the same record you do, every time.',
        'section 3 standfirst')

    # How we choose: the three tests, with the annual re-review folded up out of
    # the footnote and into the opener, where the client wanted it.
    content = revise(
        content,
        '              Longevity medicine is not one company. We assessed the field, set one standard, and\n'
        '              chose the partners who meet it.',
        '              Longevity medicine is not one company. We assessed the field against three tests:\n'
        '              published outcomes, clinical governance, and whether the patient owns the record.\n'
        '              The partners here meet all three. Every partner is re-reviewed each year, and if a\n'
        '              better option emerges the membership moves with it.',
        'how we choose: opener, with the annual re-review folded in')

    content = revise(
        content,
        '        <p class="curated-note reveal">\n'
        '          Every partner is re-reviewed each year.<br />If a better option emerges, the membership moves with it.\n'
        '        </p>\n',
        '',
        'how we choose: footnote removed, now in the opener')

    content = _move_partner_notes_up(content)
    return content


def _move_partner_notes_up(content):
    """Put "Nothing crosses the line" at the top of the Partners section.

    The three notes are one composed block on a dark panel, a three-column grid
    with its own background: lifting one note out of it leaves a one-item grid
    above and a two-item grid below, and both read as broken. So the block moves
    up whole, above the stats, and "Nothing crosses the line" is reordered to
    lead it. That puts the statement where the client asked for it without
    dismantling the composition.
    """
    m = re.search(r'[ \t]*<div class="partner-notes[^"]*">', content)
    if not m:
        sys.exit('client revision "partner notes": the .partner-notes block was not found')
    start = content.rfind('\n', 0, m.start()) + 1

    depth, end = 0, None
    for t in re.finditer(r'<(/?)div\b[^>]*?(/?)>', content[m.start():]):
        if t.group(2) == '/':
            continue
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    if end is None:
        sys.exit('client revision "partner notes": the block is never closed')
    end = content.find('\n', end) + 1
    block = content[start:end]

    pieces = re.split(r'(?=[ \t]*<div class="partner-note">)', block)
    notes = [p for p in pieces if '<div class="partner-note">' in p]
    if len(notes) != 3:
        sys.exit(f'client revision "partner notes": expected 3 notes, found {len(notes)}')
    lead = [n for n in notes if 'Nothing crosses the line' in n]
    if len(lead) != 1:
        sys.exit('client revision "partner notes": "Nothing crosses the line" not found exactly once')
    rest = [n for n in notes if n is not lead[0]]
    head = pieces[0]
    tail = ''
    # The closing </div> of the wrapper rides on the last note; keep it there.
    reordered = head + ''.join(lead + rest) + tail

    content = content[:start] + content[end:]
    at = content.find('<!-- Proof block: the first partner engagement')
    if at < 0:
        sys.exit('client revision "partner notes": the proof block comment was not found')
    at = content.rfind('\n', 0, at) + 1
    APPLIED.append('partners: notes moved above the stats, "Nothing crosses the line" first')
    return content[:at] + reordered + '\n' + content[at:]


def apply_to_footer(footer):
    """The footer, which SiteLayout renders from components/Footer.astro."""

    # The Sitemap link. Added on 14 September and removed the same day at the
    # client's request: it pointed at the XML itself, which is what a crawler
    # reads out of robots.txt and not something a visitor has any use for.
    footer = revise(
        footer,
        '\n          <a href="/sitemap.xml">Sitemap</a>',
        '',
        'footer: Sitemap link removed')

    # For advisors. /for-advisors redirects to the home page, so the link went
    # back to the page the reader was already on. The bar's copy of it went
    # earlier the same day.
    footer = revise(
        footer,
        '          <a href="/for-advisors">For advisors and firms</a>\n',
        '',
        'footer: For advisors link removed, that route redirects to /')

    return footer


def apply_to_css(css):
    """Stylesheet consequences of the revisions above.

    Appended rather than edited in place, so the drop's own stylesheet stays
    verbatim above it and every revision-driven rule is visible in one block.
    Appended last, so it wins on order alone and needs no extra specificity.
    """
    APPLIED.append('stylesheet: case-stats to two columns, therapies panel re-centred')
    return css + """

/* ══════════════════════════════════════════════════════════════════════
   CLIENT REVISIONS, 14 September 2026
   Appended by scripts/client_revisions.py. Consequences of the markup
   changes in that file, not design decisions of their own. Do not edit by
   hand: edit the script and re-port.
   ══════════════════════════════════════════════════════════════════════ */

/* The partners proof block lost its "First of its kind" cell, so the three
   columns are two. Without this the row keeps an empty third column and the
   two figures sit in the left two-thirds of the card. The 900px stack is
   restated because it is declared earlier in the file than this block. */
.case-band .case-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
@media (max-width: 900px) {
  .case-band .case-stats { grid-template-columns: 1fr; }
}

/* The therapies panel lost its chip strip, and .gate-flow was pinned to the
   foot of a stretching column by margin-top: auto. With nothing above it that
   left roughly 200px of empty gradient between the card's head and its two
   conditions. The conditions now sit in the middle of the space instead. */
.gate { justify-content: center; }
.gate-flow { margin-top: 0; }
"""

# ── UNAPPLIED ────────────────────────────────────────────────────────────────
#
# "New block, after the biomarker feature: One record, held in your name. Every
# panel, scan and wearable stream lands in a single clinical record. Grant a new
# physician access in an afternoon, and take it with you if you leave. We do not
# sell it, license it, or share it with your advisor, your employer or an
# insurer."
#
# Not applied. The last sentence contradicts the live privacy policy, which says
# under Sharing and disclosure:
#
#   "Wealth advisors: With your explicit consent, relevant health summary data
#    may be shared with your advisory firm to support integrated financial and
#    health planning"
#
# and permits transfer of personal data on a merger or acquisition under
# "Business transfers", which sits badly with an unqualified "we do not license
# it". A home page that promises what its own policy contradicts is a worse
# outcome than no block at all, and in the US an unsubstantiated data-handling
# promise is an FTC deception exposure rather than a copy question.
#
# Resolve one of two ways, then add the block here:
#   * amend the privacy policy so the promise is true, or
#   * soften the sentence to what the policy actually allows, for example
#     "never shared with your employer or an insurer, and with your advisory
#     firm only on your explicit instruction".
