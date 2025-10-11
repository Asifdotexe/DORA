"""
This module defines and applies a consistent, modern visual style for all plots.

The design principles are inspired by "Storytelling with Data" by Cole Nussbaumer Knaflic,
focusing on clarity, de-cluttering, and strategic use of color.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# To ensure our charts are clean and professional, we define a specific color palette.
# We use a strong primary color to draw attention and shades of gray for context.
PRIMARY_BLUE = "#1a535c"  # The deep teal from the 'DORA' text
ACCENT_AQUA = "#4ecdc4"  # The light aqua from the 'O' pie chart
ACCENT_NAVY = "#003f5c"  # A darker blue for contrast
BACKGROUND_COLOR = "#f8f9fa"  # A very light gray for a soft, clean look
TEXT_COLOR = "#343a40"  # A dark gray for readable text
GRAY_COLOR = "#adb5bd"  # A light gray for non-critical elements like grid lines


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
            "grid.color": "#dee2e6",
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
            "font.sans-serif": ["Lato", "Arial", "sans-serif"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": True,
            "axes.edgecolor": GRAY_COLOR,
            "axes.titlepad": 25,
            "axes.labelpad": 15,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "xtick.major.pad": 10,
            "ytick.major.pad": 10,
            "figure.titlesize": "large",
            "figure.titleweight": "bold",
            "axes.titlesize": "large",
            "axes.labelsize": "medium",
        }
    )
