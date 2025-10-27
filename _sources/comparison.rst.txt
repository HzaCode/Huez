Comparison with Other Tools
============================

This page compares Huez with other popular color management tools and explains why Huez offers unique advantages for scientific visualization.

Quick Comparison
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 16 16 16 16 16

   * - Feature
     - **Huez**
     - seaborn
     - palettable
     - matplotlib
     - colorcet
   * - **Cross-library unification**
     - ✅ 5 libraries
     - ❌ Seaborn only
     - ❌ Manual
     - ❌ Matplotlib only
     - ❌ Manual
   * - **Intelligent color expansion**
     - ✅ LAB space
     - 🟡 Simple cycle
     - ❌ None
     - 🟡 Simple cycle
     - ❌ None
   * - **Smart colormap detection**
     - ✅ Automatic
     - ❌ Manual
     - ❌ Manual
     - ❌ Manual
     - ❌ Manual
   * - **Colorblind safety check**
     - ✅ 3 CVD types
     - ❌ None
     - ❌ None
     - ❌ None
     - ❌ None
   * - **One-line setup**
     - ✅ ``hz.use()``
     - 🟡 Partial
     - ❌ Per-plot
     - 🟡 Partial
     - ❌ Per-plot
   * - **Print optimization**
     - ✅ mode="print"
     - ❌ None
     - ❌ None
     - ❌ None
     - ❌ None
   * - **Academic journal styles**
     - ✅ 6+ journals
     - ❌ None
     - 🟡 Some
     - ❌ None
     - ❌ None
   * - **Context manager**
     - ✅ ``hz.using()``
     - ❌ None
     - ❌ None
     - 🟡 plt.style
     - ❌ None

**Legend:** ✅ Full support | 🟡 Partial support | ❌ Not supported

---

Detailed Comparisons
--------------------

Huez vs Seaborn
^^^^^^^^^^^^^^^

**Seaborn Approach:**

.. code-block:: python

   import seaborn as sns
   import matplotlib.pyplot as plt
   
   # Set palette (seaborn only)
   sns.set_palette("deep")
   
   # Works for seaborn
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   
   # But matplotlib needs separate configuration
   plt.plot(x, y)  # Uses default colors, not "deep"
   
   # Plotly needs yet another configuration
   import plotly.graph_objects as go
   fig = go.Figure()  # Doesn't use "deep" palette

**Limitations:**

- ❌ Only affects seaborn plots
- ❌ Matplotlib, plotly, altair need separate configuration
- ❌ No intelligent color expansion (just cycles colors)
- ❌ No automatic colormap detection for heatmaps
- ❌ No colorblind accessibility checking
- ❌ No print mode optimization

**Huez Approach:**

.. code-block:: python

   import huez as hz
   import seaborn as sns
   import matplotlib.pyplot as plt
   import plotly.graph_objects as go
   
   # One line for all libraries
   hz.use("scheme-1")
   
   # All use consistent colors automatically
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   plt.plot(x, y)
   fig = go.Figure(); fig.add_trace(go.Scatter(x=x, y=y))

**Advantages:**

- ✅ One setup for 5 libraries (matplotlib, seaborn, plotly, altair, plotnine)
- ✅ Intelligent LAB space color expansion for 15+ categories
- ✅ Automatic sequential/diverging colormap detection
- ✅ Built-in colorblind safety verification
- ✅ Print mode for grayscale-friendly colors
- ✅ Academic journal styles (Nature, Lancet, etc.)

**When to use seaborn:**

- You only use seaborn
- You need specific seaborn themes (darkgrid, whitegrid, etc.)

**When to use Huez:**

- You use multiple visualization libraries
- You need more than 10 distinct colors
- You want automatic colormap detection
- You need colorblind accessibility
- You're preparing figures for publication

**Best approach:** Use both!

.. code-block:: python

   import seaborn as sns
   import huez as hz
   
   sns.set_theme(style="whitegrid")  # Layout from seaborn
   hz.use("npg")                      # Colors from Huez

---

Huez vs Matplotlib Styles
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Matplotlib Style Approach:**

.. code-block:: python

   import matplotlib.pyplot as plt
   
   # Apply style
   plt.style.use('seaborn-v0_8')
   
   # Plot
   plt.plot(x, y)

**What matplotlib styles provide:**

- ✅ Figure aesthetics (grid, background, spines)
- ✅ Font settings
- ✅ Line widths, marker sizes
- 🟡 Basic color cycles

**What matplotlib styles DON'T provide:**

- ❌ Intelligent color expansion
- ❌ Colormap detection
- ❌ Colorblind checking
- ❌ Print optimization
- ❌ Cross-library consistency
- ❌ Academic journal styles

**Huez Approach:**

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   # Combine: matplotlib for layout, Huez for colors
   plt.style.use('seaborn-v0_8-whitegrid')
   hz.use("scheme-1", mode="print", ensure_accessible=True)
   
   plt.plot(x, y)

**Key Difference:**

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Aspect
     - Matplotlib Styles
     - Huez
   * - **Purpose**
     - Layout & aesthetics
     - Intelligent colors
   * - **Color management**
     - Static color cycle
     - Dynamic + intelligent
   * - **Multi-library**
     - Matplotlib only
     - 5 libraries
   * - **Accessibility**
     - None
     - Built-in checks
   * - **Best use**
     - Layout configuration
     - Color intelligence

**Recommendation:** Use matplotlib styles for layout, Huez for colors.

---

Huez vs palettable / colorbrewer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**palettable Approach:**

.. code-block:: python

   from palettable.cartocolors.qualitative import Bold_10
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # Get colors
   colors = Bold_10.hex_colors
   
   # Apply manually to each library
   plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
   sns.set_palette(colors)
   
   # Still need to configure plotly separately
   # No intelligent features
   
   # Plot
   plt.plot(x, y)

**What palettable provides:**

- ✅ Large collection of beautiful palettes (1000+)
- ✅ ColorBrewer, CartoDB, Tableau, etc.
- ✅ Well-tested color combinations

**What palettable DOESN'T provide:**

- ❌ Cross-library integration
- ❌ Automatic application
- ❌ Color expansion beyond palette size
- ❌ Colormap detection
- ❌ Accessibility checking
- ❌ Print optimization

**Huez Approach:**

.. code-block:: python

   import huez as hz
   
   # One line, all libraries
   hz.use("scheme-1", ensure_accessible=True)
   
   # Plot 15 categories - auto-expands from 8 base colors
   for i in range(15):
       plt.plot(x, y + i, label=f'Series {i}')

**Or combine palettable with Huez:**

.. code-block:: python

   from palettable.cartocolors.qualitative import Bold_10
   import huez as hz
   
   # Use palettable palette with Huez intelligence
   hz.use_palette(Bold_10.hex_colors, 
                  auto_expand=True,
                  ensure_accessible=True)

**Comparison:**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - palettable
     - Huez
   * - **Palette collection**
     - ✅ 1000+ palettes
     - 🟡 30+ palettes
   * - **Auto-application**
     - ❌ Manual setup
     - ✅ One line
   * - **Color expansion**
     - ❌ Fixed size
     - ✅ LAB interpolation
   * - **Accessibility**
     - ❌ None
     - ✅ Automatic checks
   * - **Multi-library**
     - ❌ Manual per library
     - ✅ 5 libraries
   * - **Intelligence**
     - ❌ Static palettes
     - ✅ Dynamic adaptation

**When to use palettable:**

- You need a specific palette from ColorBrewer/CartoDB
- You have fewer than 10 categories
- You don't need intelligent features

**When to use Huez:**

- You want one-line setup across all libraries
- You have 10+ categories
- You need automatic colormap detection
- You want accessibility checking
- You're preparing for publication

**Best approach:** Use palettable palettes with Huez intelligence!

---

Huez vs plotly / altair defaults
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Plotly Default:**

.. code-block:: python

   import plotly.graph_objects as go
   
   # Uses default plotly colors
   fig = go.Figure()
   for i in range(10):
       fig.add_trace(go.Scatter(x=x, y=y+i, name=f'Series {i}'))
   
   # Problems:
   # - Different from matplotlib/seaborn
   # - Colors repeat after 10
   # - No accessibility checks

**Altair Default:**

.. code-block:: python

   import altair as alt
   
   # Uses default Vega colors
   alt.Chart(df).mark_circle().encode(
       x='x:Q', y='y:Q', color='category:N'
   )
   
   # Problems:
   # - Different from other libraries
   # - Limited to 10 colors
   # - No intelligent expansion

**Huez Approach:**

.. code-block:: python

   import huez as hz
   import plotly.graph_objects as go
   import altair as alt
   
   # One setup for both
   hz.use("scheme-1")
   
   # Plotly uses Huez colors
   fig = go.Figure()
   for i in range(15):  # 15 categories, auto-expanded
       fig.add_trace(go.Scatter(x=x, y=y+i, name=f'Series {i}'))
   
   # Altair uses same colors
   alt.Chart(df).mark_circle().encode(x='x:Q', y='y:Q', color='category:N')

**Advantages:**

- ✅ Consistent colors across matplotlib, seaborn, plotly, altair, plotnine
- ✅ Automatic expansion beyond 10 categories
- ✅ Colorblind safety verification
- ✅ Print optimization
- ✅ No manual configuration per library

---

Huez vs colorcet
^^^^^^^^^^^^^^^^

**colorcet Approach:**

.. code-block:: python

   import colorcet as cc
   import matplotlib.pyplot as plt
   
   # Use perceptually uniform colormap
   plt.imshow(data, cmap=cc.cm.fire)

**What colorcet provides:**

- ✅ Perceptually uniform colormaps
- ✅ Great for heatmaps and images
- ✅ Many colormap variants

**What colorcet DOESN'T provide:**

- ❌ Discrete color palettes
- ❌ Cross-library integration
- ❌ Automatic colormap detection
- ❌ One-line setup
- ❌ Accessibility checking

**Huez Approach:**

.. code-block:: python

   import huez as hz
   import seaborn as sns
   
   hz.use("scheme-1")
   
   # Auto-detects data distribution
   sns.heatmap(correlation_data)  # Uses diverging colormap
   sns.heatmap(expression_data)   # Uses sequential colormap

**Comparison:**

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Feature
     - colorcet
     - Huez
   * - **Perceptual uniformity**
     - ✅ Excellent
     - ✅ LAB space
   * - **Discrete palettes**
     - ❌ None
     - ✅ Many
   * - **Auto-detection**
     - ❌ Manual
     - ✅ Automatic
   * - **Multi-library**
     - ❌ Manual
     - ✅ 5 libraries
   * - **Use case**
     - Heatmaps/images only
     - All plot types

**When to use colorcet:**

- You specifically need perceptually uniform continuous colormaps
- You're working only with heatmaps/images

**When to use Huez:**

- You need both discrete palettes and colormaps
- You want automatic colormap selection
- You use multiple plot types

---

Migration Guides
----------------

From Seaborn to Huez
^^^^^^^^^^^^^^^^^^^^

**Before (Seaborn only):**

.. code-block:: python

   import seaborn as sns
   import matplotlib.pyplot as plt
   
   sns.set_palette("deep")
   sns.set_context("paper")
   
   # Each library needs separate config
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   plt.plot(x, y)  # Doesn't use "deep" palette

**After (Huez):**

.. code-block:: python

   import seaborn as sns
   import matplotlib.pyplot as plt
   import huez as hz
   
   hz.use("scheme-1")
   sns.set_context("paper")  # Keep seaborn's layout settings
   
   # Both use consistent colors
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   plt.plot(x, y)

**Migration steps:**

1. Install Huez: ``pip install huez[all]``
2. Add ``import huez as hz`` at the top
3. Replace ``sns.set_palette()`` with ``hz.use()``
4. Remove manual color specifications

From Matplotlib Styles to Huez
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before:**

.. code-block:: python

   import matplotlib.pyplot as plt
   
   plt.style.use('seaborn-v0_8')
   plt.plot(x, y)

**After:**

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   plt.style.use('seaborn-v0_8-whitegrid')  # Keep for layout
   hz.use("scheme-1")                        # Add for colors
   
   plt.plot(x, y)

**What you gain:**

- Intelligent color expansion
- Automatic colormap detection
- Colorblind safety
- Print optimization
- Cross-library consistency

From Manual Color Configuration to Huez
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before (lots of manual work):**

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   import plotly.graph_objects as go
   
   # Manual configuration for each library
   colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F']
   
   plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
   sns.set_palette(colors)
   
   # Still need to configure plotly
   go.Figure(layout=dict(colorway=colors))
   
   # No expansion for 15+ categories
   # No accessibility checks
   # No print optimization

**After (one line):**

.. code-block:: python

   import huez as hz
   
   hz.use("scheme-1", mode="print", ensure_accessible=True)
   
   # Everything configured automatically
   # Works for matplotlib, seaborn, plotly, altair, plotnine
   # Auto-expands for 15+ categories
   # Accessibility checked
   # Print-optimized

**Lines of code:** 15+ → 1

**Time saved:** ~10 minutes per project

---

Why Choose Huez?
----------------

Choose Huez if you:
^^^^^^^^^^^^^^^^^^^

✅ Use **multiple visualization libraries** (matplotlib + seaborn + plotly)

✅ Plot **more than 10 categories** and need color expansion

✅ Want **automatic colormap detection** for heatmaps

✅ Need **colorblind accessibility** (8% of population)

✅ Prepare figures for **journal submission**

✅ Want **print-friendly** colors for B&W printing

✅ Need **consistent colors** across all your plots

✅ Value **time savings** (1 line vs 50 lines of config)

Continue using other tools if you:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Only use one library (matplotlib OR seaborn OR plotly)
- Have fewer than 10 categories
- Don't need accessibility checking
- Only create figures for screen viewing
- Prefer complete manual control

The Best Approach: Combine Tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**You don't have to choose one!** Huez works well with other tools:

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   from palettable.cartocolors.qualitative import Bold_10
   import huez as hz
   
   # matplotlib style for layout
   plt.style.use('seaborn-v0_8-whitegrid')
   
   # seaborn context for font sizes
   sns.set_context("paper", font_scale=1.2)
   
   # palettable for base colors
   base_colors = Bold_10.hex_colors
   
   # Huez for intelligence
   hz.use_palette(base_colors,
                  auto_expand=True,
                  ensure_accessible=True,
                  mode="print")
   
   # Now plot with all the benefits!
   plt.plot(x, y)

**Result:** Layout from matplotlib, sizing from seaborn, colors from palettable, intelligence from Huez!

---

Summary
-------

.. important::

   **Huez is not a replacement for other tools—it's an enhancement.**
   
   - Keep using matplotlib styles for layout
   - Keep using seaborn contexts for sizing
   - Keep using your favorite palettes
   
   **Add Huez for intelligent color management:**
   
   - One-line setup across all libraries
   - Automatic color expansion
   - Smart colormap detection
   - Colorblind safety verification
   - Print optimization

**The unique value of Huez:** It's the only tool that combines cross-library unification with built-in intelligence for automatic adaptation.

Next Steps
----------

- Try the :doc:`quickstart` to see Huez in action
- Read about :doc:`intelligence/index` features
- Check the :doc:`gallery/index` for visual comparisons
- See :doc:`faq` for common questions



