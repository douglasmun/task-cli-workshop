# Architecture

## Data Flow

```
CLI Input → Commander.js → Command Handler → Store Layer → JSON File
```

## Modules
- `src/index.ts` — CLI entry point, command registration
- `src/commands/` — one file per command, no direct file I/O
- `src/store/tasks.ts` — all file read/write operations
- `src/types.ts` — shared TypeScript interfaces

## Design Decisions
- JSON file storage (not SQLite) for simplicity
- Store in user home directory (~/.task-cli-data.json)
- IDs are auto-incrementing integers, not UUIDs
