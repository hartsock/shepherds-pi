---
name: herdr-helpers-tab
description: Prepare or reuse a Herdr Helpers tab with verified idle Pi workers for a shepherd. Use when the operator requests a flock or an authorized task needs additional helper capacity.
---

# Prepare Pi helpers

Follow [Herdr](../herdr/SKILL.md) in the intended execution host and session.
Use installed CLI help for current syntax. Verify Pi's configured backend
with [setup guidance](../pi-inference-backend/SKILL.md) when needed. Keep the
operator's configured model and provider unless the assignment specifies others.

For a task, size the flock to independent ready work. For a setup-only request,
use the requested count, or four workers when unspecified, and leave them idle.
For edits, assign separate worktrees and owned files before starting workers
in those directories. [Shepherd](../shepherd/SKILL.md) owns that plan.

## Inspect and prepare

Inspect existing tabs, panes, and agents with explicit workspace targets.
Reuse only workers whose identity, state, directory, and ownership are known.
Create missing capacity in verified empty shell panes; leave existing work
intact. Never send a shell command into a running agent.

For a new Helpers tab, use the caller's workspace and preserve focus:

```sh
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --label Helpers --no-focus
```

Read returned tab and pane IDs. Split with explicit pane IDs, assigned working
directories, and `--no-focus`. Use a balanced layout: a 2-by-2 helper grid keeps
four workers readable. Do not infer IDs from visual positions or reuse an
unrelated Helpers tab merely because its label matches.

## Start and verify

Check the agent roster for name collisions. In each verified shell pane,
start Pi with a unique name using its configured defaults:

```sh
herdr agent start pi-01 --kind pi --pane <helper-pane-id>
```

When the assignment specifies explicit model/provider flags, pass those after
`--` according to installed help. Credentials stay with their configured
provider; do not put them in pane commands, prompts, or command arguments.

Start workers sequentially and inspect readiness after each launch. Verify
identity, model, and the assigned directory before dispatch. `idle` or `done`
can indicate readiness; `blocked` needs attention and `unknown` needs inspection.
Stop adding capacity on the first readiness or inference failure. Do not focus
a tab merely to change its status label.

## Return to shepherding

Report the observed names, pane IDs, directories, model, and readiness. A
setup-only request ends here. When work is assigned, return to
[shepherd](../shepherd/SKILL.md) to brief helpers, dispatch independent work
before waiting, inspect artifacts, correct defects, and integrate results.
The [worked assignments](../../docs/shepherding.md) show the full workflow.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:53 EDT | Date: 2026-09-11

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:59 EDT | Date: 2026-09-11
