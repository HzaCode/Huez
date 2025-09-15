"""
PyVista adapter for huez.
"""

import warnings
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class PyVistaAdapter(Adapter):
    """Adapter for PyVista."""

    def __init__(self):
        super().__init__("pyvista")

    def _check_availability(self) -> bool:
        """Check if pyvista is available."""
        try:
            import pyvista as pv
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to PyVista."""
        import pyvista as pv

        # Get colormap
        try:
            sequential_cmap = get_palette(scheme.palettes.sequential, "sequential")
        except Exception as e:
            warnings.warn(f"Failed to get colormap for PyVista: {e}")
            sequential_cmap = "viridis"

        # Create custom theme
        try:
            theme = pv.themes.DefaultTheme()
            theme.background = [1.0, 1.0, 1.0]  # White background
            theme.color = [0.3, 0.3, 0.3]       # Dark gray for meshes
            theme.color_cycler = get_palette(scheme.palettes.discrete, "discrete")
            theme.cmap = sequential_cmap

            # Font settings
            theme.font.size = scheme.fonts.size
            theme.font.family = scheme.fonts.family

            # Apply theme
            pv.set_plot_theme(theme)

        except Exception as e:
            warnings.warn(f"Failed to apply PyVista theme: {e}")


