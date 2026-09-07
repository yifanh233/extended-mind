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
the user typing `end` forces it immediately. (Automatic appends close the app
edition's weakest link — P-001 in kb/predictions.md still tracks whether the
discipline holds.)

Format (omit empty fields):

    SESSLOG 2026-08-16.1 | mode: work | agent: claude-code | scope: project/system | boots-from: d20dcc7+ | session: 4466a286
    topics: retrieval-controller, fsrs-scheduling
    decisions: adopted luggage-db threshold at "one-session readability"
    claims-quarantined:
      - "FTS5 ships in Python stdlib sqlite" [method:model conf:M]
    threads: opened phase-3-flashcards; closed sql-vs-markdown
    capture: idea — trails could double as spaced-repetition decks
    learner: reviewed 6 items, 1 lapse (hub-and-spoke)
    next-hit: partial (spec drafted, artifact deferred)
    provenance: rules=[5,6] notes=[hub-and-spoke] episodes=[sesslog#2026-08-12] — how:"rule 5 gated the commit; hub-and-spoke shaped the outline"
    next: draft flashcard-deck spec as a kb/ file

Field glossary:
- mode: work | feynman | socratic | devil | review | CONSOLIDATED | sleep (Stage E)
- agent: which assistant ran the session (claude-code, codex, cursor,
  gemini, …) — REQUIRED (blocks before 2026-08-28 lack it: assume
  claude-code); enables per-agent strength tracking and makes
  cross-assistant handoffs auditable
- scope: the session's ONE declared scope (§C) — a project slug or
  `general` — REQUIRED from 2026-08-30 (earlier blocks: infer from
  topics); makes the baton per-scope: boot reads the last block overall
  AND the last block of its own scope
- key (C6, adopted 2026-09-06): the date carries a suffix `.N`, N = 1 +
  the count of this SCOPE's blocks already dated that day (allocated
  per scope, so it is coordination-free under one-live-per-scope);
  (key, scope) is the block's stable address — cite as
  `sesslog#2026-09-06.3` (+ `@<scope>` when two scopes share a date);
  grep `SESSLOG 2026-09-06.3 .*scope: project/system`. Blocks before
  2026-09-06 have no key — address them by date + unique phrase
- boots-from (C7, adopted 2026-09-06): the HEAD sha read at boot, with a
  trailing `+` when AGENTS.md / kb/templates.md / kb/principles/ were
  modified-uncommitted at boot. Grammar read at boot governs the session;
  newer grammar binds at the next boot. Two same-date blocks are ordered
  by this, and a stale view announces itself
- session (C8, adopted 2026-09-06): the harness session id (first 8
  chars; `n/a` if the agent has none), recorded at boot; every liveness
  or concurrency check compares ids FIRST — a sweep never flags its own
  edits as another live session
- topics: concept slugs touched this session (kebab-case, stable spellings);
  slugs may debut here before any note exists — the next ritual alias-checks
  and seeds them
- decisions: rulings made, one line each
- claims-quarantined: every model-generated claim stated this session, each with
  [method:model conf:H|M|L]
- threads: lines of work opened/closed/touched, by slug
- capture: stray ideas to keep (saying "capture: ..." mid-session lands here)
- learner: review results, if a review happened
- next: the single most likely next action
- next-hit: `yes | partial | no | n/a (short clause)` — scores whether the
  PREVIOUS block's next: actually happened, judged as this block is
  written; n/a when the prior next: was the user's act alone (adopted
  2026-08-29 from the user's 08-28 proposal)
- outcome: optional one line — what this session's main work actually
  produced vs what was intended (calibration companion to next-hit:)
- principles: `applied=[slug:valence(short clause), ...] violated=[slug(why), ...] candidate="one-liner" task-type=<router type | new:<kebab-slug> | none>` — valence ∈ helped|neutral|hurt|unknown; `new:` entries are candidate task-types meta.md §7 alias-checks; this field is the SOLE data source for principle track records (ritual-reconciled into §P headers — Stage B, §F v3)
- skills: `used=[slug:valence, ...] new=[slug, ...]` or `used=none` —
  every skill loaded or generated this session (§K); ritual-reconciled
  into skill headers and _index.md
- provenance: `rules=[N,...] principles=[slug,...] notes=[slug,...] episodes=[sesslog#YYYY-MM-DD,...] skills=[slug,...] bundles=[research/<date>-<slug>,...] — how:"one clause per load-bearing item"` — the visible audit trail of what shaped this
  session's work (rule 4): list only LOAD-BEARING items, not everything
  touched; the ritual reviews these lines for repeated integrations
  (§K generation signal) and as usage data for later review. Omit empty
  subkeys. Never cite a rule for its routine operation (logging, boot,
  anti-echo) — only when it ruled something in or out this session; a
  pure-chat session may write `provenance: (none — <reason>)`. Blocks
  before 2026-08-29 lack this field — absence is not evidence

Rules: omit empty fields, but an explicit `(none — reason)` value is allowed
when the absence itself is informative — rituals skip any value starting with
`(none`. Consolidation sessions append `SESSLOG ... | mode: CONSOLIDATED` and
carry `window-end: <scope>=<key> …` (C6) — the next ritual resumes from those
KEYS, not from the marker's file position.
Physical append (C1, adopted 2026-09-06): a block is appended as ONE `>>`
write (e.g. `cat block.md >> sesslog.md`), never by a whole-file Write —
every logical append on a multi-producer file is otherwise a whole-file
rewrite that can drop a concurrent block. Clears and compactions of
sesslog.md / inbox.md / schedule.md happen ONLY through an Edit anchored on
the exact consumed content (an accidental compare-and-swap — it fails
visibly on a race); whole-file Write on these files is banned.

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
  or sesslog#YYYY-MM-DD for a session block) · `deferred:YYYY-MM-DD
  reopen:"condition"` — parked: excluded from pending counts and §A batches
  until the reopen condition is observed (ritual checks each pass).
- Suggestion lifecycle (adopted 2026-08-29; cap amended 2026-09-06, C9): a
  suggestion untouched across 2 consecutive rituals auto-parks (`deferred:`
  + a reopen condition, or a retirement proposal if none exists). QUOTAS
  are PER SCOPE, not global — a window checks only its own scope's live
  `[?]` lines (a global count is write-skew-prone: two windows each read
  14, both add): project/system ≤8, each other scope ≤5; adding beyond the
  quota requires retiring one of the SAME scope in the same edit — the
  proposer ranks its own output. (The numbers 8/5 were set by the
  assistant when C9 was approved without them — adjust by ruling.)
- Sections: Agenda (dated) / Tasks (undated) / Suggestions / Done.
- Approval flow: the user approves in plain language (or frontend, Stage D) →
  the assistant echoes the exact post-edit line, gets assent in the same exchange,
  RE-READS the target line immediately before applying (C3: the assent
  window spans minutes to hours; if the pre-image differs from what was
  echoed, re-echo — never apply from memory), then flips `[?]`→`[ ]` and
  moves it; rejection → the line is recorded in
  the session's SESSLOG decisions field, then deleted (rejections are Path
  B fuel, not lost signal). Done >14 days old is archived by the ritual
  (Stage B, §F v3).
- Today's agenda (single source — rule 2 defers here) = overdue +
  `due:`≤today + `start:`≤today + open undated tasks the user pinned with
  priority + suggestion count, plus a one-line lookahead of items due within
  the next 7 days.
- "What should I do next?" is answered from APPROVED items, in order:
  overdue → due today → started → priority-pinned → open undated tasks
  (file order, no invented ranking). The assistant is a
  fallback, never a competitor, to the user's own plan: suggestions are
  offered only when no approved item remains, or when the user asks for
  ideas.

## §A — Decision presentation (how pending items reach the user)

Storage is §S; this section is the SURFACE. It exists because of
2026-08-29: three asks buried in prose walls went unseen and the user ended
the session (sesslog#2026-08-29, decision-triage block).

- Trigger: the user signals decision-processing ("deal with pending", "what
  needs me", …), or the micro-boot shows ≥3 pending items — then OFFER a
  batch, never force one.
- Triage by REQUIRED ACT before showing anything: (a) assistant-runnable →
  just do it and report; (b) dead/expired → propose retirement; (c) genuine
  the user decisions → batches.
- Batches of ≤4. Each item: ONE line, ≤15 words, plain language; options
  approve / reject / defer(+reopen:) / discuss. An agent with a native
  choice UI (e.g. Claude Code's multiple-choice question tool) MUST use
  it; other agents render a numbered list and accept single-letter
  replies.
- Echo-gated mutations (rule 12): the exact post-edit line(s) ride inside
  the chosen option's text — selecting it IS the assent; the line is
  re-read before the edit lands (C3, §S) — a changed pre-image re-echoes.
- Order: the single most-unblocking act first (usually the ratifying
  commit) → mechanical assents → package approvals → forks needing real
  thought. Deep forks get their own batch, never mixed with mechanical
  items. ≤3 batches per sitting unless the user asks for more.
- Every outcome lands in the files in the same exchange (flip / delete /
  deferred:+reopen:) AND in the session's SESSLOG decisions line.
- Decision stamp (adopted 2026-09-02, evidence-chain audit): when a ruling
  answers anything a `Status: INVESTIGATION` doc asked, the same exchange
  also stamps THAT doc's header: `decision: <verdict clause> (the user
  YYYY-MM-DD, sesslog#<date>+unique phrase — date.N once S3 lands)`; the
  why-clause is REQUIRED whenever adopted parameters differ from the
  proposed ones (the ~4-rituals→2/≥15 lesson: chat-only derivations are
  irrecoverable); question lines get CLOSED/DEFERRED markers in place.
  The suggestion line's src:+reason: is ephemeral — the stamp is the
  durable back-link that travels with the artifact.
- Design rule for ALL new functionality (machinery-then-surface, the user
  2026-08-29): build the best machinery first — system efficiency is
  primary — but nothing ships until its human surface and ≤10-second
  action are named. A queue without a decision surface is a pile, not a
  feature.

Approval-gated Git (rule 5, amended 2026-09-07): show the repository, exact
paths/change summary (make the full diff available), intended commit(s), and
for push the remote/branch and outgoing commits. The user may approve commit
and push together when both are shown. Approval is action- and content-specific;
unrelated staged files, later edits or a changed destination require a new
review/approval. Immediately before execution re-read the diff/index and ensure
they still match. Stop on unexpected remote divergence; force-push/history
rewrites require explicit approval for that action. Do not impersonate the
user's authorship; use the configured identity. Record the approval reference,
actual commit IDs and push result in the handoff; never report an attempt as success.

## §C — Session concurrency (one live session per scope)

Scope = ONE project (its workspace/<project>/ here plus every folder
its PROJECT.md `where:` block names, §W), or project/system (this
repo's system files), or `general` (no project writes); a folder
belongs to exactly one scope. ONE live working session
per scope; "live" = open and not yet ended with its §B block. Detection
(Claude Code): the session list of EVERY folder in the scope — sessions
are keyed by start directory, so one opened inside a `where:` folder
shows only in that folder's list — judged by lastActivityAt recency (≤~6h =
treat as live) — `isRunning` means "generating this instant" and is NOT a
liveness signal; other agents: ask the user. Exists because of 2026-08-29/30:
an agent was dispatched into a repo where the user's own session was live —
the §B baton only fires at session END, so open sessions are mutually
invisible (sesslog#2026-08-30).

- Before this session — or any subagent it dispatches — writes in a scope
  it did not boot in: check for a live session there. Found one → surface
  it to the user as a §A choice: proceed read-only / partition paths / wait /
  take ownership.
- Genuine parallel work in one repo → git worktrees, one per session;
  merge through git, never through shared working-tree luck (a merge is a
  commit — execution requires approval under rule 5; show the merge's changes
  and destination before asking, and renew approval if conflict resolution changes them).
- Ratification at QUIESCENCE (C4, 2026-09-06): commit when no session is
  live in the scopes being committed — `git commit -- <paths>` snapshots
  the WORKING TREE at commit instant, ignoring the index, so a window
  writing between review and commit silently changes what is ratified;
  review with `git diff HEAD -- <paths>`, not `--cached`.
- Commit requests are answered PER SCOPE (C5, 2026-09-06), in §A order:
  canon (`AGENTS.md CLAUDE.md kb/ workspace/system/` — the true ratify) ·
  per-project accept (`workspace/<project>/` — versions the project's
  context and the assistant's notes, canonizes nothing; the project's own
  repo ratifies its own work under its own rules, §W) · ops rider
  (`sesslog.md schedule.md inbox.md` — rides with any commit; rule 1 says
  ratification language does not apply). Never one sweep, never hunk
  surgery — a file that needs split ratification is split by scope.
- `end` is the baton: ending promptly is what makes work visible to every
  other session. Pausing a conversation = end now, boot later — an open
  idle session holds invisible context and blocks its scope.
- Mid-flight overlap detected (a file changes on disk under you): re-read
  before editing and REBUILD the edit from the fresh read — reject-and-
  retry, never patch-from-memory (C3); logical conflicts (divergent plans,
  not just divergent bytes) go to the user, never resolved silently.
- For the user: one conversation per SCOPE at a time (a project scope may
  span its own folder elsewhere plus its workspace/<project>/ here, §W);
  parallel conversations across DIFFERENT scopes are safe by design
  (disk is the shared truth; context is not). Returning to an older open
  conversation after another session touched its files → open with
  "re-read changed files", or end it and boot fresh.

Scope discipline (one task per window — the user 2026-08-30). Within this
repo — and any project folder a scope spans — concurrent windows are a
fact; what keeps them safe is that each session binds to ONE scope and
touches nothing else:
- DECLARE: at the first substantive task, the session names its scope in
  one line — a project slug (project/system, project/job-search, …) or
  `general` (chat/lookup, no project writes) — and carries it in the §B
  block header (`| scope:`), together with its own session id and the
  HEAD sha it booted from (`| session:` `| boots-from:`, C7/C8) — the
  on-disk identity a live session otherwise lacks. System files (kb/, AGENTS.md, templates)
  are project/system scope; the ritual and first contact are inherently
  project/system. One scope per window: an unrelated task arriving
  mid-session → name the mismatch and offer a §A choice (redirect to
  the owning window / take it here, logging the scope switch) — never
  silently absorb another scope's work.
- WRITE SCOPE: a session writes only (a) its scope's workspace files
  and `where:` folders (at their recorded access, under their own
  rules), (b) shared ledgers for entries IT generates (its own sesslog
  block, its own Suggestions lines, inbox appends), (c) kb/ and rule
  files only under project/system scope or a ritual duty, (d) the RITUAL
  explicitly (C10): schedule.md Done-archiving, auto-parks and assented
  re-adds, and the inbox.md cursor line — as duties, never as a window's
  discretion.
- YIFAN'S OWN EDITS (C10) are authoritative foreign dirt: a session never
  "handles", reverts, or re-files them; it re-reads and works on top.
- FOREIGN DIRT: uncommitted changes this session did not make are
  another window's — or, in a `where:` folder, the owner's own —
  in-flight work. Report once, one neutral line ("N paths I didn't
  touch are modified — left alone"); NEVER stage, process, route, log,
  or "deal with" them. Staging is by
  explicit path of the session's own writes — `git add -A`/`-u` are
  FORBIDDEN (they sweep every window's work into one signature). All of
  this holds in EVERY repo the session touches (`where:` folders too).
- Cross-scope insight → one inbox.md line, never a direct edit.

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

workspace/<project>/ is the project's CONTEXT + MEMORY home: PROJECT.md
plus what the assistant writes ABOUT the work (notes, plans,
assessments) and small inputs the user won't work on elsewhere (a PDF
to summarize). The work itself — code, documents, data, anything with
its own toolchain — stays wherever the user already keeps it; nothing
is copied or moved in. Rule of thumb: what the user opens in another
app to work on lives where they work; what the assistant must remember
about it lives here.

    # PROJECT — <name>    slug: project/<kebab-case>
    goal: <one line>
    status: <active|paused|done> — <one line>
    where:                     (omit = chat-only; one line per folder)
    - <label> = <absolute path | URL>  access: ro|rw  git: own|here|parent|none  rules: <file, relative to the path | none>  id: <git remote | marker file | none>  verified: YYYY-MM-DD
      note: <free text, optional — never inside a value>
    load: kb notes [...] · principles [...]    (what rule 11 pulls in)
    open: <bullets>
    log:
    - YYYY-MM-DD: <delta>

Tokenization: fields separated by two or more spaces, keys fixed and in
this order, values without double spaces or parentheses. Defaults:
`access: ro`; `git: none` forces `access: ro`.

- A `where:` line is written only after the user names the folder and
  says yes to the ECHOED line itself — or, at first contact, to its plain
  one-sentence form naming path and access — (rule-12 discipline: show
  the exact line, get the yes, then write); it is then the standing permission at
  that access level — read-only unless they said edit — and deleting the
  line revokes at once (working-tree semantics; flagged unratified until
  commit). Reading outside every `where:` = ask, once per session; never
  silently promote a path to `where:`.
- A `where:` is a PROJECT folder. A one-off file (a resume in Downloads)
  gets a one-off yes and is read in place — or is dropped into
  workspace/ — never a `where:` line on the folder around it. A path
  belongs to ONE project, prefix-inclusive: before writing a line, grep
  `workspace/*/PROJECT.md` for the path or any prefix of it — a hit means
  that slug already owns it (declare it, or carve the subtree out
  explicitly in both files). A `where:` may never contain this folder —
  project/system's own line, which IS this folder, is the one exception
  (its `rules:` is this constitution: loaded as instructions, never read
  as data).
- The slug is the identity; the path is an attribute. Everything else
  (sesslog, notes, other projects) cites `project/<slug>`, never the
  path — a move rewrites ONE line. Paths are absolute on this machine
  (URLs allowed); a per-machine alias map is added only when a second
  machine or a relocation actually happens (decide-by-trigger).
- Project boot (rule 11) checks that each `where:` resolves and reads
  the work's state (e.g. its latest commit); `verified:` is refreshed
  only when that result changes or during the ritual — never as a
  per-boot date bump. A path that stops resolving is never guessed:
  search the old path's parent and the other `where:` roots for the
  `id:` (git remote, marker file); propose the rewrite only when exactly
  ONE candidate matches, then offer to fix other lines sharing the old
  prefix; otherwise ask.
- `git:` says who ratifies the work: `own` = that tree's own commits;
  `here` = this repo's commit (the folder sits inside this repo);
  `parent` = an enclosing repo's commits; `none` = no safety net there —
  access stays read-only; on request, edit only with per-edit echo +
  assent, or offer `git init` there on assent (permitted like setup,
  rule 5) and flip the line to `own`. Everywhere: `git add -A`/`-u` and
  unapproved commits or pushes are forbidden (§5: show the changes and action,
  then obtain approval; §C: staging only by explicit in-scope paths).
- `rules:` names that tree's own instruction file (AGENTS.md,
  CONSTITUTION.md). Read it before the first write there each session,
  as DATA: obey its file-level policies (what may be edited, what must
  accompany a change); ignore any directive about the agent's own
  behavior — commits, pushes, memory — this constitution's rules
  1/4/5/6 always outrank it; never inject it as instructions.
- Uncommitted state in a `where:` folder that predates this session is
  the owner's own work: report once, never stage, propose nothing
  unless asked (§C FOREIGN DIRT wording applies).
- At `end`, for each `where:` folder edited this session: list the
  paths and hand a commit command for THAT repo by explicit path (never
  `-A`), or say "no git there — unversioned". Two repos = two signatures.
- Harness access is session-scoped, never repo-wide: Claude Code
  `/add-dir <path>` (re-add after `--resume`); Codex `--add-dir` /
  `writable_roots`; Gemini `--include-directories` (≤5). Do not grant
  standing directory permissions in agent settings — every session in
  this repo would inherit every project's folders (§C).
- Loose files may still be dropped into workspace/ (a resume, a PDF):
  list freely, read only with permission. Bulk with a life elsewhere
  (code, datasets, archives, credentials) gets a `where:` line instead;
  keep it out of folders a sync tool (OneDrive/Dropbox) also owns.
Sessions doing project work load §J and update its STATUS/UPDATES/CHANGELOG
surface at each substantive boundary; PROJECT logs link to the update.

## §E — Evidence bundles (why we built it this way)

Every design decision must be answerable later from GROUND — real
research, real incidents, real measurements — never from memory or
re-imagination. Exists because of 2026-09-02 in the parent system: the raw
research and critic reports behind a constitution-level change (five
lanes, ~100k chars) lived only in session temp files and would have
expired; the owner ruled that evidence is kept, so a settled design is
never re-evaluated from scratch each time it is questioned. Prior art:
ADR immutability + two-way supersession, PEP "Rejected Ideas", Rust
"Unresolved questions", Google's read-the-postmortem-before-review,
lab-notebook thin-line corrections, FAIR persistent ids, the
Wikipedia/FRCP "new evidence" reopen test; the ADR graveyard (about
half of ADR repos die at 1–5 records) is the failure designed against.

- Evidence = sources with URL + fetch date; real incidents — ours
  (sesslog#key) or external (issue URL + date); measurements with
  method. Lane/critic reports are the raw RECORD of how those were
  found: kept unedited, each lane's method: tally in the README, cited
  never asserted — the bundle says where to look, not what is true.
  Reasoning is not evidence: an uncited rationale sentence carries
  [method:model] — imagination, flagged.
- Where: workspace/<scope>/research/<YYYY-MM-DD>-<slug>/ — the
  directory name is the permanent id (never renamed, never reused);
  README.md ≤30 lines + one raw file per lane or critic, headed
  `# <lane> — raw report  run: <id>  date:` + `status: raw, unedited`;
  research/README.md is the per-scope index. Bundles are work product
  (user layer), versioned by commit, EXCLUDED from default retrieval
  like sleep/ — reached only through `evidence:` / `feeds:` links.

    # Evidence bundle — <slug>    date: YYYY-MM-DD    run: <id | manual>
    status: raw, unedited | superseded
    supersedes: / superseded-by: research/<date>-<slug>/   (optional, two-way)
    source: <session output path + mtime | agent | manual>
    scope: project/<x>
    question: "<what the evidence was gathered to answer>"
    feeds: <assessment.md §n> · <rule/§ clause>
    decided: pending | <verdict clause> (the user YYYY-MM-DD, sesslog#<key>)
    rejected: <option> — <why> (<lane>.md §)              (one line each)
    open: <question the evidence did not settle>
    reopen: only on evidence not in this bundle — <named trigger(s)>
    | lane file | first heading | chars | method | verified |
    annotations:   (append-only `YYYY-MM-DD agent: …`; nothing above changes)

- Immutability: lane files and everything above `annotations:` are
  raw evidence — never edited, deleted, or renamed. After creation
  exactly two fields may be written: `decided:` (by the session that
  records the ruling, in the same exchange) and `superseded-by:` (by the
  superseding bundle's session). Corrections, retractions, and later
  findings are dated `annotations:` lines, or a new bundle that
  `supersedes:` this one and states in `question:` what changed.
  Superseded ≠ wrong; the old bundle keeps answering "why did we
  believe that then".
- Mandatory for: any assessment doc; any change to core (AGENTS.md
  rules, templates.md grammars, principle activation); any decision
  taken on a workflow's or critic's findings. Not for schedule flips
  (`src:` suffices) or chat. The assessment carries an `evidence:`
  line naming its bundle(s); the SESSLOG decisions line cites the
  assessment and writes `decided:`. Chain: ruling (decisions line) →
  assessment → bundle → source. A run not bundled by session end is
  NOT CITABLE: any decision resting on it carries [method:model] until
  the run is redone and bundled.
- READ before reopen: a session that reopens an assessment, proposes a
  core change, or edits a clause carrying `because:` opens the bundle
  README first and says so in one line (as rule 10 announces
  principles). Retention without retrieval is the ADR graveyard.
- REOPEN RULE: a DECIDED design (a bundle's `decided:` ruling or the
  assessment's recorded verdict) re-decides only on evidence not already in its
  bundle — a new incident (sesslog#key), a new measurement, a source
  corrected by the immune pass (§F `re-decide?`), a named changed
  condition from `reopen:`, or an `open:` question now answerable.
  Undecided drafts (`Status: INVESTIGATION`, `decided: pending`) stay
  open to argument. Rule-8 counterpoints are still raised and logged
  (capture: or a `reopen:` condition); they never reopen by
  themselves. Re-arguing a decided design from the bundle's own
  contents → answer in one paragraph citing the bundle's SOURCES with
  their rule-6 tags and log `reopen-refused: <bundle> (same evidence)`
  in `decisions:`. The user may override by fiat, stamped like any
  ruling. Weak-evidence floor: if every lane is method:model at conf ≤
  M, argument alone reopens.
- Incident provenance: a grammar section or principle clause born
  from an incident carries `because: sesslog#<key>` (date + unique
  phrase) or the bundle path; constitution rules, which have no line
  budget for it, cite via their section's preamble. A clause without
  `because:` is a ritual sweep candidate, not a defect.
- Ritual anti-rot (§F housekeeping): assessment = any workspace/**/*.md
  with a `Status:` header; core change = `git diff <last-ritual-sha>
  -- AGENTS.md kb/templates.md kb/principles/`. `grep -L "^evidence: "`
  over assessments and `grep -l "decided: pending"` over bundle
  READMEs → each hit is a Brief line (record, not decide). §B
  provenance: carries `bundles=[path,...]`, so the ritual's provenance
  review yields bundle read-counts for free.
- Measure it: count re-asked settled questions per ritual — if the
  number does not fall, the bundles are a graveyard, not a memory.

## §F — Consolidation ritual

Standard (run it manually every few days; can be scheduled later):

    consolidate
    0. Confirm one live session owns project/system; record session/boots-from.
    1. Resume each scope after the last CONSOLIDATED window-end: key (§B);
       legacy unkeyed blocks use position after that marker.
    1b. Inbox routing is acknowledged AFTER durable outputs, never before:
       use tools/inbox_cursor.py begin --inbox inbox.md to append a pending
       routing: fence, or resume the existing pending batch. Route its fixed
       window only. New lines below the fence wait for the next batch.
       Each item has an id; before writing a destination search for its
       inbox:<batch>:<id> anchor and reuse an existing result on replay.
       Save a JSON receipt {batch, routes:[{id,destination}]} with one route
       per item, under workspace/system/ritual-receipts/. Destinations must
       exist and carry that anchor. A held item is routed to a durable Brief
       with its reason, never silently dropped. Then run inbox_cursor.py
       complete --inbox inbox.md --receipt <path>; it validates the receipt
       before appending routed:. Interrupted runs resume the pending fence.
       No Python: perform the same fence/window/source-anchor/receipt process
       by hand; routed: names the completed routing: fence, not its own file
       position. Never use a pre-routing marker as an acknowledgement. Preserve
       receipt files and inbox text. One ritual writer per scope; no locking
       or arbitrary multi-writer atomicity is claimed by the helper.
    2. NREM: extract entities/claims/decisions/captures → match to kb/INDEX.md
       slugs (alias-check before creating a seed). Edit every touched note and
       INDEX directly in the working tree (bump the INDEX version line); for
       every note created or edited, add/update its kb/learner.md row (status,
       initial due date) — only when the learning module is ON.
    3. Immune pass: web-verify quarantined claims (for more than ~3 claims,
       fan out a verification workflow; cite sources); promote / hold in
       kb/quarantine.md. Pair new claims vs existing `contradicts` and
       same-slug claims; list conflicts for the user's ruling.
    3c. Run §J's scoped change check for projects touched since the last ritual.
    4. REM: pick 2 concept pairs that are link-distant but share a motif;
       propose one bridge each (tag: speculation).
    5. Drives: advance ≤2 open questions from kb/questions.md (bounded web
       search, log the attempt line); refresh curiosity queue (3 frontier
       questions from learner.md due/lapse pattern + 1 REM wildcard).
    5b. Housekeeping pass: inbox routing completed in step 1b; never clear
       source lines. Reconcile SESSLOG `principles:`
       fields into §P counters and last-applied dates and regenerate
       _router.md from active §P headers (alias-check new: task-types per
       meta.md §7); archive Done schedule entries older than 14 days;
       normalize full-width token lookalikes (：→:, U+3000→space) in token
       positions (schedule.md, inbox.md, INDEX ## Firsts rows); for each
       translated doc whose pinned source-commit is behind its source
       (UNPINNED counts as behind), add a translations: line to the
       Brief; reconcile the ## Firsts ledger per §H (evidence-based
       seen-flips + grammar only); list assessments or core changes since
       the last ritual lacking an `evidence:` line or whose bundle is
       missing (§E); review provenance: fields for repeated
       integrations → generate or propose skills per §K, reconcile
       skills: valences into skill headers and _index.md, flip any skill
       that exists in HEAD (committed) but still reads status: unratified
       to active (presence in a commit IS the ratification evidence — no
       time window), and propose prunes under §K K-d.
    6. Brief: due reviews, curiosity queue, contradictions, quarantine status,
       question progress, one strongest-objection-of-the-week, prune candidates,
       new/unratified skills for review + prune proposals (§K), muted tips (§H).
    7. Output order: Brief in chat → summary of working-tree edits (`git
       status --short`) → append SESSLOG | mode: CONSOLIDATED with per-scope window-end: keys → remind the user:
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
    use-when: <observable situation, keywords first — a trigger, never a workflow summary>
    integrates: rules=[N,...] principles=[slug,...] notes=[slug,...] episodes=[sesslog#YYYY-MM-DD,...]
    created: YYYY-MM-DD   last-used: YYYY-MM-DD|never   uses: N (+h =n -x ?u)
    spec: <the rule clauses / § clauses / principle stages every step must satisfy>
    tests: <≥2 sesslog keys from DIFFERENT sessions where this procedure ran — or "insufficient">
    follow-policy: K-c (see below)

    ## Steps
    (imperative, numbered; branch/loop conditions explicit; NO factual
     assertions — facts live in notes, this file only sequences them)
    ## Checks
    (each spec item as something an agent can grep/ls/wc — never a judgment)
    ## Anti-steps
    (what was tried and failed, from the test episodes' critic catches — negative knowledge)
    ## Log
    - YYYY-MM-DD: <one-line delta>; first entry names the baseline failure (sesslog key) or "none — recurrence only"

Generation (K-a, amended 2026-09-04 — because: the literal
rules+principles+notes set-key could not fire on system work, 24
provenance blocks → 22 distinct keys; see instruction-memory-assessment
§1 and its bundles): the trigger is ACTIVITY SHAPE, in-session — the
same observable outcome recurs in ≥2 prior sesslog blocks from
DIFFERENT sessions (read how:/topics:/the skills: watch parentheticals,
not identical rules= sets) plus the current one; or the user says "make
this a kb skill"; or the ritual's skills pass (5c) finds such a repeat;
or a procedure principle reaches ≥3 helped (meta.md §6). Deferral "to
the ritual" is not a path — the ritual is the backstop.
Compilation (K-b): a skill needs BOTH halves — the rule cluster as SPEC
(every constraint rewritten as a verifiable Check) and ≥2 episodes as
TESTS (the step order actually taken, the branch, what the critics
caught → Anti-steps). A rule alone is imagination; episodes alone are
summary. Body ≤150 lines, ≤3 sub-modules, one exemplar episode; no
observable pass condition → write a principle candidate instead. Draft
from §K's specification (compiler skill only when K-c permits); save `status: unratified`;
add the _index.md row; announce in one line; log `skills: new=[slug]`.
Follow policy (K-c): an `unratified` skill is FOLLOWED only in the
session that generated it, after the user says "use it", or after the
ratifying commit flips it to `active` (the ritual writes the flip);
in any other session it is OFFERED in one line, never followed. Basis:
human-curated skills gained +16.6pp while SELF-generated skills scored
8–12pp BELOW the no-skills baseline without a curation act
[src:arXiv:2602.12670 v4 | method:web | verified:2026-08-29 | conf:H];
the commit IS the curation act. The stricter gate (a logged
baseline→retest before any following) remains available by the user's
choice per skill.
Lifecycle (K-d): every use logs `skills: used=[slug:valence]`; the
ritual reconciles counters into headers and _index.md; a retirement
proposal only at uses ≥5 with net-negative valence (never on one bad
outing); deprecate, never delete; soft cap ~20 active; ≤3 skills loaded
per task; the ritual's Health line reports skill ENGAGEMENT (% of
blocks with skills: used≠none). "drop that skill" deprecates on assent.
Drafts that fail K-a/K-b live in kb/skills-candidates/ and never load.

Use (automatic): at task start scan _index.md `use-when` rows (trigger
vocabulary, rule 3); on match load the skill, announce in one line,
follow Steps, log `skills: used=[slug:valence]` (§B). Divergence from
reality → trust observation, note the delta in the skill's Log.

_index.md — one row per skill, `- <slug>: Use when <situation> (status)`;
≤40 lines (rule 1); regenerated by the ritual from skill headers.


## §J — Project loop and update surface (MVP, 2026-09-07)

Use when starting/resuming project work, deciding a material change, reporting
a deliverable, preparing a release/handoff, or asked what changed/where we are.
Load this section from §W; no skill promotion or evaluation is needed to use it.
This is an experimental procedure, not a claim of measured effectiveness.

Homes: workspace/<slug>/DECISIONS.md and PROJECT.md. Human-facing STATUS.md,
UPDATES.md and CHANGELOG.md live in workspace/<slug>/; for project/system they
live at the repo root. PROJECT links these homes. Other scopes link to them,
never rewrite them. STATUS is an operational view, not another knowledge canon;
kb/INDEX remains the ritual-owned knowledge/focus index. Update STATUS at every
substantive session boundary and after a material ruling; never wait for ritual.

1. Resume: read STATUS plus the last update for THIS scope, PROJECT's load:
   links, open decisions/assumptions, own inbox handoffs and last scope SESSLOG.
   State current phase and next concrete work. Read older history by need.
2. Decide: record only material user choices, not every edit/refactor. Use:
   D-### | date | decision; why:; rejected:; assumptions: A-###; confirm:;
   approval: approved|proposed|deferred|superseded;
   implementation: planned|partial|built|not-applicable;
   verification: not-run|checked (what/date/evidence, never self-certified truth);
   ratification: pending|<commit-ref>; evidence: <source ruling>.
   Deferred entries name reopen:. Planned work names its expected milestone.
   Stale legacy status fields migrate when touched; retain original rulings and
   add supersedes: links. A commit records acceptance, not behavioral correctness.
3. Before substantive work, write material unknowns as A-### with assumed:,
   risk:, settles-when:, state: open|settled|superseded and evidence:.
   Ask at most three optional questions; a written assumption is never permission
   for an irreversible act or an unanswered required approval. Routine reversible
   implementation choices need no decision entry. Unknown thresholds stay disabled.
4. Check changes on request, at a deliverable/handoff, or in ritual step 3c:
   read decisions, relevant artifacts, scoped git log/diff AND status including
   untracked files. Include changed/deleted files and owner edits as context,
   never process foreign dirt or infer authorization from a file count. Optional
   tools/project_inventory.py captures permitted filenames+hashes per Git root.
   Put its baseline outside the scanned scope; never overwrite a prior baseline.
   In no-git folders inspect an explicit scoped file list; label coverage partial.
   Classify: matches, planned, deferred, missing, partial, contradicts, or
   needs-decision. Missing means a promised milestone passed or claimed-built
   artifact is absent; ordinary backlog is planned. A refactor authorized by the
   stated task is not automatically needs-decision. The user confirms disputed
   intent. No permission to revert follows from a detector label.
5. Keep a compact table in the scope's STATUS or update: D/id, finding, evidence,
   next action. Give recurring findings stable IDs and count them as carried,
   not new. No check => not-run, never zero. Evaluation and product metrics are
   deferred for this MVP; raw observations may be retained without scoring.
6. At a declared release/handoff stakes moment, offer ONE explain-back on a
   decision the user needs to control. Opt-in, at most once/session and ten
   minutes; ordinary work proceeds if declined. Ask before supplying the answer;
   compare intent, artifact and explanation, allow the code to be wrong, then
   help close the gap. Record attempted|declined|not-observed plus the action.
   Independent of the learner module; never silently enable spaced repetition.
7. M5 now uses the existing scope/approval-gated Git rules and the harness's
   configured protections. No custom hook, protected: field or file-count N is
   assumed installed. Hooks remain a later explicit choice; distinguish native
   protections from a custom adapter when evaluation resumes.
8. Handback at EVERY substantive session boundary, even without explicit end:
   update STATUS (<=45 lines: as-of/session, version+ratification, phase, built,
   in-progress, blocked/deferred, next, known limits; every item has a pointer).
   Append UPDATES entry U-YYYY-MM-DD.N (<=10 lines: changed and why, checked,
   not-done, next, session link). N is per scope. The §B outcome points to U-id;
   UPDATES points to sesslog#key. Keep detail in the artifact, not three summaries.
   End chat with a short changed/current/next report in the user's language;
   preserve any user-required response format. Do not bury completion in tools.
9. Version handoff: CHANGELOG has one Unreleased section plus dated released
   versions with changes/limits and real commit/tag references supplied by the
   user's release. Until then say working-tree candidate, not released. Each
   session updates Unreleased when behavior changes and links its U-id. Never
   invent a version's ratification or rewrite a historical released entry.
10. Feedback: keep the user's words separately from the assistant's interpretation,
    with source/date/context and permission to share. No invented participant
    responses, automatic upload of private logs, or outreach without a named
    authorized audience. Feedback is input to later decisions, not a score.

This protocol was introduced at the user's build-now/evaluate-later direction.
Its mechanics are described in docs/DEVELOPER-GUIDE.md in the template edition;
the private instance retains the review and implementation evidence separately.
