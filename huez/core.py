"""
Core API for huez - scheme management and library adapters.
"""

import os
import contextlib
import yaml
from typing import Optional, Dict, Any, List, Union, ContextManager
from pathlib import Path

from .config import Config, validate_config
from .adapters import get_available_adapters, apply_scheme_to_adapters


# Global state
_current_scheme: Optional[str] = None
_current_config: Optional[Config] = None
_scheme_stack: List[str] = []


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


def use(scheme_name: str, config: Optional[Config] = None) -> None:
    """
    Apply a color scheme to all available visualization libraries.

    Args:
        scheme_name: Name of the scheme to use
        config: Config object. If None, uses current loaded config.
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
