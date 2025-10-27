Library Support
===============

Huez seamlessly integrates with 5 major Python visualization libraries.

.. toctree::
   :maxdepth: 2
   
   matplotlib
   seaborn
   plotly
   altair
   plotnine

Supported Libraries
-------------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Matplotlib
      :link: matplotlib
      :link-type: doc
      
      The foundational plotting library for Python.
      
      **Support**: Full ✓

   .. grid-item-card:: Seaborn
      :link: seaborn
      :link-type: doc
      
      Statistical data visualization built on matplotlib.
      
      **Support**: Full ✓ + Enhanced features

   .. grid-item-card:: Plotly
      :link: plotly
      :link-type: doc
      
      Interactive web-based visualizations.
      
      **Support**: Full ✓

   .. grid-item-card:: Altair
      :link: altair
      :link-type: doc
      
      Declarative visualization based on Vega-Lite.
      
      **Support**: Full ✓

   .. grid-item-card:: plotnine
      :link: plotnine
      :link-type: doc
      
      Grammar of Graphics for Python (ggplot2 port).
      
      **Support**: Full ✓

Cross-Library Consistency
-------------------------

One line setup works across all libraries:

.. code-block:: python

   import huez as hz
   
   # One line for all libraries
   hz.use("scheme-1")
   
   # Matplotlib
   import matplotlib.pyplot as plt
   plt.plot(x, y)
   
   # Seaborn
   import seaborn as sns
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   
   # Plotly
   import plotly.express as px
   px.scatter(df, x='x', y='y', color='category')
   
   # Altair
   import altair as alt
   alt.Chart(df).mark_point().encode(x='x', y='y', color='category')
   
   # plotnine
   from plotnine import *
   (ggplot(df, aes('x', 'y', color='category')) + geom_point())

All use the same colors automatically!

Installation
------------

Install with specific library support:

.. code-block:: bash

   # Individual libraries
   pip install huez[matplotlib]
   pip install huez[seaborn]
   pip install huez[plotly]
   pip install huez[altair]
   pip install huez[plotnine]
   
   # All libraries
   pip install huez[all]

Support Matrix
--------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 15 20

   * - Feature
     - matplotlib
     - seaborn
     - plotly
     - altair
     - plotnine
   * - Discrete colors
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
   * - Sequential colormaps
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
   * - Diverging colormaps
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
   * - Auto color expansion
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
   * - Smart colormap detection
     - ✅
     - ✅
     - ✅
     - 🟡
     - 🟡
   * - Print/presentation modes
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅

Legend: ✅ Full support | 🟡 Partial support | ❌ Not supported

Quick Examples
--------------

Each library has its own page with detailed examples. Here's a quick overview:

Matplotlib
^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   plt.plot([1, 2, 3], [1, 4, 9])

Seaborn
^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   sns.boxplot(data=df, x='category', y='value')

Plotly
^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   fig = px.scatter(df, x='x', y='y', color='category')

Altair
^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   alt.Chart(df).mark_circle().encode(x='x', y='y', color='category')

plotnine
^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   (ggplot(df, aes('x', 'y', color='category')) + geom_point())

Next Steps
----------

Explore detailed documentation for each library:

- :doc:`matplotlib` - Comprehensive matplotlib integration
- :doc:`seaborn` - Enhanced seaborn features
- :doc:`plotly` - Interactive plotly support
- :doc:`altair` - Declarative altair integration
- :doc:`plotnine` - Grammar of graphics for Python




