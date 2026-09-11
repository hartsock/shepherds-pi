# AGENTS.md: Shepherd's Pi

This is a skills library for coordinating Pi helpers. Start with
[skills/shepherd/SKILL.md](skills/shepherd/SKILL.md) when the user assigns
shepherding or parallel helper work. It covers decomposition, bounded briefs,
parallel dispatch, correction, and integration. A helper assigned a brief
executes it; it does not start another delegation chain.

Reading or editing this library does not authorize creating a live flock.
The user's task determines what setup and external actions are authorized.

## Setup when needed

Use existing tools and verified workers first. For initial setup, follow
`skills/pi-install`, `skills/pi-inference-backend`, `skills/herdr`, and
`skills/herdr-helpers-tab` in that order. Once ready, return to `shepherd`.
Keep the operator's focus and existing work intact.

Specialist guidance is optional: `tdd-red-green-blue`, `concision`, `three-cs`,
`unix-philosophy`, and `functional-cohesion` supply task-specific review
criteria. `tmux-drive` supports other TTY programs and is outside the default
flock workflow. Workers receive focused briefs, not the whole doctrine library.

## Conventions

- No secrets, tokens, or vendor-internal endpoints in this repository.
  Backend, credential, and model examples use placeholders.
- Skills use YAML frontmatter with `name` and `description`, then Markdown.
  Preserve license and authorship notices.
- Keep shared reference material in `docs/`; resolve a skill's directory
  symlink before following relative links. Avoid duplicate coordination loops.
- The installer uses the Python standard library. For installer changes, run
  `python3 -B -m unittest discover -s tests -v` and `git diff --check`.
  There is no root application build. Skill syntax checks do not prove live
  orchestration behavior; use the cases in `docs/shepherding.md` as appropriate.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:51 EDT | Date: 2026-09-11
