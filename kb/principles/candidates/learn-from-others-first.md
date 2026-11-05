# Learn from others first, before and after planning     slug: learn-from-others-first   status: candidate
type: procedure
scope: tasks=[planning, system-design, investigation]   stage=[plan|execute]
created: 2026-11-05   last-applied: –   applications: 0 (+0 =0 -0 ?0)
links: see_also=[quality-loop, machinery-then-surface] contradicts=[] derived-from=[]

## Content
Use when planning a project or any part of one, and again before building what was planned.
Skip, saying so in one line, when nothing new is being decided or built: a lookup, a
mechanical edit, or a question an earlier sweep already answered.
1. [plan] Inventory our own records first: notes, assessments, episodes, other projects.
   Internal prior art counts.
2. [plan] Own sketch first, at most 10 lines, written into the plan's header: problem,
   constraint, candidate approach. It is a hypothesis to compare against, never a commitment.
3. [plan] SEARCH BEFORE PLANNING. Who has tried this? Look for resources, tools, repos,
   papers, standards and post-mortems, including at least one failure. Budget in proportion
   to the build: one lane of a workflow, or about 30 minutes solo.
4. [plan] Write the plan after the search, compared against the sketch and the field.
   Keep a ledger in the plan: STEAL (what, how adapted, evidence), REJECT (why, with at least
   one alternative of our own), GAP (what nobody has done, where our own work goes).
   An empty search is a claim: state the search terms.
5. [execute] SEARCH AFTER PLANNING, for each planned part before building it: which tools,
   libraries, repos, templates or services already do this part? Decide USE (check licence,
   upkeep, security and fit; installing anything needs the user's word), BORROW the idea, or
   BUILD. Record the choice beside that part of the plan.
6. Weigh by evidence, never by stars or source. Before adopting the first thing found,
   run one deliberate pass for an alternative.
- Do not let a search become the task. At the budget's edge, log what was covered and what
  was not, proceed, and queue the rest.
- Drafting a task-scoped rule: the search lands at promotion, not at candidacy.

## Source
- The maintainer's directive, 2026-11-02: when planning a project, search for relevant
  resources, tools and repos and use them, directly or by borrowing ideas, both before and
  after planning. [src:parent Extended Mind system, maintainer's directive | method:human | verified:2026-11-02 | conf:H]
- The maintainer's earlier directive, 2026-09-02: learn from others before building our own.
  [src:parent Extended Mind system, maintainer's directive | method:human | verified:2026-09-02 | conf:H]
- Already practiced at least 9 times in the parent system with file evidence (a study of
  published agent-skill frameworks before a build stage; a memory-lifecycle investigation
  whose four domains converged; an agent-vault review that PREVENTED an adoption; an
  ecosystem scan with a ranked steal-list and a list declined with evidence); honest
  counterexamples at the small end (the system's founding substrate was designed without a
  landscape scan — benign by luck; a decision-record grammar engaged ADR prior art in one
  line). [src:parent Extended Mind system, prior-art assessment | method:derived | verified:2026-09-02 | conf:H]
- Highest-impact science = exceptionally conventional combinations of
  prior work plus an injection of atypical ones (~2× top-5% citation
  rate); recombining familiar components lowers inventive uncertainty.
  [src:Uzzi et al. 2013 Science 342:468; Fleming 2001 Mgmt Sci 47:117 | method:web | verified:2026-09-02 | conf:H]
- NIH is measured: stable R&D groups' performance declines noticeably by
  ~5 years, tracking reduced communication with information sources
  (internal AND external); the mirror bias — overvaluing outside
  knowledge for status/scarcity — is also documented: weigh by content,
  never by source.
  [src:Katz & Allen 1982 R&D Mgmt 12:7; Menon & Pfeffer 2003 Mgmt Sci 49:497 | method:web | verified:2026-09-02 | conf:H]
- Fixation is real but a dosage problem: designers copy even
  explicitly-flawed example features (Jansson & Smith 1991);
  eye-tracking shows the first solution captures attention during
  sincere search for better (Bilalić et al. 2008/2013); yet the
  43-study meta finds examples on average RAISE novelty and quality
  while narrowing category spread (Sio et al. 2015) — bound the sweep
  and record rejects; do not skip exposure. CAVEAT: self-generated
  initial ideas fixate too (Viswanathan et al. 2020, J. Mech. Des.
  142(10) — abstract-level, conf:M), so the step-2 sketch is bounded
  (≤10 lines, hypothesis-never-commitment), not treated as a pure guard.
  [src:Design Studies 12:3; PLOS ONE 8:e75796; Design Studies 2015; JMD 142(10) | method:web | verified:2026-09-02 | conf:M-H]
- Institutional practice: Rust RFC template mandates a "Prior art"
  section; Google design docs mandate "Alternatives considered"; patent
  novelty legally requires a formalized prior-art search.
  [src:rust-lang/rfcs 0000-template.md; industrialempathy.com Design Docs at Google; USPTO MPEP §2103 | method:web | verified:2026-09-02 | conf:H]
- Honest gap: no experimental literature quantifying survey-paralysis
  was found; the time-box rests on opportunity cost + the dosage
  finding (a single uncommon example beats many), not a measured
  paralysis effect. [method:derived | verified:2026-09-02 | conf:M]

## Log
- 2026-09-02 (parent system): drafted as a candidate from the maintainer's directive; adversarially verified.
- 2026-11-02 (parent system): merged with the maintainer's two-search principle at the maintainer's
  direction; scope widened from system design to every project's planning. 2026-11-03: activated on
  the maintainer's yes to this text (meta §1 Path A).
- (template v3.2.0): shipped as an optional candidate rule. It never loads as shipped. This template's
  router has no planning, system-design or investigation row; promoting it (your yes to this text,
  meta.md §1 Path A) adds its _router.md rows and ratifies those task types (meta.md §7).
