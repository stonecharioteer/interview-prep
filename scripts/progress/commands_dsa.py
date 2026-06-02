"""DSA exercise commands."""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from .db import get_db, get_repo_root
from .models import (
    DB_FILE,
    DEFAULT_YEAR,
    LANG_EMOJI,
    STATUS_SYMBOL,
    Language,
    Status,
)
from .parsing import (
    get_commit_dates,
    get_solved_dates_from_git,
    match_exercise_to_file,
    parse_readme,
    update_exercises_file,
)
from .visualization import (
    calculate_streaks,
    generate_progress_chart,
    get_activity_dates_from_db,
    get_topic_progress_from_db,
)
from .interactive import prompt_select_from_list

console = Console()


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


def register_commands(app: typer.Typer) -> None:
    """Register DSA commands with the app."""

    @app.command()
    def init(
        force: Annotated[
            bool, typer.Option("--force", "-f", help="Overwrite existing database")
        ] = False,
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
                    date = (
                        match_exercise_to_file(ex, git_dates.get(lang_key, {})) or today
                    )
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
        console.print(
            f"[green]Created {DB_FILE} with {len(exercises)} exercises[/green]"
        )
        show_summary(repo_root)

    @app.command()
    def mark(
        exercise_id: Annotated[
            Optional[int], typer.Argument(help="Exercise ID to mark")
        ] = None,
        lang: Annotated[Optional[Language], typer.Argument(help="Language")] = None,
        status: Annotated[Status, typer.Argument(help="New status")] = Status.solved,
    ):
        """Mark an exercise with a status."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for exercise if not provided
        if exercise_id is None:
            exercises = conn.execute("""
                SELECT e.id, e.topic || ': ' || e.name as display
                FROM exercises e
                ORDER BY e.id
            """).fetchall()
            if not exercises:
                console.print("[yellow]No exercises found.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            exercise_id = prompt_select_from_list(
                [(ex[0], ex[1]) for ex in exercises], "Select exercise"
            )

        result = conn.execute(
            "SELECT name FROM exercises WHERE id = ?", [exercise_id]
        ).fetchone()
        if not result:
            console.print(f"[red]Exercise {exercise_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        name = result[0]

        # Interactive mode: prompt for language if not provided
        if lang is None:
            console.print()
            for i, language in enumerate(Language, 1):
                emoji = LANG_EMOJI[language.value]
                console.print(f"  {i}. {emoji} {language.value}")
            console.print()
            from rich.prompt import IntPrompt

            while True:
                choice = IntPrompt.ask("Select language", console=console)
                if 1 <= choice <= len(Language):
                    lang = list(Language)[choice - 1]
                    break
                console.print(f"[red]Enter 1-{len(Language)}[/red]")

        old = conn.execute(
            "SELECT status FROM progress WHERE exercise_id = ? AND language = ?",
            [exercise_id, lang.value],
        ).fetchone()
        old_status = old[0] if old else "not_started"

        date = (
            datetime.now().strftime("%Y-%m-%d")
            if status != Status.not_started
            else None
        )
        conn.execute(
            """INSERT OR REPLACE INTO progress (exercise_id, language, status, date)
               VALUES (?, ?, ?, ?)""",
            [exercise_id, lang.value, status.value, date],
        )
        conn.close()

        status_colors = {"not_started": "dim", "attempted": "yellow", "solved": "green"}
        console.print(
            f"[{status_colors[old_status]}]{old_status}[/] \u2192 "
            f"[{status_colors[status.value]}]{status.value}[/] : "
            f"[cyan]#{exercise_id}[/cyan] {name} ({lang.value})"
        )

    @app.command("list")
    def list_exercises(
        topic: Annotated[
            Optional[str], typer.Option("--topic", "-t", help="Filter by topic")
        ] = None,
        lang: Annotated[
            Optional[Language], typer.Option("--lang", "-l", help="Filter by language")
        ] = None,
        status: Annotated[
            Optional[Status], typer.Option("--status", "-s", help="Filter by status")
        ] = None,
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
        table.add_column("\U0001f40d", justify="center", width=4)
        table.add_column("\U0001f980", justify="center", width=4)
        table.add_column("\U0001f7e8", justify="center", width=4)

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
        lang: Annotated[
            Language, typer.Argument(help="Language to check")
        ] = Language.python,
        count: Annotated[
            int, typer.Option("--count", "-n", help="Number to show")
        ] = 10,
    ):
        """Show next unsolved or attempted exercises for a language."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        results = conn.execute(
            """
            SELECT e.id, e.topic, e.name, p.status
            FROM exercises e
            JOIN progress p ON e.id = p.exercise_id AND p.language = ?
            WHERE p.status IN ('not_started', 'attempted')
            ORDER BY
                CASE p.status WHEN 'attempted' THEN 0 ELSE 1 END,
                e.id
            LIMIT ?
            """,
            [lang.value, count],
        ).fetchall()
        conn.close()

        if not results:
            console.print(
                f"[green]All done![/green] No unsolved {lang.value} exercises remaining."
            )
            return

        emoji = LANG_EMOJI[lang.value]
        table = Table(title=f"{emoji} Next {len(results)} exercises")
        table.add_column("#", style="dim", width=4)
        table.add_column("Topic", style="cyan")
        table.add_column("Exercise", style="white")
        table.add_column("Status", width=10)

        for ex_id, topic, name, status in results:
            status_display = (
                "[yellow]attempted[/yellow]"
                if status == "attempted"
                else "[dim]new[/dim]"
            )
            table.add_row(str(ex_id), topic, name, status_display)

        console.print(table)

    # Topic -> filename mapping per language (2026 paths)
    TOPIC_TO_FILE = {
        "Arrays": {"python": "arrays.py", "typescript": "arrays.ts", "rust": "lib.rs"},
        "Backtracking": {
            "python": "backtracking.py",
            "typescript": None,
            "rust": "lib.rs",
        },
        "Binary search": {
            "python": "binary_search.py",
            "typescript": "binarySearch.ts",
            "rust": "lib.rs",
        },
        "Bits": {"python": "bits.py", "typescript": "bits.ts", "rust": "lib.rs"},
        "Conversions": {
            "python": "conversions.py",
            "typescript": None,
            "rust": "lib.rs",
        },
        "DP (1D)": {"python": "dp.py", "typescript": None, "rust": "lib.rs"},
        "DP (2D)": {"python": "dp.py", "typescript": None, "rust": "lib.rs"},
        "DP (bitmask)": {"python": "dp.py", "typescript": None, "rust": "lib.rs"},
        "DP (interval)": {"python": "dp.py", "typescript": None, "rust": "lib.rs"},
        "DP (string)": {"python": "dp.py", "typescript": None, "rust": "lib.rs"},
        "DP (tree)": {"python": "dp.py", "typescript": None, "rust": "lib.rs"},
        "Graph": {"python": "graph.py", "typescript": None, "rust": "lib.rs"},
        "Greedy": {"python": "greedy.py", "typescript": None, "rust": "lib.rs"},
        "Heap": {"python": "heap.py", "typescript": None, "rust": "lib.rs"},
        "Heap (max)": {"python": "heap.py", "typescript": None, "rust": "lib.rs"},
        "Heap (min)": {"python": "heap.py", "typescript": None, "rust": "lib.rs"},
        "Linked list": {
            "python": "linked_list.py",
            "typescript": "linkedList.ts",
            "rust": "lib.rs",
        },
        "Maps (dict)": {"python": "maps.py", "typescript": None, "rust": "lib.rs"},
        "Math": {"python": "math_ops.py", "typescript": None, "rust": "lib.rs"},
        "Monotonic stack": {
            "python": "monotonic_stack.py",
            "typescript": None,
            "rust": "lib.rs",
        },
        "Queue": {"python": "queue_ds.py", "typescript": "queue.ts", "rust": "lib.rs"},
        "Recursion": {
            "python": "recursion.py",
            "typescript": "recursion.ts",
            "rust": "lib.rs",
        },
        "Sliding window": {
            "python": "sliding_window.py",
            "typescript": None,
            "rust": "lib.rs",
        },
        "Sorting": {
            "python": "sorting.py",
            "typescript": "sorting.ts",
            "rust": "lib.rs",
        },
        "Stack": {"python": "stack.py", "typescript": "stack.ts", "rust": "lib.rs"},
        "String matching": {
            "python": "string_matching.py",
            "typescript": None,
            "rust": "lib.rs",
        },
        "Trees (BST)": {"python": "trees.py", "typescript": None, "rust": "lib.rs"},
        "Trees (binary)": {"python": "trees.py", "typescript": None, "rust": "lib.rs"},
        "Trie": {"python": "trie.py", "typescript": None, "rust": "lib.rs"},
        "Two pointers": {
            "python": "two_pointers.py",
            "typescript": None,
            "rust": "lib.rs",
        },
        "Union-Find": {"python": "union_find.py", "typescript": None, "rust": "lib.rs"},
    }

    LANG_SOURCE_DIR = {
        "python": "dsa/python/src/year_2026",
        "typescript": "dsa/js/src/2026",
        "rust": "dsa/rust/src",
    }

    def _resolve_file(repo_root: Path, topic: str, lang: str) -> Optional[Path]:
        """Resolve a topic + language to an actual source file path."""
        files = TOPIC_TO_FILE.get(topic)
        if not files:
            return None
        filename = files.get(lang)
        if not filename:
            return None
        source_dir = LANG_SOURCE_DIR.get(lang)
        if not source_dir:
            return None
        return repo_root / source_dir / filename

    @app.command("open")
    def open_exercise(
        lang: Annotated[Language, typer.Argument(help="Language")],
        exercise_id: Annotated[
            Optional[int], typer.Argument(help="Exercise ID to open")
        ] = None,
        next_unsolved: Annotated[
            bool, typer.Option("--next", "-N", help="Open next unsolved exercise")
        ] = False,
    ):
        """Open an exercise file in $EDITOR."""
        editor = os.environ.get("EDITOR", "vi")
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        if next_unsolved:
            result = conn.execute(
                """
                SELECT e.id, e.topic, e.name
                FROM exercises e
                JOIN progress p ON e.id = p.exercise_id AND p.language = ?
                WHERE p.status IN ('not_started', 'attempted')
                ORDER BY
                    CASE p.status WHEN 'attempted' THEN 0 ELSE 1 END,
                    e.id
                LIMIT 1
                """,
                [lang.value],
            ).fetchone()
            if not result:
                console.print(
                    f"[green]All done![/green] No unsolved {lang.value} exercises remaining."
                )
                conn.close()
                raise typer.Exit()
            exercise_id, topic, name = result
        elif exercise_id is not None:
            result = conn.execute(
                "SELECT topic, name FROM exercises WHERE id = ?", [exercise_id]
            ).fetchone()
            if not result:
                console.print(f"[red]Exercise {exercise_id} not found[/red]")
                conn.close()
                raise typer.Exit(1)
            topic, name = result
        else:
            console.print("[red]Provide an exercise ID or use --next[/red]")
            conn.close()
            raise typer.Exit(1)

        conn.close()

        file_path = _resolve_file(repo_root, topic, lang.value)
        if not file_path or not file_path.exists():
            console.print(
                f"[red]No source file found for topic '{topic}' in {lang.value}[/red]"
            )
            if file_path:
                console.print(f"[dim]Expected: {file_path}[/dim]")
            raise typer.Exit(1)

        emoji = LANG_EMOJI[lang.value]
        console.print(f"{emoji} Opening [cyan]#{exercise_id}[/cyan] {topic}: {name}")
        console.print(f"[dim]{file_path}[/dim]")
        try:
            subprocess.run([editor, str(file_path)])
        except KeyboardInterrupt:
            pass

    @app.command()
    def exercises():
        """Update exercises.md with current progress from database."""
        repo_root = get_repo_root()
        db_path = repo_root / DB_FILE

        if not db_path.exists():
            console.print("[yellow]No database found. Run 'init' first.[/yellow]")
            raise typer.Exit(1)

        update_exercises_file(repo_root, console)

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

        # Import here to avoid circular imports
        from .commands_study import get_study_activity_dates

        generate_progress_chart(
            repo_root,
            output_path,
            get_db=get_db,
            get_study_activity_dates=get_study_activity_dates,
            get_commit_dates=get_commit_dates,
        )

        conn = get_db(repo_root)
        topics = get_topic_progress_from_db(conn, "python")
        db_dates = get_activity_dates_from_db(conn)
        git_dates = get_commit_dates(repo_root)
        conn.close()

        total = sum(t["total"] for t in topics.values())
        py = sum(t["python"] for t in topics.values())
        current, longest, days = calculate_streaks(db_dates | git_dates, DEFAULT_YEAR)

        console.print(f"[green]Generated {output_path}[/green]")
        console.print(
            f"  Progress: {py}/{total} ({100 * py // total if total else 0}%)"
        )
        console.print(f"  Streak: {current} current, {longest} best, {days} total days")

    @app.command()
    def sync():
        """Update both exercises.md and progress.png from database."""
        repo_root = get_repo_root()
        db_path = repo_root / DB_FILE

        if not db_path.exists():
            console.print("[yellow]No database found. Run 'init' first.[/yellow]")
            raise typer.Exit(1)

        update_exercises_file(repo_root, console)

        os.chdir(repo_root)
        output_path = repo_root / "progress.png"
        console.print("[cyan]Generating progress chart...[/cyan]")

        # Import here to avoid circular imports
        from .commands_study import get_study_activity_dates

        generate_progress_chart(
            repo_root,
            output_path,
            get_db=get_db,
            get_study_activity_dates=get_study_activity_dates,
            get_commit_dates=get_commit_dates,
        )
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
  progress open LANG ID         Open exercise in $EDITOR
  progress open LANG --next     Open next unsolved exercise in $EDITOR

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

[cyan]Testing (via just)[/cyan]
  just test python              Run all Python 2026 tests
  just test py arrays           Python tests matching "arrays"
  just test js                  Run all TypeScript 2026 tests
  just test rust                Run all Rust tests
  just test rs arrays           Rust tests matching "arrays"
  just test all                 Run all languages

[dim]Languages: python|py | rust|rs | typescript|js|ts
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
                console.print(
                    "[yellow]No database found. Run 'progress init' to create one.[/yellow]"
                )
