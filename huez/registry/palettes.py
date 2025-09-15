"""
Color palette registry for huez.

Contains built-in palettes with permissive licenses (MIT/BSD/CC-BY)
and fallback mechanisms for missing palettes.
"""

import warnings
from typing import List, Dict, Any, Optional
from functools import lru_cache


# Built-in color palettes
# Okabe-Ito colorblind-friendly palette
OKABE_ITO = [
    '#E69F00',  # Orange
    '#56B4E9',  # Sky Blue
    '#009E73',  # Bluish Green
    '#F0E442',  # Yellow
    '#0072B2',  # Blue
    '#D55E00',  # Vermilion
    '#CC79A7',  # Reddish Purple
    '#000000',  # Black
]

# Paul Tol Bright
PAUL_TOL_BRIGHT = [
    '#4477AA', '#66CCEE', '#228833', '#CCBB44',
    '#EE6677', '#AA3377', '#BBBBBB'
]

# Paul Tol High-contrast
PAUL_TOL_HIGH_CONTRAST = [
    '#004488', '#DDAA33', '#BB5566'
]

# Paul Tol Vibrant
PAUL_TOL_VIBRANT = [
    '#0077BB', '#33BBEE', '#009988', '#EE7733',
    '#CC3311', '#EE3377', '#BBBBBB'
]

# Paul Tol Muted
PAUL_TOL_MUTED = [
    '#332288', '#88CCEE', '#44AA99', '#117733',
    '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499'
]

# Tableau 10
TABLEAU_10 = [
    '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
    '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC'
]

# CartoColor Bold
CARTOCOLOR_BOLD = [
    '#7F3C8D', '#11A579', '#3969AC', '#F2B701', '#E73F74',
    '#80BA5A', '#E68310', '#008695', '#CF1C90', '#F97B72'
]

# Glasbey (subset for categorical data)
GLASBEY = [
    '#0000FF', '#FF0000', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF',
    '#000080', '#800000', '#008000', '#808000', '#800080', '#008080',
    '#000040', '#400000', '#004000', '#404000', '#400040', '#004040'
]

# Scientific journal color palettes
# Nature Publishing Group (NPG) colors
NPG_COLORS = [
    '#E64B35',  # Red
    '#4DBBD5',  # Cyan
    '#00A087',  # Teal
    '#3C5488',  # Blue
    '#F39B7F',  # Coral
    '#8491B4',  # Purple
    '#91D1C2',  # Mint
    '#DC0000',  # Crimson
    '#7E6148',  # Brown
    '#B09C85'   # Tan
]

# American Association for the Advancement of Science (AAAS/Science)
AAAS_COLORS = [
    '#3B4992',  # Blue
    '#EE0000',  # Red
    '#008B45',  # Green
    '#631879',  # Purple
    '#008280',  # Teal
    '#BB0021',  # Crimson
    '#5F559B',  # Indigo
    '#A20056',  # Magenta
    '#808180',  # Gray
    '#1B1919'   # Black
]

# New England Journal of Medicine (NEJM)
NEJM_COLORS = [
    '#BC3C29',  # Red
    '#0072B5',  # Blue
    '#E18727',  # Orange
    '#20854E',  # Green
    '#7876B1',  # Purple
    '#6F99AD',  # Cyan
    '#FFDC91',  # Yellow
    '#EE4C97',  # Pink
    '#8C564B',  # Brown
    '#000000'   # Black
]

# The Lancet
LANCET_COLORS = [
    '#00468B',  # Blue
    '#ED0000',  # Red
    '#42B540',  # Green
    '#0099B4',  # Cyan
    '#925E9F',  # Purple
    '#FDAF91',  # Peach
    '#AD002A',  # Crimson
    '#ADB6B6',  # Gray
    '#1B1919',  # Black
    '#6F99AD'   # Teal
]

# Journal of the American Medical Association (JAMA)
JAMA_COLORS = [
    '#374E55',  # Dark Blue Gray
    '#DF8F44',  # Orange
    '#00A1D5',  # Blue
    '#B24745',  # Red
    '#79AF97',  # Green
    '#6A6599',  # Purple
    '#80796B',  # Brown
    '#8E8E8E',  # Gray
    '#000000',  # Black
    '#FFFFFF'   # White
]

# British Medical Journal (BMJ)
BMJ_COLORS = [
    '#2E2E2E',  # Dark Gray
    '#A11D21',  # Red
    '#215967',  # Teal
    '#C3B381',  # Tan
    '#64807F',  # Sage
    '#8E8E8E',  # Light Gray
    '#000000',  # Black
    '#FFFFFF',  # White
    '#EDEDED',  # Very Light Gray
    '#D4D4D4'   # Light Gray
]


# Registry of built-in palettes
PALETTE_REGISTRY = {
    "discrete": {
        "okabe-ito": OKABE_ITO,
        "paul-tol-bright": PAUL_TOL_BRIGHT,
        "paul-tol-high-contrast": PAUL_TOL_HIGH_CONTRAST,
        "paul-tol-vibrant": PAUL_TOL_VIBRANT,
        "paul-tol-muted": PAUL_TOL_MUTED,
        "tableau-10": TABLEAU_10,
        "cartocolor-bold": CARTOCOLOR_BOLD,
        "glasbey": GLASBEY,
        # Scientific journal palettes
        "npg": NPG_COLORS,
        "aaas": AAAS_COLORS,
        "nejm": NEJM_COLORS,
        "lancet": LANCET_COLORS,
        "jama": JAMA_COLORS,
        "bmj": BMJ_COLORS,
    },
    "sequential": {
        # These will map to matplotlib/seaborn colormap names
        "viridis": "viridis",
        "cividis": "cividis",
        "plasma": "plasma",
        "inferno": "inferno",
        "magma": "magma",
        "batlow": "batlow",  # From cmcrameri
        "lapaz": "lapaz",    # From cmcrameri
        "thermal": "thermal", # From cmocean
        "fire": "fire",      # From cmocean
    },
    "diverging": {
        "vik": "vik",        # From cmcrameri
        "roma": "roma",      # From cmcrameri
        "broc": "broc",      # From cmcrameri
        "coolwarm": "coolwarm",
        "RdBu": "RdBu",
        "RdYlBu": "RdYlBu",
        "Spectral": "Spectral",
        "balance": "balance", # From cmocean
    },
    "cyclic": {
        "twilight": "twilight",
        "twilight_shifted": "twilight_shifted",
        "hsv": "hsv",
        "phase": "phase",    # From cmocean
    }
}


# Fallback mappings for when specific palettes are not available
FALLBACKS = {
    "discrete": {
        "default": "okabe-ito",
        "glasbey": "okabe-ito",  # Fallback if distinctipy not available
    },
    "sequential": {
        "batlow": "viridis",
        "lapaz": "cividis",
        "thermal": "plasma",
        "fire": "inferno",
        "default": "viridis",
    },
    "diverging": {
        "vik": "coolwarm",
        "roma": "RdBu",
        "broc": "RdYlBu",
        "balance": "Spectral",
        "default": "coolwarm",
    },
    "cyclic": {
        "phase": "twilight",
        "default": "twilight",
    }
}


def validate_palette_name(name: str, kind: str) -> bool:
    """
    Check if a palette name exists in the registry.

    Args:
        name: Palette name
        kind: Palette kind ("discrete", "sequential", "diverging", "cyclic")

    Returns:
        True if palette exists or has a fallback
    """
    if kind not in PALETTE_REGISTRY:
        return False

    return name in PALETTE_REGISTRY[kind] or name in FALLBACKS[kind]


@lru_cache(maxsize=128)
def get_palette(name: str, kind: str = "discrete", n: Optional[int] = None) -> List[str]:
    """
    Get a color palette by name.

    Args:
        name: Palette name
        kind: Palette kind ("discrete", "sequential", "diverging", "cyclic")
        n: Number of colors (for discrete palettes)

    Returns:
        List of hex color strings

    Raises:
        ValueError: If palette is not found and no fallback available
    """
    if kind not in PALETTE_REGISTRY:
        raise ValueError(f"Unknown palette kind: {kind}")

    registry = PALETTE_REGISTRY[kind]

    # Try to get the palette directly
    if name in registry:
        palette_data = registry[name]

        if kind == "discrete":
            # For discrete palettes, return colors as list
            colors = palette_data
            if n is not None and n > len(colors):
                # Cycle through colors if more are needed
                import itertools
                colors = list(itertools.islice(itertools.cycle(colors), n))
            elif n is not None and n < len(colors):
                colors = colors[:n]
            return colors
        else:
            # For other kinds, try to get colors from matplotlib
            return _get_colormap_colors(palette_data, n or 256)

    # Try fallback
    if name in FALLBACKS[kind]:
        fallback_name = FALLBACKS[kind][name]
        warnings.warn(f"Palette '{name}' not found, using fallback '{fallback_name}'")
        return get_palette(fallback_name, kind, n)

    # Use default fallback
    if "default" in FALLBACKS[kind]:
        default_name = FALLBACKS[kind]["default"]
        warnings.warn(f"Palette '{name}' not found, using default '{default_name}'")
        return get_palette(default_name, kind, n)

    raise ValueError(f"Palette '{name}' not found and no fallback available")


@lru_cache(maxsize=128)
def get_colormap(name: str, kind: str = "sequential") -> str:
    """
    Get a colormap name by palette name.

    Args:
        name: Palette name
        kind: Palette kind

    Returns:
        Colormap name string
    """
    if kind not in PALETTE_REGISTRY:
        raise ValueError(f"Unknown palette kind: {kind}")

    registry = PALETTE_REGISTRY[kind]

    # Try to get the colormap directly
    if name in registry:
        cmap_name = registry[name]

        # Check if colormap exists in matplotlib
        if _colormap_exists(cmap_name):
            return cmap_name

    # Try fallback
    if name in FALLBACKS[kind]:
        fallback_name = FALLBACKS[kind][name]
        warnings.warn(f"Colormap '{name}' not found, using fallback '{fallback_name}'")
        return get_colormap(fallback_name, kind)

    # Use default fallback
    if "default" in FALLBACKS[kind]:
        default_name = FALLBACKS[kind]["default"]
        warnings.warn(f"Colormap '{name}' not found, using default '{default_name}'")
        return get_colormap(default_name, kind)

    raise ValueError(f"Colormap '{name}' not found and no fallback available")


def _get_colormap_colors(cmap_name: str, n: int = 256) -> List[str]:
    """
    Get colors from a matplotlib colormap.

    Args:
        cmap_name: Colormap name
        n: Number of colors

    Returns:
        List of hex color strings
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        cmap = plt.get_cmap(cmap_name)
        colors = cmap(np.linspace(0, 1, n))
        return [f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}' for r, g, b, _ in colors]

    except (ImportError, ValueError):
        # Fallback to a simple gradient
        return _create_fallback_gradient(n)


def _colormap_exists(cmap_name: str) -> bool:
    """
    Check if a colormap exists in matplotlib.

    Args:
        cmap_name: Colormap name

    Returns:
        True if colormap exists
    """
    try:
        import matplotlib.pyplot as plt
        plt.get_cmap(cmap_name)
        return True
    except (ImportError, ValueError):
        return False


def _create_fallback_gradient(n: int) -> List[str]:
    """
    Create a simple fallback color gradient.

    Args:
        n: Number of colors

    Returns:
        List of hex color strings
    """
    colors = []
    for i in range(n):
        # Simple blue to red gradient
        r = int(255 * (i / (n - 1)))
        b = int(255 * (1 - i / (n - 1)))
        g = 0
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    return colors


def list_available_palettes(kind: Optional[str] = None) -> Dict[str, List[str]]:
    """
    List all available palettes.

    Args:
        kind: Optional palette kind filter

    Returns:
        Dictionary mapping kinds to palette names
    """
    if kind is None:
        return {k: list(v.keys()) for k, v in PALETTE_REGISTRY.items()}

    if kind not in PALETTE_REGISTRY:
        return {}

    return {kind: list(PALETTE_REGISTRY[kind].keys())}


def get_palette_info(name: str, kind: str) -> Dict[str, Any]:
    """
    Get information about a palette.

    Args:
        name: Palette name
        kind: Palette kind

    Returns:
        Dictionary with palette information
    """
    try:
        colors = get_palette(name, kind)
        return {
            "name": name,
            "kind": kind,
            "colors": colors,
            "n_colors": len(colors)
        }
    except ValueError as e:
        return {
            "name": name,
            "kind": kind,
            "error": str(e)
        }
