# Student Guide — Claude Code CLI Power-User Workshop

You watched the demo. This guide turns it into skills you keep. Everything shown
in the session lives in this repo, so you can replay every step at your own pace.

**Slides:** <https://douglasmun.github.io/task-cli-workshop/docs/workshop-deck.html>
**Presenting or running this yourself?** See [INSTRUCTOR-GUIDE.md](INSTRUCTOR-GUIDE.md).

---

## What you'll be able to do after this

By the end of this guide you should be able to:

1. Give Claude durable project memory with `CLAUDE.md`, and work in **plan mode** so it reasons before it edits.
2. Package a repeated prompt as a **skill** and delegate scoped work to a **subagent**.
3. Run a **deterministic multi-agent workflow** that reviews a diff and adversarially verifies its own findings.
4. Wire **hooks** so good behavior (formatting, guardrails) happens automatically.
5. Explain the through-line: **Perceive → Reason → Act → Observe** — and point to where each demo sits in that loop.

---

## Prerequisites

| You need | Notes |
|---|---|
| A paid Claude plan | The advanced block (`/workflows`, `/code-review ultra`, `opusplan`, high `/effort`) shines on **Max**, but everything here runs on any paid tier. |
| Claude Code CLI **≥ 2.1.211** | Dynamic workflows need a recent build. Check with `claude --version`. If you're on an old npm-global install, see [Troubleshooting](#troubleshooting). |
| Node.js 20+ and git | `node --version`, `git --version`. |
| A terminal you're comfortable in | macOS/Linux shown; Windows works via WSL. |
| `bat` (optional) | Only if you replay the file-display demos verbatim. `brew install bat`; plain `cat` works too. |

---

## Setup (5 min)

```bash
git clone https://github.com/douglasmun/task-cli-workshop.git
cd task-cli-workshop
npm install
claude            # start a Claude Code session in the repo
```

Confirm the CLI version first — the workflow demo depends on it:

```bash
claude --version  # expect 2.1.211 or newer
```

---

## The main homework: the course

The demo was the trailer. The course is the full path.

**→ <https://douglasmun.github.io/claude-code-course.html>**

- **Levels 3–4** map directly to what you saw today (memory, skills, subagents, hooks, workflows). Start there if you already dabble.
- Keep the **cheat sheet** open as your daily reference: <https://douglasmun.github.io/claude-code-index.html>
- Rewatch the session at your own pace with the **slide deck**: <https://douglasmun.github.io/task-cli-workshop/docs/workshop-deck.html>

---

## Replay the demos yourself (in order)

Each maps to a segment from the live session. Do them in order — later demos
build on the setup from earlier ones. For each, the **What you should see** note
tells you whether it worked.

### 1. Memory + plan mode

```bash
cat CLAUDE.md                    # durable project memory — read the layered rule
```
Then, inside `claude`:
```
# press Shift+Tab to enter plan mode, then send:
Add a --due <date> flag to the add command, wired through the store.
```

**What you should see:** Claude proposes a numbered **plan** and edits nothing
until you approve it. That "reason before act" habit is the whole game.

> **Why it matters:** `CLAUDE.md` is read every session and survives context
> compaction, so you stop re-explaining your project. Plan mode makes the
> thinking reviewable before any file changes.

### 2. Skills + subagents

```
/skills                          # list skills; /add-feature takes $ARGUMENTS
/add-feature list tasks by priority
```
Then a read-only investigation in an isolated context:
```
Use the Explore agent to trace how a command reaches the data file.
```

**What you should see:** `/add-feature` runs a saved, reusable prompt. The
Explore agent runs in the background and reports back **without** cluttering your
main chat — and it only reads, never edits.

> **Why it matters:** a skill turns a good prompt into a command you can reuse; a
> subagent keeps a big job out of your main context.

### 3. The advanced block — the reason you came

Seed the planted review scenario, then let the multi-agent review find it:

```bash
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts     # makes it visible to `git diff`
```

Then, inside `claude`, launch it with a **prompt** — there is no
`/workflows review-changes` command; `/workflows` is only the progress **viewer**:

```
Use a workflow to review the uncommitted changes.
```

Approve the "Run a dynamic workflow?" dialog. Claude finds
`.claude/workflows/review-changes.js` and runs it. Watch progress with:

```
/workflows                       # live progress tree — populates once it's running
```

**What you should see:** three issues surfaced in `priority.ts` — an **off-by-one**
(correctness), an **architecture** violation (direct file write bypassing the
store), and a **missing test**. Compare it with the model-driven `/review-suite`
skill. A finished reference run is saved at [`docs/review-backup.md`](docs/review-backup.md).

Then try the reasoning knobs:
```
/effort high                     # low / medium / high / xhigh / max / auto
/model opusplan                  # Opus plans, Sonnet executes
```

> **Why it matters:** the workflow is a script (`.claude/workflows/*.js`), so it
> fans out the same agents in the same order every run — and each finding is
> checked by skeptic agents that try to refute it before it's confirmed.

### 4. Safety hooks

```bash
cat .claude/settings.json
cat .claude/hooks/format-file.sh          # PostToolUse: auto-format on every edit
cat .claude/hooks/block-dangerous-bash.sh # PreToolUse: guardrail
```
Then make any edit in a session.

**What you should see:** the format hook fires **automatically** after the edit —
no prompt, no reminder. That is the loop's *Observe* step, automated.

> **Why it matters:** expert use scales on deterministic guardrails, not on
> remembering to format or on trusting every command.

---

## Reset the review scenario between tries

```bash
rm -f src/commands/priority.ts
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts
```

Do **not** commit `src/commands/priority.ts` — the review reads the *uncommitted*
diff. If you accidentally commit it, run `git reset HEAD~1` to un-stage.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `Unknown command: /workflow` | It's plural — but you don't launch by command anyway. Ask Claude: *"Use a workflow to review the uncommitted changes."* `/workflows` is only the viewer. |
| `/workflows` shows "No dynamic workflows in this session" | That panel lists workflows **already running/run** this session — it's not a launcher. It populates after you ask Claude to run one. |
| `claude --version` shows an old version (e.g. 2.1.83) | You likely have a deprecated npm-global install shadowing the native one. Remove it: `npm uninstall -g @anthropic-ai/claude-code` (may need `sudo`), ensure `~/.local/bin` is on your `PATH`, open a new terminal, re-check. |
| Review finds nothing / no diff | The seed isn't in the diff. Re-seed (above) and confirm with `git diff --stat`. |
| The workflow warns about token usage | Expected — it fans out many subagents. On Max this is comfortable; stop any run with `/workflows` → `x`. |
| `bat: command not found` | The file-display demos use `bat`. Install it (`brew install bat`) or just use `cat` instead. |

---

## Stretch goals

- Write your own skill in `.claude/skills/` for a workflow you repeat.
- Add a review dimension to `.claude/workflows/review-changes.js` (append to the `DIMENSIONS` array) and re-run it.
- Fix the three planted bugs in `priority.ts` and add `__tests__/priority.test.ts` so the suite passes.

---

## Milestone branches (reference checkpoints)

This repo also carries the course's milestone branches — each is a known-good
reference for one module. See [`README.md`](README.md) for the full table.
