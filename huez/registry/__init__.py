"""
Color palette registry for huez.
"""

from .journals import (
    get_journal_palette,
    get_journal_palette_info,
    is_journal_palette,
    list_journal_palettes,
)
from .palettes import (
    get_colormap,
    get_palette,
    get_palette_info,
    list_available_palettes,
    validate_palette_name,
)

__all__ = [
    "get_palette",
    "get_colormap",
    "list_available_palettes",
    "get_palette_info",
    "validate_palette_name",
    "get_journal_palette",
    "list_journal_palettes",
    "get_journal_palette_info",
    "is_journal_palette",
]
