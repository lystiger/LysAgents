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

## Checking evidence

`python3 scripts/check_evidence.py SPEC EVIDENCE` checks that every
criterion in a spec has exactly one proof row in its EVIDENCE.md. It exits 0
when complete, 1 with one problem per line, and 2 on bad input. Criteria are
lines starting `AC<n>.` under `## Acceptance criteria`. Proofs are the second
cell of table rows whose first cell is `AC<n>`, and empty, `TODO`, `TBD`, `-`
or `UNPROVEN` count as no proof.

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
