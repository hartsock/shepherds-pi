"""Checks for tools/dupes. Run: python3 -m unittest discover skills/herdr-winnow/tools"""

import contextlib
import io
import os
import subprocess
import tempfile
import unittest
from importlib.machinery import SourceFileLoader

dupes = SourceFileLoader(
    "dupes", os.path.join(os.path.dirname(__file__), "dupes")
).load_module()

BLOCK = "\n".join(f"total += price[{i}] * qty[{i}]" for i in range(8))


def run(files, *args):
    with tempfile.TemporaryDirectory() as d:
        for name, text in files.items():
            with open(os.path.join(d, name), "w") as f:
                f.write(text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = dupes.main([*args, d])
        return code, [line.split("\t") for line in out.getvalue().splitlines()]


class Dupes(unittest.TestCase):
    def test_clean_tree_exits_zero(self):
        self.assertEqual(run({"a.py": BLOCK, "b.py": "print(1)\n"}), (0, []))

    def test_overlapping_windows_merge_into_one_block(self):
        code, rows = run({"a.py": "x = 1\n" + BLOCK, "b.py": "  " + BLOCK.replace("\n", "\n  ")})
        self.assertEqual(code, 1)
        self.assertEqual(len(rows), 1)
        copies, length, saving, where = rows[0]
        self.assertEqual((copies, length, saving), ("2", "8", "8"))
        self.assertTrue(where.endswith("b.py:1") and "a.py:2" in where)

    def test_min_count_applies_rule_of_three(self):
        self.assertEqual(run({"a.py": BLOCK, "b.py": BLOCK}, "--min-count", "3"), (0, []))
        code, rows = run({"a.py": BLOCK, "b.py": BLOCK, "c.py": BLOCK}, "--min-count", "3")
        self.assertEqual((code, rows[0][:3]), (1, ["3", "8", "16"]))

    def test_git_ignored_files_are_not_scanned(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            with open(os.path.join(d, ".gitignore"), "w") as f:
                f.write("target/\n")
            for name in ("src/a.py", "src/b.py", "target/c.py"):
                os.makedirs(os.path.dirname(os.path.join(d, name)), exist_ok=True)
                with open(os.path.join(d, name), "w") as f:
                    f.write(BLOCK)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = dupes.main([d])
            rows = [line.split("\t") for line in out.getvalue().splitlines()]
        self.assertEqual(code, 1)
        self.assertEqual(len(rows), 1)
        copies, length, saving, where = rows[0]
        self.assertEqual((copies, length, saving), ("2", "8", "8"))
        self.assertIn("src", where)
        self.assertNotIn("target", where)

    def test_explicit_file_scan_tolerates_deleted_tracked_sibling(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            for name in ("a.py", "gone.py"):
                with open(os.path.join(d, name), "w") as f:
                    f.write(BLOCK)
            subprocess.run(["git", "-C", d, "add", "."], check=True)
            os.remove(os.path.join(d, "gone.py"))  # tracked in the index, gone on disk
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = dupes.main([os.path.join(d, "a.py")])
        self.assertEqual((code, out.getvalue()), (0, ""))

    def test_nonexistent_path_is_usage_error_not_parent_scan(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            for name in ("a.py", "b.py"):
                with open(os.path.join(d, name), "w") as f:
                    f.write(BLOCK)
            subprocess.run(["git", "-C", d, "add", "."], check=True)
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as cm:
                    dupes.main([os.path.join(d, "typo")])
        self.assertEqual((cm.exception.code, out.getvalue()), (2, ""))
        self.assertIn("typo", err.getvalue())

    def test_path_aliases_do_not_manufacture_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "one.py"), "w") as f:
                f.write(BLOCK)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = dupes.main([d, os.path.join(d, ".")])
        self.assertEqual((code, out.getvalue()), (0, ""))

    def test_unequal_copies_keep_the_longest_continuing_block(self):
        # a and b share eight lines; c shares only the first six.
        six = "\n".join(BLOCK.splitlines()[:6])
        code, rows = run({"a.py": BLOCK, "b.py": BLOCK, "c.py": six})
        self.assertEqual(code, 1)
        by_copies = {r[0]: r for r in rows}
        self.assertEqual(by_copies["2"][1:3], ["8", "8"])
        self.assertEqual(sorted(p.rsplit("/", 1)[-1] for p in by_copies["2"][3].split()), ["a.py:1", "b.py:1"])
        self.assertEqual(by_copies["3"][1:3], ["6", "12"])
        self.assertEqual(sorted(p.rsplit("/", 1)[-1] for p in by_copies["3"][3].split()), ["a.py:1", "b.py:1", "c.py:1"])

    def test_block_longer_than_recursion_limit_is_reported(self):
        long = "\n".join(f"value_{i} = {i}" for i in range(1200))
        code, rows = run({"a.py": long, "b.py": long})
        self.assertEqual(code, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][:3], ["2", "1200", "1200"])

    def test_punctuation_and_blank_lines_are_not_duplication(self):
        noise = "}\n\n)\n---\n" * 10
        self.assertEqual(run({"a.js": noise, "b.js": noise}), (0, []))


if __name__ == "__main__":
    unittest.main()
