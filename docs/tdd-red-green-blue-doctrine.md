Reference doctrine for the [tdd-red-green-blue shepherd skill](../skills/tdd-red-green-blue/SKILL.md).
Read the relevant section when preparing a helper brief; the skill defines
how to supervise the work. Examples describe design choices, not permission
to expand the assigned task.

# TDD — Red, Green, Blue

Three colors, one cycle, repeated in steps small enough to take minutes,
not hours:

```
RED    write a failing test that describes the next desired behavior
GREEN  write the minimum code that makes it pass
BLUE   clean up structure — no new behavior, every test still green
       (some traditions call this step "refactor" — same step, this
       repo names it for the color scheme: red, green, blue)
REPEAT
```

If a cycle is taking longer than a few minutes, the step is too big.
Split it into a smaller one.

## Red — write the failing test first

Ask, before writing anything:
- What is the **smallest** behavior worth specifying right now?
- What is the **simplest** input/output pair that proves it?
- If this test runs against today's code, will it fail **for the right
  reason** — missing behavior, not a typo or import error?

Structure with Arrange/Act/Assert:

```
# Arrange — set up inputs and dependencies
# Act        — call the unit under test
# Assert   — verify the observable outcome
```

A good test:
- has a name that reads like a sentence describing the behavior
  (`returns_zero_for_empty_input`, not `test1`)
- tests one behavior — one assertion, or a tightly related group
- fails before any implementation exists, and fails on the right line

**Never write more than one failing test before making it pass.** Stacking
failing tests loses the thread of which one you're driving toward.

## Green — the minimum implementation

- Write **only** enough code to make the current failing test pass.
- Hardcoding a return value is a legitimate Green step — the next Red test
  will force generalization. Don't skip ahead to the general solution
  before a test demands it.
- Do not add error handling, edge cases, or optimization the current test
  doesn't require. That belongs to a future Red step.
- Run the affected regression suite and required project checks, not just
  the new test. Broaden to the full suite when the change warrants it.

## Blue — refactor only when green

Only touch structure once every test passes:
- Remove duplication, in both code and tests.
- Rename for intent.
- Extract a function when a block does more than one thing.
- Simplify conditionals.
- Run the suite again — green after the refactor means behavior was
  preserved, not just that the code looks nicer.

**Never refactor with a failing test.** Get to green first; a red test
during a refactor means you can't tell whether you broke behavior or
were already broken.

## Repeat

Progress looks like a staircase of small cycles, each one hardening the
implementation toward the general case:

```
Cycle 1: empty input returns the default        → Red → Green → Blue
Cycle 2: single item returns that item           → Red → Green → Blue
Cycle 3: multiple items combine correctly        → Red → Green → Blue
Cycle 4: invalid input raises the right error    → Red → Green → Blue
```

## FIRST — what makes a unit test worth keeping

- **F**ast — runs in milliseconds; a slow suite stops getting run.
- **I**solated — no shared state with other tests; order shouldn't matter.
- **R**epeatable — same result every run, on any machine, at any time.
- **S**elf-validating — pass or fail, no human reading output to decide.
- **T**imely — written just before the code it drives, not after.

## Gotchas

| Pitfall | Fix |
|---|---|
| Writing implementation before the test | The test must exist and fail first — that's the whole discipline |
| Multiple failing tests stacked up | One at a time: get to green before writing the next red |
| Refactoring with a failing test | Get to green first |
| Test passes with zero implementation | The assertion is testing nothing — check it |
| Adding error handling nothing tests for yet | Write the failing error-case test first |
| Test named `test_1` or `test_login` | Name it after the behavior, not the feature area |
| Deleting a passing test because the code got simpler | Tests are the specification — don't delete, update deliberately |

## Related

`skills/functional-cohesion` in this repo covers *where* code should live;
this skill covers *how it gets proven correct as it's written*. They
compose: drive each cohesive unit's behavior through Red/Green/Blue rather
than writing a unit whole and testing it after.
