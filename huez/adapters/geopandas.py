"""
GeoPandas adapter for huez.
"""

import warnings
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class GeoPandasAdapter(Adapter):
    """Adapter for GeoPandas."""

    def __init__(self):
        super().__init__("geopandas")

    def _check_availability(self) -> bool:
        """Check if geopandas is available."""
        try:
            import geopandas as gpd
            return True
        except (ImportError, FileNotFoundError, OSError):
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to GeoPandas."""
        # GeoPandas inherits matplotlib settings, so we don't need to do much here
        # The main work is done by the matplotlib adapter

        # However, we can set some GeoPandas-specific defaults
        try:
            import geopandas as gpd
        except (ImportError, FileNotFoundError, OSError) as e:
            warnings.warn(f"GeoPandas not available: {e}")
            return

            # Set default colormaps for geographic data
            # These are optimized for geographic visualization
            geo_colormaps = {
                'sequential': 'viridis',  # Good for choropleth maps
                'diverging': 'RdYlBu_r',  # Good for difference maps
            }

            # Store in global defaults for GeoPandas to use
            if hasattr(gpd, '_default_options'):
                gpd._default_options.update({
                    'cmap': geo_colormaps['sequential']
                })

        except Exception as e:
            warnings.warn(f"Failed to apply GeoPandas settings: {e}")


def get_geographic_colormap(kind: str = "sequential") -> str:
    """
    Get geographic-optimized colormap.

    Args:
        kind: Type of colormap ("sequential" or "diverging")

    Returns:
        Colormap name optimized for geographic data
    """
    geo_colormaps = {
        'sequential': 'viridis',      # Perceptually uniform, good for choropleth
        'diverging': 'RdYlBu_r',      # Blue-red diverging, good for differences
        'categorical': 'tab10'        # Categorical data
    }

    return geo_colormaps.get(kind, geo_colormaps['sequential'])
