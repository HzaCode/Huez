"""
Intelligent Color Expansion using LAB color space

This module provides functions for expanding color palettes while maintaining
perceptual uniformity. Colors are interpolated in LAB color space to ensure
that the generated colors are evenly distributed in terms of human perception.
"""

import warnings
from typing import List

import numpy as np


def hex_to_rgb(hex_color: str) -> tuple:
    """
    Convert hex color to RGB tuple.

    Args:
        hex_color: Hex color string (e.g., '#E64B35')

    Returns:
        RGB tuple with values in [0, 1]
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple) -> str:
    """
    Convert RGB tuple to hex color string.

    Args:
        rgb: RGB tuple with values in [0, 1]

    Returns:
        Hex color string (e.g., '#E64B35')
    """
    return f"#{int(np.clip(rgb[0] * 255, 0, 255)):02x}{int(np.clip(rgb[1] * 255, 0, 255)):02x}{int(np.clip(rgb[2] * 255, 0, 255)):02x}"


def rgb_to_lab(rgb: tuple) -> np.ndarray:
    """
    Convert RGB to LAB color space.

    Args:
        rgb: RGB tuple with values in [0, 1]

    Returns:
        LAB color as numpy array [L, a, b]
    """
    # First convert RGB to XYZ
    r, g, b = rgb

    # Linearize RGB
    def linearize(c):
        if c <= 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r_lin = linearize(r)
    g_lin = linearize(g)
    b_lin = linearize(b)

    # RGB to XYZ (using D65 illuminant)
    x = r_lin * 0.4124564 + g_lin * 0.3575761 + b_lin * 0.1804375
    y = r_lin * 0.2126729 + g_lin * 0.7151522 + b_lin * 0.0721750
    z = r_lin * 0.0193339 + g_lin * 0.1191920 + b_lin * 0.9503041

    # Normalize by D65 white point
    x = x / 0.95047
    y = y / 1.00000
    z = z / 1.08883

    # XYZ to LAB
    def f(t):
        delta = 6 / 29
        if t > delta**3:
            return t ** (1 / 3)
        else:
            return t / (3 * delta**2) + 4 / 29

    fx = f(x)
    fy = f(y)
    fz = f(z)

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    return np.array([L, a, b])


def lab_to_rgb(lab: np.ndarray) -> tuple:
    """
    Convert LAB color space to RGB.

    Args:
        lab: LAB color as numpy array [L, a, b]

    Returns:
        RGB tuple with values in [0, 1]
    """
    L, a, b = lab

    # LAB to XYZ
    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    def f_inv(t):
        delta = 6 / 29
        if t > delta:
            return t**3
        else:
            return 3 * delta**2 * (t - 4 / 29)

    x = f_inv(fx) * 0.95047
    y = f_inv(fy) * 1.00000
    z = f_inv(fz) * 1.08883

    # XYZ to RGB
    r_lin = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g_lin = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b_lin = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    # Delinearize
    def delinearize(c):
        if c <= 0.0031308:
            return 12.92 * c
        else:
            return 1.055 * c ** (1 / 2.4) - 0.055

    r = delinearize(r_lin)
    g = delinearize(g_lin)
    b = delinearize(b_lin)

    return (r, g, b)


def intelligent_color_expansion(base_colors: List[str], n_needed: int) -> List[str]:
    """
    Expand a color palette to a larger number of colors using LAB interpolation.

    This function interpolates colors in the perceptually uniform LAB color space
    to generate a larger palette while maintaining visual distinctiveness.

    Args:
        base_colors: List of hex color strings (e.g., ['#E64B35', '#4DBBD5'])
        n_needed: Number of colors needed in the output

    Returns:
        List of hex color strings with length n_needed

    Examples:
        >>> base = ['#E64B35', '#4DBBD5', '#00A087']
        >>> expanded = intelligent_color_expansion(base, 10)
        >>> len(expanded)
        10
    """
    if n_needed <= 0:
        raise ValueError(f"n_needed must be positive, got {n_needed}")

    if not base_colors:
        raise ValueError("base_colors cannot be empty")

    # If we need fewer or equal colors than base, just return subset
    if n_needed <= len(base_colors):
        return base_colors[:n_needed]

    # Warn user about expansion
    warnings.warn(
        f"Expanding palette from {len(base_colors)} to {n_needed} colors using LAB interpolation",
        UserWarning,
        stacklevel=2,
    )

    # Convert base colors to LAB
    lab_colors = []
    for hex_color in base_colors:
        rgb = hex_to_rgb(hex_color)
        lab = rgb_to_lab(rgb)
        lab_colors.append(lab)

    # Interpolate in LAB space
    expanded = []
    if len(base_colors) == 1:
        # If only one color, just repeat it
        return base_colors * n_needed

    # Create evenly spaced indices
    indices = np.linspace(0, len(lab_colors) - 1, n_needed)

    for idx in indices:
        # Find the two surrounding colors
        base_idx = int(np.floor(idx))
        next_idx = min(base_idx + 1, len(lab_colors) - 1)

        # Calculate interpolation weight
        weight = idx - base_idx

        # Interpolate in LAB space
        lab_interpolated = (1 - weight) * lab_colors[base_idx] + weight * lab_colors[
            next_idx
        ]

        # Convert back to RGB and hex
        rgb = lab_to_rgb(lab_interpolated)
        hex_color = rgb_to_hex(rgb)
        expanded.append(hex_color)

    return expanded
