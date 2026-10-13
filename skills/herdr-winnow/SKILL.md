---
name: herdr-winnow
description: Run a herdr flock that winnows a codebase. It finds duplicated code and duplicated or wordy prose, refactors one finding per lane without changing behaviour, then re-scans. It stops when a round finds nothing worth cutting. Follows Fowler's Refactoring.
argument-hint: "<project> [rounds=5]"
---

# Winnow a Codebase

A [herdr-flock](../herdr-flock/SKILL.md) with one job: make the code say
everything once and only once. The tab, roles, lanes, pipeline and
enforcement are the flock's. This skill adds the loop, the order of
moves for each finding, and what a lane must prove.

> Refactoring: a change made to the internal structure of software to make
> it easier to understand and cheaper to modify without changing its
> observable behavior. — Martin Fowler, *Refactoring*, p50
> ([notes](https://gist.github.com/deanhunt/1c0ca8c5fe17b9b4f34a))

A winnow lane wears one hat (Beck's two hats, p54). It restructures and
adds no function. If a lane turns up a bug or a missing feature, record
it as separate work and don't fix it in the lane.

## The loop

Each round runs from a fresh `main`:

1. **Scan.** A read-only helper runs the [scan](#scan) and writes
   `.handoff/winnow/ROUND-<n>.md`, one line per finding, biggest saving
   first: `<id> <tag> <saving> <locations> <proposed move>`.
2. **Triage.** The shepherd applies the Rule of Three (p58). Three or more
   copies get refactored. Two copies get refactored only when they must
   change together (shotgun surgery, p80). Otherwise note them and move on.
   Don't brief a finding in a file another open lane is moving or
   splitting; hold it and re-scan after that lane merges.
3. **Brief.** Give each lane one finding, or one cluster inside one unit.
   The flock's cap on active lanes applies.
4. **Refactor, review, merge.** Use the flock pipeline, with the lane
   evidence and reviewer checks below.
5. **Record.** Append the round to the [ledger](#ledger).
6. **Stop** when a scan finds nothing that passes triage, when net lines
   didn't fall this round, or when the round cap is reached. Report the
   ledger to the operator. Count "net lines didn't fall" only for rounds
   that briefed lanes.

Refactoring is "something you do all the time in little bursts" (p58).
Keep rounds small, so each merge is easy to review and the next scan runs
against code that has already shrunk.

## Scan

- **Duplicated code:** `tools/dupes --lines 6 <src>`.
  See [the contract](#toolsdupes). A hit inside an inline test module (e.g.
  Rust `#[cfg(test)]`) is test code; check scope before briefing it.
- **Duplicated prose:** `tools/dupes --lines 3 <docs>` finds copied
  passages. A reader finds paraphrase: the same idea explained in two
  places.
- **Wordy prose:** review with [concision](../concision/SKILL.md).
  Run its `ai-tells` tool if it's already installed.
- **Over-engineering:** use [ponytail-audit](https://github.com/DietrichGebert/ponytail/tree/main/skills/ponytail-audit)
  tags (`delete`, `stdlib`, `native`, `yagni`, `shrink`). A wrapper that
  only delegates is duplication with an extra hop.

## The ladder, per finding

Stop at the first rung that holds
([ponytail](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)):

1. **Is one copy dead?** Delete it.
2. **Does an existing helper already do this?** Point every copy at it.
3. **Does the stdlib or platform do it?** Use that.
4. **Do the copies differ only in data?** Extract the data into a table
   that one mechanism reads ([three-cs](../three-cs/SKILL.md)). Don't add
   a branch per copy.
5. **Only then, extract a function.** Name it for its intent, not its
   steps (p76). Put it in the unit that owns the job, never in `utils`
   or `common` ([functional-cohesion](../functional-cohesion/SKILL.md)).
   Expose the narrowest interface that works.

For prose: delete the repeat, or keep one canonical home and link to it
from the others. Then compress the survivor with
[concision](../concision/SKILL.md).

## What a lane must prove

This is the Blue phase of [tdd-red-green-blue](../tdd-red-green-blue/SKILL.md),
with the tests built first (p7).

1. **Cover every copy.** If a copy has no test, add a characterization test
   that passes on the old code. Show that it bites: break that copy, watch
   the test fail, then restore the copy.
2. **Take small steps.** Compile and run the narrow tests after each one
   (p20, p50). When moving code, move it verbatim first and merge the
   copies in a second step.
3. **Keep assertions fixed.** Test assertions don't change. An edited
   assertion means behaviour changed, so the lane is no longer a refactor.
4. **Stay in scope.** No performance work (p32). No change to a published
   interface unless the brief allows it (p65).

`RESULT.md` holds the head SHA, the finding id, `git diff --shortstat`,
the test commands with their output, and a `dupes` re-run that no longer
lists the finding.

A prose lane lists the facts, commands and links that must survive. The
reviewer checks each one. There's no quota for how much to cut.

## Reviewer checks

On top of the flock's verdict file:

- The diff changes structure only. The only test changes are new
  characterization tests.
- Shared code lives in a unit named for its job.
- Every new abstraction has at least two callers today. If the only users
  of a method are tests, it's speculative generality (p83).
- Net lines went down.

## Ledger

`.handoff/winnow/LEDGER.md` gets one row per round:
`round | findings | duplicated lines | net lines | PRs`.
"Duplicated lines" is the sum of the `saving` column from `dupes`. That
sum may only go down. If it rises, a lane added duplication: stop the loop
and fix that lane before starting the next round.

## `tools/dupes`

A single job ([unix-philosophy](../unix-philosophy/SKILL.md)), stdlib
Python only.

```
dupes [--lines N] [--min-count K] PATH...
```

- **What it finds:** blocks of N or more lines that appear K or more times
  (defaults 6 and 2). Leading and trailing whitespace is ignored. Blank
  lines and punctuation-only lines are skipped. Files inside a git repo are
  listed with `git ls-files --exclude-standard`, so git-ignored output such
  as `target/` and `node_modules/` is never scanned.
- **Known overlap:** a run nested in a longer block is reported on its own
  only when it has more copies than the enclosing block. Its `saving`
  then overlaps the enclosing block's `saving`, so do not add the two.
  Read the rows as candidates, not as a total.
- **Output:** one block per line on stdout, tab-separated:
  `copies lines saving path:line…`, biggest saving first.
- **Exit status:** 0 if nothing repeats, 1 if something does, 2 on a usage
  error.
- **Rule of Three:** pass `--min-count 3` to report only blocks with
  three or more copies.
- **Self-check:** `python3 -m unittest discover skills/herdr-winnow/tools`.

It finds copies, not paraphrase. Reworded or reflowed text needs a reader.
If the project already uses a clone detector (jscpd, PMD CPD, pylint
`duplicate-code`), use that one instead.

## Related

- [herdr-flock](../herdr-flock/SKILL.md): tab, roles, lanes, pipeline
- [shepherd](../shepherd/SKILL.md): the brief, inspect and steer loop
- [concision](../concision/SKILL.md): the prose passes
