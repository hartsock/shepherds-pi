Reference doctrine for the [three-cs shepherd skill](../skills/three-cs/SKILL.md).
Read the relevant section when preparing a helper brief; the skill defines
how to supervise the work. Examples describe design choices, not permission
to expand the assigned task.

This reference retains the Apache-2.0 attribution below.

# The Three Cs — Composition, Configuration, Convention

The house data-vs-logic doctrine. One sentence:

> **Knowledge belongs in data, not logic.** Language- or domain-specific
> knowledge — keyword lists, magic constants, recognition rules, mappings —
> should be pure data that is *composed*, *configured* (droppable /
> overridable), and *convention-driven*, so a new language or domain is
> **config, not code**.

The three Cs, unpacked:

- **Composition** — knowledge comes in units that combine. Packs merge by
  name; layers stack (built-ins → global drop-ins → project drop-ins →
  inline config); a later layer adds or overrides without touching the
  earlier ones. The engine never knows how many packs exist.
- **Configuration** — every knowledge unit is droppable and overridable by
  the operator: a `.toml` in a drop-in directory, an inline config section,
  an overridable property. Never a recompile. Never an inline `json!`/list
  literal pretending to be config (that's code wearing a data costume).
- **Convention** — the *shape* and *location* of the data follow house
  conventions so new units need no wiring: `<name>.toml` in a known drop-in
  dir, merge-by-name, an explicit error policy (optional malformed packs may be skipped
  with diagnostics; required or security-sensitive data must not silently fall back). Convention is what makes composition and configuration cheap.

## Why this matters

Hardcoded knowledge is **lock-in at the source level**. A keyword list baked
into a `match` means every new language is a source patch, a review, a release.
The same list as a droppable pack means a new language is a file a user writes
at their desk. The doctrine is the workspace philosophy applied to code:
plain-text, replaceable, no lock-in — don't confuse the instrument (the engine)
with the thing observed (the knowledge).

There's a second payoff for agents specifically: pure data is **legible and
diffable**. An agent (or a reviewer) can audit a `.toml` of rules at a glance;
auditing the same knowledge threaded through control flow requires reading the
whole function.

## The load-bearing counterweight: working code over all

**Functional results come first.** It is fine — *expected* — to compromise to a
hardcoded, simple implementation to **get a feature working**. Do not let the
three Cs block shipping a working result. A hardcoded list that ships today
beats a pluggable pack system that ships next month.

Then **return to the three Cs**: once it works (tests green, behavior proven),
refactor the hardcoded values into pure-data config, composition seams, and
conventions. The sequence is deliberate — the working version teaches you the
real shape of the data before you design its schema.

The discipline in both directions:

- Don't gold-plate first: no speculative pack systems for knowledge with one
  known instance. (YAGNI still binds; the *second* instance is the signal.)
- Don't skip the circle-back: when you hardcode to ship, **flag it** — a
  `// three-Cs: de-hardcode into <pack/config>` comment or a follow-up issue.
  A hardcoded list that encodes domain knowledge and has no flag is debt
  hiding as design.

## What counts as "knowledge" (and what doesn't)

Move to data:

- **Keyword / phrase / pattern lists** — language keywords, domain phrases,
  recognition regexes, redaction patterns.
- **Magic constants that encode a domain fact** — model context windows, file
  extensions per language, danger classifications per command.
- **Mappings and tables** — command → tool, extension → language, verb →
  capability class.
- **Schemas** — an inline `json!` schema literal is an anti-pattern; it
  belongs in a data file with an overridable property.

Keep in code:

- **Invariants and safety floors** — the danger-tier *enforcement*, the
  attenuation-only rule, precedence laws. The *table* of dangerous targets is
  data; the rule "high-danger is never auto-allowable" is logic. Policy
  *mechanics* are code; policy *content* is data.
- **Algorithms** — the merge, the matcher, the renderer. The engine is code;
  what it consumes is data.

Litmus test: **would a competent operator ever want a different value without
wanting different behavior?** If yes, it's configuration. If changing it changes
what the program *means*, it's code.

## What "good" looks like (a worked example)

Say a tool needs to know, per programming language, things like its file
extensions, its comment syntax, and how to find a symbol definition in it.
That knowledge could live in a big `match`/`switch` keyed on language name
inside the tool's source — or it can become a **language pack**: pure
data, one file per language, loaded rather than compiled in.

- **Built-in packs** (say, Rust, Python, Bash, Go) ship as data bundled
  with the tool itself, and double as the canonical examples anyone
  copies to write a new one.
- **External packs**: drop a `<name>.toml` into a well-known directory —
  `~/.yourtool/language-packs/` (global) or `.yourtool/language-packs/`
  (project-local) — or supply one inline in config.
- **Merge-by-name**: a community-contributed Ruby pack *adds* a new
  language; a local `rust.toml` *overrides* the built-in one — without
  ever touching the tool's source.
- **Tolerant loading**: a malformed optional language pack is skipped with a warning
  when the contract permits it. Required configuration errors remain failures.

Adding a language becomes *config, not code*. The same shape generalizes
to any growing per-instance table a real system accumulates: model cards
for an LLM router, credential-backend definitions, plugin manifests, a
table of commands a policy engine treats as dangerous. Whenever you build
a new drop-in, copy the same conventions — same layering, same
merge-by-name, same tolerant loading — so people learn the pattern once
and reuse it everywhere.

## How to apply it (the de-hardcode recipe)

1. **Find the knowledge.** In the working (possibly hardcoded) code, identify
   what is *domain fact* vs. *mechanism*. The facts move; the mechanism stays.
2. **Design the data shape from the working code** — the fields you actually
   needed, not the fields you imagine. Prefer flat, obvious TOML.
3. **Ship the built-ins as data too.** The hardcoded values become the
   built-in layer expressed in the same schema — they double as documentation
   and as the test fixtures.
4. **Wire the three Cs**: layered composition (built-in → global → project →
   inline), merge-by-name override, conventional drop-in location, explicit
   error handling appropriate to optional versus required data.
5. **Test the engine against data, not constants.** The unit tests feed
   crafted packs/tables; adding a domain never adds a test of the engine.
6. **Document the drop-in** (one example file in `examples/`, one line in the
   relevant doc) — a pluggable seam nobody knows about is a hardcoded list
   with extra steps.

## Relationship to the other doctrines

- **Functional cohesion** (see the `functional-cohesion` skill) decides *where
  units live and how they connect*; the three Cs decide *what a unit is made
  of*. They compose: the target is a cohesive, loosely-coupled module whose
  knowledge is pure data behind a narrow seam.
- **Library/consumer split**: libraries expose structs/API seams and pure-data
  contracts; consumers supply the UI and the operator's config. A library that
  hardcodes consumer knowledge violates both doctrines at once.
- **TDD**: data-driven engines are the easiest things to test — the fixture
  *is* a pack. If testing requires patching constants, that's the three-Cs
  smell showing up in the test suite.

## Checklist

- [ ] Does any list/constant/table here encode **language- or domain-specific
      knowledge**? → candidate for data.
- [ ] Is there an inline `json!` / literal schema or config? → move to a data
      file with an overridable property.
- [ ] Can an operator add/override a knowledge unit **without recompiling**
      (drop-in file, merge-by-name)?
- [ ] Does loading handle malformed units according to the contract, without
      silently weakening required configuration or safety?
- [ ] If you hardcoded to ship (correct choice!): is the **circle-back
      flagged** (comment or issue)?
- [ ] Are the built-ins expressed **in the same schema** as the drop-ins?
- [ ] Did the safety floors stay in **code** (only the content moved to data)?

---

Adapted from Shawn Hartsock's [newt-agent](https://github.com/Gilamonster-Foundation/newt-agent/tree/main/.newt/bundled-skills/three-cs) `bundled-skills/three-cs`, Apache-2.0. **Modified from the original**: the "What 'good' looks like" example was genericized — the source version cites specific `newt-core`/`newt` internals, which would send a reader here chasing a codebase this repo has no other reason to reference.

Shepherd adaptation: the loading examples now distinguish optional packs
from required or security-sensitive configuration; they do not authorize
silent fallback for the latter.
