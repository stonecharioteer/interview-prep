"""
Unified DSA exercise progress tracker CLI.

Uses DuckDB for tracking, generates README updates and progress visualizations.
"""

import typer
from rich.console import Console

# Create app instances
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

# Register commands
from . import commands_dsa, commands_study

commands_dsa.register_commands(app)
commands_study.register_commands(study_app)


def main():
    """Entry point for the CLI."""
    app()


# Expose key components for imports
from .models import (
    DB_FILE,
    DEFAULT_YEAR,
    LANG_EMOJI,
    PALETTE,
    STATUS_SYMBOL,
    STUDY_STATUS_SYMBOL,
    Language,
    Status,
    StudyStatus,
)
from .db import get_db, get_repo_root
from .visualization import (
    calculate_streaks,
    generate_progress_chart,
    get_activity_dates_from_db,
    get_topic_progress_from_db,
    parse_chapters_string,
)
from .parsing import (
    get_commit_dates,
    get_solved_dates_from_git,
    match_exercise_to_file,
    parse_readme,
    update_exercises_file,
)
from .interactive import prompt_select_from_list, prompt_text, prompt_int
from .commands_study import get_study_activity_dates, show_study_summary
from .commands_dsa import show_summary

__all__ = [
    "app",
    "study_app",
    "console",
    "main",
    # Models
    "DB_FILE",
    "DEFAULT_YEAR",
    "LANG_EMOJI",
    "PALETTE",
    "STATUS_SYMBOL",
    "STUDY_STATUS_SYMBOL",
    "Language",
    "Status",
    "StudyStatus",
    # Database
    "get_db",
    "get_repo_root",
    # Visualization
    "calculate_streaks",
    "generate_progress_chart",
    "get_activity_dates_from_db",
    "get_topic_progress_from_db",
    "parse_chapters_string",
    # Parsing
    "get_commit_dates",
    "get_solved_dates_from_git",
    "match_exercise_to_file",
    "parse_readme",
    "update_exercises_file",
    # Interactive
    "prompt_select_from_list",
    "prompt_text",
    "prompt_int",
    # Commands
    "get_study_activity_dates",
    "show_study_summary",
    "show_summary",
]
