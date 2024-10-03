import os 
import numpy as np
import pandas as pd
# MATPLOTLIB BACKEND: To handle the Tkinter exception during testing and testing doesn't require
# us to use the interface hence running matplotlib with non-GUI backend
import matplotlib
matplotlib.use('Agg')  

from src.multivariate_analysis import multivariate_analysis

def test_multivariate_analysis():
    # Setup
    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40],
        'C': [100,200,300,np.nan],
        'D': ['Asif','is','testing','this']
    })
    
    output_dir = 'tests/output_test/'
    if not os.path.exists(output_dir):
        os.makedirs(f'{output_dir}/charts/')
        
    # test
    multivariate_analysis(df, output_dir)
    
    # assertions
    assert os.path.exists(f"{output_dir}/charts/correlation_matrix.png"), "Correlation matrix chart not created"
    
    # teardown
    os.remove(f"{output_dir}/charts/correlation_matrix.png")