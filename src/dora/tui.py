from typing import ClassVar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
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

        try:
            if is_kaggle_url(path):
                self.call_from_thread(
                    self.notify, "Downloading Kaggle dataset for autocomplete...", severity="information"
                )
                dataset_id = extract_dataset_id(path)
                files = download_files(dataset_id)
                if not files:
                    return
                file_path = str(files[0])
            else:
                if not os.path.exists(path) or not os.path.isfile(path):
                    return
                file_path = path

            if file_path.endswith(".csv"):
                cols = pd.read_csv(file_path, nrows=0).columns.tolist()
            elif file_path.endswith(".parquet"):
                cols = pd.read_parquet(file_path).columns.tolist()
            elif file_path.endswith(".xlsx"):
                cols = pd.read_excel(file_path, nrows=0).columns.tolist()
            else:
                return

            def update_suggester():
                target_input = self.query_one("#target_variable", Input)
                target_input.suggester = SuggestFromList([str(c) for c in cols], case_sensitive=False)
                self.notify(f"Found {len(cols)} columns for autocomplete", severity="information")

            self.call_from_thread(update_suggester)

        except (OSError, ValueError, RuntimeError) as e:
            import logging

            logging.getLogger(__name__).debug("Failed to load columns: %s", e)

    def on_input_changed(self, event: Input.Changed) -> None:
        """When input_file changes, load columns for target_variable autocomplete in background."""
        if event.input.id == "input_file":
            path = event.value.strip()
            if path:
                self.load_columns(path)
