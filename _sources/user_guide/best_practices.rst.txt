Best Practices
==============

Guidelines and recommendations for using Huez effectively.

General Principles
------------------

Let Huez Handle Colors Automatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Do:**

.. code-block:: python

   hz.use("scheme-1")
   
   # ✅ Good: Let Huez assign colors
   plt.plot(x, y1, label='Series 1')
   plt.plot(x, y2, label='Series 2')
   
   # ✅ Good: Automatic colormap detection
   sns.heatmap(data)

**Don't:**

.. code-block:: python

   hz.use("scheme-1")
   
   # ❌ Bad: Explicit colors override Huez
   plt.plot(x, y1, color='red')
   
   # ❌ Bad: Bypasses intelligent features
   sns.heatmap(data, cmap='viridis')

Apply Schemes Early
^^^^^^^^^^^^^^^^^^^

Apply your scheme before creating figures:

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   import huez as hz
   
   # ✅ Good: Apply first
   hz.use("scheme-1")
   
   # Then create figures
   plt.figure()
   plt.plot(x, y)

Choose Appropriate Modes
^^^^^^^^^^^^^^^^^^^^^^^^^

Match the mode to your output:

.. code-block:: python

   # For screen display
   hz.use("scheme-1", mode="screen")
   
   # For journal submission
   hz.use("scheme-1", mode="print")
   
   # For presentations
   hz.use("scheme-1", mode="presentation")

Publication Workflow
--------------------

Journal Article
^^^^^^^^^^^^^^^

.. code-block:: python

   import huez as hz
   import matplotlib.pyplot as plt
   
   # Use journal style with print mode
   hz.use("npg", mode="print", ensure_accessible=True)
   
   # High resolution
   fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=300)
   
   # Plot with thick lines for print
   ax.plot(x, y1, linewidth=2, marker='o', markevery=5, label='Control')
   ax.plot(x, y2, linewidth=2, marker='s', markevery=5, label='Treatment')
   
   # Clear labels
   ax.set_xlabel('Time (hours)', fontsize=9)
   ax.set_ylabel('Response', fontsize=9)
   ax.legend(fontsize=8, frameon=False)
   
   # Save high-resolution
   plt.savefig('figure1.pdf', dpi=300, bbox_inches='tight')

**Checklist:**

- ☐ Use ``mode="print"``
- ☐ Set ``ensure_accessible=True``
- ☐ Use ``figsize`` matching journal requirements (typically 3.5" or 7" wide)
- ☐ Set ``dpi=300`` or higher
- ☐ Add markers to lines
- ☐ Use ``bbox_inches='tight'``
- ☐ Save as PDF or high-res PNG

Conference Poster
^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1", mode="presentation")
   
   # Large size for poster
   fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
   
   # Very thick lines and large markers
   ax.plot(x, y, linewidth=4, marker='o', markersize=10)
   
   # Large fonts
   ax.set_xlabel('X Label', fontsize=24)
   ax.set_ylabel('Y Label', fontsize=24)
   ax.set_title('Clear Title', fontsize=28, fontweight='bold')
   ax.tick_params(labelsize=20)
   
   plt.savefig('poster_figure.png', dpi=150, bbox_inches='tight')

Accessibility
-------------

Ensure Colorblind Safety
^^^^^^^^^^^^^^^^^^^^^^^^^

Always check colorblind accessibility:

.. code-block:: python

   # Check before using
   result = hz.check_accessibility("npg")
   
   if not result['safe']:
       print("⚠️ Not colorblind-safe!")
       print(result['suggestions'])
       
       # Use recommended alternative
       hz.use("okabe-ito")
   else:
       hz.use("npg")

Or use automatic checking:

.. code-block:: python

   hz.use("scheme-1", ensure_accessible=True)

Use Colorblind-Safe Palettes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For maximum accessibility:

.. code-block:: python

   # Recommended colorblind-safe palettes
   hz.use("okabe-ito")
   hz.use("paul-tol-bright")
   hz.use("paul-tol-vibrant")

Add Redundant Encoding
^^^^^^^^^^^^^^^^^^^^^^^

Don't rely on color alone:

.. code-block:: python

   hz.use("scheme-1")
   
   # Add markers
   plt.plot(x, y1, marker='o', label='Group A')
   plt.plot(x, y2, marker='s', label='Group B')
   plt.plot(x, y3, marker='^', label='Group C')
   
   # Or line styles
   plt.plot(x, y1, linestyle='-', label='Solid')
   plt.plot(x, y2, linestyle='--', label='Dashed')
   plt.plot(x, y3, linestyle='-.', label='Dash-dot')

Multi-Category Plots
--------------------

When plotting many categories:

.. code-block:: python

   hz.use("scheme-1")
   
   # Huez automatically expands colors
   for i in range(15):
       plt.plot(x, y + i*0.5, label=f'Series {i+1}')
   
   plt.legend()

If more than 10 categories:

.. code-block:: python

   hz.use("scheme-1")
   
   # Add markers for better distinction
   markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', '+', 'x']
   
   for i in range(12):
       plt.plot(x, y + i*0.5, 
                marker=markers[i % len(markers)],
                markevery=5,
                label=f'Series {i+1}')

Or consider faceting:

.. code-block:: python

   import seaborn as sns
   
   hz.use("scheme-1")
   
   # Use facets instead of many colors
   g = sns.FacetGrid(df, col='category', col_wrap=4)
   g.map(plt.plot, 'x', 'y')

Heatmaps
--------

Let Huez detect colormap type:

.. code-block:: python

   hz.use("scheme-1")
   
   # ✅ Good: Automatic detection
   sns.heatmap(correlation_matrix)  # Auto-detects diverging
   sns.heatmap(count_matrix)        # Auto-detects sequential

Manual selection if needed:

.. code-block:: python

   # Force specific colormap type
   cmap = hz.cmap(kind="diverging")
   sns.heatmap(data, cmap=cmap, center=0, vmin=-1, vmax=1)

Add value annotations for clarity:

.. code-block:: python

   sns.heatmap(data, annot=True, fmt='.2f', cmap=hz.cmap())

Consistent Multi-Panel Figures
-------------------------------

Maintain consistency across panels:

.. code-block:: python

   hz.use("scheme-1")
   
   fig, axes = plt.subplots(2, 2, figsize=(12, 10))
   
   # All panels use same color scheme
   axes[0, 0].plot(x, y1, label='Data 1')
   axes[0, 0].plot(x, y2, label='Data 2')
   axes[0, 0].legend()
   axes[0, 0].set_title('Panel A')
   
   axes[0, 1].scatter(x, y, c=categories)
   axes[0, 1].set_title('Panel B')
   
   axes[1, 0].bar(categories, values)
   axes[1, 0].set_title('Panel C')
   
   axes[1, 1].hist(data, bins=30)
   axes[1, 1].set_title('Panel D')
   
   plt.tight_layout()

File Formats
------------

Choose appropriate format for output:

**PDF for Publications:**

.. code-block:: python

   plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')

Advantages: Vector format, lossless, editable

**PNG for Web/Presentations:**

.. code-block:: python

   plt.savefig('figure.png', dpi=150, bbox_inches='tight', 
               facecolor='white', edgecolor='none')

Advantages: Widely supported, good for screenshots

**SVG for Editability:**

.. code-block:: python

   plt.savefig('figure.svg', bbox_inches='tight')

Advantages: Vector, editable in Inkscape/Illustrator

Performance
-----------

For large datasets:

.. code-block:: python

   # Huez has minimal overhead
   hz.use("scheme-1")
   
   # Performance tips
   plt.plot(x, y, rasterized=True)  # Rasterize if many points
   
   # Reduce DPI for exploratory work
   plt.figure(dpi=72)

Combining with Other Styles
----------------------------

Huez manages colors only:

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   import huez as hz
   
   # Apply matplotlib style for layout
   plt.style.use('seaborn-v0_8-whitegrid')
   
   # Apply Huez for colors
   hz.use("scheme-1")
   
   # Or use seaborn context
   sns.set_context("paper", font_scale=1.5)
   hz.use("lancet")

Common Pitfalls
---------------

**Pitfall 1: Applying Scheme After Plotting**

.. code-block:: python

   # ❌ Wrong order
   plt.plot(x, y)
   hz.use("scheme-1")  # Too late!

   # ✅ Correct order
   hz.use("scheme-1")
   plt.plot(x, y)

**Pitfall 2: Explicit Colors**

.. code-block:: python

   # ❌ Overrides Huez
   plt.plot(x, y, color='red')
   
   # ✅ Let Huez handle it
   plt.plot(x, y)

**Pitfall 3: Wrong Mode**

.. code-block:: python

   # ❌ Screen mode for printing
   hz.use("scheme-1", mode="screen")
   plt.savefig('paper_figure.pdf')  # May not print well
   
   # ✅ Print mode for publications
   hz.use("scheme-1", mode="print")
   plt.savefig('paper_figure.pdf')

Testing Your Figures
---------------------

**Test in Grayscale:**

.. code-block:: python

   # Save and convert to grayscale
   plt.savefig('test.png')
   
   from PIL import Image
   img = Image.open('test.png').convert('L')
   img.show()

**Test for Colorblindness:**

.. code-block:: python

   hz.use("scheme-1")
   
   # Check safety
   colors = hz.palette()
   result = hz.check_accessibility(colors)
   print(result)

**Preview Before Publishing:**

.. code-block:: python

   hz.preview("scheme-1", mode="print")

Quick Reference
---------------

.. code-block:: python

   import huez as hz
   
   # Setup
   hz.use("scheme-1")                           # Basic
   hz.use("scheme-1", mode="print")             # For print
   hz.use("scheme-1", ensure_accessible=True)   # Check accessibility
   
   # Preview
   hz.preview("scheme-1")                       # Preview scheme
   hz.list_schemes()                            # List all
   
   # Get colors
   colors = hz.palette()                        # Current palette
   cmap = hz.cmap(kind="diverging")             # Get colormap
   
   # Status
   current = hz.current_scheme()                # Current scheme name
   hz.status()                                  # Full status
   
   # Context manager
   with hz.using("lancet"):
       # Temporary scheme
       pass

Summary
-------

.. important::

   **Key Takeaways**
   
   1. Apply schemes before plotting
   2. Let Huez handle colors automatically
   3. Use appropriate modes (screen/print/presentation)
   4. Ensure colorblind accessibility
   5. Add redundant encoding for complex plots
   6. Test in grayscale before printing
   7. Use high DPI (300+) for publications

Next Steps
----------

- Explore :doc:`../intelligence/index` for automatic features
- Check :doc:`../gallery/index` for examples
- Read :doc:`../api/index` for complete reference




