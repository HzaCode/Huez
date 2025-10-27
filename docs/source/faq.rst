Frequently Asked Questions
===========================

General Questions
-----------------

What is Huez?
^^^^^^^^^^^^^

Huez is the first intelligent color management system for Python visualization. It automatically manages colors across matplotlib, seaborn, plotly, altair, and plotnine with built-in intelligence for color expansion, colormap detection, and accessibility checking.

Why do I need Huez?
^^^^^^^^^^^^^^^^^^^

**You need Huez if you:**

- Use multiple visualization libraries (matplotlib + seaborn + plotly)
- Want consistent colors across all your plots without manual configuration
- Need to ensure your plots are colorblind-accessible (8% of population)
- Submit to journals that require print-friendly figures
- Plot more than 10 categories and colors start repeating
- Want automatic sequential/diverging colormap selection for heatmaps

**Traditional approach:**

.. code-block:: python

   # Manual configuration for each library
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#E64B35', '#4DBBD5'])
   sns.set_palette(['#E64B35', '#4DBBD5'])
   # Still need to configure plotly, altair separately...
   # No color expansion, no accessibility checks

**With Huez:**

.. code-block:: python

   import huez as hz
   
   hz.use("scheme-1")  # One line for all libraries + intelligence

Is Huez free?
^^^^^^^^^^^^^

Yes! Huez is open-source and licensed under MIT. It's completely free for academic and commercial use.

Installation & Setup
--------------------

How do I install Huez?
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install huez[all]

For minimal installation without optional dependencies:

.. code-block:: bash

   pip install huez

Which Python versions are supported?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Huez supports Python 3.7 and above.

Do I need to install all visualization libraries?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No! Huez only requires the libraries you actually use. Install what you need:

.. code-block:: bash

   pip install huez matplotlib seaborn  # Just matplotlib + seaborn
   pip install huez[all]                # All supported libraries

Usage Questions
---------------

How do I apply a color scheme?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import huez as hz
   
   # Before any plotting
   hz.use("scheme-1")
   
   # Then plot normally
   import matplotlib.pyplot as plt
   plt.plot(x, y)

Must I call hz.use() before every plot?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No! Call ``hz.use()`` once at the beginning of your script or notebook. It applies globally to all subsequent plots.

.. code-block:: python

   import huez as hz
   import matplotlib.pyplot as plt
   
   hz.use("scheme-1")  # Once at the start
   
   # All these use the same scheme
   plt.figure()
   plt.plot(x, y1)
   
   plt.figure()
   plt.plot(x, y2)

Can I use explicit colors like color='red'?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**You can, but you shouldn't** if you want Huez's intelligent features.

.. code-block:: python

   hz.use("scheme-1")
   
   # ❌ This overrides Huez
   plt.plot(x, y, color='red')
   
   # ✅ Let Huez handle colors
   plt.plot(x, y, label='Data')

**Reason:** Explicit colors bypass intelligent features like color expansion, accessibility checking, and print optimization.

How do I preview a scheme before using it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import huez as hz
   
   # Preview scheme
   hz.preview("scheme-1")
   
   # Preview in print mode
   hz.preview("scheme-1", mode="print")
   
   # List all available schemes
   print(hz.list_schemes())

Features & Capabilities
-----------------------

Does Huez work with all plot types?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes! Huez works with:

- ✅ Line plots, scatter plots, bar charts
- ✅ Heatmaps, contour plots
- ✅ Histograms, box plots, violin plots
- ✅ 3D plots, subplots, facets
- ✅ Any plot type from matplotlib, seaborn, plotly, altair, plotnine

Can Huez handle more than 10 categories?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Yes!** This is one of Huez's key features.

.. code-block:: python

   hz.use("scheme-1")
   
   # Plot 15 categories - Huez auto-expands to 15 distinct colors
   for i in range(15):
       plt.plot(x, y + i*0.5, label=f'Category {i+1}')

**Technology:** LAB color space interpolation generates perceptually distinct colors.

How does automatic colormap detection work?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Huez analyzes your data distribution:

.. code-block:: python

   import seaborn as sns
   import numpy as np
   
   hz.use("scheme-1")
   
   # Correlation matrix: values from -1 to +1
   corr = np.corrcoef(data)
   sns.heatmap(corr)  # Auto-detects diverging colormap (coolwarm)
   
   # Temperature data: values from 0 to 100
   temp = np.random.uniform(0, 100, (10, 10))
   sns.heatmap(temp)  # Auto-detects sequential colormap (viridis)

**Detection logic:**

- Data centered at zero with positive/negative values → Diverging
- Data all positive or all negative → Sequential

What is colorblind accessibility checking?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Huez simulates how your colors appear to people with color vision deficiency:

.. code-block:: python

   # Automatic checking
   hz.use("scheme-1", ensure_accessible=True)
   
   # Manual checking
   result = hz.check_accessibility("npg")
   if not result['safe']:
       print(result['warnings'])  # Specific issues
       print(result['suggestions'])  # Recommended alternatives

**Checks for:**

- Deuteranopia (red-green colorblindness, 5% of males)
- Protanopia (red-green colorblindness, 2% of males)
- Tritanopia (blue-yellow colorblindness, <1%)

Publication & Printing
----------------------

Which mode should I use for journal submission?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1", mode="print", ensure_accessible=True)

**Reasons:**

- ``mode="print"`` optimizes colors for black & white printing
- ``ensure_accessible=True`` ensures 8% of readers (colorblind) can read your figures
- Meets most journal requirements

Will my figures print well in black & white?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes! The ``mode="print"`` specifically optimizes for grayscale conversion:

.. code-block:: python

   hz.use("scheme-1", mode="print")
   
   plt.plot(x, y1, label='Control')
   plt.plot(x, y2, label='Treatment')
   plt.savefig('figure.pdf', dpi=300)

**Result:** Colors convert to well-separated gray values (0.00 to 0.62 range).

What DPI should I use for publications?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   hz.use("scheme-1", mode="print")
   
   fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=300)
   # ... plot ...
   plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')

**Recommendations:**

- **Journals:** 300-600 DPI
- **Presentations:** 150 DPI
- **Web:** 72-96 DPI

Can I use Huez with Nature/Science/Cell journals?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Absolutely!** Huez includes journal-specific styles:

.. code-block:: python

   hz.use("npg")      # Nature Publishing Group
   hz.use("aaas")     # Science (AAAS)
   hz.use("lancet")   # The Lancet
   hz.use("nejm")     # New England Journal of Medicine
   hz.use("jama")     # JAMA

These schemes are based on official journal style guides.

Advanced Usage
--------------

Can I create custom color schemes?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes! Create a YAML configuration file:

.. code-block:: yaml

   # my_scheme.yaml
   version: 1
   default_scheme: my_custom
   schemes:
     my_custom:
       title: "My Custom Scheme"
       palettes:
         discrete: ["#E64B35", "#4DBBD5", "#00A087"]
         sequential: "viridis"
         diverging: "coolwarm"
       figure:
         dpi: 300
       fonts:
         family: "Arial"
         size: 10

Load and use:

.. code-block:: python

   hz.load_config("my_scheme.yaml")
   hz.use("my_custom")

Can I temporarily switch schemes?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, use the context manager:

.. code-block:: python

   hz.use("scheme-1")
   
   plt.plot(x, y1)  # Uses scheme-1
   
   with hz.using("lancet"):
       plt.plot(x, y2)  # Temporarily uses lancet
   
   plt.plot(x, y3)  # Back to scheme-1

How do I get colors for manual use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get current palette
   colors = hz.palette()
   print(colors)  # ['#E64B35', '#4DBBD5', '#00A087', ...]
   
   # Get specific number of colors
   colors_10 = hz.get_colors(n=10)
   
   # Get a colormap
   cmap = hz.cmap(kind="diverging")
   plt.imshow(data, cmap=cmap)

Can I disable intelligent features?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, but not recommended:

.. code-block:: python

   hz.use("scheme-1", 
          auto_expand=False,        # Disable color expansion
          smart_cmap=False,          # Disable colormap detection
          ensure_accessible=False)   # Disable accessibility checks

**Why you might want this:** Maximum control, specific requirements.

**Why you shouldn't:** You lose Huez's main advantages.

Performance & Compatibility
----------------------------

Does Huez slow down my plotting?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**No.** Huez has minimal overhead:

- Color expansion: <10ms (once at initialization)
- Colormap detection: <5ms (per heatmap)
- Accessibility check: <50ms (once at initialization)

**Total:** Typically <100ms, imperceptible to users.

Is Huez compatible with Jupyter notebooks?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Yes!** Huez works perfectly in:

- Jupyter Notebook
- JupyterLab
- Google Colab
- VSCode notebooks

.. code-block:: python

   # In a Jupyter cell
   import huez as hz
   import matplotlib.pyplot as plt
   
   hz.use("scheme-1")
   plt.plot(x, y)
   plt.show()

Can I use Huez with plt.style.use()?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes! Huez manages colors only, so you can combine:

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   plt.style.use('seaborn-v0_8-whitegrid')  # Layout style
   hz.use("scheme-1")                        # Colors

Does Huez work with pandas plotting?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Yes!** Pandas uses matplotlib backend:

.. code-block:: python

   import pandas as pd
   import huez as hz
   
   hz.use("scheme-1")
   
   df.plot(kind='line')
   df.plot(kind='bar')
   df.plot(kind='scatter', x='A', y='B', c='C')

Troubleshooting
---------------

Huez doesn't seem to work. What's wrong?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Checklist:**

1. Did you call ``hz.use()`` **before** plotting?
   
   .. code-block:: python
   
      # ❌ Wrong order
      plt.plot(x, y)
      hz.use("scheme-1")  # Too late!
      
      # ✅ Correct order
      hz.use("scheme-1")
      plt.plot(x, y)

2. Are you using explicit colors?
   
   .. code-block:: python
   
      # ❌ Overrides Huez
      plt.plot(x, y, color='red')
      
      # ✅ Let Huez handle it
      plt.plot(x, y)

3. Is the library supported?
   
   .. code-block:: python
   
      # Check supported libraries
      import huez
      print(huez.supported_libraries())

My colors still look wrong after applying Huez
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Try resetting matplotlib:

.. code-block:: python

   import matplotlib.pyplot as plt
   import huez as hz
   
   plt.rcdefaults()  # Reset to defaults
   hz.use("scheme-1")  # Apply Huez

Or restart your notebook kernel if using Jupyter.

How do I report a bug or request a feature?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**GitHub Issues:** https://github.com/hzacode/huez/issues

**Before reporting:**

1. Check if issue already exists
2. Provide minimal reproducible example
3. Include Huez version: ``import huez; print(huez.__version__)``
4. Include environment info (Python version, OS)

Where can I get help?
^^^^^^^^^^^^^^^^^^^^^

**Resources:**

- 📖 Documentation: https://huez.readthedocs.io
- 💬 GitHub Discussions: https://github.com/hzacode/huez/discussions
- 🐛 Bug Reports: https://github.com/hzacode/huez/issues
- 📧 Email: (add your contact)

Comparison with Other Tools
----------------------------

How is Huez different from seaborn.set_palette()?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - seaborn.set_palette()
     - Huez
   * - Affects multiple libraries
     - ❌ Seaborn only
     - ✅ 5 libraries
   * - Color expansion
     - 🟡 Simple cycle
     - ✅ LAB interpolation
   * - Colormap detection
     - ❌ Manual
     - ✅ Automatic
   * - Accessibility checking
     - ❌ None
     - ✅ Built-in
   * - Print optimization
     - ❌ None
     - ✅ mode="print"

Why not just use matplotlib styles?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Matplotlib styles handle layout, not intelligent color management:

.. code-block:: python

   # matplotlib style: layout only
   plt.style.use('seaborn-v0_8')
   
   # Huez: intelligent colors
   hz.use("scheme-1")
   
   # Best: combine both
   plt.style.use('seaborn-v0_8-whitegrid')
   hz.use("scheme-1")

What about palettable or colorbrewer?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**palettable/colorbrewer:** Static color palette libraries

- ✅ Good: Many pre-defined palettes
- ❌ No cross-library integration
- ❌ No intelligent expansion
- ❌ No accessibility checking
- ❌ Manual application per plot

**Huez:** Intelligent color management system

- ✅ One-line setup across all libraries
- ✅ Automatic color expansion
- ✅ Smart colormap detection
- ✅ Built-in accessibility
- ✅ Print optimization

**Use together:** You can use palettable palettes with Huez!

.. code-block:: python

   from palettable.cartocolors.qualitative import Bold_10
   
   hz.use_palette(Bold_10.hex_colors)

Citations & Credits
-------------------

How do I cite Huez in my paper?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bibtex

   @software{huez2025,
     author = {Ang},
     title = {Huez: An Intelligent Color Management System for Python Visualization},
     year = {2025},
     url = {https://github.com/hzacode/huez},
     version = {0.0.5}
   }

**Text citation:**

"Color schemes were managed using Huez (v0.0.5), an intelligent color management system for Python visualization (https://github.com/hzacode/huez)."

What algorithms does Huez use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Color Expansion:**

- LAB color space interpolation (CIE 1976)
- Perceptually uniform color generation

**Colorblind Simulation:**

- Brettel et al. (1997) algorithm
- Delta E (CIE76) color difference metric

**Accessibility:**

- WCAG 2.0 contrast ratio standards
- Minimum contrast thresholds

**References:**

- Brettel, H., Viénot, F., & Mollon, J. D. (1997). Computerized simulation of color appearance for dichromats. *Journal of the Optical Society of America A*, 14(10), 2647-2655.
- CIE. (1976). Colorimetry. *CIE Publication* 15.2.

Still Have Questions?
---------------------

**Check these resources:**

- :doc:`quickstart` - Get started in 5 minutes
- :doc:`user_guide/index` - Comprehensive tutorials
- :doc:`api/index` - Complete API reference
- :doc:`gallery/index` - Visual examples

**Or ask the community:**

- GitHub Discussions: https://github.com/hzacode/huez/discussions
- Open an issue: https://github.com/hzacode/huez/issues



