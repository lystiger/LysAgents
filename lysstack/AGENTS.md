# AGENTS.md

This is the single entry point for AI agents working in LysStack. Global coding,
stack, diagram and inline delivery rules live in `~/Projects/LysOmarchy/agents/rules.md`
(installed into `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and `~/.gemini/AGENTS.md`).

LysStack is the engineering knowledge and brief repository: policy, decisions,
constraints, lessons, task briefs, specs, and long-term memory. Product source
code lives in product repositories. **LysStack contains no product code and runs
no jobs.** Work runs inline in product repositories under the delivery gates
in the global agent rules (`~/Projects/LysOmarchy/agents/rules.md`, "Multi-agent
work"); this file does not restate them.

## Sources of Truth

| Question | Source |
| --- | --- |
| How does a new project or feature run? | `operating_system/project-playbook.md` (every agent follows it) |
| What matters now? | `operating_system/current_focus.md` |
| What is the active brief? | `operating_system/active_task.md` |
| How is a project specified or scoped? | `projects/<project>/brief.md`, `projects/<project>/spec.md`, `projects/<project>/roadmap.md` |
| How is a project designed? | `projects/<project>/architecture.md` |
| What limits the solution? | `projects/<project>/constraints.md` |
| What has Lystiger decided? | `projects/<project>/decisions.md` |
| What did agents decide along the way? | `operating_system/decision-log.md` |
| What failed or was learned? | `projects/<project>/lessons.md` |
| What applies across projects? | `memory/` |

`current_focus.md` sets priorities but does not authorize work.

## Review Roles (Inline & Herdr Crew)

When reviewing or running multi-pane work (`~/Projects/Herdr-lab/crew.sh`), roles
describe phase responsibilities, not fixed agents:

- **BUILDER:** implements the acceptance criteria with minimal scope, tests first.
- **HARDENER:** reviews the Builder branch and changes code only for a concrete defect, risk, or missing acceptance criterion.
- **VERIFIER:** independent adversarial evaluation by a different agent/provider without modifying product source. Classifies every acceptance criterion as `PASS`, `FAIL`, or `UNPROVEN`.
- **SECURITY:** read-only review for injection, unauthorized access, secret leaks, data exposure, and dependency risk (`PASS`, `FAIL`, or `UNPROVEN`).
- **Lystiger:** approves specs (`Ready`), reviews merged changes, and owns production deploys.

## Agent Rules in LysStack

1. Draft briefs and specs only. Never set a brief to `Ready`; only Lystiger does that.
2. Stay in scope. Name anything out of scope instead of doing it.
3. Route project decisions to `projects/<project>/decisions.md` and routine run choices to `operating_system/decision-log.md`.
4. Label evidence. Test results and tool output are deterministic. Reasoning is not proof.
5. Mark anything unverified as `UNPROVEN` rather than guessing.
6. Never write secrets, credentials, or private data into the repository.
7. Stop and report when blocked or when a round cap is reached. Do not loop.
8. Address the user as Lystiger. Do not call the user "the human" or "a human" in messages to them.

## Grill-Me Mode

Run grill-me before drafting any big task. A task is big when it spans more than one module or repository, changes an API or data model, or has more than about five acceptance criteria. The method follows Matt Pocock's grilling skill (github.com/mattpocock/skills).

- **Frontier rounds.** Each round asks every question whose prerequisites are settled. Number them, and give each a recommended answer. Lystiger replies "yes" to take all the recommendations, or names the numbers to change. Questions that depend on an open one wait for a later round.
- **Facts first.** Before asking, look things up in `LysStack` and the target repository. Ask only decisions, never facts.
- **Record as you go.** Each settled answer goes into the brief's Decisions section, with its source (Lystiger, or the fact that settled it). Nothing is written to a project `decisions.md` until Lystiger promotes it.
- **Stop when the frontier is empty and Lystiger says "agreed".** Then build the brief or spec and save it as a draft. Do not act on the plan before that confirmation.
- **Safety cap.** At six rounds, stop and list what is still open. This is a warning, not a silent end.

## Task Lifecycle

Statuses: `Draft` → `Ready` → `In progress` → `Complete`, with `Blocked` when work cannot continue.

1. **Draft:** Lystiger, or an agent on Lystiger's instruction, writes the brief or spec. A draft is never executed.
2. **Ready:** only Lystiger sets this. It requires a project, goal, target repository, acceptance criteria, and verification commands.
3. **In progress:** work runs inline (or via Herdr crew) on a branch/worktree in the target repository.
4. **Complete:** only after every acceptance criterion passes, deterministic verification and independent review (`PASS`) are recorded, and the PR is merged.

Use `Blocked` with the blocker, what was tried, and what is needed to resume.

## Recording Decisions

- **Human or orchestrator decisions** (architecture, constraints, meaningful
  tradeoffs, and every change a human makes to a brief that should apply
  later) go to `projects/<project>/decisions.md`. Each entry names the brief
  revision it came from.
- **Agent-level decisions** (routine choices made during a run) go to
  `operating_system/decision-log.md`.
- **Cross-project knowledge** goes to `memory/`.
- **Routine implementation details** are not decisions. Do not record them.

Decision format:

```markdown
### Decision 001: Title

- **Date:** YYYY-MM-DD
- **Source:** human, orchestrator, or agent; brief revision if any
- **Problem:** What needs to be decided?
- **Decision:** What was selected?
- **Reason:** Why was it selected?
- **Rejected:** What alternatives were rejected?
- **Status:** Proposed, accepted, superseded, or rejected
```

## Completion Protocol

Before a brief is marked `Complete`:

- Confirm every acceptance criterion
- Run the listed verification commands, or record why they could not run
- Record significant decisions in the project's `decisions.md`
- Record reusable lessons in the project's `lessons.md`
- Promote cross-project knowledge to `memory/`
- Update architecture, constraints, or deployment docs if the work changed them
- Add a completion summary and verification results to `active_task.md`
- Update `current_focus.md` if priorities or blockers changed

## Hard Constraints

- Never commit secrets, credentials, PII, or private business data.
- Merge only after the gates in the global agent rules pass.
- Keep this repository Markdown-first and config-only. Product source belongs in
  its product repository.
- Do not add heavy agent frameworks without a recorded decision in
  `memory/decisions.md`.
