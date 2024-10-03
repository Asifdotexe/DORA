import os
import pandas as pd
import numpy as np
# MATPLOTLIB BACKEND: To handle the Tkinter exception during testing and testing doesn't require
# us to use the interface hence running matplotlib with non-GUI backendp
import matplotlib
matplotlib.use('Agg')

from src.bivariate_analysis import bivariate_analysis

def test_bivariate_analysis():
    # Setup
    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40],
        'C': ['Asif','Sayyed','Dora',np.nan]
    })
    output_dir = 'tests/output_test/'
    if not os.path.exists(output_dir):
        os.makedirs(f'{output_dir}/charts/')

    # Test
    bivariate_analysis(df, output_dir)

    # Assertions
    assert os.path.exists(f"{output_dir}/charts/bivariate_A_vs_B.png"), "Bivariate chart for A vs B not created"

    # Teardown
    os.remove(f"{output_dir}/charts/bivariate_A_vs_B.png")
