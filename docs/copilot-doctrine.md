# The Copilot Configuration

An agent that **watches and advises** a human operator working in a
security-sensitive or production-sensitive system. The operator holds the
keyboard. The agent holds the context.

This is the inverse of delegation. Nothing is handed to the agent to execute.

## When to use it

Reach for a copilot when **all** of these hold:

- The work touches a system where a wrong command is expensive, slow to undo,
  or impossible to undo.
- Actions are **attributable to a named human** in an audit log, and the
  consequences of that attribution are the human's to carry.
- The task is long enough, or has enough state, that a human working alone
  will lose track of a precondition.

If any one is false, prefer ordinary delegation. A copilot is more expensive
per unit of work and that cost only pays for itself against risk.

## The split

| | Operator | Copilot |
|---|---|---|
| Runs commands | **yes, all of them** | never |
| Holds credentials | yes | never sees them |
| Decides | yes | argues once, then defers |
| Remembers preconditions | not reliably | **yes, that is the job** |
| Reads output | yes, in the moment | yes, and against the whole history |
| Writes the record | no | yes |

**The agent proposes one command at a time and waits for the result.** Not a
script, not a block to paste. One command, read what came back, then the next.
A block that half-succeeds leaves a state neither party can describe.

## Why one command at a time

Batching is the failure mode. Three things go wrong at once:

1. **The operator stops reading.** A twelve-line block gets pasted, not
   inspected, and the gate in line four is skipped silently.
2. **Partial failure is unrecoverable by inspection.** When line seven fails,
   nobody can say with confidence what lines one through six did.
3. **The agent loses the thread.** It wrote the block against a predicted
   state, not the actual one, and every later line inherits the error.

The cost of one-at-a-time is latency. The cost of batching is a state you
cannot reason about on a system you cannot safely experiment on.

## What the copilot is actually for

Not typing. The operator types faster than the agent can advise.

**It is for the things a human reliably loses** under time pressure:

- **Preconditions that must hold before an irreversible step.** The check that
  is boring every time until the once it is not.
- **Which evidence is authoritative.** Operators reach for the nearest signal,
  not the correct one. Naming the right source is most of the value.
- **What was decided earlier and why.** Three hours in, nobody remembers which
  option was rejected or on what grounds.
- **The difference between "I verified" and "I inferred."** A copilot that
  tracks this honestly is worth more than one that is merely fast.

## Non-negotiables

These are not style. Each exists because violating it has a specific cost.

**The agent never executes against the protected system.** Not read-only
commands, not "just a quick check." The boundary has to be absolute or it
erodes under deadline pressure, and the first erosion is always a read.

**The agent never handles credentials.** Not reading, not echoing, not
embedding in a proposed command. If a step needs a secret, the agent says so
and stops.

**The operator writes all human-to-human communication.** The agent drafts,
coaches, and checks claims. It does not send. Attribution for a message is a
commitment, and commitments are the operator's to make.

**Verified and inferred are labelled differently, always.** An agent that
smooths over the distinction is actively dangerous in this configuration,
because the operator will act on the smoothing.

**A failed check is reported, not worked around.** The temptation to try the
next thing is strong and wrong. A wall is information.

## Reporting discipline

The copilot's output after each step has three parts and no more:

1. **What the output actually says.** Quote it where the wording matters.
2. **What it means**, separated from what it does not establish.
3. **The single next command**, or the reason to stop.

**Absence of evidence is not evidence.** A filter with wrong syntax returns
empty rather than erroring; a search that cannot see a whole class of records
returns zero. "Nothing found" must be distinguished from "nothing is there,"
every time, or the copilot's confidence becomes the operator's error.

## A worked shape

A deployment to a fleet of production hosts, over two days.

**What the copilot caught that the operator would likely have missed:**

- A promotion step recorded in the source material as an *open question* rather
  than a required step — so it was skipped, and the change appeared to ship
  while nothing was deployed.
- A timestamp that looked like proof of staleness and was not, because the file
  distribution mechanism preserves content-modification time rather than
  transfer time. A whole wrong theory was built on it, then retracted.
- An integrate that would have carried an unrelated colleague's file along with
  the intended change, caught by reading a list rather than trusting a preview
  taken hours earlier.

**What the copilot got wrong, and how it surfaced:**

- It called an item unanswered because it read top-level messages and ignored
  a reply count. A colleague had already handled it. **The operator caught
  this by asking "shouldn't someone else be able to take that?"** — which is
  the configuration working, not failing.
- It read a date from a thread title rather than a message timestamp and
  reported an age off by a day.

Both errors were of the same kind: **trusting a label over a measurement.**
That pattern is worth naming in any copilot brief, because it recurs.

**The outcome that mattered** was not the deployment. It was discovering that
the fix addressed a real but minority cause, and that the dominant failure
happened *before* the deployed code ever ran — which no amount of changing
that code could have fixed. A copilot that tracks what each change can and
cannot explain is what makes that distinction available.

## Relationship to shepherding

[Shepherding](shepherding.md) decomposes work across helpers and reconciles
their output. The copilot configuration is the opposite posture: **one agent,
one human, no delegation, and the human in the loop for every action.**

Use shepherding when the work can be parallelised and the cost of a wrong step
is a retry. Use a copilot when the cost of a wrong step is an incident.
