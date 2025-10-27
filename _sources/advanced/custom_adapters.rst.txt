Custom Adapters
===============

Extend Huez to support additional visualization libraries.

Creating an Adapter
-------------------

To add support for a new library, create an adapter class:

.. code-block:: python

   from huez.adapters.base import Adapter
   
   class MyLibraryAdapter(Adapter):
       """Adapter for MyLibrary"""
       
       def apply(self, config):
           """Apply configuration to MyLibrary"""
           # Set discrete colors
           mylibrary.set_colors(config['palettes']['discrete'])
           
           # Set colormaps
           mylibrary.set_colormap(config['palettes']['sequential'])
           
           # Set fonts
           mylibrary.set_font(config['fonts']['family'])
       
       def reset(self):
           """Reset to MyLibrary defaults"""
           mylibrary.reset_defaults()

Register the Adapter
--------------------

Register your adapter:

.. code-block:: python

   # In your code
   from huez.registry import register_adapter
   
   register_adapter('mylibrary', MyLibraryAdapter())

Or via configuration:

.. code-block:: yaml

   # adapters_registry.yaml
   adapters:
     mylibrary:
       module: mypackage.adapters
       class: MyLibraryAdapter

Example: Bokeh Adapter
----------------------

Complete example for Bokeh:

.. code-block:: python

   from huez.adapters.base import Adapter
   from bokeh.palettes import Palette
   from bokeh.models import LinearColorMapper
   
   class BokehAdapter(Adapter):
       def __init__(self):
           self.original_palette = None
       
       def apply(self, config):
           # Save original
           self.original_palette = Palette.default
           
           # Apply discrete colors
           colors = config['palettes']['discrete']
           Palette.default = colors
           
           # Apply to existing figures
           from bokeh.io import curdoc
           doc = curdoc()
           for root in doc.roots:
               self._apply_to_figure(root, colors)
       
       def reset(self):
           if self.original_palette:
               Palette.default = self.original_palette
       
       def _apply_to_figure(self, figure, colors):
           # Update figure colors
           if hasattr(figure, 'renderers'):
               for i, renderer in enumerate(figure.renderers):
                   if hasattr(renderer, 'glyph'):
                       renderer.glyph.fill_color = colors[i % len(colors)]

Testing Your Adapter
--------------------

Test that your adapter works:

.. code-block:: python

   def test_mylibrary_adapter():
       import huez as hz
       import mylibrary
       
       # Apply scheme
       hz.use("scheme-1")
       
       # Create plot
       mylibrary.plot([1, 2, 3], [1, 4, 9])
       
       # Verify colors
       assert mylibrary.get_current_colors() == hz.palette()

Best Practices
--------------

1. **Save defaults**: Always save original settings in ``__init__``
2. **Full reset**: ``reset()`` should restore all original settings
3. **Error handling**: Handle library-specific exceptions
4. **Documentation**: Document library-specific behavior
5. **Testing**: Write comprehensive tests

Contributing
------------

To contribute an adapter to Huez:

1. Create adapter in ``huez/adapters/yourlibrary.py``
2. Add tests in ``tests/unit/test_adapters.py``
3. Update ``adapters_registry.yaml``
4. Add documentation page
5. Submit pull request

See :doc:`../contributing` for details.

Next Steps
----------

- Check existing adapters in ``huez/adapters/``
- See :doc:`../contributing` for contribution guidelines


