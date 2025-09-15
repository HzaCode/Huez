"""
Built-in default configurations for huez.
"""

from ..config import Config, Scheme, FontConfig, PalettesConfig, FigureConfig, StyleConfig


def get_default_config() -> Config:
    """Get the built-in default configuration."""
    config = Config()

    # Scheme 1: Nature Journal (NPG) Style
    scheme1 = Scheme(
        title="Nature Journal Style",
        fonts=FontConfig(family="DejaVu Sans", size=9),
        palettes=PalettesConfig(
            discrete="npg",
            sequential="viridis",
            diverging="vik",
            cyclic="twilight"
        ),
        figure=FigureConfig(size=[3.5, 2.5], dpi=300),  # Single column width
        style=StyleConfig(grid="y", legend_loc="best", spine_top_right_off=True)
    )

    # Scheme 2: Science Journal (AAAS) Style
    scheme2 = Scheme(
        title="Science Journal Style",
        fonts=FontConfig(family="DejaVu Sans", size=9),
        palettes=PalettesConfig(
            discrete="aaas",
            sequential="plasma",
            diverging="coolwarm",
            cyclic="twilight"
        ),
        figure=FigureConfig(size=[3.5, 2.5], dpi=300),
        style=StyleConfig(grid="both", legend_loc="upper right", spine_top_right_off=True)
    )

    # Scheme 3: NEJM Style
    scheme3 = Scheme(
        title="NEJM Style",
        fonts=FontConfig(family="DejaVu Sans", size=9),
        palettes=PalettesConfig(
            discrete="nejm",
            sequential="cividis",
            diverging="RdBu",
            cyclic="twilight"
        ),
        figure=FigureConfig(size=[3.5, 2.5], dpi=300),
        style=StyleConfig(grid="y", legend_loc="best", spine_top_right_off=False)
    )

    # Scheme 4: Lancet Style
    lancet = Scheme(
        title="Lancet Style",
        fonts=FontConfig(family="DejaVu Sans", size=10),
        palettes=PalettesConfig(
            discrete="lancet",
            sequential="viridis",
            diverging="coolwarm",
            cyclic="twilight"
        ),
        figure=FigureConfig(size=[4.0, 3.0], dpi=150),
        style=StyleConfig(grid="y", legend_loc="best", spine_top_right_off=True)
    )

    # Scheme 5: JAMA Style
    scheme5 = Scheme(
        title="JAMA Style",
        fonts=FontConfig(family="DejaVu Sans", size=9),
        palettes=PalettesConfig(
            discrete="jama",
            sequential="plasma",
            diverging="Spectral",
            cyclic="twilight"
        ),
        figure=FigureConfig(size=[3.5, 2.5], dpi=300),
        style=StyleConfig(grid="y", legend_loc="best", spine_top_right_off=True)
    )

    config.schemes = {
        "scheme-1": scheme1,
        "scheme-2": scheme2,
        "scheme-3": scheme3,
        "lancet": lancet,
        "scheme-5": scheme5
    }

    return config
