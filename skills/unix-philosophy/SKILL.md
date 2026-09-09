---
name: unix-philosophy
description: Write small, composable, text-based tools that do one thing well and connect through simple interfaces — the design taste behind pipes, filters, and everything in this repo's own tooling.
when_to_use: When designing a new script, CLI, or skill's bundled tool; when a tool is growing flags for unrelated concerns; when deciding whether two behaviors belong in one program or two; when a tool's output format is making it hard to compose with anything else.
---

# The Unix Philosophy

Doug McIlroy's summary, still the whole doctrine:

> Write programs that do one thing and do it well. Write programs to work
> together. Write programs to handle text streams, because that is a
> universal interface.

## The core rules

- **Do one thing well.** A program that tries to do everything does
  nothing well, and every feature it adds is a feature every caller has
  to learn to ignore. If a tool's `--help` needs sections, it has
  probably outgrown "one thing."
- **Expect the output of every program to become the input to another,
  as yet unknown, program.** Don't clutter output with anything that
  isn't the data. No banners, no progress bars on stdout, no "Done!" —
  those go to stderr, or nowhere.
- **Design and build software, even operating systems, to be tried
  early**, ideally within weeks. Don't hesitate to throw away the
  clumsy parts and rebuild. A tool nobody has run yet is still a guess.
- **Use tools in preference to unskilled help to lighten a programming
  task**, even if a detour is needed to build the tools, and expect to
  throw some of them out after you've finished using them. Writing a
  small script to do the boring part is not overhead — it's the job.

## Text streams — and their analogs — as the universal interface

Prefer plain text over a bespoke binary or proprietary format whenever
the data will ever be read, diffed, greppable, or piped. In practice this
usually means reaching for one of a handful of well-known structured-text
formats rather than inventing a new one:

- **CSV** — tabular data, the lowest-ceremony structured format there is.
  Opens in a spreadsheet, greps like any other text file, diffs one row
  per line.
- **JSON** — nested data with a schema every language already has a
  parser for. The default for anything an API returns or a program
  consumes.
- **YAML** — JSON's more human-writable cousin, for config a person
  edits directly — this repo's own `SKILL.md` frontmatter is YAML for
  exactly that reason.

What they share, and why any of them beats a bespoke format:

- **Diffable.** `git diff` on a text config tells a reviewer exactly
  what changed, one line at a time. A binary blob tells them nothing.
- **Composable.** `grep`, `sed`, `awk`, `jq`, `yq` all already understand
  these formats. A new bespoke format means every consumer needs a new
  parser before it can do anything with the data.
- **Legible without tooling.** `cat` and a human eye is a debugger of
  last resort that always works.

This is also the reasoning behind every `SKILL.md` in this repo being
plain markdown: no build step, no proprietary schema, readable by a human
or an agent with nothing but a text reader.

**Text isn't the only universal interface — it's the shell's version of
one.** When you aren't working with streams, a common interface or API
fills the same niche: a narrow, stable seam that any number of unknown
future callers can plug into without knowing each other's internals.
Object-oriented design has its own name for choosing that seam well:
**composition over inheritance.** An inheritance hierarchy couples a
subclass to its parent's implementation details across generations — the
OOP equivalent of a proprietary binary format only one program can read.
Composing small objects behind an interface is the equivalent of piping
text between programs: each piece stays replaceable, testable, and
recombinable in ways its author never had to predict. Same discipline,
different medium.

## Small tools over monoliths

When a tool starts accumulating flags for unrelated concerns — one flag
for output format, one for a retry policy, one for a completely different
input source — that's the signal to split it into two tools that pipe
together rather than one tool with a mode switch. Two 40-line scripts
connected by a pipe are easier to test, replace, and understand than one
200-line script with branches.

The counter-force is real: sometimes a single combined tool is genuinely
simpler for the caller (see `skills/three-cs` in this repo for the
parallel argument about hardcoding to ship first). The discipline isn't
"never combine" — it's noticing when you *are* combining, and asking
whether the seam belongs between two programs instead of inside one.

## Silence is a feature

A well-behaved Unix program that succeeds says nothing. Output is for
data or for errors, not for reassurance. Chatty success output is noise
that has to be filtered out by whatever's downstream — a human or another
program.

## How this shows up in this repo

- Every skill here is a markdown file, not a binary or a service —
  greppable, diffable, and requires no runtime beyond a text reader.
- `skills/concision`'s bundled `tools/ai-tells` does one thing (report
  writing tells in a file) and reads/writes plain text.
- `skills/pi-inference-backend`'s verification steps are individually
  runnable `curl`/`pi` one-liners, not a single opaque setup script — each
  step is checkable on its own.
- `skills/herdr-helpers-tab` composes `herdr`'s small pane/tab primitives
  (`split`, `run`, `rename`) rather than asking for one "make me 4 panes"
  command that doesn't exist — the herdr CLI itself is built the same way.

## Checklist

- [ ] Does this tool do one job, statable in one sentence?
- [ ] Does it read/write plain text (or well-known structured text like
      JSON) — or, in code, expose a narrow interface rather than an
      inheritance hierarchy — so it composes with callers that don't know
      it exists?
- [ ] Is success silent, with errors going to stderr?
- [ ] If it's grown a mode switch for an unrelated concern, should it be
      two tools instead?
- [ ] Could someone else's tool consume this one's output without reading
      its source first?
