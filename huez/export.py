"""
Export functionality for huez color schemes.

This module provides functions to export color schemes to various formats
for use in external applications or for sharing.
"""

import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from .config import Scheme
from .registry.palettes import get_palette


def export_all_styles(scheme: Scheme, output_dir: str, formats: Optional[List[str]] = None) -> None:
    """
    Export style files for external use.

    Args:
        scheme: Color scheme to export
        output_dir: Directory to save style files
        formats: List of formats to export. If None, exports all available.
    """
    if formats is None:
        formats = ["json", "yaml", "css", "matplotlib"]

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Export to each requested format
    for fmt in formats:
        if fmt.lower() == "json":
            export_to_json(scheme, output_dir)
        elif fmt.lower() == "yaml":
            export_to_yaml(scheme, output_dir)
        elif fmt.lower() == "css":
            export_to_css(scheme, output_dir)
        elif fmt.lower() == "matplotlib":
            export_matplotlib_style(scheme, output_dir)
        else:
            raise ValueError(f"Unsupported export format: {fmt}")


def export_to_json(scheme: Scheme, output_dir: str) -> None:
    """Export scheme to JSON format."""
    data = _scheme_to_dict(scheme)
    output_path = os.path.join(output_dir, f"{scheme.title.lower().replace(' ', '_')}.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def export_to_yaml(scheme: Scheme, output_dir: str) -> None:
    """Export scheme to YAML format."""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required for YAML export. Install with: pip install PyYAML")

    data = _scheme_to_dict(scheme)
    output_path = os.path.join(output_dir, f"{scheme.title.lower().replace(' ', '_')}.yaml")

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def export_to_css(scheme: Scheme, output_dir: str) -> None:
    """Export scheme to CSS variables format."""
    output_path = os.path.join(output_dir, f"{scheme.title.lower().replace(' ', '_')}.css")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"/* {scheme.title} - Huez Color Scheme */\n")
        f.write(":root {\n")

        # Get color palettes
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete", 10)
            for i, color in enumerate(discrete_colors):
                f.write(f"  --huez-discrete-{i}: {color};\n")
        except Exception:
            pass  # Skip if palette not available

        try:
            sequential_colors = get_palette(scheme.palettes.sequential, "sequential", 10)
            for i, color in enumerate(sequential_colors):
                f.write(f"  --huez-sequential-{i}: {color};\n")
        except Exception:
            pass

        f.write("}\n")


def export_matplotlib_style(scheme: Scheme, output_dir: str) -> None:
    """Export scheme to matplotlib style file."""
    output_path = os.path.join(output_dir, f"{scheme.title.lower().replace(' ', '_')}.mplstyle")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {scheme.title} - Huez Color Scheme for Matplotlib\n\n")

        # Figure settings
        f.write(f"figure.dpi: {scheme.figure.dpi}\n")
        f.write(f"figure.figsize: {scheme.figure.size[0]} {scheme.figure.size[1]}\n\n")

        # Font settings
        f.write(f"font.family: {scheme.fonts.family}\n")
        f.write(f"font.size: {scheme.fonts.size}\n\n")

        # Color cycle (discrete palette)
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete", 10)
            color_cycle = ", ".join([f"'{c}'" for c in discrete_colors])
            f.write(f"axes.prop_cycle: cycler('color', [{color_cycle}])\n")
        except Exception:
            pass

        # Grid settings
        if scheme.style.grid == "both":
            f.write("axes.grid: True\n")
        elif scheme.style.grid == "x":
            f.write("axes.grid.axis: x\n")
            f.write("axes.grid: True\n")
        elif scheme.style.grid == "y":
            f.write("axes.grid.axis: y\n")
            f.write("axes.grid: True\n")
        else:
            f.write("axes.grid: False\n")

        # Legend settings
        f.write(f"legend.loc: {scheme.style.legend_loc}\n")

        # Spine settings
        if scheme.style.spine_top_right_off:
            f.write("axes.spines.top: False\n")
            f.write("axes.spines.right: False\n")


def _scheme_to_dict(scheme: Scheme) -> Dict[str, Any]:
    """Convert scheme to dictionary for serialization."""
    return {
        "title": scheme.title,
        "fonts": {
            "family": scheme.fonts.family,
            "size": scheme.fonts.size
        },
        "palettes": {
            "discrete": scheme.palettes.discrete,
            "sequential": scheme.palettes.sequential,
            "diverging": scheme.palettes.diverging,
            "cyclic": scheme.palettes.cyclic
        },
        "figure": {
            "size": scheme.figure.size,
            "dpi": scheme.figure.dpi
        },
        "style": {
            "grid": scheme.style.grid,
            "legend_loc": scheme.style.legend_loc,
            "spine_top_right_off": scheme.style.spine_top_right_off
        }
    }
