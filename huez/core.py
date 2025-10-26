"""
Core API for Huez - Color Scheme Management and Library Adapters

This module provides the main API for managing color schemes and applying them
across different Python visualization libraries. It handles configuration loading,
scheme switching, and adapter management.
"""

import contextlib
import yaml
from typing import Optional, Dict, Any, List, ContextManager

from .config import Config, validate_config
from .adapters import get_available_adapters, apply_scheme_to_adapters


# Global state
_current_scheme: Optional[str] = None
_current_config: Optional[Config] = None
_scheme_stack: List[str] = []


def _enhance_for_presentation(colors: List[str]) -> List[str]:
    """Enhance colors for presentation (higher contrast, brightness)."""
    import matplotlib.colors as mcolors
    
    enhanced = []
    for color in colors:
        rgb = mcolors.to_rgb(color)
        # Increase saturation and brightness
        hsv = mcolors.rgb_to_hsv(rgb)
        hsv[1] = min(1.0, hsv[1] * 1.2)  # Increase saturation
        hsv[2] = min(1.0, hsv[2] * 1.1)  # Increase brightness
        rgb_enhanced = mcolors.hsv_to_rgb(hsv)
        enhanced.append(mcolors.to_hex(rgb_enhanced))
    
    return enhanced


def _apply_display_mode(scheme, mode: str):
    """
    Apply display mode transformations to a scheme.
    
    Args:
        scheme: Original scheme
        mode: "print" or "presentation"
    
    Returns:
        Modified scheme with mode-appropriate colors
    """
    import copy
    from .registry.palettes import get_palette
    
    # Create a copy to avoid modifying original
    modified_scheme = copy.deepcopy(scheme)
    
    if mode == "print":
        # Print mode: Use colors with varying lightness that remain distinguishable in B&W
        # These colors are carefully chosen to have different grayscale values
        print_safe_colors = [
            '#000000',  # Black (Lightness: 0%)
            '#E64B35',  # Red (Lightness: 40%)
            '#4DBBD5',  # Cyan (Lightness: 70%)
            '#00A087',  # Green (Lightness: 60%)
            '#3C5488',  # Blue (Lightness: 35%)
            '#F39B7F',  # Orange (Lightness: 75%)
            '#8491B4',  # Light blue (Lightness: 65%)
            '#91D1C2',  # Mint (Lightness: 80%)
        ]
        # Store for adapter use
        modified_scheme._display_mode_colors = print_safe_colors
        modified_scheme._display_mode_note = "Colors optimized for B&W printing"
        
    elif mode == "presentation":
        # Presentation mode: Enhance contrast and brightness
        try:
            original_colors = get_palette(scheme.palettes.discrete, "discrete")
            enhanced_colors = _enhance_for_presentation(original_colors)
            modified_scheme._display_mode_colors = enhanced_colors
        except Exception:
            pass
    
    # Store mode info
    modified_scheme._display_mode = mode
    
    return modified_scheme


def load_config(path: Optional[str] = None) -> Config:
    """
    Load configuration from YAML file or use defaults.

    Args:
        path: Path to YAML config file. If None, uses built-in defaults.

    Returns:
        Config object
    """
    global _current_config

    if path is None:
        # Load built-in defaults
        from .data.defaults import get_default_config
        _current_config = get_default_config()
    else:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        _current_config = Config.from_dict(data)

    # Validate configuration
    validate_config(_current_config)

    return _current_config


def use(scheme_name: str,
        config: Optional[Config] = None,
        auto_expand: bool = True,
        smart_cmap: bool = True,
        ensure_accessible: bool = False,
        mode: str = "screen") -> None:
    """
    Apply a color scheme to all available visualization libraries.

    Args:
        scheme_name: Name of the scheme to use
        config: Config object. If None, uses current loaded config.
        auto_expand: Enable intelligent color expansion for unlimited categories
        smart_cmap: Enable automatic colormap detection for heatmaps
        ensure_accessible: Check and warn about colorblind accessibility
        mode: Display mode - "screen" (default), "print" (grayscale-friendly), or "presentation" (high contrast)
        
    Example:
        >>> import huez as hz
        >>> hz.use("nature")  # Screen mode
        >>> hz.use("nature", mode="print")  # Print-friendly colors
        >>> hz.use("nature", mode="presentation")  # High contrast for projectors
    """
    global _current_scheme, _current_config

    if config is not None:
        _current_config = config
        validate_config(_current_config)

    if _current_config is None:
        load_config()

    if scheme_name not in _current_config.schemes:
        available = list(_current_config.schemes.keys())
        raise ValueError(f"Scheme '{scheme_name}' not found. Available: {available}")

    _current_scheme = scheme_name
    scheme = _current_config.schemes[scheme_name]
    
    # Apply display mode transformations
    if mode != "screen":
        scheme = _apply_display_mode(scheme, mode)
    
    # Intelligence features
    if ensure_accessible:
        from .intelligence.accessibility import check_colorblind_safety
        from .registry.palettes import get_palette
        
        try:
            colors = get_palette(scheme.palettes.discrete, "discrete")
            result = check_colorblind_safety(colors, verbose=False)
            
            if not result['safe']:
                import warnings
                warnings.warn(
                    f"\n[Huez Accessibility Warning] Scheme '{scheme_name}' may not be "
                    f"colorblind-safe:\n" + "\n".join(f"  • {w}" for w in result['warnings']) +
                    "\n\nSuggestions:\n" + "\n".join(f"  • {s}" for s in result['suggestions']),
                    UserWarning
                )
        except Exception as e:
            import warnings
            warnings.warn(f"Failed to check accessibility: {e}", UserWarning)
    
    # Store intelligence settings for adapters
    if hasattr(scheme, '_intelligence_settings'):
        scheme._intelligence_settings.update({
            'auto_expand': auto_expand,
            'smart_cmap': smart_cmap,
        })
    else:
        scheme._intelligence_settings = {
            'auto_expand': auto_expand,
            'smart_cmap': smart_cmap,
        }

    # Apply to all available adapters
    adapters = get_available_adapters()
    apply_scheme_to_adapters(scheme, adapters)


def current_scheme() -> Optional[str]:
    """
    Get the name of the currently active scheme.

    Returns:
        Name of current scheme, or None if no scheme is active
    """
    return _current_scheme


@contextlib.contextmanager
def using(scheme_name: str) -> ContextManager[None]:
    """
    Context manager for temporarily using a different scheme.

    Args:
        scheme_name: Name of the scheme to use temporarily
    """
    global _current_scheme, _scheme_stack

    # Save current scheme
    previous_scheme = _current_scheme
    _scheme_stack.append(previous_scheme)

    try:
        use(scheme_name)
        yield
    finally:
        # Restore previous scheme
        restored_scheme = _scheme_stack.pop()
        if restored_scheme is not None:
            use(restored_scheme)
        else:
            _current_scheme = None


def palette(scheme_name: Optional[str] = None,
           kind: str = "discrete",
           n: Optional[int] = None) -> List[str]:
    """
    Get a color palette from the current or specified scheme.

    Args:
        scheme_name: Name of scheme. If None, uses current scheme.
        kind: Type of palette ("discrete", "sequential", "diverging", "cyclic")
        n: Number of colors for discrete palettes. If None, uses default.

    Returns:
        List of hex color strings
    """
    from .registry.palettes import get_palette

    # Check if scheme_name is actually a palette name (not a scheme name)
    from .registry.palettes import validate_palette_name
    if scheme_name and validate_palette_name(scheme_name, kind):
        # It's a direct palette name
        return get_palette(scheme_name, kind, n)

    # It's a scheme name
    if scheme_name is None:
        scheme_name = _current_scheme
        if scheme_name is None:
            raise ValueError("No scheme is currently active. Call huez.use() first.")

    if _current_config is None:
        load_config()

    if scheme_name not in _current_config.schemes:
        raise ValueError(f"Scheme '{scheme_name}' not found. Available schemes: {list(_current_config.schemes.keys())}")

    scheme = _current_config.schemes[scheme_name]
    palette_name = getattr(scheme.palettes, kind)

    return get_palette(palette_name, kind, n)


def cmap(scheme_name: Optional[str] = None,
         kind: str = "sequential") -> str:
    """
    Get a colormap name from the current or specified scheme.

    Args:
        scheme_name: Name of scheme. If None, uses current scheme.
        kind: Type of colormap ("sequential", "diverging", "cyclic")

    Returns:
        Colormap name string
    """
    from .registry.palettes import get_colormap

    if scheme_name is None:
        scheme_name = _current_scheme
        if scheme_name is None:
            raise ValueError("No scheme is currently active. Call huez.use() first.")

    if _current_config is None:
        load_config()

    scheme = _current_config.schemes[scheme_name]
    cmap_name = getattr(scheme.palettes, kind)

    return get_colormap(cmap_name, kind)


def gg_scales() -> Any:
    """
    Get plotnine scales for consistent coloring.

    Returns:
        plotnine scale objects that can be added to plots
    """
    try:
        from .adapters.plotnine import get_plotnine_scales
        return get_plotnine_scales()
    except ImportError:
        raise ImportError("plotnine is not installed. Install with: pip install plotnine")


def export_styles(output_dir: str,
                 scheme: Optional[str] = None,
                 formats: Optional[List[str]] = None) -> None:
    """
    Export style files for external use.

    Args:
        output_dir: Directory to save style files
        scheme: Scheme name. If None, uses current scheme.
        formats: List of formats to export. If None, exports all available.
    """
    from .export import export_all_styles

    if scheme is None:
        scheme = _current_scheme
        if scheme is None:
            raise ValueError("No scheme is currently active. Call huez.use() first.")

    if _current_config is None:
        load_config()

    scheme_config = _current_config.schemes[scheme]
    export_all_styles(scheme_config, output_dir, formats)


def preview_gallery(output_dir: str,
                   scheme: Optional[str] = None) -> None:
    """
    Generate a preview gallery showing the scheme.

    Args:
        output_dir: Directory to save preview files
        scheme: Scheme name. If None, uses current scheme.
    """
    from .preview import generate_gallery

    if scheme is None:
        scheme = _current_scheme
        if scheme is None:
            raise ValueError("No scheme is currently active. Call huez.use() first.")

    if _current_config is None:
        load_config()

    scheme_config = _current_config.schemes[scheme]
    generate_gallery(scheme_config, output_dir)


def check_palette(scheme: Optional[str] = None,
                 kinds: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Check palette quality (colorblind safety, contrast, etc.).

    Args:
        scheme: Scheme name. If None, uses current scheme.
        kinds: Types of palettes to check. If None, checks all.

    Returns:
        Dictionary with quality check results
    """
    from .quality.checks import check_palette_quality

    if scheme is None:
        scheme = _current_scheme
        if scheme is None:
            raise ValueError("No scheme is currently active. Call huez.use() first.")

    if _current_config is None:
        load_config()

    scheme_config = _current_config.schemes[scheme]
    return check_palette_quality(scheme_config, kinds)


def lint_figure(file_path: str,
               report_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Lint a figure file for visualization best practices.

    Args:
        file_path: Path to the figure file
        report_path: Optional path to save detailed report

    Returns:
        Dictionary with linting results
    """
    from .quality.lint import lint_figure_file

    return lint_figure_file(file_path, report_path)


# ============================================================================
# Convenience Functions for Automatic Color Adaptation
# ============================================================================

def auto_colors(library: str = "auto", n: int = None) -> List[str]:
    """
    Get colors automatically adapted for a specific library.
    
    Args:
        library: Target library ("auto", "matplotlib", "seaborn", "plotly", "altair", "plotnine")
        n: Number of colors to return
        
    Returns:
        List of hex color strings
        
    Example:
        colors = hz.auto_colors("plotly", n=5)
    """
    if library == "auto":
        # Try to detect which library is being used
        library = _detect_active_library()
    
    if library in ["matplotlib", "seaborn"]:
        # These libraries handle colors automatically through rcParams
        return palette(n=n, kind="discrete")
    elif library == "plotly":
        try:
            from .adapters.plotly import get_plotly_colors
            return get_plotly_colors(n)
        except ImportError:
            return palette(n=n, kind="discrete")
    elif library == "altair":
        try:
            from .adapters.altair import get_altair_colors
            return get_altair_colors(n)
        except ImportError:
            return palette(n=n, kind="discrete")
    else:
        return palette(n=n, kind="discrete")


def _detect_active_library() -> str:
    """
    Try to detect which visualization library is currently being used.
    
    Returns:
        Library name or "matplotlib" as default
    """
    import sys
    
    # Check if libraries are imported in the current session
    if 'plotly' in sys.modules:
        return "plotly"
    elif 'altair' in sys.modules:
        return "altair"
    elif 'seaborn' in sys.modules:
        return "seaborn"
    elif 'plotnine' in sys.modules:
        return "plotnine"
    else:
        return "matplotlib"  # Default fallback


def quick_setup(scheme: str = "scheme-1") -> None:
    """
    Quick setup for immediate use - loads config and applies scheme.
    
    Args:
        scheme: Scheme name to apply
        
    Example:
        import huez as hz
        hz.quick_setup("scheme-1")  # Ready to use!
    """
    load_config()
    use(scheme)
    print(f"✅ Huez activated color scheme: {scheme}")
    print(f"📊 Supported libraries: {', '.join(_get_available_library_names())}")


def _get_available_library_names() -> List[str]:
    """Get names of available visualization libraries."""
    adapters = get_available_adapters()
    return [adapter.get_name() for adapter in adapters]


def colors(n: int = None, library: str = "auto") -> List[str]:
    """
    Simplified function to get colors - no need to specify 'kind' or 'scheme_name'.
    
    Args:
        n: Number of colors
        library: Target library for optimization
        
    Returns:
        List of hex color strings
        
    Example:
        # Instead of: colors = hz.palette(n=3, kind="discrete")
        colors = hz.colors(3)  # Much simpler!
    """
    return auto_colors(library=library, n=n)


def apply_to_figure(fig, library: str = "auto"):
    """
    Apply huez colors to an existing figure object.
    
    Args:
        fig: Figure object (matplotlib, plotly, etc.)
        library: Library type ("auto", "matplotlib", "plotly", "altair")
        
    Returns:
        Figure with colors applied
        
    Example:
        fig = plt.figure()
        # ... create plot ...
        fig = hz.apply_to_figure(fig, "matplotlib")
    """
    if library == "auto":
        library = _detect_active_library()
    
    if library == "plotly":
        try:
            from .adapters.plotly import plotly_auto_colors
            return plotly_auto_colors(fig)
        except ImportError:
            pass
    elif library == "altair":
        try:
            from .adapters.altair import altair_auto_color
            return altair_auto_color(fig)
        except ImportError:
            pass
    
    # For matplotlib/seaborn, colors are already applied via rcParams
    return fig


def status() -> Dict[str, Any]:
    """
    Get current huez status and available libraries.
    
    Returns:
        Dictionary with status information
        
    Example:
        print(hz.status())
    """
    from .adapters.base import get_adapter_status
    
    return {
        "current_scheme": current_scheme(),
        "available_libraries": get_adapter_status(),
        "config_loaded": _current_config is not None,
        "total_schemes": len(_current_config.schemes) if _current_config else 0
    }


def help_usage() -> None:
    """
    Print helpful usage information.
    """
    print("""
🎨 Huez - Unified Python visualization color scheme

🚀 Quick start:
    import huez as hz
    hz.quick_setup("scheme-1")  # One-click setup

📊 Basic usage:
    # Traditional way (still supported)
    colors = hz.palette(n=3, kind="discrete")

    # New simplified way (recommended)
    colors = hz.colors(3)  # Much simpler!

🎯 Auto-adaptation:
    # Matplotlib/Seaborn - Fully automatic
    plt.plot(x, y)  # Automatically uses huez colors

    # Plotly/Altair - Also automatic!
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))  # Automatic coloring

📈 Check status:
    hz.status()  # View current status

💡 More info: https://github.com/huez/huez
    """)


# Aliases for backward compatibility and convenience
get_colors = colors  # Alias
setup = quick_setup  # Alias


# ============================================================================
# Intelligence Features
# ============================================================================

def check_accessibility(colors: Optional[List[str]] = None, 
                        scheme_name: Optional[str] = None,
                        verbose: bool = True) -> Dict[str, Any]:
    """
    Check colorblind accessibility of a color palette.
    
    Args:
        colors: List of hex colors to check. If None, uses current scheme.
        scheme_name: Name of scheme to check. If None, uses current scheme.
        verbose: Print detailed report
        
    Returns:
        Dictionary with safety analysis
        
    Example:
        >>> import huez as hz
        >>> hz.use("npg")
        >>> result = hz.check_accessibility()
        >>> if not result['safe']:
        ...     print("Warning: Not colorblind-safe!")
    """
    from .intelligence.accessibility import check_colorblind_safety
    from .registry.palettes import get_palette
    
    # Determine which colors to check
    if colors is None:
        if scheme_name is None:
            scheme_name = _current_scheme
            if scheme_name is None:
                raise ValueError("No scheme is active. Call hz.use() first or provide colors/scheme_name.")
        
        if _current_config is None:
            load_config()
        
        scheme = _current_config.schemes[scheme_name]
        colors = get_palette(scheme.palettes.discrete, "discrete")
    
    return check_colorblind_safety(colors, verbose=verbose)


def expand_colors(colors: List[str], n_needed: int) -> List[str]:
    """
    Intelligently expand a color palette using LAB space interpolation.
    
    Args:
        colors: Base color palette (hex format)
        n_needed: Number of colors needed
        
    Returns:
        Expanded color list
        
    Example:
        >>> import huez as hz
        >>> base = ['#E64B35', '#4DBBD5', '#00A087']
        >>> expanded = hz.expand_colors(base, 10)
        >>> len(expanded)
        10
    """
    from .intelligence.color_expansion import intelligent_color_expansion
    return intelligent_color_expansion(colors, n_needed)


def detect_colormap(data, verbose: bool = True) -> str:
    """
    Automatically detect appropriate colormap type for data.
    
    Args:
        data: Numeric data (numpy array or list)
        verbose: Print detection reasoning
        
    Returns:
        "sequential" or "diverging"
        
    Example:
        >>> import numpy as np
        >>> import huez as hz
        >>> corr_data = np.random.randn(10, 10)
        >>> cmap_type = hz.detect_colormap(corr_data)
        >>> print(cmap_type)  # "diverging" for symmetric data
    """
    from .intelligence.colormap_detection import detect_colormap_type
    return detect_colormap_type(data, verbose=verbose)


def smart_cmap(data, scheme_name: Optional[str] = None) -> str:
    """
    Get appropriate colormap name based on data analysis.
    
    Args:
        data: Numeric data to analyze
        scheme_name: Scheme to use. If None, uses current scheme.
        
    Returns:
        Colormap name
        
    Example:
        >>> import numpy as np
        >>> import seaborn as sns
        >>> import huez as hz
        >>> 
        >>> hz.use("nature")
        >>> data = np.random.randn(10, 10)  # Symmetric data
        >>> cmap_name = hz.smart_cmap(data)
        >>> sns.heatmap(data, cmap=cmap_name)  # Automatically uses diverging
    """
    from .intelligence.colormap_detection import detect_colormap_type
    
    if scheme_name is None:
        scheme_name = _current_scheme
        if scheme_name is None:
            raise ValueError("No scheme is active. Call hz.use() first.")
    
    if _current_config is None:
        load_config()
    
    # Detect data type
    cmap_type = detect_colormap_type(data, verbose=False)
    
    # Get appropriate colormap from scheme
    scheme = _current_config.schemes[scheme_name]
    from .registry.palettes import get_colormap
    
    if cmap_type == "diverging":
        return get_colormap(scheme.palettes.diverging, "diverging")
    else:
        return get_colormap(scheme.palettes.sequential, "sequential")


# ============================================================================
# Preview and Utility Functions
# ============================================================================

def preview(scheme_name: Optional[str] = None, mode: str = "screen") -> None:
    """
    Display a quick preview of a color scheme.
    
    Args:
        scheme_name: Name of scheme to preview. If None, shows current scheme.
        mode: Display mode - "screen", "print", or "presentation"
        
    Example:
        >>> import huez as hz
        >>> hz.preview("nature")  # Preview Nature scheme
        >>> hz.preview("nature", mode="print")  # Preview in print mode
        >>> hz.preview()  # Preview current scheme
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from .registry.palettes import get_palette
    
    # Determine which scheme to preview
    if scheme_name is None:
        scheme_name = _current_scheme
        if scheme_name is None:
            raise ValueError("No scheme is active. Provide scheme_name or call hz.use() first.")
    
    if _current_config is None:
        load_config()
    
    if scheme_name not in _current_config.schemes:
        available = list(_current_config.schemes.keys())
        raise ValueError(f"Scheme '{scheme_name}' not found. Available: {available}")
    
    scheme = _current_config.schemes[scheme_name]
    
    # Apply mode transformation if needed
    if mode != "screen":
        scheme = _apply_display_mode(scheme, mode)
    
    # Get colors
    try:
        if hasattr(scheme, '_display_mode_colors'):
            colors = scheme._display_mode_colors
        else:
            colors = get_palette(scheme.palettes.discrete, "discrete", n=8)
    except Exception as e:
        print(f"Error loading palette: {e}")
        return
    
    # Create preview figure
    fig = plt.figure(figsize=(10, 6))
    
    # Title
    mode_text = f" ({mode} mode)" if mode != "screen" else ""
    fig.suptitle(f'{scheme.title}{mode_text}', fontsize=16, fontweight='bold')
    
    # Color swatches
    ax1 = plt.subplot(2, 2, (1, 2))
    ax1.set_title('Discrete Colors', fontsize=12, pad=10)
    
    for i, color in enumerate(colors):
        rect = plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black', linewidth=1)
        ax1.add_patch(rect)
        ax1.text(i + 0.5, -0.3, color, ha='center', va='top', fontsize=8, rotation=45)
    
    ax1.set_xlim(0, len(colors))
    ax1.set_ylim(-0.5, 1.2)
    ax1.axis('off')
    
    # Sample line plot
    ax2 = plt.subplot(2, 2, 3)
    ax2.set_title('Line Plot Example', fontsize=10)
    x = np.linspace(0, 10, 100)
    for i in range(min(5, len(colors))):
        y = np.sin(x + i * np.pi/4) + i
        ax2.plot(x, y, color=colors[i], linewidth=2, label=f'Series {i+1}')
    ax2.legend(fontsize=8, loc='best')
    ax2.grid(True, alpha=0.3)
    
    # Sample bar chart
    ax3 = plt.subplot(2, 2, 4)
    ax3.set_title('Bar Chart Example', fontsize=10)
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [3, 7, 2, 5, 8]
    ax3.bar(categories, values, color=colors[:len(categories)])
    ax3.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\nScheme: {scheme.title}")
    print(f"Mode: {mode}")
    print(f"Discrete palette: {scheme.palettes.discrete}")
    print(f"Colors: {len(colors)}")
    if mode == "print":
        print("Note: Print mode uses grayscale-friendly colors")
    elif mode == "presentation":
        print("Note: Presentation mode uses enhanced contrast")


def list_schemes() -> List[str]:
    """
    List all available color schemes.
    
    Returns:
        List of scheme names
        
    Example:
        >>> import huez as hz
        >>> schemes = hz.list_schemes()
        >>> print(schemes)
    """
    if _current_config is None:
        load_config()
    
    return list(_current_config.schemes.keys())
