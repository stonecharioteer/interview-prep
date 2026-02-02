# Study Tracker Implementation TODO

## Phase 1: Foundation
- [x] Create TODO.md tracking file

## Phase 2: Database Schema
- [x] Add books table
- [x] Add book_progress table
- [x] Add courses table
- [x] Add lectures table
- [x] Add lecture_progress table
- [x] Add homework table
- [x] Add homework_progress table
- [x] Add projects table
- [x] Add project_progress table
- [x] Add papers table
- [x] Add paper_progress table
- [x] Add course_books association table
- [x] Add lecture_chapters association table
- [x] Add course_papers association table
- [x] Add lecture_papers association table

## Phase 3: Book Commands
- [x] Add StudyStatus enum
- [x] Create study_app sub-app
- [x] Implement book-add command
- [x] Implement book-read command
- [x] Implement book-list command
- [x] Implement book-show command

## Phase 4: Course Commands
- [x] Implement course-add command
- [x] Implement lecture-add command
- [x] Implement watch command
- [x] Implement course-list command
- [x] Implement course-show command

## Phase 5: Homework & Project Commands
- [x] Implement homework-add command
- [x] Implement homework-done command
- [x] Implement project-add command
- [x] Implement project-done command

## Phase 5b: Paper Commands
- [x] Implement paper-add command
- [x] Implement paper-read command
- [x] Implement paper-list command

## Phase 5c: Association Commands
- [x] Implement course-book command
- [x] Implement lecture-chapters command
- [x] Implement course-paper command
- [x] Implement lecture-paper command
- [x] Display associations in course-show output

## Phase 6: Summary & Streak
- [x] Implement study summary (default callback)
- [x] Implement get_study_activity_dates()
- [x] Calculate study streak (separate from DSA)
- [x] Implement recent command

## Phase 7: Visualization
- [x] Add books section to progress.png
- [x] Add courses section to progress.png
- [x] Add papers section to progress.png
- [x] Add study streak calendar to progress.png (combined with DSA, color-coded)
- [x] Update generate_progress_chart() for combined view

## Phase 8: Justfile & Docs
- [x] Update `just progress` to be a pass-through alias (all args forwarded to progress.py)

## Phase 9: Book Chapter Progress Redesign
Replacing session-based tracking with chapter-level completion tracking.

### Database
- [x] Add chapter_progress table (book_id, chapter_number, progress_pct, updated_date)
- [x] Migrate/drop old book_progress table

### Commands
- [x] Update book-read to track chapter completion: `book-read ID --chapter N [--progress PCT]`
- [x] Support bulk completion: `book-read ID --chapters 1-3`
- [x] Update book-show to display per-chapter progress
- [x] Update book-list to show overall book completion percentage

### Visualization
- [x] Update get_study_data_for_chart to calculate book progress from chapter_progress
- [x] Show accurate book completion percentage in progress.png
