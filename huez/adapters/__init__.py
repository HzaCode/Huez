"""
Library adapters for huez - Support for 5 major mainstream visualization libraries
"""

from .base import Adapter, get_available_adapters, apply_scheme_to_adapters, ALL_ADAPTERS
from .mpl import MatplotlibAdapter
from .seaborn import SeabornAdapter
from .plotnine import PlotnineAdapter
from .altair import AltairAdapter
from .plotly import PlotlyAdapter

# Create adapter registry
matplotlib = MatplotlibAdapter()
seaborn = SeabornAdapter()
plotnine = PlotnineAdapter()
altair = AltairAdapter()
plotly = PlotlyAdapter()

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
