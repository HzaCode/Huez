"""
huez - Your all-in-one color solution in Python

A unified color solution that provides consistent color schemes and themes
across multiple visualization libraries including Matplotlib, Seaborn, plotnine,
Altair, and Plotly.
"""

__version__ = "0.0.3"
__author__ = "Ang"
__email__ = "ang@hezhiang.com"

from .core import (
    load_config,
    use,
    current_scheme,
    palette,
    cmap,
    gg_scales,
    using,
    export_styles,
    preview_gallery,
    check_palette,
    lint_figure,
    # New convenience functions
    auto_colors,
    quick_setup,
    colors,
    apply_to_figure,
    status,
    help_usage,
    get_colors,  # Alias
    setup,       # Alias
)

__all__ = [
    "load_config",
    "use",
    "current_scheme",
    "palette",
    "cmap",
    "gg_scales",
    "using",
    "export_styles",
    "preview_gallery",
    "check_palette",
    "lint_figure",
    # New convenience functions
    "auto_colors",
    "quick_setup",
    "colors",
    "apply_to_figure",
    "status",
    "help_usage",
    "get_colors",  # Alias
    "setup",       # Alias
]


