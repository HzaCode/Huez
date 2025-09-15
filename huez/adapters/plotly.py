"""
Plotly adapter for huez.
"""

import warnings
from typing import Dict, Any
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette, get_colormap


class PlotlyAdapter(Adapter):
    """Adapter for Plotly."""

    def __init__(self):
        super().__init__("plotly")

    def _check_availability(self) -> bool:
        """Check if plotly is available."""
        try:
            import plotly.graph_objects as go
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to Plotly."""
        import plotly.graph_objects as go
        import plotly.io as pio

        # Get palettes with fallback
        try:
            # Try with color correction first
            try:
                from ..color_correction import get_corrected_palette
                base_colors = get_palette(scheme.palettes.discrete, "discrete")
                discrete_colors = get_corrected_palette(base_colors, "plotly")
            except:
                # Fallback to basic palette
                discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            
            # Get colormap names with fallback
            try:
                from ..color_correction import get_best_colormap_for_library
                sequential_cmap = get_best_colormap_for_library(scheme.palettes.sequential, "plotly")
                diverging_cmap = get_best_colormap_for_library(scheme.palettes.diverging, "plotly")
            except:
                # Fallback to simple colormap names
                sequential_cmap = self._convert_colormap_name(scheme.palettes.sequential)
                diverging_cmap = self._convert_colormap_name(scheme.palettes.diverging)
                
        except Exception as e:
            warnings.warn(f"Failed to get palettes for Plotly: {e}")
            # Use default colors as last resort
            discrete_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
            sequential_cmap = "viridis"
            diverging_cmap = "rdbu"

        # Create comprehensive template
        template = go.layout.Template()

        # Set colorway (discrete colors) - this is the key for automatic coloring
        template.layout.colorway = discrete_colors

        # Create better colorscales
        if len(discrete_colors) >= 3:
            # Multi-color sequential scale
            n_colors = len(discrete_colors)
            sequential_scale = []
            for i, color in enumerate(discrete_colors[:3]):  # Use first 3 colors
                sequential_scale.append([i / 2, color])
            template.layout.colorscale.sequential = sequential_scale

            # Better diverging scale using first and last colors
            template.layout.colorscale.diverging = [
                [0, discrete_colors[0]],
                [0.5, "#ffffff"],
                [1, discrete_colors[-1]]
            ]
        else:
            # Fallback for fewer colors
            template.layout.colorscale.sequential = [
                [0, discrete_colors[0]],
                [1, discrete_colors[-1] if len(discrete_colors) > 1 else discrete_colors[0]]
            ]
            template.layout.colorscale.diverging = [
                [0, discrete_colors[0]],
                [0.5, "#ffffff"],
                [1, discrete_colors[-1] if len(discrete_colors) > 1 else discrete_colors[0]]
            ]

        # Set comprehensive font styling
        template.layout.font = dict(
            family=scheme.fonts.family,
            size=scheme.fonts.size,
            color="#333333"
        )

        # Set title styling
        template.layout.title = dict(
            font=dict(
                family=scheme.fonts.family,
                size=scheme.fonts.size + 4,
                color="#333333"
            )
        )

        # Set background colors
        template.layout.paper_bgcolor = "white"
        template.layout.plot_bgcolor = "white"

        # Configure axes with grid settings
        grid_color = "rgba(128,128,128,0.2)"
        
        # X-axis configuration
        template.layout.xaxis = dict(
            gridcolor=grid_color,
            showgrid=scheme.style.grid in ["x", "both"],
            zeroline=False,
            showline=not scheme.style.spine_top_right_off,
            linecolor="#333333",
            tickfont=dict(
                family=scheme.fonts.family,
                size=scheme.fonts.size,
                color="#333333"
            ),
            title=dict(
                font=dict(
                    family=scheme.fonts.family,
                    size=scheme.fonts.size + 2,
                    color="#333333"
                )
            )
        )
        
        # Y-axis configuration
        template.layout.yaxis = dict(
            gridcolor=grid_color,
            showgrid=scheme.style.grid in ["y", "both"],
            zeroline=False,
            showline=not scheme.style.spine_top_right_off,
            linecolor="#333333",
            tickfont=dict(
                family=scheme.fonts.family,
                size=scheme.fonts.size,
                color="#333333"
            ),
            title=dict(
                font=dict(
                    family=scheme.fonts.family,
                    size=scheme.fonts.size + 2,
                    color="#333333"
                )
            )
        )

        # Legend styling
        template.layout.legend = dict(
            font=dict(
                family=scheme.fonts.family,
                size=scheme.fonts.size,
                color="#333333"
            )
        )

        # Set default trace colors for different plot types
        template.data.scatter = [go.Scatter(
            marker=dict(color=discrete_colors[0]),
            line=dict(color=discrete_colors[0])
        )]
        
        template.data.bar = [go.Bar(
            marker=dict(color=discrete_colors[0])
        )]
        
        template.data.histogram = [go.Histogram(
            marker=dict(color=discrete_colors[0])
        )]

        # Register and set as default
        pio.templates['huez'] = template
        pio.templates.default = 'huez'
        
        # Store colors globally for helper functions
        global _plotly_colors
        _plotly_colors = discrete_colors

    def _convert_colormap_name(self, cmap_name: str) -> str:
        """Convert colormap names to Plotly-compatible names."""
        plotly_mapping = {
            "viridis": "viridis",
            "coolwarm": "rdbu",
            "plasma": "plasma", 
            "inferno": "inferno",
            "seismic": "rdylbu",
            "RdBu": "rdbu",
            "RdYlBu": "rdylbu"
        }
        return plotly_mapping.get(cmap_name, cmap_name.lower())


def export_plotly_template(scheme: Scheme, output_path: str) -> None:
    """
    Export Plotly template.

    Args:
        scheme: Color scheme
        output_path: Path to save template file
    """
    import json

    try:
        import plotly.graph_objects as go

        discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
        sequential_cmap = get_colormap(scheme.palettes.sequential, "sequential")
        diverging_cmap = get_colormap(scheme.palettes.diverging, "diverging")
    except Exception as e:
        warnings.warn(f"Failed to get palettes for Plotly template export: {e}")
        return

    # Create template data
    template_data = {
        "data": {
            "scatter": [{"mode": "markers"}],
            "bar": [{}],
            "line": [{}]
        },
        "layout": {
            "colorway": discrete_colors,
            "colorscale": {
                "sequential": sequential_cmap,
                "diverging": diverging_cmap
            },
            "font": {
                "family": scheme.fonts.family,
                "size": scheme.fonts.size
            },
            "title": {
                "font": {
                    "family": scheme.fonts.family,
                    "size": scheme.fonts.size + 4
                }
            },
            "xaxis": {
                "title": {
                    "font": {
                        "family": scheme.fonts.family,
                        "size": scheme.fonts.size + 2
                    }
                },
                "tickfont": {
                    "family": scheme.fonts.family,
                    "size": scheme.fonts.size
                }
            },
            "yaxis": {
                "title": {
                    "font": {
                        "family": scheme.fonts.family,
                        "size": scheme.fonts.size + 2
                    }
                },
                "tickfont": {
                    "family": scheme.fonts.family,
                    "size": scheme.fonts.size
                }
            }
        }
    }

    with open(output_path, 'w') as f:
        json.dump(template_data, f, indent=2)


# Global variable to store current colors
_plotly_colors = None


def get_plotly_colors(n: int = None):
    """
    Get current Plotly colors for manual use.
    
    Args:
        n: Number of colors to return. If None, returns all available colors.
        
    Returns:
        List of hex color strings
        
    Note:
        This is a convenience function for cases where you need explicit colors.
        In most cases, Plotly should automatically use the template colors.
    """
    global _plotly_colors
    
    if _plotly_colors is None:
        # Fallback to huez.palette if no template is active
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
        return _plotly_colors
    elif n <= len(_plotly_colors):
        return _plotly_colors[:n]
    else:
        # Cycle through colors if more needed
        import itertools
        return list(itertools.islice(itertools.cycle(_plotly_colors), n))


def plotly_auto_colors(fig, color_sequence: list = None):
    """
    Automatically apply huez colors to a Plotly figure.
    
    Args:
        fig: Plotly figure object
        color_sequence: Optional custom color sequence
        
    Returns:
        Figure with colors applied
        
    Example:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1,2,3], y=[1,2,3]))
        fig = plotly_auto_colors(fig)
    """
    if color_sequence is None:
        color_sequence = get_plotly_colors()
    
    # Apply colors to existing traces
    for i, trace in enumerate(fig.data):
        color_idx = i % len(color_sequence)
        color = color_sequence[color_idx]
        
        # Apply color based on trace type
        if hasattr(trace, 'marker') and trace.marker is not None:
            trace.marker.color = color
        if hasattr(trace, 'line') and trace.line is not None:
            trace.line.color = color
    
    return fig


def create_plotly_colorscale(colors: list = None, colorscale_type: str = "sequential"):
    """
    Create a Plotly colorscale from huez colors.
    
    Args:
        colors: List of colors. If None, uses current huez colors.
        colorscale_type: Type of colorscale ("sequential", "diverging")
        
    Returns:
        Plotly colorscale list
        
    Example:
        colorscale = create_plotly_colorscale()
        fig.add_trace(go.Heatmap(z=data, colorscale=colorscale))
    """
    if colors is None:
        colors = get_plotly_colors()
    
    if colorscale_type == "diverging":
        # Create diverging colorscale: first color - white - last color
        return [
            [0, colors[0]],
            [0.5, "#ffffff"],
            [1, colors[-1]]
        ]
    else:
        # Create sequential colorscale
        n_colors = len(colors)
        if n_colors == 1:
            return [[0, colors[0]], [1, colors[0]]]
        
        colorscale = []
        for i, color in enumerate(colors):
            position = i / (n_colors - 1)
            colorscale.append([position, color])
        
        return colorscale


def plotly_discrete_colormap(categories: list, colors: list = None):
    """
    Create a discrete color mapping for categorical data.
    
    Args:
        categories: List of category names
        colors: List of colors. If None, uses current huez colors.
        
    Returns:
        Dictionary mapping categories to colors
        
    Example:
        color_map = plotly_discrete_colormap(['A', 'B', 'C'])
        fig.add_trace(go.Scatter(
            x=x, y=y, 
            marker=dict(color=[color_map[cat] for cat in categories])
        ))
    """
    if colors is None:
        colors = get_plotly_colors()
    
    color_map = {}
    for i, category in enumerate(categories):
        color_idx = i % len(colors)
        color_map[category] = colors[color_idx]
    
    return color_map


