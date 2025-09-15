"""
Color correction module - Compensate for rendering differences across different plotting libraries
"""

import colorsys
from typing import List, Dict, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hexadecimal color to RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB to hexadecimal color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def adjust_brightness(hex_color: str, factor: float) -> str:
    """Adjust color brightness"""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

    # Adjust brightness
    l = max(0, min(1, l * factor))
    
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex((int(r*255), int(g*255), int(b*255)))


def adjust_saturation(hex_color: str, factor: float) -> str:
    """Adjust color saturation"""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

    # Adjust saturation
    s = max(0, min(1, s * factor))
    
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex((int(r*255), int(g*255), int(b*255)))


# Minimal intervention color correction (only for the most obvious issues)
LIBRARY_CORRECTIONS = {
    "plotly": {
        "brightness": 0.97,  # Slightly darken to match other libraries
        "saturation": 1.0,   # No saturation adjustment
        "gamma": 1.0
    },
    "altair": {
        "brightness": 1.0,   # No adjustment
        "saturation": 1.0,   # No adjustment
        "gamma": 1.0
    },
    "seaborn": {
        "brightness": 1.0,   # Keep consistent
        "saturation": 1.0,
        "gamma": 1.0
    },
    "matplotlib": {
        "brightness": 1.0,   # Baseline
        "saturation": 1.0,
        "gamma": 1.0
    },
    "plotnine": {
        "brightness": 1.0,   # No adjustment
        "saturation": 1.0,   # No adjustment
        "gamma": 1.0
    }
}


def correct_colors_for_library(colors: List[str], library: str) -> List[str]:
    """
    Correct colors for a specific library

    Args:
        colors: Original color list
        library: Target library name

    Returns:
        Corrected color list
    """
    if library not in LIBRARY_CORRECTIONS:
        return colors
    
    correction = LIBRARY_CORRECTIONS[library]
    corrected_colors = []
    
    for color in colors:
        # Apply brightness correction
        if correction["brightness"] != 1.0:
            color = adjust_brightness(color, correction["brightness"])

        # Apply saturation correction
        if correction["saturation"] != 1.0:
            color = adjust_saturation(color, correction["saturation"])
        
        corrected_colors.append(color)
    
    return corrected_colors


def get_corrected_palette(base_colors: List[str], target_library: str) -> List[str]:
    """
    Get palette optimized for a specific library

    Args:
        base_colors: Base color list
        target_library: Target library name

    Returns:
        Optimized color list
    """
    return correct_colors_for_library(base_colors, target_library)


def analyze_color_difference(color1: str, color2: str) -> Dict[str, float]:
    """
    Analyze the difference between two colors

    Args:
        color1: First color
        color2: Second color

    Returns:
        Dictionary containing various difference metrics
    """
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    # Euclidean distance
    euclidean = ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)**0.5

    # Perceptual difference (simplified version)
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2

    # Weighted perceptual difference (human eye most sensitive to green)
    perceptual = (2*dr**2 + 4*dg**2 + 3*db**2)**0.5

    return {
        "euclidean": euclidean,
        "perceptual": perceptual,
        "red_diff": abs(dr),
        "green_diff": abs(dg),
        "blue_diff": abs(db)
    }


def get_best_colormap_for_library(cmap_name: str, library: str) -> str:
    """
    Select the best colormap name for a specific library

    Args:
        cmap_name: Original colormap name
        library: Target library name

    Returns:
        Best colormap name for the library
    """
    # Colormap mappings supported by each library
    library_colormaps = {
        "matplotlib": {
            "viridis", "plasma", "inferno", "magma", "cividis",
            "coolwarm", "bwr", "seismic", "RdBu", "RdYlBu", "PiYG"
        },
        "plotly": {
            "viridis", "plasma", "inferno", "magma", "cividis",
            "rdbu", "rdylbu", "spectral", "bluered"
        },
        "altair": {
            "viridis", "plasma", "inferno", "magma", "cividis",
            "redblue", "redyellowblue", "brownbluegreen", "purpleorange"
        },
        "plotnine": {
            "viridis", "plasma", "inferno", "magma", "cividis",
            "coolwarm", "seismic", "RdBu", "RdYlBu"
        }
    }

    supported = library_colormaps.get(library, set())

    # If original name is supported, return it directly
    if cmap_name in supported:
        return cmap_name

    # Otherwise choose the best alternative
    alternatives = {
        "coolwarm": ["rdbu", "redblue", "RdBu"],
        "seismic": ["rdbu", "redblue", "RdBu"],
        "RdBu": ["rdbu", "redblue", "coolwarm"],
        "RdYlBu": ["rdylbu", "redyellowblue", "coolwarm"]
    }

    if cmap_name in alternatives:
        for alt in alternatives[cmap_name]:
            if alt in supported:
                return alt

    # Default fallback
    defaults = {
        "matplotlib": "viridis",
        "plotly": "viridis",
        "altair": "viridis",
        "plotnine": "viridis"
    }

    return defaults.get(library, "viridis")
