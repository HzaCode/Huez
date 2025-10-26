Chart Type Adaptation
=====================

Get intelligent recommendations based on chart complexity and type.

The Problem
-----------

Complex charts with many elements can be hard to interpret, even with good colors.

**Traditional approach**: No guidance → users struggle

**Huez approach**: Automatic detection + actionable recommendations

What It Does
------------

Huez analyzes your chart and provides:

1. **Chart type detection**: Line, scatter, bar, or mixed
2. **Complexity assessment**: Simple, medium, or complex
3. **Actionable recommendations**: Specific improvements

Example
-------

.. code-block:: python

   from huez.intelligence import detect_chart_type, adapt_colors_for_chart
   import matplotlib.pyplot as plt
   import huez as hz
   
   hz.use("scheme-1")
   
   # Create complex plot with 12 lines
   fig, ax = plt.subplots()
   for i in range(12):
       ax.plot(x, y + i*0.5, label=f'Series {i+1}')
   ax.legend()
   
   # Get recommendations
   chart_info = detect_chart_type(ax)
   colors, advice = adapt_colors_for_chart(hz.palette(), chart_info)
   
   print(advice['recommendations'])

Output:

.. code-block:: text

   Chart Analysis:
   - Type: line
   - Elements: 12 lines
   - Complexity: complex
   
   Recommendations:
   • Consider adding markers to distinguish lines
   • Suggested markers: ['o', 's', '^', 'v', 'D', 'p', '*', 'h', '+', 'x', 'X', 'd']
   • Consider using different line styles
   • Suggested line styles: ['-', '--', '-.', ':']
   • For better clarity, consider splitting into multiple panels or faceted plots

Chart Type Detection
--------------------

Detects chart types by analyzing matplotlib artists:

Line Charts
^^^^^^^^^^^

.. code-block:: python

   # Detects as "line" chart
   ax.plot(x, y)
   
   chart_info = detect_chart_type(ax)
   # {'type': 'line', 'n_lines': 1, 'n_scatter': 0, 'n_bars': 0}

Scatter Plots
^^^^^^^^^^^^^

.. code-block:: python

   # Detects as "scatter" chart
   ax.scatter(x, y)
   
   chart_info = detect_chart_type(ax)
   # {'type': 'scatter', 'n_lines': 0, 'n_scatter': 1, 'n_bars': 0}

Bar Charts
^^^^^^^^^^

.. code-block:: python

   # Detects as "bar" chart
   ax.bar(categories, values)
   
   chart_info = detect_chart_type(ax)
   # {'type': 'bar', 'n_lines': 0, 'n_scatter': 0, 'n_bars': 5}

Mixed Charts
^^^^^^^^^^^^

.. code-block:: python

   # Detects as "mixed" chart
   ax.plot(x, y1)
   ax.scatter(x, y2)
   
   chart_info = detect_chart_type(ax)
   # {'type': 'mixed', 'n_lines': 1, 'n_scatter': 1, 'n_bars': 0}

Complexity Levels
-----------------

Simple (≤ 4 elements)
^^^^^^^^^^^^^^^^^^^^^

**No special actions needed**

.. code-block:: python

   # 3 lines → simple
   for i in range(3):
       plt.plot(x, y + i*0.5)
   
   # Recommendation: None needed

Medium (5-7 elements)
^^^^^^^^^^^^^^^^^^^^^

**Consider adding differentiation**

.. code-block:: python

   # 6 lines → medium
   for i in range(6):
       plt.plot(x, y + i*0.5)
   
   # Recommendation: Use different line styles

Complex (8+ elements)
^^^^^^^^^^^^^^^^^^^^^

**Strong recommendations**

.. code-block:: python

   # 12 lines → complex
   for i in range(12):
       plt.plot(x, y + i*0.5)
   
   # Recommendations:
   # - Add markers
   # - Use line styles
   # - Consider faceting

Recommendations by Type
-----------------------

For Line Charts
^^^^^^^^^^^^^^^

.. code-block:: python

   # Medium complexity (5-7 lines)
   recommendations = [
       "Consider using different line styles",
       "Suggested: ['-', '--', '-.', ':']"
   ]
   
   # High complexity (8+ lines)
   recommendations = [
       "Add markers to distinguish lines",
       "Suggested markers: ['o', 's', '^', 'v', 'D', 'p', '*']",
       "Use different line styles",
       "Consider faceting or grouping"
   ]

For Scatter Plots
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # High complexity (many categories)
   recommendations = [
       "Consider using different marker shapes",
       "Or use faceted plots with FacetGrid"
   ]

For Bar Charts
^^^^^^^^^^^^^^

.. code-block:: python

   # High complexity (many bars)
   recommendations = [
       "Consider adding hatches/patterns",
       "Suggested hatches: ['/', '\\\\', '|', '-', '+', 'x']",
       "Or group bars into categories"
   ]

Usage Examples
--------------

Example 1: Apply Recommendations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import matplotlib.pyplot as plt
   from huez.intelligence import detect_chart_type, adapt_colors_for_chart
   import huez as hz
   
   hz.use("scheme-1")
   
   # Create complex plot
   fig, ax = plt.subplots()
   colors = hz.palette()
   
   markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', '+', 'x']
   linestyles = ['-', '--', '-.', ':']
   
   for i in range(10):
       ax.plot(x, y + i*0.5, 
               color=colors[i % len(colors)],
               marker=markers[i % len(markers)],
               linestyle=linestyles[i % len(linestyles)],
               markevery=10,
               label=f'Series {i+1}')
   
   ax.legend()
   plt.show()

Example 2: Faceting Alternative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import seaborn as sns
   import pandas as pd
   
   hz.use("scheme-1")
   
   # Instead of 16 lines in one plot
   # Use faceted plots
   g = sns.FacetGrid(df, col='category', col_wrap=4, height=3)
   g.map(plt.plot, 'x', 'y')
   g.add_legend()
   plt.show()

Example 3: Bar Chart with Hatches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1")
   
   colors = hz.palette()
   hatches = ['/', '\\\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
   
   for i, (cat, val) in enumerate(zip(categories, values)):
       plt.bar(i, val, 
               color=colors[i % len(colors)],
               hatch=hatches[i % len(hatches)],
               edgecolor='black',
               label=cat)
   
   plt.legend()
   plt.show()

Technical Details
-----------------

Detection Algorithm
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def detect_chart_type(ax):
       \"\"\"Detect chart type and complexity\"\"\"
       
       # Count artists
       n_lines = len(ax.get_lines())
       n_collections = len(ax.collections)  # Scatter, bar, etc.
       n_patches = len(ax.patches)  # Bar patches
       
       # Determine primary type
       if n_lines > 0 and n_collections == 0:
           chart_type = "line"
       elif n_collections > 0 and n_lines == 0:
           if n_patches > 0:
               chart_type = "bar"
           else:
               chart_type = "scatter"
       elif n_lines > 0 and n_collections > 0:
           chart_type = "mixed"
       else:
           chart_type = "unknown"
       
       # Determine complexity
       total_elements = n_lines + n_collections + (n_patches // 2)
       
       if total_elements <= 4:
           complexity = "simple"
       elif total_elements <= 7:
           complexity = "medium"
       else:
           complexity = "complex"
       
       return {
           'type': chart_type,
           'complexity': complexity,
           'n_lines': n_lines,
           'n_scatter': len([c for c in ax.collections if 'scatter' in str(type(c)).lower()]),
           'n_bars': n_patches // 2,  # Each bar has 2 patches
           'total_elements': total_elements
       }

Adaptation Logic
^^^^^^^^^^^^^^^^

.. code-block:: python

   def adapt_colors_for_chart(colors, chart_info):
       \"\"\"Provide recommendations based on chart complexity\"\"\"
       
       recommendations = []
       advice = {'markers': [], 'linestyles': [], 'hatches': []}
       
       if chart_info['complexity'] == 'simple':
           recommendations.append("No special actions needed")
       
       elif chart_info['complexity'] == 'medium':
           if chart_info['type'] == 'line':
               recommendations.append("Consider using different line styles")
               advice['linestyles'] = ['-', '--', '-.', ':']
       
       elif chart_info['complexity'] == 'complex':
           if chart_info['type'] == 'line':
               recommendations.extend([
                   "Add markers to distinguish lines",
                   "Use different line styles",
                   "Consider faceting"
               ])
               advice['markers'] = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', '+', 'x']
               advice['linestyles'] = ['-', '--', '-.', ':']
           
           elif chart_info['type'] == 'bar':
               recommendations.append("Add hatches/patterns")
               advice['hatches'] = ['/', '\\\\', '|', '-', '+', 'x']
       
       return colors, {'recommendations': recommendations, **advice}

Best Practices
--------------

When to Use Markers
^^^^^^^^^^^^^^^^^^^

- **5+ lines**: Consider markers
- **8+ lines**: Strongly recommended
- **Spacing**: Use ``markevery`` parameter

.. code-block:: python

   # Good: Not overcrowded
   plt.plot(x, y, marker='o', markevery=10)

When to Use Facets
^^^^^^^^^^^^^^^^^^

- **10+ categories**: Consider faceting
- **16+ categories**: Strongly recommended

.. code-block:: python

   # Better than 16 lines in one plot
   g = sns.FacetGrid(df, col='category', col_wrap=4)
   g.map(plt.plot, 'x', 'y')

When to Use Hatches
^^^^^^^^^^^^^^^^^^^

- **Bar charts**: Always recommended
- **Print mode**: Essential for B&W
- **Colorblind safety**: Extra distinction

.. code-block:: python

   hz.use("scheme-1", mode="print")
   plt.bar(x, y, hatch='//', edgecolor='black')

Configuration
-------------

.. code-block:: yaml

   schemes:
     my_scheme:
       intelligence:
         auto_adapt: true  # Enable adaptation
         complexity_thresholds:
           simple: 4
           medium: 7

API Reference
-------------

.. autofunction:: huez.intelligence.detect_chart_type
.. autofunction:: huez.intelligence.adapt_colors_for_chart

Further Reading
---------------

- Few, S. (2012). *Show Me the Numbers*. Chapter on Visual Encoding
- Cairo, A. (2016). *The Truthful Art*. Chapter on Complexity Management
- Tufte, E. (2001). *The Visual Display of Quantitative Information*

Next Steps
----------

- Learn about :doc:`color_expansion` for many categories
- Check :doc:`accessibility` for additional encodings
- Read :doc:`../user_guide/best_practices` for visualization tips



