"""
HoloViews adapter for huez.
"""

import warnings
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class HoloViewsAdapter(Adapter):
    """Adapter for HoloViews."""

    def __init__(self):
        super().__init__("holoviews")

    def _check_availability(self) -> bool:
        """Check if holoviews is available."""
        try:
            import holoviews as hv
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to HoloViews."""
        import holoviews as hv

        # Get palettes
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            sequential_cmap = get_palette(scheme.palettes.sequential, "sequential")
        except Exception as e:
            warnings.warn(f"Failed to get palettes for HoloViews: {e}")
            return

        # Set default color cycles
        try:
            hv.config.default_cmap = sequential_cmap
            hv.config.default_color_cycler = hv.config.Cycle(discrete_colors)
        except Exception as e:
            warnings.warn(f"Failed to set HoloViews defaults: {e}")

        # Configure plot options
        try:
            hv.config.fontsize = {
                'title': scheme.fonts.size + 4,
                'labels': scheme.fonts.size,
                'xticks': scheme.fonts.size - 2,
                'yticks': scheme.fonts.size - 2,
                'cticks': scheme.fonts.size - 2
            }
        except Exception as e:
            warnings.warn(f"Failed to set HoloViews font options: {e}")


