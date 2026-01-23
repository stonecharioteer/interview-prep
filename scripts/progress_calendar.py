#!/usr/bin/env python3
"""Generate a topic-based progress chart and habit tracker for DSA exercises."""

import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Quirky color palette - soft pastels with pops of color
PALETTE = {
    "python": "#6366f1",     # Indigo
    "rust": "#f97316",       # Orange
    "js": "#eab308",         # Amber
    "bg": "#f1f5f9",         # Slate 100
    "active": "#10b981",     # Emerald
    "inactive": "#e2e8f0",   # Slate 200
    "text": "#475569",       # Slate 600
    "text_light": "#94a3b8", # Slate 400
    "accent": "#8b5cf6",     # Violet
}


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
        if match:
            topic = match.group(1).strip()
            py_done = match.group(2) == "x"
            rust_done = match.group(3) == "x"
            js_done = match.group(4) == "x"

            # Normalize topic names
            if topic.startswith("Trees (binary)"):
                topic = "Trees (binary)"
            elif topic.startswith("Trees (BST)"):
                topic = "Trees (BST)"
            elif topic.startswith("DP "):
                topic = "Dynamic Programming"
            elif topic.startswith("Heap"):
                topic = "Heap"
            elif topic.startswith("Graph"):
                topic = "Graph"
            elif topic.startswith("Union-Find"):
                topic = "Union-Find"
            elif topic.startswith("String matching"):
                topic = "String Matching"
            elif topic.startswith("Conversions"):
                topic = "Conversions"

            if topic not in topics:
                topics[topic] = {"total": 0, "python": 0, "rust": 0, "js": 0}

            topics[topic]["total"] += 1
            if py_done:
                topics[topic]["python"] += 1
            if rust_done:
                topics[topic]["rust"] += 1
            if js_done:
                topics[topic]["js"] += 1

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


def generate_progress_chart(topics: dict, commit_dates: set, output_path: Path, year: int = 2026) -> None:
    """Generate combined progress bars and habit tracker."""
    sorted_topics = sorted(topics.items(), key=lambda x: x[1]["total"], reverse=True)

    topic_names = [t[0] for t in sorted_topics]
    totals = [t[1]["total"] for t in sorted_topics]
    python_done = [t[1]["python"] for t in sorted_topics]
    rust_done = [t[1]["rust"] for t in sorted_topics]
    js_done = [t[1]["js"] for t in sorted_topics]

    # Create figure - tighter layout
    fig = plt.figure(figsize=(12, max(12, len(topic_names) * 0.45 + 5)))
    fig.patch.set_facecolor("white")

    gs = fig.add_gridspec(3, 1, height_ratios=[len(topic_names) * 1.2, 19, 0.8], hspace=0.08)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])

    # ============ TOP: Topic Progress Bars ============
    ax1.set_facecolor("white")
    y_pos = np.arange(len(topic_names)) * 1.4  # More vertical spacing
    bar_height = 0.38

    # Background bars with rounded ends
    ax1.barh(y_pos, totals, height=1.1, color=PALETTE["bg"], zorder=1,
             left=0, edgecolor="none")

    # Progress bars
    ax1.barh(y_pos + bar_height, python_done, height=bar_height,
             color=PALETTE["python"], label="Python", zorder=2)
    ax1.barh(y_pos, rust_done, height=bar_height,
             color=PALETTE["rust"], label="Rust", zorder=2)
    ax1.barh(y_pos - bar_height, js_done, height=bar_height,
             color=PALETTE["js"], label="JavaScript", zorder=2)

    # Labels with fun formatting
    for i, (total, py, rs, js) in enumerate(zip(totals, python_done, rust_done, js_done)):
        y = y_pos[i]
        ax1.text(total + 0.5, y, f"/{total}", va="center", ha="left",
                 fontsize=9, color=PALETTE["text_light"], fontweight="medium")
        if py > 0:
            ax1.text(py - 0.3, y + bar_height, str(py), va="center", ha="right",
                     fontsize=8, color="white", fontweight="bold")
        if rs > 0:
            ax1.text(rs - 0.3, y, str(rs), va="center", ha="right",
                     fontsize=8, color="white", fontweight="bold")
        if js > 0:
            ax1.text(js - 0.3, y - bar_height, str(js), va="center", ha="right",
                     fontsize=8, color="#333", fontweight="bold")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(topic_names, fontsize=10, color=PALETTE["text"])
    ax1.invert_yaxis()
    ax1.set_xlim(0, max(totals) + 4)

    # Clean up spines
    for spine in ax1.spines.values():
        spine.set_visible(False)
    ax1.tick_params(left=False, bottom=False, labelbottom=False)

    # Legend - horizontal below the bars
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.01),
               ncol=3, frameon=False, fontsize=9,
               labelcolor=PALETTE["text"], handletextpad=0.3, columnspacing=1)

    # Title
    total_exercises = sum(totals)
    total_py = sum(python_done)
    pct = 100 * total_py // total_exercises

    title = f"DSA Progress: {total_py}/{total_exercises} ({pct}%)"
    ax1.set_title(title, fontsize=14, fontweight="bold", color=PALETTE["text"],
                  pad=15, loc="left")

    # ============ MIDDLE: Habit Tracker Calendar ============
    ax2.set_facecolor("white")

    start_date = datetime(year, 1, 1)
    start_weekday = (start_date.weekday() + 1) % 7
    start_date = start_date - timedelta(days=start_weekday)

    current_date = start_date
    month_positions = {}

    # Track dates for adding day-of-month markers
    date_markers = []  # (week, day, day_of_month)

    for week in range(53):
        for day in range(7):
            if current_date.year == year:
                date_str = current_date.strftime("%Y-%m-%d")
                is_active = date_str in commit_dates
                color = PALETTE["active"] if is_active else PALETTE["inactive"]

                if current_date.day <= 7 and day == 0:
                    month_positions[current_date.month] = week

                # Mark 1st and 15th of each month for reference
                if current_date.day == 1 or current_date.day == 15:
                    date_markers.append((week, day, current_date.day))

                rect = mpatches.FancyBboxPatch(
                    (week, 6 - day), 0.85, 0.85,
                    boxstyle="round,pad=0,rounding_size=0.2",
                    facecolor=color,
                    edgecolor="white",
                    linewidth=0.5,
                )
                ax2.add_patch(rect)

            current_date += timedelta(days=1)

    # Add date markers (1st and 15th)
    for week, day, day_num in date_markers:
        ax2.text(week + 0.42, 6 - day + 0.42, str(day_num),
                 ha="center", va="center", fontsize=5,
                 color="#666" if day_num == 1 else "#999", fontweight="bold")

    # Set limits to center the calendar (53 weeks = 0-52)
    ax2.set_xlim(-3, 56)
    ax2.set_ylim(-5, 8.5)
    ax2.set_aspect("equal")
    ax2.axis("off")

    # Day labels
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, label in enumerate(day_labels):
        ax2.text(-1.5, 6 - i + 0.4, label, ha="right", va="center",
                 fontsize=8, color=PALETTE["text_light"])

    # Month labels
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for month, week_pos in month_positions.items():
        ax2.text(week_pos + 0.4, 7.5, months[month - 1], ha="center", va="bottom",
                 fontsize=9, color=PALETTE["text"], fontweight="medium")

    # Streak stats
    current_streak, longest_streak, total_days = calculate_streaks(commit_dates, year)

    fire = "●" if current_streak >= 3 else "○"
    trophy = "★" if longest_streak >= 7 else "☆"

    stats_parts = [
        f"{fire} {current_streak} day{'s' if current_streak != 1 else ''} current",
        f"{trophy} {longest_streak} day{'s' if longest_streak != 1 else ''} best",
        f"◆ {total_days} day{'s' if total_days != 1 else ''} total",
    ]

    ax2.text(26.5, -1.2, "  |  ".join(stats_parts), ha="center", va="top",
             fontsize=11, color=PALETTE["text"], fontweight="bold")

    # Legend - centered below stats
    legend_x = 21.5
    legend_y = -3.5
    rect = mpatches.FancyBboxPatch((legend_x, legend_y - 0.4), 0.85, 0.85,
                                    boxstyle="round,pad=0,rounding_size=0.2",
                                    facecolor=PALETTE["inactive"], edgecolor="white", linewidth=0.5)
    ax2.add_patch(rect)
    ax2.text(legend_x + 1.2, legend_y, "Rest", ha="left", va="center",
             fontsize=8, color=PALETTE["text_light"])

    rect = mpatches.FancyBboxPatch((legend_x + 5, legend_y - 0.4), 0.85, 0.85,
                                    boxstyle="round,pad=0,rounding_size=0.2",
                                    facecolor=PALETTE["active"], edgecolor="white", linewidth=0.5)
    ax2.add_patch(rect)
    ax2.text(legend_x + 6.2, legend_y, "Learned", ha="left", va="center",
             fontsize=8, color=PALETTE["text_light"])

    # ============ BOTTOM: Timestamp and repo link ============
    ax3.set_facecolor("white")
    ax3.axis("off")

    timestamp = format_timestamp()
    ax3.text(0.5, 0.7, f"Last updated: {timestamp}",
             ha="center", va="center", fontsize=9,
             color=PALETTE["text_light"], style="italic",
             transform=ax3.transAxes)
    ax3.text(0.5, 0.2, "github.com/stonecharioteer/interview-prep",
             ha="center", va="center", fontsize=8,
             color=PALETTE["text_light"],
             transform=ax3.transAxes)

    fig.savefig(output_path, dpi=200, bbox_inches="tight",
                facecolor="white", edgecolor="none", pad_inches=0.15)
    plt.close(fig)


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    import os
    os.chdir(repo_root)

    readme_path = repo_root / "README.md"
    output_path = repo_root / "progress.png"

    topics = parse_readme_progress(readme_path)
    commit_dates = get_commit_dates()

    generate_progress_chart(topics, commit_dates, output_path, year=2026)

    print(f"Generated {output_path}")

    total = sum(t["total"] for t in topics.values())
    py = sum(t["python"] for t in topics.values())
    current, longest, days = calculate_streaks(commit_dates, 2026)
    print(f"  Progress: {py}/{total} ({100*py//total}%)")
    print(f"  Streak: {current} current, {longest} best, {days} total days")
    print(f"  Updated: {format_timestamp()}")


if __name__ == "__main__":
    main()
