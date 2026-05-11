---
name: deploy-check
description: Verify task-cli is ready to build, release, or deploy
tools: [Read, Grep, Glob, Bash]
user-invocable: true
---
Run a release readiness check for $ARGUMENTS.

Checklist:
1. Read package.json, tsconfig.json, CLAUDE.md, and README.md.
2. Verify dependencies are installed or report that `npm install` is needed.
3. Run `npm test`.
4. Run `npm run build`.
5. Check `git status --short` and summarize uncommitted changes.
6. Confirm README usage examples match the current CLI behavior.

Return:
- Status: ready or blocked
- Evidence: exact commands run
- Blockers: concrete fixes required before release
- Follow-ups: non-blocking improvements
