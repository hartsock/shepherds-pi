---
name: presentation
description: Shepherd a pi helper building or revising generated user-facing surfaces. Brief one shared emitter, deterministic committed output, accessible navigation, and structural tests, then inspect those boundaries in the result.
license: Apache-2.0
---

# Shepherd presentation surfaces

You define the shared-shell boundary and evidence; pi implements it without mixing page-specific content into the header, navigation, or footer.

For helper selection, transport, and blocked-state handling, follow the [shared shepherd loop](../../docs/shepherding.md).

## Brief the helper

Name every page type, owned files, expected destinations, whether generated
artifacts are committed, and checks. Require one shell emitter for every type.

> Inspect every generated page path and identify the one function that emits
> the shared header, navigation, and footer. Route every page type through it
> without changing page content. Keep destinations in one constant. If artifacts
> are committed, prove two clean builds byte-equal. Parse each result and assert
> one labeled landmark, one accessible name per destination, and local navigation.
> Pin and vendor external design dependencies. Report files, commands, results.

## Inspect the result

- Ask which single function emits the shell. More than one fails the boundary.
- Trace every page type to that function; copied markup is not an emitter.
- Compare committed builds byte for byte and inspect any difference.
- Parse output to verify the landmark, label, destinations, and local navigation.
- Confirm external presentation dependencies are pinned and vendored.

Use [three-cs](../three-cs/SKILL.md) for the destination set: emitter and tests
share one data constant instead of repeating destination literals per test.

Screenshot comparison is not acceptance evidence for this doctrine. Accept
when the shell has one emitter, committed output is reproducible, semantic
navigation is present, and structural tests cover every page type. Consult the
[presentation doctrine](../../docs/presentation-doctrine.md) for the rationale.

---

Adapted from Shawn Hartsock's [newt-agent](https://github.com/Gilamonster-Foundation/newt-agent/tree/main/.newt/bundled-skills/presentation) `bundled-skills/presentation`, Apache-2.0. Modified into shepherd instructions for briefing and inspecting pi helpers.

Model: GPT-5 | Harness: Codex | Operator: Shawn Hartsock | Time: 13:08 EDT | Date: 2026-09-11
