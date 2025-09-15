"""
Plotnine adapter for huez.
"""

import warnings
from typing import Any
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette, get_colormap


class PlotnineAdapter(Adapter):
    """Adapter for plotnine."""

    def __init__(self):
        super().__init__("plotnine")

    def _check_availability(self) -> bool:
        """Check if plotnine is available."""
        try:
            import plotnine as p9
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to plotnine."""
        import plotnine as p9
        import plotnine.options as options

        # Get palettes for consistent theming
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            # Get colormap for heatmaps, using intelligent selection
            from ..color_correction import get_best_colormap_for_library
            sequential_cmap = get_best_colormap_for_library(scheme.palettes.sequential, "plotnine")
            diverging_cmap = get_best_colormap_for_library(scheme.palettes.diverging, "plotnine")
        except Exception as e:
            warnings.warn(f"Failed to get palettes for plotnine: {e}")
            discrete_colors = None
            sequential_cmap = diverging_cmap = None

        # Set default theme
        theme = p9.theme_minimal()

        # Apply font settings
        theme = theme + p9.theme(
            text=p9.element_text(family=scheme.fonts.family, size=scheme.fonts.size),
            title=p9.element_text(family=scheme.fonts.family, size=scheme.fonts.size + 4),
            axis_title=p9.element_text(family=scheme.fonts.family, size=scheme.fonts.size + 2),
            legend_title=p9.element_text(family=scheme.fonts.family, size=scheme.fonts.size + 2)
        )

        # Apply figure size and DPI
        options.figure_size = scheme.figure.size
        options.dpi = scheme.figure.dpi

        # Apply grid style with consistent colors
        # Fix: Use plotnine-compatible color format instead of CSS rgba()
        grid_color = "#808080"  # Gray color compatible with plotnine
        if scheme.style.grid == "x":
            theme = theme + p9.theme(
                panel_grid_major_x=p9.element_line(color=grid_color, alpha=0.8),
                panel_grid_major_y=p9.element_blank()
            )
        elif scheme.style.grid == "y":
            theme = theme + p9.theme(
                panel_grid_major_y=p9.element_line(color=grid_color, alpha=0.8),
                panel_grid_major_x=p9.element_blank()
            )
        elif scheme.style.grid == "both":
            theme = theme + p9.theme(
                panel_grid_major=p9.element_line(color=grid_color, alpha=0.8)
            )
        else:  # none
            theme = theme + p9.theme(panel_grid_major=p9.element_blank())

        # Apply spine style
        if scheme.style.spine_top_right_off:
            theme = theme + p9.theme(
                axis_line_x=p9.element_line(),
                axis_line_y=p9.element_line(),
                panel_border=p9.element_blank()
            )

        # Set background colors
        theme = theme + p9.theme(
            panel_background=p9.element_rect(fill="white"),
            plot_background=p9.element_rect(fill="white")
        )

        # Set as default theme
        p9.theme_set(theme)

        # Set default color palette (if available)
        if discrete_colors:
            # plotnine has no global color settings, but we can try to modify the default palette
            try:
                # Try to set plotnine's default color cycle
                import matplotlib.pyplot as plt
                # Since plotnine is based on matplotlib, this may affect default colors
                plt.rcParams['axes.prop_cycle'] = plt.cycler(color=discrete_colors)

                # Store colors for auxiliary functions
                global _plotnine_colors
                _plotnine_colors = discrete_colors

            except Exception as e:
                warnings.warn(f"Failed to set plotnine default colors: {e}")

        # Store current color scheme for auxiliary functions
        global _current_plotnine_scheme
        _current_plotnine_scheme = scheme

        # Enable auto-coloring functionality
        _enable_auto_coloring()


def get_plotnine_scales(scale_type: str = "auto") -> Any:
    """
    Get plotnine scales for consistent coloring.

    Args:
        scale_type: Type of scales to return
            - "discrete": Only discrete scales (for categorical data)
            - "continuous": Only continuous scales (for numerical data)
            - "auto": Both types (may cause conflicts in some cases)

    Returns:
        List of plotnine scale objects that can be added to plots
    """
    try:
        import plotnine as p9
        from ..core import current_scheme

        scheme_name = current_scheme()
        if scheme_name:
            # Get current config
            from ..core import _current_config
            if _current_config:
                scheme = _current_config.schemes[scheme_name]

                # Get palettes
                discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
                from ..color_correction import get_best_colormap_for_library
                sequential_cmap = get_best_colormap_for_library(scheme.palettes.sequential, "plotnine")
                diverging_cmap = get_best_colormap_for_library(scheme.palettes.diverging, "plotnine")

                # Create scales list based on requested type
                scales = []

                if scale_type in ["discrete", "auto"]:
                    # Add discrete scales for categorical data
                    scales.append(p9.scale_color_manual(values=discrete_colors))
                    scales.append(p9.scale_fill_manual(values=discrete_colors))

                # Comment out continuous scales to avoid conflicts with discrete scales
                # plotnine cannot apply discrete and continuous color/fill scales simultaneously
                # if scale_type in ["continuous", "auto"]:
                #     # Add continuous scales for numerical data
                #     try:
                #         if sequential_cmap:
                #             scales.append(p9.scale_color_cmap(cmap_name=sequential_cmap))
                #             scales.append(p9.scale_fill_cmap(cmap_name=sequential_cmap))
                #     except Exception:
                #         # If continuous scales fail, just skip them
                #         pass

                return scales

    except Exception as e:
        warnings.warn(f"Failed to create plotnine scales: {e}")

    # Fallback - return basic scales based on type
    try:
        import plotnine as p9
        scales = []

        if scale_type in ["discrete", "auto"]:
            scales.extend([p9.scale_color_discrete(), p9.scale_fill_discrete()])

        # Comment out continuous scales to avoid conflicts
        # if scale_type in ["continuous", "auto"]:
        #     try:
        #         scales.extend([p9.scale_color_continuous(), p9.scale_fill_continuous()])
        #     except:
        #         pass

        return scales if scales else [p9.scale_color_discrete(), p9.scale_fill_discrete()]
    except ImportError:
        raise ImportError("plotnine is not installed")


# Global variables to store current colors and scheme
_plotnine_colors = None
_current_plotnine_scheme = None


def get_plotnine_colors(n: int = None):
    """
    Get current plotnine colors for manual use.
    
    Args:
        n: Number of colors to return. If None, returns all available colors.
        
    Returns:
        List of hex color strings
        
    Note:
        This is a convenience function for cases where you need explicit colors.
        Prefer using hz.gg_scales() for automatic color application.
    """
    global _plotnine_colors
    
    if _plotnine_colors is None:
        # Fallback to huez.palette if no scheme is active
        from ..core import palette
        try:
            return palette(n=n, kind="discrete")
        except:
            # Last resort fallback
            colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
            if n is None:
                return colors
            elif n <= len(colors):
                return colors[:n]
            else:
                # Cycle through colors if more needed
                import itertools
                return list(itertools.islice(itertools.cycle(colors), n))
    
    if n is None:
        return _plotnine_colors
    elif n <= len(_plotnine_colors):
        return _plotnine_colors[:n]
    else:
        # Cycle through colors if more needed
        import itertools
        return list(itertools.islice(itertools.cycle(_plotnine_colors), n))


def plotnine_manual_colors(categories: list = None, colors: list = None):
    """
    Create manual color scales for plotnine.
    
    Args:
        categories: List of category names. If None, uses colors in order.
        colors: List of colors. If None, uses current huez colors.
        
    Returns:
        Tuple of (scale_color_manual, scale_fill_manual)
        
    Example:
        color_scale, fill_scale = plotnine_manual_colors(['A', 'B', 'C'])
        (ggplot(df, aes('x', 'y', color='category')) + 
         geom_point() + 
         color_scale + 
         fill_scale)
    """
    import plotnine as p9
    
    if colors is None:
        colors = get_plotnine_colors()
    
    if categories is not None:
        # Create mapping from categories to colors
        color_map = {}
        for i, category in enumerate(categories):
            color_idx = i % len(colors)
            color_map[category] = colors[color_idx]
        
        return (
            p9.scale_color_manual(values=color_map),
            p9.scale_fill_manual(values=color_map)
        )
    else:
        # Use colors in order
        return (
            p9.scale_color_manual(values=colors),
            p9.scale_fill_manual(values=colors)
        )


def plotnine_auto_scales():
    """
    Get automatic scales based on current huez scheme.
    
    Returns:
        List of plotnine scale objects
        
    Example:
        scales = plotnine_auto_scales()
        (ggplot(df, aes('x', 'y', color='category')) + 
         geom_point() + 
         scales[0] + scales[1])  # color and fill scales
    """
    return get_plotnine_scales("discrete")


def gg_color_manual(values: list = None):
    """
    Simplified function to create manual color scale.
    
    Args:
        values: List of colors. If None, uses current huez colors.
        
    Returns:
        plotnine scale_color_manual object
        
    Example:
        (ggplot(df, aes('x', 'y', color='category')) + 
         geom_point() + 
         gg_color_manual())
    """
    import plotnine as p9
    
    if values is None:
        values = get_plotnine_colors()
    
    return p9.scale_color_manual(values=values)


def gg_fill_manual(values: list = None):
    """
    Simplified function to create manual fill scale.
    
    Args:
        values: List of colors. If None, uses current huez colors.
        
    Returns:
        plotnine scale_fill_manual object
        
    Example:
        (ggplot(df, aes('x', 'y', fill='category')) + 
         geom_bar() + 
         gg_fill_manual())
    """
    import plotnine as p9
    
    if values is None:
        values = get_plotnine_colors()
    
    return p9.scale_fill_manual(values=values)


# ============================================================================
# Auto-coloring functionality - Let plotnine use native syntax
# ============================================================================

_auto_coloring_enabled = False
_original_ggplot_save = None
_original_ggplot_draw = None


def _enable_auto_coloring():
    """Enable plotnine auto-coloring functionality"""
    global _auto_coloring_enabled, _original_ggplot_save, _original_ggplot_draw

    if _auto_coloring_enabled:
        return

    try:
        import plotnine as p9

        # Save original methods
        _original_ggplot_save = p9.ggplot.save
        _original_ggplot_draw = p9.ggplot.draw

        # Replace save method
        def auto_save(self, *args, **kwargs):
            # Automatically add huez colors before saving
            enhanced_plot = _auto_add_huez_scales(self)
            return _original_ggplot_save(enhanced_plot, *args, **kwargs)

        # Replace draw method
        def auto_draw(self, *args, **kwargs):
            # Automatically add huez colors before drawing
            enhanced_plot = _auto_add_huez_scales(self)
            return _original_ggplot_draw(enhanced_plot, *args, **kwargs)

        # Apply monkey patch
        p9.ggplot.save = auto_save
        p9.ggplot.draw = auto_draw

        _auto_coloring_enabled = True
        print("🎨 plotnine auto-coloring enabled! Now you can use native syntax directly")

    except Exception as e:
        warnings.warn(f"Failed to enable plotnine auto-coloring: {e}")


def _disable_auto_coloring():
    """Disable plotnine auto-coloring functionality"""
    global _auto_coloring_enabled, _original_ggplot_save, _original_ggplot_draw
    
    if not _auto_coloring_enabled:
        return
    
    try:
        import plotnine as p9
        
        # Restore original methods
        if _original_ggplot_save:
            p9.ggplot.save = _original_ggplot_save
        if _original_ggplot_draw:
            p9.ggplot.draw = _original_ggplot_draw
        
        _auto_coloring_enabled = False
        print("🔧 plotnine auto-coloring disabled")
        
    except Exception as e:
        warnings.warn(f"Failed to disable plotnine auto-coloring: {e}")


def _auto_add_huez_scales(plot):
    """Automatically add huez colors to plotnine plots"""
    try:
        import plotnine as p9

        # Check if manual color scales already exist
        has_color_scale = False
        has_fill_scale = False
        
        for layer in plot.layers + plot.scales:
            if hasattr(layer, 'aesthetics'):
                if 'colour' in layer.aesthetics or 'color' in layer.aesthetics:
                    has_color_scale = True
                if 'fill' in layer.aesthetics:
                    has_fill_scale = True
        
        # Check if color mapping is needed
        needs_color = False
        needs_fill = False

        # Check aes mapping
        if hasattr(plot, 'mapping') and plot.mapping:
            if 'colour' in plot.mapping or 'color' in plot.mapping:
                needs_color = True
            if 'fill' in plot.mapping:
                needs_fill = True

        # Check aes mapping for each layer
        for layer in plot.layers:
            if hasattr(layer, 'mapping') and layer.mapping:
                if 'colour' in layer.mapping or 'color' in layer.mapping:
                    needs_color = True
                if 'fill' in layer.mapping:
                    needs_fill = True

        # If color is needed but not manually set, automatically add it
        enhanced_plot = plot
        
        if needs_color and not has_color_scale:
            colors = get_plotnine_colors()
            if colors:
                enhanced_plot = enhanced_plot + p9.scale_color_manual(values=colors)
        
        if needs_fill and not has_fill_scale:
            colors = get_plotnine_colors()
            if colors:
                enhanced_plot = enhanced_plot + p9.scale_fill_manual(values=colors)
        
        return enhanced_plot
        
    except Exception as e:
        warnings.warn(f"Failed to auto-add huez scales: {e}")
        return plot


def disable_auto_coloring():
    """
    Disable plotnine auto-coloring functionality.

    After calling this function, you need to manually use hz.gg_scales() or other methods to add colors.

    Example:
        from huez.adapters.plotnine import disable_auto_coloring
        disable_auto_coloring()
    """
    _disable_auto_coloring()


def enable_auto_coloring():
    """
    Enable plotnine auto-coloring functionality.

    Once enabled, plotnine will automatically apply huez colors without manually adding hz.gg_scales().

    Example:
        from huez.adapters.plotnine import enable_auto_coloring
        enable_auto_coloring()
    """
    _enable_auto_coloring()


def is_auto_coloring_enabled():
    """
    Check if plotnine auto-coloring is enabled.

    Returns:
        bool: True if auto-coloring is enabled
    """
    return _auto_coloring_enabled


