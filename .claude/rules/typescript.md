# TypeScript Conventions

- Use `readonly` for properties that shouldn't be modified
- Prefer `interface` over `type` for object shapes
- Use `unknown` instead of `any` — narrow with type guards
- Destructure function parameters when there are 3+ params
- Use template literals, not string concatenation
- Handle all Promise rejections — no unhandled promises
