from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button
from textual.message import Message

from .widgets.timer import Timer

class TaskyApp(App):
    """A Textual app to manage tasks and track time."""

    BINDINGS = [
        ("s", "start_timer", "Start"),
        ("p", "pause_timer", "Pause"),
        ("r", "reset_timer", "Reset"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

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
        align: center middle; /* Corrected alignment */
    }
    
    #timer-display {
        width: 80%; /* Make timer take up more space */
        height: 50%; /* Adjust height */
        content-align: center middle;
        border: round steelblue;
        /* font-size: 10; */ /* Removed invalid property */
        margin-bottom: 1;
    }

    #timer-controls {
        width: 80%;
        height: auto;
        layout: horizontal;
        align: center middle; /* Corrected alignment */
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
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield Static("PROJECTS", id="sidebar-title")
                yield Static("\n[Coming Soon]", id="sidebar-content")
            with Vertical(id="content-area"):
                yield Timer(id="timer-display")
                with Horizontal(id="timer-controls"):
                    yield Button("Start", id="start-button", variant="success")
                    yield Button("Pause", id="pause-button", variant="warning")
                    yield Button("Reset", id="reset-button", variant="error")
                yield Static("Notes Area\n\n[Coming Soon]", id="notes-area")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        timer_widget = self.query_one(Timer)
        if event.button.id == "start-button":
            timer_widget.start()
        elif event.button.id == "pause-button":
            timer_widget.pause()
        elif event.button.id == "reset-button":
            timer_widget.reset()

    def action_start_timer(self) -> None:
        """An action to start the timer."""
        self.query_one(Timer).start()

    def action_pause_timer(self) -> None:
        """An action to pause the timer."""
        self.query_one(Timer).pause()

    def action_reset_timer(self) -> None:
        """An action to reset the timer."""
        self.query_one(Timer).reset()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_timer_timer_finished(self, message: Timer.TimerFinished) -> None:
        """Handle timer finished message."""
        self.bell() # Play a sound
        self.notify("Timer Finished!", title="Tasky")
        # Here you might want to automatically start a break timer or prompt the user

def main():
    """Run the Textual application."""
    app = TaskyApp()
    app.run()

if __name__ == "__main__":
    main()
