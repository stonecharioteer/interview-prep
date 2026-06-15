# Repository Guidelines

## Purpose & Learning Approach

- Deliberate DSA/LeetCode practice focused on pattern recognition, not grinding.
- Start slow and explicit (invariants, edge cases, complexity), then increase speed.
- Never modify DSA solution code. The repo owner writes solutions to learn; agents may inspect/read solution files for context, but must not create, edit, format, refactor, or overwrite files under `dsa/python/src/`, `dsa/js/src/`, or `dsa/rust/src/` unless the owner explicitly asks to change a specific non-solution support file.
- **Never directly provide solutions.** When asked about a problem, act as a coach: ask clarifying questions, prompt the user to articulate their own approach, suggest they think about invariants or edge cases, and guide them to discover the solution themselves. Do not give away code, optimal algorithms, or key insights unless the user explicitly requests them.

## Project Structure & Module Organization

- `dsa/js/` holds Node JavaScript solutions and tests.
- `dsa/python/` holds Python sources in `dsa/python/src` and tests in `dsa/python/test`.
- `dsa/rust/` holds Rust solutions in `dsa/rust/src`.
- `dist-sys/` is reserved for distributed systems practice (e.g. Fly.io / Maelstrom).
- `notes/` (recommended) for system design notes/diagrams.
- Use a year-based folder inside each DSA language area, e.g., `dsa/python/solutions/2025/` or `dsa/js/solutions/2025/`.
- `justfile` defines workflows across languages.

## Build, Test, and Development Commands

- `just test all` runs tests for all languages.
- `just test py|js|rust` runs tests for a single language.
- `just test <lang> <filter>` passes a filter to the selected test runner.
- `just setup` installs core Python, JavaScript, and Rust dependencies and installs the latest repo hooks.
- `just install-hooks` installs repo-managed git hooks; run it again after hook config changes so the latest hooks are active.
- `just setup-notebooks` installs optional notebook tooling.
- `just lint` runs Ruff, Prettier checks, and `cargo fmt --check`.
- `just typecheck` runs the JavaScript/TypeScript typechecker.
- Python: `cd dsa/python && uv run pytest`.
- JavaScript: `pnpm --dir dsa/js test`.
- Rust: `cd dsa/rust && cargo test`.

## Coding Style & Naming Conventions

- Python: 4-space indentation, `snake_case` functions/variables, `CamelCase` classes.
- JavaScript: 2-space indentation, `camelCase` functions.
- Rust: `rustfmt` defaults, `snake_case` for functions/modules, `CamelCase` for types.
- Tooling: `ruff`, `cargo fmt` as needed.

## Testing Guidelines

- Python: `pytest` in `dsa/python/test` using `test_*.py`; JavaScript: `*.test.js`; Rust: `#[cfg(test)]`.
- Agents may improve test harnesses, fixtures, documentation, and tooling, but must not implement or patch DSA solutions to make tests pass.
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
- If hook definitions change, reinstall/update them with `just install-hooks` before continuing work.

## Commit & Pull Request Guidelines

- Recent history uses Conventional Commits (e.g., `feat(python): ...`, `chore: ...`). Match that pattern when possible.
- PRs should include a short summary, tests run, and any related notes or links.

## Tooling & Dependencies

- Required tooling: `uv`, `pnpm`, `rustup`, `just`, and `gum`.
- Git hooks enforce no direct commits to `main`, Conventional Commits, and staged-file formatting for Python, JS/TS/Markdown, and Rust.
