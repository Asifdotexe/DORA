@echo off
echo Running pre-commit checks...
uv run pre-commit run --all-files
pause
