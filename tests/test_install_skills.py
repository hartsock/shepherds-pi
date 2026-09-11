import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/install-skills.py"
spec = importlib.util.spec_from_file_location("install_skills", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallSkillsTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.target = Path(directory.name) / "skills"

    def test_default_installs_coordination_without_optional_doctrine_or_tty_tools(self):
        installer.install(ROOT / "skills", self.target)
        self.assertTrue((self.target / "shepherd/SKILL.md").is_file())
        self.assertTrue((self.target / "herdr/SKILL.md").is_file())
        self.assertTrue((self.target / "herdr-helpers-tab/SKILL.md").is_file())
        self.assertFalse((self.target / "concision").exists())
        self.assertFalse((self.target / "tmux-drive").exists())

    def test_optional_selection_is_additive_and_resources_survive_symlink_resolution(
        self,
    ):
        installer.install(ROOT / "skills", self.target, extra=["concision"])
        self.assertTrue((self.target / "shepherd/SKILL.md").is_file())
        self.assertTrue((self.target / "concision/tools/ai-tells").is_file())
        source = (self.target / "shepherd/SKILL.md").resolve()
        self.assertTrue((source.parent / "../../docs/shepherding.md").is_file())
        self.assertEqual(
            installer.install(ROOT / "skills", self.target, extra=["concision"]), 0
        )

    def test_full_library_is_explicit_and_includes_bundled_tools(self):
        installer.install(ROOT / "skills", self.target, all_skills=True)
        self.assertTrue((self.target / "tmux-drive/tools/tdrive.sh").is_file())
        expected = {
            p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()
        }
        self.assertEqual({p.name for p in self.target.iterdir()}, expected)

    def test_unknown_and_path_like_names_fail_before_creating_target(self):
        for name in ["missing-skill", "../herdr", "/tmp/skill"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                installer.install(ROOT / "skills", self.target, extra=[name])
            self.assertFalse(self.target.exists())

    def test_conflicting_file_directory_or_broken_link_prevents_partial_install(self):
        for kind in ["file", "directory", "broken-link"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                conflict = target / "herdr"
                if kind == "file":
                    conflict.write_text("existing")
                elif kind == "directory":
                    conflict.mkdir()
                else:
                    conflict.symlink_to(target / "absent")
                with self.assertRaises(ValueError):
                    installer.install(ROOT / "skills", target)
                self.assertEqual([p.name for p in target.iterdir()], ["herdr"])
                if kind == "file":
                    self.assertEqual(conflict.read_text(), "existing")

    def test_cli_selects_optional_skill_and_rejects_conflict_without_writes(self):
        command = [sys.executable, "-B", str(SCRIPT), "--target", str(self.target)]
        result = subprocess.run(command + ["--skill", "concision"], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "concision/SKILL.md").is_file())
        before = {p.name: p.readlink() for p in self.target.iterdir()}
        result = subprocess.run(
            command + ["--skill", "missing-skill"], capture_output=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual({p.name: p.readlink() for p in self.target.iterdir()}, before)


if __name__ == "__main__":
    unittest.main()

# Model: GPT-6 | Harness: Codex | Operator: S Hartsock | Time: 00:52 EDT | Date: 2026-09-11
