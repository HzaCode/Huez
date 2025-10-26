"""
Huez Intelligence Module

Provides intelligent features for color management:
- Color expansion using LAB interpolation
- Automatic colormap detection
- Color accessibility checks for CVD
"""

from .accessibility import (check_colorblind_safety,
                            get_colorblind_safe_palettes)
from .color_expansion import intelligent_color_expansion
from .colormap_detection import detect_colormap_type, suggest_colormap

__all__ = [
    "intelligent_color_expansion",
    "detect_colormap_type",
    "suggest_colormap",
    "check_colorblind_safety",
    "get_colorblind_safe_palettes",
]
