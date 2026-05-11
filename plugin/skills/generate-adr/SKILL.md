---
name: generate-adr
description: Draft an architecture decision record for task-cli changes
tools: [Read, Write, Glob]
user-invocable: true
---
Create an ADR for the decision described by $ARGUMENTS.

Process:
1. Read docs/architecture.md and CLAUDE.md.
2. If the `task-cli-knowledge` MCP server is connected, use it to retrieve related docs and cowork context before drafting.
3. Create a new file under docs/adr/ named `NNNN-short-title.md`.
4. Use this structure: Status, Context, Decision, Consequences, Alternatives Considered.
5. Reference relevant files with @file syntax where helpful.
6. Keep the ADR factual and concise.

Do not change implementation code while generating the ADR.
