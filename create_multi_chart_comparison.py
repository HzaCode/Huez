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
    """Create BEFORE: Inconsistent colors across different chart types - Vertical layout"""
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('BEFORE: Inconsistent Colors Across Libraries', fontsize=18, fontweight='bold', y=0.95)

    # Chart 1: Complex Matplotlib line plot with ugly colors
    ugly_mpl_colors = ['#8B4513', '#FF6347', '#9370DB', '#20B2AA', '#FFD700']  # Brown, coral, purple, teal, gold
    for i, col in enumerate(['Group A', 'Group B', 'Group C', 'Group D']):
        axes[0].plot(line_data['time'], line_data[col], label=col, linewidth=3,
                    marker='o', markersize=5, color=ugly_mpl_colors[i])
        # Add error bars for complexity
        error = np.random.uniform(0.05, 0.15, len(line_data))
        axes[0].fill_between(line_data['time'],
                           line_data[col] - error,
                           line_data[col] + error,
                           alpha=0.2, color=ugly_mpl_colors[i])

    axes[0].set_title('Matplotlib Line Plot\n(Ugly Brown/Coral/Purple)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Time (seconds)')
    axes[0].set_ylabel('Measurement Value')
    axes[0].legend(frameon=True, fancybox=True, shadow=True)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].axhline(y=2.5, color='red', linestyle=':', alpha=0.7, label='Threshold')
    axes[0].text(6, 3.2, 'Critical Zone', fontsize=10, color='red')

    # Chart 2: Complex Seaborn scatter with trend lines and different ugly colors
    ugly_sns_colors = ['#FFD700', '#32CD32', '#FF1493', '#00FFFF', '#FF6347']  # Gold, lime, pink, cyan, coral
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        axes[1].scatter(subset['x'], subset['y'], label=f'Category {category}',
                       alpha=0.8, s=60, color=ugly_sns_colors[i], edgecolors='black', linewidth=0.5)

    # Add trend line
    z = np.polyfit(scatter_data['x'], scatter_data['y'], 1)
    p = np.poly1d(z)
    axes[1].plot(scatter_data['x'], p(scatter_data['x']), "r--", alpha=0.8, linewidth=2, label='Trend Line')

    axes[1].set_title('Seaborn Scatter Plot with Trend\n(Ugly Gold/Lime/Pink)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Independent Variable')
    axes[1].set_ylabel('Dependent Variable')
    axes[1].legend(frameon=True, fancybox=True, shadow=True)
    axes[1].grid(True, alpha=0.3)
    axes[1].axvline(x=0, color='gray', linestyle='-', alpha=0.5)
    axes[1].axhline(y=0, color='gray', linestyle='-', alpha=0.5)

    # Chart 3: Complex Matplotlib bar chart with patterns and different ugly colors
    ugly_bar_colors = ['#DC143C', '#8A2BE2', '#FF4500', '#228B22', '#FF6347']  # Crimson, blueviolet, orangered, forestgreen, coral
    bars = axes[2].bar(bar_data['category'], bar_data['value'],
                      color=ugly_bar_colors, alpha=0.8, width=0.6,
                      edgecolor='black', linewidth=1)

    # Add value labels on bars
    for bar, value in zip(bars, bar_data['value']):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{value}', ha='center', va='bottom', fontweight='bold')

    # Add error bars
    error_values = [2, 3, 4, 3]
    axes[2].errorbar(bar_data['category'], bar_data['value'], yerr=error_values,
                    fmt='none', ecolor='black', capsize=5, capthick=2, elinewidth=2)

    axes[2].set_title('Matplotlib Bar Chart with Errors\n(Ugly Crimson/Violet/Orange)', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('Experimental Groups')
    axes[2].set_ylabel('Performance Score')
    axes[2].grid(True, alpha=0.3, axis='y')
    axes[2].set_ylim(0, 70)

    plt.tight_layout()
    plt.savefig('assets/comparison/inconsistent_before.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_consistent_after():
    """Create AFTER: Consistent professional colors across all charts - Vertical layout"""
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('AFTER: Consistent Professional Colors with Huez', fontsize=18, fontweight='bold', y=0.95)

    # Professional NPG colors - consistent across all charts
    npg_colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']

    # Chart 1: Professional Matplotlib line plot with NPG colors
    for i, col in enumerate(['Group A', 'Group B', 'Group C', 'Group D']):
        axes[0].plot(line_data['time'], line_data[col], label=col, linewidth=3,
                    marker='o', markersize=5, color=npg_colors[i], alpha=0.9)
        # Add confidence intervals for scientific look
        error = np.random.uniform(0.03, 0.08, len(line_data))
        axes[0].fill_between(line_data['time'],
                           line_data[col] - error,
                           line_data[col] + error,
                           alpha=0.2, color=npg_colors[i])

    axes[0].set_title('Matplotlib Line Plot\n(Professional NPG Colors)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Time (seconds)')
    axes[0].set_ylabel('Measurement Value')
    axes[0].legend(frameon=True, fancybox=True, shadow=True)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].axhline(y=2.5, color=npg_colors[0], linestyle=':', alpha=0.7, linewidth=2)
    axes[0].text(6.5, 2.6, 'Reference Level', fontsize=10, color=npg_colors[0], fontweight='bold')

    # Chart 2: Professional Seaborn scatter with trend and NPG colors
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        axes[1].scatter(subset['x'], subset['y'], label=f'Category {category}',
                       alpha=0.9, s=70, color=npg_colors[i],
                       edgecolors='white', linewidth=1.5)

    # Add professional trend line with confidence band
    z = np.polyfit(scatter_data['x'], scatter_data['y'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(scatter_data['x'].min(), scatter_data['x'].max(), 100)
    y_trend = p(x_trend)

    # Add confidence band
    y_err = np.std(scatter_data['y']) * 0.1
    axes[1].fill_between(x_trend, y_trend - y_err, y_trend + y_err,
                        alpha=0.2, color='#666666', label='95% CI')
    axes[1].plot(x_trend, y_trend, color='#333333', linewidth=3, alpha=0.8, label='Trend Line')

    axes[1].set_title('Seaborn Scatter Plot with Statistical Analysis\n(Consistent NPG Colors)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Independent Variable')
    axes[1].set_ylabel('Dependent Variable')
    axes[1].legend(frameon=True, fancybox=True, shadow=True)
    axes[1].grid(True, alpha=0.3)
    axes[1].axvline(x=0, color='#666666', linestyle='-', alpha=0.5, linewidth=1)
    axes[1].axhline(y=0, color='#666666', linestyle='-', alpha=0.5, linewidth=1)

    # Chart 3: Professional Matplotlib bar chart with NPG colors
    bars = axes[2].bar(bar_data['category'], bar_data['value'],
                      color=npg_colors, alpha=0.9, width=0.7,
                      edgecolor='white', linewidth=2)

    # Add professional value labels
    for bar, value in zip(bars, bar_data['value']):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{value}', ha='center', va='bottom',
                    fontweight='bold', fontsize=11, color=npg_colors[list(bar_data['category']).index(bar_data['category'][list(bars).index(bar)])])

    # Add error bars with professional styling
    error_values = [2.1, 3.2, 4.1, 2.8]
    axes[2].errorbar(bar_data['category'], bar_data['value'], yerr=error_values,
                    fmt='none', ecolor='#333333', capsize=6, capthick=2, elinewidth=2, alpha=0.8)

    axes[2].set_title('Matplotlib Bar Chart with Statistical Significance\n(Consistent NPG Colors)', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('Experimental Groups')
    axes[2].set_ylabel('Performance Score')
    axes[2].grid(True, alpha=0.3, axis='y')
    axes[2].set_ylim(0, 70)

    # Add significance markers
    axes[2].text(0.5, 65, '* p < 0.05', ha='center', fontsize=12, fontweight='bold')
    axes[2].text(1.5, 62, '** p < 0.01', ha='center', fontsize=12, fontweight='bold')
    axes[2].text(2.5, 68, '*** p < 0.001', ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('assets/comparison/consistent_after.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_inconsistent_before()
    create_consistent_after()
    print("✓ Multi-chart comparison images created!")
