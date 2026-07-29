# Memory Index

This file serves as an index to the persistent memory files stored in the memory directory. Each line represents a memory file containing a specific fact or piece of information.

## Memory Format

Each memory file follows this format:
```markdown
---
name: <short-kebab-case-slug>
description: <one-line summary — used to decide relevance during recall>
metadata:
  type: user | feedback | project | reference
---

<the fact; for feedback/project, follow with **Why:** and **How to apply:** lines. Link related memories with [[their-name]].
```

## Current Memories

*No memories recorded yet*