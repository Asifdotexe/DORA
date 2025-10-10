"""
This module contains utility functions and decorators for the DORA project.
"""

import functools
import logging
import time


def timer(func):
    """A decorator that logs the execution time of a function."""

    # We use @functools.wraps to ensure the decorated function keeps its original name and docstring.
    # This is important for debugging and introspection.
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        # To measure the duration, we record the time just before the function runs.
        start_time = time.perf_counter()
        # The original function is executed here, and we store its result to return later.
        value = func(*args, **kwargs)
        # We record the time again after the function completes.
        end_time = time.perf_counter()
        run_time = end_time - start_time
        # We log the result in a clear, readable format.
        logging.info("--- Finished %s in %.2f seconds ---", func.__name__, run_time)
        return value

    return wrapper_timer
