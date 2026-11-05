# Coordination reference — read only the triggered section

## Research

At most two agents plan/research at once, with separate output paths. Each may
read relevant sources and save its own report and durable session submission;
neither edits implementation, runs tests/experiments, integrates, publishes shared
logs or changes LIVE while both are working. The user starts the parallel phase;
an already sole worker can record its assignments beforehand. Do not invent an
extra agent or require one to provide a critic check.

Record task, input commit plus hashes for uncommitted inputs, findings, evidence
and open questions in the report/session manifest. The helper's `check` reports
changed inputs; the later sole worker re-reads those that changed. Preserve
IDEA → CRITIQUE → COUNTER with short counters. When integrating, retain both
reports and briefly identify additions, overlap, conflicts and what was kept.
Use a finding table only when helpful; no separate receipt/ack file is required.
Intent conflicts go to the user; agreement is not correctness proof. Surface
pending reports in the next STATUS update. Submitted does not mean integrated,
approved, implemented, checked or committed.

## Records

Use at registration/handback; templates §B supplies the body. From the instance
root (use actual agent, scope and observed base):

```sh
python tools/coordination.py new --agent codex --scope project/example --role integrator --task "Current task" --base <commit-or-unversioned>
python tools/coordination.py submit --session <uuid> --body coordination/sessions/<uuid>/handoff.md
python tools/coordination.py publish --session <uuid> --publisher <current-sole-worker-uuid>
```

`new` generates identity, not permission. For parallel research use `--role
reviewer` and `--input <relevant-file>` per input, then stop after submit. For solo
work inputs are optional; no unrelated-file inventory is needed. The sole worker
records its active row and Publisher in LIVE before shared writes. Put only the
§B body in handoff.md, without a SESSLOG header. The helper preserves authorship,
UUID and source hash, allocates max date/scope N + 1, and deduplicates retries.
An absent publisher leaves a pending submission. At handback release the row and
clear Publisher. No Python: keep a UUID submission; the sole worker may append
once after checking record IDs and preserving fields. State that this fallback
has only procedural protection.

## Consolidation

Load with templates §F on `pending`, a review reply, a control word, or a relay
printed by `submit`. These commands work only where `tools/consolidation.py` is
installed; elsewhere `coordination.py` says so in one line and nothing else
changes. coordination/consolidation.md switches the helper: missing or
unparsable means off, and the narrower of the working file and HEAD applies, so
narrowing works at once and widening needs a commit.

```sh
python tools/coordination.py pending --scope project/example
python tools/coordination.py pending --scope project/example --full --session <uuid>
python tools/coordination.py rule y <id> [<id> ...] --session <uuid> --quote "<the user's reply>"
python tools/coordination.py rules --labels <label,...>
python tools/coordination.py rules --check
```

Add `--interactive` to `new` when the user types in the session. `pending`
without `--session` writes nothing; with `--full --session` it records what was
shown, and `rule` (y, n, later, reopen) accepts only items shown in that same
interactive session, with the user's reply quoted. `rules --labels` prints the
library lines a new project inherits (templates §W); `rules --check` reports
drift and writes nothing. Proposals are moved, never deleted. No Python: where
coordination/proposals/seed.md exists, read its cards by hand; otherwise review
own-scope [?] lines and owed: items; record rulings in decisions:; counts and
date lanes are then lost.

## Ritual

Load only on explicit consolidation with templates §F. Other agents pause.

```sh
python tools/coordination.py window --output coordination/windows/<unique-name>.json
python tools/coordination.py complete --snapshot coordination/windows/<unique-name>.json --evidence workspace/system/ritual-receipts/<unique-name>.md --publisher <current-sole-worker-uuid>
```

A window freezes exact unprocessed blocks, including duplicate legacy keys.
First run has `bootstrap: true`: reconcile historical membership using old
consolidation evidence. Never seed completion from max key/window-end. Finish
the frozen batch and save immutable evidence containing
`coordination-window:<window-id>` before complete; partial work leaves it open.
Later arrivals stay pending regardless of dates. CONSOLIDATED cites the receipt.
A budgeted deep pass, where §F defines one, freezes no window and skips window
and complete; its CONSOLIDATED record lists covered: and partial: instead.
Without Python save exact consumed IDs/hashes and a durable receipt. Receipts
check membership/evidence, not consolidation quality.

## Recovery

On interrupted/failed publication preserve pending-publication.json and retry
the SAME submission with the current authorized publisher. The helper's OS lock
and journal allow completion only when partial bytes match the intended append.
For a busy lock wait for that call to end; never delete the inert lock filename.
Conflicting bytes fail visibly: preserve evidence and reconcile before continuing;
never erase a journal to force progress. Protection covers cooperating local
publication calls, not arbitrary editors, remote replicas, agent admission or
Git. Read helper source/tests only when diagnosing or changing that mechanism.
