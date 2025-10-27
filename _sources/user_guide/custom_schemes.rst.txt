Custom Schemes
==============

This guide shows you how to create and configure your own color schemes.

Creating a Custom Configuration
--------------------------------

Create a YAML file with your custom scheme:

**my_config.yaml:**

.. code-block:: yaml

   version: 1
   default_scheme: my_custom_scheme
   
   schemes:
     my_custom_scheme:
       title: "My Custom Color Scheme"
       
       fonts:
         family: "DejaVu Sans"
         size: 10
       
       palettes:
         discrete: "npg"           # Use built-in palette
         sequential: "viridis"     # Built-in colormap
         diverging: "coolwarm"     # Built-in colormap
         cyclic: "twilight"        # Built-in colormap
       
       figure:
         dpi: 300
         facecolor: "white"
         edgecolor: "white"
       
       style:
         grid: "y"                 # Show grid on y-axis only
         legend_loc: "best"
         spine_top_right_off: true

Loading Custom Configuration
-----------------------------

Load your custom configuration:

.. code-block:: python

   import huez as hz
   
   # Load configuration file
   hz.load_config("my_config.yaml")
   
   # Use your custom scheme
   hz.use("my_custom_scheme")

Custom Color Palette
--------------------

Define your own colors:

.. code-block:: yaml

   schemes:
     my_palette_scheme:
       title: "My Brand Colors"
       
       palettes:
         discrete:
           colors:
             - "#FF6B6B"  # Red
             - "#4ECDC4"  # Cyan
             - "#45B7D1"  # Blue
             - "#FFA07A"  # Salmon
             - "#98D8C8"  # Mint
             - "#F7DC6F"  # Yellow
           
         sequential: "viridis"
         diverging: "coolwarm"

.. code-block:: python

   hz.load_config("my_config.yaml")
   hz.use("my_palette_scheme")

Complete Custom Colormaps
--------------------------

Define custom colormaps using color lists:

.. code-block:: yaml

   schemes:
     my_colormap_scheme:
       title: "Custom Colormaps"
       
       palettes:
         discrete: "npg"
         
         sequential:
           colors:
             - "#f7fbff"
             - "#deebf7"
             - "#c6dbef"
             - "#9ecae1"
             - "#6baed6"
             - "#4292c6"
             - "#2171b5"
             - "#08519c"
             - "#08306b"
           name: "my_blue_sequential"
         
         diverging:
           colors:
             - "#67001f"
             - "#b2182b"
             - "#d6604d"
             - "#f4a582"
             - "#fddbc7"
             - "#f7f7f7"
             - "#d1e5f0"
             - "#92c5de"
             - "#4393c3"
             - "#2166ac"
             - "#053061"
           name: "my_red_blue_diverging"

Multi-Mode Configuration
-------------------------

Define different colors for different modes:

.. code-block:: yaml

   schemes:
     adaptive_scheme:
       title: "Adaptive Multi-Mode Scheme"
       
       modes:
         screen:
           palettes:
             discrete: "npg"
             sequential: "viridis"
             diverging: "coolwarm"
           
         print:
           palettes:
             discrete:
               colors:
                 - "#000000"  # Black
                 - "#404040"  # Dark gray
                 - "#808080"  # Gray
                 - "#C0C0C0"  # Light gray
                 - "#606060"  # Medium gray
             sequential: "gray"
             diverging: "RdGy"
           
         presentation:
           palettes:
             discrete:
               colors:
                 - "#E31A1C"  # Bright red
                 - "#1F78B4"  # Bright blue
                 - "#33A02C"  # Bright green
                 - "#FF7F00"  # Bright orange
             sequential: "plasma"
             diverging: "RdBu"

Configuration Options Reference
--------------------------------

Complete reference for configuration options:

**Top Level:**

.. code-block:: yaml

   version: 1                  # Configuration version
   default_scheme: "name"      # Default scheme to use

**Scheme Structure:**

.. code-block:: yaml

   schemes:
     scheme_name:
       title: "Scheme Title"
       
       # Font configuration
       fonts:
         family: "sans-serif"  # Font family
         size: 10              # Base font size
         
       # Color palettes
       palettes:
         discrete: "palette_name"
         sequential: "colormap_name"
         diverging: "colormap_name"
         cyclic: "colormap_name"
       
       # Figure settings
       figure:
         dpi: 100
         figsize: [6.4, 4.8]
         facecolor: "white"
         edgecolor: "white"
       
       # Style settings
       style:
         grid: "both"           # "both", "x", "y", or "none"
         legend_loc: "best"
         spine_top_right_off: true
         
       # Axes settings
       axes:
         facecolor: "white"
         edgecolor: "black"
         linewidth: 0.8
         grid: true
         grid_alpha: 0.3

Built-in Palettes
-----------------

You can reference built-in palettes:

**Journal Palettes:**

- ``npg`` - Nature Publishing Group
- ``aaas`` - Science/AAAS
- ``nejm`` - New England Journal of Medicine
- ``lancet`` - The Lancet
- ``jama`` - JAMA
- ``bmj`` - BMJ

**Colorblind-Safe:**

- ``okabe-ito``
- ``paul-tol-bright``
- ``paul-tol-vibrant``

**Matplotlib Colormaps:**

- Sequential: ``viridis``, ``plasma``, ``inferno``, ``magma``, ``cividis``
- Diverging: ``coolwarm``, ``bwr``, ``seismic``, ``RdBu``, ``RdYlBu``
- Cyclic: ``twilight``, ``twilight_shifted``

Example: Corporate Branding
----------------------------

Create a scheme matching your corporate brand:

.. code-block:: yaml

   schemes:
     company_brand:
       title: "Company Brand Colors"
       
       palettes:
         discrete:
           colors:
             - "#003366"  # Corporate Blue (primary)
             - "#FF6600"  # Corporate Orange (secondary)
             - "#00CC99"  # Corporate Teal (accent)
             - "#999999"  # Corporate Gray (neutral)
             - "#663399"  # Corporate Purple (highlight)
       
       fonts:
         family: "Arial"  # Corporate font
         size: 11
       
       figure:
         facecolor: "#F8F8F8"  # Light gray background
       
       style:
         grid: "y"
         legend_loc: "upper right"

.. code-block:: python

   hz.load_config("company_config.yaml")
   hz.use("company_brand")

Example: Academic Publication
------------------------------

Optimized for journal submission:

.. code-block:: yaml

   schemes:
     academic_publication:
       title: "Academic Publication Style"
       
       palettes:
         discrete: "okabe-ito"  # Colorblind-safe
         sequential: "viridis"
         diverging: "coolwarm"
       
       fonts:
         family: "Times New Roman"
         size: 9
       
       figure:
         dpi: 300              # High resolution
         figsize: [3.5, 2.5]   # Single column width
       
       style:
         grid: "both"
         legend_loc: "best"
         spine_top_right_off: true
       
       axes:
         linewidth: 0.5        # Thin borders

.. code-block:: python

   hz.load_config("academic_config.yaml")
   hz.use("academic_publication", mode="print", ensure_accessible=True)

Combining Schemes
-----------------

Inherit from existing schemes:

.. code-block:: yaml

   schemes:
     base_scheme:
       title: "Base Scheme"
       palettes:
         discrete: "npg"
         sequential: "viridis"
         diverging: "coolwarm"
       fonts:
         family: "sans-serif"
         size: 10
     
     derived_scheme:
       extends: "base_scheme"  # Inherit from base_scheme
       title: "Derived Scheme"
       palettes:
         discrete: "lancet"    # Override only discrete palette

Programmatic Scheme Creation
-----------------------------

Create schemes programmatically:

.. code-block:: python

   import huez as hz
   
   # Define scheme as dictionary
   custom_scheme = {
       'title': 'Programmatic Scheme',
       'palettes': {
           'discrete': {
               'colors': ['#E64B35', '#4DBBD5', '#00A087', '#3C5488']
           },
           'sequential': 'viridis',
           'diverging': 'coolwarm'
       },
       'fonts': {
           'family': 'Arial',
           'size': 11
       }
   }
   
   # Register scheme (not yet implemented - placeholder)
   # hz.register_scheme('my_scheme', custom_scheme)
   # hz.use('my_scheme')

Exporting Current Scheme
-------------------------

Export the current scheme to a file:

.. code-block:: python

   import huez as hz
   
   hz.use("lancet")
   
   # Export current configuration
   hz.export_styles("my_exported_config.yaml")
   
   # Now you can modify and reload it
   hz.load_config("my_exported_config.yaml")

Validation
----------

Huez validates your configuration:

.. code-block:: python

   try:
       hz.load_config("my_config.yaml")
   except ValueError as e:
       print(f"Configuration error: {e}")

Common validation errors:

- Missing required fields
- Invalid color format
- Unknown palette names
- Invalid YAML syntax

Tips
----

.. tip::

   **Start with Existing Schemes**
   
   Export an existing scheme and modify it:
   
   .. code-block:: python
   
      hz.use("npg")
      hz.export_styles("my_base.yaml")
      # Edit my_base.yaml, then reload

.. note::

   **Color Format**
   
   Colors can be specified in multiple formats:
   
   - Hex: ``#FF6B6B``
   - RGB: ``rgb(255, 107, 107)``
   - Named: ``red``, ``blue``, etc.

.. warning::

   **Colormap Names**
   
   Use matplotlib colormap names for sequential/diverging colormaps.
   See `matplotlib colormaps <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`_.

Next Steps
----------

- Check :doc:`best_practices` for configuration tips
- Explore :doc:`../gallery/palettes` for inspiration


