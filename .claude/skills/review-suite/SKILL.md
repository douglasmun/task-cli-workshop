---
name: review-suite
description: >
  Run a full pre-merge review suite: security scan + test coverage review,
  each in its own isolated subagent. Results are synthesised into a single
  go/no-go recommendation. Invoke before merging any feature branch.
tools: [Read, Grep, Glob, Bash, Agent]
context: fork
user-invocable: true
---

# Review Suite — Orchestrated Agent Handoff

This skill demonstrates agent orchestration: two specialist agents run in
parallel subagents via context:fork. Each agent receives a focused task,
produces a structured report, and hands results back to this skill. The
main session context is never polluted with their working state.

## How to invoke

```
/review-suite                        # review the current branch
/review-suite src/commands/done.ts   # focus on a specific file
```

## Execution plan

**Step 1 — Dispatch security-scanner (context:fork)**

Spawn the security-scanner agent as a subagent. Pass the scope from
$ARGUMENTS (or default to all src/ files if no argument given).

Prompt to send the subagent:
> You are the security-scanner agent. Read .claude/agents/security-scanner.md
> for your full instructions. Scan: $ARGUMENTS (default: src/ and .claude/hooks/).
> Return the SECURITY SCAN REPORT in the exact format specified.

The subagent runs in an isolated context. It reads source files, writes to
its MEMORY.md, and returns only the formatted report. It cannot edit source
files (permissionMode: plan).

**Step 2 — Dispatch test-reviewer (context:fork)**

Simultaneously spawn the test-reviewer agent as a second subagent.

Prompt to send the subagent:
> You are the test-reviewer agent. Read .claude/agents/test-reviewer.md for
> your full instructions. Focus on: $ARGUMENTS (default: all of src/ vs __tests__/).
> Return your coverage report in the format specified in your instructions.

This agent also runs isolated, reads test files, updates its own MEMORY.md,
and returns a structured coverage report.

**Step 3 — Synthesise results**

Once both subagents complete, synthesise their outputs into a single decision:

```
REVIEW SUITE SUMMARY
====================
Security: PASS | BLOCK (critical findings present)
Coverage: PASS | WARN  (missing tests present)
Overall:  GO   | NO-GO

Blocking issues (must fix before merge):
  [from security report — critical findings only]
  [from coverage report — missing tests for changed files]

Non-blocking (fix in follow-up):
  [warnings from security report]
  [weak tests from coverage report]

Recommendation: [GO — safe to merge] or [NO-GO — fix blocking issues first]
```

## Why two agents instead of one

- **Separation of concerns**: security-scanner uses Haiku (fast, cheap for
  pattern matching); test-reviewer uses Sonnet (better reasoning about
  coverage gaps). Running them in parallel is faster than sequential.

- **Context isolation**: each agent's working state (MEMORY.md lookups,
  file reads) stays in its own subagent context. The main session receives
  only the final reports — no token waste from intermediate reasoning.

- **Independent memory**: each agent maintains its own MEMORY.md tracking
  patterns it has seen across sessions. Their memories do not cross-contaminate.

This is the same pattern used in Claude Code's built-in Explore + Plan +
General-purpose orchestration: specialist agents perceive and reason in
isolation; the orchestrating context synthesises and acts.
