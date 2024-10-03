import os
import pandas as pd
import numpy as np
# MATPLOTLIB BACKEND: To handle the Tkinter exception during testing and testing doesn't require
# us to use the interface hence running matplotlib with non-GUI backend
import matplotlib
matplotlib.use('Agg')  

from src.univariate_analysis import univariate_analysis

def test_univariate_analysis():
    """This function tests the univariate analysis function
    """
    # Setup
    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': ['x', 'y', 'x', 'y'],
        'C': ['Asif','Sayyed','Dora',np.nan]
    })
    output_dir = 'tests/output_test/'
    if not os.path.exists(output_dir):
        os.makedirs(f'{output_dir}/stats/')
        os.makedirs(f'{output_dir}/charts/')

    # Test
    stats_file = univariate_analysis(df, output_dir)

    # Assertions
    assert os.path.exists(stats_file), "Stats file was not created"
    assert os.path.exists(f"{output_dir}/charts/univariate_A.png"), "Univariate chart for column A not created"
    assert os.path.exists(f"{output_dir}/charts/univariate_B.png"), "Univariate chart for column B not created"

    # Teardown
    os.remove(stats_file)
    os.remove(f"{output_dir}/charts/univariate_A.png")
    os.remove(f"{output_dir}/charts/univariate_B.png")