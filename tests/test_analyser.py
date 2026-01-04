"""
End-to-end tests for the Analyzer pipeline.
"""

from pathlib import Path

import pandas as pd
import pytest

from dora.analyzer import Analyzer
from dora.schema import (AnalysisStep, BivariateStep, Config, MultivariateStep,
                         ProfileStep, UnivariateStep)


@pytest.fixture
def test_environment(tmp_path: Path) -> dict:
    """
    Creates a self-contained test environment with a dummy CSV and config file.

    :param tmp_path: Path to the temporary file
    """
    data = {
        "age": [25, 30, 35, 40, 45],
        "sex": ["male", "female", "male", "female", "male"],
        "bmi": [22.5, 25.1, 28.3, 26.8, 30.0],
        "charges": [1000, 1200, 1500, 1800, 2200],
    }
    df = pd.DataFrame(data)

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "test_data.csv"
    df.to_csv(csv_path, index=False)

    output_dir = tmp_path / "output"

    config = Config(
        input_file=csv_path,
        output_dir=output_dir,
        report_title="Test EDA Report",
        target_variable="charges",
        analysis_pipeline=[
            AnalysisStep(profile=ProfileStep(enabled=True)),
            AnalysisStep(
                univariate=UnivariateStep(
                    enabled=True,
                    plot_types={
                        "numerical": ["histogram"],
                        "categorical": ["barplot"],
                    },
                )
            ),
            AnalysisStep(bivariate=BivariateStep(enabled=True, target_centric=True)),
            AnalysisStep(
                multivariate=MultivariateStep(enabled=True, correlation_cols=[])
            ),
        ],
    )

    return {"df": df, "config": config, "output_dir": output_dir}


def test_full_pipeline_and_benchmark(test_environment, benchmark):
    """
    Tests the full analyzer pipeline from start to finish and audits its performance.
    """
    # Set up the analyzer with our self-contained test data.
    df = test_environment["df"]
    config = test_environment["config"]
    output_dir = test_environment["output_dir"]
    analyzer = Analyzer(df, config)

    # Run the entire pipeline and benchmark its execution time.
    # The `benchmark` fixture comes from pytest-benchmark. It runs `analyzer.run`
    # multiple times to get a reliable performance measurement.
    benchmark(analyzer.run)

    # Assert: Verify that the pipeline produced the expected output files.
    # This confirms the correctness of the run.
    assert output_dir.exists()
    assert (output_dir / "charts").exists()

    # Find the HTML report (its name is dynamic)
    html_files = list(output_dir.glob("*.html"))
    assert len(html_files) == 1, "Expected one HTML report to be generated"

    # Check for a specific, expected chart
    expected_chart = output_dir / "charts" / "multivariate_correlation_matrix.png"
    assert expected_chart.exists()
