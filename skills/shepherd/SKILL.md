---
name: shepherd
description: Coordinate Pi helpers through a task using bounded parallel assignments, artifact review, corrections, and integration. Use when the user asks to shepherd a flock, delegate to Pi helpers, or organize parallel agent work. Setup and specialist guidance load only when the task needs them.
---

# Shepherd a task

Own the user's outcome and acceptance; helpers own bounded assignments.
Look for independent work that can progress together. Use a short serial
path when dependencies or coordination cost leave no useful parallel work.
A helper receiving a brief completes it without delegating again unless
that role is explicitly assigned.

## Plan the work

Read the request, relevant project instructions, and the current artifacts.
Identify the result, constraints, available workers, and granted authority.
Reading this library does not authorize creating workers or publishing work.
Keep existing authorization; ask only for a missing decision that blocks progress.

For multiple assignments, keep a small table in the task notes:

| Task and artifact | Worker | Dependencies | Workspace and owned files | Acceptance evidence | State |
|---|---|---|---|---|---|
| Concrete result | Verified identity | Required prior result, or none | Accessible path and edit/review scope | Checks or source evidence | Ready, working, blocked, or accepted |

Resolve shared interfaces and who owns shared files before dispatch.
Read-only helpers may inspect the same checkout. Give editing helpers
separate worktrees from a known base and bounded ownership; isolation alone
does not resolve conflicting designs. Dependent work waits for its required
artifact. Match worker count to ready work and available capacity.

## Prepare and brief helpers

Reuse workers whose identity, state, directory, and ownership you have checked.
For Herdr, follow [the transport skill](../herdr/SKILL.md) in the intended
execution host and session. If that context is missing, report the prerequisite;
do not control an unrelated focused session or silently switch transports.
Use [Helpers setup](../herdr-helpers-tab/SKILL.md) only when capacity is needed
and its creation is authorized. Start workers in their assigned directories.

Give each helper the task, accessible sources, owned files, edit or review
permission, constraints, and acceptance checks. Require artifact paths,
observed evidence, and unresolved limits in its reply. Save a brief or handoff
when the task may outlive the worker's context. Include necessary excerpts
when the worker cannot reach a reference on the shepherd's host.

Load only the review guidance that changes this assignment:

| Assignment | Guidance |
|---|---|
| Behavior change or regression | [TDD](../tdd-red-green-blue/SKILL.md) |
| Writing or revision | [Concision](../concision/SKILL.md) |
| Configurable domain knowledge | [Three Cs](../three-cs/SKILL.md) |
| CLI or composable interface | [Unix philosophy](../unix-philosophy/SKILL.md) |
| Module boundaries or extraction | [Functional cohesion](../functional-cohesion/SKILL.md) |

Workers receive the relevant instructions in their briefs; they do not need
the entire shepherd skill library installed.

## Own a tab for your flock

In a shared Herdr session, create a tab for your flock rather than splitting
panes into whatever tab you currently occupy:

```sh
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --label "shepherd:<name>:<purpose>" --no-focus
```

Split helper panes inside the tab you just created, not the caller's tab.

Label convention, so an independent shepherd converges on the same scheme
without having seen this one:

```
shepherd:<name>:<purpose>
```

`<name>` is this shepherd's own Herdr agent name if it has one, otherwise a
short slug unique to this task. `<purpose>` is a few words on what the flock
is doing. The `shepherd:` prefix tells the operator the tab is shepherd-owned
and disposable, distinct from the operator's own tabs. On completion, rename
the tab to tell the operator it is safe to close:

```sh
herdr tab rename <tab_id> "shepherd:<name>:<purpose>:done"
```

Do not touch a tab or pane you did not create, including another shepherd's
flock. Close only what you created, and only within the scope the user
granted.

## Size and bound each assignment

Size an assignment to finish well inside one helper's context. Prefer several
bounded assignments over one large one: "fix findings 1 and 3, commit, report"
is an assignment; "fix seven findings" is a program to decompose into several.

Require a checkpoint cadence in the brief. A checkpoint is a durable artifact
committed, plus a one-line status the shepherd can read from the pane; the
helper produces both at each milestone, not only at the end. Require a
hand-off note before context runs out, not after: name the path in the brief
(for example a file under the worker's scratch directory). A committed
partial result with a hand-off note is an acceptable outcome; an uncommitted
near-complete result is not. Give the helper a stop rule for repeated tool
failure: two consecutive empty or failed calls of the same tool means stop
and report, not retry a third time.

Bound the size of individual tool calls in the brief, not just the
assignment: one edit per call, verify, commit, repeat. A batched call that
applies several non-overlapping edit ranges at once is a single point of
failure: when it returns empty there is no partial result and no error to
act on, only silence. A helper with plenty of context left can still wedge
this way; remaining headroom is not evidence the helper is healthy.

## Dispatch and observe

Dispatch all ready independent assignments before waiting for final results.
For Herdr, use `herdr agent prompt <target> <brief>` without `--wait` for that
initial dispatch. Then collect progress with the transport's read/wait commands.
Use waiting dispatch for a single assignment or a dependency that must finish
before the next task can begin. Confirm pickup from a response or artifact
showing the brief is being acted on; a title or busy indicator is insufficient.

Keep independent work moving while a helper is blocked. Inspect timeouts,
missing prerequisites, and questions before retrying; do not repeatedly send
the same brief to a working helper. Surface decisions requiring the operator.
Stop adding workers when readiness or inference fails, and avoid multiplying
expensive shared checks beyond the host's available capacity.

An `idle` or `done` helper may be finished or wedged; the two states look
identical from outside. Check before accepting either: time since the last
checkpoint against the pace the brief set, presence of the artifacts that
checkpoint promised, and the pane's actual last output. A pane whose last
output is the same failed call repeated is evidence of wedging, not of a
blocked question. A pane whose last output is an announcement of work with
no result following it is the same evidence: the call never returned. Read
the pane before deciding:

```sh
herdr agent read <target> --source recent-unwrapped --lines 200
```

If that does not settle it, read the worker's transcript or worktree diff
directly rather than trusting the reported state.

Rescue before replace. If a wedged helper left uncommitted work, commit it
first; do not discard a worktree to start a replacement. A replacement worker
then receives the current brief, the committed artifacts, and the remaining
work, not a repeat of the same unbounded assignment.

## Inspect, correct, and integrate

Read actual artifacts and relevant diffs. Verify reported evidence against
the acceptance criteria; `idle`, `done`, or a confident summary means inspect,
not accept. Distinguish pre-existing failures and unrun checks from passes.

Send located defects, their evidence, and a bounded correction to the owning
helper. If corrections repeat without progress, narrow the assignment or fix
its missing context. Preserve unrelated user changes.

Accept individual results when their criteria are satisfied, then reconcile
conflicting findings and integrate dependent artifacts against a known base.
Check the combined behavior and shared interfaces, with tests appropriate to
the changes. Individually passing worktrees do not prove the combined result.
The shepherd owns integration and the final account of what was checked.
Publishing, pushing, merging, and destructive cleanup follow the user's granted
scope; worker completion does not grant additional authority.

Report the outcome, evidence, unresolved limitations, and any decision still
needed. Stop when the user's acceptance criteria are met. See the
[worked assignments and evaluation cases](../../docs/shepherding.md) for examples.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:51 EDT | Date: 2026-09-11

Model: claude-sonnet-5[1m] | Harness: Claude Code | Operator: Shawn Hartsock | Time: 11:00 EDT | Date: 2026-09-11
