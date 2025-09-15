"""
Seaborn adapter for huez.
"""

import warnings
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class SeabornAdapter(Adapter):
    """Adapter for seaborn."""

    def __init__(self):
        super().__init__("seaborn")

    def _check_availability(self) -> bool:
        """Check if seaborn is available."""
        try:
            import seaborn as sns
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to seaborn."""
        import seaborn as sns
        import matplotlib.pyplot as plt

        # Set the color palette
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            sns.set_palette(discrete_colors)
        except Exception as e:
            warnings.warn(f"Failed to set seaborn palette: {e}")

        # Set seaborn theme to coordinate with matplotlib settings
        grid_style = "whitegrid" if scheme.style.grid in ["x", "y", "both"] else "white"

        sns.set_theme(
            context="paper",
            style=grid_style,
            font=scheme.fonts.family,
            font_scale=scheme.fonts.size / 11.0,
            rc={
                # Coordinate with matplotlib settings
                "axes.spines.top": not scheme.style.spine_top_right_off,
                "axes.spines.right": not scheme.style.spine_top_right_off,
                "grid.color": "#e0e0e0",
                "grid.alpha": 0.8,
                "grid.linewidth": 0.8,
                # Ensure color cycle matches matplotlib
                "axes.prop_cycle": plt.cycler(color=discrete_colors)
            }
        )

        # Ensure color cycle matches matplotlib
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=discrete_colors)


