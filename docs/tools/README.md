# docs/tools — how the figures are made

The two pictures in `docs/` are generated, not drawn by hand:

| figure | source (typed JSON IR) | outputs |
|---|---|---|
| What happens in one session? | `docs/session.archify.json` | `session.html` (interactive), `session-light.svg`, `session-dark.svg` |
| How does what you say become permanent knowledge? | `docs/architecture.archify.json` | `architecture.html` (interactive, three guided views), `architecture-light.svg`, `architecture-dark.svg` |

Renderer: [archify](https://github.com/tt-a1i/archify) (MIT) — an agent authors the IR, a deterministic
validator + renderer produces a self-contained HTML file. No LLM or network call is involved in rendering.

Regenerate (Node 18+, Python 3; archify cloned next to this repo or pointed at by `ARCHIFY`):

```bash
git clone https://github.com/tt-a1i/archify ../archify          # once
export ARCHIFY=../archify
python docs/tools/archify_autofix.py docs/session.archify.json   # validate at showcase quality; applies label suggestions
node $ARCHIFY/archify/bin/archify.mjs deliver architecture docs/session.archify.json docs/session.html --quality showcase
python docs/tools/build_svgs.py docs/session.html docs/session "What happens in one session?" "<long description>"
```

`build_svgs.py` exists because archify exports SVG only from its viewer: it lifts the `<svg>` out of the
HTML, inlines the viewer's CSS variables for the light and the dark theme, adds an opaque background, a
real `<title>` (the figure's question) and `<desc>` (the walk-through), and strips viewer-only ARIA noise.
GitHub renders the SVGs in Markdown; it shows the HTML files as source, so they are "download and open".

Parity duty: after any rule change (rule 13), re-read the IR labels against `AGENTS.md` and regenerate.
The IR was authored against archify 2.16.0-dev.0 (2026-09).
