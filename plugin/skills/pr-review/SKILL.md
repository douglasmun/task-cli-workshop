---
name: pr-review
description: Review a branch diff against the task-cli project standards
tools: [Read, Grep, Glob, Bash]
user-invocable: true
---
Review the pull request or branch diff described by $ARGUMENTS.

Process:
1. Read CLAUDE.md and docs/architecture.md.
2. Run `git status --short` and inspect the diff against the requested base ref, defaulting to `main`.
3. Review for correctness, security issues, TypeScript strictness, missing tests, and direct file I/O outside src/store/.
4. Run `npm test` when dependencies are installed.
5. Return findings first, ordered by severity, with file and line references.

Do not rewrite the code during review unless the user explicitly asks for fixes.
