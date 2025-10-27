Contributing
============

Thank you for considering contributing to Huez!

Ways to Contribute
------------------

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit code changes
- 🎨 Add color schemes
- 🔌 Create adapters for new libraries

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a branch for your changes
4. Make your changes
5. Run tests
6. Submit a pull request

Development Setup
-----------------

.. code-block:: bash

   # Clone your fork
   git clone https://github.com/yourusername/huez.git
   cd huez
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install in development mode
   pip install -e ".[dev]"
   
   # Install all optional dependencies
   pip install -e ".[all]"

Running Tests
-------------

.. code-block:: bash

   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=huez --cov-report=html
   
   # Run specific test file
   pytest tests/unit/test_intelligence.py
   
   # Run specific test
   pytest tests/unit/test_intelligence.py::test_color_expansion

Code Style
----------

We use Ruff for linting:

.. code-block:: bash

   # Run linter
   ruff check huez/
   
   # Auto-fix issues
   ruff check --fix huez/

Follow these guidelines:

- PEP 8 style
- Type hints for function signatures
- Docstrings for public functions
- Maximum line length: 100 characters

Documentation
-------------

Documentation uses Sphinx:

.. code-block:: bash

   cd docs
   make html
   
   # View in browser
   open _build/html/index.html

Adding Color Schemes
--------------------

To add a new color scheme:

1. Create YAML file in ``huez/data/schemes/``
2. Add scheme definition
3. Add tests
4. Update documentation

Example:

.. code-block:: yaml

   # huez/data/schemes/my_scheme.yaml
   schemes:
     my_scheme:
       title: "My Custom Scheme"
       palettes:
         discrete: "#FF0000,#00FF00,#0000FF"
         sequential: "viridis"
         diverging: "coolwarm"

Adding Adapters
---------------

See :doc:`advanced/custom_adapters` for detailed guide.

Pull Request Process
--------------------

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

Code Review
-----------

All submissions require review. We aim to:

- Respond within 48 hours
- Provide constructive feedback
- Merge quickly when ready

Community Guidelines
--------------------

- Be respectful and inclusive
- Help others learn
- Give credit where due
- Focus on constructive feedback

Getting Help
------------

- 💬 GitHub Discussions: Ask questions
- 🐛 GitHub Issues: Report bugs
- 📧 Email: ang@hezhiang.com

License
-------

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank You!
----------

Every contribution, no matter how small, is appreciated! 🎉




