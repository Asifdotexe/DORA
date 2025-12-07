# Data Oriented Report Automator (DORA)

<p align="center">
    <img src="data/assets/dora-updated-concept.png" alt="DORA Logo" width="200"/>
</p>

<em align="center">
An interactive command-line tool to automate Exploratory Data Analysis (EDA) and generate beautiful, insightful reports in seconds.
</em>

## Overview

Welcome to DORA! This isn't just a script; it's an intelligent EDA assistant. DORA empowers you to move from a raw dataset to a comprehensive HTML report with minimal effort. It is designed to be powerful and configurable for experts, yet simple enough for anyone to use thanks to its interactive wizard.


## 1. installation
Install DORA directly from PyPI using pip:
```bash
pip install dora-eda
# check version to validate installation
dora -v
```

## 2. Usage
DORA has two modes of operation: Interactive (for first-time runs) and Config-Driven (for reproducible automation).
Run DORA without existing configuration (Fresh run)

## A. Interactive Mode (Quick Start)
Simply run the command without arguments. DORA will launch a wizard to guide you through the setup.

```bash
dora
```
You will be prompted to:
- Select your data file (CSV, Excel, JSON, Parquet).
- Choose an output directory.
- (Optional) Select a target variable for focused analysis.
- Pick which analysis steps to perform.
- (Optional) Save your settings to a `config.yaml` file for future use.

## B. Config-Driven Mode (Advanced)
If you already have a configuration file (e.g., from a previous run), you can skip the wizard and run the analysis immediately.

```bash
dora --config <path/to/config.yaml>
```

**Example `config.yaml`:**
```bash
# --- Input/Output Settings ---
input_file: 'data/insurance.csv'
output_dir: 'output/insurance_report'
report_title: 'Exploratory Data Analysis of Insurance Premiums'

# --- Dataset Settings ---
target_variable: 'charges'

# --- Analysis Pipeline ---
analysis_pipeline:
  - profile:
      enabled: true
  - univariate:
      enabled: true
      plot_types:
        numerical: ['histogram', 'boxplot']
        categorical: ['barplot']
  - bivariate:
      enabled: true
      target_centric: true
  - multivariate:
      enabled: true
      correlation_cols: ['age', 'bmi', 'children', 'charges']
```
## 3. Supported Data Formats
DORA automatically detects and reads the following file types:
- CSV (`*.csv`)
- Excel (`*.xlsx`) - Note: Analyzes the first sheet only.
- JSON (`*.json`)
- Parquet (`*.parquet`)

## 4. Viewing the Output
After the analysis is complete, check your output directory for:
- 📄 `eda_report.html`: The full, interactive report. Open this in any web browser.
- 📈 `charts/`: A folder containing all generated plots as high-quality images.

# Developer Guide
Interested in contributing to DORA? Awesome! Follow these steps to set up your local development environment.

## 1. Prerequisites
You need Poetry for dependency management.
```bash
# Windows (Powershell)
(Invoke-WebRequest -Uri [https://install.python-poetry.org](https://install.python-poetry.org) -UseBasicParsing).Content | py -

# Linux/macOS
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
```

## 2. Setup
Clone the repository and install dependencies (including dev tools).
```bash
git clone https://github.com/Asifdotexe/DORA.git
cd dora
poetry install --with dev
```

## 3. Code Quality
We use standard tools to keep the codebase clean. Please run these before submitting a PR.

**Automated Checks (Recommended):**
Install the pre-commit hooks once, and they will run automatically on every commit.
```bash
poetry run pre-commit install
```
**Manual Checks:**
```bash
# Format code
poetry run black .
poetry run isort .

# Lint code
poetry run pylint src/dora
```
**Running Tests:**
```bash
poetry run pytest
```

## 4. How to Contribute
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Happy analyzing with DORA! 🎉
