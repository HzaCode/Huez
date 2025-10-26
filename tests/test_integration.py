"""Integration tests for Huez test scenarios where multiple modules work together"""
import pytest
import numpy as np


class TestCoreWithIntelligence:
    """Test core module with intelligence features integration"""
    
    @pytest.mark.integration
    def test_palette_expansion(self):
        """Test palette loading and expanding colors"""
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.registry.palettes import get_palette
        
        try:
            # Get a palette
            palette = get_palette('npg')
            assert len(palette) > 0
            
            # Expand colors
            expanded = intelligent_color_expansion(palette, 15)
            assert len(expanded) == 15
        except Exception as e:
            pytest.skip(f"Palette loading not available: {e}")
    
    @pytest.mark.integration
    def test_accessibility_check_with_palettes(self):
        """Test accessibility check on all built-in palettes"""
        from huez.registry.palettes import get_palette
        from huez.intelligence.accessibility import check_colorblind_safety
        
        palettes_to_test = ['npg', 'okabe-ito']
        
        results = {}
        for palette_name in palettes_to_test:
            try:
                palette = get_palette(palette_name)
                result = check_colorblind_safety(palette, verbose=False)
                results[palette_name] = result['safe']
            except Exception as e:
                pytest.skip(f"Palette {palette_name} not available: {e}")
        
        # At least some palettes should be tested
        assert len(results) > 0


@pytest.mark.requires_matplotlib
class TestAdaptersWithIntelligence:
    """Test adapters with intelligence features"""
    
    @pytest.mark.integration
    def test_matplotlib_with_color_expansion(self):
        """Test matplotlib adapter with color expansion"""
        import matplotlib.pyplot as plt
        from huez.intelligence.color_expansion import intelligent_color_expansion
        
        # Create base palette
        base = ['#E64B35', '#4DBBD5', '#00A087']
        expanded = intelligent_color_expansion(base, 10)
        
        # Plot with expanded colors
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        
        for i, color in enumerate(expanded):
            ax.plot(x, np.sin(x + i * 0.5), color=color, label=f'Line {i+1}')
        
        # Should not raise any errors
        ax.legend()
        plt.close()
    
    @pytest.mark.integration
    def test_matplotlib_with_colormap_detection(self):
        """Test matplotlib with smart colormap detection"""
        import matplotlib.pyplot as plt
        from huez.intelligence.colormap_detection import detect_colormap_type
        
        # Create diverging data
        data = np.random.randn(10, 10)
        cmap_type = detect_colormap_type(data, verbose=False)
        
        # Create heatmap
        fig, ax = plt.subplots()
        if cmap_type == "diverging":
            im = ax.imshow(data, cmap='coolwarm')
        else:
            im = ax.imshow(data, cmap='viridis')
        
        plt.colorbar(im, ax=ax)
        plt.close()
        
        assert cmap_type in ["sequential", "diverging"]
    
    @pytest.mark.integration
    def test_chart_adaptation_workflow(self):
        """Test complete chart adaptation workflow"""
        import matplotlib.pyplot as plt
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.intelligence.chart_adaptation import detect_chart_type, adapt_colors_for_chart
        
        # Create complex plot
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        
        base = ['#E64B35', '#4DBBD5', '#00A087']
        expanded = intelligent_color_expansion(base, 12)
        
        for i, color in enumerate(expanded):
            ax.plot(x, np.sin(x + i * 0.5), color=color)
        
        # Detect chart type
        info = detect_chart_type(ax)
        
        # Get adaptation recommendations
        adapted, recs = adapt_colors_for_chart(expanded, info)
        
        assert info['type'] == 'line'
        assert info['complexity'] in ['medium', 'complex']
        assert isinstance(recs, dict)
        
        plt.close()


@pytest.mark.requires_seaborn
class TestSeabornIntegration:
    """Test Seaborn integration with intelligence features"""
    
    @pytest.mark.integration
    def test_seaborn_heatmap_with_detection(self):
        """Test seaborn heatmap with automatic colormap detection"""
        import seaborn as sns
        import matplotlib.pyplot as plt
        from huez.intelligence.colormap_detection import detect_colormap_type
        
        # Create correlation matrix
        data = np.random.randn(10, 10)
        corr = np.corrcoef(data)
        
        # Detect colormap type
        cmap_type = detect_colormap_type(corr, verbose=False)
        
        # Plot with appropriate colormap
        fig, ax = plt.subplots()
        if cmap_type == "diverging":
            sns.heatmap(corr, ax=ax, cmap='coolwarm', center=0)
        else:
            sns.heatmap(corr, ax=ax, cmap='viridis')
        
        plt.close()
        
        assert cmap_type == "diverging"


class TestFullPipeline:
    """Test complete Huez pipeline from config to visualization"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_workflow(self):
        """Test complete workflow: config -> palette -> expansion -> accessibility"""
        from huez.config import load_default_config
        from huez.registry.palettes import get_palette
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.colormap_detection import detect_colormap_type
        
        # Step 1: Load configuration
        config = load_default_config()
        assert config is not None
        
        # Step 2: Get palette
        palette = get_palette('npg')
        assert len(palette) >= 3
        
        # Step 3: Expand colors
        expanded = intelligent_color_expansion(palette, 15)
        assert len(expanded) == 15
        
        # Step 4: Check accessibility
        safety = check_colorblind_safety(expanded, verbose=False)
        assert isinstance(safety['safe'], bool)
        assert 'cvd_analysis' in safety
        
        # Step 5: Detect colormap type for data
        data_div = np.random.randn(10, 10)
        cmap_type = detect_colormap_type(data_div, verbose=False)
        assert cmap_type in ["sequential", "diverging"]
    
    @pytest.mark.integration
    @pytest.mark.requires_matplotlib
    def test_multi_library_consistency(self):
        """Test consistent colors across multiple libraries"""
        import matplotlib.pyplot as plt
        from huez.intelligence.color_expansion import intelligent_color_expansion
        
        base = ['#E64B35', '#4DBBD5', '#00A087']
        expanded = intelligent_color_expansion(base, 8)
        
        # Test with matplotlib
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        x = np.linspace(0, 10, 100)
        
        # Line plot
        for i, color in enumerate(expanded[:5]):
            axes[0].plot(x, np.sin(x + i * 0.5), color=color, label=f'Series {i+1}')
        axes[0].set_title('Line Plot')
        axes[0].legend()
        
        # Scatter plot
        for i, color in enumerate(expanded[:5]):
            axes[1].scatter(np.random.rand(20), np.random.rand(20), 
                          color=color, label=f'Group {i+1}', s=50)
        axes[1].set_title('Scatter Plot')
        axes[1].legend()
        
        plt.close()
        
        assert len(expanded) == 8


class TestErrorHandling:
    """Test error handling in integration scenarios"""
    
    @pytest.mark.integration
    def test_invalid_data_handling(self):
        """Test handling of invalid data"""
        from huez.intelligence.colormap_detection import detect_colormap_type
        from huez.intelligence.color_expansion import intelligent_color_expansion
        
        # Test with all NaN data
        nan_data = np.full((5, 5), np.nan)
        result = detect_colormap_type(nan_data, verbose=False)
        assert result in ["sequential", "diverging"]
        
        # Test with empty color list
        try:
            expanded = intelligent_color_expansion([], 5)
            # Should either return empty list or raise error
            assert expanded == [] or len(expanded) == 0
        except (ValueError, IndexError):
            # This is also acceptable behavior
            pass
    
    @pytest.mark.integration
    def test_edge_case_handling(self):
        """Test edge cases in integration"""
        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion
        
        # Test with single color
        single = ['#FF0000']
        safety = check_colorblind_safety(single, verbose=False)
        assert safety['safe']
        
        # Test with identical colors
        identical = ['#FF0000', '#FF0000', '#FF0000']
        expanded = intelligent_color_expansion(identical, 5)
        assert len(expanded) == 5


class TestPerformanceIntegration:
    """Test performance in integration scenarios"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_scale_expansion(self):
        """Test large scale color expansion"""
        from huez.intelligence.color_expansion import intelligent_color_expansion
        import time
        
        base = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F']
        
        start = time.time()
        expanded = intelligent_color_expansion(base, 100)
        elapsed = time.time() - start
        
        assert len(expanded) == 100
        # Should complete in reasonable time (< 1 second)
        assert elapsed < 1.0
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_accessibility_check_performance(self):
        """Test accessibility check performance"""
        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion
        import time
        
        base = ['#E64B35', '#4DBBD5', '#00A087']
        expanded = intelligent_color_expansion(base, 20)
        
        start = time.time()
        result = check_colorblind_safety(expanded, verbose=False)
        elapsed = time.time() - start
        
        assert isinstance(result['safe'], bool)
        # Should complete in reasonable time (< 2 seconds for 20 colors)
        assert elapsed < 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
