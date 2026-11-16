# Evidence: check-evidence

DEV stage, branch `feat/check-evidence`. Tests are in
`tests/test_check_evidence.py` and run the CLI as a subprocess on temp files.
Suite: `python3 -m unittest discover -s tests` gives `Ran 20 tests ... OK`.

| AC | Proof |
|---|---|
| AC1 | `test_ac1_complete_evidence_passes` (stdout exactly `ok: 2 criteria, all with proof`, exit 0). `test_ac1_extra_columns_bold_ids_and_markdown_proofs` covers 3 columns, `**AC1**`, backticks and links. Self-check: `python3 scripts/check_evidence.py trials/check-evidence/spec.md trials/check-evidence/EVIDENCE.md` prints `ok: 11 criteria, all with proof`, exit 0. |
| AC2 | `test_ac2_missing_row` prints `missing: AC2`, exit 1. Observed: `python3 scripts/check_evidence.py trials/check-evidence/spec.md trials/check-evidence/scenarios.md` prints `missing: AC1` to `missing: AC11`, exit 1. |
| AC3 | `test_ac3_placeholders_are_no_proof` checks empty, ` todo `, `TBD`, `-`, `UNPROVEN` and `Unproven` (each gives `no proof: AC<n>`) while a real proof passes. `test_ac3_row_without_proof_cell` covers a row with no second cell. Placeholder set is at `scripts/check_evidence.py:17`. |
| AC4 | `test_ac4_unknown_row` prints `unknown: AC7`, exit 1. |
| AC5 | `test_ac5_duplicate_reported_once_and_not_proof_checked` has three AC1 rows, two of them placeholders. Output is only `duplicate: AC1`, exit 1. |
| AC6 | `test_ac6_ids_compare_as_integers` (scenario S1 shape) gives `duplicate: AC1`, `missing: AC10`. `test_ac6_leading_zero_satisfies_and_prints_without_zero` shows `AC01` satisfying `AC1` and output `missing: AC2`, `unknown: AC3` from `AC002` and `AC0003`. |
| AC7 | `test_ac7_only_section_lines_are_criteria` ignores prose, other-section and post-section `AC<n>.` lines, keeps an indented criterion and `AC99.` under `### Notes` (scenario S2). `test_ac7_level_one_heading_ends_section` and `test_ac7_heading_is_case_insensitive` cover the section bounds. |
| AC8 | Tests `test_ac8_missing_evidence_file`, `test_ac8_missing_spec_file`, `test_ac8_unreadable_file` (directory and invalid UTF-8), `test_ac8_no_section`, `test_ac8_empty_section` assert exit 2, empty stdout, exactly one stderr line starting `error:`. `test_ac8_wrong_argument_count` checks 0, 1 and 3 args for exit 2 and a `usage:` line. Observed: `python3 scripts/check_evidence.py trials/check-evidence/spec.md /nonexistent/EVIDENCE.md` prints `error: cannot read /nonexistent/EVIDENCE.md: [Errno 2] No such file or directory: '/nonexistent/EVIDENCE.md'`, exit 2. |
| AC9 | `test_ac9_all_problems_in_one_run_sorted` produces all four kinds in one run, in the order `missing: AC2`, `missing: AC3`, `duplicate: AC4`, `unknown: AC5`, `no proof: AC10`, `unknown: AC12`. Kind order table is at `scripts/check_evidence.py:19`. A lexical-sort mutant made this test fail. |
| AC10 | One file, `scripts/check_evidence.py`, imports only `re` and `sys` (lines 8-9). `test_ac10_standard_library_only` checks imports against `sys.stdlib_module_names`. Observed: `uv run --python 3.10 --no-project python -m unittest discover -s tests` on CPython 3.10.20 gives `Ran 20 tests ... OK`. The same on 3.13.18 gives `Ran 20 tests ... OK`. |
| AC11 | `README.md:33` `## Checking evidence` gives the command, the exit codes and the format contract. |
