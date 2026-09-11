#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys


DEFAULT_SKILLS = ("shepherd", "herdr", "herdr-helpers-tab")


def install(source, target, extra=(), all_skills=False):
    available = {
        path.name: path for path in source.iterdir() if (path / "SKILL.md").is_file()
    }
    selected = set(available) if all_skills else set(DEFAULT_SKILLS).union(extra)
    missing = selected.difference(available)
    if missing:
        raise ValueError("Unknown skills: " + ", ".join(sorted(missing)))
    conflicts = []
    pending = []
    for name in sorted(selected):
        skill = available[name]
        destination = target / skill.name
        if destination.is_symlink() and destination.resolve() == skill.resolve():
            continue
        if destination.exists() or destination.is_symlink():
            conflicts.append(skill.name)
        else:
            pending.append((skill, destination))
    if conflicts:
        raise ValueError(
            "Existing skills would conflict: "
            + ", ".join(conflicts)
            + ". Choose a different --target or reconcile them explicitly. Nothing changed."
        )
    target.mkdir(parents=True, exist_ok=True)
    for source_path, destination in pending:
        destination.symlink_to(source_path.resolve(), target_is_directory=True)
    return len(pending)


def main():
    parser = argparse.ArgumentParser(
        description="Install complete skill directory links without replacing existing skills."
    )
    parser.add_argument(
        "--target",
        type=Path,
        required=True,
        help="An explicitly chosen agent skills directory",
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Add an optional skill; repeat as needed",
    )
    selection.add_argument(
        "--all", action="store_true", help="Install the full skill library"
    )
    args = parser.parse_args()
    try:
        count = install(
            Path(__file__).resolve().parents[1] / "skills",
            args.target.expanduser().absolute(),
            extra=args.skill,
            all_skills=args.all,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Installed {count} skill links; already-correct links preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 09:57 EDT | Date: 2026-09-10

# Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:53 EDT | Date: 2026-09-11
