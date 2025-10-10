"""
This script configures the custom build process for Mypyc compilation.

It tells setuptools which Python files should be compiled into C extensions
for a significant performance boost.
"""

from mypyc.build import mypycify
from setuptools import setup

# This function tells setuptools which Python files to compile into C extensions.
# We target the core, CPU-bound logic for maximum performance gain.
extensions = mypycify(
    [
        "src/dora/analyzer.py",
        "src/dora/profiling.py",
        "src/dora/utils.py",
        "src/dora/plots/univariate.py",
        "src/dora/plots/bivariate.py",
        "src/dora/plots/multivariate.py",
    ]
)

# We use a standard setuptools setup to build our package, but with the compiled extensions included.
setup(
    name="dora",
    packages=["dora", "dora.plots", "dora.reporting"],
    package_dir={"": "src"},
    ext_modules=extensions,
)
