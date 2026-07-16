# Workshop Homework — Claude Code CLI

You watched the demo. This is how you turn it into skills you actually keep.
Everything demoed today lives in this repo, so you can replay it at your own pace.

## Setup (5 min)

```bash
git clone https://github.com/douglasmun/task-cli-workshop.git
cd task-cli-workshop
npm install
claude            # start a Claude Code session in the repo
```

You need a paid Claude plan. The advanced pieces (`/workflows`,
`/code-review ultra`, `opusplan`, high `/effort`) shine on **Max**, but
everything here runs on any paid tier.

## The main homework: the course

The demo was the trailer. The course is the full path.

**→ <https://douglasmun.github.io/claude-code-course.html>**

- **Levels 3–4** map directly to what you saw today (memory, skills,
  subagents, hooks, `/workflows`). Start there if you already dabble.
- Keep the **cheat sheet** open as your daily reference:
  <https://douglasmun.github.io/claude-code-index.html>

## Replay the demos yourself (in order)

Each maps to a segment from the live session.

### 1. Memory + plan mode
```bash
cat CLAUDE.md                    # durable project memory — read the layered rule
# in claude: press Shift+Tab to enter plan mode, then:
#   "Add a --due <date> flag to the add command, wired through the store."
# Watch it propose a plan BEFORE editing. That habit is the whole game.
```

### 2. Skills + subagents
```
/skills                          # list skills; /add-feature takes $ARGUMENTS
/add-feature list tasks by priority
# then, read-only investigation in an isolated context:
#   "Use the Explore agent to trace how a command reaches the data file."
```

### 3. The advanced block — the reason you came
Seed the planted review scenario, then let the multi-agent review find it:
```bash
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts     # makes it visible to `git diff`
```
```
/workflows review-changes        # deterministic multi-agent review
/workflows                       # watch the live progress tree
```
It should surface **three** issues in `priority.ts` — an off-by-one, an
architecture violation (direct file write bypassing the store), and a missing
test. Compare with the model-driven `/review-suite` skill. Then try the
reasoning knobs:
```
/effort high
/model opusplan                  # Opus plans, Sonnet executes
```

### 4. Safety hooks
```bash
cat .claude/settings.json
cat .claude/hooks/format-file.sh          # PostToolUse: auto-format on every edit
cat .claude/hooks/block-dangerous-bash.sh # PreToolUse: guardrail
# Make any edit in a session and watch the format hook fire automatically.
```

## Reset the review scenario between tries

```bash
rm -f src/commands/priority.ts
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts
```

Do **not** commit `src/commands/priority.ts` — the review reads the
*uncommitted* diff.

## Stretch goals

- Write your own skill in `.claude/skills/` for a workflow you repeat.
- Add a review dimension to `.claude/workflows/review-changes.js`
  (append to the `DIMENSIONS` array) and re-run it.
- Fix the three planted bugs in `priority.ts` and add `__tests__/priority.test.ts`.

## Milestone branches (reference checkpoints)

This repo also carries the course's milestone branches — each is a known-good
reference for one module. See `README.md` for the full table.
