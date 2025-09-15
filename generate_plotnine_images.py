#!/usr/bin/env python3
"""
Generate plotnine comparison images for README.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# Create sample data
np.random.seed(42)
n = 100
df = pd.DataFrame({
    'x': np.random.randn(n),
    'y': np.random.randn(n),
    'category': np.random.choice(['A', 'B', 'C', 'D'], n)
})

images_dir = Path("images")

def create_plotnine_style_comparison():
    """Create plotnine-style comparison using matplotlib."""
    
    # Before (default ggplot2-style colors)
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Default ggplot2 colors (approximation)
    default_colors = ['#F8766D', '#00BA38', '#619CFF', '#C77CFF']
    categories = df['category'].unique()
    
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        ax.scatter(data['x'], data['y'], label=f'Category {cat}', 
                  color=default_colors[i], alpha=0.7, s=50)
    
    ax.set_xlabel('X Value')
    ax.set_ylabel('Y Value')
    ax.set_title('Plotnine/ggplot2 - Default Colors')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('white')
    
    plt.tight_layout()
    plt.savefig(images_dir / 'p9_before.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # After (professional colors)
    fig, ax = plt.subplots(figsize=(8, 6))
    professional_colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']
    
    for i, cat in enumerate(categories):
        data = df[df['category'] == cat]
        ax.scatter(data['x'], data['y'], label=f'Category {cat}', 
                  color=professional_colors[i], alpha=0.8, s=50)
    
    ax.set_xlabel('X Value')
    ax.set_ylabel('Y Value')
    ax.set_title('Plotnine/ggplot2 - Huez Enhanced')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('white')
    
    plt.tight_layout()
    plt.savefig(images_dir / 'p9_after.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating plotnine comparison images...")
    create_plotnine_style_comparison()
    print("✓ Plotnine comparison images created")
