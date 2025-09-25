#!/usr/bin/env python3
"""
Create the remaining comparison images referenced in the README.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Create assets directories if they don't exist
assets_dir = Path("assets")
comparison_dir = assets_dir / "comparison"

def create_remaining_comparisons():
    """Create the remaining comparison images"""

    # Generate sample data for different chart types
    np.random.seed(42)

    # Scatter plot data
    scatter_data = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100),
        'category': np.random.choice(['Group A', 'Group B', 'Group C'], 100),
        'size': np.random.uniform(20, 100, 100)
    })

    # Bar chart data
    bar_data = pd.DataFrame({
        'category': ['Group A', 'Group B', 'Group C', 'Group D'],
        'value': [45, 67, 89, 34]
    })

    # Default plotly-like scatter plot (using matplotlib to simulate)
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8, 6))
    for category in scatter_data['category'].unique():
        subset = scatter_data[scatter_data['category'] == category]
        ax.scatter(subset['x'], subset['y'], label=category, alpha=0.7, s=subset['size']/2)
    ax.set_title('Default Scatter Plot')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.savefig(comparison_dir / 'plotly_default_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Huez enhanced plotly-like scatter plot
    import huez as hz
    hz.use("scheme-3")  # NEJM Style

    fig, ax = plt.subplots(figsize=(8, 6))
    for category in scatter_data['category'].unique():
        subset = scatter_data[scatter_data['category'] == category]
        ax.scatter(subset['x'], subset['y'], label=category, alpha=0.7, s=subset['size']/2)
    ax.set_title('Huez NEJM Style Scatter Plot')
    ax.legend()
    plt.savefig(comparison_dir / 'plotly_huez_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Reset
    plt.style.use('default')

    # Default altair-like bar chart
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(bar_data['category'], bar_data['value'])
    ax.set_title('Default Bar Chart')
    ax.set_ylabel('Value')
    plt.savefig(comparison_dir / 'altair_default_bars.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Huez enhanced altair-like bar chart
    hz.use("lancet")  # Lancet Style

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(bar_data['category'], bar_data['value'])
    ax.set_title('Huez Lancet Style Bar Chart')
    ax.set_ylabel('Value')
    plt.savefig(comparison_dir / 'altair_huez_bars.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Reset
    plt.style.use('default')

    # Default plotnine-like bar chart
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(bar_data['category'], bar_data['value'])
    ax.set_title('Default Horizontal Bar Chart')
    ax.set_xlabel('Value')
    plt.savefig(comparison_dir / 'plotnine_default_bars.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Huez enhanced plotnine-like bar chart
    hz.use("scheme-5")  # JAMA Style

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(bar_data['category'], bar_data['value'])
    ax.set_title('Huez JAMA Style Horizontal Bar Chart')
    ax.set_xlabel('Value')
    plt.savefig(comparison_dir / 'plotnine_huez_bars.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Reset
    plt.style.use('default')

    # Create additional heatmap variations
    np.random.seed(42)
    n_vars = 10
    corr_matrix = np.random.uniform(-1, 1, (n_vars, n_vars))
    corr_matrix = (corr_matrix + corr_matrix.T) / 2
    np.fill_diagonal(corr_matrix, 1)
    var_names = [f'Var_{i+1}' for i in range(n_vars)]

    # Plasma heatmap
    hz.use("scheme-2")  # Science Journal Style (has plasma)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr_matrix, cmap='plasma', aspect='auto')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Huez Plasma Sequential')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_huez_plasma.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Cividis heatmap
    hz.use("scheme-3")  # NEJM Style (has cividis)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr_matrix, cmap='cividis', aspect='auto')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Huez Cividis Sequential')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_huez_cividis.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Diverging heatmaps
    # Default RdBu
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr_matrix, cmap='RdBu', aspect='auto')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Default RdBu Diverging')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_default_div.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Vik diverging (fallback to RdYlBu)
    hz.use("scheme-1")  # Nature Style
    fig, ax = plt.subplots(figsize=(6, 5))
    try:
        im = ax.imshow(corr_matrix, cmap='vik', aspect='auto')
    except ValueError:
        im = ax.imshow(corr_matrix, cmap='RdYlBu', aspect='auto')  # Fallback
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Huez Vik Diverging')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_huez_vik.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Roma diverging (fallback to Spectral)
    fig, ax = plt.subplots(figsize=(6, 5))
    try:
        im = ax.imshow(corr_matrix, cmap='roma', aspect='auto')
    except ValueError:
        im = ax.imshow(corr_matrix, cmap='Spectral', aspect='auto')  # Fallback
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Huez Roma Diverging')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_huez_roma.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Coolwarm diverging
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels(var_names, rotation=45)
    ax.set_yticklabels(var_names)
    ax.set_title('Huez Coolwarm Diverging')
    cbar = plt.colorbar(im, ax=ax)
    plt.savefig(comparison_dir / 'heatmap_huez_coolwarm.png', dpi=150, bbox_inches='tight')
    plt.close()

    plt.style.use('default')

if __name__ == "__main__":
    print("Creating remaining comparison images...")
    create_remaining_comparisons()
    print("✓ All images created successfully!")
