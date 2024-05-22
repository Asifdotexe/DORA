# EDA Script

This repository contains a generalized Python script for performing Exploratory Data Analysis (EDA) using Pandas, NumPy, Matplotlib, and Seaborn.

## Features

- Load and preview data
- Summarize data structure and missing values
- Display summary statistics
- Visualize missing values
- Handle missing values
- Visualize distributions of numerical columns
- Visualize correlations
- Visualize categorical columns
- Identify and visualize outliers

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/Asifdotexe/eda_script.git
    ```

2. Navigate to the project directory:
    ```sh
    cd eda_script
    ```

3. Install required dependencies:
    ```sh
    pip install pandas numpy matplotlib seaborn
    ```

4. Run the script:
    ```sh
    python eda_script.py
    ```

## Example

You can use the script with your own dataset by changing the `file_path` variable in the script:
```python
file_path = 'your_dataset.csv'  # Replace with your actual file path
perform_eda(file_path)
