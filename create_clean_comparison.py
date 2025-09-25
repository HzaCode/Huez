#!/usr/bin/env python3
"""
Create clean line chart comparison for README.
"""

import numpy as np
import matplotlib.pyplot as plt

# Generate very clean sample data
np.random.seed(42)
time = np.linspace(0, 8, 80)

# Create clean, orderly datasets
line_data = {
    'time': time,
    'Group A': 2 + np.sin(time * 0.8) + 0.1 * np.sin(time * 2.4),
    'Group B': 1.5 + np.cos(time * 0.6) + 0.1 * np.cos(time * 1.8),
    'Group C': 2.5 + np.sin(time * 1.2) + 0.05 * np.sin(time * 3.6),
    'Group D': 1 + np.cos(time * 0.9) + 0.05 * np.cos(time * 2.7),
}

def create_clean_before():
    """Create clean 'before' plot with orderly messy colors"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Use orderly but not too ugly colors
    colors = ['#8B4513', '#CD853F', '#DAA520', '#556B2F']  # Brown, orange, gold, dark green

    for i, (label, values) in enumerate(list(line_data.items())[1:]):
        ax.plot(line_data['time'], values, label=label, linewidth=2.5,
               marker='o', markersize=4, color=colors[i])

    ax.set_title('BEFORE: Default Colors', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend(frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)

    plt.tight_layout()
    plt.savefig('assets/comparison/clean_before.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_clean_after():
    """Create clean 'after' plot with professional colors"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Use professional NPG colors
    colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']

    for i, (label, values) in enumerate(list(line_data.items())[1:]):
        ax.plot(line_data['time'], values, label=label, linewidth=2.5,
               marker='o', markersize=4, color=colors[i], alpha=0.9)

    ax.set_title('AFTER: Professional Colors', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend(frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)

    plt.tight_layout()
    plt.savefig('assets/comparison/clean_after.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_clean_before()
    create_clean_after()
    print("✓ Clean comparison images created!")
