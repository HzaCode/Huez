API Reference
=============

Complete API documentation for Huez.

.. toctree::
   :maxdepth: 2
   
   core
   intelligence
   adapters
   utils
   aliases

Quick Reference
---------------

**Core Functions:**

.. code-block:: python

   hz.use(scheme, mode="screen", ensure_accessible=False)
   hz.current_scheme()
   hz.palette()
   hz.cmap(kind="sequential")
   hz.list_schemes()
   hz.preview(scheme)
   hz.using(scheme)  # Context manager

**Intelligence:**

.. code-block:: python

   import huez as hz
   
   # Main API (recommended)
   hz.expand_colors(colors, n_needed)
   hz.detect_colormap(data)
   hz.smart_cmap(data)
   hz.check_accessibility(colors)
   
   # Or import from intelligence module
   from huez.intelligence import (
       intelligent_color_expansion,
       detect_colormap_type,
       check_colorblind_safety,
       simulate_colorblind_vision,
       detect_chart_type,
       adapt_colors_for_chart
   )

**Configuration:**

.. code-block:: python

   hz.load_config("config.yaml")
   hz.export_styles("output.yaml")

Browse by Module
----------------

- :doc:`core` - Main API functions
- :doc:`intelligence` - Smart color features
- :doc:`adapters` - Library-specific adapters
- :doc:`utils` - Utility functions

Next Steps
----------

- See :doc:`../user_guide/index` for usage examples
- Check :doc:`../intelligence/index` for smart features


