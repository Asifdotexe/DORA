import os
import shutil
import pytest
import pandas as pd
from src.univariate_analysis import univariate_analysis
from src.bivariate_analysis import bivariate_analysis
from src.multivariate_analysis import multivariate_analysis
from src.save_results import save_results
from src.main import main

# Fixture to set up and tear down the test environment at the module level
@pytest.fixture(scope='module')
def setup_test_env_module():
    input_file = 'data/insurance.csv'  # Path to a sample test CSV file
    output_dir = 'tests/output_test/'  # Directory where outputs will be saved

    # Clean up any pre-existing output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Create fresh output directories for the tests
    os.makedirs(output_dir)
    yield (input_file, output_dir)

    # Teardown: Remove the output directory after all tests in this module are complete
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

# Test case for the main function
def test_main(setup_test_env_module):
    input_file, output_dir = setup_test_env_module

    # Call the main function
    main(input_file, output_dir)

    # Check if the necessary directories were created
    assert os.path.exists(f"{output_dir}/stats/"), "Stats directory not created"
    assert os.path.exists(f"{output_dir}/charts/"), "Charts directory not created"

    # Check if key output files are created
    assert os.path.exists(f"{output_dir}/stats/univariate_analysis.txt"), "Univariate analysis file not created"
    assert os.path.exists(f"{output_dir}/charts/correlation_matrix.png"), "Correlation matrix chart not created"

# Test case for univariate analysis
def test_univariate_analysis(setup_test_env_module):
    _, output_dir = setup_test_env_module

    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': ['x', 'y', 'x', 'y'],
        'C': ['Asif', 'Sayyed', 'Dora', None]
    })

    # Call the univariate_analysis function
    univariate_analysis(df, output_dir)

    # Check if the univariate analysis output file was created
    assert os.path.exists(f"{output_dir}/stats/univariate_analysis.txt"), "Univariate analysis file not created"

# Test case for multivariate analysis
def test_multivariate_analysis(setup_test_env_module):
    _, output_dir = setup_test_env_module

    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40],
        'C': [100, 200, 300, None],
        'D': ['Asif', 'is', 'testing', 'this']
    })

    # Call the multivariate_analysis function
    multivariate_analysis(df, output_dir)

    # Check if the correlation matrix plot was created
    assert os.path.exists(f"{output_dir}/charts/correlation_matrix.png"), "Correlation matrix chart not created"

# Test case for bivariate analysis
def test_bivariate_analysis(setup_test_env_module):
    _, output_dir = setup_test_env_module

    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40],
        'C': ['a', 'b', 'c', 'd']
    })

    # Call the bivariate_analysis function
    bivariate_analysis(df, output_dir)

    # Check if bivariate analysis output exists (assume some file output)
    assert os.path.exists(f"{output_dir}/charts/bivariate_A_vs_B.png"), "Bivariate chart for A vs B not created"

# Test case for saving results
def test_save_results(setup_test_env_module):
    _, output_dir = setup_test_env_module

    # Call the save_results function
    save_results(output_dir)

    # Check if the final results were saved (assuming a report or summary is generated)
    assert os.path.exists(f"{output_dir}/eda_presentation.pptx"), "Presentation file not created"