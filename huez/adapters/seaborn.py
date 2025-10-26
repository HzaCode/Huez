"""
Seaborn adapter for huez.
"""

import warnings

from ..config import Scheme
from ..registry.palettes import get_palette
from .base import Adapter


class SeabornAdapter(Adapter):
    """Adapter for seaborn."""

    def __init__(self):
        super().__init__("seaborn")

    def _check_availability(self) -> bool:
        """Check if seaborn is available."""
        import importlib.util

        return importlib.util.find_spec("seaborn") is not None

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to seaborn."""
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Set the color palette (check for display mode override)
        try:
            if hasattr(scheme, "_display_mode_colors"):
                discrete_colors = scheme._display_mode_colors
            else:
                discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            sns.set_palette(discrete_colors)
        except Exception as e:
            warnings.warn(f"Failed to set seaborn palette: {e}")

        # Enable smart colormap auto-injection if requested
        if hasattr(scheme, "_intelligence_settings"):
            smart_cmap_enabled = scheme._intelligence_settings.get("smart_cmap", False)
            if smart_cmap_enabled:
                self._enable_smart_colormap(sns, scheme)

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
                "axes.prop_cycle": plt.cycler(color=discrete_colors),
            },
        )

        # Ensure color cycle matches matplotlib
        plt.rcParams["axes.prop_cycle"] = plt.cycler(color=discrete_colors)

    def _enable_smart_colormap(self, sns, scheme: Scheme) -> None:
        """Enable automatic colormap detection for seaborn heatmap."""
        # Save original heatmap function if not already saved
        if not hasattr(sns.heatmap, "_huez_original"):
            original_heatmap = sns.heatmap

            def smart_heatmap(*args, **kwargs):
                # Only auto-inject cmap if user didn't specify one
                if "cmap" not in kwargs and len(args) >= 1:
                    import numpy as np

                    try:
                        # Get the data (first positional argument)
                        data = args[0]

                        # Import intelligence functions
                        from ..core import smart_cmap
                        from ..intelligence.colormap_detection import (
                            detect_colormap_type,
                        )

                        # Auto-detect colormap type
                        cmap_type = detect_colormap_type(data, verbose=False)

                        # Auto-inject colormap
                        kwargs["cmap"] = smart_cmap(data)

                        # 🎯 KEY FEATURE: Auto-center diverging colormaps at 0
                        if cmap_type == "diverging" and "center" not in kwargs:
                            # Check if data crosses 0
                            data_array = np.asarray(data)
                            data_clean = data_array[np.isfinite(data_array)]
                            if (
                                len(data_clean) > 0
                                and data_clean.min() < 0 < data_clean.max()
                            ):
                                kwargs["center"] = 0

                    except Exception:
                        # If detection fails, fall back to original behavior
                        pass

                # Call original heatmap
                return original_heatmap(*args, **kwargs)

            # Mark the wrapper to avoid double-wrapping
            smart_heatmap._huez_original = original_heatmap

            # Replace seaborn's heatmap
            sns.heatmap = smart_heatmap
