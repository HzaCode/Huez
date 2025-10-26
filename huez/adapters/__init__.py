"""
Library adapters for huez - Support for 5 major mainstream visualization libraries
"""

from .altair import AltairAdapter
from .base import Adapter, apply_scheme_to_adapters, get_available_adapters
from .mpl import MatplotlibAdapter
from .plotly import PlotlyAdapter
from .plotnine import PlotnineAdapter
from .seaborn import SeabornAdapter

# Create adapter registry
matplotlib = MatplotlibAdapter()
seaborn = SeabornAdapter()
plotnine = PlotnineAdapter()
altair = AltairAdapter()
plotly = PlotlyAdapter()

# Define ALL_ADAPTERS here to avoid circular import
# Import from base after all adapters are loaded
from .base import _get_all_adapters_lazy

ALL_ADAPTERS = _get_all_adapters_lazy()

__all__ = [
    "Adapter",
    "get_available_adapters",
    "apply_scheme_to_adapters",
    "ALL_ADAPTERS",
    "MatplotlibAdapter",
    "SeabornAdapter",
    "PlotnineAdapter",
    "AltairAdapter",
    "PlotlyAdapter",
    "matplotlib",
    "seaborn",
    "plotnine",
    "altair",
    "plotly",
]
