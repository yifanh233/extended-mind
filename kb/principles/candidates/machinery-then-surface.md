# Machinery first, then its surface            slug: machinery-then-surface   status: candidate
type: guideline
scope: tasks=[system-design]   stage=[plan]
created: 2026-11-05   last-applied: –   applications: 0 (+0 =0 -0 ?0)
links: see_also=[] contradicts=[] derived-from=[]

## Content
Build the best machinery first — system efficiency is the primary
criterion; do not compromise the mechanism to simplify its interface.
THEN design the best human interaction FOR that machinery: before
anything ships, name where the human sees it and the action it asks, and
keep that action under ~10 seconds — one line to read, one choice to
make; batches ≤4; options over prose. Do NOT ship a queue, ledger, or
approval gate without a decision surface — an unsurfaced queue is a
pile, not a feature. The surface is mandatory; it comes second and
serves the machinery rather than shaping it.

## Source
- The maintainer's correction of the first draft, 2026-08-29, in a decision
  review: do not design the human interaction before the machinery; have the
  best machinery first, then the best human interaction for that machinery;
  system efficiency itself stays most important. [src:parent Extended Mind system, maintainer's correction | method:human | verified:2026-08-29 | conf:H]
- The maintainer's prior teaching the same day: consider how the user as a human
  interacts with new functionality; simpler interactions keep a free,
  extendable system from becoming a mess. [src:parent Extended Mind system, maintainer's teaching | method:human | verified:2026-08-29 | conf:H]
- The triggering failure: 24 stored-but-unsurfaced suggestions + 3 asks
  buried in prose; the first decision review then resolved 4 decisions in under
  a minute — the surface, not the decisions, was the bottleneck.
  [src:parent Extended Mind system log, 2026-08-29 | method:derived | verified:2026-08-29 | conf:H]
- Approval-queue research: review items costing >10 seconds produce
  rubber-stamping or abandonment. [src:eucalipse.com approval-queue writeup | method:web | verified:2026-08-26 | conf:M]

## Log
- 2026-08-29 (parent system): v1 (human-surface-first) drafted from natural-language teaching; the maintainer corrected the priority order in the first decision review, and it was redrafted in the maintainer's words before ratification. The Content is the maintainer's own statement.
- 2026-08-29 (parent system): promoted on the maintainer's confirmation in the second decision review; moved to kb/principles/ with its router row (meta.md §2).
- (template v3.2.0): shipped as an optional candidate rule. It never loads as shipped. This template's router has no system-design row; promoting it (your yes to this text, meta.md §1 Path A) adds its _router.md row and ratifies that task type (meta.md §7).
