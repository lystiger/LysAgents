#!/usr/bin/env python3
"""Check that an EVIDENCE.md table gives a proof for every criterion in a spec.md.

Usage: python3 scripts/check_evidence.py SPEC EVIDENCE
Exit 0 when complete, 1 when there are gaps, 2 on usage or input errors.
"""

import re
import sys

USAGE = "usage: check_evidence.py SPEC EVIDENCE"

SECTION_HEADING = "## acceptance criteria"
SECTION_END = re.compile(r"#{1,2} ")
CRITERION = re.compile(r"\s*(?:[-*] +)?AC(\d+)\.")
ROW_ID = re.compile(r"AC(\d+)|\*\*AC(\d+)\*\*")
PLACEHOLDERS = {"", "todo", "tbd", "-", "unproven"}

KIND_ORDER = ("missing", "no proof", "duplicate", "unknown")


class InputError(Exception):
    pass


def parse_criteria(text: str) -> list[int]:
    criteria = []
    in_section = False
    for line in text.splitlines():
        if line.rstrip().lower() == SECTION_HEADING:
            in_section = True
            continue
        if in_section and SECTION_END.match(line):
            break
        if in_section and (m := CRITERION.match(line)):
            criteria.append(int(m.group(1)))
    if not in_section:
        raise InputError("no '## Acceptance criteria' section")
    if not criteria:
        raise InputError("'## Acceptance criteria' section has no criteria")
    return criteria


def parse_evidence(text: str) -> list[tuple[int, str]]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = stripped[1:].split("|")
        m = ROW_ID.fullmatch(cells[0].strip())
        if m:
            proof = cells[1].strip() if len(cells) > 1 else ""
            rows.append((int(m.group(1) or m.group(2)), proof))
    return rows


def check(criteria: list[int], rows: list[tuple[int, str]]) -> list[str]:
    proofs: dict[int, list[str]] = {}
    for number, proof in rows:
        proofs.setdefault(number, []).append(proof)

    problems = set()
    for number in set(criteria):
        found = proofs.get(number, [])
        if not found:
            problems.add((number, "missing"))
        elif len(found) > 1:
            problems.add((number, "duplicate"))
        elif found[0].lower() in PLACEHOLDERS:
            problems.add((number, "no proof"))
    for number in proofs.keys() - set(criteria):
        problems.add((number, "unknown"))

    ordered = sorted(problems, key=lambda p: (p[0], KIND_ORDER.index(p[1])))
    return [f"{kind}: AC{number}" for number, kind in ordered]


def read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise InputError(f"cannot read {path}: {e}") from e


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    spec_path, evidence_path = argv
    try:
        criteria = parse_criteria(read(spec_path))
        rows = parse_evidence(read(evidence_path))
    except InputError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    problems = check(criteria, rows)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"ok: {len(set(criteria))} criteria, all with proof")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
