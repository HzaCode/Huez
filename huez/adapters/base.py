"""
Base adapter classes for huez.
"""

import warnings
from abc import ABC, abstractmethod
from typing import List, Any, Dict
from ..config import Scheme


class Adapter(ABC):
    """Base class for library adapters."""

    def __init__(self, name: str):
        self.name = name
        self.available = self._check_availability()

    @abstractmethod
    def _check_availability(self) -> bool:
        """Check if the target library is available."""
        pass

    @abstractmethod
    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply a color scheme to the target library."""
        pass

    def is_available(self) -> bool:
        """Return True if the adapter can be used."""
        return self.available

    def get_name(self) -> str:
        """Get the adapter name."""
        return self.name


def get_available_adapters() -> List[Adapter]:
    """
    Get all available adapters by scanning installed libraries.

    Returns:
        List of available adapter instances
    """
    from .mpl import MatplotlibAdapter
    from .seaborn import SeabornAdapter
    from .plotnine import PlotnineAdapter
    from .altair import AltairAdapter
    from .plotly import PlotlyAdapter

    # Only support 5 major mainstream libraries
    adapter_classes = [
        MatplotlibAdapter,
        SeabornAdapter,
        PlotnineAdapter,
        AltairAdapter,
        PlotlyAdapter,
    ]

    available_adapters = []
    for adapter_class in adapter_classes:
        try:
            adapter = adapter_class()
            if adapter.is_available():
                available_adapters.append(adapter)
        except Exception as e:
            warnings.warn(f"Failed to initialize {adapter_class.__name__}: {e}")

    if not available_adapters:
        warnings.warn("No visualization libraries found. Install matplotlib, seaborn, plotnine, altair, or plotly.")

    return available_adapters


def apply_scheme_to_adapters(scheme: Scheme, adapters: List[Adapter]) -> None:
    """
    Apply a scheme to multiple adapters.

    Args:
        scheme: Color scheme to apply
        adapters: List of adapters to apply to
    """
    for adapter in adapters:
        try:
            adapter.apply_scheme(scheme)
        except Exception as e:
            warnings.warn(f"Failed to apply scheme to {adapter.get_name()}: {e}")


def get_adapter_status() -> Dict[str, bool]:
    """
    Get the availability status of all adapters.

    Returns:
        Dictionary mapping adapter names to availability status
    """
    adapters = get_available_adapters()
    # Only focus on 5 major mainstream libraries
    all_adapter_names = [
        "matplotlib", "seaborn", "plotnine", "altair", "plotly"
    ]

    status = {}
    available_names = [adapter.get_name() for adapter in adapters]

    for name in all_adapter_names:
        status[name] = name in available_names

    return status
