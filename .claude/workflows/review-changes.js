// review-changes.js — deterministic multi-agent review workflow for task-cli.
//
// Run with:  /workflows review-changes
//
// This is the runnable counterpart to the /review-suite skill. The skill is
// MODEL-DRIVEN (Claude decides when to spawn each agent). This workflow is
// DETERMINISTIC: the control flow — fan out by dimension, then adversarially
// verify every finding — runs the same way every time.
//
// Pattern demonstrated: pipeline() with NO barrier between the two stages, so a
// 'bugs' finding starts verifying while the 'perf' dimension is still being
// reviewed. Each surviving finding is confirmed only if a majority of
// independent skeptics FAIL to refute it.

export const meta = {
  name: 'review-changes',
  description: 'Review the task-cli diff across dimensions, then adversarially verify each finding',
  phases: [
    { title: 'Review', detail: 'one agent per review dimension' },
    { title: 'Verify', detail: 'independent skeptics try to refute each finding' },
  ],
}

// The dimensions we fan out over. Add or remove entries to scale the review.
const DIMENSIONS = [
  {
    key: 'correctness',
    prompt:
      'Review the uncommitted git diff of this task-cli project for CORRECTNESS bugs ' +
      '(off-by-one IDs, wrong status transitions, unhandled empty-store cases, bad JSON I/O). ' +
      'Only report issues you can point to a specific line for. Run `git diff` to see the changes.',
  },
  {
    key: 'tests',
    prompt:
      'Review the uncommitted git diff for TEST-COVERAGE gaps. For each changed function in ' +
      'src/commands/ or src/store/, is there a matching test in __tests__/ that exercises the new ' +
      'behaviour? Report any changed path with no covering test. Run `git diff` and read __tests__/.',
  },
  {
    key: 'architecture',
    prompt:
      'Review the uncommitted git diff for ARCHITECTURE violations of the layered rule: ' +
      'src/commands/ must NOT touch the filesystem directly — all JSON read/write goes through ' +
      'src/store/tasks.ts. Report any command file that reads or writes files itself.',
  },
]

// JSON Schemas force each agent to return validated structured output.
const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          file: { type: 'string' },
          line: { type: 'integer' },
          detail: { type: 'string' },
        },
        required: ['title', 'file', 'detail'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean' },
    reason: { type: 'string' },
  },
  required: ['refuted', 'reason'],
}

// How many independent skeptics vote on each finding. A finding survives only
// if fewer than a majority manage to refute it.
const SKEPTICS = 3

log(`Reviewing ${DIMENSIONS.length} dimensions, ${SKEPTICS} skeptics per finding.`)

// pipeline(): each dimension flows Review -> Verify independently, no barrier.
const results = await pipeline(
  DIMENSIONS,
  // Stage 1 — review one dimension.
  (d) => agent(d.prompt, { label: `review:${d.key}`, phase: 'Review', schema: FINDINGS }),
  // Stage 2 — adversarially verify each finding this dimension produced.
  (review, dimension) =>
    parallel(
      (review?.findings ?? []).map((f) => () =>
        parallel(
          Array.from({ length: SKEPTICS }, (_, i) => () =>
            agent(
              `You are skeptic #${i + 1}. Try to REFUTE this ${dimension.key} finding about task-cli:\n` +
                `"${f.title}" in ${f.file}${f.line ? ':' + f.line : ''} — ${f.detail}\n` +
                'Read the actual code. If the finding is wrong, not real, or already handled, set refuted=true. ' +
                'Default to refuted=true when uncertain — a false alarm is worse than a miss here.',
              { label: `verify:${f.file}#${i + 1}`, phase: 'Verify', schema: VERDICT },
            ),
          ),
        ).then((votes) => {
          const refuting = votes.filter(Boolean).filter((v) => v.refuted).length
          return { ...f, dimension: dimension.key, confirmed: refuting < Math.ceil(SKEPTICS / 2) }
        }),
      ),
    ),
)

const confirmed = results
  .flat()
  .filter(Boolean)
  .filter((f) => f.confirmed)

log(`${confirmed.length} findings survived adversarial verification.`)
return { confirmed }
