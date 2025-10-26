"""
Quality tools for huez - colorblind simulation, contrast checking, and figure linting.
"""

from .checks import check_palette_quality
from .lint import lint_figure_file

__all__ = ["check_palette_quality", "lint_figure_file"]
