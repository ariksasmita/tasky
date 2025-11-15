from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Footer, Input, Label

class ProjectDialog(ModalScreen[str]):
    """Modal screen for adding a new project."""

    BINDINGS = [
        ("escape", "dismiss()", "Dismiss"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="project-dialog-container"):
            yield Label("Enter Project Name:")
            yield Input(placeholder="New Project Name", id="project-name-input")
            with Vertical(id="project-dialog-buttons"):
                yield Button("Add Project", variant="success", id="add-project-button")
                yield Button("Cancel", variant="default", id="cancel-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-project-button":
            project_name = self.query_one("#project-name-input", Input).value
            if project_name:
                self.dismiss(project_name)
            else:
                # Optionally, add some visual feedback for empty input
                pass
        elif event.button.id == "cancel-button":
            self.dismiss()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # If Enter is pressed in the input field, treat it as "Add Project"
        project_name = self.query_one("#project-name-input", Input).value
        if project_name:
            self.dismiss(project_name)
        else:
            pass

    def on_mount(self) -> None:
        self.query_one("#project-name-input", Input).focus()

