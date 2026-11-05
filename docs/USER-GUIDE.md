# Extended Mind user guide

This guide describes the pilot working-tree edition. [AGENTS.md](../AGENTS.md)
and [kb/templates.md](../kb/templates.md) govern behavior; version status is in
[CHANGELOG.md](../CHANGELOG.md). Effectiveness has not been evaluated.

## Start with real work

Download a copy into its own folder, open it with your coding agent, and say
`hi`. The assistant asks who you are, what you want help with and your language.
Give it one concrete task. If your project lives elsewhere, name its folder;
the assistant records the access you approve in that project's PROJECT.md.
Your code and documents stay where they already live.

The agent needs file access, a shell and Git. Web access is needed to verify
external claims; without it, those claims remain unverified. Python 3.9 or later
is optional for the five small helpers in `tools/` (inbox routing, file inventory,
coordination records, consolidation and project layout checks); the written
protocol can be followed by hand. No background service is installed.

## Read the EM line

Each answer the assistant gives you ends with a blank line, `---` and one
short line, for example:

`EM · used: PROJECT.md → resumed the draft · found: a stale date → kb/questions.md · changed: STATUS.md · waiting: your commit`

- `used:` what it relied on, and what that did to the answer.
- `found:` something it noticed, and where it put it.
- `changed:` the files it edited.
- `waiting:` the one thing that needs you.

Empty parts are left out. `EM · —` means nothing happened. The line replaces
a chat summary. Helper agents the assistant starts do not write one; only the
answer to you does.

## See where you are

For this system, open [STATUS.md](../STATUS.md). It states the current phase,
what is built, what remains, the next step and known limits. It is refreshed at
each substantive session boundary and after material decisions.

[UPDATES.md](../UPDATES.md) has a short entry for each session: what changed,
why, what was checked, what was not done and where to continue. Each entry
points to its SESSLOG block. [CHANGELOG.md](../CHANGELOG.md) groups behavior
changes under Unreleased until you release an accepted version.

Your other projects have the same three files under `workspace/<project>/`.
Ask “Where are we now?” or “What changed since my last session?” The assistant
loads that scope's current page and updates instead of giving you its full log.
These are operational views; canonical knowledge remains in `kb/`.

## Work across sessions

1. Name the project and the outcome you want. The assistant retrieves its
   current status, recent handoff and relevant decisions.
2. Material choices go into DECISIONS.md with their rationale and a concrete
   way to check implementation. Uncertainties are written as assumptions.
   These records do not authorize actions you have not approved.
3. At a deliverable or on “check project drift,” it compares decisions with
   artifacts, including untracked files in the permitted scope. Planned work
   remains planned; a changed file is not automatically unauthorized work.
4. Each substantive session ends with a brief update and a saved handoff.
   Saying `end` forces this immediately. To switch agents, end here, then open
   the same folder with the next agent and name the project.

Use one working conversation for implementation or testing. Only planning
and research may overlap (two agents, separate reports). The folder is the handoff,
so anything left only in a conversation is not dependable shared context.

## Decide and accept changes

The assistant can draft in the working tree within the scope you granted.
Files therefore change before a commit. Your commit accepts a version; it
does not automatically prove that every assertion or behavior is correct.
The assistant may commit or push after showing you the changes and receiving
your approval for those actions. You can approve both together when the commit
contents and push destination are shown. Changed contents require renewed approval.

Ask for the changed paths and a short explanation, inspect the diff, then approve
the agent to execute the shown actions, or run the commands yourself. Separate project
repositories require separate acceptance steps. Never copy a command that
sweeps unrelated projects into one commit. An Unreleased entry stays Unreleased
until you actually accept and release it; no release tag is invented.

## Plan your day

Tell the assistant what you want on your schedule. It echoes the exact line
for your assent before changing approved tasks. Its suggestions use `[?]` and
do not become your tasks without approval. Only you assign priority.

“What should I do next?” uses your approved schedule first. Due notices appear
when a session opens; they do not imply an installed background reminder.
Say `capture: ...` to leave something for later without sorting it now.

## Maintain the records

Upkeep happens inside your sessions; there is no tidy-up rhythm to keep. Each
handback records what you asked for later and what the assistant learned. When
something waits for you, the EM line says so. Say `pending` to see up to four
items at a time. Reply `y #id` to approve one, `n #id` to decline it, `later #id`
to hide it for 14 days, or `undo #id` / `reopen #id` to change your mind.
Approved edits come with a commit for you to accept, as always.

The helper, `tools/consolidation.py`, starts in shadow mode: it counts and shows,
and drafts nothing. Its switch is `coordination/consolidation.md`. Say
"consolidation off" to stop it. This edition has no drafting step, so
"consolidation on" still behaves like shadow. A new folder reports a deep pass
as due until one has run; the deep pass stays optional.

Say `consolidate` for that deeper pass. It routes captures, checks up to ten
claims when sources are available, files up to two notes with your yes and
reports anything that needs your judgment. Routing is recoverable: a pending
batch stays pending until its destinations and receipt are saved. Source
captures stay in the inbox.

Knowledge claims carry source/method/date/confidence. Model-only claims stay
quarantined; a confident answer is not verification. Skills are proposed from
repeated work. An unratified skill can run only in its generating session,
after your explicit “use it,” or after ratification, as §K specifies.

## Rules at four scopes

Everything that steers the assistant is a rule. Rules differ only in where
they live and when they load:

| Scope | Where it lives | When it loads |
|---|---|---|
| Universal rules | AGENTS.md and the kb/templates.md sections it points to | Every session |
| Project-scoped rules | A project's `constraints:` lines in its PROJECT.md | Sessions in that project |
| Task-scoped rules | The active files in kb/principles/, listed in its `_router.md` | Tasks of a matching type |
| Candidate rules | kb/principles/candidates/ | Never, until you promote one |

Candidate rules never load. To switch one on, say "promote <name>": the
assistant moves the file into kb/principles/, adds its router row and shows
you the commit. To leave one off, do nothing. After 12 weeks unpromoted, a
deep pass may offer to retire a candidate rule as a `pending` item; answer `n`
to keep it. This edition ships five optional candidate rules:
learn-from-others-first, machinery-then-surface, decide-by-trigger,
close-the-loop-first and quality-loop. Each file says what it asks of the
assistant, which task types it needs in the router and where it came from.

The rule library, kb/rules.md, lists rules with their labels. Reading an
entry there applies nothing. Project labels, such as `code` or `money`, say
which new projects inherit a rule. When you create a project, the assistant
proposes its `labels:` line and shows each matching library rule as a
`constraints:` line for your yes. An existing project gets a matching rule only
as a `pending` item. To switch a labelled rule off for one project, decline the
line or ask the assistant to remove it from that project's `constraints:`. To
retire it everywhere, ask the assistant to mark its library entry
`status: retired <date> <why>`.

This edition ships six optional labelled rules. None applies until a project
with its label takes a copy:

| Label | Rule |
|---|---|
| `code` | archive/ is retained evidence, never active source and never executed |
| `outward` | discovery and ranking may run automatically; submission to other people or services never does |
| `money` | the assistant observes, scores and suggests; it never executes a trade, purchase or payment |
| `personal` | personal content stays here; ideas that mature into durable knowledge go to kb/notes/ only through the normal claim and ratification path |
| `casual` | no project machinery, plans or deliverables unless you ask for them |
| `casual` | a thought that grows into real work becomes its own project, not a subfolder |

`python tools/coordination.py rules --labels <label>` lists what a label
brings, and `rules --check` reports drift between the library and its copies.

These are names only. The folder kb/principles/, the `principles:` field and
the `principle:` keyword keep their spellings.

## Ask for a different thinking mode

| Say | What happens |
|---|---|
| `feynman` | You explain; the assistant probes gaps. |
| `socratic` | The assistant uses questions to help you reason. |
| `devil` | It argues a strong opposing case. |
| `review` | Explicitly runs a learning review; routine learning stays on standby. |
| `pending` | Shows up to four items waiting for your yes or no. |
| `consolidate` | Runs the optional deep pass: captures, claims and up to two notes. |
| `boot` | Gives a fuller recovery of the recorded state. |
| `end` | Writes the handoff and update now. |

Before a release or handoff, the pilot may offer one short explain-back on a
decision you need to control. You can decline. An unfamiliar implementation
may be wrong; the exercise is not a test of whether you can repeat its code.

## Privacy and feedback

Your records are local files, but the agent may send what it reads to its
provider under that tool's settings. Git does not encrypt committed contents.
Do not put credentials or private project logs in a public feedback issue.
Mark a project `private: true` in its PROJECT.md to keep its text off other
projects' boot lines, relays and EM lines; they show counts only.
The pilot does not upload feedback automatically.

Use [FEEDBACK.md](../FEEDBACK.md) to report one useful or frustrating moment.
The three prompts are: what you tried, what happened, and what you expected.
You may instead tell the person who invited you; no GitHub account is required
for that private conversation. Formal evaluation is deferred.

## If something goes wrong

- **The agent repeats old work:** ask it to read STATUS, the latest UPDATES
  entry and the last SESSLOG for this scope; point to the missed decision.
- **The current page is stale:** ask for a refresh from the underlying artifacts,
  with uncertainty stated. A summary is not authority to overwrite source work.
- **A deep pass was interrupted:** resume its pending routing batch. Never
  mark it completed just to clear a warning.
- **Your agent ignores the rules:** stop the action and inspect what instruction
  file it loaded. The protocol is not a sandbox or a guaranteed enforcement layer.
- **A field or date is unknown:** leave it unknown; do not substitute a guess.

The Chinese guides are retained from the earlier edition and have not been
resynced for this pilot. English rules and current change records describe
this edition; ask for an explanation in your preferred language.

## Working with several agents

You may run two agents together for planning or research, each saving a separate
report. Pause both passes before one agent implements, tests or integrates the
results. This applies across project scopes too. The current sole worker keeps
the shared project state up to date; no permanent integrator is needed.
You settle disagreements about intent. Pending reports remain available.
The assistant follows [the coordination procedure](../kb/coordination.md).
