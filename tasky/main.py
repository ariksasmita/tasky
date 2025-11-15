from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button
from typing import Union
from textual.message import Message
from textual.reactive import reactive
import datetime

from .widgets.timer import Timer
from .widgets.project_list import ProjectList
from .widgets.project_dialog import ProjectDialog
from .widgets.task_dialog import TaskDialog # New import
from .database import add_project, create_task_session, update_task_session # Updated import
from .models import TaskSession # New import

class TaskyApp(App):
    """A Textual app to manage tasks and track time."""

    BINDINGS = [
        ("s", "start_timer", "Start"),
        ("p", "pause_timer", "Pause"),
        ("r", "reset_timer", "Reset"),
        ("a", "add_project", "Add Project"),
        ("n", "new_task", "New Task"), # New binding
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    current_task_session: reactive[Union[TaskSession, None]] = reactive(None)

    CSS = """
    Screen {
        layout: vertical;
    }

    #main-container {
        layout: horizontal;
        height: 1fr;
    }

    #sidebar {
        width: 30;
        border-right: heavy steelblue;
        padding: 1 2;
    }

    #content-area {
        width: 1fr;
        padding: 1 2;
        align: center middle;
    }
    
    #current-task-display {
        width: 80%;
        height: auto;
        text-align: center;
        text-style: bold;
        color: green;
        margin-bottom: 1;
    }

    #timer-display {
        width: 80%;
        height: 50%;
        content-align: center middle;
        border: round steelblue;
        margin-bottom: 1;
    }

    #timer-controls {
        width: 80%;
        height: auto;
        layout: horizontal;
        align: center middle;
        margin-top: 1;
    }

    #timer-controls Button {
        margin: 0 1;
        width: 1fr;
    }

    #notes-area {
        height: 1fr;
        margin-top: 2;
        border: round gray;
        padding: 1;
    }
    
    #sidebar-title {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: steelblue;
        margin-bottom: 1;
    }

    #project-dialog-container, #task-dialog-container {
        width: 60%;
        height: auto;
        background: $panel;
        border: thick $accent;
        padding: 2;
        align: center middle;
    }

    #project-dialog-buttons, #task-dialog-buttons {
        margin-top: 1;
        layout: horizontal;
        width: 100%;
        align: center middle;
    }

    #project-dialog-buttons Button, #task-dialog-buttons Button {
        margin: 0 1;
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield Static("PROJECTS", id="sidebar-title")
                yield ProjectList(id="project-list")
            with Vertical(id="content-area"):
                yield Static("No task active", id="current-task-display") # Display current task
                yield Timer(id="timer-display")
                with Horizontal(id="timer-controls"):
                    yield Button("Start", id="start-button", variant="success")
                    yield Button("Pause", id="pause-button", variant="warning")
                    yield Button("Reset", id="reset-button", variant="error")
                yield Static("Notes Area\n\n[Coming Soon]", id="notes-area")
        yield Footer()

    def watch_current_task_session(self, task_session: Union[TaskSession, None]) -> None:
        """Update the display when the current task session changes."""
        if task_session:
            self.query_one("#current-task-display", Static).update(f"Current Task: {task_session.title}")
        else:
            self.query_one("#current-task-display", Static).update("No task active")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        timer_widget = self.query_one(Timer)
        if event.button.id == "start-button":
            if self.current_task_session: # Only start if a task is selected
                timer_widget.start()
            else:
                self.notify("Please start a new task first (N)", title="Info")
        elif event.button.id == "pause-button":
            timer_widget.pause()
            if self.current_task_session:
                update_task_session(
                    self.current_task_session.id,
                    datetime.datetime.utcnow(),
                    timer_widget.initial_duration - timer_widget.time_remaining,
                    "paused"
                )
        elif event.button.id == "reset-button":
            timer_widget.reset()
            if self.current_task_session:
                update_task_session(
                    self.current_task_session.id,
                    datetime.datetime.utcnow(),
                    0, # Reset duration
                    "reset" # Or "cancelled"
                )
                self.current_task_session = None # Clear current task
        elif event.button.id == "add-project-button":
            self.action_add_project()
        elif event.button.id == "new-task-button": # Assuming a button for new task in future
            self.action_new_task()

    def action_start_timer(self) -> None:
        """An action to start the timer."""
        if self.current_task_session:
            self.query_one(Timer).start()
        else:
            self.notify("Please start a new task first (N)", title="Info")

    def action_pause_timer(self) -> None:
        """An action to pause the timer."""
        timer_widget = self.query_one(Timer)
        timer_widget.pause()
        if self.current_task_session:
            update_task_session(
                self.current_task_session.id,
                datetime.datetime.utcnow(),
                timer_widget.initial_duration - timer_widget.time_remaining,
                "paused"
            )

    def action_reset_timer(self) -> None:
        """An action to reset the timer."""
        timer_widget = self.query_one(Timer)
        timer_widget.reset()
        if self.current_task_session:
            update_task_session(
                self.current_task_session.id,
                datetime.datetime.utcnow(),
                0,
                "reset"
            )
            self.current_task_session = None

    def action_add_project(self) -> None:
        """An action to add a new project."""
        def handle_project_name(project_name: Union[str, None]) -> None:
            if project_name:
                new_project = add_project(project_name)
                if new_project:
                    self.query_one(ProjectList).load_projects()
                    self.notify(f"Project '{new_project.name}' added!", title="Success")
                else:
                    self.notify(f"Project '{project_name}' already exists or could not be added.", title="Error", severity="error")
            else:
                self.notify("Project creation cancelled.", title="Info")

        self.push_screen(ProjectDialog(), handle_project_name)

    def action_new_task(self) -> None:
        """An action to start a new task."""
        def handle_task_data(task_data: Union[dict, None]) -> None:
            if task_data:
                new_session = create_task_session(
                    task_data["title"],
                    task_data["description"],
                    task_data["project_id"]
                )
                self.current_task_session = new_session
                timer_widget = self.query_one(Timer)
                timer_widget.set_duration(1500) # Default to 25 minutes
                timer_widget.start()
                self.notify(f"Task '{new_session.title}' started!", title="Success")
            else:
                self.notify("Task creation cancelled.", title="Info")
        
        self.push_screen(TaskDialog(), handle_task_data)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_timer_timer_finished(self, message: Timer.TimerFinished) -> None:
        """Handle timer finished message."""
        self.bell()
        self.notify("Timer Finished!", title="Tasky")
        if self.current_task_session:
            timer_widget = self.query_one(Timer)
            update_task_session(
                self.current_task_session.id,
                datetime.datetime.utcnow(),
                timer_widget.initial_duration, # Full duration completed
                "completed"
            )
            self.current_task_session = None # Clear current task
