# Claude Code Course — Starter Project

A CLI task manager built progressively across the
[Claude Code + Cowork Course](https://douglasmun.github.io/claude-code-course.html).

## Branches

Each branch represents a course milestone. Checkout the branch
matching your current module:

| Branch | Course Module | What's Added |
|--------|--------------|--------------|
| `milestone-1-scaffold` | Module 05 | Basic CLI: add, list, done |
| `milestone-2-memory` | Module 10 | CLAUDE.md + .claudeignore |
| `milestone-3-skills` | Module 11 | /add-feature skill with $ARGUMENTS |
| `milestone-4-hooks` | Module 15 | Auto-format + safety hooks |
| `milestone-5-agents` | Module 17 | test-reviewer agent with memory |
| `milestone-6-plugin` | Module 21 | Full plugin package |
| `main` | Complete | Everything + CI + Cowork files |

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
- Custom skills: `.claude/skills/add-feature`, `pr-review`, `deploy-check`, and `generate-adr`
- Custom agent: `.claude/agents/test-reviewer.md`
- Hooks: `.claude/settings.json` plus reusable hook scripts in `.claude/hooks/`
- MCP configuration: `.mcp.json`
- Plugin package: `plugin/`
- Cowork context and plugin package: `cowork/`
- CI/headless Claude workflow: `.github/workflows/claude-review.yml`
- Completion evidence: `docs/course/completion-matrix.md`

Reviewers: run `npm test && npm run build` to confirm the code works, then cross-reference each item in `docs/course/completion-matrix.md` with the file path listed.

## Companion Resources

- [Course Community (GitHub Discussions)](https://github.com/douglasmun/claude-code-course-starter/discussions) — ask questions, share your capstone, get unstuck
- [Course](https://douglasmun.github.io/claude-code-course.html)
- [Cheat Sheet](https://douglasmun.github.io/claude-code-cheatsheet-v1.0.html)
- [Capstone Evidence Guide](docs/course/capstone-evidence-guide.md)

## Community

**GitHub Discussions:** [github.com/douglasmun/claude-code-course-starter/discussions](https://github.com/douglasmun/claude-code-course-starter/discussions)

| Category | Use it for |
|---|---|
| [Q&A](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/q-a) | Setup issues, concept questions, stuck on a module |
| [Show & Tell](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/show-and-tell) | Share your capstone, plugins you built, workflows you've automated |
| [Ideas](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/ideas) | Suggest course improvements, new labs, feature requests |

Peer learning accelerates completion. If you're stuck, someone else has been stuck in the same place.
