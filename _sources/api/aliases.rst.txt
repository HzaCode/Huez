API Aliases and Naming Conventions
===================================

Overview
--------

For convenience and ease of use, Huez provides simplified function names at the top level
of the package. This page documents the relationship between these simplified names and
their full internal implementations.

Function Alias Mapping
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Recommended (Simplified)
     - Full Name
     - Purpose
   * - ``hz.check_accessibility()``
     - ``huez.intelligence.check_colorblind_safety()``
     - Colorblind safety check
   * - ``hz.expand_colors()``
     - ``huez.intelligence.intelligent_color_expansion()``
     - Color palette expansion
   * - ``hz.detect_colormap()``
     - ``huez.intelligence.detect_colormap_type()``
     - Colormap type detection
   * - ``hz.smart_cmap()``
     - (combined function)
     - Smart colormap selection
   * - ``hz.colors()``
     - (simplified palette access)
     - Get colors
   * - ``hz.get_colors()``
     - ``hz.colors()`` alias
     - Get colors (alternative name)
   * - ``hz.setup()``
     - ``hz.quick_setup()`` alias
     - Quick setup (alternative name)

Recommended Usage Patterns
---------------------------

For Most Users
^^^^^^^^^^^^^^

We recommend using the **simplified top-level API** for clarity and brevity:

.. code-block:: python

   import huez as hz
   
   # ✅ Recommended: Clear and concise
   hz.use("scheme-1")
   colors = hz.colors(10)
   result = hz.check_accessibility()
   expanded = hz.expand_colors(colors, 15)
   cmap_type = hz.detect_colormap(data)

This approach is:

- **Easier to type** - shorter names
- **Easier to remember** - intuitive naming
- **Consistent** - all under the ``hz`` namespace

For Advanced Users
^^^^^^^^^^^^^^^^^^

If you prefer the full function names or need direct access to internal modules:

.. code-block:: python

   from huez.intelligence import (
       intelligent_color_expansion,
       detect_colormap_type,
       check_colorblind_safety
   )
   
   # ✅ Also valid: Full names for clarity
   expanded = intelligent_color_expansion(colors, 15)
   cmap_type = detect_colormap_type(data)
   result = check_colorblind_safety(colors)

This approach is useful when:

- You want self-documenting code with explicit function names
- You're building libraries that use Huez internally
- You prefer explicit imports over namespace access

Both Are Equivalent
^^^^^^^^^^^^^^^^^^^^

**Important**: Both approaches call the same underlying functions. Choose based on your preference:

.. code-block:: python

   import huez as hz
   from huez.intelligence import intelligent_color_expansion
   
   # These two lines do exactly the same thing:
   colors_1 = hz.expand_colors(base_colors, 10)
   colors_2 = intelligent_color_expansion(base_colors, 10)
   
   assert colors_1 == colors_2  # ✓ True

Complete API Comparison
------------------------

Intelligence Features
^^^^^^^^^^^^^^^^^^^^^

**Color Expansion:**

.. code-block:: python

   # Simplified API
   import huez as hz
   expanded = hz.expand_colors(colors, n_needed=15)
   
   # Full API
   from huez.intelligence import intelligent_color_expansion
   expanded = intelligent_color_expansion(colors, n_needed=15)

**Colormap Detection:**

.. code-block:: python

   # Simplified API
   cmap_type = hz.detect_colormap(data, verbose=True)
   
   # Full API
   from huez.intelligence import detect_colormap_type
   cmap_type = detect_colormap_type(data, verbose=True)

**Accessibility Check:**

.. code-block:: python

   # Simplified API
   result = hz.check_accessibility(colors, verbose=True)
   
   # Full API
   from huez.intelligence import check_colorblind_safety
   result = check_colorblind_safety(colors, verbose=True)

**Smart Colormap:**

.. code-block:: python

   # Only available as simplified API
   import huez as hz
   cmap = hz.smart_cmap(data)

Utility Functions
^^^^^^^^^^^^^^^^^

**Getting Colors:**

.. code-block:: python

   # Three equivalent ways:
   colors = hz.palette(n=10)      # Traditional
   colors = hz.colors(10)          # Simplified
   colors = hz.get_colors(10)      # Alias

**Quick Setup:**

.. code-block:: python

   # Two equivalent ways:
   hz.quick_setup("scheme-1")
   hz.setup("scheme-1")  # Alias

Design Philosophy
-----------------

Why Simplified Names?
^^^^^^^^^^^^^^^^^^^^^

1. **Reduced Typing**: ``hz.expand_colors()`` vs ``intelligent_color_expansion()``
2. **Easier Discovery**: All functions under one namespace
3. **Better Autocomplete**: IDE suggestions are more helpful
4. **Consistent Pattern**: Similar to other popular libraries (e.g., ``np.array``, ``pd.read_csv``)

Why Keep Full Names?
^^^^^^^^^^^^^^^^^^^^

1. **Backward Compatibility**: Existing code continues to work
2. **Self-Documentation**: Function names describe what they do
3. **Advanced Use Cases**: Direct module access for library developers
4. **Explicit Imports**: Some developers prefer ``from X import Y`` style

Migration Guide
---------------

If you have existing code using full function names, you don't need to change anything.
Both styles will continue to be supported.

However, if you want to modernize your code:

**Before:**

.. code-block:: python

   from huez.intelligence import (
       intelligent_color_expansion,
       detect_colormap_type,
       check_colorblind_safety
   )
   import huez
   
   huez.use("scheme-1")
   expanded = intelligent_color_expansion(colors, 15)
   cmap_type = detect_colormap_type(data)
   result = check_colorblind_safety(colors)

**After:**

.. code-block:: python

   import huez as hz
   
   hz.use("scheme-1")
   expanded = hz.expand_colors(colors, 15)
   cmap_type = hz.detect_colormap(data)
   result = hz.check_accessibility(colors)

FAQs
----

**Q: Which style should I use?**

A: For most users, we recommend the simplified top-level API (``hz.expand_colors()``, etc.).
It's shorter and easier to use. Use the full names if you prefer more explicit code.

**Q: Are both styles equally supported?**

A: Yes! Both are first-class APIs and will be maintained long-term.

**Q: Will the simplified names change?**

A: No. Once established, API names follow semantic versioning. Breaking changes would only
occur in major version updates (e.g., 1.x → 2.x).

**Q: Can I mix both styles?**

A: Yes, but we recommend picking one style for consistency within a project.

**Q: What about performance?**

A: Both styles call the same underlying functions. There's no performance difference.

Next Steps
----------

- Browse :doc:`core` for complete API reference
- Read :doc:`../intelligence/index` for intelligence features
- Check :doc:`../user_guide/index` for usage examples


