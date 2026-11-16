# Retro: check-evidence trial (2026-11-17)

First end-to-end run of PRETEST -> DEV -> TEST. Grill "agreed" at 01:28,
VERDICT at about 01:33.

## Predictions vs results

| Prediction | Result |
|---|---|
| P1. DEV's own tests pass first time | Right. 20 tests, OK. |
| P2. 7 or 8 of 9 holdouts, misses on H4/H5 | Wrong. 9/9. The spec was precise enough that the hard cases weren't hard. |
| P3. AC10 (Python 3.10+) ends UNPROVEN | Wrong. Both DEV and TEST ran the suite on 3.10.20 with `uv`. |
| P4. Under 30 minutes | Right. About 5 minutes. |

## What escaped, and which step should have caught it

- **`**UNPROVEN**` in bold passes as proof.** Found by DEV (ambiguity 4)
  and confirmed by TEST. This is the exact failure D1 was meant to stop: a
  green checker on unproven work. PRETEST wrote the placeholder rule but
  no scenario attacked it with Markdown formatting. S3 only used plain text.
- **A `## ` line inside a fenced code block ends the criteria section.**
  Spec gap. No scenario covered code fences.
- **AC11 says "one or two sentences"; the README has four.** TEST passed it
  as "within intent". A verifier that relaxes a stated limit is a soft gate.

All 9 holdouts passed, and every gap was found outside them, by agents
probing the edges themselves. Holdouts proved the contract; the probing
found where the contract was thin.

## What the grill missed

- How Markdown formatting interacts with placeholders and headings.
- Whether TEST may judge "intent" or must apply the letter of an AC.

## Process deviations

- TEST ran on Claude Sonnet, same provider as DEV (G5). Different-provider
  review is UNPROVEN.
- Holdouts were hidden by instruction only (DEV reported it did not read
  them). Nothing enforced the fence.
- PRETEST scenarios were drafted by the spec's author, not adversarially by
  another provider.

## Follow-ups (each goes back to the grill, not straight into code)

1. Strip `*`, `_` and backticks before the placeholder test, so
   `**UNPROVEN**` is no proof. New AC plus a holdout.
2. Ignore heading lines inside fenced code blocks.
3. Tell the TEST stage to apply numeric limits literally, and to mark
   "within intent" as UNPROVEN instead of PASS.
