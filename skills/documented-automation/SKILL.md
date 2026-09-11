---
name: documented-automation
description: Guide a pi helper in documenting repository-writing automation where its effects appear. Use when machine identities author, merge, tag, or write in another repository and reviewers need auditable identity, authority, constraints, and source.
---

# Shepherd documented automation

You choose the target repository and review the declaration. Automation that
writes there must be explained there, beside the history or files it changes.
The helper documents the boundary; it does not change automation, permissions,
or access, publish, or start another delegation chain.

For helper selection, isolation, dispatch, integration, and blocked states, follow the [shared shepherd loop](../../docs/shepherding.md).

## Brief the declaration

Give pi the target, owned files, machine-authored evidence, account names, and source location. State whether the task permits edits or is review-only.

> Inspect the repository and its machine-authored history. Take each acting
> identity's exact name from evidence. Document what it does, what its credential
> can do, what the program or repository controls restrict, and where the source
> lives. Quote source constraints exactly and identify their revision. Keep the
> declaration where readers meet the effects. Report files, checks, and
> unsupported claims. Do not change automation, credentials, or access.

## Inspect the result

Read the declaration against the history and source, not the helper's summary.

- Are every authoring, merging, tagging, and writing identity named exactly?
- Are intended actions separate from the credential's wider authority?
- Are constraints quoted from source rather than paraphrased?
- Can a reader reach the named file and revision to audit each quote?

If history contains a machine account, search for its exact name with
`git grep -n -F '<machine-account>' -- .`. Zero hits is a finding, not an exemption.

## Steer and accept

Return a located correction when a claim blurs code and credential authority,
omits an identity, or paraphrases a constraint. Accept when a reader can find
the actor, action, constraint, and source without guessing. Consult the
[documented-automation doctrine](../../docs/documented-automation-doctrine.md).

Model: GPT-5 | Harness: Codex | Operator: Shawn Hartsock | Time: 13:10 EDT | Date: 2026-09-11
