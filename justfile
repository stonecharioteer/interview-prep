
# Use bash for all commands (fail on errors and undefined vars)
set shell := ["bash", "-euo", "pipefail", "-c"]

fmt:
  uv run --project dsa/python ruff format dsa/python/ scripts/
  pnpm --dir dsa/js exec prettier --write ../../README.md ../../AGENTS.md "src/**/*.ts" "test/**/*.ts"
  cd dsa/rust && cargo fmt

lint:
  uv run --project dsa/python ruff check dsa/python/test scripts/
  pnpm --dir dsa/js exec prettier --check ../../README.md ../../AGENTS.md "src/**/*.ts" "test/**/*.ts"
  cd dsa/rust && cargo fmt --check

typecheck:
  pnpm --dir dsa/js typecheck

install-hooks:
  git config core.hooksPath .githooks
  chmod +x .githooks/pre-commit .githooks/commit-msg

setup:
  uv sync --project dsa/python --group dev
  pnpm --dir dsa/js install
  cd dsa/rust && cargo fetch
  just install-hooks

setup-notebooks:
  uv sync --project dsa/python --group dev --group notebooks

# ============ Testing ============

# Run tests: just test <lang> [filter]
# Examples: just test python, just test rust arrays, just test js "binary search"
# DSA languages live under dsa/.
test LANG *FILTER:
  #!/usr/bin/env bash
  set -euo pipefail
  case "{{LANG}}" in
    python|py)
      if [ -z "{{FILTER}}" ]; then
        cd dsa/python && uv run python -m pytest test/
      else
        cd dsa/python && uv run python -m pytest test/ -k "{{FILTER}}"
      fi
      ;;
    js|typescript|ts)
      if [ -z "{{FILTER}}" ]; then
        pnpm --dir dsa/js test
      else
        pnpm --dir dsa/js exec vitest run -t "{{FILTER}}"
      fi
      ;;
    rust|rs)
      if [ -z "{{FILTER}}" ]; then
        cd dsa/rust && cargo test
      else
        cd dsa/rust && cargo test "{{FILTER}}"
      fi
      ;;
    all)
      just test python {{FILTER}}
      just test js {{FILTER}}
      just test rust {{FILTER}}
      ;;
    *)
      echo "Unknown language: {{LANG}}. Use python|py, js|ts, rust|rs, or all"
      exit 1
      ;;
  esac

# ============ Utility ============

# Run arbitrary commands via uv in the python project
uv-run *ARGS:
  uv run --project dsa/python {{ARGS}}

# ============ Progress Tracking ============

# Progress CLI - pass any args/subcommands directly
# Examples:
#   just progress                          # show DSA summary
#   just progress study                    # show study summary
#   just progress study book-add "Title"   # add a book
#   just progress mark 28 python solved    # mark exercise
#   just progress --help                   # see all commands
progress *ARGS:
  @uv run --project dsa/python python scripts/progress {{ARGS}}

# Open an exercise by ID in $EDITOR
open LANG NUMBER:
  @uv run --project dsa/python python scripts/progress open {{LANG}} {{NUMBER}}

# Open the next unsolved exercise in $EDITOR
open-next LANG:
  @uv run --project dsa/python python scripts/progress open {{LANG}} --next

# Show solved counts grouped by date
progress-solved-by-date:
  @duckdb progress.db -c "SELECT date, COUNT(*) AS solved FROM progress WHERE status = 'solved' AND date IS NOT NULL GROUP BY date ORDER BY date"

# ============ Deploy ============

# Publish tutorials/ to GitHub Pages via gh-pages branch
publish:
  git subtree push --prefix tutorials origin gh-pages

# ============ Help ============

# Show usage tips for the progress CLI
cheat:
  @glow cheatsheet.md
