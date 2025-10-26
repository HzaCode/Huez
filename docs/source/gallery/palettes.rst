Color Palettes
==============

All available color palettes in Huez.

Journal Styles
--------------

.. grid:: 3
   :gutter: 2

   .. grid-item::
      .. image:: /_static/palettes/npg_palette.png
         :width: 100%
      
      **NPG**
      
      Nature Publishing Group
      
      .. code-block:: python
      
         hz.use("npg")

   .. grid-item::
      .. image:: /_static/palettes/lancet_palette.png
         :width: 100%
      
      **Lancet**
      
      The Lancet Journal
      
      .. code-block:: python
      
         hz.use("lancet")

   .. grid-item::
      .. image:: /_static/palettes/nejm_palette.png
         :width: 100%
      
      **NEJM**
      
      New England Journal of Medicine
      
      .. code-block:: python
      
         hz.use("nejm")

   .. grid-item::
      .. image:: /_static/palettes/aaas_palette.png
         :width: 100%
      
      **AAAS**
      
      Science/AAAS
      
      .. code-block:: python
      
         hz.use("aaas")

   .. grid-item::
      .. image:: /_static/palettes/jama_palette.png
         :width: 100%
      
      **JAMA**
      
      Journal of the American Medical Association
      
      .. code-block:: python
      
         hz.use("jama")

   .. grid-item::
      .. image:: /_static/palettes/bmj_palette.png
         :width: 100%
      
      **BMJ**
      
      British Medical Journal
      
      .. code-block:: python
      
         hz.use("bmj")

Colorblind-Safe Palettes
-------------------------

.. grid:: 3
   :gutter: 2

   .. grid-item::
      .. image:: /_static/palettes/okabe-ito_palette.png
         :width: 100%
      
      **Okabe-Ito**
      
      8 colors, maximum distinction
      
      .. code-block:: python
      
         hz.use("okabe-ito")

   .. grid-item::
      .. image:: /_static/palettes/paul-tol-bright_palette.png
         :width: 100%
      
      **Paul Tol Bright**
      
      7 bright colors
      
      .. code-block:: python
      
         hz.use("paul-tol-bright")

   .. grid-item::
      .. image:: /_static/palettes/paul-tol-vibrant_palette.png
         :width: 100%
      
      **Paul Tol Vibrant**
      
      7 vibrant colors
      
      .. code-block:: python
      
         hz.use("paul-tol-vibrant")

Usage
-----

Preview any palette:

.. code-block:: python

   import huez as hz
   
   # Preview palette
   hz.preview("npg")
   
   # List all palettes
   print(hz.list_schemes())
   
   # Use a palette
   hz.use("lancet")

Next Steps
----------

- See :doc:`comparisons` for before/after examples
- Read :doc:`../user_guide/custom_schemes` to create your own
- Check :doc:`../intelligence/accessibility` for colorblind safety



