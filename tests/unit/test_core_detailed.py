"""Detailed tests for huez.core module - focus on high coverage"""

import pytest
import tempfile
import os


class TestLoadConfig:
    """Test load_config function"""

    def test_load_default_config(self):
        """Test loading default config"""
        from huez.core import load_config

        config = load_config()
        assert config is not None
        assert len(config.schemes) > 0
        assert "scheme-1" in config.schemes

    def test_load_config_from_yaml_file(self):
        """Test loading config from YAML file"""
        from huez.core import load_config

        yaml_content = """
version: 1
default_scheme: test-scheme
schemes:
  test-scheme:
    title: Test Scheme
    fonts:
      family: Arial
      size: 10
    palettes:
      discrete: npg
      sequential: viridis
      diverging: coolwarm
      cyclic: twilight
    figure:
      size: [8.0, 6.0]
      dpi: 150
    style:
      grid: both
      legend_loc: best
      spine_top_right_off: true
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            config = load_config(temp_path)
            assert config.default_scheme == "test-scheme"
            assert "test-scheme" in config.schemes
        finally:
            os.remove(temp_path)


class TestUseFunction:
    """Test use() function with various parameters"""

    def test_use_basic(self):
        """Test basic use"""
        from huez.core import use, current_scheme

        use("scheme-1")
        assert current_scheme() == "scheme-1"

    def test_use_with_auto_expand(self):
        """Test use with auto_expand"""
        from huez.core import use

        use("scheme-1", auto_expand=True)
        use("scheme-1", auto_expand=False)

    def test_use_with_smart_cmap(self):
        """Test use with smart_cmap"""
        from huez.core import use

        use("scheme-1", smart_cmap=True)
        use("scheme-1", smart_cmap=False)

    def test_use_with_screen_mode(self):
        """Test use with screen mode"""
        from huez.core import use

        use("scheme-1", mode="screen")

    def test_use_with_print_mode(self):
        """Test use with print mode"""
        from huez.core import use

        use("scheme-1", mode="print")

    def test_use_with_presentation_mode(self):
        """Test use with presentation mode"""
        from huez.core import use

        use("scheme-1", mode="presentation")

    def test_use_with_custom_config(self):
        """Test use with custom config"""
        from huez.core import use, load_config

        config = load_config()
        use("scheme-1", config=config)

    def test_use_nonexistent_scheme(self):
        """Test using nonexistent scheme raises error"""
        from huez.core import use

        with pytest.raises(ValueError, match="not found"):
            use("nonexistent-scheme-xyz-123")

    def test_use_switches_scheme(self):
        """Test switching between schemes"""
        from huez.core import use, current_scheme

        use("scheme-1")
        assert current_scheme() == "scheme-1"

        use("scheme-2")
        assert current_scheme() == "scheme-2"


class TestCurrentScheme:
    """Test current_scheme() function"""

    def test_current_scheme_returns_active(self):
        """Test current_scheme returns active scheme"""
        from huez.core import use, current_scheme

        use("scheme-1")
        assert current_scheme() == "scheme-1"

    def test_current_scheme_none_initially(self):
        """Test current_scheme can be None"""
        from huez.core import current_scheme

        # May be None or a string
        result = current_scheme()
        assert result is None or isinstance(result, str)


class TestUsingContextManager:
    """Test using() context manager"""

    def test_using_basic(self):
        """Test basic context manager usage"""
        from huez.core import use, using, current_scheme

        use("scheme-1")
        original = current_scheme()

        with using("scheme-2"):
            assert current_scheme() == "scheme-2"

        assert current_scheme() == original

    def test_using_nested(self):
        """Test nested context managers"""
        from huez.core import use, using, current_scheme

        use("scheme-1")

        with using("scheme-2"):
            assert current_scheme() == "scheme-2"

            with using("scheme-3"):
                assert current_scheme() == "scheme-3"

            assert current_scheme() == "scheme-2"

        assert current_scheme() == "scheme-1"

    def test_using_restores_on_exception(self):
        """Test context manager restores on exception"""
        from huez.core import use, using, current_scheme

        use("scheme-1")
        original = current_scheme()

        try:
            with using("scheme-2"):
                assert current_scheme() == "scheme-2"
                raise RuntimeError("Test error")
        except RuntimeError:
            pass

        assert current_scheme() == original


class TestPaletteFunction:
    """Test palette() function"""

    def test_palette_from_current_scheme(self):
        """Test getting palette from current scheme"""
        from huez.core import use, palette

        use("scheme-1")
        colors = palette()
        assert isinstance(colors, list)
        assert len(colors) > 0
        assert all(isinstance(c, str) for c in colors)

    def test_palette_with_scheme_name(self):
        """Test getting palette with scheme name"""
        from huez.core import palette

        colors = palette("npg")
        assert isinstance(colors, list)
        assert len(colors) > 0

    def test_palette_discrete(self):
        """Test getting discrete palette"""
        from huez.core import palette

        colors = palette("npg", kind="discrete")
        assert isinstance(colors, list)

    def test_palette_sequential(self):
        """Test getting sequential palette"""
        from huez.core import palette

        colors = palette("viridis", kind="sequential")
        assert isinstance(colors, list)

    def test_palette_diverging(self):
        """Test getting diverging palette"""
        from huez.core import palette

        colors = palette("coolwarm", kind="diverging")
        assert isinstance(colors, list)

    def test_palette_with_n(self):
        """Test getting n colors"""
        from huez.core import palette

        colors = palette("npg", n=5)
        assert len(colors) == 5

    def test_palette_with_n_larger_than_available(self):
        """Test getting more colors than available"""
        from huez.core import palette

        colors = palette("npg", n=20)
        assert len(colors) == 20


class TestCmapFunction:
    """Test cmap() function"""

    def test_cmap_basic(self):
        """Test getting colormap"""
        from huez.core import cmap

        cm = cmap("viridis")
        assert cm is not None

    def test_cmap_from_current_scheme(self):
        """Test getting colormap from current scheme"""
        from huez.core import use, cmap

        use("scheme-1")
        cm = cmap()
        assert cm is not None

    def test_cmap_sequential(self):
        """Test getting sequential colormap"""
        from huez.core import cmap

        cm = cmap("viridis", kind="sequential")
        assert cm is not None

    def test_cmap_diverging(self):
        """Test getting diverging colormap"""
        from huez.core import cmap

        cm = cmap("coolwarm", kind="diverging")
        assert cm is not None


class TestAutoColors:
    """Test auto_colors() function"""

    def test_auto_colors_basic(self):
        """Test auto colors"""
        from huez.core import auto_colors

        colors = auto_colors(n=5)
        assert isinstance(colors, list)
        assert len(colors) == 5

    def test_auto_colors_matplotlib(self):
        """Test auto colors for matplotlib"""
        from huez.core import auto_colors

        colors = auto_colors(library="matplotlib", n=3)
        assert len(colors) == 3

    def test_auto_colors_auto_detect(self):
        """Test auto colors with auto detection"""
        from huez.core import auto_colors

        colors = auto_colors(library="auto", n=4)
        assert len(colors) == 4


class TestQuickSetup:
    """Test quick_setup() function"""

    def test_quick_setup(self):
        """Test quick setup"""
        from huez.core import quick_setup, current_scheme

        quick_setup("npg")
        assert current_scheme() is not None

    def test_quick_setup_with_scheme(self):
        """Test quick setup with specific scheme"""
        from huez.core import quick_setup, current_scheme

        quick_setup("scheme-1")
        assert current_scheme() == "scheme-1"


class TestColorsFunction:
    """Test colors() function"""

    def test_colors_basic(self):
        """Test getting colors"""
        from huez.core import use, colors

        use("scheme-1")
        cols = colors()
        assert isinstance(cols, list)
        assert len(cols) > 0

    def test_colors_with_n(self):
        """Test getting n colors"""
        from huez.core import use, colors

        use("scheme-1")
        cols = colors(n=5)
        assert len(cols) == 5

    def test_colors_with_library(self):
        """Test getting colors for specific library"""
        from huez.core import use, colors

        use("scheme-1")
        cols = colors(library="matplotlib")
        assert isinstance(cols, list)

    def test_colors_auto_library(self):
        """Test getting colors with auto library detection"""
        from huez.core import use, colors

        use("scheme-1")
        cols = colors(library="auto")
        assert isinstance(cols, list)


class TestApplyToFigure:
    """Test apply_to_figure() function"""

    @pytest.mark.requires_matplotlib
    def test_apply_to_figure_matplotlib(self):
        """Test applying to matplotlib figure"""
        import matplotlib.pyplot as plt
        from huez.core import apply_to_figure

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])

        apply_to_figure(fig, library="matplotlib")

        plt.close(fig)

    @pytest.mark.requires_matplotlib
    def test_apply_to_figure_auto(self):
        """Test applying with auto detection"""
        import matplotlib.pyplot as plt
        from huez.core import apply_to_figure

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])

        apply_to_figure(fig, library="auto")

        plt.close(fig)


class TestStatusFunction:
    """Test status() function"""

    def test_status(self):
        """Test getting status"""
        from huez.core import use, status

        use("scheme-1")
        st = status()

        assert isinstance(st, dict)
        assert "current_scheme" in st

    def test_status_contains_adapters(self):
        """Test status contains adapter info"""
        from huez.core import use, status

        use("scheme-1")
        st = status()

        assert "available_adapters" in st or "adapters" in st


class TestHelpUsage:
    """Test help_usage() function"""

    def test_help_usage(self):
        """Test help usage doesn't raise"""
        from huez.core import help_usage

        # Should not raise
        help_usage()


class TestListSchemes:
    """Test list_schemes() function"""

    def test_list_schemes(self):
        """Test listing schemes"""
        from huez.core import list_schemes

        schemes = list_schemes()

        assert isinstance(schemes, list)
        assert len(schemes) > 0

    def test_list_schemes_contains_defaults(self):
        """Test list contains default schemes"""
        from huez.core import list_schemes

        schemes = list_schemes()

        assert "scheme-1" in schemes


class TestPrivateHelpers:
    """Test private helper functions"""

    def test_enhance_for_presentation(self):
        """Test _enhance_for_presentation"""
        from huez.core import _enhance_for_presentation

        colors = ["#E64B35", "#4DBBD5", "#00A087"]
        enhanced = _enhance_for_presentation(colors)

        assert len(enhanced) == len(colors)
        assert all(c.startswith("#") for c in enhanced)

    def test_apply_display_mode_print(self):
        """Test _apply_display_mode with print"""
        from huez.core import _apply_display_mode, load_config

        config = load_config()
        scheme = config.schemes["scheme-1"]

        modified = _apply_display_mode(scheme, "print")
        assert hasattr(modified, "_display_mode")
        assert modified._display_mode == "print"

    def test_apply_display_mode_presentation(self):
        """Test _apply_display_mode with presentation"""
        from huez.core import _apply_display_mode, load_config

        config = load_config()
        scheme = config.schemes["scheme-1"]

        modified = _apply_display_mode(scheme, "presentation")
        assert hasattr(modified, "_display_mode")

    def test_detect_active_library(self):
        """Test _detect_active_library"""
        from huez.core import _detect_active_library

        lib = _detect_active_library()
        assert isinstance(lib, str)

    def test_get_available_library_names(self):
        """Test _get_available_library_names"""
        from huez.core import _get_available_library_names

        libs = _get_available_library_names()
        assert isinstance(libs, list)


class TestEdgeCases:
    """Test edge cases"""

    def test_use_without_loading_config(self):
        """Test use loads config automatically"""
        from huez.core import use

        # Should auto-load config
        use("scheme-1")

    def test_palette_without_current_scheme(self):
        """Test palette with scheme name when no current scheme"""
        from huez.core import palette

        colors = palette("npg")
        assert isinstance(colors, list)

    def test_colors_with_zero_n(self):
        """Test colors with n=0"""
        from huez.core import use, colors

        use("scheme-1")
        cols = colors(n=0)
        assert isinstance(cols, list)

    def test_multiple_use_calls(self):
        """Test multiple use calls"""
        from huez.core import use, current_scheme

        for scheme in ["scheme-1", "scheme-2", "scheme-3"]:
            use(scheme)
            assert current_scheme() == scheme


class TestAliases:
    """Test function aliases"""

    def test_get_colors_alias(self):
        """Test get_colors is alias for colors"""
        import huez as hz

        hz.use("scheme-1")
        colors1 = hz.colors()
        colors2 = hz.get_colors()

        assert colors1 == colors2

    def test_setup_alias(self):
        """Test setup is alias for quick_setup"""
        import huez as hz

        hz.setup("npg")
        assert hz.current_scheme() is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
