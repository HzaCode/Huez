#!/usr/bin/env python3
"""
Create multi-chart comparison showing inconsistent vs consistent colors.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Generate sample data
np.random.seed(42)
time = np.linspace(0, 8, 80)

# Create datasets
line_data = pd.DataFrame({
    'time': time,
    'Group A': 2 + np.sin(time * 0.8),
    'Group B': 1.5 + np.cos(time * 0.6),
    'Group C': 2.5 + np.sin(time * 1.2),
    'Group D': 1 + np.cos(time * 0.9),
})

scatter_data = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100),
    'category': np.random.choice(['A', 'B', 'C', 'D'], 100)
})

bar_data = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [23, 45, 56, 32]
})

def create_inconsistent_before():
    """Create BEFORE: Inconsistent colors across different chart types"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('BEFORE: Inconsistent Colors Across Libraries', fontsize=16, fontweight='bold')

    # Chart 1: Matplotlib line plot with ugly colors
    ugly_mpl_colors = ['#8B4513', '#FF6347', '#9370DB', '#20B2AA']  # Brown, coral, purple, teal
    for i, col in enumerate(['Group A', 'Group B', 'Group C', 'Group D']):
        axes[0].plot(line_data['time'], line_data[col], label=col, linewidth=2.5,
                    marker='o', markersize=4, color=ugly_mpl_colors[i])
    axes[0].set_title('Matplotlib\n(Ugly Brown/Coral)', fontsize=12)
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Value')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Chart 2: Seaborn scatter with different ugly colors
    ugly_sns_colors = ['#FFD700', '#32CD32', '#FF1493', '#00FFFF']  # Gold, lime, pink, cyan
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        axes[1].scatter(subset['x'], subset['y'], label=category, alpha=0.7, s=50,
                       color=ugly_sns_colors[i])
    axes[1].set_title('Seaborn\n(Ugly Gold/Lime)', fontsize=12)
    axes[1].set_xlabel('X Value')
    axes[1].set_ylabel('Y Value')
    axes[1].legend()

    # Chart 3: Matplotlib bar chart with yet different ugly colors
    ugly_bar_colors = ['#DC143C', '#8A2BE2', '#FF4500', '#228B22']  # Crimson, blueviolet, orangered, forestgreen
    bars = axes[2].bar(bar_data['category'], bar_data['value'],
                      color=ugly_bar_colors, alpha=0.8)
    axes[2].set_title('Matplotlib Bars\n(Ugly Crimson/Violet)', fontsize=12)
    axes[2].set_xlabel('Category')
    axes[2].set_ylabel('Value')

    plt.tight_layout()
    plt.savefig('assets/comparison/inconsistent_before.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_consistent_after():
    """Create AFTER: Consistent professional colors across all charts"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('AFTER: Consistent Professional Colors with Huez', fontsize=16, fontweight='bold')

    # Professional NPG colors - consistent across all charts
    npg_colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']

    # Chart 1: Matplotlib line plot with NPG colors
    for i, col in enumerate(['Group A', 'Group B', 'Group C', 'Group D']):
        axes[0].plot(line_data['time'], line_data[col], label=col, linewidth=2.5,
                    marker='o', markersize=4, color=npg_colors[i])
    axes[0].set_title('Matplotlib\n(NPG Colors)', fontsize=12)
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Value')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Chart 2: Seaborn scatter with SAME NPG colors
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        axes[1].scatter(subset['x'], subset['y'], label=category, alpha=0.8, s=50,
                       color=npg_colors[i])
    axes[1].set_title('Seaborn\n(Same NPG Colors)', fontsize=12)
    axes[1].set_xlabel('X Value')
    axes[1].set_ylabel('Y Value')
    axes[1].legend()

    # Chart 3: Matplotlib bar chart with SAME NPG colors
    bars = axes[2].bar(bar_data['category'], bar_data['value'],
                      color=npg_colors, alpha=0.9)
    axes[2].set_title('Matplotlib Bars\n(Same NPG Colors)', fontsize=12)
    axes[2].set_xlabel('Category')
    axes[2].set_ylabel('Value')

    plt.tight_layout()
    plt.savefig('assets/comparison/consistent_after.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_inconsistent_before()
    create_consistent_after()
    print("✓ Multi-chart comparison images created!")
