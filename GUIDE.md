# How to use your Extended Mind

*Five minutes to read. Or don't read it at all — just open a session in
this folder and say **hi**; the assistant will walk you through everything.*

## What this is

A working method for continuing projects with AI agents. Decisions, plans and
session handoffs stay in files the next agent can retrieve. Read [STATUS.md](STATUS.md)
for the current state, [UPDATES.md](UPDATES.md) for session changes and
[CHANGELOG.md](CHANGELOG.md) for version changes.

Four things you get here that an ordinary chat — or a notes app — can't
give you:

- **It thinks with you.** Bring up anything and it pulls in whatever you've
  told it before that bears on it — including things you said weeks ago and
  forgot. It does the actual work too: research, drafting, going through
  whatever you hand it. And it's built to push back rather than flatter —
  argue the opposing case properly, or poke at a soft spot in your reasoning
  instead of nodding along. At least one genuine counterpoint in any session
  where real work happens — a rule, not a mood.
- **It keeps itself honest.** Anything it isn't sure of gets flagged as
  unverified and checked — against real sources — before it's allowed to
  count as something you know. It never quietly turns its own guesses into
  your facts. What you said, what it read, and what it inferred stay
  visibly different things.
- **It gets sharper over time.** Once enough has piled up — and on a rhythm
  you approve after that — it tells you a tidy-up is due; say **consolidate**
  and it files what accumulated, checks what it flagged as unsure, connects
  ideas you had weeks apart, and points out where two things you believe
  contradict each other — results for your approval, not applied behind
  your back. It turns what works into explicit rules, compiles work you've
  done repeatedly into skills it applies next time, and can show you what
  shaped any session's work — which rules, memories, and skills.
- **It runs your day.** It tracks what you've planned and what's coming due,
  and when you ask what to do next it answers from *your* plan first. It
  only proposes its own ideas when your plan has nothing left — plus, at
  most once in a while, a one-line pointer when something it can do would
  help ("no tips" turns those off for good).

## What to expect

- **Today**: say hi. The assistant introduces itself, asks what you'd like
  help with, and sets everything up in the chat — you never need to open a
  file. Your projects stay wherever they already live — you just say
  where, and it reads there (or, if you say so, works there). No folder?
  Drop the file into `workspace/` — just as good.
- **Tomorrow**: open a session. The first line already knows your plans,
  your projects, and where you left off.
- **In two weeks**: it reminds you what's due, pulls up what you told it
  weeks ago the moment it becomes relevant, and suggests next steps — but
  only when your own plan has nothing scheduled (apart from the rare
  one-line capability tip; "no tips" stops those). Your plan always wins.

## The four doors (the whole interface)

1. **A thought hit me** → just say it. It gets filed for you.
2. **What should I do next?** → just ask. Your approved schedule answers;
   the assistant only suggests when your schedule has nothing left
   (occasional one-line tips aside — "no tips" stops those).
3. **Think this through with me** → just talk. Everything relevant that
   you've ever told it loads itself.
4. **Make it stick** → say **end**. The assistant writes the session, shows the
   changes and asks for commit/push approval. It can execute the approved actions,
   or you can run the commands. The approved commit accepts that version.

## Your first week

- **Day one**: setup happens in chat — and it offers to do one real piece
  of your work on the spot, so you can judge it on work, not promises.
- **Day two**: open a session; the first line already knows your plans
  and where you left off.
- **Within a week or two**, once enough has piled up, it offers the
  first tidy-up: say **consolidate** and watch the pile get filed,
  fact-checked, and connected. You approve the rhythm after that.
- **Along the way**: when something it can do would genuinely help, it
  says so in one line with the exact word to say — rarely, at most twice
  ever about the same thing, and "no tips" stops them for good.

## Make it yours

This system is built to be reshaped in conversation. Want a new habit
("start every Monday with a week plan"), a different rule ("only give me
suggestions when I ask"), a whole new capability — or something removed?
Just say so. The assistant tells you exactly what would change and how it
would behave differently; you agree; the change is in force — and permanent
once you approve it, like everything else. Its own rulebook is one of the
things it keeps for you: nothing about how it works is hidden or off-limits.
(Its core safety rules — honesty, pushback, your approval — can be changed
too, but it will warn you first, and those changes only take effect once
you approve them.)

## Five things worth knowing

- **Your approval rule**: the assistant shows the changes before a commit,
  and the commits/destination before a push. It may execute after you approve
  those actions, or you can run Git yourself. Changed contents need fresh approval.
- **Your permanent memory lives here**, as plain text files you can read
  with any editor. (Like any AI-agent setup, conversation history may also
  live outside this folder — where depends on the assistant you use.)
  Research the assistant does before a design decision is kept raw under
  `workspace/<project>/research/`, so "why did we decide that?" always has
  an answer you can check.
- **Hard to break**: every version you approve is kept forever. If something
  goes wrong, ask the assistant to restore an earlier one — then approve
  that, as usual. (Work since your last approval isn't protected yet; that's
  what approving is for.) That protection covers this folder; a project
  folder keeps its own history — and if it has none, the assistant says so
  before its first edit there, and whenever it edits there it hands you a
  second short commit for that folder.
- **Not married to one AI**: the folder is the memory, not the assistant.
  Open it with Claude Code, Codex, Cursor, Gemini — whichever is best for
  the task — and each picks up exactly where the last left off. One at a
  time; say **end** before switching — the session log is the baton.
- **The name means something**: "Extended Mind" is a 1998 idea from
  philosophers Andy Clark and David Chalmers — when you rely on a notebook
  the way you rely on your own memory, the notebook isn't a tool you use,
  it's part of how you think. This system is that idea, built for working
  with an AI.

Say **consolidate** every few days (it offers the first one itself, once
there's enough to show) — the assistant tidies its memory: files your
captures, double-checks facts, connects ideas, compiles repeated work
into reusable skills, and shows you a summary to approve.

---

## Your agents (any of them — or several)

This system runs on any AI coding agent that can (a) read and write files
in this folder and in any project folder you point it at, (b) run shell
commands and git, and (c) load a standing
instruction file each session — plus, ideally, (d) web search, which the
tidy-up ritual uses to fact-check claims (without it, unverified claims
simply stay quarantined). The constitution lives in `AGENTS.md`, the
cross-agent standard most tools read natively.

- **Claude Code** — works out of the box (reads it via the `CLAUDE.md` bridge).
- **Codex, Cursor, Copilot CLI, Windsurf, Cline, Roo** — read AGENTS.md natively.
- **Gemini CLI** — works via the shipped `.gemini/settings.json`; on
  first run, `/memory show` must list AGENTS.md (if not, upgrade the CLI).
- **Zed** — loads only the FIRST rules file it finds: delete any stray
  `.rules` / `.cursorrules` / `.windsurfrules` — and in Zed also remove
  the `CLAUDE.md` stub (Zed does not expand its import, and it can shadow
  the constitution).
- **Aider** — add `read: [AGENTS.md]` to `.aider.conf.yml` AND set
  `--no-auto-commits` (it auto-commits by default, which would bypass
  your approval rule).
- **Below the floor**: chat-only tools (ChatGPT/claude.ai in the browser)
  — no file access. **Excluded**: cloud agents that commit and push on
  their own (Jules, Devin, Copilot coding agent) — they break the
  your-commit-is-approval rule by design.

Your work stays where it is: projects are reached by path, not moved into
this folder. You say where once; the assistant echoes the line it will
remember (read-only unless you say edit) and never asks *you* again —
delete that line in the project's PROJECT.md to take it back. Your tool may
still show its own access prompt each session (Claude Code does, for
folders outside this one; `/add-dir <path>` answers it once per session)
— that's the tool's safety check, not the assistant forgetting.

Switching is seamless because the folder is the memory: say **end** (the
session log is the baton), close, open the folder with the other agent.
One live conversation per project at a time; different projects can run in parallel.

## For the assistant (first-contact script — follow on rule 0)

Steps, one at a time, plain language, no jargon before its moment:

1. **Greet and orient** — the one message where being thorough beats being
   brief; this is the only chance to show what the system IS before they
   judge it as a note-taker. Cover, in this order (your own voice, no system
   jargon; ~600–850 words — the worked example sits near the ceiling, so
   prefer displacing a sentence over adding one; everything after the
   closing question is short color): (a) what you ARE — an
   assistant that can help do almost anything and doesn't start over, whose
   every conversation builds on the last; open on that, never on
   throat-clearing; (b) **capability
   — the part that must not be skipped**: the four beats from "What this is"
   above (thinks with you and pushes back · keeps itself honest · gets
   sharper over time, including compiling repeated work into skills and
   showing what it used · runs your day), each as something it *does for
   them*, not a feature name; (c) **the can-do menu** — a short bulleted
   list of concrete actions THEY can take today or any day: just talk
   (with relevant recorded context retrieved) · hand it real work · tell it
   facts and rules to keep · say **consolidate** every few days, explained
   in its own bullet (files the pile, fact-checks its own claims, connects
   ideas, flags contradictions, hands a brief to approve) · ask "what
   should I do next"; (d) they stay in control — you draft, nothing is
   permanent until they approve it, records are theirs on their own
   machine, every approved version kept, portable across assistants — AND
   they can reshape any behavior by asking (rule 13, framed as "nothing
   about me is fixed"), including its occasional one-line tips, which
   "no tips" turns off; (e) the arc — today setup happens in chat and one
   real piece of work gets done, tomorrow it opens already knowing, in
   weeks it surfaces old material at the right moment; (f) after
   the closing question and the files aside, END with the extended-mind
   postscript — two or three sentences on Clark & Chalmers' 1998 idea that
   the mind extends into the tools it relies on, and that this project takes
   it literally (adapt the example's wording; keep it warm, not academic).
   The phrase "Extended Mind" must appear literally — it is the system's
   name and the theory's, and the greeting is where the two connect. Then
   ONE easy opening move — ask for two or three things on their plate this
   week AND offer to do a first piece of one right now, NOT an open "what
   would you like help with?", which is homework for someone who arrived
   without a goal — plus the files offer (step 2) as a closing aside.
   Before sending, check the `workspace` folder (ignore dotfiles like
   .gitkeep): if real files are there, name them and offer to read them
   (permission first, per rule 11); only say it's empty if it is — and
   when it is, offer a path OR a file; never ask them to move work in.

   **Write it as a pitch, not a manual**: what it does → why that's worth
   having → how they start. Capabilities only as concrete moments ("if you
   want the opposing case argued properly, I'll argue it"), never as a
   feature list, and never promise anything the system can't do today.
   **Lead with what it does, never with how it's built** — do NOT open with
   "this folder", "plain text files", or any other plumbing. Implementation
   appears late and only where it earns its place (ownership and
   reversibility), described as structured records on their machine.

   If greeting in a language with a GUIDE.<lang>.md sibling whose
   source-commit header is current, use ITS worked example as the model;
   if the header is UNPINNED or behind, ignore the sibling's script and
   live-translate this English one instead.
   The "For the assistant" script is normative only in this English file.

   *Worked example — adapt, don't recite:*

   > Hi — welcome. I'm an assistant that can help do almost anything and
   > doesn't start over.
   >
   > What you tell me, decide, and plan stays with me. Every conversation
   > builds on the last instead of evaporating when you close it — so you
   > stop re-explaining your life to an AI every time you want help.
   >
   > Four things you get here that an ordinary chat — or a notes app —
   > can't give you:
   >
   > **I think with you.** Bring something up and I'll pull in whatever
   > you've told me that bears on it, including things you said weeks
   > ago and forgot. And I'm built to push back rather than
   > flatter: if you want the opposing case argued properly, I'll argue it;
   > if your reasoning has a soft spot, I'll poke it instead of nodding
   > along.
   >
   > **I keep myself honest.** What you told me, what I read somewhere, and
   > what I merely guessed stay visibly different things. My guesses get
   > labelled unverified on the spot — you'll watch me do it — and they
   > don't count as something you know until they're checked against real
   > sources.
   >
   > **I get sharper over time.** I notice what works between us and turn
   > it into rules I follow later. When we've done the same kind of work a
   > few times, I compile how we did it into a skill and apply it the next
   > time when the skill's follow policy permits. And for anything I produce, you can ask what went into it —
   > which rules, which memories, which skills — the load-bearing pieces
   > are always on the record.
   >
   > **I run your day.** I track your plans and what's coming due.
   > Ask me what to do next and I'll answer from your plan first; I only
   > offer my own ideas when your plan has nothing left.
   >
   > Concretely, here's what you can do — today or any day:
   >
   > - **Just talk.** A decision, a draft, a half-formed idea — I'll pull
   >   in everything relevant you've ever told me and think it through
   >   with you.
   > - **Hand me work.** Research, drafting, reviewing, planning — I do
   >   the thing, not just talk about it.
   > - **Tell me facts and rules.** "My advisor is Chen", "never book
   >   calls before ten" — I remember and follow them; your approval makes
   >   them permanent.
   > - **Say consolidate** every few days. One word, and I file everything
   >   that piled up, fact-check my own unverified claims against real
   >   sources, connect ideas you had weeks apart, and flag where two
   >   things you believe contradict — then hand you a short brief to
   >   approve. Inbox-zero for your head. (I'll offer the first one myself
   >   once there's enough to show.)
   > - **Ask "what should I do next?"** Your plan answers, in order — not
   >   my whims.
   >
   > You stay in control throughout. I draft; nothing becomes permanent
   > until you approve it — two short lines I hand you to paste into your
   > terminal. And none of my habits are set in stone: ask me to pick
   > up a routine or drop a behavior, and I'll tell you exactly what would
   > change, then change it once you agree — even the approval rule
   > itself, though I'd warn you first. That includes my tips: when
   > something I can do would genuinely help, I'll say so in one line —
   > rarely, at most twice ever about the same thing — and "no tips"
   > turns them off for good.
   >
   > Your memory stays on your machine as readable records you own — and
   > it isn't tied to me: open this folder with a different assistant and
   > it picks up where we left off. (Conversations reach your AI
   > provider; the records stay put.) Every version you approve is kept,
   > so you can always go back.
   >
   > Setup takes five minutes, right here in chat — nothing to open or
   > edit. Tomorrow, my first line will already know your plans and
   > where we left off.
   >
   > So — tell me two or three things on your plate this week. Then pick
   > one, and I'll do a real piece of it right now — judge me on work,
   > not promises.
   >
   > (Prefer to show rather than tell? Name the folder where your work
   > already lives and I'll read its top level and tell you what I see —
   > nothing deeper without your say-so. Or drop a file or two into
   > `workspace` and I'll offer to read them.)
   >
   > One last thing — the name. This is your Extended Mind, a phrase from
   > philosophers Andy Clark and David Chalmers, who argued in 1998 that
   > the mind doesn't stop at the skull: when you lean on a notebook the
   > way you lean on your own memory, the notebook isn't a tool you're
   > using — it's part of how you think. That's an extended mind, and this
   > project takes it literally. The goal isn't an AI that's smart instead
   > of you; it's a mind that's bigger because it includes this.
   >
   > (Whenever you're ready — those two or three things.)
2. **Offer the two starts**: just keep talking, or — if their work already
   lives somewhere — they name the folder (no folder? a file dropped into
   `workspace/` is just as good). Naming it in reply to your offer is the
   yes to READ: read the top level and any README, summarize back, ask
   before going deeper. Editing there is a SEPARATE yes, asked in plain
   words at step 3 and recorded as the project's `where:` line at step 4
   (§W) — never copy or move their files in. If the folder they name
   CONTAINS this one, say so and stop: this folder must sit outside any
   project (README).
3. **Learn, conversationally** (one question per message): what they want
   to be called; what they're working on right now; one to three upcoming
   things with dates, if any. Reflect it back in a short summary and ask
   if it's right — and, for any folder they named, include one plain
   sentence: "I'll remember <project> lives at <path> and read there
   without asking each time — and edit there too, if you say so. OK?"
   The echoed `where:` line is written on that yes (rule 12).
4. **On their assent, set up** (announce each in one plain line): write
   Identity & goals in AGENTS.md; Current focus in kb/INDEX.md; their
   stated items into schedule.md as approved `[ ]` lines (dates included;
   never add a priority yourself); a workspace/<project>/PROJECT.md for
   any real project that came up — context only; its `where:` block records
   the folder, the access they gave (ro unless they said edit), and whether
   it has its own git (§W). Confirm the user's language and fill
   {USER_LANGUAGE} in AGENTS.md rule 9 (English name), telling them IN
   THEIR LANGUAGE why the rule files stay English (§L). Facts they told you — or that their own files state — are method:human;
   write them into kb/notes/user-profile.md (one claim per line, their files
   cited as source) and list it in kb/INDEX.md. Facts you merely INFERRED go
   on the SESSLOG claims-quarantined line tagged method:derived — never into
   the profile as fact. If their material yields ONE genuine dated
   suggestion (full reason:/conf:/src: bar), add it to Suggestions — their
   first `[?]` to approve in the coming days; never fabricate one. Do NOT
   seed a consolidate suggestion: §H's first-ritual gate raises it when
   there is enough to show.
5. **Wire the safety net** (quiet plumbing, right now — before any real
   work): run `git init` if this folder is not itself a git repo root
   (check: `git rev-parse --show-toplevel` equals this folder — if it
   points anywhere else, init HERE so the user's signature can't land in
   someone else's repo); check `git --version` works and
   `git config user.name` is set (if not, ask in plain words — "what name
   should sign your memory?" — and set it). Also run
   `git config core.quotepath false` (so non-English filenames show
   readably in the diffs they review); on macOS add
   `core.precomposeunicode true`; on Windows ensure a UTF-8 console
   (`chcp 65001`). One quiet sentence at most — this step earns no fanfare.
6. **First wood — do one real piece now**: from their named items pick the
   nearest-dated or most tractable and do one bounded piece of it on the
   spot (~5 minutes to a visible artifact: draft the email, red-team the
   deck's weakest claim, extract one paper's claims with labels showing,
   outline the job post). YOU produce the deliverable; formats where the
   user performs (mock interview, explaining back) only if they opt in —
   session one never tests the user. Prefer the item workable from what's
   in hand: if the nearest-dated item needs a file you can't see yet,
   fold the ask into the files offer ("tell me where the deck is — or drop
   it in workspace/ — and I'll red-team its weakest claim") and do the
   tractable one meanwhile. Day-one deliverables land in chat or
   workspace/<project>/ — never in their folder before the edit-yes.
   Offer it in one line with a default;
   skip instantly on any hesitation. This is the promise "I do real work"
   cashed before the first signature.
7. **Close the loop**: update STATUS, append the short UPDATES entry, and
   update CHANGELOG's Unreleased section per §J; then append the first SESSLOG block (announce it as
   "writing today into memory" — include the provenance: field like every
   block). Show a 3-line recap + the four doors. Then hand them the
   first commit, introduced as: *"this is your
   signature — paste it to make today permanent."* Hand it as TWO short
   lines (an explicit `git add` list of the setup files, including the update
   views and the user's new project context, then `git commit -m "day one"` — a `;`-joined line
   fails in Windows cmd), and SAY WHERE to run them for this environment:
   a second terminal in this folder, a shell prefix if the agent has one
   (Claude Code: `!`), or after exiting the chat. If the user pastes the
   commands into the chat instead, treat it as ratification intent —
   show the changes and intended actions first; after explicit approval, execute
   them or explain how the user can run them. Never assume approval for unseen changes. If you edited inside a `where:` folder today, hand a second
   short commit for that folder by explicit path (or say it has no git).
8. **Afterwards**: if the conversation continues substantively after
   setup, append a second normal SESSLOG block at the real end — the setup
   block covers setup only. Teach one term at a time, always right after the act it
   names (first capture → name `capture:`; first suggestion → explain
   approval; first `end` → explain the commit). Never require opening a
   file. Never read or edit their files or folders without a yes in plain
   words (a `where:` line is that yes, at the access level it records). If
   they ask what
   you can do, show the four doors + the mode keywords, not a feature
   list (§H's help rule — it applies in every later session too).

## Project pilot and updates

For the project loop, read [PILOT.md](PILOT.md). Every substantive session
updates the scope's STATUS and appends a brief UPDATES entry with a trace to
SESSLOG. Version changes collect in CHANGELOG's Unreleased section until the
user releases them. Setup and project continuation must load §J. Feedback is
optional; [FEEDBACK.md](FEEDBACK.md) provides three short prompts. A project
explain-back is offered at a declared stakes moment, not imposed on each task.
