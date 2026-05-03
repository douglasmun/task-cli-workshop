---
name: add-feature
description: Plan and implement a new feature for the task-cli project
tools: [Read, Edit, Write, Bash, Grep, Glob]
user-invocable: true
---
Implement the feature described by $ARGUMENTS for the task-cli project.

Follow this process:
1. Read CLAUDE.md and understand the project conventions
2. Plan the changes needed (which files to modify/create)
3. Implement the feature following the existing patterns in src/commands/
4. Add or update tests in __tests__/
5. Run `npm test` to verify all tests pass
6. Run `npm run format` to ensure consistent formatting

Constraints:
- Follow the conventions in CLAUDE.md
- All file I/O goes through src/store/tasks.ts
- Every new command gets its own file in src/commands/
- Every new feature gets at least one test
