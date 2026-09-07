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
is optional for the two small inspection/routing helpers; the written protocol
can be followed by hand. No background service is installed.

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

One live conversation per project at a time. Different project scopes can run
in parallel, subject to their file permissions. The folder is the handoff,
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

Say `consolidate` when you want the maintenance ritual. It routes captures,
checks claims when sources are available, reconciles decisions, updates the
knowledge index and presents items requiring your judgment. Routing is
recoverable: a pending window remains pending until its destinations and
receipt are saved. Source captures stay in the inbox.

Knowledge claims carry source/method/date/confidence. Model-only claims stay
quarantined; a confident answer is not verification. Skills are proposed from
repeated work. An unratified skill can run only in its generating session,
after your explicit “use it,” or after ratification, as §K specifies.

## Ask for a different thinking mode

| Say | What happens |
|---|---|
| `feynman` | You explain; the assistant probes gaps. |
| `socratic` | The assistant uses questions to help you reason. |
| `devil` | It argues a strong opposing case. |
| `review` | Explicitly runs a learning review; routine learning stays on standby. |
| `boot` | Gives a fuller recovery of the recorded state. |
| `end` | Writes the handoff and update now. |

Before a release or handoff, the pilot may offer one short explain-back on a
decision you need to control. You can decline. An unfamiliar implementation
may be wrong; the exercise is not a test of whether you can repeat its code.

## Privacy and feedback

Your records are local files, but the agent may send what it reads to its
provider under that tool's settings. Git does not encrypt committed contents.
Do not put credentials or private project logs in a public feedback issue.
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
- **A ritual was interrupted:** resume its pending routing batch. Never mark
  it completed just to clear a warning.
- **Your agent ignores the rules:** stop the action and inspect what instruction
  file it loaded. The protocol is not a sandbox or a guaranteed enforcement layer.
- **A field or date is unknown:** leave it unknown; do not substitute a guess.

The Chinese guides are retained from the earlier edition and have not been
resynced for this pilot. English rules and current change records describe
this edition; ask for an explanation in your preferred language.
