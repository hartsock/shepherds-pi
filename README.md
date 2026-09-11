# Shepherd's Pi

<p align="center">
  <img src="assets/logo.png" width="220" alt="Shepherd's Pi logo — a pi symbol shepherding three sheep inside a circular badge">
</p>

## Combine Herdr and Pi

Like peanut butter and chocolate, herdr and pi are two great tastes that
taste great together. Herdr gives you the multiplexed panes and the
socket API to drive them; pi gives you a small, fast, model-agnostic agent
to put in each pane. A herdr tab full of idle `pi` panes is a flock — ready
for a shepherding agent to dispatch work into.

A skills repo, in the style of [ponytail](https://github.com/DietrichGebert/ponytail):
plain-text instructions for standing up a **[herdr](https://herdr.dev)**
workspace, wiring **[pi](https://github.com/earendil-works/pi)** to an
inference backend of your choice, and raising a flock of idle helper panes
ready for another agent to shepherd. Bring your own backend, your own
model, your own repo.

![Codex shepherding two pi agents through parallel reviews in Herdr](assets/shepherd-demo.gif)

*Codex dispatches two pi helpers and reads their progress. Recorded at 2.5× speed.*

## What is Herdr?

Super TMUX. As in Terminal Multiplexer. You have one terminal with many
sub-terminals "multiplexed" together — an MCP server (and CLI) that agents
can use to pilot multiple shell programs: split panes, launch commands,
read output, wait for output, rename and label panes, all scriptable.
[github.com/herdrdev/herdr](https://github.com/herdrdev/herdr)

## What is Pi?

A minimalist agentic coding harness — [Pi Coding Agent](https://github.com/earendil-works/pi).
It is so minimal it is actually hard for a human to use. That minimalism
reduces distractions for the LLM inside it and makes it subtly more
effective: fewer built-in opinions, less ceremony, a smaller surface to
get confused by.

## In this repo

**Setup — get pi and herdr running:**

| Skill | What it does |
|---|---|
| [`skills/pi-install`](skills/pi-install/SKILL.md) | Install `pi` and confirm it runs |
| [`skills/pi-inference-backend`](skills/pi-inference-backend/SKILL.md) | Point `pi` at any OpenAI-compatible inference endpoint and set a model as the CLI-wide default |
| [`skills/herdr`](skills/herdr/SKILL.md) | The herdr CLI itself — workspaces, tabs, panes, and agent control, straight from the tool's own authority (`herdr --help`) |
| [`skills/herdr-helpers-tab`](skills/herdr-helpers-tab/SKILL.md) | Recreate a herdr tab with a controller pane plus N idle `pi` panes, ready for another agent to dispatch into |
| [`skills/tmux-drive`](skills/tmux-drive/SKILL.md) | Drive an interactive TTY/TUI program hands-free from a non-interactive agent, on an isolated tmux server |

**Shepherd guidance: brief pi helpers, inspect their work, and steer corrections.**

These skills are for the controlling agent. Send each helper a focused brief
with the relevant guidance, then check its artifacts and evidence. See
[Guiding pi helpers](docs/shepherding.md) for the dispatch and review loop.

| Skill | What it does |
|---|---|
| [`skills/tdd-red-green-blue`](skills/tdd-red-green-blue/SKILL.md) | Guide pi through Red, Green, and Blue; verify test evidence and correct drift |
| [`skills/functional-cohesion`](skills/functional-cohesion/SKILL.md) | Supporting doctrine: group code by job and expose a narrow interface |
| [`skills/three-cs`](skills/three-cs/SKILL.md) | Guide pi to separate domain data from mechanisms without speculative frameworks |
| [`skills/unix-philosophy`](skills/unix-philosophy/SKILL.md) | Brief a single tool contract and verify pi's output composes with its consumer |
| [`skills/concision`](skills/concision/SKILL.md) | Brief pi on audience and purpose; review its draft for clarity without losing meaning |

Deeper reference material that doesn't belong inline in a skill lives in
[`docs/`](docs/):

- [`docs/shepherding.md`](docs/shepherding.md) — how the shepherd assigns,
  checks, and corrects pi work; each shepherd skill links its longer doctrine
- [`docs/pi-config-reference.md`](docs/pi-config-reference.md) — `pi`'s
  three config files (`models.json`, `settings.json`, `auth.json`) and how
  they interact
- [`docs/installing.md`](docs/installing.md) — per-agent skill install
  commands (Claude Code, Codex, pi, and a generic fallback)

## Installing the skills

Each skill is a self-contained `SKILL.md` (some carry a small bundled
`tools/` script) — plain markdown, no framework dependency. See
[`docs/installing.md`](docs/installing.md) for the symlink command for
Claude Code, Codex, pi, and any other agent that reads `SKILL.md` files.

## License

MIT for everything authored in this repo — see [`LICENSE`](LICENSE).
`skills/herdr` and `skills/tmux-drive` are mirrored from Shawn Hartsock's
[newt-agent](https://github.com/Gilamonster-Foundation/newt-agent) under
its Apache-2.0 license. `skills/three-cs` and `skills/functional-cohesion`
are adaptations under the same license. Their source notices identify the
changes; the three-Cs doctrine reference also retains its attribution.
