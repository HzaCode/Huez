Before/After Comparisons
========================

See the visual impact of Huez on real visualizations.

Cross-Library Consistency
--------------------------

**Before (Inconsistent):**

.. image:: /_static/comparison/inconsistent_before.png
   :width: 45%
   :alt: Before Huez

**After (Consistent):**

.. image:: /_static/comparison/consistent_after.png
   :width: 45%
   :alt: After Huez

With Huez, all libraries use the same professional color scheme.

Matplotlib
----------

**Default:**

.. image:: /_static/comparison/matplotlib_default_lines.png
   :width: 45%

**With Huez:**

.. image:: /_static/comparison/matplotlib_huez_lines.png
   :width: 45%

Seaborn
-------

**Default:**

.. image:: /_static/comparison/seaborn_default_lines.png
   :width: 45%

**With Huez:**

.. image:: /_static/comparison/seaborn_huez_lines.png
   :width: 45%

Plotly
------

**Default:**

.. image:: /_static/comparison/plotly_default_scatter.png
   :width: 45%

**With Huez:**

.. image:: /_static/comparison/plotly_huez_scatter.png
   :width: 45%

Altair
------

**Default:**

.. image:: /_static/comparison/altair_default_bars.png
   :width: 45%

**With Huez:**

.. image:: /_static/comparison/altair_huez_bars.png
   :width: 45%

plotnine
--------

**Default:**

.. image:: /_static/comparison/plotnine_default_bars.png
   :width: 45%

**With Huez:**

.. image:: /_static/comparison/plotnine_huez_bars.png
   :width: 45%

Code Simplification
-------------------

**Before (Manual Configuration):**

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # Manually configure each library
   plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#E64B35', '#4DBBD5', ...])
   sns.set_palette(['#E64B35', '#4DBBD5', ...])
   # ... more manual configuration ...

**After (One Line):**

.. code-block:: python

   import huez as hz
   
   hz.use("scheme-1")  # That's it!

Clean Visuals
-------------

**Before:**

.. image:: /_static/comparison/clean_before.png
   :width: 45%
   :alt: Cluttered default styles

**After:**

.. image:: /_static/comparison/clean_after.png
   :width: 45%
   :alt: Clean professional styling

Next Steps
----------

- Try it yourself with :doc:`../quickstart`
- Browse :doc:`palettes` for all color schemes
- Read :doc:`../user_guide/best_practices` for tips




