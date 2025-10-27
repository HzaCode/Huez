Quick Start
===========

Get up and running with Huez in 5 minutes!

Installation
------------

First, install Huez:

.. code-block:: bash

   pip install huez[all]

Basic Usage
-----------

The simplest way to use Huez:

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz

   # Apply a color scheme
   hz.use("scheme-1")

   # Now all your plots use consistent, professional colors
   plt.plot([1, 2, 3], [1, 4, 9], label='Data')
   plt.legend()
   plt.show()

That's it! Huez automatically configures matplotlib (and other libraries) with professional colors.

Cross-Library Consistency
--------------------------

Huez works seamlessly across multiple visualization libraries:

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   import plotly.graph_objects as go
   import huez as hz

   # One line setup for all libraries
   hz.use("scheme-1")

   # Matplotlib
   plt.figure(figsize=(10, 4))
   plt.subplot(1, 2, 1)
   plt.plot(x, y1, label='Series 1')
   plt.plot(x, y2, label='Series 2')
   plt.legend()
   plt.title('Matplotlib')

   # Seaborn
   plt.subplot(1, 2, 2)
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   plt.title('Seaborn')

   plt.tight_layout()
   plt.show()

   # Plotly (uses the same colors!)
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=x, y=y1, name='Series 1'))
   fig.add_trace(go.Scatter(x=x, y=y2, name='Series 2'))
   fig.show()

Different Modes
---------------

Huez supports three modes for different output media:

**Screen Mode (default):**

.. code-block:: python

   hz.use("scheme-1", mode="screen")
   # Optimized for digital displays

**Print Mode (grayscale-friendly):**

.. code-block:: python

   hz.use("scheme-1", mode="print")
   # Optimized for black & white printing

**Presentation Mode (high contrast):**

.. code-block:: python

   hz.use("scheme-1", mode="presentation")
   # Optimized for projectors and large screens

.. image:: _static/features/comparison_print_mode.png
   :width: 80%
   :align: center
   :alt: Print mode comparison

|

Preview Before Applying
-----------------------

Preview a color scheme before using it:

.. code-block:: python

   # Preview scheme colors
   hz.preview("scheme-1")

   # Preview in different mode
   hz.preview("scheme-1", mode="print")

   # List all available schemes
   schemes = hz.list_schemes()
   print(schemes)
   # ['scheme-1', 'scheme-2', 'scheme-3', 'lancet', 'nejm', 'npg', ...]

Using Journal Styles
--------------------

Huez includes professional color schemes from academic journals:

.. code-block:: python

   # Nature Publishing Group style
   hz.use("npg")

   # Lancet journal style
   hz.use("lancet")

   # New England Journal of Medicine
   hz.use("nejm")

   # Science/AAAS style
   hz.use("aaas")

Intelligent Features
--------------------

Huez includes smart features that work automatically:

**Color Expansion**

When you plot many categories, Huez automatically expands the color palette:

.. code-block:: python

   hz.use("scheme-1")

   # Plot 15 series - Huez generates 15 distinct colors automatically
   for i in range(15):
       plt.plot(x, y + i*0.5, label=f'Series {i+1}')
   plt.legend()
   plt.show()

.. image:: _static/features/comparison_color_expansion.png
   :width: 80%
   :align: center
   :alt: Color expansion comparison

|

**Smart Colormap Detection**

Huez automatically detects whether to use sequential or diverging colormaps:

.. code-block:: python

   import seaborn as sns
   import numpy as np

   hz.use("scheme-1")

   # Correlation matrix (-1 to 1) → automatically uses diverging colormap
   correlation = np.corrcoef(np.random.randn(10, 100))
   sns.heatmap(correlation)
   plt.show()

   # Temperature data (0 to 100) → automatically uses sequential colormap
   temperature = np.random.uniform(0, 100, (10, 10))
   sns.heatmap(temperature)
   plt.show()

.. image:: _static/features/comparison_colormap_detection.png
   :width: 80%
   :align: center
   :alt: Colormap detection comparison

|

**Colorblind Safety**

Check if your colors are colorblind-safe:

.. code-block:: python

   # Ensure colorblind accessibility
   hz.use("scheme-1", ensure_accessible=True)

   # Or check manually
   result = hz.check_accessibility("npg")
   if not result['safe']:
       print(result['warnings'])
       print(result['suggestions'])

.. image:: _static/features/comparison_colorblind_safety.png
   :width: 80%
   :align: center
   :alt: Colorblind safety comparison

|

Temporary Scheme Changes
-------------------------

Use a context manager for temporary scheme changes:

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   import huez as hz
   
   x = np.linspace(0, 10, 100)
   y1 = np.sin(x)
   y2 = np.cos(x)
   y3 = np.sin(x) * np.cos(x)
   
   # Default scheme
   hz.use("scheme-1")
   plt.figure()
   plt.plot(x, y1, label='Sine')
   plt.legend()
   plt.title('Using scheme-1')
   plt.show()

   # Temporarily use a different scheme
   with hz.using("lancet"):
       plt.figure()
       plt.plot(x, y2, label='Cosine')
       plt.legend()
       plt.title('Using lancet (temporary)')
       plt.show()

   # Back to scheme-1 automatically
   plt.figure()
   plt.plot(x, y3, label='Sine*Cosine')
   plt.legend()
   plt.title('Back to scheme-1')
   plt.show()

Getting Colors Directly
------------------------

Get colors for manual use:

.. code-block:: python

   import huez as hz
   
   # Set active scheme first
   hz.use("scheme-1")
   
   # Get the current palette
   colors = hz.palette()
   print(colors)  # ['#E64B35', '#4DBBD5', '#00A087', ...]

   # Get a specific colormap
   cmap = hz.cmap(kind="diverging")
   # Use with matplotlib: plt.imshow(data, cmap=cmap)

   # Get colors for specific number of categories (three ways):
   colors_10a = hz.palette(n=10)      # Traditional
   colors_10b = hz.colors(10)          # Simplified (recommended)
   colors_10c = hz.get_colors(n=10)   # Alias
   
   # All three return the same result
   print(len(colors_10a))  # 10

Best Practices
--------------

.. tip::

   **Let Huez Handle Colors Automatically**
   
   Avoid explicit color parameters (``color='red'``, ``cmap='viridis'``) to enable
   intelligent adaptation.

**Correct Usage:**

.. code-block:: python

   hz.use("scheme-1")
   
   # ✅ Good: Let Huez assign colors
   plt.plot(x, y1, label='Series 1')
   plt.plot(x, y2, label='Series 2')
   
   # ✅ Good: Let Huez detect colormap type
   sns.heatmap(correlation_data)

**Incorrect Usage:**

.. code-block:: python

   hz.use("scheme-1")
   
   # ❌ Wrong: Explicit color overrides Huez
   plt.plot(x, y1, color='red')
   
   # ❌ Wrong: Explicit colormap bypasses auto-detection
   sns.heatmap(data, cmap='viridis')

Next Steps
----------

- Read the :doc:`user_guide/index` for detailed tutorials
- Explore :doc:`intelligence/index` to learn about smart features
- Browse the :doc:`gallery/index` for visual examples
- Check the :doc:`api/index` for complete API reference

Common Workflows
----------------

**For Publications:**

.. code-block:: python

   # Use journal style and ensure colorblind safety
   hz.use("npg", mode="print", ensure_accessible=True)

**For Presentations:**

.. code-block:: python

   # Use high contrast mode
   hz.use("scheme-1", mode="presentation")

**For Exploratory Analysis:**

.. code-block:: python

   # Quick setup with defaults
   hz.quick_setup()  # Equivalent to hz.use("scheme-1")

Need Help?
----------

- 📖 Read the full :doc:`user_guide/index`
- 🐛 Report bugs on `GitHub Issues <https://github.com/hzacode/huez/issues>`_
- 💬 Ask questions in `Discussions <https://github.com/hzacode/huez/discussions>`_


