---
name: tdd-red-green-blue
description: Shepherd a pi helper through test-driven implementation or a regression fix. Brief one behavior, verify a meaningful Red failure, inspect the minimal Green change, and guide behavior-preserving Blue refactoring using actual test evidence.
---

# Shepherd Red, Green, Blue

You supervise pi's implementation. Keep each cycle small enough to inspect:
one observable behavior, a test that fails for that reason, a minimal fix,
then structural cleanup while tests remain green. Use this for behavior
changes and regression fixes, not to manufacture tests for prose edits.

For helper selection, transport, and blocked-state handling, follow the
[shared shepherd loop](../../docs/shepherding.md).

## Set the assignment

Give pi the repository, owned files or isolated worktree, desired behavior,
counterexample, compatibility constraints, and appropriate test commands.
Discover the project's test conventions first. If other helpers are active,
assign separate ownership; do not have them race to edit the same code or
test. A helper should not spawn more agents or publish changes unless that
is separately assigned.

State which checkpoints to return. For an uncertain bug or design, ask for
Red evidence before assigning the next implementation step. For a small,
well-understood change, pi may complete the cycle in one turn and return
the evidence for each phase; human approval is not required at every color.

> In the assigned files, reproduce the specified behavior with one focused
> test. Run it before the fix and record the command, exit status, and
> relevant failure. Implement only enough to pass, then run the affected
> suite. Refactor only after Green, with behavior unchanged, and rerun the
> affected checks. Report Red, Green, and Blue evidence, changed files,
> and remaining failures. If the test cannot run, report why; do not claim
> a Red result. No unrelated changes or further delegation.

## Inspect each phase

| Phase | Evidence to inspect | Shepherd's decision |
|---|---|---|
| Red | Test diff and pre-fix command, exit status, failure text | Does the assertion expose the requested behavior? An import error, missing tool, or broken fixture is not Red. |
| Green | Implementation diff, focused result, affected regression results | Does the fix satisfy the contract without weakening assertions or adding speculative behavior? |
| Blue | Cleanup diff and rerun results | Did only structure change? Is cleanup useful, or is the current design already sufficient? |

Read the actual test and implementation; "all green" is a report to
verify. Run checks proportional to the change and any repository-required
gates. Record pre-existing failures separately. Do not demand an unrelated,
expensive full suite at every small step, and do not call a failed required
gate a pass.

## Correct drift

- **Red is a setup failure:** send pi back to repair the fixture or report
  the missing prerequisite before implementing the behavior.
- **Implementation arrived first:** report the missing Red evidence. Where
  practical, run the new test against the pre-fix code in an isolated copy;
  do not rewrite shared history or pretend the chronology was test-first.
- **The test was weakened to pass:** point to the lost assertion and ask
  pi to restore the contract, then fix the implementation.
- **Several behaviors or a redesign appeared:** keep the current cycle
  scoped to one behavior; separate later work rather than expanding silently.
- **Blue breaks a test:** have the owning helper repair or undo its cleanup
  before beginning another behavior. Preserve unrelated user changes.

Accept the cycle when the diff matches the assigned behavior and its
evidence is sound. Report any unrun checks or blockers explicitly. For
test design details such as Arrange/Act/Assert and FIRST, consult the
[TDD doctrine](../../docs/tdd-red-green-blue-doctrine.md).
