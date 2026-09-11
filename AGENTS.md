# AGENTS.md — Shepherd's Pi

If you are an agent that landed in this repo: this is a skills library, not
an application. There is nothing to build or run at the repo root. Each
directory under `skills/` is independent — read its `SKILL.md`, do what it
says, done.

## Order of operations, if setting up from scratch

1. `skills/pi-install` — get `pi` on the machine, confirm `pi --help` runs.
2. `skills/pi-inference-backend` — point `pi` at an inference endpoint and
   set a default model, so bare `pi` (no flags) launches ready to work.
3. `skills/herdr` — the herdr CLI reference, if herdr is also in play.
4. `skills/herdr-helpers-tab` — stand up a tab of idle `pi` panes for
   another agent to dispatch into.
5. `skills/tmux-drive` — when a program needs a real TTY and neither `pi`
   nor herdr apply (an installer, a REPL, any TUI).

The skills `concision`, `tdd-red-green-blue`, `three-cs`, and
`unix-philosophy` guide the shepherd in briefing, inspecting, and steering
pi helpers. They are not setup steps or blanket instructions for workers
to delegate again. Read `docs/shepherding.md` for the coordination loop.
`functional-cohesion` remains supporting design doctrine.

## Conventions this repo follows

- No secrets, tokens, or vendor-internal endpoints anywhere in this repo.
  Every skill that needs a backend, a key, or a model name takes it as a
  placeholder/variable — never a hardcoded real value.
- Every skill is a plain `SKILL.md` with YAML frontmatter (`name`,
  `description`, optional `argument-hint`) followed by markdown. No build
  step, no runtime dependency beyond what a skill's own `tools/` says it
  needs.
- `docs/` holds reference material too long or too detailed to inline in a
  skill. Skills link to `docs/`; `docs/` doesn't duplicate skill content.
