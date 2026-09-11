Reference doctrine for the [concision shepherd skill](../skills/concision/SKILL.md).
Read the relevant section when preparing a helper brief; the skill defines
how to supervise the work. Examples describe design choices, not permission
to expand the assigned task.

# Concision — decompose, compress, de-tell

## The claim

**Concision is not fewest words. It is fewest words that still let the
reader act with understanding.** Those two diverge exactly where a
mechanism needs explaining, which is where most editing cuts hardest and
does the most damage. Compress outward writing to the bone; leave the
runbook long enough to teach.

This is a real, reported problem: writers whose natural style reads as
machine-generated to colleagues, regardless of who or what actually wrote
it. The research on AI-text detectors is that these surface markers
(em dash frequency, certain vocabulary, sentence-rhythm patterns) do not
reliably distinguish human from machine text, and detectors misfire
often. None of that matters for this skill's purpose: **readers respond
to these markers whether or not a detector would.** Optimize for how the
writing will be received, not for what a detector would conclude. Don't
argue the research at the reader — write so the question never comes up.

---

## Three passes, in order

Each pass does one job. Running them out of order wastes work:
compressing a document that should have been three documents produces a
shorter wrong document.

```
1. DECOMPOSE   is this one idea or several?
2. COMPRESS    fewer words, same information — Williams + Lanham
3. DE-TELL     strip machine-read patterns — ai-tells
```

---

## Pass 1. Decompose

**If a draft is long because it holds several ideas, stop editing.**
Trimming a document that covers five separate claims yields a shorter
document that still covers five separate claims — the wrong artifact,
just smaller. The unit of thought is not the unit of publication:
fifteen connected ideas may not be one long document, they may be
fifteen short ones.

Signs you're still in pass 1, not pass 2:
- The outline has more than one top-level claim.
- You can't state the point in one sentence.
- Cutting words makes it *less* clear, not tighter — a sign the cut
  removed a needed transition between two actually-separate ideas.

---

## Pass 2. Compress

### Williams, four moves

| Move | Ask |
|---|---|
| **A. Concision** | Which words can disappear without losing information? |
| **B. Characters and actions** | Who is acting? Make them the subject. What are they doing? Make it the verb. |
| **C. Cohesion** | Does each sentence open with something the reader already knows, and end with what's new? |
| **D. Coherence** | What is this paragraph about? Does that thing occupy the subject position in most of its sentences? |

Pass A removes: throat-clearing, ceremonial transitions, duplicated
explanation, sentences that announce an explanation is coming, hedging
qualification, repeated summary.

**Pass B matters most for technical writing.** Nominalizations hide the
actor:

```
An evaluation of the scheduler was performed.       →  We evaluated the scheduler.
The implementation of the fix was completed.        →  We fixed it.
Consideration was given to the proposal.             →  The committee considered it.
```

Watch for `-tion`, `-ment`, `-ance`, `-ity` nouns propped up by `perform`,
`conduct`, `provide`, `achieve`, `make`, `do`.

### Lanham's lard factor

Count words, revise, count again: `(original - revised) / original`.

Unedited professional prose typically compresses by about **50%**. Use
that as a stopping signal, not a target: a draft that won't compress by
a third probably wasn't padded, and cutting further starts removing
content instead of fat.

### What "fewest words" isn't

Fewest words that still let the reader act with understanding — those
diverge exactly where a mechanism needs explaining. A runbook cut four
times toward "shortest" can get worse, not better, if each cut removed
the reasoning a reader needs to improvise when reality doesn't match the
script exactly:

- Open with the concept, not the command, when the command alone won't
  transfer: state *what's being fixed* before *how*.
- Explain non-obvious commands inline rather than assuming familiarity.
- Turn a gate into a condition: "X is only needed if Y doesn't happen,"
  not a bare "get approval for X."

A reader who understands what's being fixed can improvise when reality
doesn't match the runbook. One holding only commands cannot.

**This applies to runbooks, incident notes, and handoffs — documents a
stranger has to act on. It applies much less to outward status writing**,
where the reader already has context and length itself is the whole
problem.

### Length by audience

| Artifact | Target |
|---|---|
| A status update, chat message | as short as carries the instruction |
| A summary meant to link to more detail | short, with the long version linked |
| A runbook a stranger will follow | commands, stop conditions, nothing else |
| A postmortem, changelog, deep-dive | as long as the evidence needs |

---

## Pass 3. De-tell

### Hard bans — no exceptions in outward writing

1. **Em dash.** Replace with a comma, a period, parentheses, or two
   sentences. One carve-out: a list item opening with a bolded term or
   link (`- **Term** — gloss`) is typography, not prose. Nothing else.
2. **Emoji.** None in headings, none mid-sentence. A status marker in an
   operational table is the one exception, and only where it replaces a
   word.
3. **Tier-1 AI vocabulary** — words that read as machine-written on
   sight: `delve`, `robust`, `comprehensive`, `leverage`, `paradigm`,
   `landscape` (as metaphor), `realm`, `tapestry`, `testament to`,
   `embark`, `seamless`, `crucial`, `pivotal`, `underscore`, `showcase`.

### Also strip

- Hollow intensifiers: `genuine`, `truly`, `real` (as in "a real
  improvement"), `to be honest`, `it's worth noting that`.
- Vague endorsement: `worth reading`, `worth a look`, `worth exploring`.
- Hedges: `perhaps`, `could potentially`, `it's important to note`.
- `"It's not X, it's Y"` and its split-sentence form.
- The rule of three, used reflexively rather than because three items
  are actually parallel and complete.
- `Let's` openers.
- Bold on more than one phrase per section.
- Title Case Headings.

### The bundled tool

Run these examples from the Shepherd's Pi checkout root. This tool is
optional; a shepherd can review writing without installing dependencies.

```bash
skills/concision/tools/ai-tells DRAFT.md              # report
skills/concision/tools/ai-tells DRAFT.md --hard       # exit 1 on any hard ban
skills/concision/tools/ai-tells DRAFT.md --json
```

`tools/ai-tells` wraps the
[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
detector (Conor Bronsdon, MIT license, 47 issue types), plus the em-dash
and emoji bans checked directly.

**Two runtime dependencies it does not bundle:** `node`, and a local
clone of `avoid-ai-writing`. By default the script looks for that clone
at the path in the `AI_TELLS_DETECTOR_PATH` environment variable, falling
back to `~/workspaces/avoid-ai-writing` — clone the detector wherever you
like and export that variable to point at it:

```bash
git clone https://github.com/conorbronsdon/avoid-ai-writing.git ~/workspaces/avoid-ai-writing
export AI_TELLS_DETECTOR_PATH=~/workspaces/avoid-ai-writing
```

Without both `node` and the clone, `ai-tells` exits with an error — pass
3 still works by hand from the Hard bans / Also strip lists above.

**The tool is advisory on everything except the three hard bans.** A
Tier-2 word in a sentence where it's genuinely the right word stays.

---

## Three tests before sending

- **Stranger test.** Would someone outside the immediate context know
  what was delivered?
- **Deletion test.** Remove any sentence. If nothing is lost, it was
  padding.
- **Citation test.** Can a reader act on this, or only admire it?

---

## What not to compress

- **Quoted material, code, tables, attributed text.** Flag issues,
  don't rewrite them.
- **Do-not-do instructions.** "Do not do X, here is why" earns its
  words — the explanation is what makes the warning credible.
- **Corrections to someone else's in-flight work.** Without the detail,
  the correction just repeats the original work.
- **Someone else's casual writing.** Preserve their typos and
  contractions when editing a message on their behalf; smoothing the
  rough edges erases the fingerprint that marks it as theirs.
