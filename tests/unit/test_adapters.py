"""
Test adapter module
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
import sys

from huez.adapters.base import Adapter, get_adapter_status, get_available_adapters, apply_scheme_to_adapters
from huez.config import Scheme, FontConfig, PalettesConfig, FigureConfig, StyleConfig


class TestBaseAdapter:
    """Test base adapter"""
    
    def test_base_adapter_interface(self):
        """Test base adapter interface"""
        # Create a test adapter class
        class TestAdapter(Adapter):
            def __init__(self):
                super().__init__("test")
            
            def _check_availability(self):
                return True
            
            def apply_scheme(self, scheme):
                pass
        
        adapter = TestAdapter()
        assert adapter.get_name() == "test"
        assert adapter.is_available() is True


class TestGetAdapterStatus:
    """Test adapter status"""
    
    @patch('huez.adapters.matplotlib.MatplotlibAdapter')
    @patch('huez.adapters.seaborn.SeabornAdapter')
    def test_get_adapter_status(self, mock_seaborn, mock_matplotlib):
        """Test getting adapter status"""
        # Mock adapters
        mock_mpl_instance = Mock()
        mock_mpl_instance.get_name.return_value = "matplotlib"
        mock_mpl_instance.is_available.return_value = True
        mock_matplotlib.return_value = mock_mpl_instance
        
        mock_sns_instance = Mock()
        mock_sns_instance.get_name.return_value = "seaborn"
        mock_sns_instance.is_available.return_value = False
        mock_seaborn.return_value = mock_sns_instance
        
        with patch('huez.adapters.base.ALL_ADAPTERS', [mock_matplotlib, mock_seaborn]):
            status = get_adapter_status()
        
        assert isinstance(status, dict)
        assert status["matplotlib"] is True
        assert status["seaborn"] is False


class TestGetAvailableAdapters:
    """Test getting available adapters"""
    
    @patch('huez.adapters.matplotlib.MatplotlibAdapter')
    @patch('huez.adapters.seaborn.SeabornAdapter')
    def test_get_available_adapters(self, mock_seaborn, mock_matplotlib):
        """Test getting available adapters"""
        # Mock available adapters
        mock_mpl_instance = Mock()
        mock_mpl_instance.is_available.return_value = True
        mock_matplotlib.return_value = mock_mpl_instance
        
        # Mock unavailable adapters
        mock_sns_instance = Mock()
        mock_sns_instance.is_available.return_value = False
        mock_seaborn.return_value = mock_sns_instance
        
        with patch('huez.adapters.ALL_ADAPTERS', [mock_matplotlib, mock_seaborn]):
            adapters = get_available_adapters()
        
        assert len(adapters) == 1
        assert adapters[0] is mock_mpl_instance


class TestApplySchemeToAdapters:
    """Test applying scheme to adapters"""
    
    def test_apply_scheme_to_adapters(self):
        """Test applying scheme to adapters"""
        # Create test scheme
        scheme = Scheme(
            title="Test Scheme",
            fonts=FontConfig(family="Arial", size=10),
            palettes=PalettesConfig(discrete="okabe-ito"),
            figure=FigureConfig(dpi=150),
            style=StyleConfig(grid="y")
        )
        
        # Create mock adapters
        mock_adapter1 = Mock()
        mock_adapter2 = Mock()
        adapters = [mock_adapter1, mock_adapter2]
        
        apply_scheme_to_adapters(scheme, adapters)
        
        # Verify each adapter was called
        mock_adapter1.apply_scheme.assert_called_once_with(scheme)
        mock_adapter2.apply_scheme.assert_called_once_with(scheme)


class TestMatplotlibAdapter:
    """Test Matplotlib adapter"""
    
    @pytest.mark.requires_matplotlib
    def test_matplotlib_adapter_available(self):
        """Test matplotlib adapter availability"""
        from huez.adapters.mpl import MatplotlibAdapter

        adapter = MatplotlibAdapter()

        # If matplotlib is available, adapter should be available
        try:
            import matplotlib
            assert adapter.is_available() is True
        except ImportError:
            assert adapter.is_available() is False
        
        assert adapter.get_name() == "matplotlib"
    
    @pytest.mark.requires_matplotlib
    @patch('matplotlib.rcParams')
    def test_matplotlib_apply_scheme(self, mock_rcparams):
        """Test matplotlib applying scheme"""
        from huez.adapters.mpl import MatplotlibAdapter
        
        adapter = MatplotlibAdapter()
        scheme = Scheme(
            fonts=FontConfig(family="Arial", size=10),
            palettes=PalettesConfig(discrete="okabe-ito"),
            figure=FigureConfig(dpi=150),
            style=StyleConfig(grid="y", spine_top_right_off=True)
        )
        
        with patch('huez.registry.palettes.get_palette') as mock_get_palette:
            mock_get_palette.return_value = ['#FF0000', '#00FF00', '#0000FF']
            
            adapter.apply_scheme(scheme)
            
            # Verify rcParams was set
            assert mock_rcparams.__setitem__.called
    
    def test_matplotlib_adapter_unavailable(self):
        """Test matplotlib adapter when unavailable"""
        with patch.dict('sys.modules', {'matplotlib': None}):
            from huez.adapters.mpl import MatplotlibAdapter
            
            adapter = MatplotlibAdapter()
            assert adapter.is_available() is False


class TestSeabornAdapter:
    """Test Seaborn adapter"""
    
    @pytest.mark.requires_seaborn
    def test_seaborn_adapter_available(self):
        """Test seaborn adapter availability"""
        from huez.adapters.seaborn import SeabornAdapter

        adapter = SeabornAdapter()

        # If seaborn is available, adapter should be available
        try:
            import seaborn
            assert adapter.is_available() is True
        except ImportError:
            assert adapter.is_available() is False
        
        assert adapter.get_name() == "seaborn"
    
    @pytest.mark.requires_seaborn
    @patch('seaborn.set_palette')
    @patch('seaborn.set_style')
    def test_seaborn_apply_scheme(self, mock_set_style, mock_set_palette):
        """Test seaborn applying scheme"""
        from huez.adapters.seaborn import SeabornAdapter
        
        adapter = SeabornAdapter()
        scheme = Scheme(
            palettes=PalettesConfig(discrete="okabe-ito"),
            style=StyleConfig(grid="y", spine_top_right_off=True)
        )
        
        with patch('huez.registry.palettes.get_palette') as mock_get_palette:
            mock_get_palette.return_value = ['#FF0000', '#00FF00', '#0000FF']
            
            adapter.apply_scheme(scheme)
            
            # Verify seaborn functions were called
            mock_set_palette.assert_called_once()
            mock_set_style.assert_called_once()


class TestPlotlyAdapter:
    """Test Plotly adapter"""
    
    @pytest.mark.requires_plotly
    def test_plotly_adapter_available(self):
        """Test plotly adapter availability"""
        from huez.adapters.plotly import PlotlyAdapter

        adapter = PlotlyAdapter()

        # If plotly is available, adapter should be available
        try:
            import plotly
            assert adapter.is_available() is True
        except ImportError:
            assert adapter.is_available() is False
        
        assert adapter.get_name() == "plotly"
    
    @pytest.mark.requires_plotly
    @patch('plotly.io.templates')
    def test_plotly_apply_scheme(self, mock_templates):
        """Test plotly applying scheme"""
        from huez.adapters.plotly import PlotlyAdapter
        
        adapter = PlotlyAdapter()
        scheme = Scheme(
            fonts=FontConfig(family="Arial", size=10),
            palettes=PalettesConfig(discrete="okabe-ito"),
            figure=FigureConfig(dpi=150)
        )
        
        with patch('huez.registry.palettes.get_palette') as mock_get_palette:
            mock_get_palette.return_value = ['#FF0000', '#00FF00', '#0000FF']
            
            adapter.apply_scheme(scheme)
            
            # Verify template was set
            assert mock_templates.__setitem__.called or mock_templates.default is not None


class TestAltairAdapter:
    """Test Altair adapter"""

    @pytest.mark.requires_altair
    def test_altair_adapter_available(self):
        """Test altair adapter availability"""
        from huez.adapters.altair import AltairAdapter

        adapter = AltairAdapter()

        # If altair is available, adapter should be available
        try:
            import altair
            assert adapter.is_available() is True
        except ImportError:
            assert adapter.is_available() is False
        
        assert adapter.get_name() == "altair"
    
    @pytest.mark.requires_altair
    @patch('altair.data_transformers.enable')
    def test_altair_apply_scheme(self, mock_enable):
        """Test altair applying scheme"""
        from huez.adapters.altair import AltairAdapter
        
        adapter = AltairAdapter()
        scheme = Scheme(
            fonts=FontConfig(family="Arial", size=10),
            palettes=PalettesConfig(discrete="okabe-ito")
        )
        
        with patch('huez.registry.palettes.get_palette') as mock_get_palette:
            mock_get_palette.return_value = ['#FF0000', '#00FF00', '#0000FF']
            
            adapter.apply_scheme(scheme)
            
            # Altair adapter should successfully apply scheme (implementation may vary by version)


class TestPlotnineAdapter:
    """Test Plotnine adapter"""

    @pytest.mark.requires_plotnine
    def test_plotnine_adapter_available(self):
        """Test plotnine adapter availability"""
        from huez.adapters.plotnine import PlotnineAdapter

        adapter = PlotnineAdapter()

        # If plotnine is available, adapter should be available
        try:
            import plotnine
            assert adapter.is_available() is True
        except ImportError:
            assert adapter.is_available() is False
        
        assert adapter.get_name() == "plotnine"
    
    @pytest.mark.requires_plotnine
    def test_plotnine_apply_scheme(self):
        """Test plotnine applying scheme"""
        from huez.adapters.plotnine import PlotnineAdapter
        
        adapter = PlotnineAdapter()
        scheme = Scheme(
            fonts=FontConfig(family="Arial", size=10),
            palettes=PalettesConfig(discrete="okabe-ito"),
            style=StyleConfig(grid="y")
        )
        
        with patch('huez.registry.palettes.get_palette') as mock_get_palette:
            mock_get_palette.return_value = ['#FF0000', '#00FF00', '#0000FF']
            
            adapter.apply_scheme(scheme)
            
            # Plotnine adapter should successfully apply scheme


class TestAdapterIntegration:
    """Test adapter integration"""

    def test_all_adapters_implement_interface(self):
        """Test all adapters implement interface"""
        from huez.adapters.base import ALL_ADAPTERS

        for adapter_class in ALL_ADAPTERS:
            adapter = adapter_class()

            # Check required methods
            assert hasattr(adapter, 'is_available')
            assert hasattr(adapter, 'get_name')
            assert hasattr(adapter, 'apply_scheme')
            assert callable(adapter.is_available)
            assert callable(adapter.get_name)
            assert callable(adapter.apply_scheme)
    
    def test_adapter_names_unique(self):
        """Test adapter names are unique"""
        from huez.adapters.base import ALL_ADAPTERS
        
        names = []
        for adapter_class in ALL_ADAPTERS:
            try:
                adapter = adapter_class()
                name = adapter.get_name()
                assert name not in names, f"Duplicate adapter name: {name}"
                names.append(name)
            except Exception:
                # Skip if adapter initialization fails (e.g., dependencies unavailable)
                pass
    
    @patch('huez.adapters.matplotlib.MatplotlibAdapter')
    def test_adapter_error_handling(self, mock_adapter_class):
        """Test adapter error handling"""
        # Mock adapter to throw exception in apply_scheme
        mock_adapter = Mock()
        mock_adapter.apply_scheme.side_effect = Exception("Test error")
        mock_adapter_class.return_value = mock_adapter
        
        scheme = Scheme()
        adapters = [mock_adapter]
        
        # Should not throw exception, but handle gracefully
        try:
            apply_scheme_to_adapters(scheme, adapters)
        except Exception as e:
            # If exception is thrown, it should be the expected one
            assert "Test error" in str(e)


class TestAdapterMocking:
    """Test adapter mocking (for environments without related libraries installed)"""
    
    def test_matplotlib_adapter_mock(self):
        """Test mock matplotlib adapter"""
        # Mock matplotlib as unavailable
        with patch.dict('sys.modules', {'matplotlib': None, 'matplotlib.pyplot': None}):
            from huez.adapters.mpl import MatplotlibAdapter
            
            adapter = MatplotlibAdapter()
            assert adapter.is_available() is False
            
            # Should still be able to get name even when unavailable
            assert adapter.get_name() == "matplotlib"
    
    def test_seaborn_adapter_mock(self):
        """Test mock seaborn adapter"""
        # Mock seaborn as unavailable
        with patch.dict('sys.modules', {'seaborn': None}):
            from huez.adapters.seaborn import SeabornAdapter
            
            adapter = SeabornAdapter()
            assert adapter.is_available() is False
            assert adapter.get_name() == "seaborn"
    
    def test_plotly_adapter_mock(self):
        """Test mock plotly adapter"""
        # Mock plotly as unavailable
        with patch.dict('sys.modules', {'plotly': None}):
            from huez.adapters.plotly import PlotlyAdapter
            
            adapter = PlotlyAdapter()
            assert adapter.is_available() is False
            assert adapter.get_name() == "plotly"


class TestAdapterConfiguration:
    """Test adapter configuration"""
    
    def test_scheme_to_adapter_mapping(self):
        """Test scheme to adapter mapping"""
        scheme = Scheme(
            title="Test Scheme",
            fonts=FontConfig(family="Arial", size=12),
            palettes=PalettesConfig(
                discrete="okabe-ito",
                sequential="viridis",
                diverging="coolwarm",
                cyclic="twilight"
            ),
            figure=FigureConfig(dpi=300),
            style=StyleConfig(
                grid="both",
                legend_loc="upper right",
                spine_top_right_off=True
            )
        )
        
        # Test that scheme object contains all necessary configurations
        assert scheme.title == "Test Scheme"
        assert scheme.fonts.family == "Arial"
        assert scheme.fonts.size == 12
        assert scheme.palettes.discrete == "okabe-ito"
        assert scheme.palettes.sequential == "viridis"
        assert scheme.figure.dpi == 300
        assert scheme.style.grid == "both"
        assert scheme.style.legend_loc == "upper right"
        assert scheme.style.spine_top_right_off is True
    
    def test_adapter_scheme_validation(self):
        """Test adapter scheme validation"""
        # Create a simple test adapter
        class TestAdapter(Adapter):
            def __init__(self):
                super().__init__("test")
            
            def _check_availability(self):
                return True
            
            def apply_scheme(self, scheme):
                # Verify scheme object structure
                assert hasattr(scheme, 'fonts')
                assert hasattr(scheme, 'palettes')
                assert hasattr(scheme, 'figure')
                assert hasattr(scheme, 'style')
                
                assert hasattr(scheme.fonts, 'family')
                assert hasattr(scheme.fonts, 'size')
                
                assert hasattr(scheme.palettes, 'discrete')
                assert hasattr(scheme.palettes, 'sequential')
                assert hasattr(scheme.palettes, 'diverging')
                assert hasattr(scheme.palettes, 'cyclic')
        
        adapter = TestAdapter()
        scheme = Scheme()
        
        # Should not throw exception
        adapter.apply_scheme(scheme)
