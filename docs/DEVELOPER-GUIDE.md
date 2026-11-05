# Extended Mind developer guide

This pilot is a plain-text protocol operated by a coding agent, with five
optional Python helpers. It has no server, database or automatic telemetry.
Behavior is specified by [AGENTS.md](../AGENTS.md) and
[kb/templates.md](../kb/templates.md); this guide explains their arrangement.

## Data and responsibility

| Home | Purpose | Writer / acceptance |
|---|---|---|
| `AGENTS.md`, `kb/templates.md` | rules and formats | system scope drafts; human accepts |
| `kb/notes`, `kb/principles`, `kb/skills` | canonical knowledge and procedures | system/ritual scope; commit is the trust gate |
| `kb/rules.md` | rule library: each consolidated rule once, with its labels | interactive system session, with its commit (§G) |
| `coordination/consolidation.md` | consolidation switch: state, budget, scopes | the user's words; widening needs a commit |
| `coordination/proposals/` | cards, ledger and state | `tools/consolidation.py` only; never loaded as knowledge |
| `sesslog.md` | detailed append-only handoff history | each session appends its own block |
| `schedule.md`, `inbox.md` | tasks and captures | schedule assent rules; capture appends |
| `workspace/<slug>/PROJECT.md` | project context, access and loading pointers | owning scope |
| `workspace/<slug>/DECISIONS.md` | material decisions and open assumptions | owning scope records user rulings |
| `STATUS.md`, `UPDATES.md`, `CHANGELOG.md` | system current view, session deltas, versions | system scope updates; real releases need human action |
| `workspace/<slug>/STATUS.md` and siblings | the same surfaces for another project | that project scope |

The work stays in the PROJECT `where:` folders. The assistant receives only
the access stated there and granted by its harness. A project task loads §J;
the knowledge INDEX remains ritual-owned and is not rewritten each session,
except for links the user approves in a pending review.

## The EM line

[AGENTS.md](../AGENTS.md) rule 15 specifies one line at the end of each
top-level interactive answer, after a blank line and `---`:

```text
EM · used: <item> → <effect> · found: <pointer> → <where it went> · changed: <path> · waiting: <one thing>
```

Empty fields are omitted; `EM · —` means nothing happened. The line replaces
the chat summary. It never appears in subagent output, so delegated reports
stay plain. The SESSLOG record (§B) remains the durable handoff; the EM line
is the visible trace of a single answer.

## Consolidation inside sessions

Templates §F replaces the old every-few-days ritual. Each handback record (§B)
carries `owed:` (future work the user stated), `ext:` (whether the session read
outside material), `labels:` (which rules loaded) and any lesson as
`candidate=` with `kind=` and a `proof=` or `quote=`. After `submit` or
`publish`, `tools/coordination.py` calls `tools/consolidation.py`. The helper
reads the log and the control file, counts, and returns one relay line for the
EM line's `waiting:` field. It calls no model and writes only under
`coordination/proposals/`.

```sh
python tools/coordination.py pending --scope project/system
python tools/coordination.py pending --scope project/system --full --session <uuid>
python tools/coordination.py rule y <id> --session <uuid> --quote "<the user's reply>"
python tools/coordination.py pending --stats
```

`pending` without `--session` writes nothing. With `--full --session` in an
interactive session it records which cards were shown, and `rule` accepts only
those, with the user's reply quoted. A `y` approves; the agent then makes the
approved edit and shows the commit, which is the real gate. Cards come from
dates and files: inbox lines older than 14 days, past-due predictions,
unpublished handoffs, projects without `labels:` and library drift.

`coordination/consolidation.md` is the switch. It ships at `state: shadow`: the
helper counts and shows information stubs, and drafts nothing. This edition has
no drafting step, so `state: on` also acts as shadow. A missing or unparsable
file means off, and the narrower of the working file and HEAD applies, so
narrowing works at once and widening needs a commit. The deep pass
(`consolidate`) stays optional and budgeted: at most 10 claims and 2 notes.

## Labels and the rule library

Templates §G gives every rule three labels: reach (where it binds now, derived
from its home), when (the kb/LOAD.md row that loads its home) and project labels
(which new projects inherit it). `kb/rules.md` lists each consolidated rule
once. An entry with `text:` is the exact text of a PROJECT.md `constraints:`
line tagged `[R-###]`; an entry without it points at its home. Reading the
library applies nothing; a rule binds only where its home loads.

```sh
python tools/coordination.py rules --labels <label,...>
python tools/coordination.py rules --check
```

`rules --labels` prints the lines a new project inherits; `rules --check`
reports drift and writes nothing. The library ships six optional rules
(R-001 to R-006) under the project labels code, outward, money, personal and
casual. Their home is `kb/rules.md` itself: each binds nowhere until a project
with a matching label carries its tagged copy, and `rules --check` stays
silent for one that no project copies. Only the user adds project labels, by
a ruling and a commit.

## Project loop

§J connects M1 decisions, M2 assumptions, M3 artifact comparison, M4 an optional
explain-back, M5 existing approval/scope boundaries, M6 the session handback and
M7 retained observations. Custom harness hooks and formal efficacy evaluation
are deferred. The loop is usable now; skill compilation still follows §K.

Decision fields keep approval, implementation, verification and ratification
separate. `planned` is not drift. `missing` requires an unmet promised milestone
or an absent artifact previously claimed as built. Needs-decision findings
are questions about intent, not permission to revert. Stable IDs distinguish
new findings from carried ones. Unrun checks are `not-run`, never zero.

At each boundary, refresh STATUS, append a <=10-line U-entry, update the
Unreleased changelog if behavior changed, and append SESSLOG with the U-id.
STATUS links to current evidence; UPDATES records the delta; SESSLOG keeps the
full handoff. Released changelog entries remain historical. Do not call a
working-tree candidate ratified or published.

## Inspect file changes

`tools/project_inventory.py` uses Git to enumerate tracked and non-ignored
untracked files in explicit permitted paths, then hashes file contents. It
does not modify the work, stage files, interpret decisions or infer permission.
Run one snapshot per Git root; place the baseline outside the scanned scope.

```sh
python tools/project_inventory.py snapshot --root /path/to/work --include src --include README.md --baseline workspace/example/pilot/baseline-01.json
python tools/project_inventory.py changes --root /path/to/work --include src --include README.md --baseline workspace/example/pilot/baseline-01.json
```

The second command reports added, removed and modified paths. The agent then
reads the relevant artifacts and decisions. Ignored files are outside coverage;
permission-sensitive files need a separately approved inspection. Symlinks and
out-of-root paths fail closed. A changing workspace is not a stable snapshot;
use one live writer per scope and rerun if overlap is detected.

## Resume an interrupted inbox route

```sh
python tools/inbox_cursor.py begin --inbox inbox.md
```

This appends a pending routing fence or returns the already-pending window.
It emits a batch ID and source items with stable byte-offset IDs. Write each
item's result into an allowed destination with `inbox:<batch>:<id>` beside it.
Before writing, search for that anchor so replay reuses a previous result.
Captures arriving after the fence are held for the next window, including
captures written before this batch's completion marker.

Save a UTF-8 JSON receipt under `workspace/system/ritual-receipts/`:

```json
{"batch":"<returned-batch>","routes":[{"id":"<returned-item-id>","destination":"workspace/system/ritual-brief.md"}]}
```

```sh
python tools/inbox_cursor.py complete --inbox inbox.md --receipt workspace/system/ritual-receipts/batch-01.json
```

Completion requires one destination per item, saved source anchors, an
unchanged source window and an existing receipt. It appends acknowledgement
after those checks. Repeating completion is harmless; restarting before it
returns the same pending batch. A malformed/torn marker stops for recovery.
Receipt and destination files stay local and retained. Their presence proves
recording, not the semantic correctness of the assistant's routing.

The helpers use Python 3.9+ standard library only. They are not locks, a
transactional filesystem or a security sandbox. §C's one-writer discipline
and the harness's permissions remain necessary. The written fence/receipt
procedure is the fallback if Python is unavailable.

## Check a release candidate

1. Check rule/index line budgets and local Markdown links.
2. Verify parent/template behavior deliberately, preserving template setup.
3. Run helper tests on temporary fixtures: interrupted routing, replay, late
   capture, incomplete receipts, new/untracked work and scoped deletion.
4. Rehearse setup, a real deliverable, human acceptance, fresh-session recovery
   and a second-agent handoff. Record an unrun agent test as unrun.
5. Compare the exact exported files with the prepared template and list the
   changed paths and destination for approval before an agent or human commits/pushes.
   Never publish private logs without approval to share them.

Mechanical checks are release integrity checks, not evidence of adoption or
comprehension improvement. The changelog names what was actually checked.

## Extend and collect feedback

Keep project-specific decisions in their project. Amend a rule only when that
behavior needs to apply at every matching session; put formats in templates
and repeated procedures in skills only under §K's follow policy. When behavior
changes, update the guides and Unreleased entry in the same work session.

[FEEDBACK.md](../FEEDBACK.md) and the issue form ask for concrete experiences;
no statistics are fabricated from them. The issue form follows
[GitHub's documented syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).
The maintainer separates the user's raw words from interpretation, and links
a fix to the feedback that prompted it. Outreach and recruitment are manual.

Design rationale for this pilot: source-first decisions avoid inventing intent;
completion-after-receipt avoids acknowledging unprocessed inbox work; bounded
current views make updates readable without deleting their history. These are
design choices. The public template does not depend on the author's private
research archive or claim measured superiority over another product.

## Task-scoped loading and coordination

Start at [kb/LOAD.md](../kb/LOAD.md); open only matching sections. Keep the small
boot/permission checks, then relevant project context and source. Full grammar,
history, skill bodies and exceptional procedures stay on disk until triggered.
Every system-change critic checks simpler alternatives and added reads, steps
and state (templates §A). No extra critic agent or mandatory report is needed.

Read [LIVE.md](../LIVE.md) before writes/resumes. The user selects the working
window: two agents may plan/research using separate reports, then one agent
implements, tests, integrates and publishes while the others pause. Different
project scopes or worktrees do not permit concurrent implementation/testing.
See [the small policy](../kb/coordination.md) when starting/changing activity.

At registration/handback load only [Records](../kb/coordination-reference.md#records).
The existing helper keeps UUID identity, immutable submissions, retry-safe append
and exact log membership; solo work needs no input inventory or integration matrix.
Publisher identifies the current sole worker, not a permanent role. Its helper
role token remains `integrator` for compatibility. Expiry never grants ownership.

Load [Research](../kb/coordination-reference.md#research) only for parallel passes,
[Ritual](../kb/coordination-reference.md#ritual) only on consolidation, and
[Recovery](../kb/coordination-reference.md#recovery) only for a failed/interrupted
publication. The first ritual still reconciles historical membership explicitly.
The helper protects cooperating local publication calls; LIVE cannot stop an
arbitrary editor. User approval of shown changes/actions remains the Git gate.
