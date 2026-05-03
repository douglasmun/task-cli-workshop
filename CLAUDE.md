# Project: task-cli

A CLI task manager built as the course project for the Claude Code + Cowork course.

## Stack
- TypeScript 5.4, Node.js 20+
- Commander.js for CLI parsing
- Jest + ts-jest for testing, Prettier for formatting
- `jest.config.js` configures `ts-jest` preset and `__tests__/**/*.test.ts` pattern

## Commands
- `npm start -- <command>` — run the CLI (e.g. `npm start -- add "Buy milk"`)
- `npm test` — run all tests
- `npx jest __tests__/<file>.test.ts` — run a single test file
- `npm run build` — compile TypeScript to `dist/`
- `npm run format` — run Prettier across `src/`
- `npm run lint` — run ESLint across `src/`

## Conventions
- Strict TypeScript — no `any`, no type assertions without comments
- One file per command in `src/commands/`
- Storage abstraction in `src/store/` — never read/write files directly from commands
- Tests in `__tests__/` — mirror the `src/` structure; mock the store layer with `jest.mock`
- Use descriptive variable names, not abbreviations
- Validate external input at the CLI boundary (e.g. `done <id>` validates `parseInt` result is not `NaN`)

## Architecture
See @docs/architecture.md for system boundaries.

## Claude Code Skills & Agents
- `/add-feature <description>` — plans and implements a new feature end-to-end
- `/deep-research <topic>` — forks a subagent to explore the codebase
- `test-reviewer` agent — proactively reviews test coverage after feature work

## Don't
- Modify the store path without updating tests
- Add dependencies without checking `package.json` first
- Use `console.log` for errors — use `console.error`
- Skip tests for new features
- Add direct file I/O in `src/commands/` — all storage goes through `src/store/tasks.ts`
