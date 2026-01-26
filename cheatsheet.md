# DSA Progress CLI

## Quick Start

```bash
just progress-init      # First time setup
just progress           # Show summary
just cheat              # Show this cheatsheet
```

## Track Your Work

```bash
just attempt 28 python  # Started working on it
just solve 28 python    # Completed it
just reset 28 python    # Undo / start over
```

## Find Exercises

```bash
just next python        # Next 10 unsolved
just next python 5      # Next 5 unsolved
just list               # All exercises
just topic "Trees"      # Filter by topic
just attempted python   # Show in-progress
just solved python      # Show completed
```

## Update Files

```bash
just sync               # Update exercises.md + progress.png
just exercises          # Update exercises.md only
just plot               # Update progress.png only
```

## Reference

**Languages:** `python` | `rust` | `typescript`

**Statuses:** `not_started` | `attempted` | `solved`
