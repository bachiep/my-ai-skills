#!/usr/bin/env python3
"""Test suite cho skill tao-phim-tat-iphone.

Chay:  python3 -m unittest discover -s tests -v   (tu thu muc repo)
Chi dung stdlib, khong can cai them gi.
"""
import json
import plistlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(REPO / "bin" / "shortcut-cli")]
UUID_RE = re.compile(
    r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$")


def run_cli(*args):
    r = subprocess.run([*CLI, *args], capture_output=True, text=True, timeout=120)
    return r


def load_compiled(path):
    with open(path, "rb") as f:
        return plistlib.loads(f.read())


def find_output_refs(node, out=None):
    """Tim moi dict {Type: ActionOutput, OutputUUID: ...} trong params."""
    if out is None:
        out = []
    if isinstance(node, dict):
        if node.get("Type") == "ActionOutput" and "OutputUUID" in node:
            out.append(node["OutputUUID"])
        for v in node.values():
            find_output_refs(v, out)
    elif isinstance(node, list):
        for v in node:
            find_output_refs(v, out)
    return out


class TestSkillStructure(unittest.TestCase):
    def test_frontmatter(self):
        text = (REPO / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"), "SKILL.md thieu frontmatter")
        head = text.split("---")[1]
        self.assertRegex(head, r'name:\s*"tao_phim_tat_iphone"')
        self.assertIn("description:", head)

    def test_referenced_files_exist(self):
        text = (REPO / "SKILL.md").read_text(encoding="utf-8")
        for m in re.finditer(r"`(references/[\w.-]+\.md)`", text):
            self.assertTrue((REPO / m.group(1)).is_file(),
                            f"thieu file {m.group(1)}")
        self.assertTrue((REPO / "templates").is_dir())
        self.assertTrue((REPO / "bin" / "shortcut-cli").is_file())

    def test_no_duplicate_skill_copies(self):
        # Bai hoc tu hulk-skills: khong de 2 ban skill lech nhau
        skill_files = list(REPO.glob("**/SKILL.md"))
        self.assertEqual(len(skill_files), 1, f"tim thay {len(skill_files)} SKILL.md")


class TestTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.compiled = {}
        for spec in sorted((REPO / "templates").glob("*.json")):
            out = Path(cls.tmp.name) / (spec.stem + ".shortcut")
            r = run_cli("compile", "--no-sign", str(spec), "-o", str(out))
            assert r.returncode == 0, f"compile {spec.name} loi: {r.stderr}"
            cls.compiled[spec.stem] = out

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_templates_exist(self):
        self.assertGreaterEqual(len(self.compiled), 3)

    def test_info_canonical(self):
        for name, path in self.compiled.items():
            r = run_cli("info", str(path))
            self.assertEqual(r.returncode, 0, f"info {name} loi")
            self.assertIn("OK canonical", r.stdout, f"{name} cau truc khong chuan")

    def test_uuid_uppercase_unique(self):
        # Quy tac cung: moi action phai co UUID viet hoa, duy nhat
        for name, path in self.compiled.items():
            d = load_compiled(path)
            uuids = [a["WFWorkflowActionParameters"].get("UUID")
                     for a in d["WFWorkflowActions"]]
            self.assertTrue(all(u and UUID_RE.match(u) for u in uuids),
                            f"{name} co action thieu UUID hoac khong viet hoa")
            self.assertEqual(len(set(uuids)), len(uuids),
                             f"{name} co UUID trung nhau")

    def test_magic_variable_refs_resolve(self):
        # Loi tung gap: OutputUUID tro vao khoang khong (placeholder 00000000)
        for name, path in self.compiled.items():
            d = load_compiled(path)
            uuids = {a["WFWorkflowActionParameters"].get("UUID")
                     for a in d["WFWorkflowActions"]}
            refs = find_output_refs(d["WFWorkflowActions"])
            for ref in refs:
                self.assertNotEqual(ref, "00000000-0000-0000-0000-000000000000",
                                    f"{name} con placeholder UUID")
                self.assertIn(ref, uuids,
                              f"{name} co OutputUUID khong ton tai: {ref[:8]}")

    def test_grouping_shared(self):
        # If/Menu mo-nhanh-dong phai chung GroupingIdentifier
        for name in ("menu-driven", "http-api"):
            d = load_compiled(str(self.compiled[name]))
            grps = [a["WFWorkflowActionParameters"].get("GroupingIdentifier")
                    for a in d["WFWorkflowActions"]
                    if a["WFWorkflowActionParameters"].get("WFControlFlowMode") in (0, 1, 2)]
            self.assertTrue(grps, f"{name} khong tim thay control flow")
            self.assertEqual(len(set(grps)), 1,
                             f"{name} GroupingIdentifier khong dong nhat")
            self.assertIsNotNone(grps[0])

    def test_roundtrip_action_count(self):
        for name, path in self.compiled.items():
            dec = Path(self.tmp.name) / f"{name}-dec.json"
            r = run_cli("decompile", str(path), "-o", str(dec))
            self.assertEqual(r.returncode, 0)
            n1 = len(json.loads(dec.read_text())["WFWorkflowActions"])
            rec = Path(self.tmp.name) / f"{name}-re.shortcut"
            r = run_cli("compile", "--no-sign", str(dec), "-o", str(rec))
            self.assertEqual(r.returncode, 0)
            n2 = len(load_compiled(rec)["WFWorkflowActions"])
            self.assertEqual(n1, n2, f"{name} round-trip mat action ({n1} -> {n2})")


class TestValidator(unittest.TestCase):
    VALIDATOR = [sys.executable, str(REPO / "bin" / "validate-shortcut")]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.good = str(Path(self.tmp.name) / "good.shortcut")
        r = run_cli("compile", "--no-sign",
                    str(REPO / "templates" / "http-api.json"), "-o", self.good)
        self.assertEqual(r.returncode, 0)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_file_passes(self):
        r = subprocess.run([*self.VALIDATOR, self.good],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("DAT", r.stdout)

    def test_broken_file_fails(self):
        d = load_compiled(self.good)
        # gay 3 loi: mat UUID, placeholder ref, ma dieu kien la
        del d["WFWorkflowActions"][0]["WFWorkflowActionParameters"]["UUID"]
        p2 = d["WFWorkflowActions"][2]["WFWorkflowActionParameters"]
        p2["WFURL"]["Value"]["OutputUUID"] = "00000000-0000-0000-0000-000000000000"
        d["WFWorkflowActions"][3]["WFWorkflowActionParameters"]["WFCondition"] = 42
        bad = str(Path(self.tmp.name) / "bad.shortcut")
        with open(bad, "wb") as f:
            plistlib.dump(d, f)
        r = subprocess.run([*self.VALIDATOR, bad],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 1)
        self.assertIn("thieu UUID", r.stdout)
        self.assertIn("placeholder", r.stdout)
        self.assertIn("WFCondition", r.stdout)


class TestInstallScript(unittest.TestCase):
    def test_install_to_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = str(Path(tmp) / "my-skills" / "tao-phim-tat-iphone")
            r = subprocess.run(["bash", str(REPO / "install.sh"),
                                "--target", target],
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(Path(target, "SKILL.md").is_file())
            self.assertTrue(Path(target, "bin", "shortcut-cli").is_file())
            self.assertTrue(Path(target, "references").is_dir())


if __name__ == "__main__":
    unittest.main()
