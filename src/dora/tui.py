from typing import ClassVar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.timer import Timer
from textual.widgets import Button, Checkbox, Input, Label, Static

Checkbox.BUTTON_INNER = "✓"

DORA_LOGO = r"""
 ____   ___  ____      _
|  _ \ / _ \|  _ \    / \
| | | | | | | |_) |  / _ \
| |_| | |_| |  _ <  / ___ \
|____/ \___/|_| \_\/_/   \_\

Data-Oriented Report Automator
"""


class DoraTUI(App):
    """An inline TUI for DORA configuration."""

    _column_load_timer: Timer | None = None
    _latest_path: str = ""

    CSS = """
    Screen {
        background: transparent;
        padding: 1 2;
    }
    #logo {
        color: #38bdf8;
        text-style: bold;
        margin-bottom: 2;
        margin-left: 1;
    }
    #form-container {
        width: 100%;
        height: auto;
        background: transparent;
    }
    .section-title {
        color: #94a3b8;
        text-style: bold;
        margin-bottom: 1;
        margin-top: 2;
        margin-left: 1;
    }
    .row {
        height: auto;
        margin-bottom: 1;
    }
    Label {
        width: 18;
        content-align: right middle;
        margin-right: 2;
        color: #cbd5e1;
    }
    Input {
        width: 55;
        height: 1;
        padding: 0 1;
        background: #1e293b;
        border: none;
    }
    Input:focus {
        background: #334155;
        border: none;
    }
    .check-row {
        height: auto;
        margin-bottom: 1;
        margin-left: 20;
    }
    Checkbox {
        background: transparent;
        border: none;
        height: auto;
    }
    Checkbox:focus {
        border: none;
        background: #334155;
    }
    Button {
        width: 30;
        margin-top: 2;
        margin-left: 21;
        background: #0ea5e9;
        color: white;
        text-style: bold;
        border: none;
    }
    Button:hover, Button:focus {
        background: #0284c7;
    }
    #quit-label {
        color: #64748b;
        margin-top: 1;
        margin-left: 21;
        width: 30;
        content-align: center middle;
    }
    .hidden {
        display: none;
    }
    #status-label {
        margin-left: 21;
        margin-bottom: 1;
        text-style: bold;
    }
    .status-success {
        color: #10b981;
    }
    .status-error {
        color: #ef4444;
    }
    .status-loading {
        color: #eab308;
    }
    """

    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [
        ("ctrl+q", "quit", "Quit"),
        ("up", "focus_previous", "Previous"),
        ("down", "focus_next", "Next"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="form-container"):
            yield Static(DORA_LOGO, id="logo")

            yield Static("Dataset Settings", classes="section-title")
            with Horizontal(classes="row"):
                yield Label("Input/URL:")
                yield Input(placeholder="Path or Kaggle URL (owner/dataset)", id="input_file")
            
            yield Label("", id="status-label")

            with Container(id="further-steps", classes="hidden"):
                with Horizontal(classes="row"):
                    yield Label("Save to path:")
                    yield Input(value="output", id="output_dir")
                with Horizontal(classes="row"):
                    yield Label("Report Title:")
                    yield Input(value="EDA Report", id="report_title")
                with Horizontal(classes="row"):
                    yield Label("Target variable:")
                    yield Input(placeholder="Target column name (optional)", id="target_variable")

                yield Static("Analysis Pipeline", classes="section-title")
                with Vertical(classes="check-row"):
                    yield Checkbox("Profile (Overview, missing values, stats)", value=True, id="step_profile")
                    yield Checkbox("Univariate (Distributions for single columns)", value=True, id="step_univariate")
                    yield Checkbox("Bivariate (Relationships with target variable)", value=True, id="step_bivariate")
                    yield Checkbox("Multivariate (Correlation matrix)", value=True, id="step_multivariate")

                yield Button("Run Analysis", variant="primary", id="run_btn")
            
            yield Static("Press 'Ctrl+Q' to quit", id="quit-label")

    def _submit(self) -> None:
        if self.query_one("#further-steps").has_class("hidden"):
            return

        input_file = self.query_one("#input_file", Input).value.strip()
        if not input_file:
            self.notify("Input/URL is required to run DORA!", severity="error")
            return

        output_dir = self.query_one("#output_dir", Input).value.strip()
        report_title = self.query_one("#report_title", Input).value.strip()
        target_variable = self.query_one("#target_variable", Input).value.strip()

        profile = self.query_one("#step_profile", Checkbox).value
        univariate = self.query_one("#step_univariate", Checkbox).value
        bivariate = self.query_one("#step_bivariate", Checkbox).value
        multivariate = self.query_one("#step_multivariate", Checkbox).value

        self.exit(
            {
                "input_file": input_file,
                "output_dir": output_dir,
                "report_title": report_title,
                "target_variable": target_variable if target_variable else None,
                "profile_enabled": profile,
                "univariate_enabled": univariate,
                "bivariate_enabled": bivariate,
                "multivariate_enabled": multivariate,
            }
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press to submit the form."""
        if event.button.id == "run_btn":
            self._submit()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key pressed inside any input field."""
        self._submit()

    from textual import work

    @work(thread=True)
    def load_columns(self, path: str) -> None:
        import logging
        import os

        import pandas as pd
        from textual.suggester import SuggestFromList

        from dora.kaggle import download_files, extract_dataset_id, is_kaggle_url

        def set_status(text: str, status_class: str) -> None:
            if self._latest_path != path:
                return
            lbl = self.query_one("#status-label", Label)
            lbl.update(text)
            lbl.remove_class("status-success", "status-error", "status-loading")
            lbl.add_class(status_class)

        def reveal_steps(cols: list[str]) -> None:
            if self._latest_path != path:
                return
            self.query_one("#further-steps").remove_class("hidden")
            target_input = self.query_one("#target_variable", Input)
            target_input.suggester = SuggestFromList([str(c) for c in cols], case_sensitive=False)
            set_status(f"✓ Successfully loaded {len(cols)} columns.", "status-success")

        def hide_steps(error_msg: str) -> None:
            if self._latest_path != path:
                return
            self.query_one("#further-steps").add_class("hidden")
            set_status(f"✗ {error_msg}", "status-error")

        try:
            self.call_from_thread(set_status, "⧗ Loading...", "status-loading")

            if is_kaggle_url(path):
                dataset_id = extract_dataset_id(path)
                files = download_files(dataset_id)
                if not files:
                    self.call_from_thread(hide_steps, "Failed to download Kaggle dataset.")
                    return
                file_path = str(files[0])
            else:
                if not os.path.exists(path) or not os.path.isfile(path):
                    self.call_from_thread(hide_steps, "File does not exist.")
                    return
                file_path = path

            if file_path.endswith(".csv"):
                cols = pd.read_csv(file_path, nrows=0).columns.tolist()
            elif file_path.endswith(".parquet"):
                cols = pd.read_parquet(file_path).columns.tolist()
            elif file_path.endswith(".xlsx"):
                cols = pd.read_excel(file_path, nrows=0).columns.tolist()
            elif file_path.endswith(".json"):
                cols = pd.read_json(file_path).columns.tolist()
            else:
                self.call_from_thread(hide_steps, "Unsupported file format.")
                return

            self.call_from_thread(reveal_steps, cols)

        except (OSError, ValueError, RuntimeError) as e:
            import logging

            logging.getLogger(__name__).debug("Failed to load columns: %s", e)
            self.call_from_thread(hide_steps, "Error reading file.")

    def on_input_changed(self, event: Input.Changed) -> None:
        """When input_file changes, load columns for target_variable autocomplete in background."""
        if event.input.id == "input_file":
            path = event.value.strip()
            self._latest_path = path

            if self._column_load_timer is not None:
                self._column_load_timer.stop()

            if path:
                # Debounce by 1 second so partial typings don't eagerly hit Kaggle/fs
                self._column_load_timer = self.set_timer(1.0, lambda: self.load_columns(path))
            else:
                self.query_one("#further-steps").add_class("hidden")
                lbl = self.query_one("#status-label", Label)
                lbl.update("")
                lbl.remove_class("status-success", "status-error", "status-loading")
