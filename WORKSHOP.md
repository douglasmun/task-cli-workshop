# Claude Code CLI — Power-User Workshop (60 min)

Presenter run sheet. Audience: developers who have *dabbled* with Claude Code.
Format: live demo, no in-room lab. Homework:
<https://douglasmun.github.io/claude-code-course.html> + the cheat sheet.

This repo is the demo stage. It is a clone of the `task-cli` course starter
(`main`) with a seeded review scenario on the `workshop-demo` branch so the
`/workflows` and review demos surface **real** findings live.

---

## Before you start (do this once, off-stage)

```bash
git checkout workshop-demo      # the seeded branch
npm install                     # so tests/build run if asked

# Seed the review scenario as an UNCOMMITTED change (what the review reads):
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts   # intent-to-add: makes it visible to `git diff`
git diff --stat                        # confirm priority.ts shows in the diff
```

> Do **not** `git commit` `priority.ts` — the review demo reads the *uncommitted*
> diff. If you accidentally commit it, run `git reset HEAD~1` to un-stage.

**Pre-run the slow demo once** so you can fall back to a finished result if the
live run drags or the network hiccups:

```
claude
# then, as a prompt (NOT a slash command):
Use a workflow to review the uncommitted changes.
# approve the "Run a dynamic workflow?" dialog, let it finish, keep the terminal
```

> `/workflows` is a **progress viewer**, not a launcher — you can't type
> `/workflows review-changes`. You ask Claude in plain language and it finds
> `.claude/workflows/review-changes.js`, then shows an approval dialog. Open
> `/workflows` *after* it starts to watch the live tree.

Keep a recorded GIF of that run as a backup (see `docs/` if you captured one).
A finished capture already lives at `docs/review-backup.md`.

---

## Run sheet

### 0–5 min · Frame + through-line
- "You've all run prompts. Today is the 20% of habits that make the difference."
- Draw the loop: **Perceive → Reason → Act → Observe.** Every demo maps to it.
- Announce homework now: the course site + cheat sheet.

### 5–15 min · Memory + plan mode (highest ROI)
```bash
bat CLAUDE.md                    # show durable project memory at repo root
```
- Point out the `@docs/architecture.md` reference and the layered-architecture rule.
- In a Claude session, make a multi-file change in **plan mode**:
```
# in claude:
Shift+Tab                        # cycle into plan mode
Add a `--due <date>` flag to the add command, wired through the store.
```
- Talk track: plan mode = "Reason before Act." This is the habit dabblers skip.

### 15–30 min · Skills + subagents (force multipliers)
```
/skills                          # list skills; note /add-feature takes $ARGUMENTS
/add-feature list tasks by priority
```
- Show a `context: fork` + `agent: Explore` read-only investigation:
```
Use the Explore agent to map how a command flows from CLI to the data file.
```
- Talk track: Explore is read-only, inherits the session model (capped at Opus),
  stays out of your main context. Subagents now run in the **background by
  default**, nest up to 5 deep, and can auto-commit/push/PR.

### 30–45 min · The Max-tier advanced block (centerpiece)
The seeded `priority.ts` has three planted problems — one per review dimension.
Launch the workflow with a **prompt** (not a slash command):
```
Use a workflow to review the uncommitted changes.
```
Approve the "Run a dynamic workflow?" dialog. Then, in another view:
```
/workflows                       # live progress tree — populates once it's running
```
- Expect it to surface: a **correctness** off-by-one, an **architecture**
  violation (direct FS write bypassing the store), and a **test-coverage** gap.
- Talk track: `/workflows` is the *viewer*; Claude invokes the workflow from your
  prompt (it reads `.claude/workflows/review-changes.js`). Explain `pipeline()`
  (no barrier) + adversarial verify (skeptics refute each finding). Contrast with
  the model-driven `/review-suite` skill.
- If the live run drags, fall back to `docs/review-backup.md` (a finished capture).
- Then the reasoning knobs:
```
/effort high                     # low / medium / high / xhigh / max / auto
/model opusplan                  # Opus plans, Sonnet executes
```
- Name-drop, don't demo (time): `/code-review ultra` (cloud review of a branch/PR),
  agent teams (experimental flag), remote sessions / `/sandbox`.

### 45–55 min · Safety + governance (so it scales)
```bash
bat .claude/settings.json        # hooks wiring
bat .claude/hooks/format-file.sh # PostToolUse auto-format
bat .claude/hooks/block-dangerous-bash.sh   # PreToolUse guardrail
```
- Live: make any edit in a session → watch the format hook fire automatically.
- Talk track: expert use = deterministic guardrails, not vibes. Cover the
  permission model and auto mode (`claude --permission-mode auto`).

### 55–60 min · Wrap + homework
- One takeaway: **trust but verify.**
- Homework: the course (Levels 3–4 map to today) + cheat sheet as daily reference.
- This repo is public — attendees can clone and replay every demo.

---

## The seeded scenario (what the review should catch)

`src/commands/priority.ts` (new, on `workshop-demo`) deliberately contains:

| Dimension | Planted issue |
|-----------|---------------|
| Correctness | `priority - 1` off-by-one — `--priority 1` becomes 0; top tier unreachable |
| Architecture | Direct `fs.writeFileSync` to the store file, bypassing `saveTasks()` in `src/store/tasks.ts` (violates the layered rule in `CLAUDE.md`) |
| Test coverage | No `__tests__/priority.test.ts` for the new command |

To reset the stage between runs (regenerate the uncommitted diff):
```bash
rm -f src/commands/priority.ts
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts
```
