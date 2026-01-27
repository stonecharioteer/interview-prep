#!/usr/bin/env python3
"""
Unified DSA exercise progress tracker CLI.

Uses DuckDB for tracking, generates README updates and progress visualizations.
"""

import os
import re
import subprocess
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import duckdb
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import typer
from rich.console import Console
from rich.table import Table

# ============ App Setup ============

app = typer.Typer(
    name="progress",
    help="Track DSA exercises and system design studies (books, courses, papers).",
    no_args_is_help=False,
)

study_app = typer.Typer(
    name="study",
    help="Track system design studies (books, courses, papers).",
    no_args_is_help=False,
)
app.add_typer(study_app, name="study")

console = Console()

# ============ Constants ============

# Use PROGRESS_TEST_DB=1 to use a test database file
DB_FILE = "progress_test.db" if os.environ.get("PROGRESS_TEST_DB") else "progress.db"
EXERCISES_FILE = "exercises.md"
DEFAULT_YEAR = 2026


class Language(str, Enum):
    python = "python"
    rust = "rust"
    typescript = "typescript"


class Status(str, Enum):
    not_started = "not_started"
    attempted = "attempted"
    solved = "solved"


class StudyStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


LANG_EMOJI = {"python": "🐍", "rust": "🦀", "typescript": "🟨"}
STATUS_SYMBOL = {
    "not_started": "[dim]·[/]",
    "attempted": "[yellow]○[/]",
    "solved": "[green]✓[/]",
}

PALETTE = {
    "python": "#6366f1",
    "rust": "#f97316",
    "typescript": "#eab308",
    "bg": "#f1f5f9",
    "active": "#10b981",
    "inactive": "#cbd5e1",
    "text": "#334155",
    "text_light": "#64748b",
    "text_muted": "#94a3b8",
    "accent": "#8b5cf6",
    "card_bg": "#f8fafc",
    "card_border": "#e2e8f0",
    # Streak colors - blue/orange scheme
    "dsa": "#3b82f6",      # Blue
    "study": "#f59e0b",    # Amber
    "both": "#06b6d4",     # Cyan
}

TOPIC_NORMALIZATION = {
    "Trees (binary)": "Trees (binary)",
    "Trees (BST)": "Trees (BST)",
    "DP ": "Dynamic Programming",
    "Heap": "Heap",
    "Graph": "Graph",
    "Union-Find": "Union-Find",
    "String matching": "String Matching",
    "Conversions": "Conversions",
    "Monotonic stack": "Monotonic Stack",
}


def normalize_topic(topic: str) -> str:
    for prefix, normalized in TOPIC_NORMALIZATION.items():
        if topic.startswith(prefix):
            return normalized
    return topic


# ============ Paths & Database ============


def get_repo_root() -> Path:
    return Path(__file__).parent.parent


def get_db(repo_root: Path) -> duckdb.DuckDBPyConnection:
    db_path = repo_root / DB_FILE
    conn = duckdb.connect(str(db_path))

    conn.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY,
            topic VARCHAR NOT NULL,
            name VARCHAR NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            exercise_id INTEGER NOT NULL,
            language VARCHAR NOT NULL,
            status VARCHAR NOT NULL DEFAULT 'not_started',
            date DATE,
            PRIMARY KEY (exercise_id, language),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    """)

    # ============ Study Tracking Tables ============

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            author VARCHAR,
            total_chapters INTEGER,
            url VARCHAR
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chapter_progress (
            book_id INTEGER NOT NULL,
            chapter_number INTEGER NOT NULL,
            progress_pct INTEGER NOT NULL DEFAULT 100,
            updated_date DATE NOT NULL,
            PRIMARY KEY (book_id, chapter_number),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            source VARCHAR,
            code VARCHAR,
            playlist_url VARCHAR
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY,
            course_id INTEGER NOT NULL,
            lecture_number INTEGER NOT NULL,
            title VARCHAR NOT NULL,
            url VARCHAR,
            UNIQUE (course_id, lecture_number),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lecture_progress (
            lecture_id INTEGER PRIMARY KEY,
            date DATE,
            status VARCHAR NOT NULL DEFAULT 'not_started',
            FOREIGN KEY (lecture_id) REFERENCES lectures(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY,
            lecture_id INTEGER NOT NULL,
            name VARCHAR NOT NULL,
            url VARCHAR,
            FOREIGN KEY (lecture_id) REFERENCES lectures(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS homework_progress (
            homework_id INTEGER PRIMARY KEY,
            date DATE,
            status VARCHAR NOT NULL DEFAULT 'not_started',
            FOREIGN KEY (homework_id) REFERENCES homework(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            course_id INTEGER NOT NULL,
            name VARCHAR NOT NULL,
            url VARCHAR,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS project_progress (
            project_id INTEGER PRIMARY KEY,
            date DATE,
            status VARCHAR NOT NULL DEFAULT 'not_started',
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            authors VARCHAR,
            url VARCHAR,
            year INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_progress (
            paper_id INTEGER PRIMARY KEY,
            date DATE,
            status VARCHAR NOT NULL DEFAULT 'not_started',
            FOREIGN KEY (paper_id) REFERENCES papers(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS course_books (
            course_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            PRIMARY KEY (course_id, book_id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lecture_chapters (
            lecture_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            chapters VARCHAR NOT NULL,
            PRIMARY KEY (lecture_id, book_id),
            FOREIGN KEY (lecture_id) REFERENCES lectures(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS course_papers (
            course_id INTEGER NOT NULL,
            paper_id INTEGER NOT NULL,
            PRIMARY KEY (course_id, paper_id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (paper_id) REFERENCES papers(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lecture_papers (
            lecture_id INTEGER NOT NULL,
            paper_id INTEGER NOT NULL,
            PRIMARY KEY (lecture_id, paper_id),
            FOREIGN KEY (lecture_id) REFERENCES lectures(id),
            FOREIGN KEY (paper_id) REFERENCES papers(id)
        )
    """)

    return conn


# ============ README Parsing ============


def parse_readme(readme_path: Path) -> list[dict]:
    content = readme_path.read_text()
    exercises = []

    pattern = re.compile(
        r"^(\d+)\.\s+([^:]+):\s+(.+?)\s+🐍\[([x ])\]\s+🦀\[([x ])\]\s+🟨\[([x ])\]",
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


def update_exercises_file(repo_root: Path) -> None:
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
        lines.append(f"{ex_id}. {topic}: `{name}` 🐍[{py}] 🦀[{rs}] 🟨[{ts}]")

    exercises_path = repo_root / EXERCISES_FILE
    exercises_path.write_text("\n".join(lines) + "\n")
    console.print(f"[green]Updated {EXERCISES_FILE}[/green] ({py_solved}/{total} Python exercises)")


# ============ Git History ============


def get_solved_dates_from_git(repo_root: Path) -> dict[str, dict[str, str]]:
    solved_dates: dict[str, dict[str, str]] = {lang: {} for lang in Language}

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


# ============ Summary Display ============


def show_summary(repo_root: Path) -> None:
    conn = get_db(repo_root)
    total = conn.execute("SELECT COUNT(*) FROM exercises").fetchone()[0]

    console.print()
    for lang in Language:
        emoji = LANG_EMOJI[lang.value]
        solved = conn.execute(
            "SELECT COUNT(*) FROM progress WHERE language = ? AND status = 'solved'",
            [lang.value],
        ).fetchone()[0]
        attempted = conn.execute(
            "SELECT COUNT(*) FROM progress WHERE language = ? AND status = 'attempted'",
            [lang.value],
        ).fetchone()[0]
        remaining = total - solved - attempted
        console.print(
            f"  {emoji} [green]{solved}[/] solved, [yellow]{attempted}[/] attempted, [dim]{remaining}[/] remaining"
        )

    conn.close()


# ============ Visualization ============


def get_topic_progress_from_db(conn: duckdb.DuckDBPyConnection, lang: str = "python") -> dict:
    results = conn.execute(
        """
        SELECT
            e.topic,
            COUNT(*) as total,
            SUM(CASE WHEN p.status = 'solved' THEN 1 ELSE 0 END) as solved
        FROM exercises e
        LEFT JOIN progress p ON e.id = p.exercise_id AND p.language = ?
        GROUP BY e.topic
        """,
        [lang],
    ).fetchall()

    topics = {}
    for topic, total, solved in results:
        normalized = normalize_topic(topic)
        if normalized not in topics:
            topics[normalized] = {"total": 0, "python": 0}
        topics[normalized]["total"] += total
        topics[normalized]["python"] += solved

    return topics


def get_activity_dates_from_db(conn: duckdb.DuckDBPyConnection) -> set[str]:
    results = conn.execute(
        """
        SELECT DISTINCT CAST(date AS VARCHAR) FROM progress
        WHERE date IS NOT NULL AND status = 'solved'
        """
    ).fetchall()
    return set(row[0] for row in results if row[0])


def calculate_streaks(commit_dates: set[str], year: int) -> tuple[int, int, int]:
    if not commit_dates:
        return 0, 0, 0

    year_dates = sorted([d for d in commit_dates if d.startswith(str(year))])
    if not year_dates:
        return 0, 0, 0

    total_days = len(year_dates)
    date_objs = [datetime.strptime(d, "%Y-%m-%d").date() for d in year_dates]
    date_set = set(date_objs)

    longest = 1
    current = 1
    for i in range(1, len(date_objs)):
        if (date_objs[i] - date_objs[i - 1]).days == 1:
            current += 1
            longest = max(longest, current)
        elif date_objs[i] != date_objs[i - 1]:
            current = 1

    today = datetime.now().date()
    current_streak = 0
    check_date = today

    while check_date in date_set or (current_streak == 0 and check_date == today):
        if check_date in date_set:
            current_streak += 1
        check_date -= timedelta(days=1)
        if check_date.year < year:
            break

    return current_streak, longest, total_days


def format_timestamp() -> str:
    now = datetime.now()
    return now.strftime("%B %d, %Y at %I:%M %p").replace(" 0", " ").replace("AM", "am").replace("PM", "pm")


def categorize_topics(topics: dict) -> tuple[list, list]:
    in_progress = [(name, data) for name, data in topics.items() if data["python"] > 0]
    not_started = [(name, data) for name, data in topics.items() if data["python"] == 0]
    in_progress.sort(key=lambda x: x[1]["python"], reverse=True)
    not_started.sort(key=lambda x: x[1]["total"], reverse=True)
    return in_progress, not_started


def draw_hero_section(ax, total_done: int, total_exercises: int, current_streak: int):
    ax.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    remaining = total_exercises - total_done
    donut_ax = ax.inset_axes([0.02, 0.1, 0.35, 0.85])

    donut_ax.pie(
        [total_done, remaining],
        colors=[PALETTE["python"], PALETTE["bg"]],
        startangle=90,
        wedgeprops=dict(width=0.35, edgecolor="white", linewidth=2),
    )
    center_circle = plt.Circle((0, 0), 0.45, fc="white")
    donut_ax.add_artist(center_circle)

    donut_ax.text(
        0, 0.08, f"{total_done}", fontsize=28, fontweight="bold",
        ha="center", va="center", color=PALETTE["python"]
    )
    donut_ax.text(
        0, -0.25, "done", fontsize=10, ha="center", va="center",
        color=PALETTE["text_light"]
    )

    pct = int(100 * total_done / total_exercises) if total_exercises > 0 else 0
    ax.text(4.0, 2.2, "Interview Prep", fontsize=22, fontweight="bold", color=PALETTE["text"], va="center")
    ax.text(
        4.0, 1.4, f"{total_done} of {total_exercises} DSA exercises ({pct}%)",
        fontsize=12, color=PALETTE["text_light"], va="center"
    )

    if current_streak > 0:
        badge_x, badge_y = 4.0, 0.5
        streak_color = PALETTE["active"] if current_streak >= 3 else PALETTE["text_muted"]

        badge = mpatches.FancyBboxPatch(
            (badge_x - 0.1, badge_y - 0.25), 2.2, 0.5,
            boxstyle="round,pad=0.1,rounding_size=0.2",
            facecolor=PALETTE["card_bg"],
            edgecolor=streak_color,
            linewidth=1.5,
        )
        ax.add_patch(badge)
        ax.text(
            badge_x + 1.0, badge_y, f"{current_streak}-day streak",
            fontsize=10, fontweight="bold", ha="center", va="center", color=streak_color
        )


def draw_topic_progress(ax, in_progress: list, not_started_count: int):
    ax.set_facecolor("white")

    if not in_progress:
        ax.axis("off")
        ax.text(
            0.5, 0.5, "No topics started yet!", transform=ax.transAxes,
            ha="center", va="center", fontsize=12, color=PALETTE["text_light"]
        )
        return

    topic_names = [t[0] for t in in_progress]
    totals = [t[1]["total"] for t in in_progress]
    python_done = [t[1]["python"] for t in in_progress]

    y_pos = np.arange(len(topic_names))
    bar_height = 0.6
    max_total = max(totals)

    ax.text(-0.5, -1.2, "TOPIC PROGRESS", fontsize=10, fontweight="bold", color=PALETTE["text_muted"])

    for i, total in enumerate(totals):
        ax.barh(y_pos[i], total, height=bar_height + 0.15, color=PALETTE["bg"], zorder=1)

    ax.barh(y_pos, python_done, height=bar_height, color=PALETTE["python"], zorder=2)

    label_x = max_total + 0.8
    for i, (total, py) in enumerate(zip(totals, python_done)):
        ax.text(
            label_x, y_pos[i], f"{py}/{total}", va="center", ha="left",
            fontsize=10, color=PALETTE["text"], fontweight="medium"
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(topic_names, fontsize=10, color=PALETTE["text"], fontweight="medium")
    ax.invert_yaxis()
    ax.set_xlim(-0.5, max_total + 4)
    ax.set_ylim(max(y_pos) + 0.8, -1.8)

    if not_started_count > 0:
        ax.text(
            -0.5, max(y_pos) + 0.6, f"+ {not_started_count} more topics not yet started",
            fontsize=9, color=PALETTE["text_muted"], style="italic"
        )

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)


def draw_learning_streak(ax, commit_dates: set, year: int, current_streak: int, longest_streak: int, total_days: int):
    ax.set_facecolor("white")
    ax.axis("off")

    ax.text(0, 5.5, "LEARNING STREAK", fontsize=10, fontweight="bold", color=PALETTE["text_muted"])

    today = datetime.now().date()
    days_since_sunday = (today.weekday() + 1) % 7
    this_week_start = today - timedelta(days=days_since_sunday)
    four_weeks_ago = this_week_start - timedelta(weeks=3)

    day_labels = ["S", "M", "T", "W", "T", "F", "S"]
    for i, label in enumerate(day_labels):
        ax.text(
            i + 0.44, 4.8, label, ha="center", va="center",
            fontsize=9, color=PALETTE["text_light"], fontweight="medium"
        )

    current_date = four_weeks_ago
    for week in range(4):
        for day in range(7):
            date_str = current_date.strftime("%Y-%m-%d")
            is_future = current_date > today
            is_today = current_date == today
            is_active = date_str in commit_dates

            if is_future:
                color = PALETTE["bg"]
            elif is_active:
                color = PALETTE["active"]
            else:
                color = PALETTE["inactive"]

            rect = mpatches.FancyBboxPatch(
                (day, 3.5 - week), 0.88, 0.88,
                boxstyle="round,pad=0,rounding_size=0.2",
                facecolor=color,
                edgecolor=PALETTE["accent"] if is_today else "white",
                linewidth=2 if is_today else 0.5,
            )
            ax.add_patch(rect)
            current_date += timedelta(days=1)

    week_labels = ["3 weeks ago", "2 weeks ago", "Last week", "This week"]
    for week, label in enumerate(week_labels):
        ax.text(7.5, 3.5 - week + 0.44, label, ha="left", va="center", fontsize=8, color=PALETTE["text_light"])

    stats_x = 13
    card = mpatches.FancyBboxPatch(
        (stats_x, 0.3), 6, 4.5,
        boxstyle="round,pad=0.3,rounding_size=0.4",
        facecolor=PALETTE["card_bg"],
        edgecolor=PALETTE["card_border"],
        linewidth=1,
    )
    ax.add_patch(card)

    fire_color = PALETTE["active"] if current_streak >= 3 else PALETTE["text_muted"]
    trophy_color = PALETTE["accent"] if longest_streak >= 7 else PALETTE["text_muted"]

    ax.text(stats_x + 3, 4.0, f"{current_streak}", fontsize=18, fontweight="bold", ha="center", va="center", color=fire_color)
    ax.text(stats_x + 3, 3.3, "current streak", fontsize=8, ha="center", va="center", color=PALETTE["text_light"])

    ax.text(stats_x + 3, 2.3, f"{longest_streak}", fontsize=18, fontweight="bold", ha="center", va="center", color=trophy_color)
    ax.text(stats_x + 3, 1.6, "best streak", fontsize=8, ha="center", va="center", color=PALETTE["text_light"])

    ax.text(stats_x + 3, 0.85, f"{total_days} days total", fontsize=9, ha="center", va="center", color=PALETTE["text"])

    ax.set_xlim(-0.5, 20)
    ax.set_ylim(-0.5, 6)


def parse_chapters_string(chapters_str: str) -> set[int]:
    """Parse a chapters string like '1-3' or '5,7' into a set of chapter numbers."""
    if not chapters_str:
        return set()

    chapters = set()
    parts = chapters_str.replace(" ", "").split(",")

    for part in parts:
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                chapters.update(range(int(start), int(end) + 1))
            except (ValueError, TypeError):
                pass
        else:
            try:
                chapters.add(int(part))
            except (ValueError, TypeError):
                pass

    return chapters


def get_study_data_for_chart(conn: duckdb.DuckDBPyConnection) -> dict:
    """Get study progress data for the chart."""
    # Books - calculate progress from chapter_progress
    books = conn.execute("""
        SELECT
            b.id, b.title, b.author, b.total_chapters,
            SUM(CASE WHEN cp.progress_pct = 100 THEN 1 ELSE 0 END) as chapters_completed,
            MAX(cp.updated_date) as last_read
        FROM books b
        LEFT JOIN chapter_progress cp ON b.id = cp.book_id
        GROUP BY b.id, b.title, b.author, b.total_chapters
        ORDER BY last_read DESC NULLS LAST
        LIMIT 5
    """).fetchall()

    # Courses
    courses = conn.execute("""
        SELECT
            c.id, c.name, c.source, c.code,
            COUNT(l.id) as total,
            SUM(CASE WHEN lp.status = 'completed' THEN 1 ELSE 0 END) as completed,
            MAX(lp.date) as last_watched
        FROM courses c
        LEFT JOIN lectures l ON c.id = l.course_id
        LEFT JOIN lecture_progress lp ON l.id = lp.lecture_id
        GROUP BY c.id, c.name, c.source, c.code
        ORDER BY last_watched DESC NULLS LAST
        LIMIT 5
    """).fetchall()

    # Papers
    papers = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN pp.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM papers p
        LEFT JOIN paper_progress pp ON p.id = pp.paper_id
    """).fetchone()

    return {
        "books": books,
        "courses": courses,
        "papers_total": papers[0] or 0,
        "papers_completed": papers[1] or 0,
    }


def draw_study_progress(ax, study_data: dict):
    """Draw study progress section."""
    ax.set_facecolor("white")
    ax.axis("off")

    books = study_data["books"]
    courses = study_data["courses"]
    papers_total = study_data["papers_total"]
    papers_completed = study_data["papers_completed"]

    # Filter to only books/courses with activity
    active_books = [b for b in books if (b[4] or 0) > 0]  # chapters_completed > 0
    active_courses = [c for c in courses if (c[4] or 0) > 0]  # has lectures

    if not active_books and not active_courses and papers_total == 0:
        ax.text(
            0.5, 0.5, "No study activity yet",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10, color=PALETTE["text_light"]
        )
        return

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 6)

    # Title
    ax.text(0.2, 5.5, "STUDY PROGRESS", fontsize=10, fontweight="bold", color=PALETTE["text_muted"])

    y_pos = 4.8

    # Courses section - only if there are courses with lectures
    if active_courses:
        ax.text(0.2, y_pos, "Courses:", fontsize=9, fontweight="bold", color=PALETTE["text"])
        y_pos -= 0.5

        for course_id, name, source, code, total, completed, last_watched in active_courses:
            completed = completed or 0
            total = total or 0

            # Build display name
            display_name = ""
            if source:
                display_name += f"{source} "
            if code:
                display_name += f"{code} "
            display_name += name
            if len(display_name) > 35:
                display_name = display_name[:32] + "..."

            # Progress bar background
            bar_width = 6
            bar_height = 0.3
            bar_x = 10

            rect_bg = mpatches.FancyBboxPatch(
                (bar_x, y_pos - 0.15), bar_width, bar_height,
                boxstyle="round,pad=0,rounding_size=0.1",
                facecolor=PALETTE["bg"],
                edgecolor="none",
            )
            ax.add_patch(rect_bg)

            # Progress bar fill
            if total > 0:
                pct = completed / total
                rect_fill = mpatches.FancyBboxPatch(
                    (bar_x, y_pos - 0.15), bar_width * pct, bar_height,
                    boxstyle="round,pad=0,rounding_size=0.1",
                    facecolor=PALETTE["accent"],
                    edgecolor="none",
                )
                ax.add_patch(rect_fill)

            # Course name and stats
            ax.text(0.4, y_pos, display_name, fontsize=8, color=PALETTE["text"], va="center")
            progress_str = f"{completed}/{total}" if total > 0 else "0"
            ax.text(bar_x + bar_width + 0.3, y_pos, progress_str, fontsize=8, color=PALETTE["text"], va="center")

            y_pos -= 0.5

        y_pos -= 0.2

    # Books section - only books with reading progress
    if active_books:
        ax.text(0.2, y_pos, "Books:", fontsize=9, fontweight="bold", color=PALETTE["text"])
        y_pos -= 0.5

        for book_id, title, author, total_chapters, chapters_completed, last_read in active_books:
            chapters_completed = chapters_completed or 0
            total_chapters = total_chapters or 0
            # Build display: "Title by Author"
            display_name = f"{title} by {author}" if author else title
            display_name = display_name if len(display_name) <= 40 else display_name[:37] + "..."

            # Progress bar background
            bar_width = 6
            bar_height = 0.3
            bar_x = 10

            rect_bg = mpatches.FancyBboxPatch(
                (bar_x, y_pos - 0.15), bar_width, bar_height,
                boxstyle="round,pad=0,rounding_size=0.1",
                facecolor=PALETTE["bg"],
                edgecolor="none",
            )
            ax.add_patch(rect_bg)

            # Progress bar fill
            if total_chapters > 0:
                pct = min(1.0, chapters_completed / total_chapters)
                rect_fill = mpatches.FancyBboxPatch(
                    (bar_x, y_pos - 0.15), bar_width * pct, bar_height,
                    boxstyle="round,pad=0,rounding_size=0.1",
                    facecolor=PALETTE["active"],
                    edgecolor="none",
                )
                ax.add_patch(rect_fill)
                progress_str = f"{chapters_completed}/{total_chapters}"
            else:
                # No total chapters set, just show chapters read
                progress_str = f"{chapters_completed} ch"

            ax.text(0.4, y_pos, display_name, fontsize=8, color=PALETTE["text"], va="center")
            ax.text(bar_x + bar_width + 0.3, y_pos, progress_str, fontsize=8, color=PALETTE["text"], va="center")

            y_pos -= 0.5

        y_pos -= 0.2

    # Papers summary - only count, no list
    if papers_total > 0:
        ax.text(0.2, y_pos, "Papers:", fontsize=9, fontweight="bold", color=PALETTE["text"])
        papers_text = f"{papers_completed}/{papers_total} read"
        ax.text(2.5, y_pos, papers_text, fontsize=8, color=PALETTE["text"], va="center")


def draw_combined_streak(ax, dsa_dates: set, study_dates: set, year: int,
                         dsa_current: int, dsa_longest: int, dsa_total: int,
                         study_current: int, study_longest: int, study_total: int):
    """Draw learning streak with both DSA and study stats."""
    ax.set_facecolor("white")
    ax.axis("off")

    ax.text(0, 5.5, "LEARNING STREAKS", fontsize=10, fontweight="bold", color=PALETTE["text_muted"])

    today = datetime.now().date()
    days_since_sunday = (today.weekday() + 1) % 7
    this_week_start = today - timedelta(days=days_since_sunday)
    four_weeks_ago = this_week_start - timedelta(weeks=3)

    # Combined dates for calendar
    all_dates = dsa_dates | study_dates

    day_labels = ["S", "M", "T", "W", "T", "F", "S"]
    for i, label in enumerate(day_labels):
        ax.text(
            i + 0.44, 4.8, label, ha="center", va="center",
            fontsize=9, color=PALETTE["text_light"], fontweight="medium"
        )

    current_date = four_weeks_ago
    for week in range(4):
        for day in range(7):
            date_str = current_date.strftime("%Y-%m-%d")
            is_future = current_date > today
            is_today = current_date == today
            is_dsa = date_str in dsa_dates
            is_study = date_str in study_dates

            if is_future:
                color = PALETTE["bg"]
            elif is_dsa and is_study:
                color = PALETTE["both"]  # Both
            elif is_dsa:
                color = PALETTE["dsa"]  # DSA only
            elif is_study:
                color = PALETTE["study"]  # Study only
            else:
                color = PALETTE["inactive"]

            rect = mpatches.FancyBboxPatch(
                (day, 3.5 - week), 0.88, 0.88,
                boxstyle="round,pad=0,rounding_size=0.2",
                facecolor=color,
                edgecolor=PALETTE["accent"] if is_today else "white",
                linewidth=2 if is_today else 0.5,
            )
            ax.add_patch(rect)
            current_date += timedelta(days=1)

    week_labels = ["3 weeks ago", "2 weeks ago", "Last week", "This week"]
    for week, label in enumerate(week_labels):
        ax.text(7.5, 3.5 - week + 0.44, label, ha="left", va="center", fontsize=8, color=PALETTE["text_light"])

    # Legend
    ax.text(0, -0.3, "Legend:", fontsize=8, color=PALETTE["text_light"])
    legend_items = [
        (PALETTE["dsa"], "DSA"),
        (PALETTE["study"], "Study"),
        (PALETTE["both"], "Both"),
    ]
    legend_x = 1.8
    for color, label in legend_items:
        rect = mpatches.FancyBboxPatch(
            (legend_x, -0.45), 0.4, 0.3,
            boxstyle="round,pad=0,rounding_size=0.1",
            facecolor=color, edgecolor="none"
        )
        ax.add_patch(rect)
        ax.text(legend_x + 0.6, -0.3, label, fontsize=7, color=PALETTE["text_light"], va="center")
        legend_x += 2

    # DSA stats card
    stats_x = 11.5
    card = mpatches.FancyBboxPatch(
        (stats_x, 0.3), 3.8, 4.5,
        boxstyle="round,pad=0.2,rounding_size=0.3",
        facecolor=PALETTE["card_bg"],
        edgecolor=PALETTE["card_border"],
        linewidth=1,
    )
    ax.add_patch(card)

    ax.text(stats_x + 1.9, 4.3, "DSA", fontsize=9, fontweight="bold", ha="center", color=PALETTE["dsa"])

    fire_color = PALETTE["active"] if dsa_current >= 3 else PALETTE["text_muted"]
    ax.text(stats_x + 1.9, 3.5, f"{dsa_current}", fontsize=16, fontweight="bold", ha="center", va="center", color=fire_color)
    ax.text(stats_x + 1.9, 3.0, "current", fontsize=7, ha="center", va="center", color=PALETTE["text_light"])

    ax.text(stats_x + 1.9, 2.2, f"{dsa_longest}", fontsize=14, fontweight="bold", ha="center", va="center", color=PALETTE["text_muted"])
    ax.text(stats_x + 1.9, 1.8, "best", fontsize=7, ha="center", va="center", color=PALETTE["text_light"])

    ax.text(stats_x + 1.9, 1.0, f"{dsa_total} days", fontsize=8, ha="center", va="center", color=PALETTE["text"])

    # Study stats card
    stats_x2 = 15.8
    card2 = mpatches.FancyBboxPatch(
        (stats_x2, 0.3), 3.8, 4.5,
        boxstyle="round,pad=0.2,rounding_size=0.3",
        facecolor=PALETTE["card_bg"],
        edgecolor=PALETTE["card_border"],
        linewidth=1,
    )
    ax.add_patch(card2)

    ax.text(stats_x2 + 1.9, 4.3, "Study", fontsize=9, fontweight="bold", ha="center", color=PALETTE["study"])

    fire_color2 = PALETTE["active"] if study_current >= 3 else PALETTE["text_muted"]
    ax.text(stats_x2 + 1.9, 3.5, f"{study_current}", fontsize=16, fontweight="bold", ha="center", va="center", color=fire_color2)
    ax.text(stats_x2 + 1.9, 3.0, "current", fontsize=7, ha="center", va="center", color=PALETTE["text_light"])

    ax.text(stats_x2 + 1.9, 2.2, f"{study_longest}", fontsize=14, fontweight="bold", ha="center", va="center", color=PALETTE["text_muted"])
    ax.text(stats_x2 + 1.9, 1.8, "best", fontsize=7, ha="center", va="center", color=PALETTE["text_light"])

    ax.text(stats_x2 + 1.9, 1.0, f"{study_total} days", fontsize=8, ha="center", va="center", color=PALETTE["text"])

    ax.set_xlim(-0.5, 20)
    ax.set_ylim(-1, 6)


def generate_progress_chart(repo_root: Path, output_path: Path, year: int = DEFAULT_YEAR) -> None:
    conn = get_db(repo_root)

    topics = get_topic_progress_from_db(conn, "python")
    db_dates = get_activity_dates_from_db(conn)

    # Get study data
    study_data = get_study_data_for_chart(conn)
    study_dates = get_study_activity_dates(conn)

    conn.close()

    git_dates = get_commit_dates(repo_root)
    dsa_dates = db_dates | git_dates

    in_progress, not_started = categorize_topics(topics)
    not_started_count = len(not_started)

    total_exercises = sum(t["total"] for t in topics.values())
    total_done = sum(t["python"] for t in topics.values())

    dsa_current, dsa_longest, dsa_total = calculate_streaks(dsa_dates, year)
    study_current, study_longest, study_total = calculate_streaks(study_dates, year)

    # Check if we have active study items (with actual progress)
    active_books = [b for b in study_data["books"] if (b[3] or 0) > 0]  # chapters_completed > 0
    active_courses = [c for c in study_data["courses"] if (c[4] or 0) > 0]  # has lectures
    has_study = bool(active_books or active_courses or study_data["papers_total"])

    num_topics = len(in_progress) if in_progress else 1
    num_study_items = len(active_books) + len(active_courses) + (1 if study_data["papers_total"] else 0)
    study_height = max(2, num_study_items * 0.5 + 1.5) if has_study else 0

    fig_height = max(10, 3 + num_topics * 0.6 + 1.5 + study_height + 4.5 + 0.5)

    fig = plt.figure(figsize=(12, fig_height))
    fig.patch.set_facecolor("white")

    if has_study:
        gs = fig.add_gridspec(5, 1, height_ratios=[3, num_topics * 0.6 + 1.5, study_height, 4.5, 0.5], hspace=0.15)
        ax_hero = fig.add_subplot(gs[0])
        ax_topics = fig.add_subplot(gs[1])
        ax_study = fig.add_subplot(gs[2])
        ax_calendar = fig.add_subplot(gs[3])
        ax_footer = fig.add_subplot(gs[4])
    else:
        gs = fig.add_gridspec(4, 1, height_ratios=[3, num_topics * 0.6 + 1.5, 4, 0.5], hspace=0.15)
        ax_hero = fig.add_subplot(gs[0])
        ax_topics = fig.add_subplot(gs[1])
        ax_calendar = fig.add_subplot(gs[2])
        ax_footer = fig.add_subplot(gs[3])

    draw_hero_section(ax_hero, total_done, total_exercises, dsa_current)
    draw_topic_progress(ax_topics, in_progress, not_started_count)

    if has_study:
        draw_study_progress(ax_study, study_data)
        draw_combined_streak(ax_calendar, dsa_dates, study_dates, year,
                            dsa_current, dsa_longest, dsa_total,
                            study_current, study_longest, study_total)
    else:
        draw_learning_streak(ax_calendar, dsa_dates, year, dsa_current, dsa_longest, dsa_total)

    ax_footer.set_facecolor("white")
    ax_footer.axis("off")
    timestamp = format_timestamp()
    ax_footer.text(
        0.5, 0.7, f"Last updated: {timestamp}",
        ha="center", va="center", fontsize=9,
        color=PALETTE["text_light"], style="italic", transform=ax_footer.transAxes
    )
    ax_footer.text(
        0.5, 0.2, "github.com/stonecharioteer/interview-prep",
        ha="center", va="center", fontsize=8,
        color=PALETTE["text_light"], transform=ax_footer.transAxes
    )

    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white", edgecolor="none", pad_inches=0.15)
    plt.close(fig)


# ============ CLI Commands ============


@app.command()
def init(
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing database")] = False,
):
    """Initialize database from README and git history."""
    repo_root = get_repo_root()
    db_path = repo_root / DB_FILE

    if db_path.exists() and not force:
        if not typer.confirm(f"{DB_FILE} exists. Overwrite?"):
            console.print("[dim]Aborted.[/dim]")
            raise typer.Exit()
        db_path.unlink()

    console.print("[cyan]Parsing README...[/cyan]")
    exercises = parse_readme(repo_root / "README.md")
    console.print(f"[green]Found {len(exercises)} exercises[/green]")

    console.print("[cyan]Scanning git history...[/cyan]")
    git_dates = get_solved_dates_from_git(repo_root)

    conn = get_db(repo_root)
    today = datetime.now().strftime("%Y-%m-%d")

    for ex in exercises:
        conn.execute(
            "INSERT INTO exercises (id, topic, name) VALUES (?, ?, ?)",
            [ex["id"], ex["topic"], ex["name"]],
        )

        for lang in Language:
            lang_key = lang.value
            if ex["readme_status"].get(lang_key, False):
                date = match_exercise_to_file(ex, git_dates.get(lang_key, {})) or today
                conn.execute(
                    "INSERT INTO progress (exercise_id, language, status, date) VALUES (?, ?, ?, ?)",
                    [ex["id"], lang_key, "solved", date],
                )
            else:
                conn.execute(
                    "INSERT INTO progress (exercise_id, language, status) VALUES (?, ?, ?)",
                    [ex["id"], lang_key, "not_started"],
                )

    conn.close()
    console.print(f"[green]Created {DB_FILE} with {len(exercises)} exercises[/green]")
    show_summary(repo_root)


@app.command()
def mark(
    exercise_id: Annotated[int, typer.Argument(help="Exercise ID to mark")],
    lang: Annotated[Language, typer.Argument(help="Language")],
    status: Annotated[Status, typer.Argument(help="New status")] = Status.solved,
):
    """Mark an exercise with a status."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    result = conn.execute("SELECT name FROM exercises WHERE id = ?", [exercise_id]).fetchone()
    if not result:
        console.print(f"[red]Exercise {exercise_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    name = result[0]

    old = conn.execute(
        "SELECT status FROM progress WHERE exercise_id = ? AND language = ?",
        [exercise_id, lang.value],
    ).fetchone()
    old_status = old[0] if old else "not_started"

    date = datetime.now().strftime("%Y-%m-%d") if status != Status.not_started else None
    conn.execute(
        """INSERT OR REPLACE INTO progress (exercise_id, language, status, date)
           VALUES (?, ?, ?, ?)""",
        [exercise_id, lang.value, status.value, date],
    )
    conn.close()

    status_colors = {"not_started": "dim", "attempted": "yellow", "solved": "green"}
    console.print(
        f"[{status_colors[old_status]}]{old_status}[/] → "
        f"[{status_colors[status.value]}]{status.value}[/] : "
        f"[cyan]#{exercise_id}[/cyan] {name} ({lang.value})"
    )


@app.command("list")
def list_exercises(
    topic: Annotated[Optional[str], typer.Option("--topic", "-t", help="Filter by topic")] = None,
    lang: Annotated[Optional[Language], typer.Option("--lang", "-l", help="Filter by language")] = None,
    status: Annotated[Optional[Status], typer.Option("--status", "-s", help="Filter by status")] = None,
):
    """List exercises with optional filters."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    query = """
        SELECT
            e.id,
            ANY_VALUE(e.topic) as topic,
            ANY_VALUE(e.name) as name,
            MAX(CASE WHEN p.language = 'python' THEN p.status END) as python,
            MAX(CASE WHEN p.language = 'rust' THEN p.status END) as rust,
            MAX(CASE WHEN p.language = 'typescript' THEN p.status END) as typescript
        FROM exercises e
        LEFT JOIN progress p ON e.id = p.exercise_id
    """

    conditions = []
    params = []

    if topic:
        conditions.append("LOWER(e.topic) LIKE ?")
        params.append(f"%{topic.lower()}%")

    if lang and status:
        conditions.append(
            "EXISTS (SELECT 1 FROM progress p2 WHERE p2.exercise_id = e.id AND p2.language = ? AND p2.status = ?)"
        )
        params.extend([lang.value, status.value])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY e.id ORDER BY e.id"
    results = conn.execute(query, params).fetchall()
    conn.close()

    if not results:
        console.print("[yellow]No exercises found.[/yellow]")
        return

    table = Table(title="Exercise Progress")
    table.add_column("#", style="dim", width=4)
    table.add_column("Topic", style="cyan", width=15)
    table.add_column("Exercise", width=40)
    table.add_column("🐍", justify="center", width=4)
    table.add_column("🦀", justify="center", width=4)
    table.add_column("🟨", justify="center", width=4)

    for row in results:
        ex_id, topic_name, name, py, rs, ts = row
        table.add_row(
            str(ex_id),
            topic_name,
            name,
            STATUS_SYMBOL.get(py, STATUS_SYMBOL["not_started"]),
            STATUS_SYMBOL.get(rs, STATUS_SYMBOL["not_started"]),
            STATUS_SYMBOL.get(ts, STATUS_SYMBOL["not_started"]),
        )

    console.print(table)
    show_summary(get_repo_root())


@app.command("next")
def next_exercises(
    lang: Annotated[Language, typer.Argument(help="Language to check")] = Language.python,
    count: Annotated[int, typer.Option("--count", "-n", help="Number to show")] = 10,
):
    """Show next unsolved exercises for a language."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    results = conn.execute(
        """
        SELECT e.id, e.topic, e.name
        FROM exercises e
        JOIN progress p ON e.id = p.exercise_id AND p.language = ?
        WHERE p.status = 'not_started'
        ORDER BY e.id
        LIMIT ?
        """,
        [lang.value, count],
    ).fetchall()
    conn.close()

    if not results:
        console.print(f"[green]All done![/green] No unsolved {lang.value} exercises remaining.")
        return

    emoji = LANG_EMOJI[lang.value]
    table = Table(title=f"{emoji} Next {len(results)} unsolved exercises")
    table.add_column("#", style="dim", width=4)
    table.add_column("Topic", style="cyan")
    table.add_column("Exercise", style="white")

    for ex_id, topic, name in results:
        table.add_row(str(ex_id), topic, name)

    console.print(table)


@app.command()
def exercises():
    """Update exercises.md with current progress from database."""
    repo_root = get_repo_root()
    db_path = repo_root / DB_FILE

    if not db_path.exists():
        console.print("[yellow]No database found. Run 'init' first.[/yellow]")
        raise typer.Exit(1)

    update_exercises_file(repo_root)


@app.command()
def plot():
    """Generate progress.png visualization."""
    repo_root = get_repo_root()
    db_path = repo_root / DB_FILE

    if not db_path.exists():
        console.print("[yellow]No database found. Run 'init' first.[/yellow]")
        raise typer.Exit(1)

    os.chdir(repo_root)
    output_path = repo_root / "progress.png"

    console.print("[cyan]Generating progress chart...[/cyan]")
    generate_progress_chart(repo_root, output_path)

    conn = get_db(repo_root)
    topics = get_topic_progress_from_db(conn, "python")
    db_dates = get_activity_dates_from_db(conn)
    git_dates = get_commit_dates(repo_root)
    conn.close()

    total = sum(t["total"] for t in topics.values())
    py = sum(t["python"] for t in topics.values())
    current, longest, days = calculate_streaks(db_dates | git_dates, DEFAULT_YEAR)

    console.print(f"[green]Generated {output_path}[/green]")
    console.print(f"  Progress: {py}/{total} ({100 * py // total if total else 0}%)")
    console.print(f"  Streak: {current} current, {longest} best, {days} total days")


@app.command()
def sync():
    """Update both exercises.md and progress.png from database."""
    repo_root = get_repo_root()
    db_path = repo_root / DB_FILE

    if not db_path.exists():
        console.print("[yellow]No database found. Run 'init' first.[/yellow]")
        raise typer.Exit(1)

    update_exercises_file(repo_root)

    os.chdir(repo_root)
    output_path = repo_root / "progress.png"
    console.print("[cyan]Generating progress chart...[/cyan]")
    generate_progress_chart(repo_root, output_path)
    console.print(f"[green]Generated {output_path}[/green]")

    show_summary(repo_root)


@app.command()
def cheatsheet():
    """Show quick reference for common commands."""
    cheat = """
[bold]Progress CLI Cheatsheet[/bold]

[cyan]DSA Exercises[/cyan]
  progress                      Show DSA summary
  progress mark ID LANG STATUS  Mark exercise (solved/attempted/not_started)
  progress next LANG            Next 10 unsolved exercises
  progress list [--topic X]     List exercises with optional filters

[cyan]Study Tracking[/cyan]
  progress study                Show study summary
  progress study book-add TITLE [--author X] [--chapters N]
  progress study book-read ID --chapter N [--progress PCT]
  progress study book-read ID --chapters "1-3"
  progress study book-list
  progress study course-add NAME [--source CMU] [--code 15-445]
  progress study lecture-add COURSE_ID TITLE [--number N]
  progress study watch COURSE_ID LECTURE_NUM
  progress study course-show ID
  progress study paper-add TITLE [--authors X] [--year N]
  progress study paper-read ID
  progress study recent [--days 7]

[cyan]Associations[/cyan]
  progress study course-book COURSE_ID BOOK_ID
  progress study course-paper COURSE_ID PAPER_ID
  progress study lecture-chapters LECTURE_ID BOOK_ID "1-3"

[cyan]Output Files[/cyan]
  progress sync                 Update exercises.md + progress.png
  progress plot                 Update progress.png only

[dim]Languages: python | rust | typescript
Statuses: not_started | attempted | solved[/dim]
"""
    console.print(cheat)


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """Show summary if no command given."""
    if ctx.invoked_subcommand is None:
        repo_root = get_repo_root()
        db_path = repo_root / DB_FILE

        if db_path.exists():
            show_summary(repo_root)
        else:
            console.print("[yellow]No database found. Run 'progress init' to create one.[/yellow]")


# ============ Study Commands ============

STUDY_STATUS_SYMBOL = {
    "not_started": "[dim]·[/]",
    "in_progress": "[yellow]○[/]",
    "reading": "[yellow]○[/]",
    "watching": "[yellow]○[/]",
    "completed": "[green]✓[/]",
}


# ============ Book Commands ============


@study_app.command("book-add")
def book_add(
    title: Annotated[str, typer.Argument(help="Book title")],
    author: Annotated[Optional[str], typer.Option("--author", "-a", help="Author name")] = None,
    chapters: Annotated[Optional[int], typer.Option("--chapters", "-c", help="Total chapters")] = None,
    url: Annotated[Optional[str], typer.Option("--url", help="Book URL")] = None,
):
    """Add a book to track."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM books").fetchone()
    new_id = result[0]

    conn.execute(
        "INSERT INTO books (id, title, author, total_chapters, url) VALUES (?, ?, ?, ?, ?)",
        [new_id, title, author, chapters, url],
    )
    conn.close()

    console.print(f"[green]Added book #{new_id}:[/green] {title}")
    if author:
        console.print(f"  Author: {author}")
    if chapters:
        console.print(f"  Chapters: {chapters}")


@study_app.command("book-read")
def book_read(
    book_id: Annotated[int, typer.Argument(help="Book ID")],
    chapter: Annotated[Optional[int], typer.Option("--chapter", "-c", help="Single chapter number")] = None,
    chapters: Annotated[Optional[str], typer.Option("--chapters", help="Chapter range (e.g., '1-3' or '5,7')")] = None,
    progress: Annotated[int, typer.Option("--progress", "-p", help="Progress percentage (default: 100)")] = 100,
    date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
):
    """Mark chapter(s) as read with optional progress percentage."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    book = conn.execute("SELECT title, total_chapters FROM books WHERE id = ?", [book_id]).fetchone()
    if not book:
        console.print(f"[red]Book #{book_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    book_title, total_chapters = book

    if not chapter and not chapters:
        console.print("[red]Must specify --chapter or --chapters[/red]")
        conn.close()
        raise typer.Exit(1)

    # Parse chapters to update
    chapter_nums = set()
    if chapter:
        chapter_nums.add(chapter)
    if chapters:
        chapter_nums.update(parse_chapters_string(chapters))

    if not chapter_nums:
        console.print("[red]No valid chapters specified[/red]")
        conn.close()
        raise typer.Exit(1)

    # Validate chapter numbers if total_chapters is set
    if total_chapters:
        invalid = [c for c in chapter_nums if c < 1 or c > total_chapters]
        if invalid:
            console.print(f"[red]Invalid chapters {invalid} (book has {total_chapters} chapters)[/red]")
            conn.close()
            raise typer.Exit(1)

    progress = max(0, min(100, progress))  # Clamp to 0-100
    update_date = date or datetime.now().strftime("%Y-%m-%d")

    for ch in sorted(chapter_nums):
        conn.execute("""
            INSERT OR REPLACE INTO chapter_progress (book_id, chapter_number, progress_pct, updated_date)
            VALUES (?, ?, ?, ?)
        """, [book_id, ch, progress, update_date])

    conn.close()

    if len(chapter_nums) == 1:
        ch = list(chapter_nums)[0]
        console.print(f"[green]Updated:[/green] Chapter {ch} of \"{book_title}\" → {progress}%")
    else:
        ch_list = ", ".join(str(c) for c in sorted(chapter_nums))
        console.print(f"[green]Updated:[/green] Chapters {ch_list} of \"{book_title}\" → {progress}%")


@study_app.command("book-list")
def book_list(
    status: Annotated[Optional[StudyStatus], typer.Option("--status", "-s", help="Filter by status")] = None,
):
    """List tracked books with progress."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    books = conn.execute("""
        SELECT
            b.id, b.title, b.author, b.total_chapters,
            COUNT(cp.chapter_number) as chapters_started,
            SUM(CASE WHEN cp.progress_pct = 100 THEN 1 ELSE 0 END) as chapters_done,
            MAX(cp.updated_date) as last_read
        FROM books b
        LEFT JOIN chapter_progress cp ON b.id = cp.book_id
        GROUP BY b.id, b.title, b.author, b.total_chapters
        ORDER BY last_read DESC NULLS LAST, b.id
    """).fetchall()
    conn.close()

    if not books:
        console.print("[yellow]No books tracked yet. Use 'progress study book-add' to add one.[/yellow]")
        return

    table = Table(title="Books")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", width=35)
    table.add_column("Author", width=20)
    table.add_column("Progress", justify="right", width=12)
    table.add_column("Last Read", width=12)

    for book_id, title, author, total_chapters, chapters_started, chapters_done, last_read in books:
        chapters_started = chapters_started or 0
        chapters_done = chapters_done or 0

        # Determine status
        if chapters_started == 0:
            book_status = "not_started"
        elif total_chapters and chapters_done >= total_chapters:
            book_status = "completed"
        else:
            book_status = "in_progress"

        if status and status.value != book_status:
            continue

        # Format progress
        if total_chapters:
            progress_str = f"{chapters_done}/{total_chapters}"
        elif chapters_done > 0:
            progress_str = f"{chapters_done} ch"
        else:
            progress_str = "-"

        last_read_str = str(last_read) if last_read else "-"

        table.add_row(
            str(book_id),
            title,
            author or "-",
            progress_str,
            last_read_str,
        )

    console.print(table)


@study_app.command("book-show")
def book_show(
    book_id: Annotated[int, typer.Argument(help="Book ID")],
):
    """Show book details and chapter progress."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    book = conn.execute(
        "SELECT id, title, author, total_chapters, url FROM books WHERE id = ?",
        [book_id],
    ).fetchone()

    if not book:
        console.print(f"[red]Book #{book_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    _, title, author, total_chapters, url = book

    # Get chapter progress
    chapter_progress = conn.execute("""
        SELECT chapter_number, progress_pct, updated_date
        FROM chapter_progress
        WHERE book_id = ?
        ORDER BY chapter_number
    """, [book_id]).fetchall()

    conn.close()

    # Calculate overall progress
    if total_chapters and total_chapters > 0:
        progress_map = {cp[0]: cp[1] for cp in chapter_progress}
        total_progress = sum(progress_map.get(i, 0) for i in range(1, total_chapters + 1))
        overall_pct = total_progress // total_chapters
        chapters_done = sum(1 for cp in chapter_progress if cp[1] == 100)
    else:
        overall_pct = None
        chapters_done = sum(1 for cp in chapter_progress if cp[1] == 100)

    console.print()
    console.print(f"[bold]{title}[/bold]")
    if author:
        console.print(f"  Author: {author}")
    if total_chapters:
        console.print(f"  Chapters: {chapters_done}/{total_chapters} complete ({overall_pct}%)")
    elif chapters_done:
        console.print(f"  Chapters completed: {chapters_done}")
    if url:
        console.print(f"  URL: {url}")

    if chapter_progress:
        console.print()
        console.print("[cyan]Chapter Progress:[/cyan]")
        table = Table(show_header=True)
        table.add_column("Ch", width=4, justify="right")
        table.add_column("Progress", width=10)
        table.add_column("Updated", width=12)

        for ch_num, pct, updated in chapter_progress:
            if pct == 100:
                progress_str = "[green]100%[/green]"
            elif pct > 0:
                progress_str = f"[yellow]{pct}%[/yellow]"
            else:
                progress_str = "[dim]0%[/dim]"
            date_str = str(updated) if updated else "-"
            table.add_row(str(ch_num), progress_str, date_str)

        console.print(table)
    else:
        console.print("\n[dim]No chapters tracked yet.[/dim]")


# ============ Course Commands ============


@study_app.command("course-add")
def course_add(
    name: Annotated[str, typer.Argument(help="Course name")],
    source: Annotated[Optional[str], typer.Option("--source", "-s", help="Source (e.g., CMU, MIT)")] = None,
    code: Annotated[Optional[str], typer.Option("--code", "-c", help="Course code (e.g., 15-445)")] = None,
    url: Annotated[Optional[str], typer.Option("--url", help="Playlist URL")] = None,
):
    """Add a course to track."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM courses").fetchone()
    new_id = result[0]

    conn.execute(
        "INSERT INTO courses (id, name, source, code, playlist_url) VALUES (?, ?, ?, ?, ?)",
        [new_id, name, source, code, url],
    )
    conn.close()

    display_name = ""
    if source:
        display_name += f"{source} "
    if code:
        display_name += f"{code} "
    display_name += name

    console.print(f"[green]Added course #{new_id}:[/green] {display_name}")


@study_app.command("lecture-add")
def lecture_add(
    course_id: Annotated[int, typer.Argument(help="Course ID")],
    title: Annotated[str, typer.Argument(help="Lecture title")],
    number: Annotated[Optional[int], typer.Option("--number", "-n", help="Lecture number (auto-increments if not provided)")] = None,
    url: Annotated[Optional[str], typer.Option("--url", help="Video URL")] = None,
):
    """Add a lecture to a course."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
    if not course:
        console.print(f"[red]Course #{course_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    if number is None:
        result = conn.execute(
            "SELECT COALESCE(MAX(lecture_number), 0) + 1 FROM lectures WHERE course_id = ?",
            [course_id],
        ).fetchone()
        number = result[0]

    result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM lectures").fetchone()
    new_id = result[0]

    conn.execute(
        "INSERT INTO lectures (id, course_id, lecture_number, title, url) VALUES (?, ?, ?, ?, ?)",
        [new_id, course_id, number, title, url],
    )
    conn.close()

    console.print(f"[green]Added lecture #{number}:[/green] {title} (to {course[0]})")


@study_app.command("watch")
def watch_lecture(
    course_id: Annotated[int, typer.Argument(help="Course ID")],
    lecture_number: Annotated[int, typer.Argument(help="Lecture number")],
    status: Annotated[StudyStatus, typer.Option("--status", "-s", help="Status")] = StudyStatus.completed,
    date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
):
    """Mark a lecture as watched."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    lecture = conn.execute("""
        SELECT l.id, l.title, c.name
        FROM lectures l
        JOIN courses c ON l.course_id = c.id
        WHERE l.course_id = ? AND l.lecture_number = ?
    """, [course_id, lecture_number]).fetchone()

    if not lecture:
        console.print(f"[red]Lecture #{lecture_number} not found in course #{course_id}[/red]")
        conn.close()
        raise typer.Exit(1)

    lecture_id, lecture_title, course_name = lecture
    watch_date = date or datetime.now().strftime("%Y-%m-%d")

    # Use status value, mapping in_progress to watching for lectures
    status_value = "watching" if status == StudyStatus.in_progress else status.value

    conn.execute("""
        INSERT OR REPLACE INTO lecture_progress (lecture_id, date, status)
        VALUES (?, ?, ?)
    """, [lecture_id, watch_date, status_value])
    conn.close()

    status_word = "Completed" if status == StudyStatus.completed else "Watching"
    console.print(f"[green]{status_word}:[/green] Lecture {lecture_number} \"{lecture_title}\" of {course_name}")


@study_app.command("course-list")
def course_list(
    status: Annotated[Optional[StudyStatus], typer.Option("--status", "-s", help="Filter by status")] = None,
):
    """List tracked courses with progress."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    courses = conn.execute("""
        SELECT
            c.id, c.name, c.source, c.code,
            COUNT(l.id) as total_lectures,
            SUM(CASE WHEN lp.status = 'completed' THEN 1 ELSE 0 END) as completed,
            MAX(lp.date) as last_watched
        FROM courses c
        LEFT JOIN lectures l ON c.id = l.course_id
        LEFT JOIN lecture_progress lp ON l.id = lp.lecture_id
        GROUP BY c.id
        ORDER BY last_watched DESC NULLS LAST, c.id
    """).fetchall()
    conn.close()

    if not courses:
        console.print("[yellow]No courses tracked yet. Use 'progress study course-add' to add one.[/yellow]")
        return

    table = Table(title="Courses")
    table.add_column("#", style="dim", width=4)
    table.add_column("Course", width=40)
    table.add_column("Progress", justify="right", width=12)
    table.add_column("Last Watched", width=12)

    for course_id, name, source, code, total, completed, last_watched in courses:
        completed = completed or 0
        total = total or 0

        course_status = "not_started"
        if completed > 0 and completed >= total and total > 0:
            course_status = "completed"
        elif completed > 0:
            course_status = "in_progress"

        if status and status.value != course_status:
            continue

        display_name = ""
        if source:
            display_name += f"{source} "
        if code:
            display_name += f"{code} "
        display_name += name

        progress_str = f"{completed}/{total}" if total > 0 else "0 lectures"
        if total > 0:
            pct = int(100 * completed / total)
            progress_str += f" ({pct}%)"

        table.add_row(
            str(course_id),
            display_name,
            progress_str,
            last_watched or "-",
        )

    console.print(table)


@study_app.command("course-show")
def course_show(
    course_id: Annotated[int, typer.Argument(help="Course ID")],
):
    """Show course details with lecture progress."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    course = conn.execute(
        "SELECT id, name, source, code, playlist_url FROM courses WHERE id = ?",
        [course_id],
    ).fetchone()

    if not course:
        console.print(f"[red]Course #{course_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    _, name, source, code, playlist_url = course

    display_name = ""
    if source:
        display_name += f"{source} "
    if code:
        display_name += f"{code} "
    display_name += name

    console.print()
    console.print(f"[bold]{display_name}[/bold]")
    if playlist_url:
        console.print(f"  URL: {playlist_url}")

    # Get lectures with progress
    lectures = conn.execute("""
        SELECT l.lecture_number, l.title, l.url, lp.status, lp.date
        FROM lectures l
        LEFT JOIN lecture_progress lp ON l.id = lp.lecture_id
        WHERE l.course_id = ?
        ORDER BY l.lecture_number
    """, [course_id]).fetchall()

    if lectures:
        console.print()
        console.print("[cyan]Lectures:[/cyan]")
        table = Table(show_header=True)
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", width=50)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Date", width=12)

        for num, title, url, status, date in lectures:
            status_sym = STUDY_STATUS_SYMBOL.get(status or "not_started", STUDY_STATUS_SYMBOL["not_started"])
            date_str = str(date) if date else "-"
            table.add_row(str(num), title, status_sym, date_str)

        console.print(table)

        completed = sum(1 for l in lectures if l[3] == "completed")
        total = len(lectures)
        pct = int(100 * completed / total) if total > 0 else 0
        console.print(f"\n  Progress: {completed}/{total} ({pct}%)")
    else:
        console.print("\n[dim]No lectures added yet.[/dim]")

    # Get projects
    projects = conn.execute("""
        SELECT p.id, p.name, pp.status, pp.date
        FROM projects p
        LEFT JOIN project_progress pp ON p.id = pp.project_id
        WHERE p.course_id = ?
        ORDER BY p.id
    """, [course_id]).fetchall()

    if projects:
        console.print()
        console.print("[cyan]Projects:[/cyan]")
        for proj_id, proj_name, status, date in projects:
            status_sym = STUDY_STATUS_SYMBOL.get(status or "not_started", STUDY_STATUS_SYMBOL["not_started"])
            date_str = f" ({date})" if date else ""
            console.print(f"  {status_sym} #{proj_id} {proj_name}{date_str}")

    # Get required books
    books = conn.execute("""
        SELECT b.id, b.title, b.author
        FROM course_books cb
        JOIN books b ON cb.book_id = b.id
        WHERE cb.course_id = ?
    """, [course_id]).fetchall()

    if books:
        console.print()
        console.print("[cyan]Required Books:[/cyan]")
        for book_id, title, author in books:
            author_str = f" by {author}" if author else ""
            console.print(f"  #{book_id} {title}{author_str}")

    # Get required papers
    papers = conn.execute("""
        SELECT p.id, p.title, p.authors
        FROM course_papers cp
        JOIN papers p ON cp.paper_id = p.id
        WHERE cp.course_id = ?
    """, [course_id]).fetchall()

    if papers:
        console.print()
        console.print("[cyan]Required Papers:[/cyan]")
        for paper_id, title, authors in papers:
            authors_str = f" ({authors})" if authors else ""
            console.print(f"  #{paper_id} {title}{authors_str}")

    conn.close()


# ============ Homework & Project Commands ============


@study_app.command("homework-add")
def homework_add(
    lecture_id: Annotated[int, typer.Argument(help="Lecture ID")],
    name: Annotated[str, typer.Argument(help="Homework name")],
    url: Annotated[Optional[str], typer.Option("--url", help="Homework URL")] = None,
):
    """Add homework to a lecture."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    lecture = conn.execute("""
        SELECT l.title, c.name
        FROM lectures l
        JOIN courses c ON l.course_id = c.id
        WHERE l.id = ?
    """, [lecture_id]).fetchone()

    if not lecture:
        console.print(f"[red]Lecture #{lecture_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM homework").fetchone()
    new_id = result[0]

    conn.execute(
        "INSERT INTO homework (id, lecture_id, name, url) VALUES (?, ?, ?, ?)",
        [new_id, lecture_id, name, url],
    )
    conn.close()

    console.print(f"[green]Added homework #{new_id}:[/green] {name}")
    console.print(f"  For: {lecture[0]} ({lecture[1]})")


@study_app.command("homework-done")
def homework_done(
    homework_id: Annotated[int, typer.Argument(help="Homework ID")],
    date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
):
    """Mark homework as completed."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    hw = conn.execute("SELECT name FROM homework WHERE id = ?", [homework_id]).fetchone()
    if not hw:
        console.print(f"[red]Homework #{homework_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    done_date = date or datetime.now().strftime("%Y-%m-%d")

    conn.execute("""
        INSERT OR REPLACE INTO homework_progress (homework_id, date, status)
        VALUES (?, ?, 'completed')
    """, [homework_id, done_date])
    conn.close()

    console.print(f"[green]Completed:[/green] {hw[0]}")


@study_app.command("project-add")
def project_add(
    course_id: Annotated[int, typer.Argument(help="Course ID")],
    name: Annotated[str, typer.Argument(help="Project name")],
    url: Annotated[Optional[str], typer.Option("--url", help="Project URL")] = None,
):
    """Add a project to a course."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
    if not course:
        console.print(f"[red]Course #{course_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM projects").fetchone()
    new_id = result[0]

    conn.execute(
        "INSERT INTO projects (id, course_id, name, url) VALUES (?, ?, ?, ?)",
        [new_id, course_id, name, url],
    )
    conn.close()

    console.print(f"[green]Added project #{new_id}:[/green] {name}")
    console.print(f"  For: {course[0]}")


@study_app.command("project-done")
def project_done(
    project_id: Annotated[int, typer.Argument(help="Project ID")],
    date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
):
    """Mark project as completed."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    proj = conn.execute("SELECT name FROM projects WHERE id = ?", [project_id]).fetchone()
    if not proj:
        console.print(f"[red]Project #{project_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    done_date = date or datetime.now().strftime("%Y-%m-%d")

    conn.execute("""
        INSERT OR REPLACE INTO project_progress (project_id, date, status)
        VALUES (?, ?, 'completed')
    """, [project_id, done_date])
    conn.close()

    console.print(f"[green]Completed:[/green] {proj[0]}")


# ============ Paper Commands ============


@study_app.command("paper-add")
def paper_add(
    title: Annotated[str, typer.Argument(help="Paper title")],
    authors: Annotated[Optional[str], typer.Option("--authors", "-a", help="Authors")] = None,
    url: Annotated[Optional[str], typer.Option("--url", help="Paper URL")] = None,
    year: Annotated[Optional[int], typer.Option("--year", "-y", help="Publication year")] = None,
):
    """Add a paper to track."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM papers").fetchone()
    new_id = result[0]

    conn.execute(
        "INSERT INTO papers (id, title, authors, url, year) VALUES (?, ?, ?, ?, ?)",
        [new_id, title, authors, url, year],
    )
    conn.close()

    console.print(f"[green]Added paper #{new_id}:[/green] {title}")
    if authors:
        console.print(f"  Authors: {authors}")
    if year:
        console.print(f"  Year: {year}")


@study_app.command("paper-read")
def paper_read(
    paper_id: Annotated[int, typer.Argument(help="Paper ID")],
    status: Annotated[StudyStatus, typer.Option("--status", "-s", help="Status")] = StudyStatus.completed,
    date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
):
    """Mark a paper as reading or completed."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    paper = conn.execute("SELECT title FROM papers WHERE id = ?", [paper_id]).fetchone()
    if not paper:
        console.print(f"[red]Paper #{paper_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    read_date = date or datetime.now().strftime("%Y-%m-%d")

    # Map in_progress to reading for papers
    status_value = "reading" if status == StudyStatus.in_progress else status.value

    conn.execute("""
        INSERT OR REPLACE INTO paper_progress (paper_id, date, status)
        VALUES (?, ?, ?)
    """, [paper_id, read_date, status_value])
    conn.close()

    status_word = "Completed" if status == StudyStatus.completed else "Reading"
    console.print(f"[green]{status_word}:[/green] {paper[0]}")


@study_app.command("paper-list")
def paper_list(
    status: Annotated[Optional[StudyStatus], typer.Option("--status", "-s", help="Filter by status")] = None,
):
    """List tracked papers with progress."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    papers = conn.execute("""
        SELECT
            p.id, p.title, p.authors, p.year,
            pp.status, pp.date
        FROM papers p
        LEFT JOIN paper_progress pp ON p.id = pp.paper_id
        ORDER BY pp.date DESC NULLS LAST, p.id
    """).fetchall()
    conn.close()

    if not papers:
        console.print("[yellow]No papers tracked yet. Use 'progress study paper-add' to add one.[/yellow]")
        return

    table = Table(title="Papers")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", width=40)
    table.add_column("Authors", width=20)
    table.add_column("Year", width=6)
    table.add_column("Status", justify="center", width=8)

    for paper_id, title, authors, year, paper_status, date in papers:
        paper_status = paper_status or "not_started"

        # Map status for filtering
        filter_status = paper_status
        if paper_status == "reading":
            filter_status = "in_progress"

        if status and status.value != filter_status:
            continue

        status_sym = STUDY_STATUS_SYMBOL.get(paper_status, STUDY_STATUS_SYMBOL["not_started"])

        table.add_row(
            str(paper_id),
            title,
            authors or "-",
            str(year) if year else "-",
            status_sym,
        )

    console.print(table)


# ============ Association Commands ============


@study_app.command("course-book")
def course_book(
    course_id: Annotated[int, typer.Argument(help="Course ID")],
    book_id: Annotated[int, typer.Argument(help="Book ID")],
):
    """Associate a book with a course (required reading)."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
    if not course:
        console.print(f"[red]Course #{course_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    book = conn.execute("SELECT title FROM books WHERE id = ?", [book_id]).fetchone()
    if not book:
        console.print(f"[red]Book #{book_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    conn.execute(
        "INSERT OR IGNORE INTO course_books (course_id, book_id) VALUES (?, ?)",
        [course_id, book_id],
    )
    conn.close()

    console.print(f"[green]Associated:[/green] \"{book[0]}\" with {course[0]}")


@study_app.command("lecture-chapters")
def lecture_chapters(
    lecture_id: Annotated[int, typer.Argument(help="Lecture ID")],
    book_id: Annotated[int, typer.Argument(help="Book ID")],
    chapters: Annotated[str, typer.Argument(help="Chapters (e.g., '1-3' or '5,7')")],
):
    """Associate specific chapters with a lecture."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    lecture = conn.execute("SELECT title FROM lectures WHERE id = ?", [lecture_id]).fetchone()
    if not lecture:
        console.print(f"[red]Lecture #{lecture_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    book = conn.execute("SELECT title FROM books WHERE id = ?", [book_id]).fetchone()
    if not book:
        console.print(f"[red]Book #{book_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    conn.execute("""
        INSERT OR REPLACE INTO lecture_chapters (lecture_id, book_id, chapters)
        VALUES (?, ?, ?)
    """, [lecture_id, book_id, chapters])
    conn.close()

    console.print(f"[green]Associated:[/green] Chapters {chapters} of \"{book[0]}\" with \"{lecture[0]}\"")


@study_app.command("course-paper")
def course_paper(
    course_id: Annotated[int, typer.Argument(help="Course ID")],
    paper_id: Annotated[int, typer.Argument(help="Paper ID")],
):
    """Associate a paper with a course."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
    if not course:
        console.print(f"[red]Course #{course_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    paper = conn.execute("SELECT title FROM papers WHERE id = ?", [paper_id]).fetchone()
    if not paper:
        console.print(f"[red]Paper #{paper_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    conn.execute(
        "INSERT OR IGNORE INTO course_papers (course_id, paper_id) VALUES (?, ?)",
        [course_id, paper_id],
    )
    conn.close()

    console.print(f"[green]Associated:[/green] \"{paper[0]}\" with {course[0]}")


@study_app.command("lecture-paper")
def lecture_paper(
    lecture_id: Annotated[int, typer.Argument(help="Lecture ID")],
    paper_id: Annotated[int, typer.Argument(help="Paper ID")],
):
    """Associate a paper with a lecture."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    lecture = conn.execute("SELECT title FROM lectures WHERE id = ?", [lecture_id]).fetchone()
    if not lecture:
        console.print(f"[red]Lecture #{lecture_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    paper = conn.execute("SELECT title FROM papers WHERE id = ?", [paper_id]).fetchone()
    if not paper:
        console.print(f"[red]Paper #{paper_id} not found[/red]")
        conn.close()
        raise typer.Exit(1)

    conn.execute(
        "INSERT OR IGNORE INTO lecture_papers (lecture_id, paper_id) VALUES (?, ?)",
        [lecture_id, paper_id],
    )
    conn.close()

    console.print(f"[green]Associated:[/green] \"{paper[0]}\" with \"{lecture[0]}\"")


# ============ Study Summary Commands ============


def get_study_activity_dates(conn: duckdb.DuckDBPyConnection) -> set[str]:
    """Get all study activity dates."""
    dates = set()

    # Chapter progress
    results = conn.execute("""
        SELECT DISTINCT CAST(updated_date AS VARCHAR) FROM chapter_progress
        WHERE updated_date IS NOT NULL
    """).fetchall()
    dates.update(row[0] for row in results if row[0])

    # Lecture progress
    results = conn.execute("""
        SELECT DISTINCT CAST(date AS VARCHAR) FROM lecture_progress
        WHERE date IS NOT NULL AND status = 'completed'
    """).fetchall()
    dates.update(row[0] for row in results if row[0])

    # Homework progress
    results = conn.execute("""
        SELECT DISTINCT CAST(date AS VARCHAR) FROM homework_progress
        WHERE date IS NOT NULL AND status = 'completed'
    """).fetchall()
    dates.update(row[0] for row in results if row[0])

    # Project progress
    results = conn.execute("""
        SELECT DISTINCT CAST(date AS VARCHAR) FROM project_progress
        WHERE date IS NOT NULL AND status = 'completed'
    """).fetchall()
    dates.update(row[0] for row in results if row[0])

    # Paper progress
    results = conn.execute("""
        SELECT DISTINCT CAST(date AS VARCHAR) FROM paper_progress
        WHERE date IS NOT NULL AND status = 'completed'
    """).fetchall()
    dates.update(row[0] for row in results if row[0])

    return dates


def show_study_summary(repo_root: Path) -> None:
    """Show study progress summary."""
    conn = get_db(repo_root)

    # Books
    books = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN chapters_started > 0 THEN 1 ELSE 0 END) as in_progress
        FROM (
            SELECT b.id, COUNT(cp.chapter_number) as chapters_started
            FROM books b
            LEFT JOIN chapter_progress cp ON b.id = cp.book_id
            GROUP BY b.id
        )
    """).fetchone()

    # Courses
    courses = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN completed > 0 AND completed < total_lect THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN completed > 0 AND completed >= total_lect AND total_lect > 0 THEN 1 ELSE 0 END) as done
        FROM (
            SELECT
                c.id,
                COUNT(l.id) as total_lect,
                SUM(CASE WHEN lp.status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM courses c
            LEFT JOIN lectures l ON c.id = l.course_id
            LEFT JOIN lecture_progress lp ON l.id = lp.lecture_id
            GROUP BY c.id
        )
    """).fetchone()

    # Papers
    papers = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN pp.status = 'reading' THEN 1 ELSE 0 END) as reading,
            SUM(CASE WHEN pp.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM papers p
        LEFT JOIN paper_progress pp ON p.id = pp.paper_id
    """).fetchone()

    # Study streak
    study_dates = get_study_activity_dates(conn)
    current_streak, longest_streak, total_days = calculate_streaks(study_dates, DEFAULT_YEAR)

    conn.close()

    console.print()
    console.print("[bold]Study Progress[/bold]")

    total_books, in_progress_books = books
    if total_books:
        console.print(f"  Books: {in_progress_books or 0} in progress, {total_books} tracked")

    total_courses, in_progress_courses, done_courses = courses
    if total_courses:
        console.print(f"  Courses: {done_courses or 0} completed, {in_progress_courses or 0} in progress, {total_courses} tracked")

    total_papers, reading_papers, completed_papers = papers
    if total_papers:
        console.print(f"  Papers: {completed_papers or 0} read, {reading_papers or 0} reading, {total_papers} tracked")

    if total_days > 0:
        console.print(f"  Streak: {current_streak} current, {longest_streak} best, {total_days} total days")
    elif total_books or total_courses or total_papers:
        console.print("  [dim]No study activity recorded yet[/dim]")
    else:
        console.print("  [dim]No items tracked yet[/dim]")


@study_app.command("recent")
def study_recent(
    days: Annotated[int, typer.Option("--days", "-d", help="Number of days to show")] = 7,
):
    """Show recent study activity."""
    repo_root = get_repo_root()
    conn = get_db(repo_root)

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    activities = []

    # Chapter progress
    chapter_updates = conn.execute("""
        SELECT cp.updated_date, 'Book' as type, b.title as name,
               cp.chapter_number, cp.progress_pct
        FROM chapter_progress cp
        JOIN books b ON cp.book_id = b.id
        WHERE cp.updated_date >= ?
    """, [cutoff]).fetchall()
    for date, type_, name, chapter, pct in chapter_updates:
        detail = f"Ch {chapter} → {pct}%"
        activities.append((date, type_, name, detail))

    # Lecture completions
    lecture_done = conn.execute("""
        SELECT lp.date, 'Lecture' as type, c.name || ' #' || l.lecture_number as name, l.title
        FROM lecture_progress lp
        JOIN lectures l ON lp.lecture_id = l.id
        JOIN courses c ON l.course_id = c.id
        WHERE lp.date >= ? AND lp.status = 'completed'
    """, [cutoff]).fetchall()
    for date, type_, name, title in lecture_done:
        activities.append((date, type_, name, title))

    # Paper completions
    paper_done = conn.execute("""
        SELECT pp.date, 'Paper' as type, p.title as name, pp.status
        FROM paper_progress pp
        JOIN papers p ON pp.paper_id = p.id
        WHERE pp.date >= ?
    """, [cutoff]).fetchall()
    for date, type_, name, status in paper_done:
        activities.append((date, type_, name, status))

    conn.close()

    if not activities:
        console.print(f"[yellow]No study activity in the last {days} days.[/yellow]")
        return

    activities.sort(key=lambda x: x[0], reverse=True)

    table = Table(title=f"Study Activity (last {days} days)")
    table.add_column("Date", width=12)
    table.add_column("Type", width=10)
    table.add_column("Item", width=30)
    table.add_column("Detail", width=30)

    for date, type_, name, detail in activities:
        date_str = str(date) if date else "-"
        table.add_row(date_str, type_, name, detail)

    console.print(table)


@study_app.callback(invoke_without_command=True)
def study_default(ctx: typer.Context):
    """Show study summary if no subcommand given."""
    if ctx.invoked_subcommand is None:
        repo_root = get_repo_root()
        db_path = repo_root / DB_FILE

        if db_path.exists():
            show_study_summary(repo_root)
        else:
            console.print("[yellow]No database found. Run 'progress init' to create one.[/yellow]")


if __name__ == "__main__":
    app()
