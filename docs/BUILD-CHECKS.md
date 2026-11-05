# Release checks — v3.2.0, 2026-11-05 (rules v3.2, parts 1 and 2)

These are engineering checks, not effectiveness evaluation. Part 1 adds the EM
line (rule 15) and the rule 6 sentence on tool output, fixes claims that were
already stale, and re-renders both pictures. Part 2 adds consolidation inside
sessions, the `pending` review, rule labels with a rule library, the
consolidation helper in shadow mode, and a re-rendered architecture picture.

- Release check: `python -B workspace/system/tools/check_pilot_release.py
  --check-only` exits 0 with no issues. AGENTS.md has 120 lines in both
  editions; STATUS 22 of 45, INDEX 45 of 80, LOAD 30 of 40.
- The same check on the part 1 content fails with 23 issues: the missing helper
  copy, six missing part 2 tokens, fifteen stale claims and the mode table.
  The stale claims are the helper counts in both guides, the tidy-up rhythm in
  GUIDE.md, the quarantine copy in rule 6, the first-ritual gate, the seeded
  `rec:4d` line, the §G stub, and two old architecture labels in each of the
  four figure files. Part 1's version of the check failed with 10 issues on
  the template before part 1.
- Planted faults trip each new check: a private project name in the helper
  copy, a local path in GUIDE.md and a ledger file under
  coordination/proposals/ (a README there is allowed).
- Parity: §B, §C and §J, kb/LOAD.md, kb/coordination.md,
  kb/coordination-reference.md and the four helper copies, now including
  tools/consolidation.py, match the maintainer's instance. Local links pass in
  15 docs.
- v3.2.0 adds five optional candidate rules, which the check requires to keep
  their candidate header and stay out of the router, and six optional labelled
  rules, which must pass the template helper's own `rules --check` with nothing
  printed. The privacy pattern also covers the maintainer's project names, and
  the file list comes from `git ls-files`, so untracked copies stay out of the
  manifest. The release ZIP is built with `git archive` from the published
  commit.
- 70 Python tests passed on Windows / Python 3.9.13: coordination 18,
  consolidation 40, dedupe 3, pilot 9. The new one covers an optional rule
  homed in the library: silent until a project copies it, then checked.
- Helper smoke test in a throwaway, git-initialised copy of this folder with
  one test record: `pending --scope project/system` printed
  `EM · shadow: control changed: shadow · owed 1 · deep pass due (last CONSOLIDATED none)`,
  and `rules --check` printed nothing and exited 0.
- Scope probe in a second throwaway copy, with one project folder and one ripe
  lesson each from project/system and from that project: both lessons were
  counted, and a submit from a project/system session printed
  `would stage #<id>`. The same probe on the earlier helper counted only the
  project's lesson.
- Pictures: archify v2.16.0 (commit c826e6c3a7abad19c0f3cd1ca57207d54b1ad8de),
  now pinned in docs/tools/README.md. For the architecture picture the autofix
  validator needed 0 rounds, and deliver passed 9/9 artifact checks and the
  showcase profile. Every IR label, sublabel and edge label appears in both
  SVGs. Both architecture SVGs, and architecture.html on the full diagram and
  on each of its three guided views, were screenshotted in headless Chrome and
  looked at, light and dark. The session picture is unchanged since part 1.

Session `<desc>`, as passed to build_svgs.py:

> You talk to an AI agent session in natural language. At the start of every
> session the agent loads AGENTS.md, the rule file, with the kb/LOAD.md
> router, and reads your memory files: notes, the session log, the plan and
> the inbox. It works in your project folders, which stay where they are and
> are named by where: lines. During the session it appends one log block and
> proposes plan items marked [?]. It ends each answer with the EM line: what
> it used, what it found, what it changed and what waits on you. Nothing
> becomes permanent until you approve a commit, whoever executes it, which
> ratifies this folder.

README picture alt text:

> You talk to an AI agent session; it reads this folder's rules and memory
> every session, works in your project folders, writes one log block per
> session and ends each answer with the EM line; your approval authorizes the
> commit that accepts a version.

Architecture `<desc>`, as passed to build_svgs.py:

> You talk to an AI agent session. AGENTS.md, the rule file, loads at the start
> of every session and tells the agent to consult the router in kb/principles.
> The agent proposes [?] items into schedule.md and inbox.md, appends one block
> to sesslog.md, and works in your project folders, which are named by where:
> lines. After each handback the consolidation helper reads the log and relays
> what waits for you. When you say pending and answer y or n, approved items
> become notes in kb/notes and INDEX, principle candidates, or labelled rules in
> kb/rules.md; repeated integrations become skill drafts in kb/skills. Your
> approval of a shown commit ratifies this folder, whoever runs it.

- The check reads two files the maintainer's repository does not track: the
  instance's kb/skills/_index.md and this folder's README.zh.md. Unchanged
  copies sat in the build clone; a clean checkout fails the check without them.
- Helper limits seen in the smoke test: a new folder reports a deep pass as due
  until one has run, and the notice "control changed: shadow" repeats until a
  first `pending` review shows it.
- Names (rules at every scope): the rule files and guides call the former
  principles task-scoped rules. The architecture picture was not re-rendered
  for this rename: its legend still says "principles judge", and its `<desc>`
  above still says "principle candidates".
- Not run: a fresh-agent rehearsal (say hi, one task, end) or an outside-user
  pilot. The consolidation helper was not exercised by a real agent session.
- Not measured: comprehension, usefulness, time saved, adoption, the EM line's
  token cost per answer, or how often pending items are reviewed.
- No custom hook, daemon, automatic feedback upload or Git publication installed.
  Chinese documents remain frozen: they lack the EM line, still describe the
  old tidy-up and may differ from the English candidate.

This describes release v3.2.0. See [version state](../CHANGELOG.md).
