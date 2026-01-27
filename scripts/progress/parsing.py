"""README parsing and git history functions."""

import re
import subprocess
from pathlib import Path

from .db import get_db
from .models import EXERCISES_FILE, Language


def parse_readme(readme_path: Path) -> list[dict]:
    content = readme_path.read_text()
    exercises = []

    pattern = re.compile(
        r"^(\d+)\.\s+([^:]+):\s+(.+?)\s+\U0001F40D\[([x ])\]\s+\U0001F980\[([x ])\]\s+\U0001F7E8\[([x ])\]",
        re.MULTILINE,
    )

    for match in pattern.finditer(content):
        exercises.append({
            "id": int(match.group(1)),
            "topic": match.group(2).strip(),
            "name": match.group(3).strip().replace("`", ""),
            "readme_status": {
                "python": match.group(4) == "x",
                "rust": match.group(5) == "x",
                "typescript": match.group(6) == "x",
            },
        })

    return exercises


def update_exercises_file(repo_root: Path, console) -> None:
    """Generate exercises.md with current progress from database."""
    conn = get_db(repo_root)

    # Get all exercises with status
    exercises = conn.execute(
        """
        SELECT
            e.id, ANY_VALUE(e.topic) as topic, ANY_VALUE(e.name) as name,
            MAX(CASE WHEN p.language = 'python' THEN p.status END) as python,
            MAX(CASE WHEN p.language = 'rust' THEN p.status END) as rust,
            MAX(CASE WHEN p.language = 'typescript' THEN p.status END) as typescript
        FROM exercises e
        LEFT JOIN progress p ON e.id = p.exercise_id
        GROUP BY e.id
        ORDER BY e.id
        """
    ).fetchall()

    # Get counts
    py_solved = conn.execute(
        "SELECT COUNT(*) FROM progress WHERE language = 'python' AND status = 'solved'"
    ).fetchone()[0]
    total = len(exercises)
    pct = int(100 * py_solved / total) if total else 0

    conn.close()

    # Build content
    lines = [
        "# Exercise List",
        "",
        f"**Progress: {py_solved}/{total} exercises completed in Python ({pct}%)**",
        "",
    ]

    for ex_id, topic, name, py_status, rs_status, ts_status in exercises:
        py = "x" if py_status == "solved" else " "
        rs = "x" if rs_status == "solved" else " "
        ts = "x" if ts_status == "solved" else " "
        lines.append(f"{ex_id}. {topic}: `{name}` \U0001F40D[{py}] \U0001F980[{rs}] \U0001F7E8[{ts}]")

    exercises_path = repo_root / EXERCISES_FILE
    exercises_path.write_text("\n".join(lines) + "\n")
    console.print(f"[green]Updated {EXERCISES_FILE}[/green] ({py_solved}/{total} Python exercises)")


def get_solved_dates_from_git(repo_root: Path) -> dict[str, dict[str, str]]:
    solved_dates: dict[str, dict[str, str]] = {lang.value: {} for lang in Language}

    lang_paths = {
        "python": "python/src/",
        "rust": "rust/src/",
        "typescript": "js/src/",
    }

    for lang, path in lang_paths.items():
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%ad|%s", "--date=short", "--name-only", "--", path],
                capture_output=True,
                text=True,
                cwd=repo_root,
                check=True,
            )

            current_date = None
            for line in result.stdout.split("\n"):
                if "|" in line:
                    current_date = line.split("|", 1)[0]
                elif current_date and line.strip():
                    solved_dates[lang][line.strip().lower()] = current_date

        except subprocess.CalledProcessError:
            pass

    return solved_dates


def get_commit_dates(repo_root: Path) -> set[str]:
    try:
        result = subprocess.run(
            [
                "git", "log", "--pretty=format:%ad", "--date=short", "--",
                "python/src/", "python/test/", ":!*.png", ":!*.toml", ":!*.lock",
            ],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
        return set(d for d in result.stdout.strip().split("\n") if d)
    except subprocess.CalledProcessError:
        return set()


def match_exercise_to_file(exercise: dict, filenames: dict[str, str]) -> str | None:
    keywords = [
        exercise["name"].lower().replace("(", "").replace(")", "").replace(",", ""),
        exercise["topic"].lower(),
    ]

    for filename, date in filenames.items():
        for keyword in keywords:
            keyword_parts = keyword.split()
            if any(part in filename for part in keyword_parts if len(part) > 2):
                return date
    return None
