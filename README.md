# DSA Interview Prep

This repo contains DSA practice solutions in Python, JavaScript (Node), and Rust.

## Writing New Solutions
- Use a year-based folder inside each language, e.g., `python/solutions/2026/` or `rust/solutions/2026/`.
- One file per problem per year. Keep older years intact.
- Keep solutions as simple scripts (no extra packaging).

## Running Solutions (2026)
- Python: `just run 2026 py script.py`
- Rust: `just run 2026 rust script.rs`

## Tests
- All languages: `just run-tests`
- One language: `just run-tests py|js|rust`
- With filter: `just run-some-tests <filter> <lang>`

## Dependencies
* uv
* rustup
* just
* gum
* node/npm
