from textual.app import ComposeResult
from textual.widgets import Static, Button, ListView, ListItem, Label
from textual.containers import Vertical
from textual.reactive import reactive

from ..database import SessionLocal
from ..models import Project

class ProjectList(Vertical):
    """A widget to display a list of projects."""

    projects = reactive([])

    def compose(self) -> ComposeResult:
        yield Button("Add New Project", id="add-project-button", variant="primary")
        yield ListView(id="project-list-view")

    def on_mount(self) -> None:
        self.load_projects()

    def load_projects(self) -> None:
        with SessionLocal() as session:
            projects_from_db = session.query(Project).order_by(Project.name).all()
            self.projects = projects_from_db
            self.update_list_view()

    def update_list_view(self) -> None:
        list_view = self.query_one("#project-list-view", ListView)
        list_view.clear()
        for project in self.projects:
            list_view.append(ListItem(Label(project.name), name=str(project.id)))

    def watch_projects(self, old_projects, new_projects) -> None:
        """Called when the projects reactive attribute changes."""
        self.update_list_view()

