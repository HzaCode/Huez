"""
Bokeh adapter for huez.
"""

import warnings
import json
import os
from typing import Dict, Any
from pathlib import Path
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class BokehAdapter(Adapter):
    """Adapter for Bokeh."""

    def __init__(self):
        super().__init__("bokeh")

    def _check_availability(self) -> bool:
        """Check if bokeh is available."""
        try:
            import bokeh.plotting as bkp
            import bokeh.io as bio
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to Bokeh."""
        import bokeh.plotting as bkp
        import bokeh.io as bio

        # Get palettes
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
        except Exception as e:
            warnings.warn(f"Failed to get discrete palette for Bokeh: {e}")
            return

        # Create theme configuration
        theme_config = {
            "attrs": {
                "Axis": {
                    "axis_label_text_color": "#333333",
                    "axis_label_text_font_size": f"{scheme.fonts.size}pt",
                    "axis_label_text_font": scheme.fonts.family,
                    "major_label_text_color": "#666666",
                    "major_label_text_font_size": f"{scheme.fonts.size - 2}pt",
                    "major_label_text_font": scheme.fonts.family
                },
                "Grid": {
                    "grid_line_color": "#cccccc",
                    "grid_line_alpha": 0.3 if scheme.style.grid in ["y", "both"] else 0.0,
                    "minor_grid_line_color": "#cccccc",
                    "minor_grid_line_alpha": 0.2
                },
                "Legend": {
                    "label_text_color": "#333333",
                    "label_text_font_size": f"{scheme.fonts.size - 1}pt",
                    "label_text_font": scheme.fonts.family,
                    "title_text_color": "#333333",
                    "title_text_font_size": f"{scheme.fonts.size}pt",
                    "title_text_font": scheme.fonts.family
                },
                "Plot": {
                    "background_fill_color": "#ffffff",
                    "border_fill_color": "#ffffff",
                    "outline_line_color": "#cccccc" if scheme.style.spine_top_right_off else "#333333"
                },
                "Title": {
                    "text_color": "#333333",
                    "text_font_size": f"{scheme.fonts.size + 4}pt",
                    "text_font": scheme.fonts.family
                }
            }
        }

        # Create and register theme
        try:
            from bokeh.themes import Theme
            theme = Theme(json=theme_config)
            bio.curdoc().theme = theme
        except Exception as e:
            warnings.warn(f"Failed to apply Bokeh theme: {e}")


def export_bokeh_theme(scheme: Scheme, output_path: str) -> None:
    """
    Export Bokeh theme file.

    Args:
        scheme: Color scheme
        output_path: Path to save theme file
    """
    try:
        discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
    except Exception as e:
        warnings.warn(f"Failed to get palette for Bokeh theme export: {e}")
        return

    theme_config = {
        "attrs": {
            "CategoricalColorMapper": {
                "palette": discrete_colors
            },
            "LinearColorMapper": {
                "palette": get_palette(scheme.palettes.sequential, "sequential", n=256)
            },
            "LogColorMapper": {
                "palette": get_palette(scheme.palettes.sequential, "sequential", n=256)
            }
        }
    }

    with open(output_path, 'w') as f:
        json.dump(theme_config, f, indent=2)


