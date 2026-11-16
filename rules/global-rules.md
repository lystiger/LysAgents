# How to work with me

Adapted from andrej-karpathy-skills. These bias toward caution over speed; for trivial tasks, use judgment.

## Think before coding
- State assumptions. If a request has several readings, say which you picked or ask; don't choose silently.
- If a simpler approach exists, say so and push back.
- If something is unclear, stop and name what is confusing.

## Simplicity first
- Minimum code that solves the problem. No features, options or abstractions that weren't asked for.
- No error handling for impossible cases. If 200 lines could be 50, rewrite it.

## Surgical changes
- Touch only what the task needs. Match the existing style, even if you'd do it differently.
- Don't reformat or refactor neighbouring code. Mention unrelated dead code; don't delete it.
- Remove only the imports, variables and functions your own change made unused.

## Goal-driven execution
- Turn the task into a check: a failing test that then passes, a command whose output proves it.
- For multi-step work, give a short plan with a verify step for each item, then loop until each passes.
- For UI or data tasks, run a one-shot verification script (headless browser DOM/contrast/layout checks and source-data assertions) to prove invariants before stopping.

## Quality bar
- Judge the result by looking at it, not by the checks passing. A green check script proves only what it tests.
- Before building, inspect every input yourself: open the papers, and view the images, for example as a contact sheet (`magick montage`). Know what material you have and how good it is.
- If the spec asks for more than fits the time, say so and propose a cut before building. A smaller thing done well beats a long feature list done shallowly.
- For any UI work, use ui-ux-pro-max first, whatever agent you are: read `~/.claude/skills/ui-ux-pro-max/SKILL.md`, run `python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<product> <industry> <keywords>" --design-system`, and record the chosen style, palette and fonts in the project. It is one install for every agent on this machine; read its `${CLAUDE_PLUGIN_ROOT}/.claude/skills/...` paths as `~/.claude/skills/...`. If the file is missing, say so and mark the design choices UNPROVEN instead of skipping the step silently.
- For React UI, don't hand-build components a library already does well. Read `~/.claude/skills/pick-ui-library/SKILL.md` (Emil Kowalski's curated list, pinned from `github.com/lystiger/skills` at `0f2e23b`), check `package.json` first, then use the listed library: base-ui for primitives, Sonner for toasts, Vaul for drawers, cmdk for command menus, NumberFlow for animated numbers. Don't ship default shadcn styling unchanged.
- For 3D web work only (three.js, React Three Fiber, WebGL/WebGPU, glTF from Blender), read `~/.claude/skills/3d/SKILL.md` and then only the references the task needs. Don't load it for other UI work.
- Before calling UI done, screenshot it at phone and desktop width with `chromium --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=4000 --window-size=<375 or 1440>,4000 --screenshot=<file.png> <url>`, open the images, and fix what looks wrong against the design brief.
- Never ship raw photos just resized. Crop to one aspect ratio, put the product on a neutral background with even padding, and drop images that are not product photos (print dielines, duplicates).
- When a result is poor, find the shared cause (spec, inputs or gate) before blaming the tool or the agent.
- Back every claim with evidence: `file:line`, command output or a screenshot. Mark anything unverified UNPROVEN.

## My stack
- Omarchy on Arch: Hyprland configured in Lua, the bar and widgets in Quickshell (QML), scripts in bash and Python.
- For Hyprland, Quickshell and Omarchy, the installed source under `/usr/share/omarchy` is the version actually running: read it before relying on memory or web docs.
- For other libraries and CLIs, fetch current docs with Context7 instead of answering from memory.
- Verify with what the project already uses: its test suite, `bash -n` for shell scripts, `hyprctl configerrors` after Hyprland changes.

## Diagrams
- Use ASCII diagrams in code comments, commit messages, specs and rules files that are read in a terminal or by agents. Keep them small (about eight boxes or fewer) and use plain ASCII characters so the columns stay aligned.
- Use Mermaid in READMEs, PR descriptions and docs rendered on GitHub or Claude Docs when the diagram has more than about eight nodes, or is a sequence, ER or Gantt chart. Put a one-line text summary above it.

## Multi-agent work
- Hermes (`~/Projects/Hermes-lab`) is retired as of 2026-11-09 and its stack is unplugged; don't propose or launch Hermes jobs.
- Work inline: whenever Lystiger asks for a new product or feature, in words or with a slash command, that chat becomes the orchestrator. It asks what to build, runs grill mode (`~/Projects/LysStack/AGENTS.md`) until Lystiger says "agreed", then runs the stages PRETEST, DEV and TEST, starting each stage's agents with their roles and tasks and handing work between stages through files. There is no separate orchestrator service. Features keep the same gates: a branch and PR, tests and CI green, and an independent reviewer agent's PASS before merging; never merge on a FAIL or UNPROVEN verdict. Production deploys stay with Lystiger.
- Project briefs, specs, decisions and roadmaps live in `~/Projects/LysStack/projects/<name>/`; read them before planning or changing a project, and follow `~/Projects/LysStack/AGENTS.md` when editing LysStack.
- For every new project or non-trivial feature, follow `~/Projects/LysStack/operating_system/project-playbook.md`: ask, assume, predict, produce, test, ship, and hand the result to Lystiger to try as an end user.
- The playbook runs in three stages that talk through files: PRETEST in LysStack (spec, scenarios, holdouts), DEV with pstack's `poteto-mode` in the product repository (writes `EVIDENCE.md`, stops at the PR, never merges), and TEST by a reviewer agent from a different provider, until Lystiger's LysRig gate is packaged (writes `VERDICT.md`: PASS, FAIL or UNPROVEN per criterion).
