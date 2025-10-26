"""
Color Vision Deficiency (CVD) Accessibility Checks

This module provides functions for checking color palette accessibility
and simulating how colors appear to people with different types of color
vision deficiencies.
"""

from typing import Any, Dict, List, Tuple

import numpy as np


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert hex color to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    """Convert RGB tuple (0-1 range) to hex color."""
    return "#{:02x}{:02x}{:02x}".format(
        int(np.clip(rgb[0] * 255, 0, 255)),
        int(np.clip(rgb[1] * 255, 0, 255)),
        int(np.clip(rgb[2] * 255, 0, 255)),
    )


def simulate_cvd(
    rgb: Tuple[float, float, float], cvd_type: str
) -> Tuple[float, float, float]:
    """
    Simulate color vision deficiency for a given RGB color.

    Uses Brettel et al. (1997) and Viénot et al. (1999) transformations.

    Args:
        rgb: RGB tuple with values in [0, 1]
        cvd_type: Type of CVD - "protanopia", "deuteranopia", or "tritanopia"

    Returns:
        RGB tuple showing how the color appears with CVD
    """
    # Simplified CVD simulation matrices
    # These approximate the Brettel/Viénot transformations

    matrices = {
        # Protanopia (red-blind): L-cone absent
        "protanopia": np.array(
            [
                [0.56667, 0.43333, 0.00000],
                [0.55833, 0.44167, 0.00000],
                [0.00000, 0.24167, 0.75833],
            ]
        ),
        # Deuteranopia (green-blind): M-cone absent
        "deuteranopia": np.array(
            [[0.625, 0.375, 0.000], [0.700, 0.300, 0.000], [0.000, 0.300, 0.700]]
        ),
        # Tritanopia (blue-blind): S-cone absent
        "tritanopia": np.array(
            [
                [0.95000, 0.05000, 0.00000],
                [0.00000, 0.43333, 0.56667],
                [0.00000, 0.47500, 0.52500],
            ]
        ),
    }

    if cvd_type not in matrices:
        return rgb

    # Apply transformation matrix
    rgb_array = np.array(rgb)
    transformed = np.dot(matrices[cvd_type], rgb_array)

    # Clip to valid range
    transformed = np.clip(transformed, 0, 1)

    return tuple(transformed)


def color_distance(
    rgb1: Tuple[float, float, float], rgb2: Tuple[float, float, float]
) -> float:
    """
    Calculate perceptual color distance using weighted Euclidean distance.

    This is a simplified approximation. For more accuracy, use LAB space Delta E.

    Args:
        rgb1: First RGB color
        rgb2: Second RGB color

    Returns:
        Distance value (higher = more different)
    """
    # Weighted RGB distance (approximation of perceptual difference)
    # Weights based on human perception sensitivity
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    # Red-mean formula for perceptual distance
    r_mean = (r1 + r2) / 2
    delta_r = r1 - r2
    delta_g = g1 - g2
    delta_b = b1 - b2

    distance = np.sqrt(
        (2 + r_mean) * delta_r**2 + 4 * delta_g**2 + (2 + (1 - r_mean)) * delta_b**2
    )

    return distance


def check_colorblind_safety(
    colors: List[str], threshold: float = 0.15, verbose: bool = True
) -> Dict[str, Any]:
    """
    Check if a color palette is safe for people with color vision deficiencies.

    This function simulates how the colors appear to people with protanopia,
    deuteranopia, and tritanopia, and checks if colors remain distinguishable.

    Args:
        colors: List of hex color strings (e.g., ['#E64B35', '#4DBBD5'])
        threshold: Minimum perceptual distance required for colors to be
                  considered distinguishable (0-1 scale, default 0.15)
        verbose: If True, print detailed analysis

    Returns:
        Dictionary with keys:
        - 'safe' (bool): True if palette is CVD-safe
        - 'warnings' (List[str]): List of potential issues
        - 'cvd_analysis' (Dict): Detailed analysis for each CVD type
        - 'suggestions' (List[str]): Recommendations for improvement

    Examples:
        >>> colors = ['#E64B35', '#4DBBD5', '#00A087']
        >>> result = check_colorblind_safety(colors)
        >>> result['safe']
        True
    """
    if not colors:
        return {"safe": True, "warnings": [], "cvd_analysis": {}, "suggestions": []}

    # Single color is always safe
    if len(colors) == 1:
        return {
            "safe": True,
            "warnings": [],
            "cvd_analysis": {
                "protanopia": {"distinguishable_pairs": [], "problematic_pairs": []},
                "deuteranopia": {"distinguishable_pairs": [], "problematic_pairs": []},
                "tritanopia": {"distinguishable_pairs": [], "problematic_pairs": []},
            },
            "suggestions": [],
        }

    # Convert to RGB
    rgb_colors = [hex_to_rgb(c) for c in colors]

    cvd_types = ["protanopia", "deuteranopia", "tritanopia"]
    cvd_names = {
        "protanopia": "Protanopia (red-blind)",
        "deuteranopia": "Deuteranopia (green-blind)",
        "tritanopia": "Tritanopia (blue-blind)",
    }

    results = {"safe": True, "warnings": [], "cvd_analysis": {}, "suggestions": []}

    # Check each CVD type
    for cvd_type in cvd_types:
        # Simulate how colors appear with this CVD
        simulated_colors = [simulate_cvd(rgb, cvd_type) for rgb in rgb_colors]

        # Check all pairwise distances
        distinguishable = []
        problematic = []

        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                distance = color_distance(simulated_colors[i], simulated_colors[j])

                pair_info = {
                    "color1": colors[i],
                    "color2": colors[j],
                    "distance": distance,
                }

                if distance < threshold:
                    problematic.append(pair_info)
                else:
                    distinguishable.append(pair_info)

        results["cvd_analysis"][cvd_type] = {
            "distinguishable_pairs": distinguishable,
            "problematic_pairs": problematic,
        }

        # Add warnings for problematic pairs
        if problematic:
            results["safe"] = False
            warning = f"{cvd_names[cvd_type]}: {len(problematic)} color pair(s) may be hard to distinguish"
            results["warnings"].append(warning)

            if verbose:
                print(f"⚠️  {warning}")
                for pair in problematic:
                    print(
                        f"   {pair['color1']} ↔ {pair['color2']} (distance: {pair['distance']:.3f})"
                    )

    # Generate suggestions
    if not results["safe"]:
        results["suggestions"].append(
            "Consider using a colorblind-safe palette like Okabe-Ito or ColorBrewer"
        )
        results["suggestions"].append(
            "Increase contrast between problematic color pairs"
        )
        results["suggestions"].append(
            "Add texture or patterns in addition to color coding"
        )

    # Print summary if verbose
    if verbose:
        if results["safe"]:
            print("✅ Color palette is colorblind-safe!")
            print(f"   All {len(colors)} colors are distinguishable for all CVD types.")
        else:
            print("\n💡 Suggestions:")
            for suggestion in results["suggestions"]:
                print(f"   • {suggestion}")

    return results


def get_colorblind_safe_palettes() -> Dict[str, List[str]]:
    """
    Return a collection of known colorblind-safe palettes.

    Returns:
        Dictionary mapping palette names to lists of hex colors
    """
    return {
        "okabe-ito": [
            "#E69F00",  # Orange
            "#56B4E9",  # Sky blue
            "#009E73",  # Bluish green
            "#F0E442",  # Yellow
            "#0072B2",  # Blue
            "#D55E00",  # Vermillion
            "#CC79A7",  # Reddish purple
            "#000000",  # Black
        ],
        "tol-bright": [
            "#EE6677",  # Red
            "#228833",  # Green
            "#4477AA",  # Blue
            "#CCBB44",  # Yellow
            "#66CCEE",  # Cyan
            "#AA3377",  # Purple
            "#BBBBBB",  # Grey
        ],
        "tol-muted": [
            "#332288",  # Indigo
            "#88CCEE",  # Cyan
            "#44AA99",  # Teal
            "#117733",  # Green
            "#999933",  # Olive
            "#DDCC77",  # Sand
            "#CC6677",  # Rose
            "#882255",  # Wine
            "#AA4499",  # Purple
        ],
        "ibm": [
            "#648FFF",  # Blue
            "#785EF0",  # Purple
            "#DC267F",  # Magenta
            "#FE6100",  # Orange
            "#FFB000",  # Gold
        ],
    }
