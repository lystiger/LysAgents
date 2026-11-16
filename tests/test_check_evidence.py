import ast
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check_evidence.py"


def spec(*criteria_lines, before="", after=""):
    body = "\n".join(criteria_lines)
    return f"# Spec\n\n{before}\n## Acceptance criteria\n\n{body}\n\n{after}\n"


def table(*rows):
    lines = ["| AC | Proof |", "|---|---|"]
    lines += [f"| {ac} | {proof} |" for ac, proof in rows]
    return "\n".join(lines) + "\n"


class CheckEvidenceCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def write(self, name, text):
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True, text=True,
        )

    def check(self, spec_text, evidence_text):
        return self.run_cli(
            self.write("spec.md", spec_text),
            self.write("EVIDENCE.md", evidence_text),
        )

    def assertProblems(self, result, lines):
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout.splitlines(), lines)

    def test_ac1_complete_evidence_passes(self):
        r = self.check(
            spec("AC1. one", "AC2. two"),
            table(("AC1", "`test_x`"), ("AC2", "scripts/x.py:3")),
        )
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "ok: 2 criteria, all with proof\n")

    def test_ac1_extra_columns_bold_ids_and_markdown_proofs(self):
        evidence = (
            "| AC | Proof | Notes |\n|---|---|---|\n"
            "| **AC1** | `cmd --flag` -> `ok` | fine |\n"
            "| AC2 | [log](https://example.com/a) | |\n"
        )
        r = self.check(spec("- AC1. one", "* AC2. two"), evidence)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(r.stdout, "ok: 2 criteria, all with proof\n")

    def test_ac2_missing_row(self):
        r = self.check(spec("AC1. one", "AC2. two"), table(("AC1", "proof")))
        self.assertProblems(r, ["missing: AC2"])

    def test_ac3_placeholders_are_no_proof(self):
        criteria = [f"AC{n}. c" for n in range(1, 8)]
        rows = [("AC1", ""), ("AC2", " todo "), ("AC3", "TBD"), ("AC4", "-"),
                ("AC5", "UNPROVEN"), ("AC6", "Unproven"), ("AC7", "real proof")]
        r = self.check(spec(*criteria), table(*rows))
        self.assertProblems(r, [f"no proof: AC{n}" for n in range(1, 7)])

    def test_ac3_row_without_proof_cell(self):
        r = self.check(spec("AC1. one"), "| AC1 |\n")
        self.assertProblems(r, ["no proof: AC1"])

    def test_ac4_unknown_row(self):
        r = self.check(spec("AC1. one"), table(("AC1", "p"), ("AC7", "p")))
        self.assertProblems(r, ["unknown: AC7"])

    def test_ac5_duplicate_reported_once_and_not_proof_checked(self):
        r = self.check(
            spec("AC1. one"),
            table(("AC1", "TODO"), ("AC1", "p"), ("AC1", "")),
        )
        self.assertProblems(r, ["duplicate: AC1"])

    def test_ac6_ids_compare_as_integers(self):
        criteria = [f"AC{n}. c" for n in range(1, 13)]
        rows = [(f"AC{n}", "p") for n in [*range(1, 10), 11, 12]]
        rows.append(("AC01", "p"))
        r = self.check(spec(*criteria), table(*rows))
        self.assertProblems(r, ["duplicate: AC1", "missing: AC10"])

    def test_ac6_leading_zero_satisfies_and_prints_without_zero(self):
        r = self.check(spec("AC1. one", "AC002. two"),
                       table(("AC01", "p"), ("AC0003", "p")))
        self.assertProblems(r, ["missing: AC2", "unknown: AC3"])

    def test_ac7_only_section_lines_are_criteria(self):
        text = spec(
            "AC1. real",
            "Prose mentioning AC2. inline does not count.",
            "   AC3. indented counts",
            "### Notes",
            "AC99. still in section",
            before="Unlike AC4. in the old spec.\nAC5. outside the section\n",
            after="## Design\n\nAC6. after the section\n",
        )
        r = self.check(text, table(("AC1", "p"), ("AC3", "p"), ("AC99", "p")))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(r.stdout, "ok: 3 criteria, all with proof\n")

    def test_ac7_level_one_heading_ends_section(self):
        text = "## Acceptance criteria\nAC1. a\n# Appendix\nAC2. b\n"
        r = self.check(text, table(("AC1", "p")))
        self.assertEqual(r.stdout, "ok: 1 criteria, all with proof\n")

    def test_ac7_heading_is_case_insensitive(self):
        r = self.check("## ACCEPTANCE CRITERIA\nAC1. a\n", table(("AC1", "p")))
        self.assertEqual(r.returncode, 0, r.stderr)

    def assertInputError(self, result):
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        lines = result.stderr.splitlines()
        self.assertEqual(len(lines), 1, result.stderr)
        self.assertTrue(lines[0].startswith("error:"), lines[0])

    def test_ac8_missing_evidence_file(self):
        good = self.write("spec.md", spec("AC1. one"))
        self.assertInputError(self.run_cli(good, str(self.dir / "nope.md")))

    def test_ac8_missing_spec_file(self):
        ev = self.write("EVIDENCE.md", table(("AC1", "p")))
        self.assertInputError(self.run_cli(str(self.dir / "nope.md"), ev))

    def test_ac8_unreadable_file(self):
        good = self.write("spec.md", spec("AC1. one"))
        self.assertInputError(self.run_cli(good, str(self.dir)))
        binary = self.dir / "bin.md"
        binary.write_bytes(b"\xff\xfe\x00bad")
        self.assertInputError(self.run_cli(good, str(binary)))

    def test_ac8_no_section(self):
        self.assertInputError(self.check("# Spec\nAC1. a\n", table(("AC1", "p"))))

    def test_ac8_empty_section(self):
        text = "## Acceptance criteria\n\nNone yet.\n## Design\nAC1. a\n"
        self.assertInputError(self.check(text, table(("AC1", "p"))))

    def test_ac8_wrong_argument_count(self):
        for args in [(), ("one",), ("a", "b", "c")]:
            r = self.run_cli(*args)
            self.assertEqual(r.returncode, 2)
            self.assertEqual(r.stdout, "")
            self.assertTrue(r.stderr.startswith("usage:"), r.stderr)

    def test_ac9_all_problems_in_one_run_sorted(self):
        criteria = [f"AC{n}. c" for n in (1, 2, 3, 4, 10)]
        rows = [("AC12", "p"), ("AC10", "TODO"), ("AC4", "p"), ("AC4", "p"),
                ("AC5", "p"), ("AC1", "p")]
        r = self.check(spec(*criteria), table(*rows))
        self.assertProblems(r, [
            "missing: AC2",
            "missing: AC3",
            "duplicate: AC4",
            "unknown: AC5",
            "no proof: AC10",
            "unknown: AC12",
        ])

    def test_ac10_standard_library_only(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported.add(node.module.split(".")[0])
        self.assertLessEqual(imported, set(sys.stdlib_module_names))


if __name__ == "__main__":
    unittest.main()
