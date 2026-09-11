# Guiding Pi helpers

Start with [shepherd](../skills/shepherd/SKILL.md). It owns the coordination
loop from task decomposition through a checked, integrated result. This page
shows how to apply it; setup is in [installing](installing.md).

## Parallel review

With a verified Herdr flock available, ask:

> Use shepherd to have two Pi helpers review this repository. One inspects
> test coverage and one inspects error handling. Require file and line
> evidence, reconcile their findings, and propose the smallest useful next
> action. Review only; leave source files unchanged.

| Task and artifact | Worker | Dependencies | Ownership | Acceptance evidence |
|---|---|---|---|---|
| Coverage findings | First verified helper | None | Read-only checkout; its own report | Existing behavior and located coverage gaps |
| Error-handling findings | Second verified helper | None | Same read-only checkout; its own report | Located failure paths and their caller impact |
| Reconciled review | Shepherd | Both reports | Final assessment | Claims checked against source; overlaps resolved |

Substitute live names and concrete paths into the briefs. Dispatch both
reviews without waiting for either to finish, then inspect progress and
artifacts. If one helper is blocked, keep collecting the other's work.
The final review must resolve disagreements rather than concatenate reports.

## Parallel edits with a shared interface

For a producer/consumer change, agree the record shape and failure behavior
before assigning either side. Give each helper a separate worktree from a
known base, its own implementation and test files, and the shared contract.
If the contract itself must change, assign one owner and make dependent work
wait for the accepted contract. Read-only research can proceed meanwhile.

Require each helper's diff and observed checks. The shepherd then brings the
accepted changes together and runs the actual producer-to-consumer check.
Two passing local suites can still disagree on field names or exit behavior.
Return such a defect to its owner, preserving the agreed interface.

Use [TDD](../skills/tdd-red-green-blue/SKILL.md) for behavior evidence,
[Unix philosophy](../skills/unix-philosophy/SKILL.md) for the interface, and
[cohesion](../skills/functional-cohesion/SKILL.md) when the ownership boundary
needs review. Include only the relevant parts in each worker brief.

## A small serial task

A one-sentence correction may have no independent work worth dispatching.
Handle it directly and check the result. The purpose of shepherding is useful
progress toward the outcome; worker count is not an acceptance criterion.

## A large task, bounded into several assignments

A request to "fix these seven code-review findings" is a program, not an
assignment. Decompose it before dispatch:

| Task and artifact | Worker | Dependencies | Ownership | Acceptance evidence |
|---|---|---|---|---|
| Findings 1 and 3, committed | First helper | None | Its own worktree | Commit SHA; one-line status per finding |
| Findings 2 and 5, committed | Second helper | None | Its own worktree | Commit SHA; one-line status per finding |
| Remaining findings | Shepherd or a later helper | First two committed | Known base | Combined diff checked against all seven |

Each brief names the checkpoint cadence (commit and report after each
finding, not after all of them) and the hand-off path to use if context runs
short. A helper that checkpoints after finding 1 leaves recoverable work even
if it wedges on finding 3.

## A wedged helper

A helper reports `idle` after a long stretch with no checkpoint since early
in the run. Before accepting the report:

1. Read the pane: `herdr agent read <target> --source recent-unwrapped --lines 200`.
   The last visible output is the same tool call, repeated, with an empty or
   failed result.
2. Check the worktree for uncommitted changes the checkpoints should have
   captured. Find them uncommitted, including an untracked file.
3. Commit the recoverable work before doing anything else. Do not discard
   the worktree.
4. Dispatch a replacement with the original brief, the commit SHA of the
   rescued work, and the findings still open. The replacement does not
   repeat work already committed.

Treat this as the default response to `idle` or `done` on a long-running
assignment, not a rare exception: verify pace and artifacts against the
checkpoint cadence before treating either state as success.

## Owning a tab in a shared session

Two shepherds run concurrently in one Herdr session alongside the operator's
own work. Each creates its own tab before starting its flock:

```sh
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --label "shepherd:alice:coverage-fixes" --no-focus
```

```sh
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --label "shepherd:bob:release-notes" --no-focus
```

Neither shepherd reads or closes the other's tab. Each renames its own tab
to `...:done` when its flock's work is committed and its helpers are no
longer needed, telling the operator that tab is safe to close without either
shepherd needing to coordinate with the other directly.

## Evaluate the skill

Use these cases in an isolated fixture or an authorized live flock. Record
observed decisions and artifacts, the execution environment, and any simulated
steps. Frontmatter validation and plausible plans do not establish live behavior.

| Case | Evidence to inspect |
|---|---|
| Two independent reviews | Both briefs submitted before waiting for a final result; reconciled findings |
| Two edits sharing an interface | Agreed contract, isolated worktrees, explicit ownership, combined check |
| A dependent downstream task | Dispatch occurs after the required accepted artifact is available |
| Success reported without evidence | Artifact inspection and missing evidence obtained before acceptance |
| One blocked helper | Independent work proceeds; the blocker is visible without blind resubmission |
| A small indivisible task | A short serial path without unnecessary fleet creation |
| A large task | Split into several assignments, each sized to finish inside one context, each with its own checkpoint cadence |
| A wedged helper reporting idle | Pane read and checkpoint artifacts checked before acceptance; uncommitted work rescued and committed before any replacement is dispatched |
| A helper wedged on an oversized single edit, plenty of context left | Brief bounds each call's payload, not just call count; the oversized edit is decomposed into smaller replacements rather than retried unchanged; a pane showing an announced edit with no result is treated as wedged regardless of remaining context |
| Two shepherds in one session | Each creates and owns its own tab; neither reads, splits into, or closes the other's tab or pane |

The [external dispatcher](https://github.com/Gilamonster-Foundation/newt-agent/blob/main/.newt/bundled-skills/herdr-dispatcher/SKILL.md)
provides further experience with long-running engineering efforts. Its tracker,
publication, and cleanup conventions are not requirements of this library.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:51 EDT | Date: 2026-09-11

Model: claude-sonnet-5[1m] | Harness: Claude Code | Operator: Shawn Hartsock | Time: 11:02 EDT | Date: 2026-09-11
