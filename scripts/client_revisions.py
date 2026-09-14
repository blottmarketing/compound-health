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

Two deliveries, and the second supersedes the first. The WhatsApp messages of
12:26 and 12:29 came first; "Compound Health website changes.pdf" arrived later
the same day with the same items reworded and eight more added. Where the two
disagree the PDF wins, and the four places they disagree are marked PDF below.

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

RECORD_BLOCK = """\
          <article class="feat-card">
            <div class="feat-visual tone-ink" aria-hidden="true">
              <div class="fm-card">
                <div class="fm-row fm-between"><span class="fm-title">Your clinical record</span><span class="fm-muted">In your name</span></div>
                <ul class="fm-list">
                  <li><span class="fm-chip is-moss">Panels</span><span>Every result, every year</span></li>
                  <li><span class="fm-chip is-moss">Scans</span><span>Imaging and reports</span></li>
                  <li><span class="fm-chip is-rust">Wearables</span><span>Continuous stream</span></li>
                </ul>
                <div class="fm-row fm-between"><span class="fm-muted">Grant a physician access</span><span class="fm-muted">This afternoon</span></div>
              </div>
            </div>
            <div class="feat-copy">
              <h3 class="feat-name">One record, held in your name</h3>
              <p class="feat-desc">Every panel, scan and wearable stream lands in a single clinical record. Grant a new physician access in an afternoon, and take it with you if you leave. We do not sell it, license it, or share it with your advisor, your employer or an insurer.</p>
            </div>
          </article>
"""


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

    # The whole "Where we are" strip. The PDF asks for the Healthspan stat to go
    # and adds a condition: "if that leaves fewer than three items, remove the
    # strip". Removing it leaves two, so the strip goes, and with it the hero's
    # copy of the 400 figure. The Partners section keeps the claim.
    content = _drop_hero_strip(content)

    # The reach figure in the Partners section, the only copy left once the hero
    # strip is gone. The PDF's sentence is "Delivered to an advisory team
    # covering 400 UHNW households"; the cell sets the number large and the line
    # beneath it, and the sibling cell does not repeat its own figure in its
    # line, so the number stays the number and the rest becomes the line.
    content = revise(
        content,
        "<div class=\"case-stat-label\">UHNW clients in the advisory team's book, reached through a single educational session.</div>",
        '<div class="case-stat-label">UHNW households in the advisory team we delivered to.</div>',
        'partners stat: 400 reach figure (PDF)')

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

    # The record block, after the biomarker feature. Applied on the user's
    # instruction of 14 September, having been held back once: its closing
    # sentence still contradicts the live privacy policy, which permits sharing
    # health summary data with the advisory firm on explicit consent and permits
    # transfer on a merger. The policy has to be amended, or the sentence
    # softened, before this is a promise the site can keep.
    #
    # It goes in as a sixth feature card rather than a band across the page:
    # the grid is two columns, five cards left an orphan row, and six do not.
    content = revise(
        content,
        '<h3 class="feat-name">Full biomarker tracking</h3>',
        '<h3 class="feat-name">Full biomarker tracking</h3>',
        'record block anchor check')
    marker = '</article>'
    at = content.find('<h3 class="feat-name">Full biomarker tracking</h3>')
    at = content.find(marker, at) + len(marker)
    at = content.find('\n', at) + 1
    content = content[:at] + RECORD_BLOCK + content[at:]
    APPLIED.append('new block: "One record, held in your name" after the biomarker feature')

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
        '            A private longevity membership, introduced through the people who already advise\n'
        '            you. Clinical partners selected on three things: published outcomes, clinical\n'
        '            governance, and ownership of your own data.',
        'hero standfirst (PDF)')

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
        '              The partners here meet all three. We re-run the review every year. If a better\n'
        '              clinician, test or platform emerges, your membership moves to it. You are never\n'
        '              locked to a provider because we are.',
        'how we choose: opener, with the annual re-review folded in (PDF)')

    content = revise(
        content,
        '        <p class="curated-note reveal">\n'
        '          Every partner is re-reviewed each year.<br />If a better option emerges, the membership moves with it.\n'
        '        </p>\n',
        '',
        'how we choose: footnote removed, now in the opener')

    # The data firewall note takes the PDF's own text, which is longer and says
    # more than the line it replaces: participation as well as engagement, and
    # the partner being out of the path of care as well as of the record.
    content = revise(
        content,
        '<p>Health data belongs to the individual. You see engagement, never medical information.</p>',
        '<p>Before anything else. Health data belongs to the individual. You see engagement and '
        'participation, never medical information. Your people join through you, and you are never '
        'in the path of their care or their record.</p>',
        'partners: data firewall note rewritten (PDF)')


    # ── "Fix this week", from the PDF ───────────────────────────────────

    # The tier name. "Eternal" reads as an immortality claim; the PDF offers
    # Executive, Private or Full Practice. Private was chosen: it sits beside
    # Baseline and Optimize and it is the site's own word for the membership.
    # Only the label changes. The option's value stays "eternal" so the Apps
    # Script behind the form, and every row already in the sheet, are untouched;
    # rename it there too if the client wants the stored value to match.
    content = revise(
        content,
        '<div class="plan-name">Eternal</div>',
        '<div class="plan-name">Private</div>',
        'membership: "Eternal" tier renamed Private (PDF)')
    content = revise(
        content,
        '<option value="eternal">Eternal</option>',
        '<option value="eternal">Private</option>',
        'form: tier option relabelled Private (PDF)')

    # The Baseline price note implies a figure the page never gives.
    content = revise(
        content,
        '            <p class="plan-price-note">Credited toward year one if you continue.</p>\n',
        '',
        'membership: "Credited toward year one" removed (PDF)')

    # The screening claim. Multi-cancer early detection appears four times, not
    # three as the brief says: once in the disciplines copy, twice in the tier
    # lists, and once inside an aria-hidden figure that repeats the discipline's
    # own words. The qualifier goes inline where the claim is introduced, and as
    # a note under the tiers, which is what the two tier mentions sit in. The
    # figure is decoration and is left alone, as with the biological-age label.
    content = revise(
        content,
        '                Baseline testing, multi-cancer early detection and imaging, chosen for accuracy and\n'
        '                usefulness.',
        '                Baseline testing, multi-cancer early detection and imaging, chosen for accuracy and\n'
        '                usefulness. Multi-cancer early detection is a laboratory-developed test and is not\n'
        '                FDA approved.',
        'disciplines: screening qualifier added (PDF)')

    content = revise(
        content,
        '<p class="family-note">Family and household coverage',
        '<p class="family-note">Multi-cancer early detection is a laboratory-developed test and is '
        'not FDA approved.</p>\n'
        '        <p class="family-note">Family and household coverage',
        'membership: screening qualifier added under the tiers (PDF)')

    # The referring advisor becomes required for clients. The page promises
    # introduced, not sold, and an optional field said the opposite. The label
    # drops "(optional)", the input carries required, and the submit handler
    # checks it in the client branch beside the tier.
    content = revise(
        content,
        '<label class="wf-label" for="wf-advisor">Referring advisor or firm (optional)</label>',
        '<label class="wf-label" for="wf-advisor">Referring advisor or firm</label>',
        'form: advisor label no longer says optional (PDF)')
    content = revise(
        content,
        '<input class="wf-input" type="text" id="wf-advisor" placeholder="e.g. Rockefeller Capital" />',
        '<input class="wf-input" type="text" id="wf-advisor" placeholder="e.g. Rockefeller Capital" required />',
        'form: advisor field required (PDF)')
    content = revise(
        content,
        '          if (isPartner) {\n'
        '            if (!org) { orgInput?.focus(); return; }\n'
        '          } else if (!tier) {\n'
        '            tierInput?.focus();\n'
        '            return;\n'
        '          }',
        '          if (isPartner) {\n'
        '            if (!org) { orgInput?.focus(); return; }\n'
        '          } else {\n'
        '            if (!tier) { tierInput?.focus(); return; }\n'
        '            // Introduced, not sold: a client submission names its introducer.\n'
        '            if (!advisor) { advisorInput?.focus(); return; }\n'
        '          }',
        'form: advisor required in the submit handler (PDF)')

    # The closing card carried two actions side by side, which splits intent at
    # the point of highest commitment. The partner route is reachable from the
    # bar, the footer and the Partners section itself.
    content = revise(
        content,
        '\n            <a href="#partners" class="btn-outline">For advisors and firms &#8594;</a>',
        '',
        'closing card: second CTA removed (PDF)')

    content = _move_partner_notes_up(content)
    return content


def _drop_hero_strip(content):
    """Remove the hero's "Where we are" strip, both copies of every item.

    The strip is listed twice in the source: once for reading, once aria-hidden
    so the phone marquee has something to loop. Taking the element out takes
    both. The intro timeline looks the strip up with a guard and skips it when
    it is absent, so nothing in the layout script needs changing.
    """
    m = re.search(r'[ \t]*<div class="credbar">', content)
    if not m:
        sys.exit('client revision "hero strip": the .credbar block was not found')
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
        sys.exit('client revision "hero strip": the block is never closed')
    end = content.find('\n', end) + 1
    APPLIED.append('hero: the "Where we are" strip removed entirely (PDF)')
    return content[:start] + content[end:]


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

    # For advisors. The WhatsApp round read as "remove it"; the PDF is explicit:
    # "Repoint to #partners until the real page ships". So it stays and points at
    # the Partners section, which is where the advisor material actually is while
    # /for-advisors is a redirect to the home page.
    footer = revise(
        footer,
        '<a href="/for-advisors">For advisors and firms</a>',
        '<a href={`${base}#partners`}>For advisors and firms</a>',
        'footer: For advisors repointed to #partners (PDF)')

    return footer


def apply_to_css(css):
    """Stylesheet consequences of the revisions above.

    Appended rather than edited in place, so the drop's own stylesheet stays
    verbatim above it and every revision-driven rule is visible in one block.
    Appended last, so it wins on order alone and needs no extra specificity.
    """
    APPLIED.append('stylesheet: case-stats, therapies panel, notes spacing, step-card titles')
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

/* The partner notes moved above the stats and had no space under them, so the
   dark panel sat flush on the stats card. 1rem is the gap .case-band uses
   between its own halves and the gap .deliver takes from the card above it, so
   the three blocks now sit on one rhythm. */
.partner-notes { margin-bottom: 1rem; }

/* Step cards: the titles start at the top, not the bottom.
   .step-n carried margin-bottom: auto, which pushed the title and body to the
   foot of a fixed-height card. A two-line title or a four-line body then
   started higher than its neighbours, so no two titles in the row began at the
   same height. The copy sits under the number now and the slack falls at the
   foot of the card, where it is not read as misalignment. */
.step-n { margin-bottom: 0; }
"""

# ── STILL OPEN ───────────────────────────────────────────────────────────────
#
# The record block above is live, and its closing sentence contradicts
# compoundhealth.io/privacy-policy, Sharing and disclosure:
#
#   "Wealth advisors: With your explicit consent, relevant health summary data
#    may be shared with your advisory firm to support integrated financial and
#    health planning"
#
# and the same section permits transfer of personal data on a merger, which sits
# badly with an unqualified "we do not license it". Resolve one of two ways:
#   * amend the privacy policy so the promise is true, or
#   * soften the sentence to what the policy allows, for example "never shared
#     with your employer or an insurer, and with your advisory firm only on your
#     explicit instruction".
