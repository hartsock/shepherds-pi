# Installing the skills

Every skill in this repo is a plain `SKILL.md` (some carry a small bundled
`tools/` script) — there's no build step and no framework dependency.
Installing means getting that file (or its containing directory) into
wherever your agent looks for skills. That location differs per agent;
this doc covers the ones this repo was built around plus a generic
fallback for anything else.

Install the guidance skills for the **shepherd**, the agent coordinating
pi helpers. Workers receive focused briefs; they need not discover every
shepherd skill. The pi installation below applies when pi itself is the
shepherd, or when you deliberately want these skills available there.

Clone the repo first:

```bash
git clone https://github.com/hartsock/shepherds-pi.git ~/workspaces/shepherds-pi
```

## Claude Code

Global skills directory: `~/.claude/skills/`. Project-local:
`.claude/skills/` inside a repo.

```bash
for skill in ~/workspaces/shepherds-pi/skills/*/; do
  name=$(basename "$skill")
  mkdir -p ~/.claude/skills/"$name"
  ln -sf "$skill/SKILL.md" ~/.claude/skills/"$name"/SKILL.md
  [ -d "$skill/tools" ] && ln -sfn "$skill/tools" ~/.claude/skills/"$name"/tools
done
```

Swap `~/.claude/skills/` for `.claude/skills/` (relative to a repo root) to
install project-scoped instead of global.

## Codex

Global skills directory: `~/.codex/skills/`, same `<name>/SKILL.md` shape
as Claude Code.

```bash
for skill in ~/workspaces/shepherds-pi/skills/*/; do
  name=$(basename "$skill")
  mkdir -p ~/.codex/skills/"$name"
  ln -sf "$skill/SKILL.md" ~/.codex/skills/"$name"/SKILL.md
  [ -d "$skill/tools" ] && ln -sfn "$skill/tools" ~/.codex/skills/"$name"/tools
done
```

## pi

`pi` discovers skills from several places, in order of precedence — see
`pi --help` (`--skill`, `--no-skills`) for the authoritative list. Two are
relevant here:

- **`~/.pi/agent/skills/`** — pi-specific, global.
- **`~/.agents/skills/`** (global) and **`.agents/skills/`** (project,
  walked up to the repo root) — a shared, cross-tool convention pi reads
  natively. Installing here means pi picks the skill up with **no
  pi-specific step at all**:

```bash
for skill in ~/workspaces/shepherds-pi/skills/*/; do
  name=$(basename "$skill")
  mkdir -p ~/.agents/skills/"$name"
  ln -sf "$skill/SKILL.md" ~/.agents/skills/"$name"/SKILL.md
  [ -d "$skill/tools" ] && ln -sfn "$skill/tools" ~/.agents/skills/"$name"/tools
done
```

Use `.agents/skills/` (relative to a repo root, no leading `~`) instead to
scope it to one project.

You can also load one skill for a single run without installing anything:

```bash
pi --skill ~/workspaces/shepherds-pi/skills/pi-inference-backend
```

## Any other agent

Most agents that support markdown skills at all use one of two shapes:
a single directory of `<name>/SKILL.md` folders, or a single directory of
`<name>.md` files. Check that agent's own docs for the directory it
scans, then apply the same symlink loop:

```bash
TARGET_SKILLS_DIR=/path/your/agent/uses

for skill in ~/workspaces/shepherds-pi/skills/*/; do
  name=$(basename "$skill")
  mkdir -p "$TARGET_SKILLS_DIR/$name"
  ln -sf "$skill/SKILL.md" "$TARGET_SKILLS_DIR/$name/SKILL.md"
  [ -d "$skill/tools" ] && ln -sfn "$skill/tools" "$TARGET_SKILLS_DIR/$name/tools"
done
```

If the agent wants flat `<name>.md` files instead of `<name>/SKILL.md`
directories, symlink the file directly under a renamed target instead of
the loop above:

```bash
ln -sf ~/workspaces/shepherds-pi/skills/tdd-red-green-blue/SKILL.md \
       "$TARGET_SKILLS_DIR/tdd-red-green-blue.md"
```

(That drops any bundled `tools/`, since a flat-file convention has nowhere
to put it — only `skills/concision` in this repo carries one.)

## Symlinks vs. copies

All the commands above use symlinks so `git pull` in
`~/workspaces/shepherds-pi` updates every agent at once. If your agent
doesn't follow symlinks, `cp -r` instead — you'll just need to re-copy
after pulling updates.

## Linked doctrine references

Keep the checkout available: shepherd skills link to longer references in
`docs/`. Resolve those links relative to the original `SKILL.md` in the
checkout, following its symlink first. If copying instead of symlinking,
retain the repository's `skills/` and `docs/` layout or adjust reference
paths for your installation. Copying only `SKILL.md` omits the references.
The core shepherd workflow is in each skill; read doctrine only as needed.
