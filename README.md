# DSA Interview Prep

![Progress](./progress.png)

Practice solutions in Python, JavaScript (Node), and Rust.

See [exercises.md](./exercises.md) for the full exercise list with progress tracking.

## Progress CLI

Track exercise progress using DuckDB. Run from the `python/` directory:

```bash
# Show current progress summary
uv run python ../scripts/progress.py

# Show next 10 unsolved exercises
uv run python ../scripts/progress.py next python
uv run python ../scripts/progress.py next python -n 5

# List all exercises (with optional filters)
uv run python ../scripts/progress.py list
uv run python ../scripts/progress.py list --topic "Sorting"
uv run python ../scripts/progress.py list --lang python --status solved

# Mark exercise progress
uv run python ../scripts/progress.py mark 30 python solved
uv run python ../scripts/progress.py mark 30 python attempted
uv run python ../scripts/progress.py mark 30 python not_started

# Update exercises.md and progress.png
uv run python ../scripts/progress.py sync

# Or update them separately
uv run python ../scripts/progress.py exercises  # updates exercises.md
uv run python ../scripts/progress.py plot       # updates progress.png
```

Or use just commands:

```bash
just progress          # sync exercises.md and progress.png
just next python       # show next 10 unsolved exercises
just next python 5     # show next 5 unsolved exercises
just solve 30 python   # mark exercise 30 as solved
```

## Practice Notes

- Start with small, hand-written inputs before random data.
- For each function: note intent, edge cases, and time/space complexity.
- Keep each exercise as a single script file and avoid extra packaging.

## Goal

Be comfortable with:

- **Data structures**: arrays, linked lists, stacks, queues, trees (binary, BST), heaps, tries, graphs, Union-Find
- **Techniques**: two pointers, sliding window, binary search variations, monotonic stack
- **Algorithms**: sorting (comparison and non-comparison), recursion, backtracking, greedy, dynamic programming
- **Patterns**: string matching (KMP, Rabin-Karp), bit manipulation, graph traversals (BFS/DFS), shortest paths, MST
- **Problem-solving**: recognizing which technique fits which problem shape

## Running Solutions

- Python: `just run 2026 py script.py`
- Rust: `just run 2026 rust script.rs`

## Tests

- All languages: `just run-tests`
- One language: `just run-tests py|js|rust`
- With filter: `just run-some-tests <filter> <lang>`

## Dependencies

- uv
- rustup
- just
- gum
- node/npm
