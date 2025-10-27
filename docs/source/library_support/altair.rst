Altair
======

Integration with Altair for declarative visualization based on Vega-Lite.

Basic Usage
-----------

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

Grammar of Graphics
-------------------

Altair's declarative syntax works naturally with Huez:

.. code-block:: python

   hz.use("scheme-1")
   
   alt.Chart(df).mark_line().encode(
       x='date:T',
       y='value:Q',
       color='category:N'
   ) + alt.Chart(df).mark_circle().encode(
       x='date:T',
       y='value:Q',
       color='category:N'
   )

Next Steps
----------

- See :doc:`plotnine` for ggplot2-style grammar
- Check :doc:`../user_guide/basic_usage` for more examples




