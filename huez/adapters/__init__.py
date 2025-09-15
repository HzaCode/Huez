"""
Library adapters for huez - Support for 5 major mainstream visualization libraries
"""

from .base import Adapter, get_available_adapters, apply_scheme_to_adapters
from .mpl import MatplotlibAdapter
from .seaborn import SeabornAdapter
from .plotnine import PlotnineAdapter
from .altair import AltairAdapter
from .plotly import PlotlyAdapter

__all__ = [
    "Adapter",
    "get_available_adapters",
    "apply_scheme_to_adapters",
    "MatplotlibAdapter",
    "SeabornAdapter",
    "PlotnineAdapter",
    "AltairAdapter",
    "PlotlyAdapter",
]
