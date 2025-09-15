"""
Altair adapter for huez.
"""

import warnings
from typing import Dict, Any
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette, get_colormap


class AltairAdapter(Adapter):
    """Adapter for Altair."""

    def __init__(self):
        super().__init__("altair")

    def _check_availability(self) -> bool:
        """Check if altair is available."""
        try:
            import altair as alt
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to Altair."""
        import altair as alt

        # Get palettes with fallback to basic colors
        try:
            # Try with color correction first
            try:
                from ..color_correction import get_corrected_palette
                base_colors = get_palette(scheme.palettes.discrete, "discrete")
                discrete_colors = get_corrected_palette(base_colors, "altair")
            except:
                # Fallback to basic palette
                discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            
            # Get colormap names with fallback
            try:
                from ..color_correction import get_best_colormap_for_library
                sequential_cmap = get_best_colormap_for_library(scheme.palettes.sequential, "altair")
                diverging_cmap = get_best_colormap_for_library(scheme.palettes.diverging, "altair")
            except:
                # Fallback to simple colormap names
                sequential_cmap = self._convert_colormap_name(scheme.palettes.sequential)
                diverging_cmap = self._convert_colormap_name(scheme.palettes.diverging)
                
        except Exception as e:
            warnings.warn(f"Failed to get palettes for Altair: {e}")
            # Use default colors as last resort
            discrete_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
            sequential_cmap = "viridis"
            diverging_cmap = "redblue"

        # Create comprehensive theme configuration
        theme_config = {
            "config": {
                # Color ranges for different chart types
                "range": {
                    "category": discrete_colors,
                    "ordinal": discrete_colors,
                    "heatmap": sequential_cmap,
                    "diverging": diverging_cmap,
                    "ramp": sequential_cmap
                },
                # Mark defaults for automatic color application
                "mark": {
                    "color": discrete_colors[0],  # Default mark color
                    "fill": discrete_colors[0],
                    "stroke": discrete_colors[0]
                },
                # Point/circle marks
                "point": {
                    "color": discrete_colors[0],
                    "fill": discrete_colors[0]
                },
                "circle": {
                    "color": discrete_colors[0],
                    "fill": discrete_colors[0]
                },
                # Line marks
                "line": {
                    "color": discrete_colors[0],
                    "stroke": discrete_colors[0]
                },
                # Bar marks
                "bar": {
                    "color": discrete_colors[0],
                    "fill": discrete_colors[0]
                },
                "rect": {
                    "color": discrete_colors[0],
                    "fill": discrete_colors[0]
                },
                # Text styling
                "text": {
                    "font": scheme.fonts.family,
                    "fontSize": scheme.fonts.size,
                    "color": "#333333"
                },
                "title": {
                    "font": scheme.fonts.family,
                    "fontSize": scheme.fonts.size + 4,
                    "color": "#333333"
                },
                # Axis styling
                "axis": {
                    "labelFont": scheme.fonts.family,
                    "labelFontSize": scheme.fonts.size,
                    "titleFont": scheme.fonts.family,
                    "titleFontSize": scheme.fonts.size + 2,
                    "grid": scheme.style.grid in ["both", "x", "y"],
                    "gridColor": "#e0e0e0",
                    "domain": not scheme.style.spine_top_right_off,
                    "ticks": True
                },
                "axisX": {
                    "grid": scheme.style.grid in ["both", "x"],
                    "gridColor": "#e0e0e0"
                },
                "axisY": {
                    "grid": scheme.style.grid in ["both", "y"],
                    "gridColor": "#e0e0e0"
                },
                # Legend styling
                "legend": {
                    "labelFont": scheme.fonts.family,
                    "labelFontSize": scheme.fonts.size,
                    "titleFont": scheme.fonts.family,
                    "titleFontSize": scheme.fonts.size + 2
                },
                # Background
                "background": "white",
                "view": {
                    "continuousWidth": scheme.figure.size[0] * 72,  # Convert to points
                    "continuousHeight": scheme.figure.size[1] * 72
                }
            }
        }

        # Register the theme
        alt.themes.register('huez', lambda: theme_config)

        # Enable the theme
        alt.themes.enable('huez')
        
        # Store colors globally for helper functions
        global _altair_colors
        _altair_colors = discrete_colors

    def _convert_colormap_name(self, cmap_name: str) -> str:
        """Convert colormap names to Altair-compatible names."""
        altair_mapping = {
            "viridis": "viridis",
            "coolwarm": "redblue",
            "plasma": "plasma",
            "inferno": "inferno",
            "seismic": "redblue",
            "RdBu": "redblue",
            "RdYlBu": "redyellowblue",
            # Add more mappings
            "PiYG": "pinkgreen",
            "PRGn": "purplegreen",
            "BrBG": "brownbluegreen",
            "PuOr": "purpleorange",
            "RdGy": "redgrey",
            "RdYlGn": "redyellowgreen",
            "Spectral": "spectral"
        }
        return altair_mapping.get(cmap_name, "redblue")  # Default to redblue


def export_altair_theme(scheme: Scheme, output_path: str) -> None:
    """
    Export Altair theme configuration.

    Args:
        scheme: Color scheme
        output_path: Path to save theme file
    """
    import json

    try:
        discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
        sequential_cmap = get_colormap(scheme.palettes.sequential, "sequential")
        diverging_cmap = get_colormap(scheme.palettes.diverging, "diverging")
    except Exception as e:
        warnings.warn(f"Failed to get palettes for Altair theme export: {e}")
        return

    theme_config = {
        "config": {
            "range": {
                "category": discrete_colors,
                "ordinal": discrete_colors,
                "heatmap": {"scheme": sequential_cmap},
                "diverging": {"scheme": diverging_cmap}
            },
            "text": {
                "font": scheme.fonts.family,
                "fontSize": scheme.fonts.size
            },
            "title": {
                "font": scheme.fonts.family,
                "fontSize": scheme.fonts.size + 4
            },
            "axis": {
                "labelFont": scheme.fonts.family,
                "labelFontSize": scheme.fonts.size,
                "titleFont": scheme.fonts.family,
                "titleFontSize": scheme.fonts.size + 2
            },
            "legend": {
                "labelFont": scheme.fonts.family,
                "labelFontSize": scheme.fonts.size,
                "titleFont": scheme.fonts.family,
                "titleFontSize": scheme.fonts.size + 2
            }
        }
    }

    with open(output_path, 'w') as f:
        json.dump(theme_config, f, indent=2)


# Global variable to store current colors
_altair_colors = None


def get_altair_colors(n: int = None):
    """
    Get current Altair colors for manual use.
    
    Args:
        n: Number of colors to return. If None, returns all available colors.
        
    Returns:
        List of hex color strings
        
    Note:
        This is a convenience function for cases where you need explicit colors.
        In most cases, Altair should automatically use the theme colors.
    """
    global _altair_colors
    
    if _altair_colors is None:
        # Fallback to huez.palette if no theme is active
        from ..core import palette
        try:
            return palette(n=n, kind="discrete")
        except:
            # Last resort fallback
            colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
            if n is None:
                return colors
            elif n <= len(colors):
                return colors[:n]
            else:
                # Cycle through colors if more needed
                import itertools
                return list(itertools.islice(itertools.cycle(colors), n))
    
    if n is None:
        return _altair_colors
    elif n <= len(_altair_colors):
        return _altair_colors[:n]
    else:
        # Cycle through colors if more needed
        import itertools
        return list(itertools.islice(itertools.cycle(_altair_colors), n))


def altair_color_scale(field: str, scale_type: str = "nominal"):
    """
    Create an Altair color scale that automatically uses huez colors.
    
    Args:
        field: Field name for the color encoding
        scale_type: Type of scale ("nominal", "ordinal", "quantitative")
        
    Returns:
        Altair Color encoding
        
    Example:
        chart = alt.Chart(data).mark_circle().encode(
            x='x:Q',
            y='y:Q', 
            color=altair_color_scale('category:N')
        )
    """
    import altair as alt
    
    if scale_type in ["nominal", "ordinal"]:
        # For categorical data, the theme should handle this automatically
        return alt.Color(field)
    else:
        # For quantitative data, use sequential colormap
        return alt.Color(field, scale=alt.Scale(scheme="viridis"))


def altair_auto_color(chart, color_field: str = None):
    """
    Automatically apply huez colors to an Altair chart.
    
    Args:
        chart: Altair chart object
        color_field: Optional field name for color encoding
        
    Returns:
        Chart with color encoding applied
        
    Example:
        chart = alt.Chart(data).mark_circle().encode(x='x:Q', y='y:Q')
        chart = altair_auto_color(chart, 'category:N')
    """
    if color_field:
        return chart.encode(color=altair_color_scale(color_field))
    else:
        # If no field specified, just return the chart (theme will handle default colors)
        return chart


