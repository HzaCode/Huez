"""
Configuration management for huez.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path


@dataclass
class FontConfig:
    """Font configuration."""
    family: str = "DejaVu Sans"
    size: int = 11


@dataclass
class PalettesConfig:
    """Palette configuration."""
    discrete: str = "okabe-ito"
    sequential: str = "viridis"
    diverging: str = "vik"
    cyclic: str = "twilight"


@dataclass
class FigureConfig:
    """Figure configuration."""
    size: List[float] = field(default_factory=lambda: [6.0, 4.0])
    dpi: int = 300


@dataclass
class StyleConfig:
    """Style configuration."""
    grid: str = "y"  # "x", "y", "both", "none"
    legend_loc: str = "best"
    spine_top_right_off: bool = True


@dataclass
class Scheme:
    """Color scheme configuration."""
    title: str = ""
    fonts: FontConfig = field(default_factory=FontConfig)
    palettes: PalettesConfig = field(default_factory=PalettesConfig)
    figure: FigureConfig = field(default_factory=FigureConfig)
    style: StyleConfig = field(default_factory=StyleConfig)


@dataclass
class Config:
    """Main configuration."""
    version: int = 1
    default_scheme: str = "scheme-1"
    schemes: Dict[str, Scheme] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create Config from dictionary."""
        config = cls()

        if "version" in data:
            config.version = data["version"]
        if "default_scheme" in data:
            config.default_scheme = data["default_scheme"]

        if "schemes" in data:
            for scheme_name, scheme_data in data["schemes"].items():
                scheme = Scheme()

                if "title" in scheme_data:
                    scheme.title = scheme_data["title"]

                # Parse fonts
                if "fonts" in scheme_data:
                    fonts_data = scheme_data["fonts"]
                    scheme.fonts = FontConfig(
                        family=fonts_data.get("family", "DejaVu Sans"),
                        size=fonts_data.get("size", 11)
                    )

                # Parse palettes
                if "palettes" in scheme_data:
                    palettes_data = scheme_data["palettes"]
                    scheme.palettes = PalettesConfig(
                        discrete=palettes_data.get("discrete", "okabe-ito"),
                        sequential=palettes_data.get("sequential", "viridis"),
                        diverging=palettes_data.get("diverging", "vik"),
                        cyclic=palettes_data.get("cyclic", "twilight")
                    )

                # Parse figure
                if "figure" in scheme_data:
                    figure_data = scheme_data["figure"]
                    scheme.figure = FigureConfig(
                        size=figure_data.get("size", [6.0, 4.0]),
                        dpi=figure_data.get("dpi", 300)
                    )

                # Parse style
                if "style" in scheme_data:
                    style_data = scheme_data["style"]
                    scheme.style = StyleConfig(
                        grid=style_data.get("grid", "y"),
                        legend_loc=style_data.get("legend_loc", "best"),
                        spine_top_right_off=style_data.get("spine_top_right_off", True)
                    )

                config.schemes[scheme_name] = scheme

        return config

    def to_dict(self) -> Dict[str, Any]:
        """Convert Config to dictionary."""
        schemes_dict = {}
        for name, scheme in self.schemes.items():
            schemes_dict[name] = {
                "title": scheme.title,
                "fonts": {
                    "family": scheme.fonts.family,
                    "size": scheme.fonts.size
                },
                "palettes": {
                    "discrete": scheme.palettes.discrete,
                    "sequential": scheme.palettes.sequential,
                    "diverging": scheme.palettes.diverging,
                    "cyclic": scheme.palettes.cyclic
                },
                "figure": {
                    "size": scheme.figure.size,
                    "dpi": scheme.figure.dpi
                },
                "style": {
                    "grid": scheme.style.grid,
                    "legend_loc": scheme.style.legend_loc,
                    "spine_top_right_off": scheme.style.spine_top_right_off
                }
            }

        return {
            "version": self.version,
            "default_scheme": self.default_scheme,
            "schemes": schemes_dict
        }


def validate_config(config: Config) -> None:
    """
    Validate configuration object.

    Args:
        config: Config object to validate

    Raises:
        ValueError: If configuration is invalid
    """
    if not config.schemes:
        raise ValueError("Configuration must contain at least one scheme")

    if config.default_scheme not in config.schemes:
        raise ValueError(f"Default scheme '{config.default_scheme}' not found in schemes")

    # Validate each scheme
    for scheme_name, scheme in config.schemes.items():
        # Validate palette names exist in registry
        from .registry.palettes import validate_palette_name

        for palette_type in ["discrete", "sequential", "diverging", "cyclic"]:
            palette_name = getattr(scheme.palettes, palette_type)
            if not validate_palette_name(palette_name, palette_type):
                print(f"Warning: Palette '{palette_name}' ({palette_type}) not found in registry. Will use fallback.")

        # Validate figure size
        if len(scheme.figure.size) != 2:
            raise ValueError(f"Scheme '{scheme_name}': figure.size must be [width, height]")

        # Validate grid option
        if scheme.style.grid not in ["x", "y", "both", "none"]:
            raise ValueError(f"Scheme '{scheme_name}': style.grid must be one of: x, y, both, none")

        # Validate legend location
        valid_legend_locs = ["best", "upper right", "upper left", "lower left", "lower right",
                           "right", "center left", "center right", "lower center", "upper center", "center"]
        if scheme.style.legend_loc not in valid_legend_locs:
            raise ValueError(f"Scheme '{scheme_name}': style.legend_loc must be one of: {valid_legend_locs}")


def load_config_from_file(path: str) -> Config:
    """
    Load configuration from YAML file.

    Args:
        path: Path to YAML file

    Returns:
        Config object
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"Failed to parse YAML file: {path}")

    return Config.from_dict(data)


def save_config_to_file(config: Config, path: str) -> None:
    """
    Save configuration to YAML file.

    Args:
        config: Config object
        path: Path to save file
    """
    data = config.to_dict()

    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


