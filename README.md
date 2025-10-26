

<p align="center">
  <img src="https://raw.githubusercontent.com/HzaCode/Huez/main/logo.png" alt="Huez Logo" width="200"/>
</p>

<h1 align="center">Huez</h1>

<p align="center">
  <strong>An Intelligent Color Management System for Python Visualization</strong>
  <br />
  <em>Automatic • Consistent • Accessible • Smart</em>
</p>

<p align="center">
  <!-- PyOpenSci/JOSS-specific badges should be added after acceptance -->
  <a href="https://github.com/HzaCode/Huez/actions/workflows/tests.yml">
    <img src="https://github.com/HzaCode/Huez/actions/workflows/tests.yml/badge.svg" alt="CI Tests"/>
  </a>
  <a href="https://github.com/HzaCode/Huez/actions/workflows/docs.yml">
    <img src="https://github.com/HzaCode/Huez/actions/workflows/docs.yml/badge.svg" alt="Docs"/>
  </a>
  <a href="https://pypi.org/project/huez/">
    <img src="https://img.shields.io/pypi/v/huez?color=blue" alt="PyPI Version"/>
  </a>
  <a href="https://pepy.tech/project/huez">
    <img src="https://img.shields.io/pepy/dt/huez?style=flat-square&color=306998&label=Downloads" alt="Total Downloads"/>
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"/>
  <img src="https://img.shields.io/badge/status-pre--alpha-red.svg" alt="Status"/>
  <img src="https://img.shields.io/badge/linted%20with-ruff-000000.svg" alt="Ruff"/>
</p>

---

## Statement of Need

In scientific research, high-quality visualizations are crucial for clearly communicating findings. However, **poor color management can often undermine the story the data is telling**. Python users creating publication-quality figures commonly face several challenges:

- ❌ **Inconsistent Colors**: Maintaining a unified visual style is difficult when switching between libraries like `matplotlib`, `seaborn`, and `plotly`.
- ❌ **Manual Tweaking**: Each plot requires tedious manual color specification, a process that is both time-consuming and hard to reproduce.
- ❌ **Lack of Intelligent Tools**: There is a shortage of tools that automatically select appropriate colormaps (e.g., distinguishing between sequential and diverging data) or simulate for color vision deficiencies.
- ❌ **Accessibility Issues**: Approximately 8% of men have some form of color vision deficiency. Improper color choices can render plots uninterpretable to a significant portion of the audience.

## Huez: The Intelligent Solution

Huez addresses these problems through a simple API that automates the best practices of color management.

```bash
pip install huez
```

With a single line of code, you can establish a unified, intelligent, and adaptive color system for your entire visualization workflow.

```python
import huez as hz
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 🎨 Apply a theme with one line, automatically configuring multiple libraries
hz.use("scheme-1")

# --- Matplotlib & Seaborn automatically use consistent colors ---

# 1. Automatic color handling for scatter and line plots
# Huez intelligently expands the color palette when categories exceed the default
categories = [f'Type {i+1}' for i in range(15)]
for cat in categories:
    plt.plot(np.random.rand(10), label=cat)
plt.title("Huez Automatically Expands Discrete Colors")
plt.show()

# 2. Smart detection and application of the best colormap
# Data ranges from -1 to 1 (diverging)
correlation_data = np.random.rand(10, 10) * 2 - 1
sns.heatmap(correlation_data) # Huez auto-detects diverging data and applies "coolwarm"
plt.title("Huez Intelligently Detects a Diverging Colormap")
plt.show()
```

The core strengths of Huez are **automation** and **intelligence**, allowing it to handle the heavy lifting behind the scenes:

-   **Intelligent Color Expansion**: When the number of categories exceeds the palette's default color count, Huez interpolates in the perceptually uniform LAB color space to generate a new set of visually distinct colors.
-   **Smart Colormap Detection**: Automatically analyzes the data passed to `seaborn.heatmap` or `plt.imshow` to select the most appropriate colormap type (sequential, diverging, or cyclic).
-   **Cross-Library Consistency**: Ensures that `matplotlib`, `seaborn`, `plotly`, `altair`, and `plotnine` all share the same color and style configuration.
-   **Multi-Mode Output**: Provides color schemes optimized for **screen**, **print** (grayscale-friendly), and **presentation** (high-contrast).
-   **Built-in Accessibility**: All default schemes are designed to be friendly to viewers with common color vision deficiencies, ensuring your research is accessible to a wider audience.
-   **Academic Journal Styles**: Includes built-in color and style themes from top-tier journals (e.g., *Nature*, *Lancet*, *Science*), simplifying the publication process.

---

## 🎨 Core Features & Demonstrations

### 1️⃣ Intelligent Color Expansion (5 → 15 Colors)

<p align="center">
  <img src="https://raw.githubusercontent.com/HzaCode/Huez/main/comparison_color_expansion.png" alt="Color Expansion" width="85%"/>
</p>

**Problem**: Default palettes typically offer 5-10 colors. When plotting more categories, colors are recycled, causing confusion.
**Huez Solution**: Uses perceptually uniform interpolation in LAB space to generate a larger set of unique, easily distinguishable colors.

---

### 2️⃣ Smart Colormap Detection (Correlation Heatmap)

<p align="center">
  <img src="https://raw.githubusercontent.com/HzaCode/Huez/main/comparison_colormap_detection.png" alt="Colormap Detection" width="85%"/>
</p>

**Problem (Left)**: A sequential colormap (viridis) is used for a correlation matrix, which contains both positive and negative values. The visual center of the colormap does not align with the meaningful data center (0).
**Huez Solution (Right)**: Automatically detects that the data is diverging and applies a diverging colormap (coolwarm), which is centered at 0 and uses symmetric colors.

---

### 3️⃣ Color Vision Deficiency Accessibility (Designing for 8% of the population)

<p align="center">
  <img src="https://raw.githubusercontent.com/HzaCode/Huez/main/comparison_colorblind_safety.png" alt="Colorblind Safety" width="85%"/>
</p>

**Simulated under Deuteranopia (red-green color blindness):**

-   **Before (Left)**: The default red and green colors become nearly indistinguishable.
-   **After (Right)**: Huez's colorblind-safe palette ensures all 8 categories remain distinct and clearly interpretable.

---

### 4️⃣ Print Mode: Grayscale Optimization

<p align="center">
  <img src="https://raw.githubusercontent.com/HzaCode/Huez/main/comparison_print_mode.png" alt="Print Mode" width="85%"/>
</p>

**When the plot is printed in black and white:**

-   **Before (Left)**: Colors designed for screens may convert to very similar grayscale luminance values, making lines merge together.
-   **After (Right)**: `mode="print"` selects colors that are well-separated in their grayscale equivalents, ensuring clarity in print.

---

## 🔍 Usage Guide

### Preview & Quality Checks

Before applying a scheme, you can preview its colors and check its properties.

```python
import huez as hz

# Interactively preview a color scheme
hz.preview("scheme-1")

# Preview the scheme's appearance in print mode
hz.preview("scheme-1", mode="print")

# List all available built-in schemes
schemes = hz.list_schemes()
print(schemes)
# Output: ['scheme-1', 'scheme-2', 'lancet', 'nejm', ...]

# Enforce color vision deficiency safety
# This will raise an error if the selected scheme is not accessible
hz.use("scheme-1", ensure_accessible=True)
```

<details>
<summary>📚 <b>Supported Libraries</b></summary>

Huez seamlessly integrates with the following major Python visualization libraries:

-   **Matplotlib**: `plt.plot()`, `plt.scatter()`, etc.
-   **Seaborn**: `sns.scatterplot()`, `sns.heatmap()`, etc.
-   **plotnine**: `(ggplot(...) + geom_point())`, etc.
-   **Altair**: `alt.Chart(...).encode(color=...)`, etc.
-   **Plotly**: `go.Figure()` and `plotly.express`, etc.

</details>

<details>
<summary>🎨 <b>Custom Schemes</b></summary>

You can create or override schemes using a simple YAML configuration file.

**1. Create `my_config.yaml`:**

```yaml
version: 1
default_scheme: my_custom_scheme
schemes:
  my_custom_scheme:
    title: "My Custom Style"
    fonts: { family: "Arial", size: 10 }
    palettes:
      discrete: "okabe-ito"  # Use a built-in colorblind-safe palette
      sequential: "viridis"
      diverging: "coolwarm"
    style: { grid: "y", legend_loc: "best" }
```

**2. Load and use:**

```python
import huez as hz

hz.load_config("my_config.yaml")
hz.use("my_custom_scheme")
```

</details>

<details>
<summary>🆚 <b>Comparison with Other Tools</b></summary>

| Feature | Huez | palettable | seaborn | plotly | colorcet |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cross-Library Unification** | ✅ 5 Libraries | ❌ | ❌ | ❌ | ❌ |
| **Intelligent Color Expansion** | ✅ LAB Space | ❌ | ❌ | ❌ | ❌ |
| **Smart Colormap Detection** | ✅ Automatic | ❌ | ❌ | ❌ | ❌ |
| **CVD Safety Checks** | ✅ Built-in | ❌ | ❌ | ❌ | ❌ |
| **One-Line Global Setup** | ✅ `hz.use()` | ❌ | 🟡 | 🟡 | ❌ |
| **Academic Journal Styles** | ✅ 6+ | 🟡 | ❌ | ❌ | ❌ |

**Huez's unique contribution is its built-in intelligence layer that automates adaptation to data and context.**

</details>

---

## 🤝 Contributing

Contributions are welcome! If you have ideas, suggestions, or bug reports, please feel free to open an Issue or submit a Pull Request.

This project is committed to fostering an open and welcoming environment.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

<div align="center">

---

**Making Scientific Visualization Simpler and More Robust.**

**⭐ Star us on GitHub if Huez saves you time!**

</div>
