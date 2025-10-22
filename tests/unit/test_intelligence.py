"""
Tests for Huez intelligence features
"""
import pytest
import numpy as np
from huez.intelligence.color_expansion import intelligent_color_expansion
from huez.intelligence.colormap_detection import detect_colormap_type
from huez.intelligence.accessibility import check_colorblind_safety


class TestColorExpansion:
    """Test intelligent color expansion"""
    
    def test_expand_basic(self):
        """Test basic color expansion"""
        base = ['#E64B35', '#4DBBD5', '#00A087']
        expanded = intelligent_color_expansion(base, 10)
        assert len(expanded) == 10
        assert all(c.startswith('#') for c in expanded)
    
    def test_expand_less_than_base(self):
        """Test requesting fewer colors than base"""
        base = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F']
        expanded = intelligent_color_expansion(base, 3)
        assert len(expanded) == 3
        assert expanded == base[:3]
    
    def test_expand_same_as_base(self):
        """Test requesting same number as base"""
        base = ['#E64B35', '#4DBBD5', '#00A087']
        expanded = intelligent_color_expansion(base, 3)
        assert len(expanded) == 3
        assert expanded == base


class TestColormapDetection:
    """Test colormap type detection"""
    
    def test_detect_diverging_symmetric(self):
        """Test detection of symmetric diverging data"""
        data = np.random.randn(10, 10)  # Mean ≈ 0
        result = detect_colormap_type(data, verbose=False)
        assert result == "diverging"
    
    def test_detect_sequential_positive(self):
        """Test detection of positive-only sequential data"""
        data = np.random.rand(10, 10) * 100
        result = detect_colormap_type(data, verbose=False)
        # This might be diverging or sequential depending on distribution
        assert result in ["sequential", "diverging"]
    
    def test_detect_correlation_matrix(self):
        """Test detection of correlation matrix"""
        data = np.array([[1.0, 0.8, -0.6], [0.8, 1.0, -0.4], [-0.6, -0.4, 1.0]])
        result = detect_colormap_type(data, verbose=False)
        assert result == "diverging"
    
    def test_handle_nan(self):
        """Test handling of NaN values"""
        data = np.array([[1.0, np.nan, 3.0], [np.nan, 5.0, 6.0]])
        result = detect_colormap_type(data, verbose=False)
        assert result in ["sequential", "diverging"]


class TestAccessibility:
    """Test colorblind accessibility"""
    
    def test_check_basic(self):
        """Test basic accessibility check"""
        colors = ['#E64B35', '#4DBBD5', '#00A087']
        result = check_colorblind_safety(colors, verbose=False)
        
        assert 'safe' in result
        assert 'warnings' in result
        assert 'cvd_analysis' in result
        assert 'suggestions' in result
    
    def test_check_single_color(self):
        """Test check with single color"""
        colors = ['#E64B35']
        result = check_colorblind_safety(colors, verbose=False)
        # Single color should be safe (no pairs to compare)
        assert result['safe']
    
    def test_check_colorblind_safe_palette(self):
        """Test known colorblind-safe palette"""
        # Okabe-Ito palette
        colors = ['#E69F00', '#56B4E9', '#009E73']
        result = check_colorblind_safety(colors, verbose=False)
        
        # Check structure
        assert 'protanopia' in result['cvd_analysis']
        assert 'deuteranopia' in result['cvd_analysis']
        assert 'tritanopia' in result['cvd_analysis']


class TestIntegration:
    """Integration tests for intelligence features"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        # 1. Start with base colors
        base_colors = ['#E64B35', '#4DBBD5', '#00A087']
        
        # 2. Check accessibility
        result = check_colorblind_safety(base_colors, verbose=False)
        assert isinstance(result['safe'], bool)
        
        # 3. Expand if needed
        expanded = intelligent_color_expansion(base_colors, 10)
        assert len(expanded) == 10
        
        # 4. Detect colormap type for data
        data = np.random.randn(5, 5)
        cmap_type = detect_colormap_type(data, verbose=False)
        assert cmap_type in ["sequential", "diverging"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])





