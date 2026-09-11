# Guiding pi helpers

The shepherd owns the user's task, decomposes work, assigns a bounded brief,
checks artifacts and evidence, and decides what correction or next step is
needed. A pi helper carries out its brief. The shepherd can be Codex, Claude,
pi, or another agent capable of coordinating the helpers.

Install the shepherd skills where the controlling agent reads skills. A
worker does not need the entire doctrine library: send it the relevant
instructions, source paths it can access, and acceptance criteria. If a
reference lives only on the shepherd's machine, include the needed excerpt
in the brief instead of sending an inaccessible path.

## Choose the guidance

| Work assigned to pi | Shepherd skill | Evidence to collect |
|---|---|---|
| Write or revise a document | [concision](../skills/concision/SKILL.md) | Draft or diff compared with source facts and reader needs |
| Implement behavior or fix a regression | [tdd-red-green-blue](../skills/tdd-red-green-blue/SKILL.md) | Meaningful pre-fix failure, passing fix, cleanup results |
| Extract configurable knowledge | [three-cs](../skills/three-cs/SKILL.md) | Data boundary, supported override, preserved defaults and invariants |
| Build a CLI or composable interface | [unix-philosophy](../skills/unix-philosophy/SKILL.md) | Actual consumer example, output streams, failure statuses |

Combine only the guidance the task needs. For example, use TDD to supervise
a CLI bug fix and Unix philosophy to check its output contract. Do not
force a document edit through TDD or load four full doctrines into one brief.

## Dispatch, inspect, steer

1. Resolve the assigned helper and inspect its state before sending work.
   In Herdr, follow the [Herdr skill](../skills/herdr/SKILL.md) and installed
   CLI instructions. This guide does not create a new workspace or flock.
   Before the first brief to a newly started agent, send the trivial request
   `reply with one word: ready` and wait for its actual reply. A successful
   dispatch proves only that text reached the pane, not that the agent's input
   loop consumed it.
   An immediate `idle` state or `interactive_ready: true` is not sufficient
   readiness evidence; the same inspect-don't-assume rule applies. This
   handshake costs one round trip and prevents a silent failure: an unconsumed
   brief looks like a working helper that has not reported, and a human often
   finds it first.
   Once a worker has responded this session, do not repeat the handshake before
   every assignment.
2. Give the helper one concrete result, owned files, constraints, and the
   evidence to return. State whether it may edit or only review. Helpers
   sharing a checkout need disjoint ownership; dependent changes wait for
   the prior artifact or use an explicitly chosen isolation strategy.
3. Submit the brief through the agent transport. For Herdr, use
   `herdr agent prompt <target> <brief>` with a live name or pane ID.
   Dispatch independent assignments before waiting for their results.
4. Read progress and final artifacts. An idle or done state is a cue to
   inspect, not proof of correctness. A working helper should not receive
   repeated copies of the same assignment. On a timeout or blocked state,
   inspect the cause before retrying; report a missing prerequisite rather
   than repeatedly resubmitting an impossible task.
5. Return a specific defect, the evidence that exposes it, and the smallest
   correction. Keep the correction with the helper that owns the change.
   If feedback repeats without progress, narrow the task or resolve the
   missing context instead of issuing another vague retry.
6. Accept when the assigned behavior or artifact satisfies its criteria.
   Report checked results, unverified claims, and remaining limitations.
   An accepted helper result does not itself authorize publication or merge.

Keep checkpoint messages short, but preserve commands and failure details
needed to verify the work. The shepherd should not substitute a polished
summary for missing evidence, and a helper should not recursively delegate
unless that role has explicitly been assigned.

Model: GPT-5 | Harness: Codex | Operator: Shawn Hartsock | Time: 13:24 EDT | Date: 2026-09-11
