Reference doctrine for the [presentation shepherd skill](../skills/presentation/SKILL.md).
Read the relevant section when preparing a helper brief; the skill defines
how to supervise the work. Examples describe design choices, not permission
to expand the assigned task.

# Presentation: one emitter, stable output, accessible structure

Generated user-facing surfaces need one emitter, deterministic output, and
accessible structure, because a surface assembled in several places drifts,
and a surface no one can navigate is not finished.

## One emitter

The shared shell includes the header, global navigation, and footer. Exactly
one function emits it. Every page type sends its page-specific content through
that function instead of carrying a local copy of the shell.

Copied markup starts equal and then diverges. One page gains a link, another
keeps an old label, and a third drops an accessibility fix. The review question
is direct: which single function emits the shared shell? If the answer names
more than one, the boundary is already broken.

The payoff is concrete. One project needed a new navigation destination in
four page shells. All four flowed through one emitter, so the implementation
change was one line.

## Deterministic output

Committed build artifacts are review inputs. The same source, configuration,
and dependency versions must produce the same bytes. Timestamps, unstable
ordering, environment-specific paths, and unpinned inputs turn every rebuild
into noise. That noise hides the change a reviewer needs to inspect.

Test the contract by building the same inputs twice in clean locations and
comparing bytes. A readable diff is a product property, not build trivia.

## Accessible by construction

Build navigation semantics into the emitter. A navigation region is a
landmark with a label. Each destination appears once in that region with a
stable accessible name.

Global navigation answers, "Where else can I go?" Local navigation answers,
"How do I get back?" Adding the global region must not replace or displace the
local one. A reader needs both paths.

## Assert structure, not pixels

Parse generated output and assert the structure that matters:

- the labeled navigation landmark exists once per page;
- every expected destination appears once with its accessible name; and
- local navigation remains present beside the global region.

These checks are cheap and stable. They catch missing landmarks, duplicate
links, and broken names. Screenshot comparison is not part of this doctrine;
pixel similarity does not prove navigable structure.

## Test data, not test literals

Keep the expected destination set in one constant shared by the emitter and
its tests. Do not paste the same list into every test. Otherwise one added
destination breaks several unrelated cases, and the failures no longer show
which boundary failed.

This is the [three Cs](../skills/three-cs/SKILL.md) applied to presentation:
destinations are data, while emitting and validating the shell are mechanisms.

## Borrowed design systems

Pin the version of any external design system and vendor the assets the build
depends on. An unpinned stylesheet can change committed output without a
commit in the project's history. Determinism stops at every unpinned input.

## Shepherd review

Ask for the emitter function, every page type that calls it, two byte-identical
builds, and parsed structural assertions. Check that global and local
navigation coexist. Reject copied shells, repeated destination literals,
pixel-only evidence, and unpinned presentation dependencies.

---

Model: GPT-5 | Harness: Codex | Operator: Shawn Hartsock | Time: 13:07 EDT | Date: 2026-09-11
