"""
Intelligent Colormap Type Detection

This module provides functions for automatically detecting the most appropriate
colormap type (sequential, diverging, or cyclic) based on data characteristics.
"""

import numpy as np
from typing import Union, Optional


def detect_colormap_type(
    data: Union[np.ndarray, list],
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    verbose: bool = True
) -> str:
    """
    Automatically detect the most appropriate colormap type for data.
    
    This function analyzes data characteristics to recommend:
    - "sequential": Data with a natural ordering from low to high (e.g., 0-100)
    - "diverging": Data with a meaningful center point (e.g., correlation -1 to 1)
    - "cyclic": Data that wraps around (e.g., angles 0-360)
    
    Args:
        data: Input data as numpy array or list
        vmin: Optional minimum value for range analysis
        vmax: Optional maximum value for range analysis
        verbose: If True, print detection reasoning
        
    Returns:
        String indicating colormap type: "sequential", "diverging", or "cyclic"
        
    Examples:
        >>> import numpy as np
        >>> # Correlation matrix (-1 to 1)
        >>> data = np.array([[1.0, 0.8, -0.6], [0.8, 1.0, -0.4], [-0.6, -0.4, 1.0]])
        >>> detect_colormap_type(data)
        'diverging'
        
        >>> # Positive-only data
        >>> data = np.random.rand(10, 10) * 100
        >>> detect_colormap_type(data)
        'sequential'
    """
    # Convert to numpy array if needed
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    
    # Flatten data
    data_flat = data.flatten()
    
    # Remove NaN and infinite values
    data_clean = data_flat[np.isfinite(data_flat)]
    
    if len(data_clean) == 0:
        if verbose:
            print("⚠️  No valid data points found. Defaulting to sequential colormap.")
        return "sequential"
    
    # Calculate statistics
    data_min = vmin if vmin is not None else np.min(data_clean)
    data_max = vmax if vmax is not None else np.max(data_clean)
    data_mean = np.mean(data_clean)
    data_median = np.median(data_clean)
    data_range = data_max - data_min
    
    if data_range == 0:
        if verbose:
            print("⚠️  Data has zero range. Defaulting to sequential colormap.")
        return "sequential"
    
    # Detection logic
    
    # 1. Check for cyclic data (e.g., angles)
    # Cyclic if data appears to wrap around (e.g., 0-360 or 0-2π)
    if data_min >= 0 and data_max <= 360 and data_range > 300:
        if verbose:
            print(f"🔵 Detected cyclic data (range: {data_min:.1f} to {data_max:.1f})")
            print("   → Recommended: cyclic colormap")
        return "cyclic"
    
    if data_min >= 0 and data_max <= 2 * np.pi and data_range > 5.5:
        if verbose:
            print(f"🔵 Detected cyclic data in radians (range: {data_min:.2f} to {data_max:.2f})")
            print("   → Recommended: cyclic colormap")
        return "cyclic"
    
    # 2. Check for diverging data
    # Diverging if:
    # - Data spans across zero with significant values on both sides
    # - Data appears to be centered (like correlation matrix)
    
    # Check if data crosses zero
    crosses_zero = data_min < 0 < data_max
    
    if crosses_zero:
        # Calculate how centered the data is around zero
        abs_min = abs(data_min)
        abs_max = abs(data_max)
        symmetry_ratio = min(abs_min, abs_max) / max(abs_min, abs_max)
        
        # If reasonably symmetric around zero (within 3:1 ratio)
        if symmetry_ratio > 0.3:
            if verbose:
                print("🔴🔵 Detected diverging data:")
                print(f"   Range: {data_min:.2f} to {data_max:.2f}")
                print(f"   Mean: {data_mean:.2f}, Median: {data_median:.2f}")
                print(f"   Symmetry ratio: {symmetry_ratio:.2f}")
                print("   → Recommended: diverging colormap (centered at 0)")
            return "diverging"
    
    # Check if data looks like it should be centered (e.g., -1 to 1 correlation)
    if data_min >= -1.1 and data_max <= 1.1 and crosses_zero:
        if verbose:
            print(f"🔴🔵 Detected correlation-like data (range: {data_min:.2f} to {data_max:.2f})")
            print("   → Recommended: diverging colormap")
        return "diverging"
    
    # 3. Check for data that should be centered even if not symmetric
    # E.g., change data, anomalies, deviations from mean
    center_ratio = abs(data_mean) / data_range if data_range > 0 else 0
    
    # If mean is near the center of the range (within 20-80%)
    if crosses_zero and 0.2 < center_ratio < 0.8:
        if verbose:
            print("🔴🔵 Detected data with meaningful center:")
            print(f"   Range: {data_min:.2f} to {data_max:.2f}")
            print(f"   Mean at {center_ratio*100:.1f}% of range")
            print("   → Recommended: diverging colormap")
        return "diverging"
    
    # 4. Default to sequential
    # Sequential for data with natural low-to-high ordering
    if verbose:
        print(f"🟢 Detected sequential data (range: {data_min:.2f} to {data_max:.2f})")
        print("   → Recommended: sequential colormap")
    
    return "sequential"


def suggest_colormap(
    data: Union[np.ndarray, list],
    library: str = "matplotlib",
    verbose: bool = True
) -> str:
    """
    Suggest a specific colormap name based on data type and library.
    
    Args:
        data: Input data to analyze
        library: Visualization library ("matplotlib", "seaborn", "plotly")
        verbose: If True, print suggestion reasoning
        
    Returns:
        String with suggested colormap name
        
    Examples:
        >>> data = np.random.randn(10, 10)
        >>> suggest_colormap(data, library="matplotlib")
        'coolwarm'
    """
    cmap_type = detect_colormap_type(data, verbose=False)
    
    # Colormap recommendations by library
    recommendations = {
        "matplotlib": {
            "sequential": "viridis",
            "diverging": "coolwarm",
            "cyclic": "twilight"
        },
        "seaborn": {
            "sequential": "viridis",
            "diverging": "coolwarm",
            "cyclic": "twilight"
        },
        "plotly": {
            "sequential": "Viridis",
            "diverging": "RdBu",
            "cyclic": "Phase"
        }
    }
    
    library = library.lower()
    if library not in recommendations:
        library = "matplotlib"
    
    suggested = recommendations[library][cmap_type]
    
    if verbose:
        print(f"📊 Data type: {cmap_type}")
        print(f"🎨 Suggested colormap for {library}: '{suggested}'")
    
    return suggested
