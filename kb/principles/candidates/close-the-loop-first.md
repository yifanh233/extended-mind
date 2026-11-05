# Close the loop first            slug: close-the-loop-first   status: candidate
type: guideline
scope: tasks=[system-design, investigation]   stage=[plan|verify]
created: 2026-11-05   last-applied: –   applications: 0 (+0 =0 -0 ?0)
links: see_also=[] contradicts=[] derived-from=[]

## Content
Get one full cycle of a system working end-to-end before adding the next
layer of sophistication. When designing an addition, name the still-unproven
loops it will sit on, and prefer sequencing that exercises them first. A loop
is closed by an executed run that produces evidence, never by shipping a
draft: an unexecuted finding is a hypothesis until it runs. Do NOT stack a
second unratified plan on top of a first; merge into one living plan.

## Source
- A design invariant of the parent system's v1.0 plan (2026-08-16), reaffirmed when a
  later plan risked landing before any consolidation pass or review had ever run —
  flagged 2026-08-20 in an architecture review ("assembled, engine not yet run
  under load"). [src:parent Extended Mind system, v1.0 plan and architecture review | method:derived | verified:2026-08-26 | conf:H]

## Log
- 2026-08-26 (parent system): drafted as a candidate (single sustained design thread — the maintainer's call).
- 2026-11-04 (parent system): activated on the maintainer's yes in a pending review, with the sentence on executed runs added from a security-review project's lesson (an unexecuted finding stayed unconfirmed until it ran) and scope widened to investigation, plan|verify; 10 uses by then (9 helped, 1 hurt).
- (template v3.2.0): shipped as an optional candidate rule. It never loads as shipped. This template's router has no system-design or investigation row; promoting it (your yes to this text, meta.md §1 Path A) adds its _router.md rows and ratifies those task types (meta.md §7).
