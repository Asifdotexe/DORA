# Data Oriented Report Automator (DORA)

![DORA Logo](data/dora-updated-concept.png)

## Overview

Welcome to **DORA**! This project is designed to automate the Exploratory Data Analysis (EDA) process, allowing you to effortlessly explore your datasets, generate insightful reports, and create visually appealing charts—all at the click of a button. 

With DORA, you'll be able to streamline your EDA workflow, making it easier than ever to discover trends, patterns, and relationships within your data!

## Features

- **Univariate Analysis**: Generate detailed statistics and visualizations for individual variables.
- **Bivariate Analysis**: Explore relationships between pairs of variables with insightful charts.
- **Multivariate Analysis**: Dive deep into the interactions of multiple variables through advanced visualizations.
- **Automated Reporting**: Save all statistics in text files for easy access and review.
- **Chart Generation**: Automatically save all generated charts for future reference.
- **PowerPoint Presentation Compilation**: Compile your findings into a professional PowerPoint presentation with minimal effort.
- **Progress Indicators**: Get live updates with progress bars for each step, powered by `tqdm`.
- **Custom Logging**: Detailed logs help track progress and spot issues during the analysis.

## Setup

### Requirements

Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dora.git
cd dora
```

2. Create and activate the virtual environment

For Windows
```bash
python -m venv venv
venv\Scripts\activate # windows
pip install -r requirements.txt
```

## Usage

Once the setup is complete, you can use DORA by running the dora.py script. Below are the steps to perform the EDA and generate a PowerPoint presentation.

### Command-Line Interface (CLI) Instructions

```bash
python dora.py <input_file> <output_directory> [--template_path <template_path>]
```

### Example

```bash
python dora.py data/insurance.csv output/presentation --template_path templates/eda_template.pptx
```

### Arguments

- `<input_file>`: Path to the input CSV file.
- `<output_directory>`: Directory where output files will be saved.
- `--template_path`: (Optional) Path to a PowerPoint template for generating the presentation. If no template is provided, a default presentation style will be used.

### Outputs

- **Charts**: Generated charts for univariate, bivariate, and multivariate analysis saved as PNG files.
- **PowerPoint**: A compiled PowerPoint presentation summarizing the findings, with all charts included.

Happy analyzing with DORA! 🎉