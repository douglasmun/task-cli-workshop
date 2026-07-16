# Instructor Guide — Claude Code CLI Power-User Workshop (60 min)

Presenter run sheet and facilitation notes. **Audience:** developers who have
*dabbled* with Claude Code. **Format:** live demo, no in-room lab. **Homework:**
the [course](https://douglasmun.github.io/claude-code-course.html) + the
[cheat sheet](https://douglasmun.github.io/claude-code-index.html).

**Slides:** <https://douglasmun.github.io/task-cli-workshop/docs/workshop-deck.html>
**Send attendees to:** [STUDENT-GUIDE.md](STUDENT-GUIDE.md).

This repo is the demo stage — a clone of the `task-cli` course starter (`main`)
with a seeded review scenario on the `workshop-demo` branch so the workflow and
review demos surface **real** findings live.

---

## Session objectives

Attendees leave able to name and reproduce the five power-user habits:
memory + plan mode, skills, subagents, deterministic workflows, and hooks — and
to see them all as steps in one loop: **Perceive → Reason → Act → Observe.**

## What you need on stage

| Item | Check |
|---|---|
| CLI **≥ 2.1.211** | `claude --version`. Older builds lack dynamic workflows — the centerpiece won't run. |
| The deck open full-screen | Projector-ready; `←/→` to navigate, number keys to jump. |
| Terminal font bumped up | Legible from the back row. |
| `bat` installed | `brew install bat`; set `export BAT_PAGING=never` so it prints inline. Or swap the `bat` lines below for `cat`. |
| The seeded scenario staged | See "Before you start" below. |
| A backup of the slow demo | Pre-run once; keep `docs/review-backup.md` open in a tab. |
| Network + a paid/Max session | The workflow fans out many agents. |

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

Keep a recorded GIF of that run as a backup. A finished capture already lives at
[`docs/review-backup.md`](docs/review-backup.md).

---

## Run sheet

Each segment lists the **objective** (what they should walk away knowing) and the
**talk track** (the sentence that makes it land).

### 0–5 min · Frame + through-line
- **Objective:** install the mental model before any demo.
- "You've all run prompts. Today is the 20% of habits that make the difference."
- Draw the loop: **Perceive → Reason → Act → Observe.** Every demo maps to it.
- Announce homework now — the course site + cheat sheet — so late arrivals hear it.

### 5–15 min · Memory + plan mode (highest ROI)
- **Objective:** durable memory + reason-before-act.
```bash
bat CLAUDE.md                    # show durable project memory at repo root
```
- Point out the `@docs/architecture.md` reference and the layered-architecture rule
  (you'll cash this in during the review demo).
- In a Claude session, make a multi-file change in **plan mode**:
```
# in claude:
Shift+Tab                        # cycle into plan mode
Add a `--due <date>` flag to the add command, wired through the store.
```
- **Talk track:** plan mode = "Reason before Act." This is the habit dabblers skip.

### 15–30 min · Skills + subagents (force multipliers)
- **Objective:** package the repeatable, delegate the rest.
```
/skills                          # list skills; note /add-feature takes $ARGUMENTS
/add-feature list tasks by priority
```
- Show a `context: fork` + `agent: Explore` read-only investigation:
```
Use the Explore agent to map how a command flows from CLI to the data file.
```
- **Talk track:** Explore is read-only, inherits the session model (capped at Opus),
  stays out of your main context. Subagents now run in the **background by
  default**, nest up to 5 deep, and can auto-commit/push/PR.

### 30–45 min · The Max-tier advanced block (centerpiece)
- **Objective:** deterministic, self-verifying multi-agent review.
- The seeded `priority.ts` has three planted problems — one per review dimension.
  Launch the workflow with a **prompt** (not a slash command):
```
Use a workflow to review the uncommitted changes.
```
- Approve the "Run a dynamic workflow?" dialog. Then, in another view:
```
/workflows                       # live progress tree — populates once it's running
```
- Expect it to surface: a **correctness** off-by-one, an **architecture** violation
  (direct FS write bypassing the store), and a **test-coverage** gap.
- **Talk track:** `/workflows` is the *viewer*; Claude invokes the workflow from your
  prompt (it reads `.claude/workflows/review-changes.js`). Explain `pipeline()`
  (no barrier) + adversarial verify (skeptics refute each finding). Contrast with
  the model-driven `/review-suite` skill.
- If the live run drags, fall back to [`docs/review-backup.md`](docs/review-backup.md).
- Then the reasoning knobs:
```
/effort high                     # low / medium / high / xhigh / max / auto
/model opusplan                  # Opus plans, Sonnet executes
```
- Name-drop, don't demo (time): `/code-review ultra` (cloud review of a branch/PR),
  agent teams (experimental flag), remote sessions / `/sandbox`.

### 45–55 min · Safety + governance (so it scales)
- **Objective:** deterministic guardrails, not vibes.
```bash
bat .claude/settings.json        # hooks wiring
bat .claude/hooks/format-file.sh # PostToolUse auto-format
bat .claude/hooks/block-dangerous-bash.sh   # PreToolUse guardrail
```
- Live: make any edit in a session → watch the format hook fire automatically.
- **Talk track:** expert use = deterministic guardrails, not vibes. Cover the
  permission model and auto mode (`claude --permission-mode auto`).

### 55–60 min · Wrap + homework
- **Objective:** one memorable takeaway + a clear next step.
- One takeaway: **trust but verify.**
- Homework: the course (Levels 3–4 map to today) + cheat sheet as daily reference.
- This repo is public — attendees can clone and replay every demo via
  [STUDENT-GUIDE.md](STUDENT-GUIDE.md).

---

## Facilitation notes

- **Time discipline.** The centerpiece is the only segment that can overrun (the
  live run is ~2 min). If you're behind, skip the `opusplan`/`effort` knobs and
  the name-drop list — they're the first things to cut.
- **The live run may pick its own dimensions.** The model orchestrating the
  workflow can choose more or different review dimensions than the script's fixed
  three. In practice it still catches all three planted issues, but if a run
  misses one, switch to `docs/review-backup.md` — a headless pre-run that used the
  exact three and confirmed all of them.
- **Don't apply the fix on stage.** After the review, Claude offers *"Want me to
  apply that fix?"* — decline (Esc). Applying it edits `priority.ts` and destroys
  the seeded diff; you'd have to re-seed before the next run.
- **Let a failure be a teaching moment.** If a hook blocks a command or a plan
  looks wrong, narrate it — that *is* the "trust but verify" point.

## Common pitfalls (and the one-line fix)

| Pitfall | Fix |
|---|---|
| Typing `/workflows review-changes` | There's no such command. Ask in plain language; `/workflows` is the viewer. |
| CLI is an old version | `npm uninstall -g @anthropic-ai/claude-code`, ensure `~/.local/bin` on `PATH`, new terminal, re-check `claude --version`. |
| Seed committed by accident | `git reset HEAD~1` to un-stage; re-run `git add -N`. |
| Review finds nothing | Seed not in the diff — re-seed and confirm `git diff --stat`. |

## Reset the stage between runs

```bash
rm -f src/commands/priority.ts
cp workshop-seed.priority.ts.tmpl src/commands/priority.ts
git add -N src/commands/priority.ts
```

---

## The seeded scenario (what the review should catch)

`src/commands/priority.ts` (new, on `workshop-demo`) deliberately contains:

| Dimension | Planted issue |
|-----------|---------------|
| Correctness | `priority - 1` off-by-one — `--priority 1` becomes 0; top tier unreachable |
| Architecture | Direct `fs.writeFileSync` to the store file, bypassing `saveTasks()` in `src/store/tasks.ts` (violates the layered rule in `CLAUDE.md`) |
| Test coverage | No `__tests__/priority.test.ts` for the new command |

---

## After the session

- Point attendees at [STUDENT-GUIDE.md](STUDENT-GUIDE.md) and the deck for self-paced replay.
- The repo is public — they clone it and reproduce every demo.
- Encourage the stretch goals (write a skill, add a review dimension, fix + test the planted bugs).
