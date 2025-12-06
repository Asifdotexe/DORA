# Data Oriented Report Automator (DORA)

<p align="center">
    <img src="data/assets/dora-updated-concept.png" alt="DORA Logo" width="200"/>
</p>

<em align="center">
An interactive command-line tool to automate Exploratory Data Analysis (EDA) and generate beautiful, insightful reports in seconds.
</em>

## Overview

Welcome to DORA! This isn't just a script; it's an intelligent EDA assistant. DORA empowers you to move from a raw dataset to a comprehensive HTML report with minimal effort. It's designed to be powerful and configurable, yet simple enough for anyone to use thanks to its interactive mode.

## Key Features

- Dual-Mode Operation:
    - Interactive mode: A step-by-step wizard to configure your analysis (no coding involved)
    - Configuration driven: For reproducible workflows, define your analysis in a `config.yaml` file
- Flexible Data Input: Supports CSV, Excel, JSON, and Parquet files.
    - Note: For Excel files, DORA will only read and analyze the first sheet.
- Data Profiling: Get an overview of your dataset's health, including missing values, descriptive statistics and data types
- Target-centric analysis: Generates plots that explore the relationship between your features and a specified target variable
- HTML Reports: Generates a HTML report that's easy to share and view in any browser.

## User Guide

Get started with DORA in just two commands. Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed first.

### Step 1
```bash
# For Windows (Powershell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# For Linux or MacOS (Terminal)
curl -sSL https://install.python-poetry.org | python3 -
```

### Step 2
```bash
# Clone the repository
git clone https://github.com/Asifdotexe/DORA.git
cd DORA

# Install all dependencies using Poetry
poetry install

# The --with dev flag is important as it also installs development tools like pylint. (for developers only)
poetry install --with dev
```

## Quick Start (Interactive Mode)
This is the easiest way to run DORA. The interactive wizard will guide you through the entire process.

```bash
cd src/dora
poetry run python main.py
```

You will be prompted to:
- Enter the path to your CSV file.
- Specify an output directory.
- (Optionally) select a target variable.
- Choose which analysis steps to perform.
At the end, it will even ask if you want to save your choices to a `config.yaml` file for next time!

## Advanced Usage (Config-Driven Mode)
For reproducible results or to integrate DORA into a larger workflow, the configuration-driven mode is ideal.

### a. Create a config.yaml file:

```yaml
# --- Input/Output Settings ---
input_file: 'data/insurance.csv'
output_dir: 'output/insurance_report'
report_title: 'Exploratory Data Analysis of Insurance Premiums'

# --- Dataset Settings ---
target_variable: 'charges'

# --- Analysis Pipeline ---
# Define the steps to run. The tool will execute them in this order.
analysis_pipeline:
  - profile:
      # Generate detailed data profile (missing values, cardinality, stats).
      # No extra parameters needed.
      enabled: true

  - univariate:
      # Generate plots for individual columns.
      enabled: true
      plot_types:
        # Can be 'histogram', 'boxplot'
        numerical: ['histogram', 'boxplot']
        # Can be 'barplot'
        categorical: ['barplot']

  - bivariate:
      # Analyze relationships between two variables.
      enabled: true
      # If true, focuses on plotting features against the target_variable.
      # If false, would require more specific pairs to be defined (more advanced).
      target_centric: true

  - multivariate:
      # Analyze relationships among three or more variables.
      enabled: true
      # Specify columns for the correlation heatmap.
      # If empty or not provided, uses all numerical columns.
      correlation_cols: ['age', 'bmi', 'children', 'charges']
```
### b. Run DORA with the config file:

```bash
cd src/dora
poetry run python main.py --config config.yaml
```

## Viewing the Output
After the analysis is complete, you will find a new folder at your specified output path containing:
- eda_report.html: Your final, shareable report. Open it in any browser.
- charts/: A sub-folder with all the generated plots saved as individual image files.

## Developer Onboarding
Interested in contributing to DORA? Awesome! Here’s how to get set up.

### 1. Setting Up the Development Environment
The `poetry install` command you ran earlier for developers already installed all the development dependencies (like `pytest` and `pylint`).

### 2. Running Linters and Formatters
We use `black` for formatting, `isort` for sorting imports, and `pylint` for linting. We recommend setting up `pre-commit hooks` to automate this process.

```bash
# Install the pre-commit hooks (run this once)
poetry run pre-commit install

# Now, your code will be automatically checked and formatted every time you make a commit
```

To run the checks manually:

```bash
# Format code with Black and isort
poetry run black .
poetry run isort .

# Run the linter
poetry run pylint src/dora
```

### 3. How to Contribute
- Fork the repository.
- Create a new branch (git checkout -b feature/my-new-feature).
- Make your changes and add tests for them.
- Ensure all tests and pre-commit checks pass.
- Push to your branch and submit a Pull Request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Happy analyzing with DORA! 🎉
