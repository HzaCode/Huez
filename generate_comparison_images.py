#!/usr/bin/env python3
"""
Generate comparison images for README documentation.

This script creates before/after comparison images showing the difference
between default colors and Huez-enhanced visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Create images directory if it doesn't exist
images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

# Sample data
np.random.seed(42)
n = 100
df = pd.DataFrame({
    'x': np.random.randn(n),
    'y': np.random.randn(n),
    'category': np.random.choice(['A', 'B', 'C', 'D'], n),
    'value': np.random.exponential(2, n)
})

def create_matplotlib_comparison():
    """Create matplotlib before/after comparison."""
    
    # Before (default colors)
    plt.figure(figsize=(8, 6))
    categories = df['category'].unique()
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        plt.scatter(data['x'], data['y'], label=f'Category {cat}', alpha=0.7, s=50)
    
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.title('Matplotlib Scatter Plot - Default Colors')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(images_dir / 'mpl_before.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # After (with hypothetical Huez colors - using a professional palette)
    colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']  # Professional color scheme
    plt.figure(figsize=(8, 6))
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        plt.scatter(data['x'], data['y'], label=f'Category {cat}', 
                   color=colors[i], alpha=0.8, s=50)
    
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.title('Matplotlib Scatter Plot - Huez Enhanced')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(images_dir / 'mpl_after.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_seaborn_comparison():
    """Create seaborn before/after comparison."""
    
    # Before (default colors)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='x', y='y', hue='category', s=60)
    plt.title('Seaborn Scatter Plot - Default Colors')
    plt.tight_layout()
    plt.savefig(images_dir / 'sns_before.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # After (with professional palette)
    plt.figure(figsize=(8, 6))
    colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']
    sns.scatterplot(data=df, x='x', y='y', hue='category', palette=colors, s=60)
    plt.title('Seaborn Scatter Plot - Huez Enhanced')
    plt.tight_layout()
    plt.savefig(images_dir / 'sns_after.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_main_comparison():
    """Create the main before/after comparison."""
    
    # Create a more complex plot for main comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Before - default colors
    categories = df['category'].unique()
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        ax1.scatter(data['x'], data['y'], label=f'Group {cat}', alpha=0.7, s=50)
    
    ax1.set_xlabel('X Value')
    ax1.set_ylabel('Y Value')
    ax1.set_title('Before: Default Colors\n(Bland and unprofessional)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # After - professional colors
    colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        ax2.scatter(data['x'], data['y'], label=f'Group {cat}', 
                   color=colors[i], alpha=0.8, s=50)
    
    ax2.set_xlabel('X Value')
    ax2.set_ylabel('Y Value')
    ax2.set_title('After: Huez Enhanced\n(Professional publication-ready)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(images_dir / 'before_after_main.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save individual versions
    # Before only
    plt.figure(figsize=(8, 6))
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        plt.scatter(data['x'], data['y'], label=f'Group {cat}', alpha=0.7, s=50)
    
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.title('Default Colors')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(images_dir / 'before_default.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # After only
    plt.figure(figsize=(8, 6))
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        plt.scatter(data['x'], data['y'], label=f'Group {cat}', 
                   color=colors[i], alpha=0.8, s=50)
    
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.title('Huez Enhanced')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(images_dir / 'after_huez.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_scheme_previews():
    """Create preview images for different color schemes."""
    
    schemes = {
        'scheme1': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
        'lancet': ['#00468B', '#ED0000', '#42B540', '#0099B4'],
        'nature': ['#E64B35', '#4DBBD5', '#00A087', '#3C5488'],
        'nejm': ['#BC3C29', '#0072B5', '#E18727', '#20854E']
    }
    
    for scheme_name, colors in schemes.items():
        plt.figure(figsize=(6, 4))
        
        # Create a simple bar chart to show the colors
        categories = ['A', 'B', 'C', 'D']
        values = [3, 7, 2, 5]
        
        bars = plt.bar(categories, values, color=colors, alpha=0.8)
        plt.title(f'{scheme_name.title()} Color Scheme')
        plt.ylabel('Value')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(images_dir / f'{scheme_name}_preview.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    print("Generating comparison images...")
    
    create_main_comparison()
    print("✓ Main comparison images created")
    
    create_matplotlib_comparison()
    print("✓ Matplotlib comparison images created")
    
    create_seaborn_comparison()
    print("✓ Seaborn comparison images created")
    
    create_scheme_previews()
    print("✓ Scheme preview images created")
    
    print(f"\nAll images saved to: {images_dir.absolute()}")
    print("\nGenerated files:")
    for img_file in sorted(images_dir.glob("*.png")):
        print(f"  - {img_file.name}")
