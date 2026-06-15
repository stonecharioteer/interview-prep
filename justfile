
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
  chmod +x .githooks/pre-commit .githooks/commit-msg .githooks/post-commit

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
  #!/usr/bin/env bash
  set -euo pipefail

  args=( {{ARGS}} )

  if [[ "${args[0]:-}" != "sync" ]]; then
    uv run --project dsa/python python scripts/progress {{ARGS}}
    exit 0
  fi

  uv run --project dsa/python python scripts/progress {{ARGS}}

  if git diff --quiet -- exercises.md progress.png && git diff --cached --quiet -- exercises.md progress.png; then
    exit 0
  fi

  mapfile -t staged_files < <(git diff --cached --name-only --diff-filter=ACMR)
  other_staged=()
  for file in "${staged_files[@]}"; do
    case "$file" in
      exercises.md|progress.png)
        ;;
      *)
        other_staged+=("$file")
        ;;
    esac
  done

  stashed_other_changes=0
  if [[ ${#other_staged[@]} -gt 0 ]]; then
    echo "Stashing other staged changes before committing progress artifacts..."
    git stash push --staged -m "progress sync: temporarily stash staged changes" -- "${other_staged[@]}"
    stashed_other_changes=1
  fi

  git add -- exercises.md progress.png

  if git diff --cached --quiet -- exercises.md progress.png; then
    echo "No progress artifact changes to commit."
  else
    git commit -m "chore(progress): sync dsa chart" -- exercises.md progress.png
  fi

  if [[ $stashed_other_changes -eq 1 ]]; then
    echo "Restoring previously staged changes as unstaged worktree changes..."
    git stash pop --quiet || {
      echo "Could not automatically restore stashed changes. Check git stash list." >&2
      exit 1
    }
    git restore --staged -- "${other_staged[@]}" 2>/dev/null || true
  fi

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
