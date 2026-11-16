# Verdict: check-evidence

Verifier = Claude Sonnet, fresh context. Deviation from the playbook: same provider as the builder (Claude), so the "different provider" requirement is UNPROVEN for this trial.

Commands run from /home/claude/lysagents unless noted.

- `python3 /home/claude/holdouts/run_holdouts.py scripts/check_evidence.py` -> H1..H9 all PASS, `9/9 holdouts passed`.
- `python3 -m unittest discover -s tests` -> `Ran 20 tests ... OK` (Python 3.13.18).
- `uv run --python 3.10 --no-project python -m unittest discover -s tests` -> `Ran 20 tests ... OK`; interpreter confirmed `3.10.20`.
- EVIDENCE.md reruns: self-check on spec+EVIDENCE gives `ok: 11 criteria, all with proof` exit 0; spec vs scenarios.md gives `missing: AC1`..`missing: AC11` exit 1; nonexistent evidence gives `error: cannot read /nonexistent/EVIDENCE.md: [Errno 2] ...` exit 2. Imports at scripts/check_evidence.py:8-9 are `re`, `sys`; placeholder set at :17, kind order at :19; README.md:33 is `## Checking evidence`. All EVIDENCE.md rows reproduced.

| AC | Verdict | Evidence |
|---|---|---|
| AC1 | PASS | Self-check prints exactly `ok: 11 criteria, all with proof`, exit 0; holdout H1 PASS (3 cols, bold IDs, markdown proofs). |
| AC2 | PASS | spec vs scenarios.md prints `missing: AC1`..`AC11`, exit 1; H5. |
| AC3 | PASS | H2 PASS (`UNPROVEN`, ` todo `, `-`); /tmp probe: row `\| AC2 \|` with no proof cell gives `no proof: AC2`. |
| AC4 | PASS | H5 (`unknown: AC7`); unit test `test_ac4_unknown_row`. |
| AC5 | PASS | /tmp probe: three AC1 rows (two empty) prints only `duplicate: AC1` once, exit 1; H5. |
| AC6 | PASS | H3 (`duplicate: AC1`, `missing: AC10`, AC01 not unknown). |
| AC7 | PASS | H4 PASS (prose AC3/AC5, other-section AC3/AC6 ignored, `### Notes` AC99 counted). |
| AC8 | PASS | H6, H7, H8, H9 PASS; probe directory as spec gives `error: cannot read /tmp: [Errno 21] Is a directory`, exit 2; no args and 3 args give `usage: check_evidence.py SPEC EVIDENCE`, exit 2. |
| AC9 | PASS | H5 order `missing, duplicate, no proof, no proof, unknown`; sort key at scripts/check_evidence.py:75. |
| AC10 | PASS | One file in scripts/, stdlib imports only; 20 tests OK on 3.10.20 and 3.13.18. |
| AC11 | PASS | README.md:33 section with command, exit codes, contract. Note: four sentences, slightly over "one or two" for the contract plus command; judged within intent. |

| Scenario | Result | Evidence |
|---|---|---|
| S1 | held | H3 PASS: AC1 evidence does not satisfy AC10; AC01 not unknown. |
| S2 | held | H4 PASS: prose AC3 ignored, `### Notes` AC99 counted. |
| S3 | held | H2 PASS: all three placeholders give `no proof`. |
| S4 | held | H6 PASS: stderr `error:`, empty stdout, exit 2. |
| S5 | held | H5 PASS: all five problems in one run, sorted. |
| S6 | held | H1 PASS: `ok: 4 criteria, all with proof`. |

## Spec gaps found (spec silent; not build failures)

1. Placeholder wrapped in bold: row `| AC1 | **UNPROVEN** |` and `| AC2 | **TODO** |` pass as proof (`ok: 3 criteria`, exit 0). D1 only trims spaces.
2. Pipe inside a backtick code span in a proof cell: cell is split at the pipe; `` `a|b` `` yields proof `` `a ``, which still counts as proof. A proof whose real content comes after the pipe could be misjudged. Escaped pipes are a stated non-goal, unescaped-in-code is not mentioned.
3. `## ` line inside a fenced code block in the criteria section ends the section: criteria after it are dropped and their evidence rows report `unknown: AC2`, `unknown: AC3`.
4. Lowercase `ac2` row: ignored as a row (first cell must be `AC<n>`), so the criterion reports `missing: AC2`. Matches the contract literally; the message may confuse.
5. UTF-8 BOM at the start of the spec: heading not recognised, `error: no '## Acceptance criteria' section`, exit 2.
6. Same criterion number listed twice in the spec: counted once, no warning (`ok: 3 criteria`).
7. A table row not starting with `|` (e.g. `AC1 | x |`) is ignored (contract says rows start with `|`), giving `missing`.
8. CRLF line endings work (`ok: 2 criteria`); empty EVIDENCE.md gives `missing` for every criterion, exit 1; spec is silent on both but behaviour is reasonable.

## Build defects found

None. No spec-violating behaviour observed.

Overall: PASS, every AC verified by holdouts 9/9, 20 unit tests on Python 3.10.20 and 3.13.18, and reruns of every EVIDENCE.md row (the different-provider rule remains UNPROVEN as noted above, and is a process deviation, not an AC).
