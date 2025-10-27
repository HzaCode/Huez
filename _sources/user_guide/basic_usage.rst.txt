Basic Usage
===========

This page covers the fundamental ways to use Huez in your visualization workflows.

The One-Line Setup
------------------

The simplest way to use Huez is with a single line:

.. code-block:: python

   import huez as hz
   
   hz.use("scheme-1")

After this line, all your plots will automatically use consistent, professional colors across different visualization libraries.

Applying Schemes
----------------

Huez comes with several built-in schemes:

**Default Schemes:**

.. code-block:: python

   hz.use("scheme-1")  # Default scheme 1
   hz.use("scheme-2")  # Alternative scheme 2
   hz.use("scheme-3")  # Alternative scheme 3

**Journal Styles:**

.. code-block:: python

   hz.use("npg")     # Nature Publishing Group
   hz.use("lancet")  # The Lancet
   hz.use("nejm")    # New England Journal of Medicine
   hz.use("aaas")    # Science/AAAS
   hz.use("jama")    # JAMA
   hz.use("bmj")     # BMJ

**Colorblind-Safe Schemes:**

.. code-block:: python

   hz.use("okabe-ito")          # Okabe-Ito palette (8 colors)
   hz.use("paul-tol-bright")    # Paul Tol Bright (7 colors)
   hz.use("paul-tol-vibrant")   # Paul Tol Vibrant (7 colors)

Listing Available Schemes
--------------------------

To see all available schemes:

.. code-block:: python

   schemes = hz.list_schemes()
   print(schemes)

Output:

.. code-block:: text

   ['scheme-1', 'scheme-2', 'scheme-3', 'npg', 'aaas', 'nejm', 'lancet', 
    'jama', 'bmj', 'okabe-ito', 'paul-tol-bright', 'paul-tol-vibrant']

Previewing Schemes
------------------

Preview a scheme before applying it:

.. code-block:: python

   # Show color palette
   hz.preview("scheme-1")
   
   # Preview with different mode
   hz.preview("lancet", mode="print")

This opens a window showing:

- Discrete color palette (for categorical data)
- Sequential colormap (for continuous data)
- Diverging colormap (for data centered at zero)
- Example plots

Using with Different Libraries
-------------------------------

Matplotlib
^^^^^^^^^^

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   hz.use("scheme-1")
   
   # Line plots
   plt.plot(x, y1, label='Data 1')
   plt.plot(x, y2, label='Data 2')
   plt.legend()
   plt.show()
   
   # Scatter plots
   plt.scatter(x, y, c=categories)
   plt.colorbar()
   plt.show()

.. image:: /_static/comparison/matplotlib_huez_lines.png
   :width: 60%
   :align: center

|

Seaborn
^^^^^^^

.. code-block:: python

   import seaborn as sns
   import huez as hz
   
   hz.use("scheme-1")
   
   # Categorical plots
   sns.boxplot(data=df, x='category', y='value')
   
   # Heatmaps (colormap auto-detected)
   sns.heatmap(correlation_matrix)
   
   # Scatter plots with hue
   sns.scatterplot(data=df, x='x', y='y', hue='category')

.. image:: /_static/comparison/seaborn_huez_lines.png
   :width: 60%
   :align: center

|

Plotly
^^^^^^

.. code-block:: python

   import plotly.graph_objects as go
   import plotly.express as px
   import huez as hz
   
   hz.use("scheme-1")
   
   # Plotly Graph Objects
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=x, y=y1, name='Data 1'))
   fig.add_trace(go.Scatter(x=x, y=y2, name='Data 2'))
   fig.show()
   
   # Plotly Express
   fig = px.scatter(df, x='x', y='y', color='category')
   fig.show()

.. image:: /_static/comparison/plotly_huez_scatter.png
   :width: 60%
   :align: center

|

Altair
^^^^^^

.. code-block:: python

   import altair as alt
   import huez as hz
   
   hz.use("scheme-1")
   
   chart = alt.Chart(df).mark_circle().encode(
       x='x:Q',
       y='y:Q',
       color='category:N'
   )
   chart.show()

.. image:: /_static/comparison/altair_huez_bars.png
   :width: 60%
   :align: center

|

plotnine (ggplot2 for Python)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from plotnine import *
   import huez as hz
   
   hz.use("scheme-1")
   
   (ggplot(df, aes('x', 'y', color='category'))
    + geom_point()
    + theme_minimal())

.. image:: /_static/comparison/plotnine_huez_bars.png
   :width: 60%
   :align: center

|

Getting Colors Manually
------------------------

Sometimes you need to access colors directly:

**Get Current Palette:**

.. code-block:: python

   colors = hz.palette()
   print(colors)
   # ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', ...]

**Get Specific Number of Colors:**

.. code-block:: python

   hz.use("scheme-1")
   
   # Get 10 colors (automatically expands if needed)
   # Three equivalent ways:
   colors = hz.palette(n=10)      # Traditional
   colors = hz.colors(10)          # Simplified (recommended)
   colors = hz.get_colors(n=10)   # Alias

**Get Colormaps:**

.. code-block:: python

   # Get sequential colormap
   cmap_seq = hz.cmap(kind="sequential")
   
   # Get diverging colormap
   cmap_div = hz.cmap(kind="diverging")
   
   # Get cyclic colormap
   cmap_cyc = hz.cmap(kind="cyclic")
   
   # Use with matplotlib
   plt.imshow(data, cmap=cmap_seq)

**For plotnine (ggplot2):**

.. code-block:: python

   from plotnine import *
   
   hz.use("scheme-1")
   scales = hz.gg_scales()
   
   (ggplot(df, aes('x', 'y', color='category'))
    + geom_point()
    + scales['color_discrete'])

Context Manager
---------------

Use a scheme temporarily with a context manager:

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   import huez as hz
   
   x = np.linspace(0, 10, 100)
   y1 = np.sin(x)
   y2 = np.cos(x)
   y3 = np.tan(x)
   
   hz.use("scheme-1")
   
   # Create plot with scheme-1
   plt.figure()
   plt.plot(x, y1, label='Data 1')
   plt.legend()
   plt.title('scheme-1')
   plt.show()
   
   # Temporarily use different scheme
   with hz.using("lancet"):
       plt.figure()
       plt.plot(x, y2, label='Data 2')
       plt.legend()
       plt.title('lancet (temporary)')
       plt.show()
   
   # Back to scheme-1 automatically
   plt.figure()
   plt.plot(x, y3, label='Data 3')
   plt.legend()
   plt.title('Back to scheme-1')
   plt.show()

Checking Current Scheme
------------------------

Check which scheme is currently active:

.. code-block:: python

   current = hz.current_scheme()
   print(current)  # 'scheme-1'
   
   # Or get full status
   status = hz.status()
   print(status)

Applying to Existing Figures
-----------------------------

Apply Huez colors to an already created figure:

.. code-block:: python

   # Set scheme first
   hz.use("lancet")
   
   # Create figure
   fig, ax = plt.subplots()
   ax.plot(x, y1, label='Data 1')
   ax.plot(x, y2, label='Data 2')
   ax.legend()
   
   # Colors are automatically applied
   plt.show()

.. note::

   The ``apply_to_figure()`` function is for applying colors to figure objects
   from different libraries. It does not accept a ``scheme`` parameter.
   Always call ``hz.use(scheme_name)`` first to set the active scheme.

Quick Setup
-----------

For quick exploratory analysis, use ``quick_setup()``:

.. code-block:: python

   import huez as hz
   
   # Equivalent to hz.use("scheme-1")
   hz.quick_setup()

Tips
----

.. tip::

   **Avoid Explicit Color Parameters**
   
   Let Huez assign colors automatically. Avoid using explicit ``color`` or ``cmap``
   parameters to enable intelligent features like color expansion and colormap detection.

.. note::

   **Theme vs. Colors**
   
   Huez only manages colors, not other style elements like fonts or line widths.
   Use it in combination with matplotlib styles or seaborn themes:
   
   .. code-block:: python
   
      plt.style.use('seaborn-v0_8-whitegrid')
      hz.use("scheme-1")

Common Patterns
---------------

**Publication Workflow:**

.. code-block:: python

   import huez as hz
   import matplotlib.pyplot as plt
   
   # Setup for publication
   hz.use("npg", mode="print", ensure_accessible=True)
   
   # High DPI for publication quality
   plt.figure(dpi=300, figsize=(6, 4))
   plt.plot(x, y)
   plt.savefig('figure.png', dpi=300, bbox_inches='tight')

**Presentation Workflow:**

.. code-block:: python

   # High contrast for projectors
   hz.use("scheme-1", mode="presentation")
   
   # Larger figure size
   plt.figure(figsize=(12, 8))

**Multi-Panel Figures:**

.. code-block:: python

   hz.use("scheme-1")
   
   fig, axes = plt.subplots(2, 2, figsize=(12, 10))
   
   # All panels use consistent colors automatically
   axes[0, 0].plot(x, y1)
   axes[0, 1].scatter(x, y2)
   # ... and so on

Next Steps
----------

- Learn about :doc:`color_modes` for different output media
- Explore :doc:`custom_schemes` to create your own configurations
- Read :doc:`best_practices` for professional visualizations
- Check out :doc:`../intelligence/index` for intelligent features


