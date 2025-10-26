plotnine
========

Integration with plotnine, the Grammar of Graphics for Python (ggplot2 port).

Basic Usage
-----------

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

ggplot2 Syntax
--------------

Full ggplot2-style syntax supported:

.. code-block:: python

   hz.use("scheme-1")
   
   (ggplot(df, aes('x', 'y', fill='category'))
    + geom_bar(stat='identity')
    + facet_wrap('~group')
    + theme_bw()
    + labs(title='Title', x='X axis', y='Y axis'))

Getting Scales
--------------

For manual scale control:

.. code-block:: python

   hz.use("scheme-1")
   scales = hz.gg_scales()
   
   (ggplot(df, aes('x', 'y', color='category'))
    + geom_point()
    + scales['color_discrete'])

Next Steps
----------

- Check :doc:`altair` for alternative declarative syntax
- Read :doc:`../user_guide/custom_schemes` for customization



