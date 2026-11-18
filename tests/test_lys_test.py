import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import lys_test  # noqa: E402


class Overall(unittest.TestCase):
    def test_last_overall_line_wins(self):
        text = "Overall: PASS was the old one\nOverall: PASS\n...\nOverall: FAIL\n"
        self.assertEqual(lys_test.overall(text), "FAIL")

    def test_missing_overall_is_unproven(self):
        self.assertEqual(lys_test.overall("looks good to me"), "UNPROVEN")

    def test_overall_must_be_its_own_line(self):
        self.assertEqual(lys_test.overall("I'd say Overall: PASS"), "UNPROVEN")


class Combine(unittest.TestCase):
    def test_failed_holdouts_override_a_pass(self):
        self.assertEqual(lys_test.combine(False, "PASS"), "FAIL")

    def test_passed_holdouts_keep_verifier_result(self):
        for v in ("PASS", "FAIL", "UNPROVEN"):
            self.assertEqual(lys_test.combine(True, v), v)

    def test_unproven_blocks_merge(self):
        self.assertEqual(lys_test.STATE["UNPROVEN"], "failure")


class Prompt(unittest.TestCase):
    def test_brief_has_every_placeholder_filled(self):
        brief = lys_test.BRIEF.read_text()
        out = lys_test.build_prompt(brief, repo="o/r", pr="7", sha="abc", spec="s.md",
                                    evidence="E.md", holdout_output="9/9")
        self.assertNotIn("{{", out)
        self.assertIn("o/r#7", out)
        self.assertIn("9/9", out)


class Inside(unittest.TestCase):
    def test_holdouts_inside_repo_detected(self):
        self.assertTrue(lys_test.inside(Path("/r/x/h"), Path("/r")))
        self.assertFalse(lys_test.inside(Path("/rx/h"), Path("/r")))


if __name__ == "__main__":
    unittest.main()
