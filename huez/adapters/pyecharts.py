"""
PyECharts adapter for huez.
"""

import warnings
import json
from typing import Dict, Any
from .base import Adapter
from ..config import Scheme
from ..registry.palettes import get_palette


class PyEChartsAdapter(Adapter):
    """Adapter for PyECharts."""

    def __init__(self):
        super().__init__("pyecharts")

    def _check_availability(self) -> bool:
        """Check if pyecharts is available."""
        try:
            import pyecharts.options as opts
            from pyecharts.globals import ThemeType
            return True
        except ImportError:
            return False

    def apply_scheme(self, scheme: Scheme) -> None:
        """Apply scheme to PyECharts."""
        # PyECharts uses theme files, so we create a theme and register it
        try:
            theme_config = self._create_echarts_theme(scheme)

            # Save theme to a temporary file and register it
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(theme_config, f)
                theme_file = f.name

            # Register the theme
            self._register_theme(theme_config, "huez_theme")

        except Exception as e:
            warnings.warn(f"Failed to apply PyECharts theme: {e}")

    def _create_echarts_theme(self, scheme: Scheme) -> Dict[str, Any]:
        """Create ECharts theme configuration."""
        try:
            discrete_colors = get_palette(scheme.palettes.discrete, "discrete")
            sequential_cmap = get_palette(scheme.palettes.sequential, "sequential")
            diverging_cmap = get_palette(scheme.palettes.diverging, "diverging")
        except Exception as e:
            warnings.warn(f"Failed to get palettes for ECharts theme: {e}")
            discrete_colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de']
            sequential_cmap = 'viridis'
            diverging_cmap = 'RdYlBu'

        theme_config = {
            "color": discrete_colors,
            "backgroundColor": "#ffffff",
            "textStyle": {
                "fontFamily": scheme.fonts.family,
                "fontSize": scheme.fonts.size
            },
            "title": {
                "textStyle": {
                    "fontFamily": scheme.fonts.family,
                    "fontSize": scheme.fonts.size + 4,
                    "color": "#333333"
                }
            },
            "legend": {
                "textStyle": {
                    "fontFamily": scheme.fonts.family,
                    "fontSize": scheme.fonts.size - 1,
                    "color": "#666666"
                }
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": True
            },
            "categoryAxis": {
                "axisLine": {
                    "lineStyle": {
                        "color": "#cccccc"
                    }
                },
                "axisTick": {
                    "lineStyle": {
                        "color": "#cccccc"
                    }
                },
                "axisLabel": {
                    "textStyle": {
                        "color": "#666666",
                        "fontFamily": scheme.fonts.family,
                        "fontSize": scheme.fonts.size - 2
                    }
                }
            },
            "valueAxis": {
                "axisLine": {
                    "lineStyle": {
                        "color": "#cccccc"
                    }
                },
                "axisTick": {
                    "lineStyle": {
                        "color": "#cccccc"
                    }
                },
                "axisLabel": {
                    "textStyle": {
                        "color": "#666666",
                        "fontFamily": scheme.fonts.family,
                        "fontSize": scheme.fonts.size - 2
                    }
                },
                "splitLine": {
                    "lineStyle": {
                        "color": "#eeeeee",
                        "type": "dashed"
                    }
                }
            },
            "toolbox": {
                "iconStyle": {
                    "normal": {
                        "borderColor": "#666666"
                    }
                }
            }
        }

        return theme_config

    def _register_theme(self, theme_config: Dict[str, Any], theme_name: str) -> None:
        """Register theme with PyECharts."""
        try:
            from pyecharts.globals import ThemeType

            # Create a custom theme class
            class HueTheme:
                def __init__(self, config):
                    self.config = config

                def get_theme(self):
                    return self.config

            # Register theme
            theme_instance = HueTheme(theme_config)
            setattr(ThemeType, theme_name.upper(), theme_name)

        except Exception as e:
            warnings.warn(f"Failed to register PyECharts theme: {e}")


def export_echarts_theme(scheme: Scheme, output_path: str) -> None:
    """
    Export ECharts theme file.

    Args:
        scheme: Color scheme
        output_path: Path to save theme file
    """
    adapter = PyEChartsAdapter()
    theme_config = adapter._create_echarts_theme(scheme)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(theme_config, f, indent=2, ensure_ascii=False)
