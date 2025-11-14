from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.message import Message
from textual.timer import Timer as TextualTimer
from textual.widgets import Static
from textual.widget import Widget


class Timer(Static):
    """A custom Textual widget for a countdown timer."""

    DEFAULT_CLASSES = "timer"

    # Reactive attributes for time and state
    time_remaining = reactive(1500)  # Default to 25 minutes (1500 seconds)
    is_running = reactive(False)
    is_paused = reactive(False)
    initial_duration = reactive(1500) # Store initial duration for reset

    class TimerFinished(Message):
        """Posted when the timer reaches zero."""
        def __init__(self, sender: Widget) -> None:
            super().__init__(sender)

    def watch_time_remaining(self, time_remaining: int) -> None:
        """Called when time_remaining changes."""
        self.update_display()
        if time_remaining <= 0 and self.is_running:
            self.is_running = False
            self.is_paused = False
            self.post_message(self.TimerFinished(self))

    def watch_is_running(self, is_running: bool) -> None:
        """Called when is_running changes."""
        if is_running:
            self.start_timer_interval()
        else:
            self.stop_timer_interval()

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_display()

    def update_display(self) -> None:
        """Updates the timer display."""
        minutes, seconds = divmod(self.time_remaining, 60)
        self.update(f"{minutes:02d}:{seconds:02d}")

    def start_timer_interval(self) -> None:
        """Starts the interval timer."""
        if not hasattr(self, "_timer_interval") or self._timer_interval is None:
            self._timer_interval = self.set_interval(1, self.tick, pause=self.is_paused)

    def stop_timer_interval(self) -> None:
        """Stops the interval timer."""
        if hasattr(self, "_timer_interval") and self._timer_interval is not None:
            self._timer_interval.pause()
            self._timer_interval = None

    def tick(self) -> None:
        """Decrements the timer by one second."""
        if self.is_running and not self.is_paused:
            self.time_remaining -= 1

    def start(self) -> None:
        """Starts or resumes the timer."""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
        elif self.is_paused:
            self.is_paused = False
            if hasattr(self, "_timer_interval") and self._timer_interval is not None:
                self._timer_interval.resume()

    def pause(self) -> None:
        """Pauses the timer."""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            if hasattr(self, "_timer_interval") and self._timer_interval is not None:
                self._timer_interval.pause()

    def reset(self) -> None:
        """Resets the timer to its initial duration."""
        self.is_running = False
        self.is_paused = False
        self.time_remaining = self.initial_duration
        self.update_display()

    def set_duration(self, seconds: int) -> None:
        """Sets the initial duration of the timer."""
        self.initial_duration = seconds
        self.reset()