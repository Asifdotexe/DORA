"""
This module defines and applies a consistent, modern visual style for all plots.

The design principles are inspired by "Storytelling with Data" by Cole Nussbaumer Knaflic,
focusing on clarity, de-cluttering, and strategic use of color.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# To ensure our charts are clean and professional, we define a specific color palette.
# We use a strong primary color to draw attention and shades of gray for context.
PRIMARY_COLOR = "#0077b6"  # A clear, professional blue
GRAY_COLOR = "#808080"
BACKGROUND_COLOR = "#f5f5f5"
TEXT_COLOR = "#333333"


def apply_custom_styling():
    """
    Applies a clean, modern style to matplotlib and seaborn plots.
    This function acts as a single source of truth for all visual styling.
    """
    # We set a base style and customize it to remove chart junk.
    sns.set_style(
        "whitegrid",
        {
            "axes.facecolor": BACKGROUND_COLOR,
            "figure.facecolor": BACKGROUND_COLOR,
            "grid.color": "#dcdcdc",
            "text.color": TEXT_COLOR,
            "axes.labelcolor": TEXT_COLOR,
            "xtick.color": TEXT_COLOR,
            "ytick.color": TEXT_COLOR,
        },
    )

    # We use Matplotlib's rcParams for fine-grained control over plot elements,
    # such as removing unnecessary borders (spines) and adding padding.
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.edgecolor": GRAY_COLOR,
            "axes.titlepad": 20,
            "axes.labelpad": 15,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "xtick.minor.size": 0,
            "ytick.minor.size": 0,
            "xtick.major.pad": 10,
            "ytick.major.pad": 10,
            "figure.titlesize": "large",
            "figure.titleweight": "bold",
            "axes.titlesize": "large",
            "axes.labelsize": "medium",
        }
    )
