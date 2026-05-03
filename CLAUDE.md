# Project: task-cli

A CLI task manager built as the course project for the Claude Code + Cowork course.

## Stack
- TypeScript 5.4, Node.js 20+
- Commander.js for CLI parsing
- Jest for testing, Prettier for formatting

## Commands
- `npm start -- <command>` — run the CLI
- `npm test` — run all tests
- `npm run build` — compile TypeScript
- `npm run format` — run Prettier
- `npm run lint` — run ESLint

## Conventions
- Strict TypeScript — no `any`, no type assertions without comments
- One file per command in `src/commands/`
- Storage abstraction in `src/store/` — never read/write files directly from commands
- Tests in `__tests__/` — mirror the src/ structure
- Use descriptive variable names, not abbreviations

## Architecture
See @docs/architecture.md for system boundaries.

## Don't
- Modify the store path without updating tests
- Add dependencies without checking package.json first
- Use console.log for errors — use console.error
- Skip tests for new features
