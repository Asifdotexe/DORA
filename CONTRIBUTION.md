# Contribution Onboarding

Thank you for your interest in contributing to Data-Oriented Report Automator (DORA)!

1. Prerequisites

Ensure you have [Python 3.13](https://www.python.org/downloads/) or higher installed, [Git](https://git-scm.com/) and then install [Poetry](https://python-poetry.org/):
- For Windows (PowerShell)
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
- For Linux/macOS
```bash
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
```

2. Forking / Installation
Fork and clone the repository and install the project to help development:
```bash
git clone https://github.com/Asifdotexe/DORA.git
```

```bash
cd dora
```

```bash
poetry install --with dev
```

3. Enforcing Code Quality
We highly recommend installing `pre-commit` hooks, which will run these checks automatically before every commit.
```bash
poetry run pre-commit install
```
If you prefer to run checks manually:
- Formatting: `poetry run black .`
- Linting: `poetry run pylint src/dora .`
- Import sort: `poetry run isort .`
4. Running tests

We use `pytest` for our test suites. Please ensure all tests pass before submitting a pull request.
```bash
poetry run pytest
```

## How to submit a contribution
1. Fork the repository on GitHub
2. Create a feature branch for your changes:
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes, follow the coding style and add comments where 
4. Run the checks
5. Commit your changes and push to your fork
6. Submit a pull request to the main repository

## Reporting Bugs

If you encounter any bugs or issues, please report them by creating a new issue on the [GitHub repository](https://github.com/Asifdotexe/DORA/issues).

The following should be the format of the issue:
- A clear description of the problem.
- Steps to reproduce the issue.
- The expected behavior versus the actual behavior.
- (Optional) Screenshots or videos of the issue and your operating system

Thank you for helping us improve DORA!
