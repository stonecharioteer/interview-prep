#!/usr/bin/env python3
"""Generate a topic-based progress chart and habit tracker for DSA exercises."""

import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# Color palette - soft pastels with pops of color
PALETTE = {
    "python": "#6366f1",     # Indigo
    "rust": "#f97316",       # Orange
    "js": "#eab308",         # Amber
    "bg": "#f1f5f9",         # Slate 100
    "bg_dark": "#e2e8f0",    # Slate 200 (for milestone markers)
    "active": "#10b981",     # Emerald
    "inactive": "#cbd5e1",   # Slate 300 (more visible)
    "text": "#334155",       # Slate 700 (darker for better contrast)
    "text_light": "#64748b", # Slate 500
    "text_muted": "#94a3b8", # Slate 400
    "accent": "#8b5cf6",     # Violet
    "card_bg": "#f8fafc",    # Slate 50 (for card backgrounds)
    "card_border": "#e2e8f0", # Slate 200
}

# Default year for streak calculations
DEFAULT_YEAR = 2026

# Topic name normalization mapping (prefix -> normalized name)
TOPIC_NORMALIZATION = {
    "Trees (binary)": "Trees (binary)",
    "Trees (BST)": "Trees (BST)",
    "DP ": "Dynamic Programming",
    "Heap": "Heap",
    "Graph": "Graph",
    "Union-Find": "Union-Find",
    "String matching": "String Matching",
    "Conversions": "Conversions",
}


def normalize_topic_name(topic: str) -> str:
    """Normalize topic name using prefix matching."""
    for prefix, normalized in TOPIC_NORMALIZATION.items():
        if topic.startswith(prefix):
            return normalized
    return topic


def parse_readme_progress(readme_path: Path) -> dict[str, dict]:
    """Parse README.md and extract progress by topic."""
    content = readme_path.read_text()
    lines = content.split("\n")
    topics = {}

    pattern = re.compile(
        r"^\d+\.\s+([^:]+):\s+.+🐍\[([x ])\]\s+🦀\[([x ])\]\s+🟨\[([x ])\]"
    )

    for line in lines:
        match = pattern.match(line.strip())
        if not match:
            continue

        topic = normalize_topic_name(match.group(1).strip())
        py_done = match.group(2) == "x"
        rust_done = match.group(3) == "x"
        js_done = match.group(4) == "x"

        if topic not in topics:
            topics[topic] = {"total": 0, "python": 0, "rust": 0, "js": 0}

        topics[topic]["total"] += 1
        topics[topic]["python"] += py_done
        topics[topic]["rust"] += rust_done
        topics[topic]["js"] += js_done

    return topics


def get_commit_dates() -> set[str]:
    """Get unique commit dates for actual exercise code."""
    result = subprocess.run(
        ["git", "log", "--pretty=format:%ad", "--date=short", "--",
         "python/src/", "python/test/",
         ":!*.png", ":!*.toml", ":!*.lock"],
        capture_output=True,
        text=True,
        check=True,
    )
    dates = result.stdout.strip().split("\n")
    return set(d for d in dates if d)


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
    """Split topics into in_progress (Python > 0) and not_started."""
    in_progress = [(name, data) for name, data in topics.items() if data["python"] > 0]
    not_started = [(name, data) for name, data in topics.items() if data["python"] == 0]
    # Sort by Python progress descending
    in_progress.sort(key=lambda x: x[1]["python"], reverse=True)
    not_started.sort(key=lambda x: x[1]["total"], reverse=True)
    return in_progress, not_started


def draw_hero_section(ax, total_done: int, total_exercises: int, current_streak: int):
    """Draw donut chart with headline and streak badge."""
    ax.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    # Donut chart - create a pie chart with a circle in the middle
    remaining = total_exercises - total_done
    donut_ax = ax.inset_axes([0.02, 0.1, 0.35, 0.85])  # [x, y, width, height]

    wedges, _ = donut_ax.pie(
        [total_done, remaining],
        colors=[PALETTE["python"], PALETTE["bg"]],
        startangle=90,
        wedgeprops=dict(width=0.35, edgecolor="white", linewidth=2),
    )
    # Center circle for donut effect
    center_circle = plt.Circle((0, 0), 0.45, fc="white")
    donut_ax.add_artist(center_circle)

    # Center text
    donut_ax.text(0, 0.08, f"{total_done}", fontsize=28, fontweight="bold",
                  ha="center", va="center", color=PALETTE["python"])
    donut_ax.text(0, -0.25, "done", fontsize=10, ha="center", va="center",
                  color=PALETTE["text_light"])

    # Headline text
    pct = int(100 * total_done / total_exercises) if total_exercises > 0 else 0
    ax.text(4.0, 2.2, "DSA Progress", fontsize=22, fontweight="bold",
            color=PALETTE["text"], va="center")
    ax.text(4.0, 1.4, f"{total_done} of {total_exercises} exercises completed ({pct}%)",
            fontsize=12, color=PALETTE["text_light"], va="center")

    # Streak badge
    if current_streak > 0:
        badge_x, badge_y = 4.0, 0.5
        streak_color = PALETTE["active"] if current_streak >= 3 else PALETTE["text_muted"]

        # Badge background
        badge = mpatches.FancyBboxPatch(
            (badge_x - 0.1, badge_y - 0.25), 2.2, 0.5,
            boxstyle="round,pad=0.1,rounding_size=0.2",
            facecolor=PALETTE["card_bg"],
            edgecolor=streak_color,
            linewidth=1.5,
        )
        ax.add_patch(badge)

        ax.text(badge_x + 1.0, badge_y, f"{current_streak}-day streak",
                fontsize=10, fontweight="bold", ha="center", va="center",
                color=streak_color)


def draw_topic_progress(ax, in_progress: list, not_started_count: int):
    """Draw simplified Python-only progress bars for in-progress topics."""
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

    # Section header
    ax.text(-0.5, -1.2, "TOPIC PROGRESS", fontsize=10, fontweight="bold",
            color=PALETTE["text_muted"])

    # Background bars
    for i, total in enumerate(totals):
        ax.barh(y_pos[i], total, height=bar_height + 0.15, color=PALETTE["bg"],
                zorder=1, left=0, edgecolor="none")

    # Progress bars (Python only)
    ax.barh(y_pos, python_done, height=bar_height,
            color=PALETTE["python"], zorder=2)

    # Labels
    label_x = max_total + 0.8
    for i, (total, py) in enumerate(zip(totals, python_done)):
        ax.text(label_x, y_pos[i], f"{py}/{total}",
                va="center", ha="left", fontsize=10, color=PALETTE["text"],
                fontweight="medium")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(topic_names, fontsize=10, color=PALETTE["text"], fontweight="medium")
    ax.invert_yaxis()
    ax.set_xlim(-0.5, max_total + 4)
    ax.set_ylim(max(y_pos) + 0.8, -1.8)

    # Summary line for not-started topics
    if not_started_count > 0:
        summary_y = max(y_pos) + 0.6
        ax.text(-0.5, summary_y, f"+ {not_started_count} more topics not yet started",
                fontsize=9, color=PALETTE["text_muted"], style="italic")

    # Clean up spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)


def draw_learning_streak(ax, commit_dates: set, year: int, current_streak: int,
                         longest_streak: int, total_days: int):
    """Draw compact 4-week calendar with this-week row and small stats card."""
    ax.set_facecolor("white")
    ax.axis("off")

    # Section header
    ax.text(0, 5.5, "LEARNING STREAK", fontsize=10, fontweight="bold",
            color=PALETTE["text_muted"])

    today = datetime.now().date()
    # Find the start of this week (Sunday)
    days_since_sunday = (today.weekday() + 1) % 7
    this_week_start = today - timedelta(days=days_since_sunday)

    # Calculate 4 weeks back
    four_weeks_ago = this_week_start - timedelta(weeks=3)

    # Day labels
    day_labels = ["S", "M", "T", "W", "T", "F", "S"]
    for i, label in enumerate(day_labels):
        ax.text(i + 0.44, 4.8, label, ha="center", va="center",
                fontsize=9, color=PALETTE["text_light"], fontweight="medium")

    # Draw 4 weeks of calendar
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

    # Week labels on the right (oldest at top, newest at bottom)
    week_labels = ["3 weeks ago", "2 weeks ago", "Last week", "This week"]
    for week, label in enumerate(week_labels):
        ax.text(7.5, 3.5 - week + 0.44, label, ha="left", va="center",
                fontsize=8, color=PALETTE["text_light"])

    # Stats card - compact on the right side
    stats_x = 13
    card = mpatches.FancyBboxPatch(
        (stats_x, 0.3), 6, 4.5,
        boxstyle="round,pad=0.3,rounding_size=0.4",
        facecolor=PALETTE["card_bg"],
        edgecolor=PALETTE["card_border"],
        linewidth=1,
    )
    ax.add_patch(card)

    # Stats
    fire_color = PALETTE["active"] if current_streak >= 3 else PALETTE["text_muted"]
    trophy_color = PALETTE["accent"] if longest_streak >= 7 else PALETTE["text_muted"]

    # Current streak
    ax.text(stats_x + 3, 4.0, f"{current_streak}", fontsize=18, fontweight="bold",
            ha="center", va="center", color=fire_color)
    ax.text(stats_x + 3, 3.3, "current streak", fontsize=8, ha="center", va="center",
            color=PALETTE["text_light"])

    # Best streak
    ax.text(stats_x + 3, 2.3, f"{longest_streak}", fontsize=18, fontweight="bold",
            ha="center", va="center", color=trophy_color)
    ax.text(stats_x + 3, 1.6, "best streak", fontsize=8, ha="center", va="center",
            color=PALETTE["text_light"])

    # Total days
    ax.text(stats_x + 3, 0.85, f"{total_days} days total", fontsize=9,
            ha="center", va="center", color=PALETTE["text"])

    # Set limits
    ax.set_xlim(-0.5, 20)
    ax.set_ylim(-0.5, 6)


def generate_progress_chart(topics: dict, commit_dates: set, output_path: Path, year: int = DEFAULT_YEAR) -> None:
    """Generate combined progress bars and habit tracker."""
    # Categorize topics
    in_progress, not_started = categorize_topics(topics)
    not_started_count = len(not_started)

    # Calculate totals
    total_exercises = sum(t["total"] for t in topics.values())
    total_done = sum(t["python"] for t in topics.values())

    # Calculate streaks
    current_streak, longest_streak, total_days = calculate_streaks(commit_dates, year)

    # Calculate figure height based on in-progress topics
    num_topics = len(in_progress) if in_progress else 1
    fig_height = max(10, 3 + num_topics * 0.6 + 1.5 + 4 + 0.5)

    # Create figure with new layout
    fig = plt.figure(figsize=(12, fig_height))
    fig.patch.set_facecolor("white")

    # New gridspec: [Hero | Topics | Calendar | Footer]
    gs = fig.add_gridspec(4, 1,
                          height_ratios=[3, num_topics * 0.6 + 1.5, 4, 0.5],
                          hspace=0.15)

    ax_hero = fig.add_subplot(gs[0])
    ax_topics = fig.add_subplot(gs[1])
    ax_calendar = fig.add_subplot(gs[2])
    ax_footer = fig.add_subplot(gs[3])

    # Draw sections
    draw_hero_section(ax_hero, total_done, total_exercises, current_streak)
    draw_topic_progress(ax_topics, in_progress, not_started_count)
    draw_learning_streak(ax_calendar, commit_dates, year, current_streak,
                         longest_streak, total_days)

    # Footer
    ax_footer.set_facecolor("white")
    ax_footer.axis("off")

    timestamp = format_timestamp()
    ax_footer.text(0.5, 0.7, f"Last updated: {timestamp}",
                   ha="center", va="center", fontsize=9,
                   color=PALETTE["text_light"], style="italic",
                   transform=ax_footer.transAxes)
    ax_footer.text(0.5, 0.2, "github.com/stonecharioteer/interview-prep",
                   ha="center", va="center", fontsize=8,
                   color=PALETTE["text_light"],
                   transform=ax_footer.transAxes)

    fig.savefig(output_path, dpi=200, bbox_inches="tight",
                facecolor="white", edgecolor="none", pad_inches=0.15)
    plt.close(fig)


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)

    readme_path = repo_root / "README.md"
    output_path = repo_root / "progress.png"

    topics = parse_readme_progress(readme_path)
    commit_dates = get_commit_dates()

    generate_progress_chart(topics, commit_dates, output_path)

    total = sum(t["total"] for t in topics.values())
    py = sum(t["python"] for t in topics.values())
    current, longest, days = calculate_streaks(commit_dates, DEFAULT_YEAR)

    print(f"Generated {output_path}")
    print(f"  Progress: {py}/{total} ({100 * py // total}%)")
    print(f"  Streak: {current} current, {longest} best, {days} total days")
    print(f"  Updated: {format_timestamp()}")


if __name__ == "__main__":
    main()
