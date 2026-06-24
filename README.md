# Interview Prep

This repo now has two main workspaces:

- [`dsa/`](./dsa/README.md): data structures and algorithms practice
- [`dist-sys/`](./dist-sys/README.md): distributed systems practice, including Fly.io / Maelstrom work

It also includes shared tooling and study/progress tracking at the repo root.

## Progress CLI

Track DSA exercises and system design studies using DuckDB.

```bash
just progress              # Show DSA summary
just progress study        # Show study summary
just progress --help       # See all commands
```

### Study Tracking

Track books, courses, papers, and associated materials:

```bash
just progress study                      # Show study summary

# Books
just progress study book-add "DDIA" --author "Kleppmann" --chapters 12
just progress study book-read 1 --chapter 1

# Courses
just progress study course-add "Database Systems" --source CMU --code "15-445"
just progress study lecture-add 1 "Introduction" --number 1

# Papers
just progress study paper-add "Dynamo" --authors "DeCandia et al." --year 2007
just progress study paper-read 1
```

## Workflow

```bash
just setup
just install-hooks
just fmt
just lint
just test all
```

## Layout

- `dsa/` — DSA language workspaces
- `dist-sys/` — distributed systems workspaces
- `scripts/` — shared progress tooling and utilities
- `tutorials/` — tutorial site content
- `notes/` — optional study notes

See the workspace READMEs for domain-specific details.
