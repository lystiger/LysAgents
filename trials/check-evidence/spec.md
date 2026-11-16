# Spec: check-evidence

**Status:** Ready (Lystiger said "agreed" to grill round 1, 2026-11-17 01:28).
**Target repo:** lystiger/LysAgents, branch `feat/check-evidence`.
**Drafted by:** Claude (PRETEST stage).

## Context

The playbook's DEV stage writes `EVIDENCE.md` with one row per acceptance
criterion, and TEST checks every row. Nothing checks mechanically that the
rows match the spec. A criterion can be dropped, or a proof cell left as
`TODO`, and only a careful reader notices. This turns that check into a
lever any stage can rerun.

## Goals

- One command says whether `EVIDENCE.md` covers every criterion in
  `spec.md`, each with a proof, and names every gap.

## Non-goals

- Judging whether a proof is *true*. That stays with the TEST reviewer.
- Parsing any other file (VERDICT.md, scenarios.md).
- Fixing or rewriting either file.
- Escaped pipes (`\|`) inside table cells.

## Decisions

- G1 (Lystiger, round 1): target LysAgents, stop at PR, Lystiger merges.
- G2 (Lystiger): feature is `check-evidence`.
- G3 (Lystiger): one file, `scripts/check_evidence.py`, standard library only.
- G4 (Lystiger): format contract below.
- G5 (Lystiger): TEST by a fresh Claude agent on a different model; the
  different-provider rule is UNPROVEN for this trial.
- G6 (Lystiger): holdouts written in PRETEST, kept outside DEV's work tree.
- D1 (Claude, PRETEST, routine): a proof of `UNPROVEN` counts as no proof.
  Reason: UNPROVEN means "no proof yet"; a checker that passes it would
  report green on unproven work. Also treated as no proof: empty, `TODO`,
  `TBD`, `-`, case-insensitive, after trimming spaces.

## Format contract

**Spec.** Criteria live in the section whose heading is exactly
`## Acceptance criteria` (case-insensitive), up to the next heading of level
1 or 2 (`# ` or `## `). A criterion is a line that starts with `AC<number>.`,
optionally after a list marker (`- `, `* `) and leading spaces. `AC<n>`
written anywhere else, inside or outside the section, is not a criterion.

**Evidence.** A Markdown table row is a line that starts with `|` (after
optional spaces). A row counts when its first cell, trimmed, is exactly
`AC<number>` (optionally wrapped in `**`). Its proof is the second cell.
Header and separator rows are ignored because their first cell is not
`AC<number>`. Extra columns are ignored.

**Numbers.** IDs compare as integers: `AC1` and `AC10` are different,
`AC01` equals `AC1`. Output always prints `AC<int>` without leading zeros.

## Acceptance criteria

AC1. `python3 scripts/check_evidence.py SPEC EVIDENCE` exits 0 and prints
exactly `ok: <N> criteria, all with proof` when every criterion has exactly
one row with a proof and there are no other rows.

AC2. A criterion with no row prints `missing: AC<n>` and exits 1.

AC3. A row whose proof is empty or a placeholder (see D1) prints
`no proof: AC<n>` and exits 1.

AC4. A row for a number that is not a criterion prints `unknown: AC<n>` and
exits 1.

AC5. A criterion with two or more rows prints `duplicate: AC<n>` once and
exits 1. Duplicates are not also checked for proof.

AC6. IDs compare as integers, so `AC1` evidence does not satisfy `AC10`,
and `AC01` satisfies `AC1`.

AC7. Only lines in the `## Acceptance criteria` section, starting with
`AC<n>.`, are criteria. Mentions of `AC<n>` in prose or other sections are
ignored.

AC8. Missing or unreadable file, no `## Acceptance criteria` section, or a
section with zero criteria prints one line starting `error:` to stderr and
exits 2. Wrong argument count also exits 2 with a usage line on stderr.

AC9. All problems are reported in one run, one per line on stdout, sorted by
AC number, then by kind in the order missing, no proof, duplicate, unknown.

AC10. One file, Python standard library only, runs on Python 3.10+. Tests
in `tests/` run green with `python3 -m unittest discover -s tests`.

AC11. `README.md` gains a short "Checking evidence" section with the
command and the format contract in one or two sentences.

## Design

Two pure functions, `parse_criteria(text) -> list[int]` and
`parse_evidence(text) -> list[tuple[int, str]]`, and one
`check(criteria, rows) -> list[str]` that returns the problem lines. `main`
handles files, exit codes and printing.

## Alternatives

- A Markdown library: rejected by G3 (stdlib only).
- Accept `UNPROVEN` as a proof: rejected by D1.

## Risks

- Real EVIDENCE.md files may use a different first-column label. The
  contract is strict on purpose; a mismatch shows up as `missing`.

## Test plan

- DEV: unit tests in `tests/`.
- TEST: hidden holdouts and the scenarios in `scenarios.md`, run by an
  independent agent.

## Rollout

A new file and a README section. Way back: revert the PR.
