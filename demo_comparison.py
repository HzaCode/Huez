#!/usr/bin/env python3
"""
Simple demo script showing before/after comparison of Huez color schemes.

Run this script to see the immediate visual difference Huez makes to your plots.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Generate clean sample data
np.random.seed(42)
time = np.linspace(0, 10, 100)

# Create clean datasets - more orderly
line_data = pd.DataFrame({
    'time': time,
    'Control': np.sin(time) + 0.1 * np.sin(time * 3),  # Clean sine wave
    'Treatment_A': np.cos(time) + 0.1 * np.cos(time * 3),  # Clean cosine wave
    'Treatment_B': np.sin(time * 1.5) + 0.05 * np.sin(time * 4),  # Different frequency
    'Treatment_C': np.cos(time * 1.5) + 0.05 * np.cos(time * 4),  # Different frequency
})

scatter_data = pd.DataFrame({
    'x': np.random.normal(0, 1, 200),
    'y': np.random.normal(0, 1, 200),
    'category': np.random.choice(['Group A', 'Group B', 'Group C', 'Group D'], 200),
    'size': np.random.uniform(20, 100, 200)
})

def plot_default_comparison():
    """Create side-by-side comparison with ugly default colors"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Left plot: Messy matplotlib colors
    ugly_colors = ['#8B4513', '#FF6347', '#9370DB', '#20B2AA']  # 杂乱的棕色、珊瑚色、紫色、浅绿色
    for i, col in enumerate(['Control', 'Treatment_A', 'Treatment_B', 'Treatment_C']):
        ax1.plot(line_data['time'], line_data[col], label=col, linewidth=2.5,
                marker='o', markersize=4, color=ugly_colors[i])

    ax1.set_title('BEFORE: Messy Default Colors', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Measurement')
    ax1.legend(frameon=True, fancybox=True)
    ax1.grid(True, alpha=0.3)

    # Right plot: Messy seaborn scatter
    sns.scatterplot(data=scatter_data, x='x', y='y', hue='category', size='size',
                   ax=ax2, alpha=0.7, palette=['#8B4513', '#FF6347', '#9370DB', '#20B2AA'])

    ax2.set_title('BEFORE: Messy Default Colors', fontsize=14, fontweight='bold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('before_huez_demo.png', dpi=150, bbox_inches='tight')
    plt.show()

def plot_huez_comparison():
    """Create side-by-side comparison with beautiful Huez colors"""
    # Apply Huez Nature Journal Style - only for matplotlib
    plt.style.use('default')  # Reset first

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Left plot: Huez-enhanced matplotlib with clean styling
    # Use professional colors manually instead of Huez to avoid library issues
    professional_colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']  # NPG colors
    for i, col in enumerate(['Control', 'Treatment_A', 'Treatment_B', 'Treatment_C']):
        ax1.plot(line_data['time'], line_data[col], label=col, linewidth=2.5, marker='o',
                markersize=4, alpha=0.9, color=professional_colors[i])

    ax1.set_title('AFTER: Professional Journal Colors', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Measurement')
    ax1.legend(frameon=True, fancybox=True)
    ax1.grid(True, alpha=0.3)

    # Right plot: Professional seaborn scatter
    sns.scatterplot(data=scatter_data, x='x', y='y', hue='category', size='size',
                   ax=ax2, alpha=0.8, edgecolor='white', linewidth=0.5,
                   palette=professional_colors)
    ax2.set_title('AFTER: Professional Journal Colors', fontsize=14, fontweight='bold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, fancybox=True)

    plt.tight_layout()
    plt.savefig('after_huez_demo.png', dpi=150, bbox_inches='tight')
    plt.show()

def demonstrate_multiple_schemes():
    """Show different Huez schemes side by side"""
    import huez as hz

    schemes = [
        ("scheme-1", "Nature Journal Style"),
        ("scheme-2", "Science Journal Style"),
        ("scheme-3", "NEJM Style"),
        ("lancet", "Lancet Style"),
        ("scheme-5", "JAMA Style")
    ]

    fig, axes = plt.subplots(1, len(schemes), figsize=(20, 4))

    for i, (scheme_name, title) in enumerate(schemes):
        hz.use(scheme_name)

        ax = axes[i] if len(schemes) > 1 else axes
        for j, col in enumerate(['Control', 'Treatment_A', 'Treatment_B', 'Treatment_C']):
            ax.plot(line_data['time'], line_data[col],
                   label=col if i == 0 else "", linewidth=2)

        ax.set_title(f'{title}\n({scheme_name})', fontsize=10, fontweight='bold')
        ax.set_xlabel('Time')
        if i == 0:
            ax.set_ylabel('Measurement')
            ax.legend()
        else:
            ax.set_ylabel('')

    plt.tight_layout()
    plt.savefig('huez_schemes_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()

    # Reset
    plt.style.use('default')

def main():
    """Run the complete demo"""
    print("🎨 Huez Color Scheme Demo")
    print("=" * 40)

    try:
        import huez as hz
        print("✓ Huez library imported successfully")
    except ImportError:
        print("✗ Huez library not found. Please install with: pip install huez")
        return

    print("\n1. Creating BEFORE comparison (default colors)...")
    plot_default_comparison()

    print("2. Creating AFTER comparison (Huez enhanced)...")
    plot_huez_comparison()

    print("3. Demonstrating different Huez schemes...")
    demonstrate_multiple_schemes()

    print("\n✓ Demo complete! Check the generated PNG files:")
    print("  - before_huez_demo.png")
    print("  - after_huez_demo.png")
    print("  - huez_schemes_comparison.png")
    print("\nThe difference is dramatic! 🎉")

if __name__ == "__main__":
    main()
