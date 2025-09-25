#!/usr/bin/env python3
"""
Script to generate before/after comparison images for Huez README.

This script creates visualizations showing the difference between default
library colors and Huez-enhanced professional color schemes.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Create assets directories
assets_dir = Path("assets")
comparison_dir = assets_dir / "comparison"
palettes_dir = assets_dir / "palettes"

for dir_path in [comparison_dir, palettes_dir]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Set up sample data
np.random.seed(42)
n_points = 100
n_categories = 5

# Time series data
time = np.linspace(0, 10, n_points)
data = {
    'time': time,
    'series1': np.sin(time) + np.random.normal(0, 0.1, n_points),
    'series2': np.cos(time) + np.random.normal(0, 0.1, n_points),
    'series3': np.sin(time * 2) + np.random.normal(0, 0.1, n_points),
    'series4': np.cos(time * 2) + np.random.normal(0, 0.1, n_points),
    'series5': np.sin(time * 3) + np.random.normal(0, 0.1, n_points),
}

df_lines = pd.DataFrame(data)

# Categorical scatter data
categories = ['A', 'B', 'C', 'D', 'E'] * 20
scatter_data = {
    'x': np.random.normal(0, 1, n_points),
    'y': np.random.normal(0, 1, n_points),
    'category': categories[:n_points],
    'size': np.random.uniform(10, 100, n_points)
}
df_scatter = pd.DataFrame(scatter_data)

# Bar chart data
bar_data = {
    'category': ['Group A', 'Group B', 'Group C', 'Group D', 'Group E'],
    'value': [23, 45, 56, 78, 32],
    'error': [2, 3, 4, 5, 2]
}
df_bars = pd.DataFrame(bar_data)

def create_default_matplotlib_lines():
    """Create ugly default matplotlib line plot"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # 使用非常难看的颜色组合
    ugly_colors = ['#FF00FF', '#00FFFF', '#FFFF00', '#FF0000', '#00FF00']
    for i, col in enumerate(['series1', 'series2', 'series3', 'series4', 'series5']):
        ax.plot(df_lines['time'], df_lines[col], label=f'Series {i+1}',
               linewidth=3, marker='s', markersize=4, color=ugly_colors[i])

    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('BEFORE: 丑陋的默认颜色', fontweight='bold', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3, color='purple', linestyle='--')

    plt.tight_layout()
    plt.savefig(comparison_dir / 'matplotlib_default_lines.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_huez_matplotlib_lines():
    """Create Huez-enhanced matplotlib line plot"""
    # Import huez and apply scheme
    import huez as hz
    hz.use("scheme-1")  # Nature Journal Style

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, col in enumerate(['series1', 'series2', 'series3', 'series4', 'series5']):
        ax.plot(df_lines['time'], df_lines[col], label=f'Series {i+1}', linewidth=2)

    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Huez Nature Journal Style (scheme-1)')
    ax.legend()

    plt.tight_layout()
    plt.savefig(comparison_dir / 'matplotlib_huez_lines.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Reset to default
    plt.style.use('default')

def create_default_seaborn_lines():
    """Create ugly default seaborn line plot"""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8, 5))

    # Melt data for seaborn
    df_melted = df_lines.melt(id_vars=['time'], var_name='series', value_name='value')

    # 强制使用非常难看的颜色
    ugly_palette = ['#FF1493', '#32CD32', '#FFD700', '#DC143C', '#00FFFF']
    sns.lineplot(data=df_melted, x='time', y='value', hue='series', ax=ax,
                linewidth=3, palette=ugly_palette, marker='o', markersize=6)

    ax.set_title('BEFORE: 刺眼的默认配色', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3, color='orange', linestyle='-.')

    plt.tight_layout()
    plt.savefig(comparison_dir / 'seaborn_default_lines.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_huez_seaborn_lines():
    """Create Huez-enhanced seaborn line plot"""
    import huez as hz
    hz.use("scheme-2")  # Science Journal Style

    fig, ax = plt.subplots(figsize=(8, 5))

    # Melt data for seaborn
    df_melted = df_lines.melt(id_vars=['time'], var_name='series', value_name='value')

    sns.lineplot(data=df_melted, x='time', y='value', hue='series', ax=ax, linewidth=2)

    ax.set_title('Huez Science Journal Style (scheme-2)')

    plt.tight_layout()
    plt.savefig(comparison_dir / 'seaborn_huez_lines.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Reset
    plt.style.use('default')

def create_color_palette_showcase():
    """Create showcase images of different color palettes"""
    from huez.registry.palettes import PALETTE_REGISTRY

    # Journal palettes to showcase
    journal_palettes = {
        'npg': ('Nature Publishing Group', PALETTE_REGISTRY['discrete']['npg']),
        'aaas': ('AAAS/Science', PALETTE_REGISTRY['discrete']['aaas']),
        'nejm': ('NEJM', PALETTE_REGISTRY['discrete']['nejm']),
        'lancet': ('The Lancet', PALETTE_REGISTRY['discrete']['lancet']),
        'jama': ('JAMA', PALETTE_REGISTRY['discrete']['jama']),
        'bmj': ('BMJ', PALETTE_REGISTRY['discrete']['bmj']),
        'okabe-ito': ('Okabe-Ito (Colorblind-friendly)', PALETTE_REGISTRY['discrete']['okabe-ito']),
        'paul-tol-bright': ('Paul Tol Bright', PALETTE_REGISTRY['discrete']['paul-tol-bright']),
        'paul-tol-vibrant': ('Paul Tol Vibrant', PALETTE_REGISTRY['discrete']['paul-tol-vibrant'])
    }

    for palette_name, (title, colors) in journal_palettes.items():
        fig, ax = plt.subplots(figsize=(10, 2))

        # Create color bars
        n_colors = len(colors)
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i/n_colors, 0), 1/n_colors, 1, color=color))
            # Add color hex code
            ax.text((i + 0.5)/n_colors, 0.5, color.upper(),
                   ha='center', va='center', fontsize=8, fontweight='bold',
                   color='white' if i < n_colors//2 else 'black')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(f'{title} - {n_colors} Colors', fontsize=12, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()
        plt.savefig(palettes_dir / f'{palette_name}_palette.png', dpi=150, bbox_inches='tight')
        plt.close()

def create_heatmap_examples():
    """Create heatmap comparison examples"""
    # Generate sample correlation matrix
    np.random.seed(42)
    n_vars = 10
    corr_matrix = np.random.uniform(-1, 1, (n_vars, n_vars))
    # Make it symmetric
    corr_matrix = (corr_matrix + corr_matrix.T) / 2
    # Set diagonal to 1
    np.fill_diagonal(corr_matrix, 1)

    var_names = [f'Var_{i+1}' for i in range(n_vars)]

    # Default sequential heatmap
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr_matrix, cmap='viridis', aspect='auto')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Default Sequential (viridis)')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_default_seq.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Huez enhanced sequential
    import huez as hz
    hz.use("scheme-1")

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr_matrix, cmap='viridis', aspect='auto')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Huez Enhanced Sequential (viridis)')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_huez_viridis.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Reset
    plt.style.use('default')

def main():
    """Generate all comparison images"""
    print("Generating comparison images for Huez README...")

    try:
        import huez as hz
        print("✓ Huez library found")
    except ImportError:
        print("✗ Huez library not found. Please install it first.")
        return

    # Generate images
    print("Creating matplotlib line plot comparisons...")
    create_default_matplotlib_lines()
    create_huez_matplotlib_lines()

    print("Creating seaborn line plot comparisons...")
    create_default_seaborn_lines()
    create_huez_seaborn_lines()

    print("Creating color palette showcases...")
    create_color_palette_showcase()

    print("Creating heatmap examples...")
    create_heatmap_examples()

    print("✓ All comparison images generated successfully!")
    print(f"Images saved to: {assets_dir.absolute()}")

if __name__ == "__main__":
    main()
