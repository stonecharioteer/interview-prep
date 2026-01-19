# Repository Guidelines

## Purpose & Learning Approach
- Deliberate DSA/LeetCode practice focused on pattern recognition, not grinding.
- Start slow and explicit (invariants, edge cases, complexity), then increase speed.

## Project Structure & Module Organization
- `js/` holds Node JavaScript solutions (`main.js`) and tests (`main.test.js`).
- `python/` holds Python sources in `python/src/interview_prep` and tests in `python/test`.
- `rust/` holds Rust solutions in `rust/src`.
- `notes/` (recommended) for system design notes/diagrams.
- Use a year-based folder inside each language, e.g., `python/solutions/2025/` or `js/solutions/2025/`.
- `justfile` defines workflows across languages.

## Build, Test, and Development Commands
- `just run-tests` runs tests for all languages.
- `just run-tests py|js|rust` runs tests for a single language.
- `just run-some-tests <filter> <lang>` passes a filter to the selected test runner.
- Python: `cd python && uv run pytest`.
- JavaScript: `cd js && npm test`.
- Rust: `cd rust && cargo test`.

## Coding Style & Naming Conventions
- Python: 4-space indentation, `snake_case` functions/variables, `CamelCase` classes.
- JavaScript: 2-space indentation, `camelCase` functions.
- Rust: `rustfmt` defaults, `snake_case` for functions/modules, `CamelCase` for types.
- Tooling: `ruff`, `cargo fmt` as needed.

## Testing Guidelines
- Python: `pytest` in `python/test` using `test_*.py`; JavaScript: `*.test.js`; Rust: `#[cfg(test)]`.
- No explicit coverage thresholds; focus on edge cases and complexity checks.

## Yearly Practice & Solution Recording
- Keep each solution tied to a year for easy repeats (e.g., `2024/`, `2025/`).
- One file per problem per year with a short header comment (name, date, pattern, complexity).
- Keep solutions simple: plain scripts like `script.py` or `main.rs`; avoid extra packaging.

## Adding New Languages
- Add a top-level folder (e.g., `go/`, `java/`) with a minimal runner/test setup.
- Update `justfile` with `run-tests-<lang>` and `run-some-tests-<lang>` targets.
- Mirror the year-based solution layout to keep structure consistent across languages.

## Justfile Best Practices
- Keep recipes small and composable; prefer delegating to language-specific runners.
- Accept `LANG`/`FILTER` args and document expected values in comments.
- Keep outputs deterministic; avoid writing outside the repo or overwriting solution files.

## Commit & Pull Request Guidelines
- Recent history uses Conventional Commits (e.g., `feat(python): ...`, `chore: ...`). Match that pattern when possible.
- PRs should include a short summary, tests run, and any related notes or links.

## Tooling & Dependencies
- Required tooling: `uv`, `node/npm`, `rustup`, `just`, and `gum`.
