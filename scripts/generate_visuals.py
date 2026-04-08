import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.colors import LinearSegmentedColormap

# --- 1. SET UP PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
funnel_path = os.path.join(BASE_DIR, '..', 'data', 'funnel_general.csv')
retention_path = os.path.join(BASE_DIR, '..', 'data', 'retention_cohort.csv')
visuals_dir = os.path.join(BASE_DIR, '..', 'visuals')

os.makedirs(visuals_dir, exist_ok=True)

# --- 2. GENERATE FUNNEL CHART (Monochromatic) ---
if os.path.exists(funnel_path):
    print("Reading funnel data...")
    funnel = pd.read_csv(funnel_path)
    
    plt.figure(figsize=(10, 6))
    stages = funnel.columns
    values = funnel.iloc[0].values
    
    # Create a monochromatic palette (Light to Dark)
    # Using Blues_r (reversed) so the top (Select Item) is light and bottom (Purchase) is dark
    mono_palette = sns.color_palette("Blues", n_colors=len(stages))
    
    sns.barplot(x=values, y=stages, hue=stages, palette=mono_palette, legend=False)
    
    plt.title('MercadoLibre: Purchase Funnel Conversion (%)', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Conversion Rate (%)', fontsize=12)
    plt.ylabel('Funnel Stage', fontsize=12)
    plt.xlim(0, 100)
    
    for i, v in enumerate(values):
        plt.text(v + 1, i, f"{v:.1f}%", va='center', fontweight='bold', color='#333333')
        
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'conversion_funnel.png'), dpi=300)
    print("✅ Success: conversion_funnel.png (Monochromatic) saved.")

# --- 3. GENERATE RETENTION HEATMAP (Green-Yellow-Red) ---
if os.path.exists(retention_path):
    print("Reading retention data...")
    retention = pd.read_csv(retention_path, index_col='cohort')
    
    plt.figure(figsize=(12, 8))
    
    # Custom Color Map: Green (High) -> Yellow (Mid) -> Red (Low)
    # We use 'RdYlGn' (Red-Yellow-Green) which is a standard Matplotlib divergent map
    # Since high numbers are "good", Green should be at the high end.
    
    sns.heatmap(retention, 
                annot=True, 
                fmt=".1f", 
                cmap='RdYlGn',  # Red for low, Green for high
                linewidths=.5, 
                cbar_kws={'label': 'Retention (%)'})
    
    plt.title('MercadoLibre: Monthly Cohort Retention Heatmap', fontsize=14, pad=20, fontweight='bold')
    plt.xlabel('Retention Period (Days)', fontsize=12)
    plt.ylabel('Registration Month (Cohort)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'retention_heatmap.png'), dpi=300)
    print("✅ Success: retention_heatmap.png (Green-Yellow-Red) saved.")