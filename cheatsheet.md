# Progress CLI Cheatsheet

## Quick Start

```bash
just progress init          # First time setup
just progress               # Show DSA summary
just progress cheatsheet    # Show quick reference
```

## DSA Exercises

```bash
just progress mark 28 python solved      # Mark as solved
just progress mark 28 python attempted   # Mark as attempted
just progress mark 28 python not_started # Reset

just progress next python        # Next 10 unsolved
just progress next python -n 5   # Next 5 unsolved
just progress list               # All exercises
just progress list --topic Trees # Filter by topic
just progress list --lang python --status attempted  # Filter by status
```

## Study Tracking

```bash
just progress study              # Show study summary
just progress study recent       # Recent activity (7 days)
```

### Books

```bash
just progress study book-add "DDIA" --author "Kleppmann" --chapters 12
just progress study book-read 1 --chapters "1-3"
just progress study book-list
just progress study book-show 1
```

### Courses

```bash
just progress study course-add "Database Systems" --source CMU --code "15-445"
just progress study lecture-add 1 "Introduction" --number 1
just progress study watch 1 1                    # Mark lecture 1 of course 1 as watched
just progress study course-list
just progress study course-show 1
```

### Homework & Projects

```bash
just progress study homework-add 1 "SQL Homework"   # Add to lecture 1
just progress study homework-done 1
just progress study project-add 1 "Buffer Pool"     # Add to course 1
just progress study project-done 1
```

### Papers

```bash
just progress study paper-add "Dynamo" --authors "DeCandia et al." --year 2007
just progress study paper-read 1
just progress study paper-list
```

### Associations

```bash
just progress study course-book 1 1              # Book 1 required for course 1
just progress study course-paper 1 1             # Paper 1 required for course 1
just progress study lecture-chapters 1 1 "1-3"   # Chapters 1-3 of book 1 for lecture 1
just progress study lecture-paper 1 1            # Paper 1 required for lecture 1
```

## Output Files

```bash
just progress sync       # Update exercises.md + progress.png
just progress exercises  # Update exercises.md only
just progress plot       # Update progress.png only
```

## Reference

**Languages:** `python` | `rust` | `typescript`

**Statuses:** `not_started` | `attempted` | `solved`

**Study Statuses:** `not_started` | `in_progress` | `completed`
