## Date: 2026-08-09
### Goal: Port package to uv and optimize dependencies
- Migrated pyproject.toml from Poetry to standard PEP format and switched to uv.
  - Why: Faster dependency resolution and standard ecosystem compatibility.
- Split dependencies into core, `cli`, and `ui` optional groups.
  - Why: Prevent bloating the environment for users who only need specific features (like only the terminal tool or only the web UI).
- Kept jinja2 in core dependencies.
  - Why: It is required for HTML generation across all use cases (core, cli, ui).
- Added kagglehub to both `cli` and `ui` optional groups.
  - Why: Both interfaces require it for downloading datasets via kaggle links.
- Created `run_precommit.bat` script.
  - Why: To provide a quick and easy way for Windows users to run `uv run pre-commit run --all-files`.
- Updated GitHub Actions workflows (`ci.yaml` and `release.yaml`) to use `uv` instead of Poetry.
  - Why: To ensure continuous integration and deployments use the new package manager for building, testing, and publishing to PyPI.
