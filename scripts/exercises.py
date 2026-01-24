#!/usr/bin/env python3
"""
Exercise progress tracker using DuckDB.

Manages a database tracking exercise completion status across languages,
and generates progress visualizations.
"""

import argparse
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

console = Console()

# ============ Constants ============

DB_FILE = "progress.db"
LANGUAGES = ["python", "rust", "typescript"]
STATUSES = ["not_started", "attempted", "solved"]
DEFAULT_YEAR = 2026

# Color palette for visualizations
PALETTE = {
    "python": "#6366f1",      # Indigo
    "rust": "#f97316",        # Orange
    "typescript": "#eab308",  # Amber
    "bg": "#f1f5f9",          # Slate 100
    "active": "#10b981",      # Emerald
    "inactive": "#cbd5e1",    # Slate 300
    "text": "#334155",        # Slate 700
    "text_light": "#64748b",  # Slate 500
    "text_muted": "#94a3b8",  # Slate 400
    "accent": "#8b5cf6",      # Violet
    "card_bg": "#f8fafc",     # Slate 50
    "card_border": "#e2e8f0", # Slate 200
}

# Topic normalization for grouping
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
    """Normalize topic name for grouping."""
    for prefix, normalized in TOPIC_NORMALIZATION.items():
        if topic.startswith(prefix):
            return normalized
    return topic


# ============ Database Functions ============

def get_repo_root() -> Path:
    """Get repository root directory."""
    return Path(__file__).parent.parent


def get_db(repo_root: Path) -> duckdb.DuckDBPyConnection:
    """Get database connection, creating tables if needed."""
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


def parse_readme(readme_path: Path) -> list[dict]:
    """Parse exercises from README.md."""
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


def get_solved_dates_from_git(repo_root: Path) -> dict[str, dict[str, str]]:
    """Get approximate solve dates from git history."""
    solved_dates: dict[str, dict[str, str]] = {lang: {} for lang in LANGUAGES}

    lang_paths = {
        "python": "python/src/",
        "rust": "rust/src/",
        "typescript": "js/src/",
    }

    for lang, path in lang_paths.items():
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%ad|%s", "--date=short", "--name-only", "--", path],
                capture_output=True, text=True, cwd=repo_root, check=True,
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


def match_exercise_to_file(exercise: dict, filenames: dict[str, str]) -> str | None:
    """Try to match an exercise to a git file and return the date."""
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


# ============ CLI Commands ============

def init_progress(repo_root: Path, force: bool = False) -> None:
    """Initialize database from README and git history."""
    db_path = repo_root / DB_FILE

    if db_path.exists() and not force:
        if not Confirm.ask(f"[yellow]{DB_FILE} exists. Overwrite?[/yellow]"):
            console.print("[dim]Aborted.[/dim]")
            return
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
            [ex["id"], ex["topic"], ex["name"]]
        )

        for lang in LANGUAGES:
            if ex["readme_status"].get(lang, False):
                date = match_exercise_to_file(ex, git_dates.get(lang, {})) or today
                conn.execute(
                    "INSERT INTO progress (exercise_id, language, status, date) VALUES (?, ?, ?, ?)",
                    [ex["id"], lang, "solved", date]
                )
            else:
                conn.execute(
                    "INSERT INTO progress (exercise_id, language, status) VALUES (?, ?, ?)",
                    [ex["id"], lang, "not_started"]
                )

    conn.close()
    console.print(f"[green]Created {DB_FILE} with {len(exercises)} exercises[/green]")
    show_summary(repo_root)


def mark_exercise(repo_root: Path, exercise_id: int, lang: str, status: str) -> None:
    """Mark an exercise with a status."""
    if lang not in LANGUAGES:
        console.print(f"[red]Invalid language: {lang}. Use: {', '.join(LANGUAGES)}[/red]")
        return

    if status not in STATUSES:
        console.print(f"[red]Invalid status: {status}. Use: {', '.join(STATUSES)}[/red]")
        return

    conn = get_db(repo_root)

    result = conn.execute("SELECT name FROM exercises WHERE id = ?", [exercise_id]).fetchone()
    if not result:
        console.print(f"[red]Exercise {exercise_id} not found[/red]")
        conn.close()
        return

    name = result[0]

    old = conn.execute(
        "SELECT status FROM progress WHERE exercise_id = ? AND language = ?",
        [exercise_id, lang]
    ).fetchone()
    old_status = old[0] if old else "not_started"

    date = datetime.now().strftime("%Y-%m-%d") if status != "not_started" else None
    conn.execute(
        """INSERT OR REPLACE INTO progress (exercise_id, language, status, date)
           VALUES (?, ?, ?, ?)""",
        [exercise_id, lang, status, date]
    )
    conn.close()

    status_colors = {"not_started": "dim", "attempted": "yellow", "solved": "green"}
    console.print(
        f"[{status_colors[old_status]}]{old_status}[/] → "
        f"[{status_colors[status]}]{status}[/] : "
        f"[cyan]#{exercise_id}[/cyan] {name} ({lang})"
    )


def show_summary(repo_root: Path) -> None:
    """Show progress summary."""
    conn = get_db(repo_root)
    total = conn.execute("SELECT COUNT(*) FROM exercises").fetchone()[0]

    console.print()
    for lang, emoji in [("python", "🐍"), ("rust", "🦀"), ("typescript", "🟨")]:
        solved = conn.execute(
            "SELECT COUNT(*) FROM progress WHERE language = ? AND status = 'solved'", [lang]
        ).fetchone()[0]
        attempted = conn.execute(
            "SELECT COUNT(*) FROM progress WHERE language = ? AND status = 'attempted'", [lang]
        ).fetchone()[0]
        remaining = total - solved - attempted
        console.print(f"  {emoji} [green]{solved}[/] solved, [yellow]{attempted}[/] attempted, [dim]{remaining}[/] remaining")

    conn.close()


def list_exercises(repo_root: Path, topic: str | None = None, lang: str | None = None,
                   status_filter: str | None = None) -> None:
    """List exercises with optional filters."""
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

    if lang and status_filter:
        conditions.append("EXISTS (SELECT 1 FROM progress p2 WHERE p2.exercise_id = e.id AND p2.language = ? AND p2.status = ?)")
        params.extend([lang, status_filter])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY e.id ORDER BY e.id"
    results = conn.execute(query, params).fetchall()

    if not results:
        console.print("[yellow]No exercises found.[/yellow]")
        conn.close()
        return

    table = Table(title="Exercise Progress")
    table.add_column("#", style="dim", width=4)
    table.add_column("Topic", style="cyan", width=15)
    table.add_column("Exercise", width=40)
    table.add_column("🐍", justify="center", width=4)
    table.add_column("🦀", justify="center", width=4)
    table.add_column("🟨", justify="center", width=4)

    status_symbols = {"not_started": "[dim]·[/]", "attempted": "[yellow]○[/]", "solved": "[green]✓[/]", None: "[dim]·[/]"}

    for row in results:
        ex_id, topic_name, name, py, rs, ts = row
        table.add_row(
            str(ex_id), topic_name, name,
            status_symbols.get(py, status_symbols[None]),
            status_symbols.get(rs, status_symbols[None]),
            status_symbols.get(ts, status_symbols[None]),
        )

    console.print(table)
    conn.close()
    show_summary(repo_root)


def interactive_mark(repo_root: Path) -> None:
    """Interactive mode to mark exercises."""
    conn = get_db(repo_root)
    count = conn.execute("SELECT COUNT(*) FROM exercises").fetchone()[0]
    conn.close()

    if count == 0:
        console.print("[yellow]No exercises found. Run 'init' first.[/yellow]")
        return

    list_exercises(repo_root)

    console.print()
    ex_id = Prompt.ask("Exercise #", default="")
    if not ex_id:
        return

    try:
        ex_id = int(ex_id)
    except ValueError:
        console.print("[red]Invalid exercise number[/red]")
        return

    lang = Prompt.ask("Language", choices=LANGUAGES)
    status = Prompt.ask("Status", choices=STATUSES, default="solved")

    mark_exercise(repo_root, ex_id, lang, status)


def export_db(repo_root: Path, fmt: str) -> None:
    """Export database to various formats."""
    conn = get_db(repo_root)

    query = """
        SELECT e.id, e.topic, e.name,
            p_py.status as python_status, p_py.date as python_date,
            p_rs.status as rust_status, p_rs.date as rust_date,
            p_ts.status as typescript_status, p_ts.date as typescript_date
        FROM exercises e
        LEFT JOIN progress p_py ON e.id = p_py.exercise_id AND p_py.language = 'python'
        LEFT JOIN progress p_rs ON e.id = p_rs.exercise_id AND p_rs.language = 'rust'
        LEFT JOIN progress p_ts ON e.id = p_ts.exercise_id AND p_ts.language = 'typescript'
        ORDER BY e.id
    """

    output_file = repo_root / f"progress.{fmt}"

    if fmt == "csv":
        conn.execute(f"COPY ({query}) TO '{output_file}' (HEADER, DELIMITER ',')")
    elif fmt == "parquet":
        conn.execute(f"COPY ({query}) TO '{output_file}' (FORMAT PARQUET)")
    elif fmt == "json":
        conn.execute(f"COPY ({query}) TO '{output_file}' (FORMAT JSON, ARRAY true)")

    conn.close()
    console.print(f"[green]Exported to {output_file}[/green]")


# ============ Visualization Data Functions ============

def get_topic_progress_from_db(conn: duckdb.DuckDBPyConnection, lang: str = "python") -> dict[str, dict]:
    """Get topic-level progress from database."""
    results = conn.execute("""
        SELECT
            e.topic,
            COUNT(*) as total,
            SUM(CASE WHEN p.status = 'solved' THEN 1 ELSE 0 END) as solved
        FROM exercises e
        LEFT JOIN progress p ON e.id = p.exercise_id AND p.language = ?
        GROUP BY e.topic
    """, [lang]).fetchall()

    topics = {}
    for topic, total, solved in results:
        normalized = normalize_topic(topic)
        if normalized not in topics:
            topics[normalized] = {"total": 0, "python": 0}
        topics[normalized]["total"] += total
        topics[normalized]["python"] += solved

    return topics


def get_activity_dates_from_db(conn: duckdb.DuckDBPyConnection) -> set[str]:
    """Get all dates with solved exercises from database."""
    results = conn.execute("""
        SELECT DISTINCT CAST(date AS VARCHAR) FROM progress
        WHERE date IS NOT NULL AND status = 'solved'
    """).fetchall()

    return set(row[0] for row in results if row[0])


def get_commit_dates(repo_root: Path) -> set[str]:
    """Get unique commit dates for exercise code (fallback to git)."""
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%ad", "--date=short", "--",
             "python/src/", "python/test/", ":!*.png", ":!*.toml", ":!*.lock"],
            capture_output=True, text=True, cwd=repo_root, check=True,
        )
        return set(d for d in result.stdout.strip().split("\n") if d)
    except subprocess.CalledProcessError:
        return set()


# ============ Visualization Drawing Functions ============

def calculate_streaks(commit_dates: set[str], year: int) -> tuple[int, int, int]:
    """Calculate current streak, longest streak, and total active days."""
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
        if (date_objs[i] - date_objs[i-1]).days == 1:
            current += 1
            longest = max(longest, current)
        elif date_objs[i] != date_objs[i-1]:
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
    """Return a human-friendly timestamp."""
    now = datetime.now()
    return now.strftime("%B %d, %Y at %I:%M %p").replace(" 0", " ").replace("AM", "am").replace("PM", "pm")


def categorize_topics(topics: dict) -> tuple[list, list]:
    """Split topics into in_progress and not_started."""
    in_progress = [(name, data) for name, data in topics.items() if data["python"] > 0]
    not_started = [(name, data) for name, data in topics.items() if data["python"] == 0]
    in_progress.sort(key=lambda x: x[1]["python"], reverse=True)
    not_started.sort(key=lambda x: x[1]["total"], reverse=True)
    return in_progress, not_started


def draw_hero_section(ax, total_done: int, total_exercises: int, current_streak: int):
    """Draw donut chart with headline and streak badge."""
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

    donut_ax.text(0, 0.08, f"{total_done}", fontsize=28, fontweight="bold",
                  ha="center", va="center", color=PALETTE["python"])
    donut_ax.text(0, -0.25, "done", fontsize=10, ha="center", va="center",
                  color=PALETTE["text_light"])

    pct = int(100 * total_done / total_exercises) if total_exercises > 0 else 0
    ax.text(4.0, 2.2, "DSA Progress", fontsize=22, fontweight="bold",
            color=PALETTE["text"], va="center")
    ax.text(4.0, 1.4, f"{total_done} of {total_exercises} exercises completed ({pct}%)",
            fontsize=12, color=PALETTE["text_light"], va="center")

    if current_streak > 0:
        badge_x, badge_y = 4.0, 0.5
        streak_color = PALETTE["active"] if current_streak >= 3 else PALETTE["text_muted"]

        badge = mpatches.FancyBboxPatch(
            (badge_x - 0.1, badge_y - 0.25), 2.2, 0.5,
            boxstyle="round,pad=0.1,rounding_size=0.2",
            facecolor=PALETTE["card_bg"], edgecolor=streak_color, linewidth=1.5,
        )
        ax.add_patch(badge)
        ax.text(badge_x + 1.0, badge_y, f"{current_streak}-day streak",
                fontsize=10, fontweight="bold", ha="center", va="center", color=streak_color)


def draw_topic_progress(ax, in_progress: list, not_started_count: int):
    """Draw simplified Python-only progress bars."""
    ax.set_facecolor("white")

    if not in_progress:
        ax.axis("off")
        ax.text(0.5, 0.5, "No topics started yet!", transform=ax.transAxes,
                ha="center", va="center", fontsize=12, color=PALETTE["text_light"])
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
        ax.text(label_x, y_pos[i], f"{py}/{total}", va="center", ha="left",
                fontsize=10, color=PALETTE["text"], fontweight="medium")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(topic_names, fontsize=10, color=PALETTE["text"], fontweight="medium")
    ax.invert_yaxis()
    ax.set_xlim(-0.5, max_total + 4)
    ax.set_ylim(max(y_pos) + 0.8, -1.8)

    if not_started_count > 0:
        ax.text(-0.5, max(y_pos) + 0.6, f"+ {not_started_count} more topics not yet started",
                fontsize=9, color=PALETTE["text_muted"], style="italic")

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)


def draw_learning_streak(ax, commit_dates: set, year: int, current_streak: int,
                         longest_streak: int, total_days: int):
    """Draw compact 4-week calendar with stats card."""
    ax.set_facecolor("white")
    ax.axis("off")

    ax.text(0, 5.5, "LEARNING STREAK", fontsize=10, fontweight="bold", color=PALETTE["text_muted"])

    today = datetime.now().date()
    days_since_sunday = (today.weekday() + 1) % 7
    this_week_start = today - timedelta(days=days_since_sunday)
    four_weeks_ago = this_week_start - timedelta(weeks=3)

    day_labels = ["S", "M", "T", "W", "T", "F", "S"]
    for i, label in enumerate(day_labels):
        ax.text(i + 0.44, 4.8, label, ha="center", va="center",
                fontsize=9, color=PALETTE["text_light"], fontweight="medium")

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
        ax.text(7.5, 3.5 - week + 0.44, label, ha="left", va="center",
                fontsize=8, color=PALETTE["text_light"])

    stats_x = 13
    card = mpatches.FancyBboxPatch(
        (stats_x, 0.3), 6, 4.5,
        boxstyle="round,pad=0.3,rounding_size=0.4",
        facecolor=PALETTE["card_bg"], edgecolor=PALETTE["card_border"], linewidth=1,
    )
    ax.add_patch(card)

    fire_color = PALETTE["active"] if current_streak >= 3 else PALETTE["text_muted"]
    trophy_color = PALETTE["accent"] if longest_streak >= 7 else PALETTE["text_muted"]

    ax.text(stats_x + 3, 4.0, f"{current_streak}", fontsize=18, fontweight="bold",
            ha="center", va="center", color=fire_color)
    ax.text(stats_x + 3, 3.3, "current streak", fontsize=8, ha="center", va="center",
            color=PALETTE["text_light"])

    ax.text(stats_x + 3, 2.3, f"{longest_streak}", fontsize=18, fontweight="bold",
            ha="center", va="center", color=trophy_color)
    ax.text(stats_x + 3, 1.6, "best streak", fontsize=8, ha="center", va="center",
            color=PALETTE["text_light"])

    ax.text(stats_x + 3, 0.85, f"{total_days} days total", fontsize=9,
            ha="center", va="center", color=PALETTE["text"])

    ax.set_xlim(-0.5, 20)
    ax.set_ylim(-0.5, 6)


def generate_progress_chart(repo_root: Path, output_path: Path, year: int = DEFAULT_YEAR) -> None:
    """Generate progress chart from database."""
    conn = get_db(repo_root)

    # Get data from database
    topics = get_topic_progress_from_db(conn, "python")
    db_dates = get_activity_dates_from_db(conn)
    conn.close()

    # Also get git commit dates for more complete picture
    git_dates = get_commit_dates(repo_root)
    commit_dates = db_dates | git_dates

    # Process topics
    in_progress, not_started = categorize_topics(topics)
    not_started_count = len(not_started)

    total_exercises = sum(t["total"] for t in topics.values())
    total_done = sum(t["python"] for t in topics.values())

    current_streak, longest_streak, total_days = calculate_streaks(commit_dates, year)

    # Create figure
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
    ax_footer.text(0.5, 0.7, f"Last updated: {timestamp}",
                   ha="center", va="center", fontsize=9,
                   color=PALETTE["text_light"], style="italic", transform=ax_footer.transAxes)
    ax_footer.text(0.5, 0.2, "github.com/stonecharioteer/interview-prep",
                   ha="center", va="center", fontsize=8,
                   color=PALETTE["text_light"], transform=ax_footer.transAxes)

    fig.savefig(output_path, dpi=200, bbox_inches="tight",
                facecolor="white", edgecolor="none", pad_inches=0.15)
    plt.close(fig)


def plot_progress(repo_root: Path) -> None:
    """Generate progress chart command."""
    db_path = repo_root / DB_FILE
    if not db_path.exists():
        console.print("[yellow]No database found. Run 'init' first.[/yellow]")
        return

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


# ============ Main ============

def main():
    parser = argparse.ArgumentParser(description="Track exercise progress")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize database from README")
    init_parser.add_argument("--force", "-f", action="store_true", help="Overwrite existing")

    # mark
    mark_parser = subparsers.add_parser("mark", help="Mark exercise status")
    mark_parser.add_argument("id", type=int, help="Exercise ID")
    mark_parser.add_argument("lang", choices=LANGUAGES, help="Language")
    mark_parser.add_argument("status", choices=STATUSES, nargs="?", default="solved")

    # list
    list_parser = subparsers.add_parser("list", help="List exercises")
    list_parser.add_argument("--topic", "-t", help="Filter by topic")
    list_parser.add_argument("--lang", "-l", choices=LANGUAGES, help="Filter by language")
    list_parser.add_argument("--status", "-s", choices=STATUSES, help="Filter by status")

    # interactive
    subparsers.add_parser("i", help="Interactive mode")

    # export
    export_parser = subparsers.add_parser("export", help="Export to file")
    export_parser.add_argument("format", choices=["csv", "parquet", "json"])

    # plot
    subparsers.add_parser("plot", help="Generate progress chart (progress.png)")

    args = parser.parse_args()
    repo_root = get_repo_root()

    if args.command == "init":
        init_progress(repo_root, args.force)
    elif args.command == "mark":
        mark_exercise(repo_root, args.id, args.lang, args.status)
    elif args.command == "list":
        list_exercises(repo_root, args.topic, args.lang, args.status)
    elif args.command == "i":
        interactive_mark(repo_root)
    elif args.command == "export":
        export_db(repo_root, args.format)
    elif args.command == "plot":
        plot_progress(repo_root)
    else:
        db_path = repo_root / DB_FILE
        if db_path.exists():
            list_exercises(repo_root)
        else:
            console.print("[yellow]No database found. Run 'exercises init' to create one.[/yellow]")


if __name__ == "__main__":
    main()
