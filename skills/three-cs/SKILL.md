---
name: three-cs
description: Guide a pi helper in separating domain knowledge from mechanisms using Composition, Configuration, and Convention. Use when supervising growing tables, configurable behavior, or a data extraction, while preventing speculative frameworks and preserving safety invariants.
license: Apache-2.0
---

# Shepherd the three Cs

You choose the boundary and review pi's implementation. Domain knowledge
belongs in composable, configurable data; algorithms, precedence laws,
and safety enforcement remain code. Working behavior comes first. Do not
turn a single known case into a speculative configuration framework.

For helper selection, transport, and blocked-state handling, follow the
[shared shepherd loop](../../docs/shepherding.md).

## Brief from the working code

Ask pi to identify the changing knowledge, the mechanism consuming it,
existing configuration conventions, and a concrete operator use case.
For a review-only request, stop at findings and a proposed boundary.
For implementation, assign owned files, preserved behavior, data shape,
and the exact extension or override to demonstrate.

> Inspect the assigned mapping and its callers. Identify domain facts
> that an operator needs to add or override, and the invariants that must
> stay enforced in code. Reuse the project's format, loading locations,
> precedence, and error policy. Within the assigned scope, extract only
> the needed data and prove existing behavior plus the requested override.
> Report the changed boundary, example data, test commands and results,
> and any deferred hardcoding. No unrelated framework or delegation.

For a new feature, let pi establish a small working implementation before
extracting data. If hardcoding is an intentional intermediate step, name
what remains and when to revisit it. Recording that limitation does not
authorize opening an issue or expanding the implementation.

## Inspect all three Cs

| Principle | Ask pi to demonstrate | Reject this shortcut |
|---|---|---|
| Composition | Existing and added data combine through the same mechanism | Another domain-specific branch in the engine |
| Configuration | A supported value or unit changes through operator data | A source literal renamed `config` that still needs recompilation |
| Convention | Loading, identity, and override order follow the existing project contract | New ad hoc search paths or undocumented precedence |

Inspect the diff, example data, and observed tests. Built-ins and external
units should use the same schema where both exist. Require only the layers
the task needs; built-in/global/project/inline is an example, not a mandate.
Prove that the old defaults still work and the requested addition or override
does not require another mechanism change.

Have pi distinguish optional data from required or security-sensitive
configuration. A malformed optional pack may be skipped with a diagnostic
when that matches the contract. Required configuration must not silently
fall back, and a data override must never weaken safety enforcement.

## Steer and accept

Give a concrete correction tied to the boundary:

> This moves the extension list into a file, but adding a language still
> requires a new switch arm. Make the existing loader consume that entry
> and prove it with a second fixture; keep the matching algorithm unchanged.

If pi introduces a plugin framework for one table, narrow the change to the
existing data seam. If it makes an invariant configurable, restore enforcement
in code. Accept when the operator use case works, defaults are preserved,
the precedence is explicit, and the evidence covers malformed input under
the chosen policy. Report any deferred extraction without claiming it done.

Consult the [three-Cs doctrine](../../docs/three-cs-doctrine.md) for the
knowledge/mechanism distinction and language-pack example.

---

Adapted from Shawn Hartsock's [newt-agent](https://github.com/Gilamonster-Foundation/newt-agent/tree/main/.newt/bundled-skills/three-cs)
`bundled-skills/three-cs`, Apache-2.0. Modified into shepherd instructions
for briefing, inspecting, and steering pi helpers. The longer doctrine
and its prior adaptation notice are retained in the linked reference.
