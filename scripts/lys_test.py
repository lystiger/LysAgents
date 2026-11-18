#!/usr/bin/env python3
"""TEST gate: run hidden holdouts and an independent verifier on a PR, then
post the verdict as a commit status that branch protection can require.

    lys_test.py PR --spec PATH --evidence PATH --holdouts DIR [options]

Holdouts contract: DIR/run is executable, takes the checkout path as its only
argument, prints its results and exits 0 only when every holdout passes.
DIR must be outside the repository so the builder cannot read it.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

CONTEXT = "lys/verdict"
DEFAULT_VERIFIER = (
    "codex exec --sandbox workspace-write -C {worktree} "
    "--output-last-message {verdict_file} - < {prompt_file}"
)
BRIEF = Path(__file__).resolve().parent.parent / "lysstack/operating_system/test-brief.md"
OVERALL = re.compile(r"^\s*Overall:\s*(PASS|FAIL|UNPROVEN)\s*$", re.MULTILINE)
STATE = {"PASS": "success", "FAIL": "failure", "UNPROVEN": "failure"}


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout.strip()


def overall(verdict_text: str) -> str:
    found = OVERALL.findall(verdict_text)
    return found[-1] if found else "UNPROVEN"


def combine(holdouts_ok: bool, verifier_overall: str) -> str:
    return verifier_overall if holdouts_ok else "FAIL"


def build_prompt(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def inside(child: Path, parent: Path) -> bool:
    return child == parent or parent in child.parents


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pr", type=int)
    ap.add_argument("--spec", required=True, help="spec path inside the repo")
    ap.add_argument("--evidence", required=True, help="EVIDENCE.md path inside the repo")
    ap.add_argument("--holdouts", required=True, type=Path, help="directory with an executable `run`")
    ap.add_argument("--repo", help="owner/name; default: from `gh repo view`")
    ap.add_argument("--verifier", default=os.environ.get("LYS_VERIFIER", DEFAULT_VERIFIER),
                    help="shell command; placeholders {worktree} {prompt_file} {verdict_file}")
    ap.add_argument("--out", type=Path, default=Path.home() / ".lys-test/runs")
    ap.add_argument("--no-post", action="store_true", help="do not post a commit status")
    ap.add_argument("--comment", action="store_true", help="also post the verdict as a PR comment")
    a = ap.parse_args(argv)

    root = Path(sh(["git", "rev-parse", "--show-toplevel"]))
    holdouts = a.holdouts.resolve()
    if inside(holdouts, root):
        print(f"error: holdouts {holdouts} are inside the repository; move them out", file=sys.stderr)
        return 2
    if not os.access(holdouts / "run", os.X_OK):
        print(f"error: {holdouts}/run is missing or not executable", file=sys.stderr)
        return 2

    repo = a.repo or sh(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
    pr = json.loads(sh(["gh", "api", f"repos/{repo}/pulls/{a.pr}"]))
    sha = pr["head"]["sha"]
    run_dir = a.out / f"{repo.replace('/', '-')}-{a.pr}-{sha[:12]}"
    run_dir.mkdir(parents=True, exist_ok=True)

    sh(["git", "fetch", "-q", "origin", f"pull/{a.pr}/head"], cwd=root)
    worktree = Path(tempfile.mkdtemp(prefix=f"lys-test-{a.pr}-"))
    sh(["git", "worktree", "add", "-q", "--detach", str(worktree), sha], cwd=root)
    try:
        if not post_pending(a, repo, sha):
            return 2
        h = subprocess.run([str(holdouts / "run"), str(worktree)], capture_output=True, text=True)
        holdout_output = (h.stdout + h.stderr).strip() or "(no output)"
        (run_dir / "holdouts.txt").write_text(f"exit {h.returncode}\n{holdout_output}\n")

        prompt_file, verdict_file = run_dir / "prompt.md", run_dir / "VERDICT.md"
        verdict_file.write_text("")
        prompt_file.write_text(build_prompt(
            BRIEF.read_text(), repo=repo, pr=str(a.pr), sha=sha, spec=a.spec,
            evidence=a.evidence, holdout_output=holdout_output))
        cmd = a.verifier.format(worktree=shlex.quote(str(worktree)),
                                prompt_file=shlex.quote(str(prompt_file)),
                                verdict_file=shlex.quote(str(verdict_file)))
        v = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=worktree)
        (run_dir / "verifier.log").write_text(f"$ {cmd}\nexit {v.returncode}\n{v.stdout}\n{v.stderr}")
        verdict = verdict_file.read_text().strip() or v.stdout.strip()
        verdict_file.write_text(verdict + "\n")

        touched = sh(["git", "status", "--porcelain", "--untracked-files=no"], cwd=worktree)
        result = combine(h.returncode == 0, overall(verdict))
        if touched:
            result = "FAIL"
        why = ("verifier changed tracked files" if touched
               else "holdouts failed" if h.returncode != 0
               else f"verifier: {overall(verdict)}")
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=root, capture_output=True)

    description = f"{result} ({why})"[:140]
    print(f"{repo}#{a.pr} @ {sha[:12]}: {description}")
    print(f"verdict: {run_dir / 'VERDICT.md'}")
    if not a.no_post:
        sh(["gh", "api", f"repos/{repo}/statuses/{sha}", "-f", f"state={STATE[result]}",
            "-f", f"context={CONTEXT}", "-f", f"description={description}"])
        if a.comment:
            sh(["gh", "api", f"repos/{repo}/issues/{a.pr}/comments", "-F", f"body=@{run_dir / 'VERDICT.md'}"])
    return 0 if result == "PASS" else 1


def post_pending(a, repo, sha) -> bool:
    if a.no_post:
        return True
    try:
        sh(["gh", "api", f"repos/{repo}/statuses/{sha}", "-f", "state=pending",
            "-f", f"context={CONTEXT}", "-f", "description=lys-test running"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"error: could not post status: {e.stderr.strip()}", file=sys.stderr)
        return False


if __name__ == "__main__":
    sys.exit(main())
