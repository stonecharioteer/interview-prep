"""Study tracking commands (books, courses, papers)."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Optional

import duckdb
import typer
from rich.console import Console
from rich.table import Table

from .db import get_db, get_repo_root
from .models import DB_FILE, DEFAULT_YEAR, STUDY_STATUS_SYMBOL, StudyStatus
from .visualization import calculate_streaks, parse_chapters_string
from .interactive import prompt_select_from_list, prompt_text, prompt_int

console = Console()


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


def register_commands(study_app: typer.Typer) -> None:
    """Register study commands with the study_app."""

    # ============ Book Commands ============

    @study_app.command("book-add")
    def book_add(
        title: Annotated[Optional[str], typer.Argument(help="Book title")] = None,
        author: Annotated[Optional[str], typer.Option("--author", "-a", help="Author name")] = None,
        chapters: Annotated[Optional[int], typer.Option("--chapters", "-c", help="Total chapters")] = None,
        url: Annotated[Optional[str], typer.Option("--url", help="Book URL")] = None,
    ):
        """Add a book to track."""
        # Interactive mode: prompt for title if not provided
        if title is None:
            title = prompt_text("Book title")

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
        book_id: Annotated[Optional[int], typer.Argument(help="Book ID")] = None,
        chapter: Annotated[Optional[int], typer.Option("--chapter", "-c", help="Single chapter number")] = None,
        chapters: Annotated[Optional[str], typer.Option("--chapters", help="Chapter range (e.g., '1-3' or '5,7')")] = None,
        progress: Annotated[int, typer.Option("--progress", "-p", help="Progress percentage (default: 100)")] = 100,
        date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
    ):
        """Mark chapter(s) as read with optional progress percentage."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for book if not provided
        if book_id is None:
            books = conn.execute("""
                SELECT id, title || COALESCE(' by ' || author, '') as display
                FROM books
                ORDER BY id
            """).fetchall()
            if not books:
                console.print("[yellow]No books tracked yet. Use 'progress study book-add' to add one.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            book_id = prompt_select_from_list(
                [(b[0], b[1]) for b in books],
                "Select book"
            )

        book = conn.execute("SELECT title, total_chapters FROM books WHERE id = ?", [book_id]).fetchone()
        if not book:
            console.print(f"[red]Book #{book_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        book_title, total_chapters = book

        # Interactive mode: prompt for chapter if not provided
        if chapter is None and chapters is None:
            chapter = prompt_int("Chapter number")

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
            console.print(f"[green]Updated:[/green] Chapter {ch} of \"{book_title}\" \u2192 {progress}%")
        else:
            ch_list = ", ".join(str(c) for c in sorted(chapter_nums))
            console.print(f"[green]Updated:[/green] Chapters {ch_list} of \"{book_title}\" \u2192 {progress}%")

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
        book_id: Annotated[Optional[int], typer.Argument(help="Book ID")] = None,
    ):
        """Show book details and chapter progress."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for book if not provided
        if book_id is None:
            books = conn.execute("""
                SELECT id, title || COALESCE(' by ' || author, '') as display
                FROM books
                ORDER BY id
            """).fetchall()
            if not books:
                console.print("[yellow]No books tracked yet. Use 'progress study book-add' to add one.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            book_id = prompt_select_from_list(
                [(b[0], b[1]) for b in books],
                "Select book"
            )

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
        name: Annotated[Optional[str], typer.Argument(help="Course name")] = None,
        source: Annotated[Optional[str], typer.Option("--source", "-s", help="Source (e.g., CMU, MIT)")] = None,
        code: Annotated[Optional[str], typer.Option("--code", "-c", help="Course code (e.g., 15-445)")] = None,
        url: Annotated[Optional[str], typer.Option("--url", help="Playlist URL")] = None,
    ):
        """Add a course to track."""
        # Interactive mode: prompt for name if not provided
        if name is None:
            name = prompt_text("Course name")

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
        course_id: Annotated[Optional[int], typer.Argument(help="Course ID")] = None,
        title: Annotated[Optional[str], typer.Argument(help="Lecture title")] = None,
        number: Annotated[Optional[int], typer.Option("--number", "-n", help="Lecture number (auto-increments if not provided)")] = None,
        url: Annotated[Optional[str], typer.Option("--url", help="Video URL")] = None,
    ):
        """Add a lecture to a course."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for course if not provided
        if course_id is None:
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet. Use 'progress study course-add' to add one.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )

        course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
        if not course:
            console.print(f"[red]Course #{course_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for title if not provided
        if title is None:
            title = prompt_text("Lecture title")

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
        course_id: Annotated[Optional[int], typer.Argument(help="Course ID")] = None,
        lecture_number: Annotated[Optional[int], typer.Argument(help="Lecture number")] = None,
        status: Annotated[StudyStatus, typer.Option("--status", "-s", help="Status")] = StudyStatus.completed,
        date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
    ):
        """Mark a lecture as watched."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for course if not provided
        if course_id is None:
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet. Use 'progress study course-add' to add one.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )

        # Interactive mode: prompt for lecture if not provided
        if lecture_number is None:
            lectures = conn.execute("""
                SELECT l.lecture_number, '#' || l.lecture_number || ' ' || l.title as display
                FROM lectures l
                WHERE l.course_id = ?
                ORDER BY l.lecture_number
            """, [course_id]).fetchall()
            if not lectures:
                console.print(f"[yellow]No lectures found for course #{course_id}.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            lecture_number = prompt_select_from_list(
                [(l[0], l[1]) for l in lectures],
                "Select lecture"
            )

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
            GROUP BY c.id, c.name, c.source, c.code
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
                str(last_watched) if last_watched else "-",
            )

        console.print(table)

    @study_app.command("course-show")
    def course_show(
        course_id: Annotated[Optional[int], typer.Argument(help="Course ID")] = None,
    ):
        """Show course details with lecture progress."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for course if not provided
        if course_id is None:
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet. Use 'progress study course-add' to add one.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )

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
        lecture_id: Annotated[Optional[int], typer.Argument(help="Lecture ID")] = None,
        name: Annotated[Optional[str], typer.Argument(help="Homework name")] = None,
        url: Annotated[Optional[str], typer.Option("--url", help="Homework URL")] = None,
    ):
        """Add homework to a lecture."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for lecture if not provided
        if lecture_id is None:
            # First select course
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )
            # Then select lecture
            lectures = conn.execute("""
                SELECT l.id, '#' || l.lecture_number || ' ' || l.title as display
                FROM lectures l
                WHERE l.course_id = ?
                ORDER BY l.lecture_number
            """, [course_id]).fetchall()
            if not lectures:
                console.print(f"[yellow]No lectures found for course #{course_id}.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            lecture_id = prompt_select_from_list(
                [(l[0], l[1]) for l in lectures],
                "Select lecture"
            )

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

        # Interactive mode: prompt for name if not provided
        if name is None:
            name = prompt_text("Homework name")

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
        homework_id: Annotated[Optional[int], typer.Argument(help="Homework ID")] = None,
        date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
    ):
        """Mark homework as completed."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for homework if not provided
        if homework_id is None:
            homework = conn.execute("""
                SELECT h.id, h.name || ' (' || c.name || ')' as display
                FROM homework h
                JOIN lectures l ON h.lecture_id = l.id
                JOIN courses c ON l.course_id = c.id
                LEFT JOIN homework_progress hp ON h.id = hp.homework_id
                WHERE hp.status IS NULL OR hp.status != 'completed'
                ORDER BY h.id
            """).fetchall()
            if not homework:
                console.print("[yellow]No pending homework found.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            homework_id = prompt_select_from_list(
                [(h[0], h[1]) for h in homework],
                "Select homework"
            )

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
        course_id: Annotated[Optional[int], typer.Argument(help="Course ID")] = None,
        name: Annotated[Optional[str], typer.Argument(help="Project name")] = None,
        url: Annotated[Optional[str], typer.Option("--url", help="Project URL")] = None,
    ):
        """Add a project to a course."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for course if not provided
        if course_id is None:
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet. Use 'progress study course-add' to add one.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )

        course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
        if not course:
            console.print(f"[red]Course #{course_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for name if not provided
        if name is None:
            name = prompt_text("Project name")

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
        project_id: Annotated[Optional[int], typer.Argument(help="Project ID")] = None,
        date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
    ):
        """Mark project as completed."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for project if not provided
        if project_id is None:
            projects = conn.execute("""
                SELECT p.id, p.name || ' (' || c.name || ')' as display
                FROM projects p
                JOIN courses c ON p.course_id = c.id
                LEFT JOIN project_progress pp ON p.id = pp.project_id
                WHERE pp.status IS NULL OR pp.status != 'completed'
                ORDER BY p.id
            """).fetchall()
            if not projects:
                console.print("[yellow]No pending projects found.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            project_id = prompt_select_from_list(
                [(p[0], p[1]) for p in projects],
                "Select project"
            )

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
        title: Annotated[Optional[str], typer.Argument(help="Paper title")] = None,
        authors: Annotated[Optional[str], typer.Option("--authors", "-a", help="Authors")] = None,
        url: Annotated[Optional[str], typer.Option("--url", help="Paper URL")] = None,
        year: Annotated[Optional[int], typer.Option("--year", "-y", help="Publication year")] = None,
    ):
        """Add a paper to track."""
        # Interactive mode: prompt for title if not provided
        if title is None:
            title = prompt_text("Paper title")

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
        paper_id: Annotated[Optional[int], typer.Argument(help="Paper ID")] = None,
        status: Annotated[StudyStatus, typer.Option("--status", "-s", help="Status")] = StudyStatus.completed,
        date: Annotated[Optional[str], typer.Option("--date", "-d", help="Date (YYYY-MM-DD, default: today)")] = None,
    ):
        """Mark a paper as reading or completed."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for paper if not provided
        if paper_id is None:
            papers = conn.execute("""
                SELECT p.id, p.title || COALESCE(' (' || p.authors || ')', '') as display
                FROM papers p
                LEFT JOIN paper_progress pp ON p.id = pp.paper_id
                WHERE pp.status IS NULL OR pp.status != 'completed'
                ORDER BY p.id
            """).fetchall()
            if not papers:
                console.print("[yellow]No unread papers found.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            paper_id = prompt_select_from_list(
                [(p[0], p[1]) for p in papers],
                "Select paper"
            )

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
        course_id: Annotated[Optional[int], typer.Argument(help="Course ID")] = None,
        book_id: Annotated[Optional[int], typer.Argument(help="Book ID")] = None,
    ):
        """Associate a book with a course (required reading)."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for course if not provided
        if course_id is None:
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )

        course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
        if not course:
            console.print(f"[red]Course #{course_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for book if not provided
        if book_id is None:
            books = conn.execute("""
                SELECT id, title || COALESCE(' by ' || author, '') as display
                FROM books
                ORDER BY id
            """).fetchall()
            if not books:
                console.print("[yellow]No books tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            book_id = prompt_select_from_list(
                [(b[0], b[1]) for b in books],
                "Select book"
            )

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
        lecture_id: Annotated[Optional[int], typer.Argument(help="Lecture ID")] = None,
        book_id: Annotated[Optional[int], typer.Argument(help="Book ID")] = None,
        chapters: Annotated[Optional[str], typer.Argument(help="Chapters (e.g., '1-3' or '5,7')")] = None,
    ):
        """Associate specific chapters with a lecture."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for lecture if not provided
        if lecture_id is None:
            # First select course
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )
            # Then select lecture
            lectures = conn.execute("""
                SELECT l.id, '#' || l.lecture_number || ' ' || l.title as display
                FROM lectures l
                WHERE l.course_id = ?
                ORDER BY l.lecture_number
            """, [course_id]).fetchall()
            if not lectures:
                console.print(f"[yellow]No lectures found for course #{course_id}.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            lecture_id = prompt_select_from_list(
                [(l[0], l[1]) for l in lectures],
                "Select lecture"
            )

        lecture = conn.execute("SELECT title FROM lectures WHERE id = ?", [lecture_id]).fetchone()
        if not lecture:
            console.print(f"[red]Lecture #{lecture_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for book if not provided
        if book_id is None:
            books = conn.execute("""
                SELECT id, title || COALESCE(' by ' || author, '') as display
                FROM books
                ORDER BY id
            """).fetchall()
            if not books:
                console.print("[yellow]No books tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            book_id = prompt_select_from_list(
                [(b[0], b[1]) for b in books],
                "Select book"
            )

        book = conn.execute("SELECT title FROM books WHERE id = ?", [book_id]).fetchone()
        if not book:
            console.print(f"[red]Book #{book_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for chapters if not provided
        if chapters is None:
            chapters = prompt_text("Chapters (e.g., '1-3' or '5,7')")

        conn.execute("""
            INSERT OR REPLACE INTO lecture_chapters (lecture_id, book_id, chapters)
            VALUES (?, ?, ?)
        """, [lecture_id, book_id, chapters])
        conn.close()

        console.print(f"[green]Associated:[/green] Chapters {chapters} of \"{book[0]}\" with \"{lecture[0]}\"")

    @study_app.command("course-paper")
    def course_paper(
        course_id: Annotated[Optional[int], typer.Argument(help="Course ID")] = None,
        paper_id: Annotated[Optional[int], typer.Argument(help="Paper ID")] = None,
    ):
        """Associate a paper with a course."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for course if not provided
        if course_id is None:
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )

        course = conn.execute("SELECT name FROM courses WHERE id = ?", [course_id]).fetchone()
        if not course:
            console.print(f"[red]Course #{course_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for paper if not provided
        if paper_id is None:
            papers = conn.execute("""
                SELECT id, title || COALESCE(' (' || authors || ')', '') as display
                FROM papers
                ORDER BY id
            """).fetchall()
            if not papers:
                console.print("[yellow]No papers tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            paper_id = prompt_select_from_list(
                [(p[0], p[1]) for p in papers],
                "Select paper"
            )

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
        lecture_id: Annotated[Optional[int], typer.Argument(help="Lecture ID")] = None,
        paper_id: Annotated[Optional[int], typer.Argument(help="Paper ID")] = None,
    ):
        """Associate a paper with a lecture."""
        repo_root = get_repo_root()
        conn = get_db(repo_root)

        # Interactive mode: prompt for lecture if not provided
        if lecture_id is None:
            # First select course
            courses = conn.execute("""
                SELECT id, COALESCE(source || ' ', '') || COALESCE(code || ' ', '') || name as display
                FROM courses
                ORDER BY id
            """).fetchall()
            if not courses:
                console.print("[yellow]No courses tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            course_id = prompt_select_from_list(
                [(c[0], c[1]) for c in courses],
                "Select course"
            )
            # Then select lecture
            lectures = conn.execute("""
                SELECT l.id, '#' || l.lecture_number || ' ' || l.title as display
                FROM lectures l
                WHERE l.course_id = ?
                ORDER BY l.lecture_number
            """, [course_id]).fetchall()
            if not lectures:
                console.print(f"[yellow]No lectures found for course #{course_id}.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            lecture_id = prompt_select_from_list(
                [(l[0], l[1]) for l in lectures],
                "Select lecture"
            )

        lecture = conn.execute("SELECT title FROM lectures WHERE id = ?", [lecture_id]).fetchone()
        if not lecture:
            console.print(f"[red]Lecture #{lecture_id} not found[/red]")
            conn.close()
            raise typer.Exit(1)

        # Interactive mode: prompt for paper if not provided
        if paper_id is None:
            papers = conn.execute("""
                SELECT id, title || COALESCE(' (' || authors || ')', '') as display
                FROM papers
                ORDER BY id
            """).fetchall()
            if not papers:
                console.print("[yellow]No papers tracked yet.[/yellow]")
                conn.close()
                raise typer.Exit(1)
            paper_id = prompt_select_from_list(
                [(p[0], p[1]) for p in papers],
                "Select paper"
            )

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
            detail = f"Ch {chapter} \u2192 {pct}%"
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
