---
name: deep-research
description: Research a topic thoroughly across the codebase
tools: [Read, Grep, Glob, Bash]
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly:
1. Find all relevant files using Glob and Grep.
2. Read and analyze the code in detail.
3. Check git history for recent changes to related files.
4. Summarize findings with specific file references.
5. Identify potential issues or improvements.
