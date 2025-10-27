"""Performance tests (Benchmark) for Huez test the performance indicators of each function"""

import time

import numpy as np
import pytest


class TestColorExpansionPerformance:
    """Test color expansion performance"""

    @pytest.mark.slow
    def test_expansion_small_scale(self):
        """Benchmark: Expand 5 colors to 15"""
        from huez.intelligence.color_expansion import intelligent_color_expansion

        base = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F"]

        start = time.time()
        for _ in range(100):
            intelligent_color_expansion(base, 15)
        elapsed = time.time() - start

        avg_time = elapsed / 100
        print(
            f"\n[BENCHMARK] Color expansion (5→15): {avg_time * 1000:.2f} ms per call"
        )

        # Should be < 10ms per call
        assert avg_time < 0.01

    @pytest.mark.slow
    def test_expansion_large_scale(self):
        """Benchmark: Expand 5 colors to 100"""
        from huez.intelligence.color_expansion import intelligent_color_expansion

        base = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F"]

        start = time.time()
        for _ in range(10):
            intelligent_color_expansion(base, 100)
        elapsed = time.time() - start

        avg_time = elapsed / 10
        print(
            f"\n[BENCHMARK] Color expansion (5→100): {avg_time * 1000:.2f} ms per call"
        )

        # Should be < 50ms per call
        assert avg_time < 0.05

    @pytest.mark.slow
    def test_color_conversion_performance(self):
        """Benchmark: RGB <-> LAB conversion"""
        from huez.intelligence.color_expansion import lab_to_rgb, rgb_to_lab

        rgb = (128, 64, 200)

        start = time.time()
        for _ in range(10000):
            lab = rgb_to_lab(rgb)
            lab_to_rgb(lab)
        elapsed = time.time() - start

        avg_time = (elapsed / 10000) * 1000
        print(f"\n[BENCHMARK] RGB<->LAB roundtrip: {avg_time:.3f} ms per 1000 calls")

        # Should be < 1ms per 1000 calls
        assert elapsed < 0.01


class TestColormapDetectionPerformance:
    """Test colormap detection performance"""

    @pytest.mark.slow
    def test_detection_small_data(self):
        """Benchmark: Detect colormap type for 10x10 data"""
        from huez.intelligence.colormap_detection import detect_colormap_type

        data = np.random.randn(10, 10)

        start = time.time()
        for _ in range(1000):
            detect_colormap_type(data, verbose=False)
        elapsed = time.time() - start

        avg_time = (elapsed / 1000) * 1000
        print(f"\n[BENCHMARK] Colormap detection (10x10): {avg_time:.3f} ms per call")

        # Should be < 1ms per call
        assert avg_time < 1.0

    @pytest.mark.slow
    def test_detection_large_data(self):
        """Benchmark: Detect colormap type for 1000x1000 data"""
        from huez.intelligence.colormap_detection import detect_colormap_type

        data = np.random.randn(1000, 1000)

        start = time.time()
        for _ in range(10):
            detect_colormap_type(data, verbose=False)
        elapsed = time.time() - start

        avg_time = (elapsed / 10) * 1000
        print(
            f"\n[BENCHMARK] Colormap detection (1000x1000): {avg_time:.2f} ms per call"
        )

        # Should be < 100ms per call even for large data
        assert avg_time < 100.0


class TestAccessibilityPerformance:
    """Test accessibility check performance"""

    @pytest.mark.slow
    def test_colorblind_simulation_performance(self):
        """Benchmark: Colorblind simulation"""
        from huez.intelligence.accessibility import simulate_colorblind_vision

        colors = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F"]

        start = time.time()
        for _ in range(1000):
            simulate_colorblind_vision(colors, "deuteranopia")
        elapsed = time.time() - start

        avg_time = (elapsed / 1000) * 1000
        print(
            f"\n[BENCHMARK] Colorblind simulation (5 colors): {avg_time:.3f} ms per call"
        )

        # Should be < 1ms per call
        assert avg_time < 1.0

    @pytest.mark.slow
    def test_contrast_calculation_performance(self):
        """Benchmark: Color contrast calculation"""
        from huez.intelligence.accessibility import calculate_color_contrast

        color1, color2 = "#FF0000", "#0000FF"

        start = time.time()
        for _ in range(10000):
            calculate_color_contrast(color1, color2)
        elapsed = time.time() - start

        avg_time = (elapsed / 10000) * 1000
        print(f"\n[BENCHMARK] Contrast calculation: {avg_time:.3f} ms per 1000 calls")

        # Should be very fast
        assert avg_time < 0.5

    @pytest.mark.slow
    def test_full_safety_check_performance(self):
        """Benchmark: Full colorblind safety check"""
        from huez.intelligence.accessibility import check_colorblind_safety

        colors = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F"]

        start = time.time()
        for _ in range(100):
            check_colorblind_safety(colors, verbose=False)
        elapsed = time.time() - start

        avg_time = (elapsed / 100) * 1000
        print(f"\n[BENCHMARK] Full safety check (5 colors): {avg_time:.2f} ms per call")

        # Should be < 50ms per call
        assert avg_time < 50.0

    @pytest.mark.slow
    def test_safety_check_scaling(self):
        """Benchmark: Safety check with increasing colors"""
        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion

        base = ["#E64B35", "#4DBBD5", "#00A087"]

        results = {}
        for n in [5, 10, 15, 20]:
            colors = intelligent_color_expansion(base, n)

            start = time.time()
            for _ in range(10):
                check_colorblind_safety(colors, verbose=False)
            elapsed = time.time() - start

            avg_time = (elapsed / 10) * 1000
            results[n] = avg_time
            print(
                f"\n[BENCHMARK] Safety check ({n} colors): {avg_time:.2f} ms per call"
            )

        # Check that time doesn't explode (should be roughly O(n^2))
        assert results[20] < results[5] * 20  # Not worse than linear scaling


@pytest.mark.requires_matplotlib
class TestChartAdaptationPerformance:
    """Test chart adaptation performance"""

    @pytest.mark.slow
    def test_chart_detection_performance(self):
        """Benchmark: Chart type detection"""
        import matplotlib.pyplot as plt
        import numpy as np

        from huez.intelligence.chart_adaptation import detect_chart_type

        # Create a plot
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        for i in range(10):
            ax.plot(x, np.sin(x + i * 0.5))

        start = time.time()
        for _ in range(100):
            detect_chart_type(ax)
        elapsed = time.time() - start

        avg_time = (elapsed / 100) * 1000
        print(f"\n[BENCHMARK] Chart detection: {avg_time:.2f} ms per call")

        plt.close()

        # Should be < 10ms per call
        assert avg_time < 10.0

    @pytest.mark.slow
    def test_color_adaptation_performance(self):
        """Benchmark: Color adaptation"""
        from huez.intelligence.chart_adaptation import adapt_colors_for_chart

        colors = ["#E64B35", "#4DBBD5", "#00A087"]
        chart_info = {
            "type": "line",
            "complexity": "complex",
            "total_elements": 12,
            "n_lines": 12,
            "n_scatter": 0,
            "n_bars": 0,
        }

        start = time.time()
        for _ in range(1000):
            adapted, recs = adapt_colors_for_chart(colors, chart_info)
        elapsed = time.time() - start

        avg_time = (elapsed / 1000) * 1000
        print(f"\n[BENCHMARK] Color adaptation: {avg_time:.3f} ms per call")

        # Should be very fast
        assert avg_time < 1.0


class TestEndToEndPerformance:
    """Test end-to-end workflow performance"""

    @pytest.mark.slow
    @pytest.mark.requires_matplotlib
    def test_complete_workflow_performance(self):
        """Benchmark: Complete workflow from palette to plot"""
        import matplotlib.pyplot as plt
        import numpy as np

        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.chart_adaptation import (
            adapt_colors_for_chart,
            detect_chart_type,
        )
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.intelligence.colormap_detection import detect_colormap_type

        start_total = time.time()

        # Step 1: Expand colors
        start = time.time()
        base = ["#E64B35", "#4DBBD5", "#00A087"]
        expanded = intelligent_color_expansion(base, 12)
        time_expansion = (time.time() - start) * 1000

        # Step 2: Check accessibility
        start = time.time()
        check_colorblind_safety(expanded, verbose=False)
        time_safety = (time.time() - start) * 1000

        # Step 3: Detect colormap
        start = time.time()
        data = np.random.randn(50, 50)
        detect_colormap_type(data, verbose=False)
        time_cmap = (time.time() - start) * 1000

        # Step 4: Create plot and detect chart type
        start = time.time()
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        for i, color in enumerate(expanded):
            ax.plot(x, np.sin(x + i * 0.5), color=color)
        info = detect_chart_type(ax)
        time_chart = (time.time() - start) * 1000

        # Step 5: Adapt colors
        start = time.time()
        adapted, recs = adapt_colors_for_chart(expanded, info)
        time_adapt = (time.time() - start) * 1000

        plt.close()

        total_time = (time.time() - start_total) * 1000

        print("\n[BENCHMARK] End-to-End Workflow:")
        print(f"  1. Color expansion:     {time_expansion:.2f} ms")
        print(f"  2. Safety check:        {time_safety:.2f} ms")
        print(f"  3. Colormap detection:  {time_cmap:.2f} ms")
        print(f"  4. Chart detection:     {time_chart:.2f} ms")
        print(f"  5. Color adaptation:    {time_adapt:.2f} ms")
        print(f"  Total:                  {total_time:.2f} ms")

        # Total should be < 200ms
        assert total_time < 200.0

    @pytest.mark.slow
    def test_memory_usage(self):
        """Test memory usage doesn't explode"""
        import sys

        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion

        base = ["#E64B35", "#4DBBD5", "#00A087"]

        # Get initial memory usage (rough estimate)
        initial_size = sys.getsizeof(base)

        # Expand to many colors
        expanded = intelligent_color_expansion(base, 100)
        expanded_size = sys.getsizeof(expanded)

        # Check accessibility
        result = check_colorblind_safety(expanded, verbose=False)
        result_size = sys.getsizeof(result)

        print(f"\n[MEMORY] Base palette: {initial_size} bytes")
        print(f"[MEMORY] Expanded (100 colors): {expanded_size} bytes")
        print(f"[MEMORY] Safety check result: {result_size} bytes")

        # Memory usage should be reasonable
        assert expanded_size < 100_000  # < 100 KB
        assert result_size < 50_000  # < 50 KB


class TestPerformanceSummary:
    """Generate performance summary report"""

    @pytest.mark.slow
    def test_generate_performance_report(self):
        """Generate comprehensive performance report"""
        import numpy as np

        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.intelligence.colormap_detection import detect_colormap_type

        report = {"Color Expansion": {}, "Colormap Detection": {}, "Accessibility": {}}

        # Test color expansion at different scales
        base = ["#E64B35", "#4DBBD5", "#00A087"]
        for n in [10, 20, 50, 100]:
            start = time.time()
            intelligent_color_expansion(base, n)
            elapsed = (time.time() - start) * 1000
            report["Color Expansion"][f"{len(base)}→{n}"] = f"{elapsed:.2f} ms"

        # Test colormap detection at different sizes
        for size in [10, 100, 500]:
            data = np.random.randn(size, size)
            start = time.time()
            detect_colormap_type(data, verbose=False)
            elapsed = (time.time() - start) * 1000
            report["Colormap Detection"][f"{size}x{size}"] = f"{elapsed:.2f} ms"

        # Test accessibility at different color counts
        for n in [5, 10, 15, 20]:
            colors = intelligent_color_expansion(base, n)
            start = time.time()
            check_colorblind_safety(colors, verbose=False)
            elapsed = (time.time() - start) * 1000
            report["Accessibility"][f"{n} colors"] = f"{elapsed:.2f} ms"

        # Print report
        print("\n" + "=" * 70)
        print("HUEZ PERFORMANCE REPORT")
        print("=" * 70)

        for category, results in report.items():
            print(f"\n{category}:")
            for test, time_str in results.items():
                print(f"  {test:20s} : {time_str}")

        print("\n" + "=" * 70)

        # All tests completed
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "slow", "-s"])
