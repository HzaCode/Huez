Colorblind Accessibility
========================

Ensure your visualizations are accessible to 8% of the population with color vision deficiency.

The Problem
-----------

**8% of males** (1 in 12) and **0.5% of females** have color vision deficiency (CVD).

.. image:: /_static/features/comparison_colorblind_safety.png
   :width: 85%
   :align: center
   :alt: Colorblind safety comparison

|

**Top Row (NPG Palette)**: 
- Normal vision: Colors distinct
- Deuteranopia (green-blind): Red/green bars indistinguishable
- Result: ✗ NOT colorblind-safe

**Bottom Row (Okabe-Ito Palette)**:
- All 4 views: Colors remain distinct
- Result: ✓ Colorblind-safe

Why This Matters
----------------

**Accessibility is Essential:**

- **8% of readers** may misinterpret your figures
- **Ethical responsibility**: Inclusive science communication
- **Journal requirements**: Many require colorblind-safe figures
- **Better for everyone**: High-contrast colors benefit all readers

Types of Color Vision Deficiency
---------------------------------

Protanopia (Red-Blind)
^^^^^^^^^^^^^^^^^^^^^^

- **Prevalence**: ~1% of males
- **Missing**: L (long-wavelength) cones
- **Confused colors**: Red/green, red/brown, red/orange

Deuteranopia (Green-Blind)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Prevalence**: ~1% of males **(most common)**
- **Missing**: M (medium-wavelength) cones
- **Confused colors**: Green/red, green/brown, blue/purple

Tritanopia (Blue-Blind)
^^^^^^^^^^^^^^^^^^^^^^^

- **Prevalence**: ~0.001% (rare)
- **Missing**: S (short-wavelength) cones
- **Confused colors**: Blue/green, yellow/violet

Detection Algorithm
-------------------

Huez checks colorblind safety using:

1. **Color Blindness Simulation**: Brettel et al. (1997) algorithm
2. **Contrast Calculation**: WCAG 2.0 standards
3. **Perceptual Distance**: Delta E color difference

Step 1: Simulate CVD
^^^^^^^^^^^^^^^^^^^^

Transform colors as seen by colorblind individuals:

.. code-block:: python

   def simulate_colorblind_vision(colors, cvd_type="deuteranopia"):
       """Apply CVD transformation matrix"""
       
       # Deuteranopia matrix (simplified)
       matrix = [
           [0.625, 0.375, 0.0],
           [0.7, 0.3, 0.0],
           [0.0, 0.3, 0.7]
       ]
       
       # Apply to each color
       simulated = []
       for color in colors:
           rgb = hex_to_rgb(color)
           new_r = matrix[0][0]*rgb[0] + matrix[0][1]*rgb[1] + matrix[0][2]*rgb[2]
           new_g = matrix[1][0]*rgb[0] + matrix[1][1]*rgb[1] + matrix[1][2]*rgb[2]
           new_b = matrix[2][0]*rgb[0] + matrix[2][1]*rgb[1] + matrix[2][2]*rgb[2]
           simulated.append(rgb_to_hex((new_r, new_g, new_b)))
       
       return simulated

Step 2: Calculate Contrast
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use WCAG 2.0 contrast ratio:

.. code-block:: python

   def calculate_color_contrast(color1, color2):
       """WCAG 2.0 contrast ratio"""
       l1 = relative_luminance(color1)
       l2 = relative_luminance(color2)
       
       contrast = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
       return contrast  # Range: 1.0 to 21.0

**WCAG Standards:**

- **AA (minimum)**: 3.0:1 for large text/graphics
- **AAA (enhanced)**: 4.5:1 for large text, 7.0:1 for normal text

Step 3: Calculate Perceptual Distance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simplified Delta E:

.. code-block:: python

   def calculate_perceptual_distance(color1, color2):
       """Weighted Euclidean distance in RGB"""
       rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
       
       dr = (rgb1[0] - rgb2[0]) / 255.0
       dg = (rgb1[1] - rgb2[1]) / 255.0
       db = (rgb1[2] - rgb2[2]) / 255.0
       
       # Weight green more (human eye sensitivity)
       distance = ((2*dr**2 + 4*dg**2 + 3*db**2) ** 0.5) * 100
       return distance

**Interpretation:**

- < 1.0: Imperceptible difference
- 1.0 - 2.0: Perceptible if looking carefully
- 2.0 - 10.0: Notable difference
- **> 10.0**: Very obvious (threshold used by Huez)

Usage
-----

Automatic Checking
^^^^^^^^^^^^^^^^^^

Enable automatic checking:

.. code-block:: python

   import huez as hz
   
   # Automatic colorblind safety check
   hz.use("scheme-1", ensure_accessible=True)
   
   # If not safe, shows warning with suggestions

Manual Checking
^^^^^^^^^^^^^^^

Check any color scheme:

.. code-block:: python

   import huez as hz
   
   colors = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F"]
   result = hz.check_accessibility(colors, verbose=True)
   
   if not result['safe']:
       print("⚠️ Not colorblind-safe!")
       print("\nWarnings:")
       for warning in result['warnings']:
           print(f"  - {warning}")
       
       print("\nSuggestions:")
       for suggestion in result['suggestions']:
           print(f"  • {suggestion}")

.. note::

   The top-level function ``hz.check_accessibility()`` is equivalent to
   ``huez.intelligence.check_colorblind_safety()``. We recommend using
   the shorter name for most use cases.

Simulation
^^^^^^^^^^

Visualize how colors appear to colorblind individuals:

.. code-block:: python

   from huez.intelligence import simulate_colorblind_vision
   import matplotlib.pyplot as plt
   import matplotlib.patches as mpatches
   
   colors = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F"]
   
   fig, axes = plt.subplots(4, 1, figsize=(10, 8))
   views = [
       ("Normal Vision", colors),
       ("Protanopia", simulate_colorblind_vision(colors, "protanopia")),
       ("Deuteranopia", simulate_colorblind_vision(colors, "deuteranopia")),
       ("Tritanopia", simulate_colorblind_vision(colors, "tritanopia"))
   ]
   
   for ax, (title, palette) in zip(axes, views):
       for i, color in enumerate(palette):
           ax.add_patch(mpatches.Rectangle((i, 0), 1, 1, 
                                            facecolor=color, edgecolor='black'))
       ax.set_xlim(0, len(palette))
       ax.set_ylim(0, 1)
       ax.set_title(title)
       ax.axis('off')
   
   plt.tight_layout()
   plt.show()

Example Output
--------------

**NPG Palette (NOT safe):**

.. code-block:: text

   ============================================================
   Colorblind Safety Check Results
   ============================================================
   
   ⚠ Color scheme may not be accessible to some users:
     - protanopia: 6 color pairs may be hard to distinguish
     - deuteranopia: 6 color pairs may be hard to distinguish
     - tritanopia: 10 color pairs may be hard to distinguish
   
   Detailed Analysis:
   
     protanopia (red-blind): ✗ FAIL
       Min contrast: 1.24 (threshold: 3.00)
       Min distance: 5.67 (threshold: 10.00)
   
     deuteranopia (green-blind): ✗ FAIL
       Min contrast: 1.18 (threshold: 3.00)
       Min distance: 4.92 (threshold: 10.00)
   
     tritanopia (blue-blind): ✗ FAIL
       Min contrast: 1.45 (threshold: 3.00)
       Min distance: 7.83 (threshold: 10.00)
   
   Suggestions:
     • Consider using a colorblind-safe palette like 'okabe-ito' or 'paul-tol-bright'
     • Add additional visual encodings (markers, line styles, textures)
     • Increase color contrast by adjusting lightness values
   ============================================================

**Okabe-Ito Palette (SAFE):**

.. code-block:: text

   ✓ Color scheme is colorblind-safe for all CVD types!
   
   Detailed Analysis:
   
     protanopia (red-blind): ✓ PASS
       Min contrast: 3.24 (threshold: 3.00)
       Min distance: 15.67 (threshold: 10.00)
   
     deuteranopia (green-blind): ✓ PASS
       Min contrast: 3.18 (threshold: 3.00)
       Min distance: 14.92 (threshold: 10.00)
   
     tritanopia (blue-blind): ✓ PASS
       Min contrast: 4.45 (threshold: 3.00)
       Min distance: 18.83 (threshold: 10.00)

Colorblind-Safe Palettes
-------------------------

Huez includes pre-vetted colorblind-safe palettes:

Okabe-Ito (8 colors)
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("okabe-ito")

- Specifically designed for colorblindness
- 8 colors, all highly distinct
- Most reliable choice

Paul Tol Bright (7 colors)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("paul-tol-bright")

- Bright, vibrant colors
- Good for presentations
- 7 colors

Paul Tol Vibrant (7 colors)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("paul-tol-vibrant")

- Higher saturation than Bright
- Excellent distinction
- 7 colors

Best Practices
--------------

Use Redundant Encoding
^^^^^^^^^^^^^^^^^^^^^^^

**Don't rely on color alone:**

.. code-block:: python

   hz.use("scheme-1")
   
   # ✅ Good: Color + markers
   plt.plot(x, y1, marker='o', markevery=5, label='Control')
   plt.plot(x, y2, marker='s', markevery=5, label='Treatment')
   
   # ✅ Good: Color + line styles
   plt.plot(x, y1, linestyle='-', label='Observed')
   plt.plot(x, y2, linestyle='--', label='Predicted')
   
   # ✅ Good: Color + textures (bar plots)
   plt.bar(x, y1, hatch='//', label='Group A')
   plt.bar(x, y2, hatch='\\\\', label='Group B')

Choose High-Contrast Colors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prefer large lightness differences:

.. code-block:: python

   # ✅ Good: Light vs. dark
   colors_good = ["#FFFF00", "#0000FF"]  # Yellow vs. blue
   
   # ❌ Bad: Similar lightness
   colors_bad = ["#FF0000", "#00FF00"]   # Red vs. green

For Heatmaps
^^^^^^^^^^^^

Use colorblind-safe colormaps:

.. code-block:: python

   hz.use("scheme-1")
   
   # ✅ Good: Viridis (colorblind-safe)
   cmap = hz.cmap(kind="sequential")
   sns.heatmap(data, cmap=cmap)
   
   # ✅ Good: Coolwarm for diverging
   cmap = hz.cmap(kind="diverging")
   sns.heatmap(correlation, cmap=cmap, center=0)

Avoid Red-Green
^^^^^^^^^^^^^^^^

Never use red-green color pairs:

.. code-block:: python

   # ❌ BAD: Red-green (deuteranopia cannot distinguish)
   plt.plot(x, y1, color='red', label='Positive')
   plt.plot(x, y2, color='green', label='Negative')
   
   # ✅ GOOD: Blue-orange or blue-red
   hz.use("scheme-1")  # Uses blue-red palette
   plt.plot(x, y1, label='Positive')
   plt.plot(x, y2, label='Negative')

Test Your Figures
^^^^^^^^^^^^^^^^^

Always test in simulated colorblind view:

.. code-block:: python

   from huez.intelligence import check_colorblind_safety
   
   # Before finalizing publication
   colors = hz.palette()
   result = check_colorblind_safety(colors, verbose=True)
   
   assert result['safe'], "Colors not colorblind-safe!"

Configuration
-------------

Configure thresholds:

.. code-block:: python

   from huez.intelligence import check_colorblind_safety
   
   # Stricter thresholds
   result = check_colorblind_safety(
       colors,
       min_contrast=4.5,    # AAA standard
       min_distance=15.0,   # Higher threshold
       verbose=True
   )

Or in config file:

.. code-block:: yaml

   schemes:
     my_scheme:
       intelligence:
         ensure_accessible: true
         min_contrast: 4.5
         colorblind_threshold: 15.0

API Reference
-------------

.. autofunction:: huez.intelligence.check_colorblind_safety
.. autofunction:: huez.intelligence.simulate_colorblind_vision

Further Reading
---------------

- `Color Universal Design (CUD) <https://jfly.uni-koeln.de/color/>`_
- `WCAG 2.0 Contrast Guidelines <https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html>`_
- Okabe & Ito (2008). "Color Universal Design"
- Brettel et al. (1997). "Computerized simulation of color appearance for dichromats"

Next Steps
----------

- Explore colorblind-safe palettes in :doc:`../gallery/palettes`
- Learn about :doc:`color_expansion` for many categories
- Read :doc:`../user_guide/best_practices` for accessibility tips


