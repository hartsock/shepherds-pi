# Installing the skills

Install on the machine where the shepherd runs. Keep the checkout available:
skill directories link to shared doctrine in `docs/`. Workers receive focused
briefs and need not discover the shepherd's full skill library.

```sh
git clone https://github.com/hartsock/shepherds-pi.git
cd shepherds-pi
python3 tools/install-skills.py --target "$HOME/.agents/skills"
```

Python 3.9+ is required for the installer; it uses only the standard library.
By default it installs `shepherd`, `herdr`, and `herdr-helpers-tab`. It links
whole directories, leaves already-correct links alone, and checks all selected
names for collisions before creating links. A collision leaves existing skills
untouched; choose project scope or reconcile that name explicitly.

| Shepherd | Example install target |
|---|---|
| Codex | `.agents/skills` in the project or the agent's global skills directory |
| Claude Code | `.claude/skills` in the project or the agent's global skills directory |
| Pi as the shepherd | `.agents/skills` in the project or Pi's configured skills directory |
| Other harness | Its documented directory of skill folders |

Pass the selected directory through `--target`. Install in the intended
project when it differs from this library's checkout. The global example above
uses the shared agent-skills directory; Claude Code users can instead use
`--target "$HOME/.claude/skills"`.

## Add only the guidance you need

Use `--skill` repeatedly to add named skills to the core installation:

```sh
python3 tools/install-skills.py --target "$HOME/.agents/skills" \
  --skill pi-install --skill pi-inference-backend
python3 tools/install-skills.py --target "$HOME/.agents/skills" \
  --skill tdd-red-green-blue --skill unix-philosophy
```

Concision, three Cs, and functional cohesion are also optional review guidance.
`tmux-drive` is for other interactive programs; normal flock work uses Herdr.
To install everything explicitly:

```sh
python3 tools/install-skills.py --target "$HOME/.agents/skills" --all
```

Selection controls new links. Running the installer again does not uninstall
previously installed optional skills or change the agent's other configuration.

## Follow resources from the source directory

Resolve each installed skill directory's symlink before following relative
references into this repository. This preserves both `tools/` resources and
shared `docs/` paths. If the harness cannot follow symlinks, point it at the
checkout directly or retain the repository layout when copying. Copying only
`SKILL.md` loses those references.

Once tools and workers are ready, start with
[shepherd](../skills/shepherd/SKILL.md). Its
[worked examples](shepherding.md) cover review, editing, and a small serial task.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:53 EDT | Date: 2026-09-11

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:59 EDT | Date: 2026-09-11
