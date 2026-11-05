# Quality loop            slug: quality-loop   status: candidate
type: procedure
scope: tasks=[system-design, investigation]   stage=[plan|execute|verify|capture]   (major or structural changes only)
created: 2026-11-05   last-applied: –   applications: 0 (+0 =0 -0 ?0)
links: see_also=[close-the-loop-first] contradicts=[] derived-from=[]

## Content
Use only for major or structural changes: a new, retired or restructured
mechanism, rule, file layout, data flow or component, or a build spanning
several files or sessions. Skip, saying so in one line, for routine edits,
fixes, copy changes and small single-file tweaks.
1. [plan] Frame the question; name what a wrong answer would cost; decide
   research lanes (3–5, each a different angle: mechanics, prior art,
   fit-against-actuals, adversarial value judgment).
2. [execute] When a wrong answer costs more than the lanes, fan out
   parallel research; repo-facing lanes cite file:line, web lanes cite
   sources with confidence tags; every lane returns
   design_lessons + caveats, not just findings.
3. [execute] Synthesize ONE deliverable yourself — never delegate the
   synthesis; agents feed it, the session owns it.
4. [verify] Adversarial multi-lens verification of the deliverable
   (2–3 lenses: constitutional/budget coherence · user desirability ·
   honesty/feasibility) — each lens tries to BREAK it, with file:line
   evidence. Expect to find your own fresh edits among the findings; the
   editor cannot see their own artifacts.
5. [execute] Fix ALL blockers/majors before shipping; then audit what the
   fixes added, and walk any instructions literally before they reach a
   person.
6. [capture] Bookkeep: schedule suggestion(s) for the decisions it opens,
   PROJECT log line, SESSLOG block with provenance, stage the tree.
Loop condition: if verification finds a blocker in the FRAME of the
design (not its text), return to step 1, not step 5.

## Source
- Applied ~8× 2026-08-26..29 in the parent Extended Mind system (mobile access, an API, a multi-stage design and its implementation, a re-translation, a tool review, structure and budgets): every verification pass found 1–4 blockers including the author's own same-day edits; zero shipped blockers known. [src:parent Extended Mind system log, 2026-08-28..29 | method:derived | verified:2026-08-29 | conf:H]
- SkillsBench-adjacent caution: self-generated procedures without outcome evidence show no measured benefit — this candidate shipped in the parent with 8 helped-shaped events but zero formal valence rows; the counter starts at 0 and must be earned. [src:parent Extended Mind system, skills format (§K) | method:derived | verified:2026-08-29 | conf:M]

## Log
- 2026-08-29 (parent system): proposed by the first consolidation pass — the dominant unnamed procedure of a build burst; task type system-design (observed 12 times) to enter the router only on the maintainer's activation.
- 2026-11-04 (parent system): activated on the maintainer's yes in a pending review, with three edits (a mandatory prior-art clause dropped because learn-from-others-first loads on these task types; lanes fan out only when a wrong answer costs more than them; step 5 audits what the fixes added) and the maintainer's scope: major or structural changes only, not every edit; 6 uses by then (5 helped, 1 neutral).
- (template v3.2.0): shipped as an optional candidate rule. It never loads as shipped. Its prior-art step lives in learn-from-others-first, so promote both together. This template's router has no system-design or investigation row; promoting it (your yes to this text, meta.md §1 Path A) adds its _router.md rows, with its scope note, and ratifies those task types (meta.md §7).
