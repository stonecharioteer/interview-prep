#!/usr/bin/env python3
"""Show next N unsolved problems for a given language."""

import argparse
import re
from pathlib import Path

from rich.console import Console
from rich.table import Table

LANG_PATTERNS = {
    "python": ("🐍", r"🐍\[ \]"),
    "py": ("🐍", r"🐍\[ \]"),
    "rust": ("🦀", r"🦀\[ \]"),
    "js": ("🟨", r"🟨\[ \]"),
    "javascript": ("🟨", r"🟨\[ \]"),
}

LANG_COLORS = {
    "🐍": "blue",
    "🦀": "orange1",
    "🟨": "yellow",
}


def parse_exercises(readme_path: Path, lang: str, limit: int) -> list[tuple[int, str, str]]:
    """Parse README and return unsolved exercises for the given language."""
    emoji, pattern = LANG_PATTERNS[lang]
    content = readme_path.read_text()

    exercise_re = re.compile(r"^(\d+)\.\s+([^:]+):\s+(.+?)\s+🐍\[[x ]\]", re.MULTILINE)
    unchecked_re = re.compile(pattern)

    results = []
    for match in exercise_re.finditer(content):
        line = match.group(0)
        if unchecked_re.search(content[match.start():match.end() + 20]):
            num = int(match.group(1))
            topic = match.group(2).strip()
            desc = match.group(3).strip()
            # Clean up description (remove trailing emoji markers)
            desc = re.sub(r"\s*🐍\[[x ]\].*$", "", desc)
            results.append((num, topic, desc))
            if len(results) >= limit:
                break

    return results


def main():
    parser = argparse.ArgumentParser(description="Show next unsolved problems")
    parser.add_argument("lang", choices=["python", "py", "rust", "js", "javascript"],
                        help="Language to check")
    parser.add_argument("-n", "--count", type=int, default=10,
                        help="Number of problems to show (default: 10)")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"

    exercises = parse_exercises(readme_path, args.lang, args.count)

    console = Console()
    emoji, _ = LANG_PATTERNS[args.lang]
    color = LANG_COLORS[emoji]

    if not exercises:
        console.print(f"[green]All done![/green] No unsolved {args.lang} exercises remaining.")
        return

    table = Table(title=f"{emoji} Next {len(exercises)} unsolved exercises",
                  title_style=f"bold {color}")
    table.add_column("#", style="dim", width=4)
    table.add_column("Topic", style="cyan")
    table.add_column("Exercise", style="white")

    for num, topic, desc in exercises:
        table.add_row(str(num), topic, desc)

    console.print(table)


if __name__ == "__main__":
    main()
