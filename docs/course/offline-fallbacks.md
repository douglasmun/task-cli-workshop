---
type: project
status: active
date: 2026-05-11
tags: [course, offline, fallbacks]
---

# Offline Fallback Paths

Use this guide when an external service, account, or plan tier is unavailable. Every capstone item has a local alternative.

## 1. MCP without Obsidian

Use the filesystem MCP server instead of an Obsidian vault connector. Add this to `.mcp.json` in the repo root:

```json
{"mcpServers":{"fs":{"command":"npx","args":["-y","@anthropic-ai/mcp-server-filesystem","."]}}}
```

This configuration is already present in this repo. It exposes all project files under the current directory to Claude Code via MCP without requiring an Obsidian install or vault.

## 2. Plugin install without marketplace

Run the following from the repo root inside a Claude Code session to install locally:

```bash
claude plugin install ./plugin
```

No marketplace account or plan tier is required. The plugin installs the same skills, hooks, agent, and MCP config that a marketplace publish would deliver. For the Core Pass, local install is sufficient.

## 3. CI without GitHub Actions

Simulate a headless CI review locally by running Claude Code in non-interactive mode:

```bash
claude -p "Review the latest diff for missing tests." > review-output.txt
```

Inspect `review-output.txt` to confirm Claude Code ran and returned findings. This is equivalent to the `.github/workflows/claude-review.yml` step for evidence purposes.

## 4. Cowork plugin without a Cowork account

Load `cowork/plugin/` as a local plugin. The skills and agents inside that directory operate fully within Claude Code and do not require a live Cowork connection:

```bash
claude plugin install ./cowork/plugin
```

Context files at `cowork/about-me.md`, `cowork/brand-voice.md`, and `cowork/working-preferences.md` are read directly by Claude Code from the filesystem.

## 5. Teammate validation without a real teammate

Simulate teammate validation by cloning the repo into a temporary directory and confirming the project memory and tooling load correctly:

```bash
git clone . /tmp/task-cli-validate
cd /tmp/task-cli-validate
npm install
claude --print "List all skills, hooks, and agents you can see in this project."
```

Confirm the output lists `CLAUDE.md`, the skills in `.claude/skills/`, the hooks in `.claude/hooks/`, and the agent at `.claude/agents/test-reviewer.md`. This verifies the project is self-contained and reproducible in a fresh checkout without teammate coordination.

## Getting Help

If a fallback path doesn't work for your environment, post in [Q&A Discussions](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/q-a) with:
- Your OS and shell
- The exact command you ran
- The error output

Include which fallback you were attempting (MCP / plugin / CI / Cowork / teammate).
