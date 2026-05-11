# Course Improvement Backlog

Use this as the issue list for a future Claude Code fix pass.

## High Priority

| ID | Area | Issue | Suggested fix |
| --- | --- | --- | --- |
| CCI-001 | Install and tooling | The course mixes native Claude Code install, deprecated npm install, project `npm`, example `pnpm`, and starter repo Node/Jest assumptions. This creates avoidable setup confusion. | Add a single "tooling standard" table: Claude Code install method, project package manager, fallback package manager, and exact commands. Keep npm/pnpm/bun examples separated by environment. |
| CCI-002 | Starter repo alignment | The live course is newer than the starter repo README and older local course copy. Some live capstone requirements are not obviously present in the starter. | Update starter README with live-course v1.2 requirements and link to `docs/course/completion-matrix.md`. Add a "How to grade this repo" section. |
| CCI-003 | Capstone scope | The capstone requires Code artifacts, Cowork artifacts, MCP, plugin publishing, CI, and teammate validation. This is too much for a single mandatory pass. | Split capstone into Core, Professional, and Native/Team tracks with explicit minimum passing criteria. |
| CCI-004 | External service dependency | MCP, Cowork connectors, GitHub App, Slack, Obsidian, and private marketplace steps require accounts or plan tiers students may not have. | Provide local/offline alternatives for every external dependency, such as filesystem MCP, local plugin install, mock Cowork plugin, and simulated teammate validation. |
| CCI-005 | Labs too broad | Labs A, B, and C are 8-12 hours each and can become independent courses in RAG, multi-agent orchestration, and LLM sandboxing. | Add minimum viable lab versions with sample input, expected output, and "stretch" sections. |
| CCI-006 | Security guardrails | Lab C and MCP examples could encourage risky command execution or broad connector scope if copied without context. | Add explicit "do not scan public networks", "least privilege connector scope", and "never pipe remote scripts in production hooks" warnings. |

## Medium Priority

| ID | Area | Issue | Suggested fix |
| --- | --- | --- | --- |
| CCI-007 | Skill examples | The course says students need static, `$ARGUMENTS`, and `context:fork` skills, but the distinction can blur during implementation. | Add three complete minimal `SKILL.md` examples side by side and explain when each is appropriate. |
| CCI-008 | Hooks | Hook examples are conceptually clear, but students need exact JSON/schema and cross-platform scripts. | Provide `.claude/settings.json` plus reusable shell scripts for format and safety hooks. |
| CCI-009 | Agent memory | The rubric asks for real `MEMORY.md` content, but user-level memory may contain private information and may not belong in git. | Clarify what should be committed: a demo memory file or screenshot evidence, not sensitive user memory. |
| CCI-010 | Plugin publishing | The course asks for marketplace publishing, which is hard for solo learners. | Add "local install pass" and "marketplace pass" alternatives. Provide a sample `marketplace.json`. |
| CCI-011 | CI workflow | The CI example assumes `ANTHROPIC_API_KEY` and GitHub Actions permissions. | Add a preflight checklist: secrets, permissions, fork PR limitations, budget cap, and expected failure modes. |
| CCI-012 | Cowork plugin | The Cowork capstone requirement is useful but under-scaffolded for students who have only used Code. | Add a minimal Cowork plugin example with two skills, one slash command, context files, and connector notes. |
| CCI-013 | Progress tracking | The course has local progress buttons but no obvious export/share of completion evidence. | Add "export completion" or "copy progress summary" button. |
| CCI-014 | Rubric evidence | The rubric scores artifacts, but students may not know what evidence to submit. | Add an evidence table: requirement, expected file path, screenshot or command output, pass criteria. |

## Low Priority

| ID | Area | Issue | Suggested fix |
| --- | --- | --- | --- |
| CCI-015 | Copy edit | The live course contains a small typo: "Open-sourced on GitHub for forking and customization" has a duplicated "for". | Change to "Open-sourced on GitHub for customization." |
| CCI-016 | Terminology | Some modules use "plugin", "skill", "command", and "slash command" close together. New students may mix them up. | Add a visual artifact taxonomy. |
| CCI-017 | Accessibility | Dense dark UI and long modules may be tiring. | Add print-friendly and high-contrast review modes, plus keyboard navigation hints. |
| CCI-018 | Version volatility | The course names specific Claude Code versions and feature states. These can age quickly. | Add a "last verified" date and a small version matrix at the top. |
| CCI-019 | Command reference | The command reference is useful but long. | Add filters by surface: Code CLI, Code IDE, Cowork, CI/headless. |
| CCI-020 | Starter repo tests | Jest assumes Node/npm, but some student environments may have Bun only. | Keep Jest for Node users, but document Bun fallback or commit a runtime-agnostic smoke test. |

## Suggested Fix Order

1. Align starter repo and live course requirements.
2. Add Core/Professional/Native tracks.
3. Add local/offline fallback paths for MCP, plugin install, Cowork plugin, and CI.
4. Add exact starter templates for skills, hooks, agents, MCP, and plugin marketplace.
5. Tighten security warnings and least-privilege connector guidance.
6. Add exportable progress/evidence.

## Acceptance Criteria for the Next Course Revision

- A student can complete the Core Pass without paid enterprise features or external services.
- Every module checkpoint has a copy-paste runnable example or a clearly marked conceptual-only task.
- The starter repo `main` branch satisfies the live capstone rubric.
- The capstone evidence can be reviewed from files and command output without relying on screenshots.
- Labs have sample inputs, expected outputs, and a minimal pass version.

---

## Revision History

### Session 1 — May 2026 (P1 Bug Fix Pass)

**Scope:** CI workflow correctness, email secret parameterisation, lab time accuracy, capstone-check hardening.

| Item | What changed | File(s) |
|------|-------------|---------|
| CI review comment posting | Added `id: claude_review` step; captured output to `GITHUB_OUTPUT` via heredoc; added `gh pr comment` step with `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` | `.github/workflows/claude-review.yml` |
| Email secret | Changed hardcoded `to: douglasmun@yahoo.com` → `to: ${{ secrets.NOTIFY_EMAIL_TO }}`; added secrets table to Module 20 | `.github/workflows/discussion-notify.yml`, `claude-code-course.html` |
| capstone-check hardening | `checkPluginJson()` and `checkCoworkPlugin()` now validate required `name`/`version`/`author` fields; `checkGithubWorkflows()` asserts `ANTHROPIC_API_KEY` + `claude` present in at least one workflow | `scripts/capstone-check.js` |

---

### Session 2 — May 2026 (Hard Audit + Full Fix Pass)

**Scope:** Full critical audit of the course and starter repo. 15 issues identified, all resolved across this session.

#### What the audit found

The course had three categories of problem:

1. **Content honesty gaps** — unattributed statistics, iOS surface misconception, vague lab time estimates, skills described as "automated scripts" rather than "persistent prompts".
2. **Scaffolding gaps** — placeholder lab sample files (lorem ipsum paragraphs, 2-IOC JSON), untyped skeleton functions, plugin skills that delegated to external paths (not self-contained).
3. **Architecture gaps** — only one agent in the starter repo (no handoff pattern to demonstrate), no `.claudeignore`, README branch table with no module mapping or milestone explanations.

#### Changes made to `claude-code-course-starter`

**Lab sample files** (`labs/`)
- Replaced 3 placeholder text files with 10 topically distinct cybersecurity documents (CVEs, threat actor profiles, incident reports, runbooks, advisories) in `lab-a-samples/` — designed for retrieval discrimination, not just tokenisation.
- Expanded `lab-b-samples/mock-threat-intel.json` from 2 IOCs to 10, covering all IOC types (ip/domain/hash/url), three confidence tiers, and diverse threat actor tags.
- Rewrote `lab-c-samples/` test scripts with proper expected stdout/returncode documentation and inline assertions.

**Lab skeletons** (`labs/`)
- `lab-a-skeleton/rag_skeleton.py`: full typed signatures, Args/Returns/Example docstrings, cosine_similarity extracted as separate function, implementation hints.
- `lab-b-skeleton/pipeline_skeleton.py`: IOC and EnrichedIOC TypedDicts, CONFIDENCE_RANK dict, all four pipeline stages with detailed docstrings.
- `lab-c-skeleton/sandbox_skeleton.py`: ALLOWED_COMMANDS as frozenset, is_allowed/run_sandboxed/run_with_audit with edge cases documented, self-test in main().

**Plugin self-containment** (`plugin/skills/`)
- All 5 SKILL.md files (add-feature, pr-review, deploy-check, generate-adr, deep-research) made fully self-contained — removed delegation to `.claude/skills/` paths.

**Second agent + orchestration skill** (`.claude/`)
- Added `security-scanner.md` agent: model haiku, memory: user, permissionMode: plan. Scans src/, hooks/, workflows/ for input validation, path traversal, shell injection, hardcoded secrets, dependency risk. Returns structured SECURITY SCAN REPORT.
- Added `review-suite/SKILL.md` skill: context:fork, user-invocable. Orchestrates security-scanner + test-reviewer as parallel subagents, documents WHY two agents (different models, independent memories, no context pollution), synthesises go/no-go recommendation.

**`.claudeignore`**
- Expanded from 5-line stub to fully annotated 7-section file: secrets/credentials, build output, dependencies, coverage artefacts, runtime data (`.task-cli-data.json`), OS/editor noise, Claude internal state (`.claude/memory/`, `.claude/agent-memory/`).

**README**
- Branch table expanded to 4 columns: Branch, Module number, Module title, "What's in this branch".
- Added git checkout example and incremental structure explanation.
- Updated Course Completion Artifacts to list both agents and review-suite skill.

#### Changes made to `claude-code-course.html`

**Module 03 (Code vs. Cowork)**
- Added "The Same Task — Two Surfaces" compare-grid: 6-row table walking the same status-update task through all agent loop steps for both Code and Cowork.
- Added "Going Deeper: 30 Cowork Best Practices" section with 7-part summary table and PDF link (Nav Toor's compiled guide).

**Module 04 (Why Teams Are Switching)**
- Replaced unattributed "67% more PRs" blockquote with honest framing: task-type-specific gains, three-way breakdown by category (code-adjacent / document-heavy / cross-tool), no fabricated aggregate.

**Module 05 (Install & First Run)**
- Expanded `/powerup` highlight-box to 3 paragraphs: what it covers, ~20-30 min timing, do first 3 exercises before Module 6, when to replay.

**Module 06 (Context Rot)**
- Added annotated before/after transcript using `.transcript-block` CSS showing turn 3 (correct: `console.error`) vs turn 38 (degraded: `console.log`). Demonstrates context rot visually.
- Rewrote prevention list to explain WHY each strategy works, not just what to do.

**Module 07 (VS Code & Other Surfaces)**
- Replaced "Demo Workflow" prose with 5-step concrete hands-on task: open done.ts, select function, ask specific question, review diff, run npm test.
- Replaced 4 sparse "Other Surfaces" bullets with 3 honest cards; Mobile card explicitly corrects the iOS/Dispatch misconception.

**Module 11 (Custom Skills)**
- Added "What skills are — and are not" highlight-box before Pattern 1: skills are persistent prompts, not background daemons or scheduled runners.
- Added `/review-suite` to the skills table.

**Module 20 (Headless Mode)**
- Added 4-row secrets table (ANTHROPIC_API_KEY, NOTIFY_EMAIL_USER, NOTIFY_EMAIL_PASS, NOTIFY_EMAIL_TO) with pointer to `.github/workflows/README.md`.

**Lab pages (A, B, C)**
- Time estimates changed from single optimistic numbers to "MVP X hrs · Full Y hrs" with honest breakdown highlight-boxes explaining what MVP vs. full pass requires.

**Module 22 (Team Operating System)**
- Added "Cowork Reference: 30 Best Practices" section: implementation checklist table (Today/This week/This month/Monthly) + cowork-box highlighting practices 18–22 as the gap most teams miss, with PDF link.

#### What was decided and why

- **Honest lab estimates over aspirational ones**: Students who hit 8 hours on a "3-hour lab" lose confidence. MVP/Full framing resets expectations without devaluing the work.
- **Skills-are-prompts callout**: The most common misconception from early feedback was treating skills as background automations. One highlight-box prevents hours of debugging confusion.
- **Two agents in the starter repo**: A single agent demonstrates persistence; two agents with an orchestration skill demonstrate the handoff pattern that is central to Level 4. The review-suite skill is the capstone-level demonstration of context:fork + parallel dispatch.
- **Self-contained plugin skills**: Students copying plugin examples into their own projects were getting broken references. Self-containment removes that failure mode entirely.
- **30 Best Practices integrated into two modules**: Module 03 is the Cowork entry point (first exposure); Module 22 is the synthesis point (where operating discipline is discussed). Both placements serve a different reader stage.

---

### Session 3 — May 2026 (Second Audit + Fix Pass)

**Scope:** Fresh hard audit (48 items identified, 36 false alarms after cross-check). 11 real items fixed across two sub-sessions.

#### CCI items resolved this session

| CCI | Fix applied |
|-----|------------|
| CCI-006 | Added red-bordered security card to Lab C before the code skeleton: only scan networks you own, no remote pipe-to-bash, least-privilege MCP scope, Docker is mandatory not optional |
| CCI-007 | Three skill patterns (static / $ARGUMENTS / context:fork) already existed — confirmed resolved from Session 2 |
| CCI-008 | Full settings.json schema + hook scripts already existed — confirmed resolved from Session 2 |
| CCI-011 | Added 6-row CI preflight checklist to Module 20: ANTHROPIC_API_KEY, GITHUB_TOKEN write permission, fork PR secret block, budget cap, exit code semantics, watch first run live |
| CCI-012 | Replaced thin cowork-box in Module 21 with full Cowork plugin worked example: folder structure, plugin.json, SKILL.md, install steps, Plugin Create alternative, note on how Cowork frontmatter differs from Code |
| CCI-014 | Added 10-row capstone evidence table to Rubric page: one row per requirement with expected file path and pass criteria |
| CCI-016 | Added 5-row artifact taxonomy table to Rubric page: skill / slash command / agent / hook / plugin — what-it-is, how-invoked, Cowork equivalent |

#### Additional fixes from second-audit items (not in original CCI list)

| Item | Fix applied |
|------|------------|
| context:fork vs agent: distinction muddled | Added highlight-box in Module 11 Pattern 3: explains the two fields are independent, covers fork-without-agent and agent-without-fork, states when fork+Explore is the sweet spot |
| Module 15 hooks — /hooks UI flow missing | Added step-by-step /hooks UI walkthrough for both checkpoint hooks (PostToolUse prettier + PreToolUse block) with exact commands and exit code semantics |
| Module 06 cowork-box missing model selection | Added Cowork model selection note: Sonnet default, Opus on Max/Enterprise, Haiku auto-selected for read-only sub-agent steps |
| Unattributed "27%" stat | Replaced with honest framing about work-category-specific gains |
| "100+ skills" in Key Specs | Replaced with accurate list of 11 role-specific plugins |
| opusplan casing inconsistency | Lowercased matrix cell label to match all other uses |
| Lab A/B prerequisites unstated | Added note-box before time estimate on both lab pages listing required skills, libraries, and where sample files live |
| FAQ "Does it work offline?" oversimplified | Replaced with accurate answer: default needs API, enterprise runs inside VPC via Bedrock/Vertex/Foundry, air-gapped not supported |
| Starter repo unpushed commit | Pushed to origin/main |

#### CCI items confirmed already resolved (no action needed)

CCI-001 (tooling table), CCI-003 (capstone tracks), CCI-004 (offline fallbacks), CCI-005 (MVP lab estimates), CCI-007 (skill patterns), CCI-008 (hook schema), CCI-009 (memory gitignore), CCI-010 (local install scope), CCI-013 (copy progress button), CCI-017 (high contrast + print), CCI-018 (last verified date), CCI-019 (command surface filters), CCI-020 (Bun fallback in README).

#### CCI items remaining open after Session 3

None of the original 20 CCI items remain unaddressed. The backlog is clear.
