# Coordination — small default

Policy: the user serializes work. Applies across projects and harnesses here.
At most two agents may work concurrently, and both must be planning/research.
Implementation, testing, integration, rituals and shared publication run with
ONE working agent; the others pause. Worktrees do not create an exception.

Before writing/resuming, read current LIVE.md and relevant user rulings.
The user's task instruction selects the sole worker; no separate permanent
integrator or per-file ownership allocation is needed. If another worker is
still active or a handoff is unclear, pause conflicting work and clarify.
An empty/expired row alone grants no permission. LIVE is advisory, not a lock.

For solo work, record the interval in LIVE (UUID, task/scope, activity, authority,
active/released, timezone expiry); set Publisher to that UUID for shared writes.
At handback submit/publish, update affected project views and release the row/
clear Publisher. Reuse the interval while actively working; after a completed
handoff start a new one. Archive old rows outside boot load.

Load only the branch needed now:

- Parallel plans/research: [Research](coordination-reference.md#research).
- Session record/shared publication: [Records](coordination-reference.md#records).
- Explicit consolidation: [Ritual](coordination-reference.md#ritual).
- Interrupted write/helper failure: [Recovery](coordination-reference.md#recovery).

Parallel researchers follow Research instead of editing LIVE.
Routine solo work needs no review manifest, integration matrix or separate
acknowledgement file. Keep input revisions for findings another agent integrates.
Preserve approvals, scope boundaries and append-only history (templates §B/§C/§J);
publication does not approve recommendations or Git actions.

The same agent can implement then test sequentially. Parallel research saves
only separate reports/submissions, never shared state or executable changes.
