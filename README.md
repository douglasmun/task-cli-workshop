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
npm start -- list
npm start -- done 1
```

## Using with Claude Code

```bash
claude                    # start a session
# Claude reads CLAUDE.md automatically
# Try: "Add a priority field to tasks"
```

## Companion Resources

- [Course](https://douglasmun.github.io/claude-code-course.html)
- [Cheat Sheet](https://douglasmun.github.io/claude-code-cheatsheet-v1.0.html)
