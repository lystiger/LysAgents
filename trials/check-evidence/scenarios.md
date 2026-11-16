# Limit scenarios: check-evidence

Drafted by Claude in PRETEST. The playbook wants a different provider to
draft these; for this trial that is UNPROVEN (G5).

| # | Attacks | Story | Expected | Breaks if | Proof |
|---|---|---|---|---|---|
| S1 | AC6 | A spec with 12 criteria. EVIDENCE.md has rows AC1 to AC9, then AC11, AC12, and AC1 again written as `AC01`. | `duplicate: AC1`, `missing: AC10`, exit 1. | AC10 counts as satisfied by AC1, or AC01 is reported as unknown. | Holdout H3 |
| S2 | AC7 | The spec's Context section says "unlike AC3 in the old spec". The criteria section has a sub-heading `### Notes` with `AC99. ignore me`. | AC3 in prose is ignored. `### Notes` does not end the section, so AC99 counts as a criterion. | AC3 from prose is required, or a level-3 heading ends the section. | Holdout H4 |
| S3 | AC3, D1 | A DEV agent runs out of time and writes `UNPROVEN`, ` todo `, and `-` as proofs. | `no proof` for all three, exit 1. | Any placeholder passes as proof. | Holdout H2 |
| S4 | AC8 | TEST runs the checker before DEV has written EVIDENCE.md. | `error:` on stderr, exit 2, nothing on stdout. | Crash with a traceback, or exit 1 (looks like a normal failure). | Holdout H6 |
| S5 | AC9 | A messy evidence file with every kind of problem at once. | All problems in one run, sorted. | Stops at the first problem, or order is unstable. | Holdout H5 |
| S6 | AC1 | A real-looking EVIDENCE.md with a 3-column table (`AC`, `Proof`, `Notes`), bold IDs, and proof text containing backticks and a link. | `ok: 4 criteria, all with proof`. | Extra column, bold, or Markdown in proof breaks parsing. | Holdout H1 |
