# Claude Code Course — Starter Project

A CLI task manager built progressively across the
[Claude Code + Cowork Course](https://douglasmun.github.io/claude-code-course.html).

> **Workshop attendee?** Start with **[HOMEWORK.md](HOMEWORK.md)** — how to replay
> every demo at your own pace. Slides:
> **[the workshop deck](https://douglasmun.github.io/task-cli-workshop/docs/workshop-deck.html)**.
> Presenters: see **[WORKSHOP.md](WORKSHOP.md)** for the timed run sheet.

## Milestone Branches

Each branch is a reference checkpoint for a specific course module.
Check out the branch that matches where you are, compare it against
your own work, then switch back to `main` (or your own branch).

```bash
git checkout milestone-3-skills   # see the reference for Module 11
git checkout main                 # return to the complete version
```

| Branch | Module | Module Title | What's in this branch |
|--------|--------|--------------|----------------------|
| `milestone-1-scaffold` | 05 | Install & First Run | Working CLI: `add`, `list`, `done` commands; `src/`, `__tests__/`, `package.json` |
| `milestone-2-memory` | 10 | CLAUDE.md, Memory & Setup | `CLAUDE.md` with `@docs/architecture.md` ref; `.claudeignore`; `docs/architecture.md` |
| `milestone-3-skills` | 11 | Custom Skills & `$ARGUMENTS` | `/add-feature` skill with `$ARGUMENTS`; `/pr-review` static skill; `.claude/skills/` directory |
| `milestone-4-hooks` | 15 | Hooks & Safety Defaults | `format-file.sh` (PostToolUse); `block-dangerous-bash.sh` (PreToolUse); `.claude/settings.json` wiring |
| `milestone-5-agents` | 17 | Custom Subagents & Agent Teams | `test-reviewer` agent (`memory: user`); `security-scanner` agent (`context: fork`); `review-suite` orchestration skill |
| `milestone-6-plugin` | 21 | Build & Publish Your Plugin | Full `plugin/` package: all skills + hooks + agent bundled; `plugin/.claude-plugin/plugin.json` |
| `main` | — | Complete submission | All of the above + CI workflow + Cowork files + community docs |

> **Why six milestones?** The branches let you check your work against a
> known-good reference at each stage without spoiling later modules.
> Each branch builds on the previous — `milestone-3-skills` includes
> everything from `milestone-2-memory`, and so on.

## Quick Start

```bash
git clone https://github.com/douglasmun/claude-code-course-starter.git
cd claude-code-course-starter
npm install
npm start -- add "My first task"
npm start -- add "Fix production bug" --priority high
npm start -- list
npm start -- done 1
```

> **Bun users:** Replace `npm install` with `bun install`, `npm start --` with `bun run src/index.ts`, and `npm test` with `bun test`. The project also ships a `bun.lock` file.

## Tooling Standard

| Context | Recommended | Fallback |
|---|---|---|
| Install Claude Code | `curl -fsSL https://claude.ai/install.sh \| sh` | `brew install claude` (Mac) |
| Project commands | `npm test`, `npm run build`, `npm run format` | `bun test`, `bun run build` |
| Run CLI | `npm start -- <command>` | `bun run src/index.ts <command>` |
| CI headless | `npx @anthropic-ai/claude-code -p "..."` | Docker with Node 20 image |

> `npm install -g @anthropic-ai/claude-code` is deprecated. Use the native binary above.

## Using with Claude Code

```bash
claude                    # start a session
# Claude reads CLAUDE.md automatically
# Try: "Add a priority field to tasks"
```

## Course Completion Artifacts

This `main` branch includes a complete course submission:

- Project memory: `CLAUDE.md`, `.claudeignore`, and `docs/architecture.md`
- Custom skills: `.claude/skills/add-feature`, `pr-review`, `deploy-check`, `generate-adr`, and `review-suite` (orchestration)
- Custom agents: `.claude/agents/test-reviewer.md` (`memory: user`) and `security-scanner.md` (`context: fork`); `review-suite` skill dispatches both in parallel
- Hooks: `.claude/settings.json` plus reusable hook scripts in `.claude/hooks/`
- MCP configuration: `.mcp.json`
- Plugin package: `plugin/`
- Cowork context and plugin package: `cowork/`
- CI/headless Claude workflow: `.github/workflows/claude-review.yml` — requires `ANTHROPIC_API_KEY` secret (see [`.github/workflows/README.md`](.github/workflows/README.md))
- Completion evidence: `docs/course/completion-matrix.md`

Reviewers: run `npm test && npm run build` to confirm the code works, then cross-reference each item in `docs/course/completion-matrix.md` with the file path listed.

## Companion Resources

- [Course Community (GitHub Discussions)](https://github.com/douglasmun/claude-code-course-starter/discussions) — ask questions, share your capstone, get unstuck
- [Workshop Deck](https://douglasmun.github.io/task-cli-workshop/docs/workshop-deck.html) — the 60-minute live-demo slides
- [Course](https://douglasmun.github.io/claude-code-course.html)
- [Cheat Sheet](https://douglasmun.github.io/claude-code-index.html)
- [Capstone Evidence Guide](docs/course/capstone-evidence-guide.md)

## Community

**GitHub Discussions:** [github.com/douglasmun/claude-code-course-starter/discussions](https://github.com/douglasmun/claude-code-course-starter/discussions)

| Category | Use it for |
|---|---|
| [Q&A](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/q-a) | Setup issues, concept questions, stuck on a module |
| [Show & Tell](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/show-and-tell) | Share your capstone, plugins you built, workflows you've automated |
| [Ideas](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/ideas) | Suggest course improvements, new labs, feature requests |

Peer learning accelerates completion. If you're stuck, someone else has been stuck in the same place.
