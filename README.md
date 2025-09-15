
<p align="center">
  <img src="logo.png" alt="Huez Logo" width="200"/>
</p>

<h1 align="center">Huez</h1>

<p align="center">
  <em>A Unified Color Scheme Solution for Python Visualization</em>
  <br />
  <a href="#features">✨ Features</a> •
  <a href="#installation">🚀 Quick Start</a> •
  <a href="#usage">📚 Libraries</a> •
  <a href="#schemes">🎨 Schemes</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"/>
  <img src="https://img.shields.io/badge/status-pre--alpha-red.svg" alt="Status"/>
</p>

<p align="center">
  <em>"Good visualizations should not be ruined by bad color schemes."</em>
</p>



**Huez** is a unified Python visualization color scheme solution that instantly upgrades your charts from amateur to professional publication-quality. 



</div>

## ✨ Features

- 🚀 **True Automatic Coloring**: All major libraries support native syntax automatic coloring, no manual color specification needed
- 🎯 **Perfect Cross-Library Consistency**: Matplotlib, Seaborn, plotnine, Altair, Plotly completely unified color experience
- 🎨 **Rich Built-in & Custom Schemes**: Professional academic palettes plus easy custom scheme creation and loading
- ⚡ **Zero Learning Cost**: Use native syntax of each library, no need to learn additional APIs
- 🔧 **One Line Does It All**: Just `hz.use("scheme-1")` to enable automatic coloring for all libraries

## 🎯 Before & After Comparison

See the dramatic improvement Huez brings to your visualizations:

### Default vs Huez Enhanced

<div align="center">

| Before (Default Colors) | After (Huez Enhanced) |
|:------------------------:|:---------------------:|
| ![Before](images/before_default.png) | ![After](images/after_huez.png) |
| *Bland default colors* | *Professional publication-ready* |

</div>

### Multiple Library Consistency

<div align="center">

| Library | Before | After |
|:-------:|:------:|:-----:|
| **Matplotlib** | ![MPL Before](images/mpl_before.png) | ![MPL After](images/mpl_after.png) |
| **Seaborn** | ![SNS Before](images/sns_before.png) | ![SNS After](images/sns_after.png) |
| **Plotnine** | ![P9 Before](images/p9_before.png) | ![P9 After](images/p9_after.png) |

*All libraries now share the same beautiful, consistent color scheme*

</div>

### 🎨 Color Scheme Gallery

<div align="center">

| Scheme | Preview | Best For |
|:------:|:-------:|:--------:|
| **scheme-1** | ![Scheme 1](images/scheme1_preview.png) | General purpose, presentations |
| **lancet** | ![Lancet](images/lancet_preview.png) | Medical publications |
| **nature** | ![Nature](images/nature_preview.png) | Scientific journals |
| **nejm** | ![NEJM](images/nejm_preview.png) | Clinical research |

</div>

> 📸 **Note**: To see these comparison images, please generate sample plots using the provided examples below. The images directory structure is ready for your visualization outputs.

## 🚀 Quick Start

### Installation

```bash
pip install huez
```

### Basic Usage

```python
import huez as hz

# 🎨 One line of code, global coloring
hz.use("scheme-1")

# ✨ Now all libraries automatically color using native syntax!
```

## 📚 Supported Visualization Libraries

**Matplotlib**

```python
import matplotlib.pyplot as plt
plt.plot(x, y1, label='Data 1')  # Pure native syntax - colors auto-applied!
plt.plot(x, y2, label='Data 2')  # Pure native syntax - colors auto-applied!
plt.legend()
```

**Seaborn**

```python
import seaborn as sns
sns.scatterplot(data=df, x='x', y='y', hue='category')  # Pure native syntax - colors auto-applied!
```

**plotnine**

```python
from plotnine import *
(ggplot(df, aes('x', 'y', color='category')) + 
 geom_point())  # Pure native syntax - colors auto-applied!
```

**Altair**

```python
import altair as alt
alt.Chart(df).mark_circle().encode(
    x='x:Q', y='y:Q', color='category:N'  # Pure native syntax - colors auto-applied!
)
```

**Plotly**

```python
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, name='Data'))  # Pure native syntax - colors auto-applied!
```

## 🎨 Rich Built-in & Custom Schemes

Huez comes with a rich collection of **professional color schemes** and supports **easy customization**:



### ✨ Custom Schemes
```python
# Switch between built-in schemes
hz.use("lancet")  # Academic journal style
hz.use("scheme-2")  # Alternative color palette

# Load custom configuration file
hz.load_config("my_custom_config.yaml")
hz.use("my_custom_scheme")
```

**Create custom config file (my_custom_config.yaml):**
```yaml
version: 1
default_scheme: my_custom_scheme
schemes:
  my_custom_scheme:
    title: "My Custom Style"
    fonts: { family: "DejaVu Sans", size: 10 }
    palettes:
      discrete: "npg"
      sequential: "viridis"
      diverging: "coolwarm"
      cyclic: "twilight"
    figure: { dpi: 300 } # Set project-wide DPI, size is controlled in code
    style: { grid: "y", legend_loc: "best", spine_top_right_off: true }
```
## 🔧 How Huez Works

**Huez takes over color management for your visualizations.** To use Huez effectively:

- **Remove explicit color parameters** from your plotting code (e.g., `color='red'`, `palette=['blue', 'green']`)
- **Let Huez handle colors automatically** through its unified schemes
- **Switch between different journal styles** without changing your code logic
- **Huez only affects global defaults** - it doesn't interfere with explicit local color settings when you need them

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

---



⭐ **If this project helps you, please give us a star!** ⭐

</div>




