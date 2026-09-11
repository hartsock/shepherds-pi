---
name: unix-philosophy
description: Shepherd a pi helper building or reviewing a small CLI, script, or composable interface. Specify one job and an input/output contract, inspect actual composition and failure behavior, and steer away from unrelated modes or noisy output.
---

# Shepherd small, composable tools

You define the tool's job and integration contract; pi implements within
that boundary. Inspect whether another caller can consume the output and
detect failures without knowing the internals. For review-only work, ask
for findings instead of edits. Do not split a tool merely because it has
several flags or a long help page.

For helper selection, transport, and blocked-state handling, follow the
[shared shepherd loop](../../docs/shepherding.md).

## Brief the interface before the implementation

Specify the one job, owned files, expected input, output format, diagnostics,
exit behavior, and an actual downstream consumer. Prefer an existing format
and command over a new parser or service. If the target is a library, define
the narrow API and its caller rather than forcing a shell interface.

> Build the assigned tool for this one job and supplied input/output
> contract. Reuse existing components where practical. Keep result data
> on stdout, diagnostics on stderr, and meaningful failure exit statuses.
> Demonstrate it with the supplied downstream consumer and representative
> success, empty-input, and failure cases. Report commands, outputs, exit
> statuses, and changed files. No unrelated modes, services, or delegation.

Provide concrete examples in place of generic references to "the contract."
Separate edit ownership if multiple helpers build producer and consumer;
agree the record format and failure behavior before they start.

## Inspect composition

- Read the implementation and run or inspect the actual producer-to-consumer
  example. A plausible command in a report is not evidence that it ran.
- Check stdout, stderr, and exit status separately. Success may produce
  useful result data; silence means no decorative chatter, not no output.
- Check the promised empty-input and malformed-input behavior. In a shell
  pipeline, verify producer failures are visible rather than masked by a
  successful last command; use the shell's supported failure handling.
- Confirm the output needs no banner stripping or knowledge of internal
  formatting. Text, JSON, CSV, or another established format should fit
  the consumer; do not force text for an inherently binary artifact.
- Check that unrelated responsibilities did not enter through convenience
  flags. Split only when independent jobs and a useful interface justify it.

## Steer and accept

Return corrections as interface failures with evidence:

> The JSON consumer fails because stdout begins with "Done!". Move the
> progress message to stderr and rerun the same pipeline. Preserve the
> JSON schema and verify both streams and the exit status.

If pi builds a monolith, identify the unrelated job and ask for the smallest
seam. If it fragments a simple tool into many scripts, ask whether callers
now need unnecessary coordination. Accept when the assigned job composes
with its consumer and the supported failure cases are observable. Do not
silently turn a small tool request into a reusable platform.

The [Unix doctrine](../../docs/unix-philosophy-doctrine.md) gives background
on one-job tools, streams, and composition through narrow interfaces.
