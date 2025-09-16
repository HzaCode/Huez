"""
Huez - Unified Color Scheme Solution for Python Visualization

A comprehensive color management library that provides consistent, professional
color schemes across multiple Python visualization libraries including Matplotlib,
Seaborn, plotnine, Altair, and Plotly. Transform your charts from amateur to
publication-ready with just one line of code.
"""

__version__ = "0.1.0"
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


