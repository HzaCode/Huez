"""
Journal-inspired palette registry.

This module provides entry points for journal-style palettes.
The actual color values are NOT stored here to avoid GPL licensing issues.
Instead, we provide mechanisms to fetch them at runtime or through optional plugins.
"""

import warnings
from typing import Any, Dict, List, Optional

# Journal palette entry points
# These are just names - actual colors are fetched at runtime
JOURNAL_PALETTES = {
    "discrete": {
        # Nature Publishing Group
        "npg": None,  # Will be fetched from ggsci at runtime
        # American Association for the Advancement of Science
        "aaas": None,
        # New England Journal of Medicine
        "nejm": None,
        # The Lancet
        "lancet": None,
        # Journal of the American Medical Association
        "jama": None,
        # British Medical Journal
        "bmj": None,
        # Journal of Clinical Oncology
        "jco": None,
    }
}


def is_journal_palette(name: str) -> bool:
    """
    Check if a palette name is a journal palette.

    Args:
        name: Palette name

    Returns:
        True if it's a journal palette
    """
    for kind_palettes in JOURNAL_PALETTES.values():
        if name in kind_palettes:
            return True
    return False


def get_journal_palette(
    name: str, kind: str = "discrete", n: Optional[int] = None
) -> List[str]:
    """
    Get a journal palette.

    This will attempt to fetch the palette from various sources:
    1. Optional huez-ggsci plugin
    2. Runtime fetch from R ggsci (requires rpy2)
    3. Fallback to built-in alternatives

    Args:
        name: Journal palette name
        kind: Palette kind (usually "discrete")
        n: Number of colors

    Returns:
        List of hex color strings

    Raises:
        ValueError: If palette cannot be found
    """
    # Try huez-ggsci plugin first
    try:
        from huez_ggsci import get_palette

        return get_palette(name, n=n)
    except ImportError:
        pass

    # Try runtime fetch from R ggsci
    try:
        return _fetch_from_r_ggsci(name, n)
    except Exception as e:
        warnings.warn(f"Failed to fetch '{name}' from R ggsci: {e}", stacklevel=2)

    # Use fallback
    fallback = _get_journal_fallback(name)
    if fallback:
        warnings.warn(
            f"Journal palette '{name}' not available, using fallback '{fallback}'",
            stacklevel=2,
        )
        from .palettes import get_palette

        return get_palette(fallback, kind, n)

    raise ValueError(f"Journal palette '{name}' not found and no fallback available")


def _fetch_from_r_ggsci(name: str, n: Optional[int] = None) -> List[str]:
    """
    Fetch palette from R ggsci at runtime using rpy2.

    Args:
        name: Palette name
        n: Number of colors

    Returns:
        List of hex color strings

    Raises:
        Exception: If fetch fails
    """
    try:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri

        pandas2ri.activate()

        # Import ggsci
        ro.r("library(ggsci)")

        # Get palette function
        palette_func = ro.r(f"ggsci::pal_{name}")

        # Call the palette function
        if n is not None:
            colors_r = palette_func(n)
        else:
            colors_r = palette_func()

        # Convert to Python list
        colors = list(colors_r)

        return colors

    except ImportError:
        raise Exception("rpy2 not installed. Install with: pip install rpy2") from None
    except Exception as e:
        raise Exception(f"Failed to fetch from R ggsci: {e}") from e


def _get_journal_fallback(name: str) -> Optional[str]:
    """
    Get fallback palette for a journal palette.

    Args:
        name: Journal palette name

    Returns:
        Fallback palette name or None
    """
    fallbacks = {
        "npg": "okabe-ito",
        "aaas": "paul-tol-bright",
        "nejm": "paul-tol-muted",
        "lancet": "tableau-10",
        "jama": "cartocolor-bold",
        "bmj": "glasbey",
        "jco": "okabe-ito",
    }

    return fallbacks.get(name)


def list_journal_palettes() -> Dict[str, List[str]]:
    """
    List all available journal palettes.

    Returns:
        Dictionary mapping kinds to palette names
    """
    return {kind: list(names.keys()) for kind, names in JOURNAL_PALETTES.items()}


def get_journal_palette_info(name: str) -> Dict[str, Any]:
    """
    Get information about a journal palette.

    Args:
        name: Journal palette name

    Returns:
        Dictionary with palette information
    """
    try:
        colors = get_journal_palette(name)
        return {
            "name": name,
            "kind": "discrete",
            "colors": colors,
            "n_colors": len(colors),
            "source": "journal",
            "available": True,
        }
    except ValueError as e:
        return {
            "name": name,
            "kind": "discrete",
            "error": str(e),
            "source": "journal",
            "available": False,
        }
