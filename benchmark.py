"""
This script runs a performance benchmark on the DORA analysis pipeline.

It repeatedly executes the main Analyzer and records the execution time for each run
to provide performance statistics (average, min, max). This is useful for
identifying performance regressions or improvements after making code changes.
"""

import logging
import time
from pathlib import Path

import pandas as pd
import yaml

from src.dora.analyzer import Analyzer

NUM_RUNS = 5
CONFIG_PATH = Path("config.yaml")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_benchmark():
    """
    Executes the DORA analyzer multiple times and reports performance statistics.
    """
    # We use a list to store the time taken for each run. This allows us to
    # calculate summary statistics after all runs are complete.
    run_times = []

    # To ensure we're benchmarking the analysis logic and not the file I/O,
    # we load the configuration and the dataset once before the loop starts.
    logging.info("--- Preparing for benchmark ---")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    input_file = config["input_file"]
    logging.info("Loading data from: %s", input_file)
    df = pd.read_csv(input_file)
    logging.info("--- Data loaded. Starting benchmark runs... ---")

    # This loop is the core of the benchmark. It runs the analysis the specified
    # number of times to get a reliable measure of performance.
    for i in range(NUM_RUNS):
        logging.info("--- Starting Run %d/%d ---", i + 1, NUM_RUNS)
        analyzer = Analyzer(df, config)

        start_time = time.perf_counter()
        analyzer.run()  # This is the function we are timing.
        end_time = time.perf_counter()

        duration = end_time - start_time
        run_times.append(duration)
        logging.info(
            "--- Run %d/%d finished in %.2f seconds ---", i + 1, NUM_RUNS, duration
        )

    # After the benchmark, we provide a clear summary of the results.
    logging.info("--- Benchmark Complete ---")
    logging.info("Total runs: %d", len(run_times))
    logging.info("Average time: %.2f seconds", sum(run_times) / len(run_times))
    logging.info("Fastest run: %.2f seconds", min(run_times))
    logging.info("Slowest run: %.2f seconds", max(run_times))


if __name__ == "__main__":
    run_benchmark()
