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
