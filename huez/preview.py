"""
Preview gallery generation for huez schemes.
"""

import os

from .config import Scheme
from .registry.palettes import get_palette


def generate_gallery(scheme: Scheme, output_dir: str) -> None:
    """
    Generate a preview gallery showing the scheme.

    Args:
        scheme: Color scheme to preview
        output_dir: Directory to save gallery files
    """
    os.makedirs(output_dir, exist_ok=True)

    # Generate HTML gallery
    _generate_html_gallery(scheme, output_dir)

    # Generate sample plots
    _generate_sample_plots(scheme, output_dir)

    # Generate colorblind simulation
    _generate_colorblind_preview(scheme, output_dir)


def _generate_html_gallery(scheme: Scheme, output_dir: str) -> None:
    """Generate HTML gallery page."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{scheme.title} - huez Preview</title>
    <style>
        body {{
            font-family: {scheme.fonts.family}, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .scheme-info {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .palettes {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .palette-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .color-swatches {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin: 10px 0;
        }}
        .color-swatch {{
            width: 30px;
            height: 30px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
        .gradient-bar {{
            width: 100%;
            height: 20px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        .plots {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }}
        .plot-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .plot-card img {{
            width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        .colorblind-section {{
            margin-top: 30px;
        }}
        .colorblind-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        .colorblind-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .colorblind-item img {{
            width: 100%;
            height: auto;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{scheme.title}</h1>
        <p>huez color scheme preview</p>
    </div>

    <div class="scheme-info">
        <h2>Scheme Information</h2>
        <p><strong>Fonts:</strong> {scheme.fonts.family}, size {scheme.fonts.size}</p>
        <p><strong>Figure size:</strong> {scheme.figure.size[0]}" × {scheme.figure.size[1]}" inches</p>
        <p><strong>DPI:</strong> {scheme.figure.dpi}</p>
        <p><strong>Grid:</strong> {scheme.style.grid}</p>
        <p><strong>Legend:</strong> {scheme.style.legend_loc}</p>
        <p><strong>Top/right spines:</strong> {'Hidden' if scheme.style.spine_top_right_off else 'Shown'}</p>
    </div>

    <h2>Color Palettes</h2>
    <div class="palettes">
"""

    # Add palette sections
    palette_configs = [
        ("discrete", "Discrete Colors", True),
        ("sequential", "Sequential Colormap", False),
        ("diverging", "Diverging Colormap", False),
        ("cyclic", "Cyclic Colormap", False),
    ]

    for palette_type, title, is_discrete in palette_configs:
        palette_name = getattr(scheme.palettes, palette_type)

        html_content += f"""
        <div class="palette-card">
            <h3>{title}</h3>
            <p><strong>Palette:</strong> {palette_name}</p>
"""

        if is_discrete:
            try:
                colors = get_palette(palette_name, palette_type, n=8)
                html_content += '<div class="color-swatches">'
                for color in colors:
                    html_content += f'<div class="color-swatch" style="background-color: {color};"></div>'
                html_content += "</div>"
                html_content += f"<p>{len(colors)} colors</p>"
            except Exception as e:
                html_content += f"<p>Error loading palette: {e}</p>"
        else:
            # For colormaps, we'll show the name and let the plots demonstrate
            html_content += '<div class="gradient-bar" style="background: linear-gradient(to right, blue, red);"></div>'
            html_content += "<p>Colormap preview in plots below</p>"

        html_content += "</div>"

    html_content += """
    </div>

    <h2>Sample Plots</h2>
    <div class="plots">
        <div class="plot-card">
            <h3>Scatter Plot</h3>
            <img src="scatter_plot.png" alt="Scatter plot example">
        </div>
        <div class="plot-card">
            <h3>Bar Chart</h3>
            <img src="bar_chart.png" alt="Bar chart example">
        </div>
        <div class="plot-card">
            <h3>Heatmap</h3>
            <img src="heatmap.png" alt="Heatmap example">
        </div>
        <div class="plot-card">
            <h3>Line Plot</h3>
            <img src="line_plot.png" alt="Line plot example">
        </div>
    </div>

    <div class="colorblind-section">
        <h2>Colorblind Safety</h2>
        <div class="colorblind-grid">
            <div class="colorblind-item">
                <h4>Normal Vision</h4>
                <img src="colorblind_normal.png" alt="Normal vision">
            </div>
            <div class="colorblind-item">
                <h4>Deuteranopia</h4>
                <img src="colorblind_deuteranopia.png" alt="Deuteranopia simulation">
            </div>
            <div class="colorblind-item">
                <h4>Protanopia</h4>
                <img src="colorblind_protanopia.png" alt="Protanopia simulation">
            </div>
            <div class="colorblind-item">
                <h4>Tritanopia</h4>
                <img src="colorblind_tritanopia.png" alt="Tritanopia simulation">
            </div>
        </div>
    </div>

    <div style="text-align: center; margin-top: 40px; color: #666;">
        <p>Generated by <strong>huez</strong> - Your all-in-one color solution in Python</p>
    </div>
</body>
</html>"""

    html_path = os.path.join(output_dir, "gallery.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def _generate_sample_plots(scheme: Scheme, output_dir: str) -> None:
    """Generate sample plots demonstrating the scheme."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        # Apply the scheme
        from .adapters.mpl import MatplotlibAdapter

        adapter = MatplotlibAdapter()
        adapter.apply_scheme(scheme)

        # Generate scatter plot
        plt.figure(figsize=scheme.figure.size)
        np.random.seed(42)
        x = np.random.randn(100)
        y = np.random.randn(100)
        colors = np.random.randint(0, 8, 100)

        plt.scatter(x, y, c=colors, alpha=0.7)
        plt.xlabel("X Variable")
        plt.ylabel("Y Variable")
        plt.title("Scatter Plot Example")
        plt.savefig(
            os.path.join(output_dir, "scatter_plot.png"),
            dpi=scheme.figure.dpi,
            bbox_inches="tight",
        )
        plt.close()

        # Generate bar chart
        plt.figure(figsize=scheme.figure.size)
        categories = ["A", "B", "C", "D", "E"]
        values = np.random.randint(10, 50, 5)

        plt.bar(categories, values)
        plt.xlabel("Categories")
        plt.ylabel("Values")
        plt.title("Bar Chart Example")
        plt.savefig(
            os.path.join(output_dir, "bar_chart.png"),
            dpi=scheme.figure.dpi,
            bbox_inches="tight",
        )
        plt.close()

        # Generate heatmap
        plt.figure(figsize=scheme.figure.size)
        data = np.random.randn(10, 10)

        plt.imshow(data, cmap=getattr(scheme.palettes, "sequential"))
        plt.colorbar()
        plt.title("Heatmap Example")
        plt.savefig(
            os.path.join(output_dir, "heatmap.png"),
            dpi=scheme.figure.dpi,
            bbox_inches="tight",
        )
        plt.close()

        # Generate line plot
        plt.figure(figsize=scheme.figure.size)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.sin(x + np.pi / 4)

        plt.plot(x, y1, label="sin(x)")
        plt.plot(x, y2, label="cos(x)")
        plt.plot(x, y3, label="sin(x+π/4)")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Line Plot Example")
        plt.legend()
        plt.savefig(
            os.path.join(output_dir, "line_plot.png"),
            dpi=scheme.figure.dpi,
            bbox_inches="tight",
        )
        plt.close()

    except ImportError:
        print("Warning: matplotlib not available for sample plot generation")
    except Exception as e:
        print(f"Warning: Failed to generate sample plots: {e}")


def _generate_colorblind_preview(scheme: Scheme, output_dir: str) -> None:
    """Generate colorblind simulation previews."""
    try:
        import matplotlib.pyplot as plt

        # Apply the scheme
        from .adapters.mpl import MatplotlibAdapter
        from .quality.checks import (
            _convert_to_grayscale,
            _hex_to_rgb,
            _rgb_to_hex,
            _simulate_colorblindness,
        )

        adapter = MatplotlibAdapter()
        adapter.apply_scheme(scheme)

        # Get discrete colors
        colors = get_palette(scheme.palettes.discrete, "discrete", n=8)
        rgb_colors = [_hex_to_rgb(color) for color in colors]

        # Create a simple test pattern
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.flatten()

        # Normal vision
        axes[0].bar(range(len(colors)), [1] * len(colors), color=colors)
        axes[0].set_title("Normal Vision")
        axes[0].set_ylim(0, 1.2)

        # Colorblind simulations
        cb_types = ["deuteranopia", "protanopia", "tritanopia"]
        titles = ["Deuteranopia", "Protanopia", "Tritanopia"]

        for i, (cb_type, title) in enumerate(zip(cb_types, titles)):
            try:
                cb_colors_rgb = _simulate_colorblindness(rgb_colors, cb_type)
                cb_colors_hex = [_rgb_to_hex(rgb) for rgb in cb_colors_rgb]

                axes[i + 1].bar(
                    range(len(cb_colors_hex)),
                    [1] * len(cb_colors_hex),
                    color=cb_colors_hex,
                )
                axes[i + 1].set_title(title)
                axes[i + 1].set_ylim(0, 1.2)
            except Exception as e:
                axes[i + 1].text(
                    0.5,
                    0.5,
                    f"Error:\n{str(e)}",
                    ha="center",
                    va="center",
                    transform=axes[i + 1].transAxes,
                )
                axes[i + 1].set_title(title)

        # Grayscale
        try:
            gray_colors_rgb = _convert_to_grayscale(rgb_colors)
            gray_colors_hex = [_rgb_to_hex(rgb) for rgb in gray_colors_rgb]

            axes[4].bar(
                range(len(gray_colors_hex)),
                [1] * len(gray_colors_hex),
                color=gray_colors_hex,
            )
            axes[4].set_title("Grayscale")
            axes[4].set_ylim(0, 1.2)
        except Exception as e:
            axes[4].text(
                0.5,
                0.5,
                f"Error:\n{str(e)}",
                ha="center",
                va="center",
                transform=axes[4].transAxes,
            )
            axes[4].set_title("Grayscale")

        # Hide unused subplots
        for i in range(5, 8):
            axes[i].axis("off")

        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, "colorblind_normal.png"),
            dpi=scheme.figure.dpi,
            bbox_inches="tight",
        )
        plt.close()

        # Generate individual colorblind images (simplified)
        for cb_type, title in zip(cb_types, titles):
            try:
                fig, ax = plt.subplots(figsize=(8, 4))
                cb_colors_rgb = _simulate_colorblindness(rgb_colors, cb_type)
                cb_colors_hex = [_rgb_to_hex(rgb) for rgb in cb_colors_rgb]

                ax.bar(
                    range(len(cb_colors_hex)),
                    [1] * len(cb_colors_hex),
                    color=cb_colors_hex,
                )
                ax.set_title(f"{title} Simulation")
                ax.set_ylim(0, 1.2)
                ax.axis("off")

                plt.savefig(
                    os.path.join(output_dir, f"colorblind_{cb_type}.png"),
                    dpi=scheme.figure.dpi,
                    bbox_inches="tight",
                )
                plt.close()
            except Exception:
                # Skip if simulation fails
                pass

    except ImportError:
        print(
            "Warning: Required libraries not available for colorblind preview generation"
        )
    except Exception as e:
        print(f"Warning: Failed to generate colorblind previews: {e}")
