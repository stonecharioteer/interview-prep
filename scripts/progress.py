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
    help="Track DSA exercise progress across languages.",
    no_args_is_help=False,
)
console = Console()

# ============ Constants ============

DB_FILE = "progress.db"
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
    ax.text(4.0, 2.2, "DSA Progress", fontsize=22, fontweight="bold", color=PALETTE["text"], va="center")
    ax.text(
        4.0, 1.4, f"{total_done} of {total_exercises} exercises completed ({pct}%)",
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


def generate_progress_chart(repo_root: Path, output_path: Path, year: int = DEFAULT_YEAR) -> None:
    conn = get_db(repo_root)

    topics = get_topic_progress_from_db(conn, "python")
    db_dates = get_activity_dates_from_db(conn)
    conn.close()

    git_dates = get_commit_dates(repo_root)
    commit_dates = db_dates | git_dates

    in_progress, not_started = categorize_topics(topics)
    not_started_count = len(not_started)

    total_exercises = sum(t["total"] for t in topics.values())
    total_done = sum(t["python"] for t in topics.values())

    current_streak, longest_streak, total_days = calculate_streaks(commit_dates, year)

    num_topics = len(in_progress) if in_progress else 1
    fig_height = max(10, 3 + num_topics * 0.6 + 1.5 + 4 + 0.5)

    fig = plt.figure(figsize=(12, fig_height))
    fig.patch.set_facecolor("white")

    gs = fig.add_gridspec(4, 1, height_ratios=[3, num_topics * 0.6 + 1.5, 4, 0.5], hspace=0.15)

    ax_hero = fig.add_subplot(gs[0])
    ax_topics = fig.add_subplot(gs[1])
    ax_calendar = fig.add_subplot(gs[2])
    ax_footer = fig.add_subplot(gs[3])

    draw_hero_section(ax_hero, total_done, total_exercises, current_streak)
    draw_topic_progress(ax_topics, in_progress, not_started_count)
    draw_learning_streak(ax_calendar, commit_dates, year, current_streak, longest_streak, total_days)

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


if __name__ == "__main__":
    app()
