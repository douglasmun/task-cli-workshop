---
type: project
status: active
date: 2026-05-11
tags: [course, capstone, evidence]
---

# Capstone Evidence Guide

Use this guide to verify your submission before sharing it with a reviewer. Each row maps a capstone requirement to the expected file path, a verification command, and the pass criterion.

## Evidence Table

| Requirement | Expected file path | Verification command | Pass criterion |
|---|---|---|---|
| CLAUDE.md | `CLAUDE.md` | `cat CLAUDE.md \| head -5` | File exists and contains `# Project:` heading with project name |
| Static skill | `.claude/skills/pr-review/SKILL.md` | `cat .claude/skills/pr-review/SKILL.md \| head -5` | File exists and has frontmatter with `name: pr-review` |
| `$ARGUMENTS` skill | `.claude/skills/deploy-check/SKILL.md` | `cat .claude/skills/deploy-check/SKILL.md \| head -5` | File exists and has frontmatter with `name: deploy-check`; body contains `$ARGUMENTS` |
| `context:fork` skill | `.claude/skills/deep-research/SKILL.md` | `cat .claude/skills/deep-research/SKILL.md \| head -5` | File exists and has frontmatter with `name: deep-research` |
| Custom agent | `.claude/agents/test-reviewer.md` | `cat .claude/agents/test-reviewer.md \| head -5` | File exists and contains agent role description |
| Two hooks | `.claude/hooks/format-file.sh`, `.claude/hooks/block-dangerous-bash.sh` | `ls .claude/hooks/` | Both files present and executable (`chmod +x` applied) |
| MCP connection | `.mcp.json` | `cat .mcp.json` | File exists and contains a valid `mcpServers` key |
| Plugin | `plugin/.claude-plugin/plugin.json` | `cat plugin/.claude-plugin/plugin.json` | File exists and contains `name`, `version`, and `author` fields |
| CI integration | `.github/workflows/claude-review.yml` | `cat .github/workflows/claude-review.yml \| head -10` | File exists and references `ANTHROPIC_API_KEY` |
| Cowork context files | `cowork/about-me.md` | `ls cowork/` | Directory contains `about-me.md`, `brand-voice.md`, `working-preferences.md` |
| Custom Cowork plugin | `cowork/plugin/` | `ls cowork/plugin/` | Directory exists and contains at least one skill or agent |

## How to Export Evidence

Run this command from the repo root to dump all relevant artifacts to a single file for review submission:

```bash
find .claude plugin cowork .github/workflows -type f | sort | xargs -I{} sh -c 'echo "=== {} ===" && cat {}' > capstone-evidence-export.txt
```

Share or attach `capstone-evidence-export.txt` with your submission. Reviewers can verify every artifact without checking out the repo.

## Share Your Capstone

Post your completed capstone in the [Show & Tell discussion](https://github.com/douglasmun/claude-code-course-starter/discussions/categories/show-and-tell). Include:
- Your repo link (or a private Gist with the key files)
- Which track you completed (Core / Professional / Native-Team)
- One thing you would do differently

Reading other students' capstones is one of the fastest ways to level up.
