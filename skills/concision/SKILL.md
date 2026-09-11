---
name: concision
description: Guide a pi helper through concise writing or revision. Use as the shepherd to brief the audience and purpose, review meaning and evidence, and steer a focused editing pass before accepting the draft.
---

# Shepherd concise writing

You are the shepherd. Give pi a bounded writing task, review its actual
draft, and return specific corrections. The helper writes; you own whether
the result preserves the user's meaning and serves the reader. If pi is
the shepherd, the same instructions apply to its helpers. A helper given
an editing brief should edit, not start another delegation chain.

For helper selection, transport, and blocked-state handling, follow the
[shepherd workflow](../shepherd/SKILL.md).

## Brief the helper

Name the artifact or output path, audience, reader's next action, source
material, and permitted edits. Identify facts, qualifications, citations,
commands, and user wording that must survive. Say whether pi should return
a draft or edit the assigned file. Do not delegate publishing implicitly.

Use three passes: separate unrelated ideas, compress each idea, then
remove distracting writing habits. Give pi only the relevant guidance
from [the doctrine](../../docs/concision-doctrine.md), not an instruction
to read everything and decide its own assignment.

Example brief, with task-specific details filled in:

> Revise the assigned draft for the named audience and reader action.
> Preserve the supplied facts, caveats, links, commands, and voice. Separate
> unrelated ideas, remove repetition, and use concrete subjects and verbs.
> Keep explanations needed to use the commands. Return the revised draft
> and briefly flag any unresolved factual ambiguity. Do not publish or
> delegate. Stay within the assigned artifact.

## Inspect the draft

Read the revision against the source, not just the helper's summary.

- Can a stranger identify the result and what to do next?
- Did compression remove evidence, a condition, a limitation, or a useful
  explanation? Shorter is not automatically better; do not set a reduction quota.
- Are claims still supported, uncertainty still visible, and links intact?
- Does each paragraph carry one idea with a clear actor and action?
- For new outward prose, remove em dashes, decorative emoji, stock AI
  vocabulary, hollow intensifiers, and repeated conclusions. Preserve
  quotations, code, attributed material, and the user's explicit style choices.

The bundled [ai-tells tool](tools/ai-tells) can supplement this review if
its Node and detector dependencies already exist. Its score is not proof
of accuracy or authorship. If unavailable, review manually; do not turn
a writing task into dependency installation.

## Steer and accept

Return a located defect and a bounded correction, for example:

> The second paragraph dropped the condition under which retries stop.
> Restore that condition in one sentence; keep the shorter introduction.

Avoid prompts such as "make it punchier" that encourage another blind cut.
Inspect the next revision for both the correction and lost meaning. Accept
when the reader can act and further cuts would remove useful content.
If a material fact is missing, report that gap instead of asking pi to
invent it. Do not keep polishing an accepted draft without a new reason.

Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:54 EDT | Date: 2026-09-11
