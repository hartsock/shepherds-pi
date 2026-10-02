---
name: herdr-flock
description: Run one project as a herdr flock. One tab holds a shepherd, an out-group reviewer and four helpers. Work moves through on-disk lanes and a gated pipeline (brief, helper push, reviewer verdict, operator yes, merge) that holds when nobody is watching.
argument-hint: "<project> [helpers=4]"
---

# Run a Flock

One project per herdr tab, named for the project:

```
┌──────────────────────┬──────────────────────┐
│ shepherd             │ reviewer             │
├──────────┬───────────┼──────────┬───────────┤
│ helper1  │ helper2   │ helper3  │ helper4   │
└──────────┴───────────┴──────────┴───────────┘
```

Build it the way [herdr-helpers-tab](../herdr-helpers-tab/SKILL.md) builds
its row: split the first pane down (ratio ~0.34), split the top right (0.5)
for the reviewer, then split the bottom into four equal columns. Rename the
panes `shepherd`, `reviewer` and `helper1`…`helper4`. Which CLI and model run
in each pane is local configuration. The one composition rule is below.

This skill is the governance layer. For the dispatch loop (briefing,
inspecting, steering one helper), read [docs/shepherding.md](../../docs/shepherding.md).

## Roles

| Role | Does | Never |
|---|---|---|
| **Shepherd** | Owns the operator conversation, briefs, the review queue, merges, cleanup | Implements a lane itself (small post-review fixes excepted); merges a draft; posts as the operator without sign-off |
| **Reviewer** | Reads one PR at one commit, writes one verdict file | Edits code, pushes, merges |
| **Helper** | Carries one lane in its own worktree and branch, pushes through hooks | Merges, bypasses a hook, changes shared config, speaks for the operator |

**The reviewer is a different model family from the shepherd.** That's
deliberate. Models favour output that resembles their own (LLM
self-preference bias), as people favour their in-group, and an out-group
reviewer catches what the author's family reads past. Mixing families
among the helpers helps too, but matters less.

## Lanes live on disk

A lane is a directory, `.handoff/<lane>/`:

- `BRIEF.md`: written by the shepherd. It holds one result, the owned files or worktree, the evidence to return, and any limits.
- `PROGRESS.md`: one line per step, appended by the helper, so a restart can resume.
- `RESULT.md`: the head SHA, then per item the mechanism at `file:line` and the red and green output.

The helper's pane title and status are cues, not evidence. The files and the
remote branch are the evidence.

## The pipeline

1. **Brief.** The shepherd writes `BRIEF.md` and dispatches it to an idle
   helper, then confirms the helper picked it up (its status goes to working,
   or it replies). Text reaching a pane is not pickup.
2. **Build.** The helper works test-first. A fix ships with a test shown
   failing without it ([tdd-red-green-blue](../tdd-red-green-blue/SKILL.md)).
3. **Push.** The helper pushes through the project's pre-push hook, then reads
   the remote ref back to confirm.
4. **Review.** The shepherd queues the PR for the reviewer. The reviewer
   writes `reviews/PR-<n>.md`, whose second line is
   `**Verdict: MERGE|FIX-FIRST** — <full head SHA> …`.
5. **Fix rounds.** On FIX-FIRST, the shepherd copies the verdict into a new
   lane brief for the same helper. Each round is re-reviewed.
6. **Merge.** Merge only when all of these hold:
   - the verdict says MERGE;
   - it names the exact head being merged (`--match-head-commit`);
   - CI is green on that head;
   - for a high-risk PR, the operator has said yes.

   A merge commit pushed after review (a conflict resolution, say) gets its
   own delta review first.
7. **Clean up.** Remove the worktree and delete the branch.

## Enforcement

Each rule closes a failure that happened.

| Rule | Prevents |
|---|---|
| Cap active build lanes (2 on a 16-core box). A lane is active until its `RESULT.md` exists. | Concurrent builds exhausting memory |
| Dispatch only into an idle pane, and confirm pickup | Briefs typed into a busy pane, stranded for hours |
| One review queue: on each verdict, send the next queued PR | A reviewer idle for hours behind a scheduler waiting on a stale timestamp |
| A helper never ends its turn waiting on a background job | Lanes that look done but stopped half-way |
| Run the narrow tests for the change, never the full suite in a loop | Small-context helpers burning hours on unrelated flakes |
| Check `git config --show-origin --get-all core.hooksPath` before every push | Hooks silently disabled for every worktree by one script |
| Kill only the PID you recorded at launch, never by pattern | One lane killing another lane's push |
| Never use the shared `git stash`, and never change shared git config | Cross-lane clobbering |
| Never `--no-verify`, except a written, narrow, operator-approved exception with evidence | A gate that quietly stops gating |
| Leak-check every outbound text: host names, local paths, session links | Private detail in public history |
| Draft PRs are untouchable | A "merge on green" firing on held work |
| Diagnose with causal signals, not elapsed time | "It timed out, so it's load" guesses |

## Watch the helpers

Small local models stall: they overflow their context, loop, or stop early.
Check them on a fixed interval (30 minutes works). For each helper:

1. Read its status, the screen tail and the lane files' modification times.
2. If it's stuck, start a fresh session and send "You are lane `<lane>`. Read
   `BRIEF.md` and `PROGRESS.md` and resume where `PROGRESS.md` says." Then
   confirm pickup.

Set the CLI's context window to what the server actually gives each session.
A server that splits its window across parallel slots gives each session
less than the model's nominal window.

## Related

- [herdr-helpers-tab](../herdr-helpers-tab/SKILL.md): building the pane row
- [docs/shepherding.md](../../docs/shepherding.md): brief, inspect, steer
- [`herdr-dispatcher`](https://github.com/Gilamonster-Foundation/newt-agent/blob/main/.newt/bundled-skills/herdr-dispatcher/SKILL.md): dispatch mechanics from many real multi-lane merges
