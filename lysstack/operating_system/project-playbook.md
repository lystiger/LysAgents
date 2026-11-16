# Project playbook

**Status:** Accepted by Lystiger in the Claude session of 2026-11-12, except
"UI work", which is still a draft. Drafted by Claude.

Every agent follows this playbook for a new project or a non-trivial feature.

How a new project goes from idea to shipped, based on HASC-OCR
(`projects/hasc-ocr/`). HASC-OCR ran steps 1 to 4 and 6, and each of those
names the HASC-OCR file that shows it done. Steps 7 and 8 have no record in
LysStack. Steps 5 and 9, the factory stages and the feature loop are new and
have not run on a project yet.

```
 grill --> spec + ADRs --> scenarios --> holdouts --> build --> verify --> retro
   ^                          |                         |
   +---- decision breaks -----+------- new decision ----+
```

## 1. Look at the real material first

Before asking anything, read the real inputs yourself: documents, photos,
spreadsheets, the current manual process. Write down what you saw as
"Claude's reading, to be confirmed by Lystiger".

- HASC-OCR: `brief.md` "October blower folder" (50 photos read) and
  "Sample observations".
- Failure case: the Uni-Green bench spec never looked at its photos, and the
  site shipped desk snapshots (`~/Work/bench-unigreen-2/`, outside LysStack).

## 2. Grill

Follow `AGENTS.md` "Grill-Me Mode". Ask decisions only, never facts. Each
settled answer becomes a dated decision (`P1`, `P2`, …) with its source.

- HASC-OCR: `brief.md` "Decisions", 105 entries (P1 to P105).
- If an answer depends on how reality behaves, don't argue it: run a spike
  (step 3).

## 3. Spike the unknowns

A small, throwaway experiment for each question the grill can't settle, run
before the decision it feeds.

- HASC-OCR: `brief.md` "First local model try (one sheet, not a score)".

## 4. Spec and ADRs

`spec.md` sections: context, goals, **non-goals**, requirements, **numbered
testable acceptance criteria**, design, alternatives, risks, test plan,
rollout with a way back.

Each ADR in `decisions.md` has: context, options, decision with owner,
consequences, and **"what would make this wrong"**.

Before building, check that the scope fits the time. If it doesn't, propose a
cut.

- HASC-OCR: `spec.md` §5 (acceptance criteria), §9 (test plan), §10
  (rollout); `decisions.md` ADR 1–5.

## 5. Limit scenarios

Concrete stories that push the idea, each ADR and the spec to their limits.
They turn every ADR's "what would make this wrong" into something that can be
run or rehearsed.

Write `projects/<name>/scenarios.md`, about 5 to 10 scenarios. Each one has:

| Field | Content |
|---|---|
| Attacks | The ADR, decision (`P…`) or acceptance criterion it pushes on |
| Story | Who does what, when, with which real data or limit |
| Expected | What the system must do, as stated in the spec |
| Breaks if | The observable sign that the decision was wrong |
| Proof | Holdout test, trial checklist item, or `UNPROVEN` |

Rules:

- Use the real limits from the brief (hardware, people, shifts, money, data
  volume), not generic ones. Cover load, bad input, failure and recovery,
  people and process, cost, and time.
- A different provider from the spec's author drafts them, adversarially.
  Lystiger picks which ones count.
- A scenario that breaks a decision before building is a cheap win: it goes
  back to the grill.
- Every chosen scenario becomes a holdout (step 6) or a trial checklist item.

Example built on HASC-OCR ADR 5, "What would make the timing wrong". P95 says
the 5am backup is "2 hours clear of its final photos", but photos after a
product run can still arrive late. The times below are the scenario's story,
not facts from the brief:

```
 04:55  a late product run uploads 6 sheets
 05:00  backup starts; worker holds new reads
 05:0x  backup still uploading on slow Wi-Fi
   ?    do the 6 sheets still meet the 15-minute limit (criterion)?
```

## 6. Holdouts

Tests or data the builder never sees or tunes against. They are what stops a
green test suite from lying.

- HASC-OCR: 20 labelled sheets per type, 8 for tuning and 12 hidden for
  testing, never committed (`spec.md` §9, §10).
- Chosen limit scenarios (step 5) join the holdouts.

## 7. Build

One strong session, inline, on a branch, against the spec. Record decisions as
`AGENTS.md` "Recording Decisions" says: Lystiger's or an orchestrator's
decisions go to `projects/<name>/decisions.md` with the brief revision they
came from, and an agent's routine run choices go to
`operating_system/decision-log.md`. An architecture choice is not routine: the
agent takes it to Lystiger first. Anything that changes the spec goes back to
Lystiger (the arrow back to grill).

## 8. Verify

- Automated: the spec's test plan, plus holdouts.
- Independent: a reviewer agent from a different provider, run with the
  tests; PASS is required.
- UI: screenshots at 375px and 1440px, judged against the design decisions
  (see "UI work" below).
- Production deploys stay with Lystiger.

## 9. Retro (15 minutes, per project or major version)

Write `projects/<name>/lessons.md`:

- How many decisions changed during the build, and why?
- Which bugs escaped after merge, and which step should have caught them?
- What did the grill miss?
- Which limit scenarios came true, and which real failure had no scenario?

## Factory stages

The steps above run as three stages. Stages talk through files, so any agent
can fill any stage. Any chat asked for a new product or feature is the orchestrator:
it asks what to build, grills until Lystiger says "agreed", then starts each
stage's agents with their roles and tasks.

```
 PRETEST (LysStack)       DEV (pstack)            TEST (LysRig later)
+------------------+    +------------------+    +---------------------+
| steps 1-6        |    | poteto-mode      |    | other provider      |
| spec, ADRs,      | -> | strong model     | -> | holdouts, scenarios | -> Lystiger
| scenarios,       |    | one design skill |    | screenshots, axe,   |
| holdouts, assets |    | stops at PR      |    | design audit        |
+------------------+    +------------------+    +---------------------+
  in:  brief, spec        out: branch, PR         out: VERDICT.md
       criteria #s             EVIDENCE.md
```

**PRETEST.** Steps 1 to 6. Also prepare the assets the build needs (for a
site, one clean cutout photo per product) and settle data gaps such as bank
details and prices. Builders cannot fix missing inputs.

**DEV.** pstack's `poteto-mode` on a strong model, run in the product
repository. It reads the spec from the project folder in LysStack. It writes
`EVIDENCE.md` with one row per acceptance criterion and its proof, then stops
at the PR and never merges. Holdouts stay outside its work tree. Lystiger's
own changes to pstack live in a separate skills layer, not in the pstack
mirror, so upstream syncs stay cheap.

**TEST.** A gate, never a fix loop. Planned: Lystiger's LysRig workflow is not
packaged as a runnable gate yet, so until it is, an independent reviewer agent
from a different provider fills this stage. It runs the project's verification
skill (made once with pstack's `create-verification-skill`), the holdouts and
scenarios, screenshots, axe and a design audit (a cheap model is enough), and
checks every row of `EVIDENCE.md`. It writes `VERDICT.md`: PASS, FAIL or
UNPROVEN per criterion. On FAIL the work goes back to DEV or to Lystiger.

**Model routing** (Uni-Green bench, 2026-11-12, `~/Work/bench-unigreen-2/`,
one run per arm, so treat it as a lead, not a proof): a strong model builds
UI, a cheap model audits. Use one design skill per build. The Impeccable arm
looked best in Claude's and Lystiger's review of the catalogue site (UNPROVEN:
no review record or score found). Taste for marketing pages is UNPROVEN. Run
third-party skills from a pinned, reviewed copy in a sandbox. Treat a provider
quota error as a VOID run, not a failure.

## Feature loop

Every non-trivial feature runs the factory at feature size, and ends with
Lystiger trying it as an end user.

| Step | What happens | Output |
|---|---|---|
| Ask | Grill the feature: decisions only, facts looked up first | dated decisions |
| Assume | List every assumption; spike the ones reality must answer | assumptions, spike results |
| Predict | Before code: expected behaviour, numbers and limit scenarios that would prove it wrong | predictions in the feature brief |
| Produce | DEV builds each layer it touches (backend, frontend, database, AI), stops at PR | branch, PR, `EVIDENCE.md` |
| Test | TEST gate checks criteria, holdouts and scenarios; predictions are compared with results | `VERDICT.md` |
| Ship | Lystiger gets a running build and a short walkthrough, uses it as an end user, then decides; production deploys stay with Lystiger | merge or back to Ask |

A prediction that turned out wrong is recorded in the retro, not hidden.

## AI component checklist

For products with AI inside, in addition to the steps above:

1. **Narrow contract.** The rest of the system calls one function, for
   example `read(image_path)` (HASC-OCR ADR 2). Models can change behind it.
2. **Real-data model test before choosing a model** (HASC-OCR rollout step
   1, P55, P73).
3. **Failure limits.** Timeouts, process isolation, and a fallback when the
   AI is wrong or down (HASC-OCR: 15-minute limit, fresh process per photo,
   Zalo kept running during the trial).
4. **Corrections feed evals.** Every human correction is a labelled
   example. Grow the holdout set from them.
5. **A cost and accuracy target**, decided in the grill, measured on
   holdouts.

## UI work

Draft, not accepted yet. To be settled with Lystiger: taste decisions need
their own grill round, references and a screenshot gate. See the discussion of
2026-11-12.