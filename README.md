# LysAgents

How Lystiger works with coding agents: the rules every agent follows, the
delivery playbook, and the model and skill setup. This repository holds the
workstyle only. It contains no product code and no project briefs.

Snapshot taken 2026-11-17 from the files that are installed and running.

## Layout

| Path | What it is | Source |
|---|---|---|
| `rules/global-rules.md` | Rules every agent follows: thinking, simplicity, surgical changes, evidence, UI quality bar, multi-agent gates | `~/.claude/CLAUDE.md` (installed from `LysOmarchy/agents/rules.md`) |
| `rules/RTK.md` | How agents treat condensed command output | `~/.claude/RTK.md` |
| `rules/pstack-models.md` | Which model runs each pstack role | `~/.claude/rules/pstack-models.md` |
| `lysstack/AGENTS.md` | Agent rules for LysStack: review roles, grill mode, task lifecycle, decision records | `LysStack/AGENTS.md` |
| `lysstack/operating_system/project-playbook.md` | Idea to shipped: grill, spike, spec, scenarios, holdouts, build, verify, retro; PRETEST, DEV and TEST stages | `LysStack/operating_system/` |
| `lysstack/operating_system/stages.toml` | Which harness and skill run each stage | `LysStack/operating_system/` |
| `lysstack/operating_system/models.toml` | Models and efforts each harness may use | `LysStack/operating_system/` |
| `skills.md` | Installed plugins and skills | `~/.claude/skills` |

## Workflow at a glance

```
 PRETEST (LysStack)       DEV (pstack)            TEST (other provider)
+------------------+    +------------------+    +---------------------+
| grill, spec,     | -> | poteto-mode      | -> | holdouts, scenarios | -> Lystiger
| ADRs, scenarios, |    | branch + PR      |    | VERDICT.md          |
| holdouts         |    | EVIDENCE.md      |    | PASS/FAIL/UNPROVEN  |
+------------------+    +------------------+    +---------------------+
```

## Running the TEST gate

`scripts/lys_test.py` runs the TEST stage on your machine and posts the result
as the commit status `lys/verdict`, so branch protection can block merges
without a PASS. No GitHub Actions minutes are used.

```
python3 scripts/lys_test.py <PR> \
  --spec trials/<name>/spec.md --evidence trials/<name>/EVIDENCE.md \
  --holdouts ~/lys-holdouts/<name>
```

It checks out the PR head in a throwaway worktree, runs `<holdouts>/run
<worktree>` (the holdouts folder must be outside the repository), then runs
Codex with `lysstack/operating_system/test-brief.md` and reads the last
`Overall:` line. Failed holdouts, a missing `Overall:` line, UNPROVEN, or a
verifier that edits tracked files all post `failure`. Runs are kept in
`~/.lys-test/runs/`. Use `--verifier` or `LYS_VERIFIER` for a different
command, `--no-post` for a dry run and `--comment` to post the verdict on the
PR. To enforce it, require the `lys/verdict` status check on `main`.

## Left out on purpose

- Run and decision logs (`run-log.md`, `decision-log.md`).
- Current project state (`active_task.md`, `current_focus.md`) and all
  `projects/<name>/` briefs, specs and verdicts.
- `hermes-delivery.md`: Hermes was retired on 2026-11-09.

`lysstack/AGENTS.md` and the playbook still reference these files and project
folders by path. The playbook also cites past projects (HASC-OCR, Uni-Green)
as worked examples.

## Related public repositories

- [lystiger/pstack](https://github.com/lystiger/pstack): workflow skills such as
  `poteto-mode`, `arena`, `architect` and `interrogate`.
- [lystiger/skills](https://github.com/lystiger/skills): curated skills,
  including `pick-ui-library`.
