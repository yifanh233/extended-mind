# Rule library    version: 1 | six optional labelled rules ship; yours join them
labels-allowed: all, local, code, outward, money, personal, casual
labels-proposed:
Every consolidated rule, labelled (AGENTS.md rule 10, kb/templates.md §G). Read it
through `python tools/coordination.py rules` or at a rule moment; otherwise grep
it. Reading an entry applies nothing: a rule binds only where its home loads. An
entry with text: is the exact text of a PROJECT.md rule; each PROJECT.md line
tagged [R-###] is a working copy, and on a difference this file wins (rule 1).
An entry without text: is a pointer, never a second copy. Labels all, local and
? are never copied to a new project. Only the user adds a value to
labels-allowed:, by a ruling and a commit. The project labels that ship: code (a
Git-backed code root, layout: dev) · outward (its acts reach other people or
services: applications, filings, submissions) · money (trades, purchases or
payments are possible) · personal (your private records or life content) ·
casual (play or chat; no project machinery unless asked).

Optional rules (R-001 to R-006) ship with the template: text: with
`home: kb/rules.md`. Each binds nowhere until a project with a matching label
carries its tagged copy (§G, §W). To leave one off, never copy it; to drop it
everywhere, retire it.

## R-001
text: archive/ is retained evidence, never active source and never executed
labels: code
when: project
home: kb/rules.md
origin: template
source: shipped with the template (v3.2.0), from the maintainer's own projects
status: active
added: 2026-11-05

## R-002
text: discovery and ranking may run automatically; submission to other people or services never does
labels: outward
when: project
home: kb/rules.md
origin: template
source: shipped with the template (v3.2.0), from the maintainer's own projects
status: active
added: 2026-11-05

## R-003
text: the assistant observes, scores and suggests; it never executes a trade, purchase or payment
labels: money
when: project
home: kb/rules.md
origin: template
source: shipped with the template (v3.2.0), from the maintainer's own projects
status: active
added: 2026-11-05

## R-004
text: personal content stays here; ideas that mature into durable knowledge go to kb/notes/ only through the normal claim and ratification path (rules 5 and 6)
labels: personal
when: project
home: kb/rules.md
origin: template
source: shipped with the template (v3.2.0), from the maintainer's own projects
status: active
added: 2026-11-05

## R-005
text: casual register: no project machinery, plans or deliverables unless the user asks for them
labels: casual
when: project
home: kb/rules.md
origin: template
source: shipped with the template (v3.2.0), from the maintainer's own projects
status: active
added: 2026-11-05

## R-006
text: a thought that grows into real work becomes its own project, not a subfolder here
labels: casual
when: project
home: kb/rules.md
origin: template
source: shipped with the template (v3.2.0), from the maintainer's own projects
status: active
added: 2026-11-05
