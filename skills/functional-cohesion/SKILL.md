---
name: functional-cohesion
description: Guide a Pi helper reviewing module boundaries or extracting a cohesive unit. Assign one job and a narrow interface, inspect ownership and behavior-preserving evidence, and correct category-based splits or unrelated redesign.
license: Apache-2.0
---

# Shepherd cohesive changes

Use this guidance when a task needs a module boundary or extraction, including
boundaries used to divide work between helpers. A long file alone does not
justify a reorganization. Follow [shepherd](../shepherd/SKILL.md) for assignment,
isolation, dispatch, and integration.

## Brief and inspect

Identify the job, callers, allowed files, and behavior to preserve. Ask the
helper to propose a unit named for its job and show the interface its callers
need. For review-only work, return findings and the proposed boundary.

> Extract the assigned unit with its tests, preserving behavior and the
> public API. Separate code motion from later design changes. Report the
> moved files, caller-facing interface, relevant test results, and remaining
> coupling. Stay within the agreed ownership and do not delegate again.

Inspect whether the unit contains the code that works together on one job.
Reject a split that merely groups all types, constants, or helpers while
scattering each feature across those files. Check both sides of the interface,
including callers and tests. Separate worktrees still need an agreed contract.

## Correct and accept

Return a specific boundary defect and the smallest correction. If an extraction
requires many newly exposed internals, reconsider the cut before widening the
API. If unrelated redesign appears, return to behavior-preserving movement.
Accept when the assigned job is easier to locate, its interface is narrow,
and appropriate tests and caller checks support the preserved behavior.

The [cohesion doctrine](../../docs/functional-cohesion-doctrine.md) contains
the detailed structural principles and extraction example.

---

Adapted from Shawn Hartsock's [newt-agent](https://github.com/Gilamonster-Foundation/newt-agent/tree/main/.newt/bundled-skills/functional-cohesion),
Apache-2.0. Modified into shepherd instructions for briefing and reviewing
helpers; the prior doctrine and adaptation notice are retained in the reference.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:51 EDT | Date: 2026-09-11
