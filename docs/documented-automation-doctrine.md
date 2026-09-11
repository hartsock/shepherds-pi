Reference doctrine for the [documented-automation shepherd skill](../skills/documented-automation/SKILL.md).
Read the relevant section when preparing a helper brief; the skill defines
how to supervise the work. Examples describe design choices, not permission
to expand the assigned task.

# Documented automation

## The claim

**Automation that writes to a repository must be declared inside that
repository, where a reader meets its effects; otherwise, correct automation
is indistinguishable from compromise.**

Automation is part of a repository's operating model when it changes that
repository. Its declaration belongs beside the resulting history, generated
files, or merge requests. Source documentation alone does not meet this need.

## The reasonable false alarm

A scheduled pipeline in one project opened and merged changes into a second
project using machine credentials. One machine account authored each merge
request. Another machine account merged it. No human approval appeared in the
record. The process was correct, limited, and working as designed.

The target repository explained none of this. Two independent reviewers, one
human and one agent, read the history as evidence of a compromised credential.
Both escalated. Both were wrong, and both reached a reasonable conclusion from
the evidence available to them.

The mechanism had documentation in the project that ran the pipeline. The
machine identities did not appear in the project receiving its changes. That
gap cost investigation time and triggered a credential-rotation scare.

## Declare effects where readers see them

The project being written to needs the declaration. A reader investigating its
history should not have to guess which other repository might contain the
writer. Documentation only in the source project helps its maintainers, not the
reviewer facing unexplained machine-authored commits in the target.

Place the declaration where it will survive the same review path as the
effects. Depending on the repository, that may be an automation policy, a
document beside generated files, or a short repository guide linked from the
affected area. The location matters less than whether a reader meets it while
following the evidence.

## Name what a reviewer must verify

| Required fact | What to record |
|---|---|
| Acting identity | The exact account name that authors, merges, tags, or writes |
| Permitted action | The paths and operations the automation is intended to perform |
| Constraint | The code, policy, checks, branch rules, or approval gates that limit it |
| Auditable source | The repository, file, and revision where the reader can inspect the mechanism |

If authoring and merging use different identities, name both and assign each
its action. Do not collapse them into a vague phrase such as "the automation
account."

## Quote constraints from the source

A paraphrase ages badly. It can outlive the control it describes, and a reader
cannot compare it with the implementation. Quote the controlling source and
link to its file and revision.

For example, suppose an invented `catalog-writer` proposes changes and an
invented `merge-service` merges them. The target repository could record:

> Source constraint, quoted from `policy.toml` at revision `abc1234`:
> `allowed_paths = ["catalog/**"]`
>
> Merge condition, quoted from the same source:
> `merge_when = "required_checks_pass"`

The quote makes drift visible. If the source changes, a reviewer can diff the
declaration against the new rule instead of trusting an old summary.

## Separate credential authority from code behavior

State what the credential can do and what the program chooses to do. These are
often different boundaries.

In the example above, the credential may have project-wide write authority
while `policy.toml` limits the program to `catalog/**`. The honest declaration
says both. Saying "the credential is limited to catalog files" would be false.
The path limit belongs to the code unless repository permissions enforce it
independently.

This distinction changes the review. A code defect may cross the program's
declared path boundary. A leaked credential may cross the wider permission
boundary. Readers need both facts to judge risk and response.

## Silence gets more expensive

The first reader investigates. The second escalates. The third stops trusting
the history. Each unexplained machine action makes the next one harder to
distinguish from abuse. Trust in a log is load-bearing; once readers discount
its authorship and approvals, the repository loses part of its audit trail.

Documentation does not make broad credentials safe. It makes expected machine
behavior recognizable, reviewable, and falsifiable. Controls still need least
privilege, tests, and monitoring appropriate to their risk.

## Shepherd review check

When history contains machine-authored commits, take the exact account name
from the history and search the target repository for it:

```sh
git grep -n -F 'catalog-writer' -- .
```

Zero hits is a finding. It means the repository records the effect but does not
declare the actor where a reviewer can discover it. Confirm that the final
declaration names the identity, action, constraint, and source, quotes the
source constraint exactly, and distinguishes credential authority from program
behavior.

---

Model: GPT-5 | Harness: Codex | Operator: Shawn Hartsock | Time: 13:06 EDT | Date: 2026-09-11
