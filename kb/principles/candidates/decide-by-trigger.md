# Decide by trigger, not by mood            slug: decide-by-trigger   status: candidate
type: guideline
scope: tasks=[system-design, decision]   stage=[plan]
created: 2026-11-05   last-applied: –   applications: 0 (+0 =0 -0 ?0)
links: see_also=[] contradicts=[] derived-from=[]

## Content
Convert recurring "should we?" debates into pre-committed triggers: name the
observable condition and the action it fires, then stop relitigating. When
adopting a mechanism whose value is uncertain, pre-commit its kill/retune
threshold (a measurable rate and a date) at adoption time, not after
attachment forms. Do NOT escalate architecture by enthusiasm.

## Source
- The parent system's v1.0 plan carried an escalation table ("decide by trigger,
  not by mood", 2026-08-16), and it fired successfully at a migration: the
  storage trigger row was simply executed, not re-debated, 2026-08-17.
  [src:parent Extended Mind system, v1.0 plan and migration assessment | method:derived | verified:2026-08-26 | conf:H]
- A pre-committed kill/retune threshold planned for a later subsystem of the parent
  system is this principle applied forward. [src:parent Extended Mind system, upgrade plan | method:derived | verified:2026-08-26 | conf:M]

## Log
- 2026-08-26 (parent system): drafted from lived history (2 supporting events).
- 2026-08-29 (parent system): a consolidation pass reconciled two helped applications by analogy (revisit gates on a tool adoption; a log-retirement trigger and a pressure gauge) and one independent derivation (triggers beat fading salience). Evidence: 3+ events across two domains.
- 2026-11-04 (parent system): activated, text unchanged, on the maintainer's yes in a pending review, after 16 valenced uses (12 helped, 4 neutral, 2026-08-26 to 2026-09-12).
- (template v3.2.0): shipped as an optional candidate rule. It never loads as shipped. This template's router has no system-design or decision row; promoting it (your yes to this text, meta.md §1 Path A) adds its _router.md rows and ratifies those task types (meta.md §7).
