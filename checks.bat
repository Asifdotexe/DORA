@echo off
echo Running pre-commit checks...
uv run prek run --all-files
pause
