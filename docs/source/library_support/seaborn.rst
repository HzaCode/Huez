Seaborn
=======

Enhanced integration with seaborn, including smart colormap detection for heatmaps.

Basic Usage
-----------

.. code-block:: python

   import seaborn as sns
   import huez as hz
   
   hz.use("scheme-1")
   
   # All seaborn plots use Huez colors
   sns.scatterplot(data=df, x='x', y='y', hue='category')
   plt.show()

Supported Plot Types
--------------------

**Categorical**: boxplot, violinplot, barplot, countplot, pointplot

**Distribution**: histplot, kdeplot, rugplot, distplot

**Relational**: scatterplot, lineplot

**Matrix**: heatmap, clustermap

**Regression**: regplot, lmplot

Smart Heatmaps
--------------

Automatic colormap detection:

.. code-block:: python

   hz.use("scheme-1")
   
   # Correlation → auto-detects diverging colormap
   sns.heatmap(correlation_matrix)
   
   # Count data → auto-detects sequential colormap
   sns.heatmap(count_matrix)

.. image:: /_static/comparison/seaborn_huez_lines.png
   :width: 60%
   :align: center

Next Steps
----------

- See :doc:`matplotlib` for matplotlib integration
- Read :doc:`../intelligence/colormap_detection` for smart heatmaps



