Color Modes
===========

Huez supports three output modes optimized for different media: **screen**, **print**, and **presentation**.

Overview
--------

Different output media have different color requirements:

- **Screen**: Optimized for digital displays (default)
- **Print**: Grayscale-friendly for black & white printing
- **Presentation**: High contrast for projectors and large screens

Switching Modes
---------------

Change modes using the ``mode`` parameter:

.. code-block:: python

   import huez as hz
   
   # Screen mode (default)
   hz.use("scheme-1", mode="screen")
   
   # Print mode
   hz.use("scheme-1", mode="print")
   
   # Presentation mode
   hz.use("scheme-1", mode="presentation")

Screen Mode
-----------

The default mode, optimized for digital displays.

**Characteristics:**

- Full color spectrum
- Optimized for RGB displays
- Standard contrast levels
- Default for exploratory analysis

**Usage:**

.. code-block:: python

   hz.use("scheme-1", mode="screen")
   # or simply
   hz.use("scheme-1")  # screen is default

**Use Cases:**

- Jupyter notebooks
- Interactive dashboards
- Web visualization
- Exploratory data analysis

Print Mode
----------

Optimized for printing, especially black & white printing.

.. image:: /_static/features/comparison_print_mode.png
   :width: 80%
   :align: center
   :alt: Print mode comparison

|

**Characteristics:**

- Colors selected for distinct grayscale values
- When printed in B&W, lines/bars remain distinguishable
- Optimized lightness distribution
- CMYK color space consideration

**Usage:**

.. code-block:: python

   hz.use("scheme-1", mode="print")

**Technical Details:**

In print mode, Huez ensures that colors have significantly different lightness values:

.. code-block:: text

   Screen Mode Grayscale Values:  [0.30, 0.45, 0.52, 0.58, 0.63, 0.70]
   Print Mode Grayscale Values:   [0.00, 0.20, 0.35, 0.50, 0.65, 0.80]
   
   Print mode has wider separation → better B&W distinction

**Example:**

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   hz.use("scheme-1", mode="print")
   
   # Plot multiple lines
   for i in range(6):
       plt.plot(x, y + i*0.5, label=f'Series {i+1}', linewidth=2)
   
   plt.legend()
   plt.title('Optimized for Grayscale Printing')
   
   # Save for print
   plt.savefig('figure_print.pdf', dpi=300, bbox_inches='tight')

**Best Practices for Print:**

.. code-block:: python

   hz.use("scheme-1", mode="print")
   
   # Use thicker lines
   plt.plot(x, y, linewidth=2)
   
   # Add markers for additional distinction
   plt.plot(x, y, marker='o', markersize=5, linewidth=2)
   
   # Use different line styles
   plt.plot(x, y1, linestyle='-', linewidth=2)
   plt.plot(x, y2, linestyle='--', linewidth=2)
   plt.plot(x, y3, linestyle='-.', linewidth=2)

**Use Cases:**

- Journal article submissions
- Print publications
- PDF reports
- Black & white printing scenarios

Presentation Mode
-----------------

Optimized for presentations and projectors.

**Characteristics:**

- High contrast colors
- Larger visual elements
- Enhanced visibility from distance
- Reduced number of colors (focus on clarity)

**Usage:**

.. code-block:: python

   hz.use("scheme-1", mode="presentation")

**Visual Adjustments:**

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   hz.use("scheme-1", mode="presentation")
   
   # Larger figure size
   plt.figure(figsize=(12, 8))
   
   # Thicker lines for visibility
   plt.plot(x, y1, linewidth=3, label='Data 1')
   plt.plot(x, y2, linewidth=3, label='Data 2')
   
   # Larger fonts
   plt.xlabel('X axis', fontsize=16)
   plt.ylabel('Y axis', fontsize=16)
   plt.title('Presentation Title', fontsize=20)
   plt.legend(fontsize=14)
   
   plt.tight_layout()
   plt.show()

**Recommended Settings:**

.. code-block:: python

   # Complete presentation setup
   hz.use("scheme-1", mode="presentation")
   
   import matplotlib as mpl
   mpl.rcParams['font.size'] = 14
   mpl.rcParams['axes.labelsize'] = 16
   mpl.rcParams['axes.titlesize'] = 20
   mpl.rcParams['xtick.labelsize'] = 12
   mpl.rcParams['ytick.labelsize'] = 12
   mpl.rcParams['legend.fontsize'] = 14
   mpl.rcParams['lines.linewidth'] = 3
   mpl.rcParams['lines.markersize'] = 8

**Use Cases:**

- Conference presentations
- Lecture slides
- Large screen displays
- Video tutorials

Mode Comparison
---------------

.. list-table:: Mode Comparison
   :header-rows: 1
   :widths: 20 25 25 30

   * - Feature
     - Screen
     - Print
     - Presentation
   * - Color Range
     - Full spectrum
     - Grayscale-optimized
     - High contrast
   * - Number of Colors
     - Standard (10+)
     - Standard (10+)
     - Reduced (6-8)
   * - Contrast Level
     - Standard
     - High (for B&W)
     - Very High
   * - Visual Elements
     - Standard
     - Thicker recommended
     - Thick required
   * - Best For
     - Digital display
     - Paper/PDF
     - Projectors

Previewing Modes
----------------

Preview how a scheme looks in different modes:

.. code-block:: python

   import huez as hz
   
   # Preview all modes
   hz.preview("scheme-1", mode="screen")
   hz.preview("scheme-1", mode="print")
   hz.preview("scheme-1", mode="presentation")

Switching Between Modes
------------------------

You can switch modes without restarting your Python session:

.. code-block:: python

   # Start with screen mode
   hz.use("scheme-1", mode="screen")
   
   # Create exploratory plots...
   plt.plot(x, y)
   plt.show()
   
   # Switch to print mode for final figure
   hz.use("scheme-1", mode="print")
   
   # Create publication-ready plot
   fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
   ax.plot(x, y, linewidth=2)
   plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')

Mode-Specific Recommendations
------------------------------

**For Screen:**

.. code-block:: python

   hz.use("scheme-1", mode="screen")
   
   # Standard settings work well
   plt.figure(figsize=(8, 6))
   plt.plot(x, y)

**For Print:**

.. code-block:: python

   hz.use("scheme-1", mode="print")
   
   # Ensure grayscale distinction
   plt.figure(figsize=(6, 4), dpi=300)
   
   # Thicker lines
   for i, data in enumerate([y1, y2, y3]):
       plt.plot(x, data, linewidth=2, marker='o', 
                markersize=4, markevery=5, label=f'Data {i+1}')
   
   plt.legend()
   plt.savefig('print_figure.pdf', dpi=300, bbox_inches='tight')

**For Presentation:**

.. code-block:: python

   hz.use("scheme-1", mode="presentation")
   
   # Large and bold
   plt.figure(figsize=(12, 8))
   
   # Very thick lines
   plt.plot(x, y1, linewidth=4, label='Data 1')
   plt.plot(x, y2, linewidth=4, label='Data 2')
   
   # Large fonts
   plt.xlabel('X axis', fontsize=20)
   plt.ylabel('Y axis', fontsize=20)
   plt.title('Clear Title', fontsize=24, fontweight='bold')
   plt.legend(fontsize=16)
   plt.grid(True, alpha=0.3)

Complete Workflow Example
--------------------------

A complete workflow using all three modes:

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   import numpy as np
   
   # Generate data
   x = np.linspace(0, 10, 100)
   y1 = np.sin(x)
   y2 = np.cos(x)
   
   # 1. Exploratory Analysis (Screen)
   hz.use("scheme-1", mode="screen")
   plt.figure()
   plt.plot(x, y1, label='sin(x)')
   plt.plot(x, y2, label='cos(x)')
   plt.legend()
   plt.title('Exploratory Analysis')
   plt.show()
   
   # 2. Publication Figure (Print)
   hz.use("scheme-1", mode="print")
   fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
   ax.plot(x, y1, linewidth=2, marker='o', markevery=10, 
           markersize=4, label='sin(x)')
   ax.plot(x, y2, linewidth=2, marker='s', markevery=10, 
           markersize=4, label='cos(x)')
   ax.set_xlabel('x')
   ax.set_ylabel('y')
   ax.legend()
   ax.set_title('Trigonometric Functions')
   plt.savefig('paper_figure.pdf', dpi=300, bbox_inches='tight')
   plt.close()
   
   # 3. Presentation Slide (Presentation)
   hz.use("scheme-1", mode="presentation")
   fig, ax = plt.subplots(figsize=(12, 8))
   ax.plot(x, y1, linewidth=4, label='sin(x)')
   ax.plot(x, y2, linewidth=4, label='cos(x)')
   ax.set_xlabel('x', fontsize=20)
   ax.set_ylabel('y', fontsize=20)
   ax.legend(fontsize=18)
   ax.set_title('Trigonometric Functions', fontsize=24, fontweight='bold')
   ax.grid(True, alpha=0.3, linewidth=1.5)
   plt.savefig('presentation_slide.png', dpi=150, bbox_inches='tight')
   plt.show()

Tips
----

.. tip::

   **Choose Mode Based on Final Output**
   
   - Working in Jupyter? → ``mode="screen"``
   - Submitting to journal? → ``mode="print"``
   - Making slides? → ``mode="presentation"``

.. note::

   **Mode Doesn't Change Data**
   
   Only visual appearance changes. Your data and computations remain the same.

.. warning::

   **Test Print Mode in Grayscale**
   
   Always preview your figures in grayscale before printing:
   
   .. code-block:: python
   
      # In matplotlib, convert to grayscale temporarily
      from PIL import Image
      import matplotlib.pyplot as plt
      
      plt.savefig('temp.png', dpi=150)
      img = Image.open('temp.png').convert('L')
      img.show()

Next Steps
----------

- Learn about :doc:`custom_schemes` to create your own modes
- Read :doc:`best_practices` for mode-specific tips
- Check :doc:`../intelligence/index` for automatic optimizations


