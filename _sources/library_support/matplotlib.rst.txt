Matplotlib
==========

Complete integration with matplotlib, the foundational plotting library for Python.

Basic Usage
-----------

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   hz.use("scheme-1")
   
   # Now all matplotlib plots use Huez colors
   plt.plot([1, 2, 3], [1, 4, 9], label='Data')
   plt.legend()
   plt.show()

What Huez Configures
--------------------

When you call ``hz.use()``, Huez sets:

- **Color cycle**: ``axes.prop_cycle``
- **Colormaps**: ``image.cmap`` (default colormap)
- **Figure settings**: DPI, facecolor, edgecolor
- **Font settings**: Family, size
- **Style settings**: Grid, legend, spines

You can still use matplotlib normally - Huez just sets better defaults.

Plot Types
----------

Line Plots
^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   
   # Multiple lines automatically get different colors
   plt.figure(figsize=(8, 5))
   plt.plot(x, y1, label='Series 1')
   plt.plot(x, y2, label='Series 2')
   plt.plot(x, y3, label='Series 3')
   plt.xlabel('X axis')
   plt.ylabel('Y axis')
   plt.legend()
   plt.show()

.. image:: /_static/comparison/matplotlib_huez_lines.png
   :width: 60%
   :align: center

|

Scatter Plots
^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   
   # Categorical scatter plot
   categories = ['A', 'B', 'C', 'D']
   colors = hz.palette()
   
   for i, cat in enumerate(categories):
       mask = df['category'] == cat
       plt.scatter(df[mask]['x'], df[mask]['y'], 
                   color=colors[i], label=cat, alpha=0.6)
   
   plt.legend()
   plt.show()

Bar Plots
^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   
   categories = ['A', 'B', 'C', 'D', 'E']
   values = [23, 45, 56, 78, 32]
   
   plt.bar(categories, values)
   plt.xlabel('Category')
   plt.ylabel('Value')
   plt.show()

Heatmaps (imshow)
^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   
   # Sequential data
   data = np.random.uniform(0, 100, (10, 10))
   plt.imshow(data, cmap=hz.cmap(kind="sequential"))
   plt.colorbar(label='Temperature (°C)')
   plt.show()
   
   # Diverging data
   correlation = np.corrcoef(np.random.randn(10, 100))
   plt.imshow(correlation, cmap=hz.cmap(kind="diverging"), 
              vmin=-1, vmax=1)
   plt.colorbar(label='Correlation')
   plt.show()

Subplots
^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   
   fig, axes = plt.subplots(2, 2, figsize=(12, 10))
   
   # All subplots use consistent colors
   axes[0, 0].plot(x, y1, label='Data 1')
   axes[0, 0].plot(x, y2, label='Data 2')
   axes[0, 0].legend()
   axes[0, 0].set_title('Line Plot')
   
   axes[0, 1].scatter(x, y1, label='Data 1')
   axes[0, 1].scatter(x, y2, label='Data 2')
   axes[0, 1].legend()
   axes[0, 1].set_title('Scatter Plot')
   
   axes[1, 0].bar(['A', 'B', 'C'], [1, 2, 3])
   axes[1, 0].set_title('Bar Plot')
   
   axes[1, 1].hist(np.random.randn(1000), bins=30)
   axes[1, 1].set_title('Histogram')
   
   plt.tight_layout()
   plt.show()

Advanced Features
-----------------

Custom Color Cycles
^^^^^^^^^^^^^^^^^^^

Get colors for manual use:

.. code-block:: python

   hz.use("scheme-1")
   
   # Get current color cycle
   colors = hz.palette()
   
   # Use manually
   for i, color in enumerate(colors[:5]):
       plt.plot(x, y + i, color=color, label=f'Line {i+1}')

Colormaps
^^^^^^^^^

Access Huez colormaps:

.. code-block:: python

   # Sequential colormap
   cmap_seq = hz.cmap(kind="sequential")
   
   # Diverging colormap
   cmap_div = hz.cmap(kind="diverging")
   
   # Cyclic colormap
   cmap_cyc = hz.cmap(kind="cyclic")
   
   # Use in plots
   plt.imshow(data, cmap=cmap_seq)
   plt.contourf(X, Y, Z, cmap=cmap_div, levels=20)

Apply to Existing Figure
^^^^^^^^^^^^^^^^^^^^^^^^^

Apply Huez to already created figures:

.. code-block:: python

   # Create figure first
   # Set scheme first
   hz.use("lancet")
   
   fig, ax = plt.subplots()
   ax.plot(x, y1, label='Data 1')
   ax.plot(x, y2, label='Data 2')
   ax.legend()
   
   # Colors are automatically applied
   plt.show()

Context Manager
^^^^^^^^^^^^^^^

Temporary scheme changes:

.. code-block:: python

   hz.use("scheme-1")
   
   # Normal plot
   plt.figure()
   plt.plot(x, y1)
   plt.show()
   
   # Temporary different scheme
   with hz.using("lancet"):
       plt.figure()
       plt.plot(x, y2)
       plt.show()
   
   # Back to scheme-1
   plt.figure()
   plt.plot(x, y3)
   plt.show()

Best Practices
--------------

For Publications
^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("npg", mode="print", ensure_accessible=True)
   
   fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=300)
   ax.plot(x, y, linewidth=2, marker='o', markevery=5)
   ax.set_xlabel('X axis', fontsize=9)
   ax.set_ylabel('Y axis', fontsize=9)
   
   plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')

For Presentations
^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1", mode="presentation")
   
   fig, ax = plt.subplots(figsize=(12, 8))
   ax.plot(x, y, linewidth=4)
   ax.set_xlabel('X axis', fontsize=20)
   ax.set_ylabel('Y axis', fontsize=20)
   ax.set_title('Title', fontsize=24, fontweight='bold')
   
   plt.savefig('slide.png', dpi=150, bbox_inches='tight')

Combining with Styles
^^^^^^^^^^^^^^^^^^^^^

Combine Huez with matplotlib styles:

.. code-block:: python

   # Apply matplotlib style for layout
   plt.style.use('seaborn-v0_8-whitegrid')
   
   # Apply Huez for colors
   hz.use("scheme-1")
   
   # Now you have nice layout + professional colors
   plt.plot(x, y)

Troubleshooting
---------------

Colors Not Changing
^^^^^^^^^^^^^^^^^^^

Make sure to apply Huez **before** creating plots:

.. code-block:: python

   # ✅ Correct order
   hz.use("scheme-1")
   plt.plot(x, y)
   
   # ❌ Wrong order
   plt.plot(x, y)
   hz.use("scheme-1")  # Too late!

Explicit Colors Override
^^^^^^^^^^^^^^^^^^^^^^^^^

Explicit ``color`` parameter overrides Huez:

.. code-block:: python

   hz.use("scheme-1")
   
   # ❌ Explicit color overrides Huez
   plt.plot(x, y, color='red')
   
   # ✅ Let Huez assign color
   plt.plot(x, y)

Colormap Not Applied
^^^^^^^^^^^^^^^^^^^^

Use ``cmap`` parameter for heatmaps:

.. code-block:: python

   hz.use("scheme-1")
   
   # ✅ Correct
   plt.imshow(data, cmap=hz.cmap())
   
   # ❌ Uses default colormap
   plt.imshow(data)

API Reference
-------------

Matplotlib-specific functions:

.. code-block:: python

   # Get current matplotlib color cycle
   colors = hz.palette()
   
   # Get matplotlib colormap
   cmap = hz.cmap(kind="sequential")
   
   # Note: apply_to_figure() does not accept 'scheme' parameter
   # Use hz.use() to set scheme first
   hz.use("lancet")  # Set scheme globally

Next Steps
----------

- Check :doc:`seaborn` for enhanced features
- Read :doc:`../user_guide/best_practices` for tips
- Explore :doc:`../gallery/index` for examples


