"""
Quality checks for color palettes - colorblind simulation and contrast analysis.
"""

from typing import Any, Dict, List, Optional

from ..config import Scheme
from ..registry.palettes import get_palette


def check_palette_quality(
    scheme: Scheme, kinds: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Check the quality of palettes in a scheme.

    Args:
        scheme: Color scheme to check
        kinds: Types of palettes to check. If None, checks all.

    Returns:
        Dictionary with quality check results
    """
    if kinds is None:
        kinds = ["discrete", "sequential", "diverging", "cyclic"]

    results = {}

    for kind in kinds:
        try:
            palette_name = getattr(scheme.palettes, kind)
            colors = get_palette(palette_name, kind)

            results[kind] = {
                "palette_name": palette_name,
                "n_colors": len(colors),
                "colors": colors,
                "checks": _check_single_palette(colors, kind),
            }
        except Exception as e:
            results[kind] = {"error": str(e)}

    # Add summary
    results["summary"] = _generate_quality_summary(results)

    return results


def _generate_quality_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of quality check results.

    Args:
        results: Quality check results

    Returns:
        Summary dictionary
    """
    summary = {
        "total_palettes": len([k for k in results.keys() if k != "summary"]),
        "successful_checks": len(
            [k for k, v in results.items() if k != "summary" and "error" not in v]
        ),
        "failed_checks": len(
            [k for k, v in results.items() if k != "summary" and "error" in v]
        ),
        "overall_score": 0.0,
    }

    if summary["total_palettes"] > 0:
        summary["overall_score"] = (
            summary["successful_checks"] / summary["total_palettes"]
        )

    return summary


def _check_single_palette(colors: List[str], kind: str) -> Dict[str, Any]:
    """
    Check a single palette for quality issues.

    Args:
        colors: List of hex color strings
        kind: Palette kind

    Returns:
        Dictionary with check results
    """
    checks = {}

    # Basic checks
    checks["has_colors"] = len(colors) > 0
    checks["unique_colors"] = len(colors) == len(set(colors))

    # Colorblind simulation
    if _has_colorblind_simulation():
        checks["colorblind_safe"] = _check_colorblind_safety(colors)
    else:
        checks["colorblind_safe"] = "simulation_unavailable"

    # Contrast checks
    checks["contrast_ratios"] = _calculate_contrast_ratios(colors)

    # Specific checks based on palette kind
    if kind == "discrete":
        checks["distinctiveness"] = _check_distinctiveness(colors)
    elif kind in ["sequential", "diverging"]:
        checks["monotonic"] = _check_monotonicity(colors, kind)
    elif kind == "cyclic":
        checks["cyclic_property"] = _check_cyclic_property(colors)

    return checks


def _has_colorblind_simulation() -> bool:
    """Check if colorblind simulation libraries are available."""
    import importlib.util

    return (
        importlib.util.find_spec("colorspacious") is not None
        or importlib.util.find_spec("cv2") is not None
    )


def _check_colorblind_safety(colors: List[str]) -> Dict[str, Any]:
    """
    Check if colors are distinguishable under different colorblind conditions.

    Args:
        colors: List of hex colors

    Returns:
        Dictionary with colorblind safety results
    """
    results = {}

    # Convert hex to RGB
    rgb_colors = [_hex_to_rgb(color) for color in colors]

    # Simulate different types of colorblindness
    colorblind_types = ["protanopia", "deuteranopia", "tritanopia"]

    for cb_type in colorblind_types:
        try:
            simulated = _simulate_colorblindness(rgb_colors, cb_type)
            results[cb_type] = _check_distinguishable(simulated)
        except Exception as e:
            results[cb_type] = f"simulation_failed: {e}"

    # Also check grayscale
    try:
        grayscale = _convert_to_grayscale(rgb_colors)
        results["grayscale"] = _check_distinguishable(grayscale)
    except Exception as e:
        results["grayscale"] = f"conversion_failed: {e}"

    return results


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb: tuple) -> str:
    """Convert RGB tuple to hex color."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def _simulate_colorblindness(colors: List[tuple], cb_type: str) -> List[tuple]:
    """
    Simulate colorblindness transformation.

    Args:
        colors: List of RGB tuples
        cb_type: Type of colorblindness

    Returns:
        List of transformed RGB tuples
    """
    import importlib.util

    if importlib.util.find_spec("colorspacious") is not None:
        # Colorblind transformation matrices
        matrices = {
            "protanopia": [[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]],
            "deuteranopia": [[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]],
            "tritanopia": [[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]],
        }

        if cb_type not in matrices:
            raise ValueError(f"Unknown colorblind type: {cb_type}")

        matrix = matrices[cb_type]
        transformed = []

        for rgb in colors:
            # Convert to linear RGB for matrix multiplication
            r, g, b = [x / 255.0 for x in rgb]

            # Apply transformation
            new_r = matrix[0][0] * r + matrix[0][1] * g + matrix[0][2] * b
            new_g = matrix[1][0] * r + matrix[1][1] * g + matrix[1][2] * b
            new_b = matrix[2][0] * r + matrix[2][1] * g + matrix[2][2] * b

            # Convert back to 0-255 range
            transformed_rgb = (
                max(0, min(255, int(new_r * 255))),
                max(0, min(255, int(new_g * 255))),
                max(0, min(255, int(new_b * 255))),
            )
            transformed.append(transformed_rgb)

        return transformed
    else:
        # Fallback to simple desaturation
        return _simple_colorblind_simulation(colors, cb_type)


def _simple_colorblind_simulation(colors: List[tuple], cb_type: str) -> List[tuple]:
    """Simple fallback colorblind simulation."""
    transformed = []

    for r, g, b in colors:
        if cb_type == "protanopia":
            # Reduce red sensitivity
            new_r = int(r * 0.567 + g * 0.433)
            new_g = int(r * 0.558 + g * 0.442)
            new_b = b
        elif cb_type == "deuteranopia":
            # Reduce green sensitivity
            new_r = int(r * 0.625 + g * 0.375)
            new_g = int(r * 0.7 + g * 0.3)
            new_b = b
        elif cb_type == "tritanopia":
            # Reduce blue sensitivity
            new_r = r
            new_g = int(g * 0.433 + b * 0.567)
            new_b = int(g * 0.242 + b * 0.758)
        else:
            new_r, new_g, new_b = r, g, b

        transformed.append((new_r, new_g, new_b))

    return transformed


def _convert_to_grayscale(colors: List[tuple]) -> List[tuple]:
    """Convert colors to grayscale."""
    grayscale = []

    for r, g, b in colors:
        # Standard luminance calculation
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        grayscale.append((gray, gray, gray))

    return grayscale


def _check_distinguishable(colors: List[tuple]) -> bool:
    """
    Check if colors are distinguishable from each other.

    Args:
        colors: List of RGB tuples

    Returns:
        True if all colors are distinguishable
    """
    if len(colors) < 2:
        return True

    min_distance = float("inf")

    for i, color1 in enumerate(colors):
        for j, color2 in enumerate(colors):
            if i != j:
                distance = _color_distance(color1, color2)
                min_distance = min(min_distance, distance)

    # Colors are distinguishable if minimum distance is > 10
    return min_distance > 10


def _color_distance(color1: tuple, color2: tuple) -> float:
    """Calculate Euclidean distance between two colors in RGB space."""
    return (
        (color1[0] - color2[0]) ** 2
        + (color1[1] - color2[1]) ** 2
        + (color1[2] - color2[2]) ** 2
    ) ** 0.5


def _calculate_contrast_ratios(colors: List[str]) -> List[float]:
    """
    Calculate contrast ratios between all pairs of colors.

    Args:
        colors: List of hex colors

    Returns:
        List of contrast ratios
    """
    if len(colors) < 2:
        return []

    ratios = []

    for i, color1 in enumerate(colors):
        rgb1 = _hex_to_rgb(color1)
        lum1 = _calculate_luminance(rgb1)

        for j, color2 in enumerate(colors):
            if i < j:
                rgb2 = _hex_to_rgb(color2)
                lum2 = _calculate_luminance(rgb2)

                ratio = _contrast_ratio(lum1, lum2)
                ratios.append(ratio)

    return ratios


def _calculate_luminance(rgb: tuple) -> float:
    """Calculate relative luminance of an RGB color."""
    r, g, b = [x / 255.0 for x in rgb]

    # Apply gamma correction
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(lum1: float, lum2: float) -> float:
    """Calculate contrast ratio between two luminances."""
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


def _check_distinctiveness(colors: List[str]) -> bool:
    """Check if discrete colors are sufficiently distinct."""
    if len(colors) < 2:
        return True

    rgb_colors = [_hex_to_rgb(color) for color in colors]

    for i, color1 in enumerate(rgb_colors):
        for j, color2 in enumerate(rgb_colors):
            if i != j:
                distance = _color_distance(color1, color2)
                if distance < 30:  # Minimum distance threshold
                    return False

    return True


def _check_monotonicity(colors: List[str], kind: str) -> bool:
    """Check if sequential/diverging palettes are monotonic in luminance."""
    if len(colors) < 3:
        return True

    rgb_colors = [_hex_to_rgb(color) for color in colors]
    luminances = [_calculate_luminance(rgb) for rgb in rgb_colors]

    if kind == "sequential":
        # Should be monotonically increasing
        return all(
            luminances[i] <= luminances[i + 1] for i in range(len(luminances) - 1)
        )
    elif kind == "diverging":
        # Should increase then decrease, or vice versa
        mid = len(luminances) // 2
        left = luminances[: mid + 1]
        right = luminances[mid:]

        left_mono = all(left[i] <= left[i + 1] for i in range(len(left) - 1))
        right_mono = all(right[i] >= right[i + 1] for i in range(len(right) - 1))

        return left_mono and right_mono

    return True


def _check_cyclic_property(colors: List[str]) -> bool:
    """Check if cyclic palette wraps around properly."""
    if len(colors) < 3:
        return True

    # First and last colors should be similar for good cyclic property
    rgb_first = _hex_to_rgb(colors[0])
    rgb_last = _hex_to_rgb(colors[-1])

    distance = _color_distance(rgb_first, rgb_last)
    return distance < 50  # Allow some tolerance
