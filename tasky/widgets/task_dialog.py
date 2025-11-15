from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Footer, Input, Label, Select, TextArea
from textual.validation import Validator, ValidationResult

from ..database import get_all_projects
from ..models import Project

class NotEmptyValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if not value.strip():
            return self.failure("Cannot be empty")
        return self.success()

class TaskDialog(ModalScreen[dict]):
    """Modal screen for adding a new task."""

    BINDINGS = [
        ("escape", "dismiss()", "Dismiss"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.projects_data = []

    def on_mount(self) -> None:
        self.load_projects_for_select()
        self.query_one("#task-title-input", Input).focus()

    def load_projects_for_select(self) -> None:
        projects = get_all_projects()
        self.projects_data = [(project.name, project.id) for project in projects]
        project_select = self.query_one("#project-select", Select)
        project_select.set_options(self.projects_data)
        if self.projects_data:
            project_select.value = self.projects_data[0][1] # Select first project by default

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="task-dialog-container"):
            yield Label("Task Title:")
            yield Input(placeholder="Task Title", id="task-title-input", validators=[NotEmptyValidator()])
            yield Label("Description (Optional):")
            yield TextArea(placeholder="Task Description", id="task-description-input")
            yield Label("Project:")
            yield Select([], id="project-select")
            with Horizontal(id="task-dialog-buttons"):
                yield Button("Start Task", variant="success", id="start-task-button")
                yield Button("Cancel", variant="default", id="cancel-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-task-button":
            title_input = self.query_one("#task-title-input", Input)
            description_input = self.query_one("#task-description-input", TextArea)
            project_select = self.query_one("#project-select", Select)

            if title_input.validate_value(title_input.value):
                task_data = {
                    "title": title_input.value,
                    "description": description_input.text,
                    "project_id": project_select.value,
                }
                self.dismiss(task_data)
            else:
                self.notify("Task title cannot be empty.", severity="error")

        elif event.button.id == "cancel-button":
            self.dismiss()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # If Enter is pressed in the title field, move focus to description
        if event.input.id == "task-title-input":
            self.query_one("#task-description-input", TextArea).focus()
        # If Enter is pressed in description, move to project select
        elif event.input.id == "task-description-input":
            self.query_one("#project-select", Select).focus()
