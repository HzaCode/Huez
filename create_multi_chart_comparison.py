import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Generate complex data for all charts
def generate_data():
    """Generate comprehensive dataset for complex dashboard"""
    # Time series data
    time = np.linspace(0, 8, 50)
    line_data = pd.DataFrame({
        'time': time,
        'Group A': 2 + 0.5 * np.sin(time) + 0.3 * np.random.normal(0, 0.1, len(time)),
        'Group B': 1.5 + 0.8 * np.cos(time * 0.7) + 0.2 * np.random.normal(0, 0.1, len(time)),
        'Group C': 1 + 1.2 * np.sin(time * 1.2) + 0.4 * np.random.normal(0, 0.1, len(time)),
        'Group D': 2.5 + 0.6 * np.cos(time * 0.5) + 0.25 * np.random.normal(0, 0.1, len(time))
    })
    
    # Scatter plot data
    n_points = 200
    scatter_data = pd.DataFrame({
        'x': np.random.normal(0, 1, n_points),
        'y': np.random.normal(0, 1, n_points),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_points),
        'size': np.random.uniform(20, 100, n_points)
    })
    
    # Bar chart data
    bar_data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'value': [23, 45, 56, 32]
    })
    
    return line_data, scatter_data, bar_data

def create_inconsistent_before():
    """Create BEFORE: Complex multi-panel inconsistent colors - Dashboard style"""
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('BEFORE: Inconsistent Colors Across Complex Research Dashboard', fontsize=20, fontweight='bold', y=0.98)

    gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3, top=0.9, bottom=0.1, left=0.1, right=0.9)

    # Generate data
    line_data, scatter_data, bar_data = generate_data()

    # Panel 1: Time series with multiple lines and annotations
    ax1 = fig.add_subplot(gs[0, :2])
    ugly_colors_1 = ['#8B4513', '#FF6347', '#9370DB', '#20B2AA'] # Brown, coral, purple, teal
    for i, col in enumerate(['Group A', 'Group B', 'Group C', 'Group D']):
        ax1.plot(line_data['time'], line_data[col], label=col, linewidth=3,
                marker='o', markersize=6, color=ugly_colors_1[i])
        # Add confidence bands
        error = np.random.uniform(0.08, 0.18, len(line_data))
        ax1.fill_between(line_data['time'], line_data[col] - error, line_data[col] + error,
                        alpha=0.3, color=ugly_colors_1[i])

    ax1.axhline(y=2.5, color='red', linestyle='--', alpha=0.8, linewidth=2)
    ax1.axvspan(2, 4, alpha=0.2, color='yellow', label='Critical Period')
    ax1.axvspan(4.5, 6, alpha=0.2, color='yellow', label='Intervention')
    ax1.set_title('Time Series Analysis\n(Brown/Coral/Purple/Teal)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel('Response Variable')
    ax1.legend(frameon=True, fancybox=True, shadow=True, loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Panel 2: Complex scatter plot with multiple groups and regression
    ax2 = fig.add_subplot(gs[0, 2:])
    ugly_colors_2 = ['#FFD700', '#32CD32', '#FF1493', '#00FFFF'] # Gold, lime, pink, cyan
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        ax2.scatter(subset['x'], subset['y'], label=f'Cluster {category}',
                   alpha=0.9, s=80, color=ugly_colors_2[i], edgecolors='black', linewidth=1.5)
        # Add regression lines
        if len(subset) > 2:
            z = np.polyfit(subset['x'], subset['y'], 1)
            p = np.poly1d(z)
            x_range = np.linspace(subset['x'].min(), subset['x'].max(), 20)
            ax2.plot(x_range, p(x_range), '--', color=ugly_colors_2[i], linewidth=3, alpha=0.8)

    ax2.axhline(y=0, color='#666666', linestyle='-', alpha=0.5, linewidth=1)
    ax2.axvline(x=0, color='#666666', linestyle='-', alpha=0.5, linewidth=1)
    ax2.set_title('Multi-Cluster Analysis\n(Gold/Lime/Pink/Cyan)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Feature X')
    ax2.set_ylabel('Feature Y')
    ax2.legend(frameon=True, fancybox=True, shadow=True, loc='upper right')
    ax2.grid(True, alpha=0.3)

    # Panel 3: Statistical comparison bars
    ax3 = fig.add_subplot(gs[1, :2])
    ugly_colors_3 = ['#DC143C', '#8A2BE2', '#FF4500', '#228B22'] # Crimson, blueviolet, orangered, forestgreen
    bars = ax3.bar(bar_data['category'], bar_data['value'],
                  color=ugly_colors_3, alpha=0.9, width=0.7,
                  edgecolor='white', linewidth=2)

    # Add detailed annotations
    for bar, value in zip(bars, bar_data['value']):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{value}±{value*0.15:.1f}', ha='center', va='bottom',
                fontweight='bold', fontsize=10)

    # Add significance indicators
    ax3.text(0.5, 55, '***', ha='center', fontsize=16, color='red', fontweight='bold')
    ax3.text(1.5, 52, '**', ha='center', fontsize=16, color='red', fontweight='bold')
    ax3.text(2.5, 58, '*', ha='center', fontsize=16, color='red', fontweight='bold')

    ax3.set_title('Statistical Comparisons\n(Crimson/Violet/Orange/Green)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Treatment Conditions')
    ax3.set_ylabel('Mean Response (±SEM)')
    ax3.set_ylim(0, 70)
    ax3.grid(True, alpha=0.3, axis='y')

    # Panel 4: Distribution analysis
    ax4 = fig.add_subplot(gs[1, 2])
    ugly_colors_4 = ['#FF6347', '#9370DB', '#20B2AA', '#FFD700']
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        ax4.hist(subset['x'], bins=8, alpha=0.8, label=f'Dist {category}',
                color=ugly_colors_4[i], edgecolor='white', linewidth=1.5)

    ax4.set_title('Distribution\nAnalysis', fontsize=11, fontweight='bold')
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Frequency')
    ax4.legend(frameon=True, fancybox=True, shadow=True)
    ax4.grid(True, alpha=0.3, axis='y')

    # Panel 5: Correlation matrix heatmap
    ax5 = fig.add_subplot(gs[1, 3])
    corr_data = np.random.uniform(-0.8, 0.9, (4, 4))
    np.fill_diagonal(corr_data, 1.0)
    im = ax5.imshow(corr_data, cmap='RdYlBu_r', vmin=-1, vmax=1)
    ax5.set_xticks(range(4))
    ax5.set_yticks(range(4))
    ax5.set_xticklabels(['A', 'B', 'C', 'D'])
    ax5.set_yticklabels(['A', 'B', 'C', 'D'])
    ax5.set_title('Correlation\nMatrix', fontsize=11, fontweight='bold')
    plt.colorbar(im, ax=ax5, shrink=0.8)

    # Panel 6: Summary statistics
    ax6 = fig.add_subplot(gs[2, :])
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC', 'Specificity']
    values = [0.85, 0.82, 0.88, 0.87, 0.90, 0.78]
    ugly_colors_6 = ['#8B4513', '#FF6347', '#9370DB', '#20B2AA', '#FFD700', '#32CD32']
    bars = ax6.bar(metrics, values, color=ugly_colors_6, alpha=0.9, width=0.7,
                  edgecolor='white', linewidth=2)
    
    # Add error bars
    errors = [0.02, 0.03, 0.025, 0.02, 0.015, 0.03]
    ax6.errorbar(metrics, values, yerr=errors, fmt='none', color='black', capsize=5, capthick=2)
    
    ax6.set_title('Model Performance Metrics\n(Mixed Color Schemes)', fontsize=14, fontweight='bold')
    ax6.set_ylabel('Performance Score')
    ax6.set_ylim(0, 1.0)
    ax6.grid(True, alpha=0.3, axis='y')

    # Add performance labels
    for bar, val in zip(bars, values):
        ax6.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')

    plt.savefig('inconsistent_before.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_consistent_after():
    """Create AFTER: Consistent professional colors with Huez - ONE LINE DOES IT ALL!"""
    # Apply Huez color scheme - this is the magic line!
    import huez as hz
    hz.use("scheme-1")  # One line changes ALL colors!
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('AFTER: Consistent Professional Colors with Huez', fontsize=20, fontweight='bold', y=0.98)

    # Create the same complex dashboard layout
    gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3,
                         top=0.9, bottom=0.1, left=0.1, right=0.9)

    # Generate data
    line_data, scatter_data, bar_data = generate_data()

    # Panel 1: Time series with Huez automatic colors
    ax1 = fig.add_subplot(gs[0, :2])
    for i, col in enumerate(['Group A', 'Group B', 'Group C', 'Group D']):
        # 🎨 HUEZ MAGIC: No need to specify color! Huez automatically assigns professional colors
        # Before: color=npg_colors[i] or color='#E64B35' 
        # Now: Huez handles it automatically!
        ax1.plot(line_data['time'], line_data[col], label=col, linewidth=3,
                marker='o', markersize=6, alpha=0.9)
        # Add confidence bands - also automatically colored by Huez
        error = np.random.uniform(0.08, 0.18, len(line_data))
        ax1.fill_between(line_data['time'], line_data[col] - error, line_data[col] + error,
                        alpha=0.3)

    ax1.axhline(y=2.5, color='red', linestyle='--', alpha=0.8, linewidth=2)
    ax1.axvspan(2, 6, alpha=0.2, color='lightblue', label='Critical Period')
    ax1.axvspan(3, 4, alpha=0.3, color='lightblue', label='Experimental Intervention')
    ax1.set_title('Time Series Analysis\n(Consistent NPG Colors)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel('Response Variable')
    ax1.legend(frameon=True, fancybox=True, shadow=True, loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Panel 2: Scatter plot with Huez automatic colors
    ax2 = fig.add_subplot(gs[0, 2:])
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        # 🎨 HUEZ MAGIC: No color specification needed! Huez auto-assigns consistent colors
        # Before: color=npg_colors[i] or color='#4DBBD5'
        # Now: Huez automatically uses the same color scheme across all plots!
        ax2.scatter(subset['x'], subset['y'], label=f'Cluster {category}',
                   alpha=0.9, s=80, edgecolors='white', linewidth=1.5)
        # Add regression lines - also automatically colored by Huez
        if len(subset) > 2:
            z = np.polyfit(subset['x'], subset['y'], 1)
            p = np.poly1d(z)
            x_range = np.linspace(subset['x'].min(), subset['x'].max(), 20)
            ax2.plot(x_range, p(x_range), '--', linewidth=3, alpha=0.8)

    ax2.axhline(y=0, color='#666666', linestyle='-', alpha=0.5, linewidth=1)
    ax2.axvline(x=0, color='#666666', linestyle='-', alpha=0.5, linewidth=1)
    ax2.set_title('Multi-Cluster Analysis\n(Consistent NPG Colors)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Feature X')
    ax2.set_ylabel('Feature Y')
    ax2.legend(frameon=True, fancybox=True, shadow=True, loc='upper right')
    ax2.grid(True, alpha=0.3)

    # Panel 3: Statistical bars with Huez automatic colors
    ax3 = fig.add_subplot(gs[1, :2])
    # 🎨 HUEZ MAGIC: Bar colors automatically assigned! No manual color specification needed
    # Before: color=npg_colors or color=['#E64B35', '#4DBBD5', '#00A087', '#3C5488']
    # Now: Huez automatically applies consistent colors to all bars!
    bars = ax3.bar(bar_data['category'], bar_data['value'],
                  alpha=0.9, width=0.7,
                  edgecolor='white', linewidth=2)

    # Add detailed annotations
    for bar, value in zip(bars, bar_data['value']):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{value}±{value*0.15:.1f}', ha='center', va='bottom',
                fontweight='bold', fontsize=10)

    # Add significance indicators
    ax3.text(0.5, 55, '***', ha='center', fontsize=16, color='red', fontweight='bold')
    ax3.text(1.5, 52, '**', ha='center', fontsize=16, color='red', fontweight='bold')
    ax3.text(2.5, 58, '*', ha='center', fontsize=16, color='red', fontweight='bold')

    ax3.set_title('Statistical Comparisons\n(Consistent NPG Colors)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Treatment Conditions')
    ax3.set_ylabel('Mean Response (±SEM)')
    ax3.set_ylim(0, 70)
    ax3.grid(True, alpha=0.3, axis='y')

    # Panel 4: Distribution analysis with Huez automatic colors
    ax4 = fig.add_subplot(gs[1, 2])
    for i, category in enumerate(['A', 'B', 'C', 'D']):
        subset = scatter_data[scatter_data['category'] == category]
        # 🎨 HUEZ MAGIC: Histogram colors automatically assigned! 
        # Before: color=ugly_colors_4[i] or color='#FF6347'
        # Now: Huez ensures consistent colors across all distribution plots!
        ax4.hist(subset['x'], bins=8, alpha=0.8, label=f'Dist {category}',
                edgecolor='white', linewidth=1.5)

    ax4.set_title('Distribution\nAnalysis', fontsize=11, fontweight='bold')
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Frequency')
    ax4.legend(frameon=True, fancybox=True, shadow=True)
    ax4.grid(True, alpha=0.3, axis='y')

    # Panel 5: Correlation matrix with consistent styling
    ax5 = fig.add_subplot(gs[1, 3])
    corr_data = np.random.uniform(-0.8, 0.9, (4, 4))
    np.fill_diagonal(corr_data, 1.0)
    im = ax5.imshow(corr_data, cmap='RdBu_r', vmin=-1, vmax=1)
    ax5.set_xticks(range(4))
    ax5.set_yticks(range(4))
    ax5.set_xticklabels(['A', 'B', 'C', 'D'])
    ax5.set_yticklabels(['A', 'B', 'C', 'D'])
    ax5.set_title('Correlation\nMatrix', fontsize=11, fontweight='bold')
    plt.colorbar(im, ax=ax5, shrink=0.8)

    # Panel 6: Performance metrics with Huez automatic colors
    ax6 = fig.add_subplot(gs[2, :])
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC', 'Specificity']
    values = [0.85, 0.82, 0.88, 0.87, 0.90, 0.78]
    # 🎨 HUEZ MAGIC: All performance metric bars automatically colored!
    # Before: color=ugly_colors_6 or color=['#8B4513', '#FF6347', '#9370DB', '#20B2AA', '#FFD700', '#32CD32']
    # Now: Huez automatically applies consistent professional colors to all metrics!
    bars = ax6.bar(metrics, values, alpha=0.9, width=0.7,
                  edgecolor='white', linewidth=2)
    
    # Add error bars
    errors = [0.02, 0.03, 0.025, 0.02, 0.015, 0.03]
    ax6.errorbar(metrics, values, yerr=errors, fmt='none', color='black', capsize=5, capthick=2)
    
    ax6.set_title('Model Performance Metrics\n(Consistent NPG Colors)', fontsize=14, fontweight='bold')
    ax6.set_ylabel('Performance Score')
    ax6.set_ylim(0, 1.0)
    ax6.grid(True, alpha=0.3, axis='y')

    # Add performance labels
    for bar, val in zip(bars, values):
        ax6.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')

    plt.savefig('consistent_after.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Creating complex multi-chart comparison...")
    create_inconsistent_before()
    create_consistent_after()
    print("✓ Multi-chart comparison images created!")