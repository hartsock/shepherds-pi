---
name: herdr-helpers-tab
description: Recreate a herdr "Helpers" tab — a controller pane plus N idle CLI-agent panes, ready for another agent to dispatch work into
argument-hint: "[count]"
---

# Setup the Helpers Tab

Recreate a herdr tab named `Helpers`: one controller pane on top, and below
it a row of equal-width panes each running a bare, idle CLI coding-agent
session (e.g. `pi` — see `skills/pi-install` and
`skills/pi-inference-backend` in this repo). The panes are a dispatch
pool — meant for another agent to hand work into, not for direct
interactive use.

Trigger phrase: **"Setup the Helpers Tab"**. Default count is 4 panes unless
told otherwise.

Which CLI/model each helper pane runs is a local configuration choice, not
part of this skill — launch whatever the operator's default agent CLI is
(invoked bare, no flags), so it picks up whatever backend/model is already
configured as that CLI's default.

## Prerequisite

`herdr` itself: `brew install herdr` (macOS/Linuxbrew) — or see
[herdr.dev](https://herdr.dev) for other install paths. This skill assumes
the `herdr` CLI is on `PATH` and its socket-API server is already running
(the `herdr` command starts it automatically on first launch).

## Procedure

1. Check for an existing `Helpers` tab: `herdr tab list`. Reuse it if
   present; otherwise create one focused: `herdr tab create --label Helpers
   --focus`. Note the resulting controller pane's `pane_id`.

2. Split the controller pane **down** to reserve the bottom of the tab for
   the helper row (ratio ~0.34 keeps the controller pane as the top third):
   `herdr pane split --pane <controller_id> --direction down --ratio 0.34`
   → returns the new bottom pane's `pane_id`.

3. Split that bottom pane **right, ratio 0.5**, repeatedly to divide it into
   N equal columns. For N=4: one split right (0.5) gives two halves, then
   split each half right (0.5) again gives four equal panes. In general,
   for N panes (N a power of 2), do `log2(N)` rounds of right-splits at
   ratio 0.5 starting from the single bottom pane, always splitting the
   newest/rightmost remaining pane at each step until N panes exist. For a
   non-power-of-2 N, split with decreasing ratios (`1/N`, `1/(N-1)`, …) so
   each resulting pane is equal width.

4. Launch the CLI agent bare (no model/provider flags) in each of the N
   panes: `herdr pane run <pane_id> <agent-command>`.

5. Label them for the roster in launch order: `herdr pane rename <pane_id>
   01` (…02, 03, …).

6. Most CLI agents that ship a herdr integration self-report their agent
   identity and session once launched (`herdr integration status` shows
   which are wired up; `herdr integration install <agent>` if not) — no
   manual `herdr pane report-agent` call is normally needed. Confirm with
   `herdr pane list` that each pane shows the expected `"agent"` field.

## Verify

`herdr pane read <pane_id> --lines 3` on each helper pane — `agent_status`
should read `"idle"` and the pane's status line should show the CLI is up
and waiting for input.

## Related

Once the panes exist, driving actual work through them — dispatching
briefs, verifying pickup, monitoring by artifact instead of by title,
steering corrections back to the owning pane — is a separate, larger
discipline: see Shawn Hartsock's
[`herdr-dispatcher`](https://github.com/Gilamonster-Foundation/newt-agent/blob/main/.newt/bundled-skills/herdr-dispatcher/SKILL.md)
skill (distilled from ~60 real multi-lane merges). This repo only covers
standing the panes up; that skill covers running a fleet through them.
