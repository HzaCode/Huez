"""
Matplotlib adapter for huez.
"""

import warnings
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette, get_colormap


class MatplotlibAdapter(Adapter):
    """Adapter for matplotlib."""

    def __init__(self):
        super().__init__("matplotlib")

    def _check_availability(self) -> bool:
        """Check if matplotlib is available."""
        import importlib.util
        return importlib.util.find_spec("matplotlib") is not None

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to matplotlib."""
        import matplotlib.pyplot as plt
        import matplotlib as mpl

        # Get the discrete palette (check for display mode override)
        try:
            if hasattr(scheme, '_display_mode_colors'):
                discrete_colors = scheme._display_mode_colors
            else:
                discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            mpl.rcParams['axes.prop_cycle'] = plt.cycler(color=discrete_colors)
        except Exception as e:
            warnings.warn(f"Failed to set discrete palette: {e}")

        # Set font properties
        mpl.rcParams['font.family'] = scheme.fonts.family
        mpl.rcParams['font.size'] = scheme.fonts.size

        # Set figure properties
        mpl.rcParams['figure.figsize'] = scheme.figure.size
        mpl.rcParams['figure.dpi'] = scheme.figure.dpi
        mpl.rcParams['savefig.dpi'] = scheme.figure.dpi

        # Set PDF font embedding
        mpl.rcParams['pdf.fonttype'] = 42  # Use TrueType fonts

        # Enable constrained layout
        plt.rcParams['figure.constrained_layout.use'] = True

        # Set grid style
        if scheme.style.grid == "x":
            plt.rcParams['axes.grid.axis'] = 'x'
            plt.rcParams['axes.grid'] = True
        elif scheme.style.grid == "y":
            plt.rcParams['axes.grid.axis'] = 'y'
            plt.rcParams['axes.grid'] = True
        elif scheme.style.grid == "both":
            plt.rcParams['axes.grid'] = True
        else:  # none
            plt.rcParams['axes.grid'] = False

        # Set spine style
        if scheme.style.spine_top_right_off:
            plt.rcParams['axes.spines.top'] = False
            plt.rcParams['axes.spines.right'] = False

        # Set legend location
        plt.rcParams['legend.loc'] = scheme.style.legend_loc

        # Apply colormaps
        try:
            # This is a bit tricky since matplotlib doesn't have a single "default colormap"
            # We'll set the image colormap
            sequential_cmap = get_colormap(scheme.palettes.sequential, "sequential")
            if sequential_cmap:
                plt.rcParams['image.cmap'] = sequential_cmap
        except Exception as e:
            warnings.warn(f"Failed to set colormap: {e}")


def export_mplstyle(scheme: Scheme, output_path: str) -> None:
    """
    Export matplotlib style file.

    Args:
        scheme: Color scheme
        output_path: Path to save .mplstyle file
    """
    import matplotlib.pyplot as plt

    # Apply scheme temporarily to get rcParams
    original_params = dict(plt.rcParams)

    try:
        adapter = MatplotlibAdapter()
        adapter.apply_scheme(scheme)

        # Write style file
        style_content = []
        for key, value in plt.rcParams.items():
            if key.startswith(('axes.', 'figure.', 'font.', 'grid.', 'legend.', 'pdf.', 'savefig.')):
                if isinstance(value, str):
                    style_content.append(f"{key}: {value}")
                elif isinstance(value, (int, float)):
                    style_content.append(f"{key}: {value}")
                elif isinstance(value, bool):
                    style_content.append(f"{key}: {value}")
                elif isinstance(value, (list, tuple)):
                    style_content.append(f"{key}: {', '.join(map(str, value))}")

        with open(output_path, 'w') as f:
            f.write("# huez matplotlib style\n")
            f.write("# Generated automatically\n\n")
            f.write('\n'.join(style_content))

    finally:
        # Restore original params
        plt.rcParams.update(original_params)


