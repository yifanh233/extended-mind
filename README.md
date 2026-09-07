# Extended Mind

A plain-text folder that keeps one person in charge of their AI agent across
months: the agent writes, you approve, every claim keeps its source.

**Pilot candidate:** project decisions, assumptions, change checks and session
handoffs are available as an experimental protocol. Their effectiveness has
not been evaluated. Custom hooks and formal evaluation come later.

**Where are we?** [Current state](STATUS.md) · [Session updates](UPDATES.md) ·
[Version changes](CHANGELOG.md). These pages distinguish built, pending and
unchecked work, with links to the detailed records.

**Get your own copy.** Download the prepared pilot ZIP, or use GitHub's
**Code → Download ZIP**, then extract it into a folder of its own outside any
existing project. The assistant initializes your own Git history during setup;
you approve the first acceptance commit; either you or the agent can run it. Your projects stay where they are.

**Then open a session** with your coding agent (Claude Code, Codex,
Cursor, Gemini CLI…) in that folder and say `hi`.
Setup happens in chat; the assistant prepares changes for your review.
(Your projects stay where they already live — you'll just say where.
Optional head start: drop a file or two about yourself into `workspace/`.)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/session-dark.svg">
  <img alt="You talk to an AI agent session; it reads this folder's rules and memory every session, works in your project folders, writes one log block per session, and your approval authorizes the commit that accepts a version." src="docs/session-light.svg" width="100%">
</picture>

*What happens in one session — click to open full size. Rendered from [docs/session.archify.json](docs/session.archify.json) with [archify](https://github.com/tt-a1i/archify) (MIT).*

Four doors:

1. **A thought hit me** → just say it.
2. **What should I do next?** → just ask; your approved schedule answers.
3. **Think this through with me** → just talk.
4. **Make it stick** → say `end`, then paste the two short commit lines it
   hands you, or approve it to run the shown commit and push.

When something it can do would help, it says so in one line — rarely, at
most twice ever about the same thing; say `no tips` to turn that off.
(GUIDE.md has a "Your first week" section for what to expect.)

The rule files stay in English; conversation follows your language. The
[Chinese guide](README.zh.md) is retained from the earlier edition and has not
been resynced for this pilot. Ask for an explanation in your preferred language.

**Try it:** [One real project across sessions](PILOT.md).
**Tell us what happened:** [Three short feedback prompts](FEEDBACK.md).

Want the details? [GUIDE.md](GUIDE.md) is a five-minute read. Your memory
lives here as plain text you can open in any editor — on your machine.

Going deeper? The rest lives in `docs/`: [USER-GUIDE.md](docs/USER-GUIDE.md) is
the reference — every word you can say, every file, and what needs your
approval; [DEVELOPER-GUIDE.md](docs/DEVELOPER-GUIDE.md) explains how it is
designed and built and shows the evidence behind each choice; and the
[architecture map](docs/architecture-light.svg) is one picture of how the pieces
fit (interactive version: download [docs/architecture.html](docs/architecture.html)
and open it locally).
