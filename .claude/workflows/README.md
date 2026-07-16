# Workflows — deterministic multi-agent orchestration

This folder holds `/workflows` scripts: JavaScript that orchestrates subagents
with **deterministic** control flow (loops, conditionals, fan-out) that runs the
same way every time. This is the counterpart to the model-driven `/review-suite`
skill in `.claude/skills/` — same goal (a thorough pre-merge review), different
control model.

| | `/review-suite` (skill) | `/workflows review-changes` |
|---|---|---|
| Control flow | Model decides when to spawn agents | You script it — same every run |
| Defined in | `SKILL.md` (natural language) | `.js` (agent/pipeline/parallel) |
| Verification | Agents report; you judge | Adversarial: N skeptics refute each finding |

## Try it (course Module 17)

```bash
git checkout main
# make a small change to a command so there's a diff to review, e.g.:
#   edit src/commands/done.ts
claude
/workflows review-changes
```

Watch the live progress tree with `/workflows`. The `Review` phase fans out one
agent per dimension (correctness, tests, architecture); the `Verify` phase
spawns independent skeptics that each try to *refute* every finding. Only
findings a majority of skeptics fail to refute are returned.

## Scripts

- **`review-changes.js`** — review the uncommitted diff across three dimensions,
  then adversarially verify each finding. Demonstrates `pipeline()` with no
  barrier between stages, nested `parallel()` for the skeptic vote, and JSON
  Schemas for validated structured output.

## Scaling it

- Add a dimension: append to the `DIMENSIONS` array in `review-changes.js`.
- Stricter verification: raise `SKEPTICS` (more skeptics per finding).
- Broader review: point the prompts at `git diff main...HEAD` instead of the
  uncommitted diff to review a whole feature branch.
