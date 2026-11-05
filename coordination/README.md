# Coordination records (operational state)

- `sessions/<uuid>/session.json`: immutable identity, task, base and input hashes.
- `sessions/<uuid>/`: that session's own review/output/acknowledgement files.
- `sessions/<uuid>/handoff.json`: immutable §B submission, awaiting publication.
- `windows/`: immutable exact ritual snapshots; first use reconciles history.
- `receipts/`: completed-window membership plus immutable evidence references.
- `publication.lock`: persistent inert file; only an OS-held lock excludes calls.
- `pending-publication.json`: unfinished append journal; preserve for recovery.
- `consolidation.md`: the consolidation control (templates §F); it ships at `state: shadow`.
- `proposals/`: cards, ledger and state the consolidation helper writes; never loaded (rule 3).

Start with [the small policy](../kb/coordination.md). Load only the needed
[reference section](../kb/coordination-reference.md): Research, Records, Ritual or Recovery.
These are versioned operational records, not knowledge canon. Parallel research never
writes shared ledgers; the later sole worker publishes. A submission is not a decision or proof of correctness.
The template contains no real session records or user identities.
