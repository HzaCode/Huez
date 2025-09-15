"""
hvPlot adapter for huez.
"""

import warnings
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class HvPlotAdapter(Adapter):
    """Adapter for hvPlot."""

    def __init__(self):
        super().__init__("hvplot")

    def _check_availability(self) -> bool:
        """Check if hvplot is available."""
        try:
            import hvplot.pandas
            return True
        except (ImportError, Exception):
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to hvPlot."""
        import hvplot.pandas

        # Get palettes
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            sequential_cmap = get_palette(scheme.palettes.sequential, "sequential")
            diverging_cmap = get_palette(scheme.palettes.diverging, "diverging")
        except Exception as e:
            warnings.warn(f"Failed to get palettes for hvPlot: {e}")
            return

        # Set default options
        try:
            import hvplot as hv
            hv.config.default_cmap = sequential_cmap
            hv.config.default_color_cycler = hv.config.Cycle(discrete_colors)
        except Exception as e:
            warnings.warn(f"Failed to set hvPlot defaults: {e}")

        # Store palettes for helper functions
        self._discrete_colors = discrete_colors
        self._sequential_cmap = sequential_cmap
        self._diverging_cmap = diverging_cmap


def get_hvplot_palette(kind: str = "discrete") -> any:
    """
    Helper function to get hvPlot-compatible color settings.

    Args:
        kind: Type of palette ("discrete", "sequential", "diverging")

    Returns:
        Color list or colormap name
    """
    try:
        from ..core import current_scheme
        from ..config import Config

        scheme_name = current_scheme()
        if scheme_name:
            from ..data.defaults import get_default_config
            config = get_default_config()
            if scheme_name in config.schemes:
                scheme = config.schemes[scheme_name]

                if kind == "discrete":
                    return get_palette(scheme.palettes.discrete, "discrete")
                elif kind == "sequential":
                    return get_palette(scheme.palettes.sequential, "sequential")
                elif kind == "diverging":
                    return get_palette(scheme.palettes.diverging, "diverging")

    except Exception as e:
        warnings.warn(f"Failed to get hvPlot palette: {e}")

    # Fallback
    return get_palette("okabe-ito", "discrete") if kind == "discrete" else "viridis"


# Convenience functions for hvPlot users
def hvplot_discrete_colors():
    """Get discrete colors for hvPlot."""
    return get_hvplot_palette("discrete")


def hvplot_sequential_cmap():
    """Get sequential colormap for hvPlot."""
    return get_hvplot_palette("sequential")


def hvplot_diverging_cmap():
    """Get diverging colormap for hvPlot."""
    return get_hvplot_palette("diverging")


