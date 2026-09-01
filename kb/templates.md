# templates.md — formats & protocol reference    version: 2 (template — discovery §H + skills §K)

Section letters are historical; the constitution refers here by them
(e.g. "kb/templates.md §F").

## §B — SESSLOG specification

End EVERY substantive session by appending ONE block at the END of sesslog.md
(repo root), separated from the previous block by one blank line. Fixed tokens
(`SESSLOG`, `CONSOLIDATED`, slug spellings) make Grep deterministic —
spellings are canonical, never vary them. Search recipes use PLAIN
SUBSTRINGS — never \b word-boundary assertions: CJK characters count as
word characters, so \bSESSLOG\b fails to match 记录SESSLOG完成. Keep a space
between CJK text and Latin tokens (good style and boundary safety). Blocks are append-only: never edit
or delete past entries.

Trigger: the assistant appends the block unprompted at session end,
announcing it;
the user typing `end` forces it immediately.

Format (omit empty fields):

    SESSLOG 2026-08-16 | mode: work | agent: claude-code | scope: project/system
    topics: retrieval-controller, fsrs-scheduling
    decisions: adopted luggage-db threshold at "one-session readability"
    claims-quarantined:
      - "FTS5 ships in Python stdlib sqlite" [method:model conf:M]
    threads: opened phase-3-flashcards; closed sql-vs-markdown
    capture: idea — trails could double as spaced-repetition decks
    learner: reviewed 6 items, 1 lapse (hub-and-spoke)
    provenance: rules=[5,6] notes=[hub-and-spoke] episodes=[sesslog#2026-08-12] — how:"rule 5 gated the commit; hub-and-spoke shaped the outline"
    next: draft flashcard-deck spec as a kb/ file

Field glossary:
- mode: work | feynman | socratic | devil | review | CONSOLIDATED
- agent: which assistant ran the session (claude-code, codex, cursor,
  gemini, …) — REQUIRED; enables per-agent strength tracking and makes
  cross-assistant handoffs auditable
- scope: the session's ONE declared scope (§C) — a project slug or
  `general` — REQUIRED; makes the baton per-scope: boot reads the last
  block overall AND the last block of its own scope
- topics: concept slugs touched this session (kebab-case, stable spellings);
  slugs may debut here before any note exists — the next ritual alias-checks
  and seeds them
- decisions: rulings made, one line each
- claims-quarantined: every model-generated or model-inferred claim stated
  this session, each with [method:model|derived conf:H|M|L]
- threads: lines of work opened/closed/touched, by slug
- capture: stray ideas to keep (saying "capture: ..." mid-session lands here)
- learner: review results, if a review happened
- next: the single most likely next action
- principles: `applied=[slug:valence(short clause), ...] violated=[slug(why), ...] candidate="one-liner" task-type=<router type | new:<kebab-slug> | none>` — valence ∈ helped|neutral|hurt|unknown; `new:` entries are candidate task-types meta.md §7 alias-checks; this field is the SOLE data source for principle track records (ritual-reconciled into §P headers)
- skills: `used=[slug:valence, ...] new=[slug, ...]` or `used=none` — every
  skill loaded or generated this session (§K); ritual-reconciled into
  skill headers and _index.md
- provenance: `rules=[N,...] principles=[slug,...] notes=[slug,...] episodes=[sesslog#YYYY-MM-DD,...] skills=[slug,...] — how:"one clause per load-bearing item"` — the visible audit trail of what shaped this
  session's work (rule 4): list only LOAD-BEARING items, not everything
  touched; the ritual reviews these lines for repeated integrations
  (§K generation signal) and for review of how the system is used.
  Omit empty subkeys. Never cite a rule for its routine operation
  (logging, boot, anti-echo) — only when it ruled something in or out
  this session; a setup or pure-chat session may write
  `provenance: (none — <reason>)`

Rules: omit empty fields, but an explicit `(none — reason)` value is allowed
when the absence itself is informative — rituals skip any value starting with
`(none`. Consolidation sessions append `SESSLOG ... | mode: CONSOLIDATED` —
the marker the next ritual greps sesslog.md for to find its starting point.

## §S — Schedule grammar (schedule.md)

One item per line, todo.txt-derived, GitHub-checkbox compatible:

    - [state] (P)? DATE? free text +tag @context key:value...

- state: `[ ]` open · `[?]` suggested (agent-proposed; the assistant's only
  free-write zone is the Suggestions section) · `[x]` done (completion date
  first after the x).
- `(A)`–`(Z)` priority, always the user's — the assistant NEVER writes priorities.
- Dates ISO `YYYY-MM-DD`. On an OPEN item a bare leading date is shorthand
  for `due:` that date (the todo.txt creation-date reading is explicitly
  ruled out); overdue = any open item whose due date, bare or keyed, is
  < today. Key vocabulary: `due:` deadline (agenda warns beforehand, shows
  overdue) · `start:` earliest-start (on the agenda from that date, carries
  forward until done) · `rec:Nd|w|m` — on completion the assistant re-adds the item
  with dates shifted from the COMPLETION date by the interval (org ".+"
  style, so a late run never reschedules into the past); the done-mark and
  re-add are ONE atomic edit, announced · `reason:"..."` + `conf:H|M|L`
  (both mandatory on every suggestion) · `src:` (mandatory when a
  suggestion derives from a recorded event or file; value = a file path,
  or sesslog#YYYY-MM-DD for a session block).
- Sections: Agenda (dated) / Tasks (undated) / Suggestions / Done.
- Approval flow: the user approves in plain language →
  the assistant echoes the exact post-edit line, gets assent in the same exchange,
  then flips `[?]`→`[ ]` and moves it; rejection → the line is recorded in
  the session's SESSLOG decisions field, then deleted (rejections are Path
  B fuel, not lost signal). Done >14 days old is archived by the ritual.
- Today's agenda (single source — rule 2 defers here) = overdue +
  `due:`≤today + `start:`≤today + open undated tasks the user pinned with
  priority + suggestion count, plus a one-line lookahead of items due within
  the next 7 days.
- "What should I do next?" is answered from APPROVED items, in order:
  overdue → due today → started → priority-pinned → open undated tasks
  (listed in file order, no invented ranking). The assistant is a
  fallback, never a competitor, to the user's own plan: suggestions are
  offered only when no approved item remains, or when the user asks for
  ideas.

## §C — Session concurrency & scope (one task per window)

Scope = a repo, or a project subtree within this one. ONE live working
session per scope; "live" = open and not yet ended with its §B block —
the baton fires only at `end`, so open sessions are mutually invisible.
Parallel windows across DIFFERENT scopes are safe by design (disk is
the shared truth; context is not).

- DECLARE: at the first substantive task, the session names its scope
  in one line — a project slug (project/<name>) or `general`
  (chat/lookup, no project writes) — and carries it in the §B header
  (`| scope:`). System files (kb/, AGENTS.md, templates) are
  project/system scope; the ritual and first contact are inherently
  project/system. One scope per window: an unrelated task arriving
  mid-session → name the mismatch and offer the choice (redirect to
  the owning window / take it here, logging the scope switch) — never
  silently absorb another scope's work.
- WRITE SCOPE: a session writes only (a) its scope's workspace files,
  (b) shared ledgers for entries IT generates (its own sesslog block,
  its own Suggestions lines, inbox appends), (c) kb/ and rule files
  only under project/system scope or a ritual duty.
- FOREIGN DIRT: uncommitted changes this session did not make are
  another window's in-flight work. Report once, one neutral line ("N
  paths outside this scope are modified — left for their windows");
  NEVER stage, process, route, log, or "deal with" them. Staging is by
  explicit path of the session's own writes — `git add -A`/`-u` are
  FORBIDDEN (they sweep every window's work into one signature).
- Before this session — or a subagent it dispatches — writes in a
  scope it did not boot in: check for a live session there (recent
  activity, not "is generating right now"); found one → surface the
  choice: proceed read-only / partition paths / wait / take ownership.
- Genuine parallel work in ONE scope → git worktrees, one per session;
  merge through git, never through shared working-tree luck. Mid-flight
  overlap (a file changes under you) → re-read before editing; logical
  conflicts go to the user, never resolved silently.
- `end` promptly — an open idle session holds invisible context and
  blocks its scope. Cross-scope insight → one inbox.md line.

## §L — Language (structure English, substance yours)

Instruction files and all grammar stay ENGLISH: translated instructions
are followed measurably less reliably, worst on non-Latin scripts
[src:arXiv:2410.15553 Multi-IF | method:web | verified:2026-08-28 | conf:M],
while English-instructions + native-conversation is the strong pattern
[src:arXiv:2210.03057 MGSM | method:web | verified:2026-08-28 | conf:M].
User-facing prose — conversation, note summaries and claims, schedule item
text, sesslog decisions/captures, reason:"..." values, principle Content/
Source prose, PROJECT.md prose — is written in the user's language (keys,
scope/stage/status vocabulary stay English). Quoted fallback strings in
the rules (e.g. "nothing due") are prose too — rendered in the user's
language, not protocol tokens.

DO-NOT-TRANSLATE (byte-identical, always): SESSLOG · CONSOLIDATED · mode
tokens (end, boot, review, consolidate, capture:, principle:) ·
field keys (topics:, decisions:, threads:, capture:, next:, agent:,
learner:, principles:, skills:, provenance:, due:, start:, rec:,
reason:, conf:, src:, method:, status:, applied=, violated=, used=,
new=, task-type=, use-when:, integrates:, uses:) · §H ledger states
(unseen, seen, off, hints:, last:, ign:) · §H section/tombstone tokens
(`## Firsts`, `Firsts:`, `firsts: complete`) · § letters · file names ·
slugs (kebab-case ASCII) · [ ] / [?] / [x]. The system name is
rendered native + English together (延展心智, Extended Mind).
`principle:` is a literal hard gate (meta.md Path A); the language-neutral
path is explicit confirmation of the drafted §P text. A near-miss prefix
(原则：, or principle： with a full-width colon) is flagged, its intent
confirmed, then routed through Path A's drafted-text confirmation — never
silently demoted, never activated on the flag alone.

Mixed-script mechanics:
- Full-width lookalikes silently break the grammar: ：(U+FF1A) is not `:`,
  U+3000 is not a space, 【】 are not brackets. "Token positions" = the
  structural slots of a grammar line — checkbox, priority, date, key:value
  tokens, AND the separators between them (prose untouched; `[?]　` is
  the separator case). The ritual's housekeeping pass normalizes
  schedule.md, inbox.md, and INDEX ## Firsts working lines; sesslog.md
  is append-only, so contamination in past blocks is FLAGGED in the
  Brief, never edited.
- Filenames: DEFAULT = ASCII kebab-case slugs, with the native-script
  title as the note's `#` heading. Native-script filenames are OPT-IN and
  require: `git config core.quotepath false` (all platforms — else CJK
  names render as octal escapes in the very diffs the user reviews),
  `core.precomposeunicode true` (macOS), UTF-8 console on Windows
  (`chcp 65001`).
- Budgets: LINE budgets carry across scripts unchanged; word budgets
  restate as characters (greeting ≈850 English words ≈ 约1,350字 zh /
  約1,900字 ja).
- Smaller/open models drift to English mid-conversation far more than
  frontier ones; the bilingual example below is the mitigation — if drift
  appears, ADD examples; never translate the rules.

Worked example — English tokens, Chinese prose (the shape every file
follows; the pinyin slug shows the default ASCII-slug lane):

    SESSLOG 2026-09-01 | mode: work | agent: cline
    topics: job-search, mianshi-zhunbei
    decisions: 面试准备改为每天早上一小时（本周以模拟面试为主）
    capture: 想法 — 把行为面试问题按 STAR 结构整理成 kb 笔记
    next: 周一早上开始第一轮模拟面试

    boot line → 焦点：求职 | 今日无到期事项（7 天内: due:2026-09-03 简历）|
    上次 next: 模拟面试 | 待批准：1 条建议

    - [ ] 修改简历并发给内推人 +job-search due:2026-09-03
    - [?] 每天早上练习一小时面试题 +job-search reason:"你说面试是本周最重要的事" conf:H src:sesslog#2026-09-01

Translated docs (README.xx.md, GUIDE.xx.md): sibling files with a 4-line
header (source / source-commit / translator / date). source-commit = the
ENGLISH source's last ratified commit at translation time (UNPINNED
counts as behind and is flagged every ritual until set); the assistant-
facing script is normative ONLY in English — translated copies exist for
the user to read and as phrasing reference; if the pinned commit is behind the source, the English file wins
(the precedence line is written inside each translation, in its own
language). One named owner per language, or the translation is deleted.
Fixes found while translating go to the English source first. After any
translation pass, grep the file for every DO-NOT-TRANSLATE token — all
must survive byte-identical.

## §D — Concept note template + claim grammar

Concept notes live at kb/notes/<slug>.md.

    # <Concept name>            slug: <kebab-case>   status: seed|growing|evergreen
    updated: YYYY-MM-DD         verified: YYYY-MM-DD
    links: instance_of=[...] part_of=[...] supports=[...] contradicts=[...] see_also=[...]

    ## Summary
    (2–6 sentences of MY endorsed understanding — human-voice prose)

    ## Claims
    - <claim text> [src:<chat-date|url|doc> | method:human|web|model|derived | verified:YYYY-MM-DD | conf:H|M|L]

    ## Open questions
    - <question> → kb/questions.md#<id>

    ## Log
    - YYYY-MM-DD: <one-line delta>

Grammar rules:
- One claim per line; editing a claim updates its `verified` date.
- `contradicts=` links are first-class and checked every ritual.
- Slugs never change once created (create alias notes instead).

## §P — Principle format (kb/principles/)

    # <Name>            slug: <kebab-case>   status: active|candidate|deprecated
    type: procedure|guideline
    scope: tasks=[<router types>|*]   stage=[plan|execute|verify|capture|*]
    created: YYYY-MM-DD   last-applied: YYYY-MM-DD   applications: 7 (+4 =2 -1 ?0)
    links: see_also=[...] contradicts=[...] derived-from=[...]

    ## Content
    (purely imperative — what/how/what-NOT; procedures: numbered stages,
     each tagged [plan|execute|verify|capture], with explicit branch/loop
     conditions. NO factual assertions here.)

    ## Source
    (the event(s) that taught this, full §D claim grammar; method may be
     human|web|model|derived — "derived" strictly = stated inference from
     tagged claims or directly observed session events)

    ## Log
    - YYYY-MM-DD: <delta>

Rules: stage vocabulary is closed (plan|execute|verify|capture|*) — it is
the join key binding guidelines to procedure stages. The full in-scope set
loads at task start; stage scoping means honored-at-that-stage. Counters
(`applications:`, `last-applied:`) are written by the ritual ONLY, from SESSLOG `principles:` fields; format `N (+h =n -x ?u)`.
Candidates live in kb/principles/candidates/ — same format,
`status: candidate` (legal only there); committing
one is versioning, NOT ratification; the ratification signal is the move
into kb/principles/ + status flip, performed by the user (directly or by
ratifying a ritual proposal). Promotion gate: the user's say-so, or ≥2
independent supporting events + ritual proposal. Amendments: hurt/violated
outcomes trigger ritual-proposed edits; scope-narrowing may follow one
event, scope-broadening needs two. _router.md lists ACTIVE principles only
and is regenerated by the ritual from §P headers; its task-type rows are
the canonical taxonomy (meta.md owns add/merge/rename).

## §R — Review scheduling (learner.md)

A review session works the due rows of kb/learner.md and updates them in the
working tree:
- pass → last-result: `pass YYYY-MM-DD`; the interval doubles (2d → 4d → 8d →
  16d → 32d …); due = today + new interval.
- lapse → last-result: `lapse YYYY-MM-DD`; due = tomorrow; add the confusion
  to misconception notes in ≤1 line.
- learner status: seed → growing after 2 consecutive passes; evergreen is
  granted only by a consolidation ritual. Learner status is independent of the
  note's own status field.
- Nothing due: say so and offer to pull the next date forward.

(Interim scheduler; module on STANDBY by default.)

## §W — Project file (workspace/<project>/PROJECT.md)

    # PROJECT — <name>    slug: project/<kebab-case>
    goal: <one line>
    status: <active|paused|done> — <one line>
    load: kb notes [...] · principles [...]    (what rule 11 pulls in)
    open: <bullets>
    log:
    - YYYY-MM-DD: <delta>

Sessions doing project work update status/open/log at session end.

## §F — Consolidation ritual

Standard (run it manually every few days; can be scheduled later):

    consolidate
    1. Grep sesslog.md for the last `mode: CONSOLIDATED` block; gather all
       SESSLOG blocks appended since.
    2. NREM: extract entities/claims/decisions/captures → match to kb/INDEX.md
       slugs (alias-check before creating a seed). Edit every touched note and
       INDEX directly in the working tree (bump the INDEX version line); for
       every note created or edited, add/update its kb/learner.md row (status,
       initial due date) — only when the learning module is ON.
    3. Immune pass: web-verify quarantined claims (for more than ~3 claims,
       fan out a verification workflow; cite sources); promote / hold in
       kb/quarantine.md. Pair new claims vs existing `contradicts` and
       same-slug claims; list conflicts for the user's ruling.
    4. REM: pick 2 concept pairs that are link-distant but share a motif;
       propose one bridge each (tag: speculation).
    5. Drives: advance ≤2 open questions from kb/questions.md (bounded web
       search, log the attempt line); refresh curiosity queue (3 frontier
       questions from learner.md due/lapse pattern + 1 REM wildcard).
    5b. Housekeeping pass: route inbox.md items added since the last ritual
       as proposals ([?] schedule lines / questions.md entries / note
       claims), clearing routed lines; reconcile SESSLOG `principles:`
       fields into §P counters and last-applied dates and regenerate
       _router.md from active §P headers (alias-check new: task-types per
       meta.md §7); archive Done schedule entries older than 14 days;
       normalize full-width token lookalikes (：→:, U+3000→space) in token
       positions (schedule.md, inbox.md, INDEX ## Firsts rows); for each
       translated doc whose pinned source-commit is behind its source
       (UNPINNED counts as behind), add a translations: line to the
       Brief; reconcile the ## Firsts ledger per §H (evidence-based
       seen-flips + grammar only); review provenance: fields for repeated
       integrations → generate or propose skills per §K, reconcile
       skills: valences into skill headers and _index.md, flip any skill
       that exists in HEAD (committed) but still reads status: unratified
       to active (presence in a commit IS the ratification evidence — no
       time window), and propose prunes after 2 hurt valences.
    6. Brief: due reviews, curiosity queue, contradictions, quarantine status,
       question progress, one strongest-objection-of-the-week, prune candidates,
       new/unratified skills for review + prune proposals (§K), muted tips (§H).
    7. Output order: Brief in chat → summary of working-tree edits (`git
       status --short`) → append SESSLOG | mode: CONSOLIDATED → remind the user:
       review the diff and commit to ratify.

First run (no prior `mode: CONSOLIDATED` marker anywhere in sesslog.md):
skip step 4 below ~6 concept slugs and step 5 while questions.md is
empty — say so plainly. A short honest first ritual beats a padded one.
The first run's Brief ALSO proposes the recurring line —
`- [?] consolidate rec:4d reason:"keeps the tidy-up rhythm you just saw" conf:M src:sesslog#<today>`
— the user's approval flips it to `[ ]` and rec: keeps the ritual
returning from then on (§S). This is the only place that line is seeded.

Deep pass (monthly, optional) — two deltas from Standard:
- add before step 2: "Build a SQLite index at .cache/mind.db (gitignored,
  disposable) from the kb/ files — nodes, edges, claims tables; report
  orphans, link-degree outliers, staleness median; update the health section
  in INDEX."
- step 6 additionally: "Include health deviations from setpoints + proposed
  gardening tasks."

## §H — Firsts & discovery (template default; user-mutable via rule 13)

Purpose: the user learns a capability at the moment it would help —
pull, not push. Surfaces: the boot line's §H checks (rule 2) and at most
ONE unprompted in-chat hint per session. Reactive teaching — naming a
mechanism right after the user's own act — is exempt from all caps and
self-limits to once per term.

Ledger — `## Firsts` in kb/INDEX.md (operational state, rule 1); one row
per capability, in exactly one of FOUR forms (brackets and parens are
LITERAL characters; `user|auto` means write one of the two words):

    - <slug>: unseen                                (seeded state, no hint yet)
    - <slug>: unseen hints:N last:YYYY-MM-DD ign:N  (hinted, not yet used)
    - <slug>: seen YYYY-MM-DD
    - <slug>: off (user YYYY-MM-DD)   /   - <slug>: off (auto YYYY-MM-DD)

No hint without its hints:/last: stamp, written in the same edit — the
row IS the cap counter, so cap enforcement is a grep, not a judgment.
Grep states with their colon prefix — `: unseen`, `: seen `, `: off ` —
never the bare word (`seen` is a substring of `unseen`). An ignore = a
hint fired (last: stamped) whose capability is still unseen when that
session's SESSLOG block is appended — increment ign: in the same edit
as the append. Degradation contract: hints are optional judgment — an
agent unsure of a state-match hints NOT AT ALL (silence is always
legal); the unseen→seen flip on first use is MANDATORY for every agent,
narration or not; missed flips are repaired by the ritual. The ritual
reconciles rows from evidence (consolidate ↔ `mode: CONSOLIDATED` ·
capture ↔ capture: fields · end-commit ↔ git log · schedule-items /
suggestion-approval ↔ decisions lines · devil / feynman-socratic ↔
mode: values OR a decisions line naming the stance — blended-stance
sessions note the stance in decisions · principle-teaching ↔
kb/principles/ contents · questions-predictions ↔ those ledger files)
— reconcile covers seen-flips and grammar normalization ONLY; hint
counts live solely on the row. No `## Firsts` section and no tombstone
→ reconcile is a no-op (graduated or pre-§H repo; NEVER re-seed).

Hints fire on state-match ONLY — the user's utterance or the repo's
state IS what the capability addresses (priority: utterance-match >
repetition 2–3× > queue threshold; never elapsed time). An utterance
that already REQUESTS the behavior ("tear this plan apart") is routed
and done (rule 7), then narrated as reactive teaching + seen-flip —
never answered with a hint; hints are only for states the user has NOT
asked to act on. One line,
phrased as SYSTEM state with the exact word to say — never the user's
tracked inaction: "(7 items are waiting to be filed — say consolidate
and I'll file them, fact-check my own claims, and show what connects)".
The first hint of any kind appends: say "no tips" to stop these. Caps:
≤1 unprompted hint per session; ≤2 lifetime per capability, the second
only ≥2 SESSLOG blocks after `last:`; 2 ignores → `off (auto)`, listed
once in the next Brief under "muted tips" (recoverable, never
re-nagged). Actionable-later hints go to schedule.md Suggestions
(`[?]` + reason: + conf: + src:), never repeated in chat.

Dismissals are restore-proof: "no tips" (intent-matched in any language
— 别再提示了 counts; not a byte token) DELETES the entire `## Firsts`
section (heading + rows) and replaces it with the single tombstone line
`Firsts: off (user YYYY-MM-DD)`, plus a SESSLOG decisions line; it also
mutes re-entry offers and every other §H nicety — only the neutral boot
counts remain. Per-capability "stop suggesting X" → `off (user DATE)` +
decisions line. Off rows and the tombstone are load-bearing state —
flag for commit (rule 5).

First-ritual gate (boot check): while no `mode: CONSOLIDATED` block
exists, offer consolidate ONCE when state crosses — ≥3 SESSLOG blocks
(grep `SESSLOG `) AND ≥5 lines total across capture: values in
sesslog.md plus item lines in inbox.md (one line = one item; headers
don't count) AND ≥3 claim bullets under claims-quarantined: headings
(NOT kb/quarantine.md, empty before the first run) — OR 10+ days since
the date of the FIRST SESSLOG block, with ≥2 blocks, whichever first.
That offer is consolidate's capability hint — stamp the consolidate row
hints:/last: in the same edit; the first run uses §F's first-run
variant. No progress counters in the boot line, ever.

Re-entry (boot check): newest SESSLOG block ≥7 days old → offer once,
"want to catch me up in two minutes?" — never state the gap length as
an observation about the user; never repeat in-session; muted by
"no tips". Zero-commit recovery (boot check): Identity set but no
commits → lead with the signature in plain words ("yesterday isn't
permanent yet — here are your two lines") — the first two boots only;
from the third, one clause inside the pending counts ("nothing
committed yet").

Graduation: when the last row is seen/off — announce in one line, append
`firsts: complete` to decisions, delete the section.

Help, always (pull — exempt from every cap): "what can you do?" in any
session → the four doors + the mode keywords + consolidate, in the
user's language; a forgotten keyword is re-taught freely on request.

## §K — Skills (kb/skills/)

A skill = compiled how-to: the integration of distributed rules, notes,
principles, and episodes into ONE repeatable procedure, written down so
the next occurrence loads one file instead of re-deriving the
combination — procedural memory consolidated from episodic + semantic.

    # <Name>    slug: <kebab-case>    status: unratified|active|deprecated
    use-when: <observable situation — a trigger, never a workflow summary>
    integrates: rules=[N,...] principles=[slug,...] notes=[slug,...] episodes=[sesslog#YYYY-MM-DD,...]
    created: YYYY-MM-DD   last-used: YYYY-MM-DD   uses: N (+h =n -x ?u)

    ## Steps
    (imperative, numbered; branch/loop conditions explicit; NO factual
     assertions — facts live in notes, this file only sequences them)

    ## Log
    - YYYY-MM-DD: <one-line delta>

Generation (automatic, rule 14): when the current session integrates
the same combination that provenance: lines show ≥2 prior times (grep
sesslog.md) — "same" = identical rules= and principles= and notes= SETS
describing the same activity (check topics:/how: overlap); episodes=
NEVER enters the match key (dates don't repeat) and is instead
accumulated into the new skill's integrates: line; the key must be
non-trivial (≥2 items, or ≥1 note/principle) — or when the ritual's
provenance review finds such a repeat — draft the skill, save
`status: unratified`,
add its _index.md row, announce in one line, and apply it from that
moment. The user's commit ratifies (ritual flips status to active after
a ratifying commit); "drop that skill" deprecates on assent. Evidence
caution: human-curated skills gained +16.6pp while SELF-generated
skills scored 8–12pp BELOW the no-skills baseline — actively harmful
without curation [src:arXiv:2602.12670 v4 | method:web |
verified:2026-08-29 | conf:H] — so every generated skill is announced,
listed in the next Brief for review, and pruned after 2 hurt valences:
generation is free, retention is earned.

Use (automatic): at task start scan _index.md `use-when` rows (trigger
vocabulary, rule 3); on match load the skill, announce in one line,
follow Steps, log `skills: used=[slug:valence]` (§B). Divergence from
reality → trust observation, note the delta in the skill's Log.

_index.md — one row per skill, `- <slug>: Use when <situation> (status)`;
≤40 lines (rule 1); regenerated by the ritual from skill headers.
