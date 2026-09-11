Reference doctrine for the [cross-project-linking shepherd skill](../skills/cross-project-linking/SKILL.md).
Read the relevant section when preparing a helper brief; the skill defines
how to supervise the work. Examples describe design choices, not permission
to expand the assigned task.

# Cross-project linking

One sentence:

> **When one system spans several properties, every property must link to
> every other property or the system becomes undiscoverable from some entry
> point.**

A property may be a repository, documentation site, package registry, or
dashboard. A person can arrive at any one of them first. Each must therefore
act as a complete entry point to the system.

## Complete the directed graph

For `N` properties, require `N × (N - 1)` directed cross-property links. A
link in one direction does not imply a path back. A property linked from every
other property but linking to none of them is still orphaned for anyone who
lands there first.

For four properties, each property needs links to the other three. The result
is twelve directed links. A partial ring or hub-and-spoke list does not meet
the contract.

## Keep the self row

Every navigation block lists all `N` properties, including itself. Mark the
current property with `You are here` or an equivalent label. Do not omit its
row.

Self-omission makes otherwise identical blocks different lengths. They then
drift quietly: one gains a destination, another keeps an old label, and a
third loses the return path. A stable row set makes comparison mechanical.
The self row does not add to the `N × (N - 1)` cross-property count.

## Define the link set once

The canonical link set is data. Apply the
[three-cs](../skills/three-cs/SKILL.md) rule: knowledge belongs in data, not
logic. Define one ordered collection of destinations, labels, roles, and
canonical URLs. Import it wherever navigation is rendered or checked.

The failure that prompted this doctrine was simple. A project hardcoded its
ecosystem links in a page generator and in two separate test allowlists. A new
destination required three coordinated edits. Missing any one made CI fail.
That is the knowledge-in-logic smell the three Cs names.

One imported constant removes that coordination hazard. The generator reads
it. The tests read it. Adding a destination becomes one data change, followed
by the same mechanical checks. Do not copy the list into a second renderer,
fixture, or allowlist.

## Test the matrix

Acceptance is mechanical, not editorial:

1. Load the canonical link set.
2. Fetch each property through the path its readers use.
3. Assert that every canonical URL appears in every property.
4. Assert that the current property is present and marked as current.

The test covers an `N × N` display matrix. Its off-diagonal cells prove the
`N × (N - 1)` directed links. A shepherd should require the command and its
result, not a helper's assurance that the pages look complete.

## Account for access asymmetry

Linking does not grant access. If properties have different visibility, a
link can be present and correct yet return `404` for most readers. Test from
the intended audience's access level. Record restricted destinations clearly,
or provide an accessible landing page that explains how to gain access.

Do not count an administrator's successful fetch as proof that ordinary
readers can navigate the system.

## Checklist

- [ ] Is there one canonical ordered link set?
- [ ] Does every property render every row, including its own current row?
- [ ] Are all `N × (N - 1)` directed cross-property links present?
- [ ] Do the generator and tests import the same link data?
- [ ] Did the shepherd inspect fetch-based assertions for every property?
- [ ] Were links tested at each intended visibility level?

---

The data-versus-logic guidance is adapted from the
[Three Cs doctrine](three-cs-doctrine.md), which retains its Apache-2.0
attribution.

Model: GPT-5.6 | Harness: Codex | Operator: Shawn Hartsock | Time: 13:04 EDT | Date: 2026-09-11
