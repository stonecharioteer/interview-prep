"""Database connection and schema management."""

from pathlib import Path

import duckdb

from .models import DB_FILE


def get_repo_root() -> Path:
    return Path(__file__).parent.parent.parent


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
