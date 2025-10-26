Installation
============

Huez requires Python 3.7 or higher.

Basic Installation
------------------

Install Huez using pip:

.. code-block:: bash

   pip install huez

This installs the core package with minimal dependencies.

Installation with Specific Libraries
-------------------------------------

If you want to use Huez with specific visualization libraries, you can install them together:

**With Matplotlib:**

.. code-block:: bash

   pip install huez[matplotlib]

**With Seaborn:**

.. code-block:: bash

   pip install huez[seaborn]

**With Plotly:**

.. code-block:: bash

   pip install huez[plotly]

**With Altair:**

.. code-block:: bash

   pip install huez[altair]

**With plotnine:**

.. code-block:: bash

   pip install huez[plotnine]

**With All Libraries:**

.. code-block:: bash

   pip install huez[all]

This installs Huez with support for all 5 visualization libraries.

Development Installation
------------------------

If you want to contribute to Huez, install it in development mode:

.. code-block:: bash

   git clone https://github.com/hzacode/huez.git
   cd huez
   pip install -e ".[dev]"

This installs Huez in editable mode with development dependencies including pytest, coverage, and linting tools.

Verify Installation
-------------------

To verify that Huez is installed correctly:

.. code-block:: python

   import huez as hz
   print(hz.__version__)
   
   # List available schemes
   print(hz.list_schemes())

You should see the version number and a list of available color schemes.

Requirements
------------

**Core Dependencies:**

- PyYAML >= 6.0
- click >= 8.0.0

**Optional Dependencies (for full functionality):**

- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- plotly >= 5.0.0
- altair >= 4.2.0
- plotnine >= 0.8.0

Troubleshooting
---------------

**Import Error:**

If you encounter an import error:

.. code-block:: python

   ModuleNotFoundError: No module named 'huez'

Make sure you have installed Huez in your current Python environment:

.. code-block:: bash

   pip show huez

**Version Conflicts:**

If you have version conflicts with visualization libraries, try creating a new virtual environment:

.. code-block:: bash

   python -m venv huez-env
   source huez-env/bin/activate  # On Windows: huez-env\Scripts\activate
   pip install huez[all]

**Permission Error:**

If you encounter permission errors during installation, use the ``--user`` flag:

.. code-block:: bash

   pip install --user huez

Updating Huez
-------------

To update Huez to the latest version:

.. code-block:: bash

   pip install --upgrade huez

To install a specific version:

.. code-block:: bash

   pip install huez==0.0.5

Next Steps
----------

Now that you have Huez installed, check out the :doc:`quickstart` guide to learn how to use it!


