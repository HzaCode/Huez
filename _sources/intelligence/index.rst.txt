Intelligence Features
=====================

Huez includes four intelligent features that automatically adapt colors to your data and visualization needs.

.. toctree::
   :maxdepth: 2
   
   color_expansion
   colormap_detection
   accessibility
   chart_adaptation

Overview
--------

Traditional color management tools require manual configuration for every scenario. Huez introduces intelligence:

1. **Color Expansion**: Automatically generates unlimited perceptually distinct colors
2. **Colormap Detection**: Automatically selects sequential vs. diverging colormaps
3. **Accessibility**: Real-time colorblind safety verification
4. **Chart Adaptation**: Provides recommendations based on chart complexity

All features work automatically when you use ``hz.use()``.

Quick Comparison
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Traditional Approach
     - Huez Intelligence
   * - 15+ categories
     - Colors repeat → confusion
     - LAB interpolation → unique colors
   * - Heatmap coloring
     - Manual ``cmap`` selection
     - Auto-detects data distribution
   * - Colorblind safety
     - Manual checking needed
     - Automatic verification
   * - Complex charts
     - No guidance
     - Actionable recommendations

Feature Cards
-------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🎨 Intelligent Color Expansion
      :link: color_expansion
      :link-type: doc
      
      LAB space interpolation generates unlimited perceptually distinct colors.
      
      **Problem Solved**: Color repetition with many categories
      
      **Technology**: Perceptually uniform LAB color space

   .. grid-item-card:: 🎯 Smart Colormap Detection
      :link: colormap_detection
      :link-type: doc
      
      Automatically detects whether data needs sequential or diverging colormap.
      
      **Problem Solved**: Wrong colormap type
      
      **Technology**: Data distribution analysis

   .. grid-item-card:: ♿ Colorblind Accessibility
      :link: accessibility
      :link-type: doc
      
      Real-time simulation of 3 types of color vision deficiency.
      
      **Problem Solved**: Inaccessible visualizations
      
      **Technology**: Brettel algorithm + WCAG standards

   .. grid-item-card:: 📊 Chart Type Adaptation
      :link: chart_adaptation
      :link-type: doc
      
      Detects chart complexity and provides visual encoding recommendations.
      
      **Problem Solved**: Unclear complex visualizations
      
      **Technology**: Chart introspection + best practices

Automatic Enablement
--------------------

Most intelligence features are enabled by default:

.. code-block:: python

   import huez as hz
   import matplotlib.pyplot as plt
   import seaborn as sns
   import numpy as np
   
   # auto_expand=True and smart_cmap=True by default
   hz.use("scheme-1")
   
   # Plot 15 categories → automatic color expansion
   x = np.linspace(0, 10, 100)
   for i in range(15):
       plt.plot(x, np.sin(x + i*0.5), label=f'Series {i+1}')
   plt.legend()
   plt.show()
   
   # Correlation heatmap → automatic diverging colormap
   correlation_matrix = np.corrcoef(np.random.randn(10, 100))
   sns.heatmap(correlation_matrix)
   plt.show()

.. note::

   **Default Intelligence Settings:**
   
   - ``auto_expand=True`` - Color expansion enabled ✓
   - ``smart_cmap=True`` - Colormap detection enabled ✓
   - ``ensure_accessible=False`` - Accessibility check disabled (must enable explicitly)

Manual Control
--------------

You can control features individually using the simplified top-level API:

**Color Expansion:**

.. code-block:: python

   import huez as hz
   
   base_colors = ["#E64B35", "#4DBBD5", "#00A087"]
   expanded = hz.expand_colors(base_colors, n_needed=15)

**Colormap Detection:**

.. code-block:: python

   import huez as hz
   import numpy as np
   
   data = np.corrcoef(np.random.randn(10, 100))
   cmap_type = hz.detect_colormap(data)
   print(cmap_type)  # 'diverging'

**Accessibility Check:**

.. code-block:: python

   import huez as hz
   
   colors = ["#E64B35", "#4DBBD5", "#00A087"]
   result = hz.check_accessibility(colors)
   
   if not result['safe']:
       print(result['warnings'])
       print(result['suggestions'])

.. note::

   **API Naming Convention**
   
   For convenience, Huez provides simplified names at the top level:
   
   - ``hz.expand_colors()`` → ``huez.intelligence.intelligent_color_expansion()``
   - ``hz.detect_colormap()`` → ``huez.intelligence.detect_colormap_type()``
   - ``hz.check_accessibility()`` → ``huez.intelligence.check_colorblind_safety()``
   
   Advanced users can use the full module names, but we recommend the simplified API
   for most use cases.

**Chart Adaptation:**

.. code-block:: python

   from huez.intelligence import detect_chart_type, adapt_colors_for_chart
   import matplotlib.pyplot as plt
   
   fig, ax = plt.subplots()
   # ... create plot ...
   
   chart_info = detect_chart_type(ax)
   colors = ["#E64B35", "#4DBBD5", "#00A087"]
   adapted_colors, advice = adapt_colors_for_chart(colors, chart_info)
   
   print(advice['recommendations'])

.. note::

   Chart adaptation functions are currently only available through direct import
   from ``huez.intelligence`` as they are advanced features for specialized use cases.

Configuration
-------------

Configure intelligence features in your config file:

.. code-block:: yaml

   schemes:
     my_scheme:
       intelligence:
         auto_expand: true              # Enable color expansion
         smart_cmap: true                # Enable colormap detection
         ensure_accessible: true         # Enable accessibility checks
         auto_adapt: false               # Enable chart adaptation
         min_contrast: 3.0               # Minimum contrast ratio
         colorblind_threshold: 10.0      # Delta E threshold

Or via API:

.. code-block:: python

   hz.use("scheme-1",
          auto_expand=True,
          smart_cmap=True,
          ensure_accessible=True)

Performance
-----------

All intelligence features have minimal performance impact:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Feature
     - Overhead
     - When Applied
   * - Color Expansion
     - < 10ms
     - Once at initialization
   * - Colormap Detection
     - < 5ms
     - Per heatmap
   * - Accessibility Check
     - < 50ms
     - Once at initialization
   * - Chart Adaptation
     - < 5ms
     - Per chart (optional)

**Total overhead**: Typically < 100ms, imperceptible to users.

Research Background
-------------------

The intelligence features are based on established research:

**Color Expansion:**

- Perceptually uniform LAB color space (CIE 1976)
- Linear interpolation in LAB preserves perceptual distance

**Colormap Detection:**

- Data distribution analysis
- Statistical heuristics for sequential vs. diverging classification

**Accessibility:**

- Brettel et al. (1997) colorblind simulation algorithm
- WCAG 2.0 contrast ratio standards
- Delta E color difference metrics (CIE76)

**Chart Adaptation:**

- Visualization best practices literature
- Empirical guidelines from Cairo (2016), Few (2012)

Next Steps
----------

Explore each feature in detail:

- :doc:`color_expansion` - Learn about LAB space interpolation
- :doc:`colormap_detection` - Understand automatic colormap selection
- :doc:`accessibility` - Ensure colorblind safety
- :doc:`chart_adaptation` - Get visualization recommendations


