Plotly
======

Integration with Plotly for interactive web-based visualizations.

Basic Usage
-----------

.. code-block:: python

   import plotly.express as px
   import plotly.graph_objects as go
   import huez as hz
   
   hz.use("scheme-1")
   
   # Plotly Express
   fig = px.scatter(df, x='x', y='y', color='category')
   fig.show()
   
   # Plotly Graph Objects
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=x, y=y1, name='Data 1'))
   fig.add_trace(go.Scatter(x=x, y=y2, name='Data 2'))
   fig.show()

.. image:: /_static/comparison/plotly_huez_scatter.png
   :width: 60%
   :align: center

Interactive Features
--------------------

Plotly's interactive features work seamlessly with Huez colors:

- Hover tooltips
- Zooming and panning
- Legend toggling
- 3D rotation

Next Steps
----------

- Check :doc:`altair` for declarative visualizations
- Explore :doc:`../gallery/index` for examples




