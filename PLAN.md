# Tasky: The Terminal Task Tracker

A beautiful and efficient task and time tracker for the terminal, designed to keep you focused and provide insights into your work habits.

## 1. Core Features

- **Interactive TUI:** A full-screen terminal application that is fully mouse and keyboard-driven.
- **Animated Timer:** A visually pleasing countdown timer for each task session (e.g., 25-minute Pomodoro).
- **Task Management:**
    - Input a `title` and `description` for each task session.
    - Start, pause, and stop the timer for the current session.
- **Project Grouping:** Assign each task session to a `project` to categorize your work.
- **Session Notes:** A dedicated area to jot down notes during an active session. All notes are saved and linked to the session.
- **Local Database:** All data is stored in a local `tasky.db` (SQLite) file in the project directory.

## 2. Awesome Suggestions (Enhancements)

- **Dashboard & Reporting:** A main screen that shows a summary of today's completed tasks, total time tracked per project, and a weekly activity graph.
- **Themes:** Allow the user to select from a few different color schemes (e.g., Solarized, Dracula, Gruvbox).
- **Custom Timers:** Allow configuration of timer lengths (work session, short break, long break).
- **Keyboard First:** Ensure the entire application can be used without touching the mouse, with intuitive shortcuts and Vim mode for all text inputs.
- **Data Export:** A feature to export task history for a given date range to CSV or JSON.
- **CLI for Quick Start:** A simple command-line interface to quickly start a task without opening the full TUI, e.g., `tasky start "My new task" --project "Work"`.

## 3. Technical Stack

- **Language:** Python 3.10+
- **TUI Framework:** [Textual](https://textual.textualize.io/)
- **Styling/Widgets:** [Rich](https://rich.readthedocs.io/en/latest/) (comes with Textual)
- **Database:** SQLite
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (for robust database interaction)

## 4. Data Model (Database Schema)

We'll need three main tables:

1.  **`projects`**
    - `id` (Integer, Primary Key)
    - `name` (String, Unique, Not Null)
    - `created_at` (DateTime)

2.  **`task_sessions`**
    - `id` (Integer, Primary Key)
    - `title` (String, Not Null)
    - `description` (Text)
    - `start_time` (DateTime, Not Null)
    - `end_time` (DateTime)
    - `duration_seconds` (Integer, Not Null)
    - `status` (String: "completed", "in_progress", "paused")
    - `project_id` (Integer, Foreign Key to `projects.id`)

3.  **`notes`**
    - `id` (Integer, Primary Key)
    - `content` (Text, Not Null)
    - `created_at` (DateTime, Not Null)
    - `session_id` (Integer, Foreign Key to `task_sessions.id`)

## 5. Development Phases

1.  **Phase 1: Setup & Core Models**
    - Set up the project structure (`pyproject.toml`, virtual environment).
    - Install dependencies (`textual`, `sqlalchemy`).
    - Create the database and table models using SQLAlchemy.

2.  **Phase 2: Basic UI Layout**
    - Create the main application screen using Textual.
    - Lay out the static UI components: a header, a main content area for the timer, a sidebar for projects/tasks, and a footer for instructions.

3.  **Phase 3: The Timer**
    - Implement the timer logic.
    - Create a custom Textual widget for the animated timer.
    - Add Start/Pause/Stop functionality.

4.  **Phase 4: Task & Project Management**
    - Create forms/dialogs to add new tasks and projects.
    - Connect the UI to the database to save a session when the timer is stopped.
    - Display a list of past tasks.

5.  **Phase 5: Note-Taking**
    - Add a text input area for notes that is active during a session.
    - Save notes to the database, linked to the current session.

6.  **Phase 6: Reporting & Polish**
    - Build the dashboard screen with summary statistics.
    - Implement themes and other enhancements.
    - Add tests.
