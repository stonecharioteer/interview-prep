"""Constants, enums, and palette definitions for progress CLI."""

import os
from enum import Enum

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


LANG_EMOJI = {"python": "\U0001F40D", "rust": "\U0001F980", "typescript": "\U0001F7E8"}

STATUS_SYMBOL = {
    "not_started": "[dim]\u00b7[/]",
    "attempted": "[yellow]\u25cb[/]",
    "solved": "[green]\u2713[/]",
}

STUDY_STATUS_SYMBOL = {
    "not_started": "[dim]\u00b7[/]",
    "in_progress": "[yellow]\u25cb[/]",
    "reading": "[yellow]\u25cb[/]",
    "watching": "[yellow]\u25cb[/]",
    "completed": "[green]\u2713[/]",
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
