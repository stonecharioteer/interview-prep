"""Progress visualization and chart generation."""

from datetime import datetime, timedelta

import duckdb
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from .models import PALETTE, normalize_topic, DEFAULT_YEAR


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


def generate_progress_chart(repo_root: Path, output_path: Path, year: int = DEFAULT_YEAR,
                            get_db=None, get_study_activity_dates=None, get_commit_dates=None) -> None:
    """Generate the progress chart PNG.

    The get_db, get_study_activity_dates, and get_commit_dates parameters are for
    dependency injection to avoid circular imports.
    """
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
