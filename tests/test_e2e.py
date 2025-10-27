"""End-to-End tests for Huez test real usage scenarios"""

import os
import tempfile

import numpy as np
import pytest


@pytest.mark.requires_matplotlib
class TestRealWorldScenarios:
    """Test real-world usage scenarios"""

    def test_genomics_multi_panel_figure(self):
        """Scenario: Multi-panel chart for a bioinformatics paper"""
        import matplotlib.pyplot as plt
        import numpy as np

        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.intelligence.colormap_detection import detect_colormap_type

        # Basic color matching
        base = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488"]

        # Expands to 12 cell types
        cell_colors = intelligent_color_expansion(base, 12)

        # Check color blindness friendliness
        check_colorblind_safety(cell_colors, verbose=False)

        # Create multi-panel charts
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Panel A: Gene expression scatter plot
        for i in range(12):
            x = np.random.randn(50)
            y = np.random.randn(50)
            axes[0, 0].scatter(
                x, y, c=cell_colors[i], label=f"Cell {i+1}", s=30, alpha=0.7
            )
        axes[0, 0].set_title("A. Single-cell UMAP")
        axes[0, 0].set_xlabel("UMAP 1")
        axes[0, 0].set_ylabel("UMAP 2")
        axes[0, 0].legend(bbox_to_anchor=(1.05, 1), fontsize=8)

        # Panel B: Gene expression heat map
        expr_data = np.random.randn(20, 12)  # 20 genes x 12 cell types
        cmap_type = detect_colormap_type(expr_data, verbose=False)
        im = axes[0, 1].imshow(
            expr_data,
            aspect="auto",
            cmap="coolwarm" if cmap_type == "diverging" else "viridis",
        )
        axes[0, 1].set_title("B. Gene Expression Heatmap")
        axes[0, 1].set_xlabel("Cell Types")
        axes[0, 1].set_ylabel("Genes")
        plt.colorbar(im, ax=axes[0, 1])

        # Panel C: Bar chart
        means = np.random.rand(12) * 10
        axes[1, 0].bar(range(12), means, color=cell_colors)
        axes[1, 0].set_title("C. Mean Expression per Cell Type")
        axes[1, 0].set_xlabel("Cell Type")
        axes[1, 0].set_ylabel("Expression Level")

        # Panel D: Line chart (time series)
        time = np.linspace(0, 24, 100)  # 24 hours
        for i in range(8):
            axes[1, 1].plot(
                time,
                np.sin(time / 4 + i * 0.5) + i * 0.3,
                color=cell_colors[i],
                label=f"Gene {i+1}",
                linewidth=2,
            )
        axes[1, 1].set_title("D. Time Series Expression")
        axes[1, 1].set_xlabel("Time (hours)")
        axes[1, 1].set_ylabel("Expression")
        axes[1, 1].legend(fontsize=8)

        plt.tight_layout()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            plt.savefig(f.name, dpi=300, bbox_inches="tight")
            temp_file = f.name

        plt.close()

        # Verify file exists
        assert os.path.exists(temp_file)
        assert os.path.getsize(temp_file) > 10000  # > 10KB

        # clean up
        os.unlink(temp_file)

    @pytest.mark.requires_matplotlib
    @pytest.mark.requires_seaborn
    def test_correlation_analysis_workflow(self):
        """Scenario: correlation analysis (requires diverging colormap)"""
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns

        from huez.intelligence.colormap_detection import detect_colormap_type

        # Generate simulation data
        np.random.seed(42)
        data = np.random.randn(100, 10)
        corr_matrix = np.corrcoef(data, rowvar=False)

        # Automatic detection should use diverging colormap
        cmap_type = detect_colormap_type(corr_matrix, verbose=False)
        assert cmap_type == "diverging"

        # Create a heat map
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr_matrix,
            cmap="coolwarm",
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax,
        )

        ax.set_title("Correlation Matrix (Auto-detected Diverging Colormap)")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            plt.savefig(f.name, dpi=300, bbox_inches="tight")
            temp_file = f.name

        plt.close()

        assert os.path.exists(temp_file)
        os.unlink(temp_file)

    def test_publication_workflow(self):
        """Scenario: Complete paper chart generation process"""
        import matplotlib.pyplot as plt

        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion

        # 1. Choose a base color palette
        base_palette = ["#E64B35", "#4DBBD5", "#00A087"]

        # 2. Expand to required quantity
        colors_15 = intelligent_color_expansion(base_palette, 15)

        # 3. Verify color blindness friendliness
        safety = check_colorblind_safety(colors_15, verbose=False)

        # 4. If unsafe, use a color-blind friendly palette
        if not safety["safe"]:
            # In practical applications, you should switch to a color-blind friendly palette such as okabe-ito
            pass

        # 5. Create multiple charts
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        # Figure 1: Line graph
        x = np.linspace(0, 10, 100)
        for i in range(min(5, len(colors_15))):
            axes[0].plot(
                x,
                np.sin(x + i * 0.5),
                color=colors_15[i],
                label=f"Series {i+1}",
                linewidth=2,
            )
        axes[0].set_title("(A) Line Plot")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Figure 2: Scatter plot
        for i in range(min(8, len(colors_15))):
            axes[1].scatter(
                np.random.randn(30),
                np.random.randn(30),
                c=colors_15[i],
                label=f"Group {i+1}",
                s=50,
                alpha=0.6,
            )
        axes[1].set_title("(B) Scatter Plot")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Figure 3: Bar chart
        categories = np.arange(10)
        values = np.random.rand(10) * 100
        axes[2].bar(categories, values, color=colors_15[:10])
        axes[2].set_title("(C) Bar Chart")
        axes[2].set_xlabel("Category")
        axes[2].set_ylabel("Value")
        axes[2].grid(True, alpha=0.3, axis="y")

        plt.tight_layout()

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            plt.savefig(f.name, format="pdf", dpi=300, bbox_inches="tight")
            temp_file = f.name

        plt.close()

        assert os.path.exists(temp_file)
        os.unlink(temp_file)


class TestDataScienceWorkflows:
    """Test data science workflows"""

    @pytest.mark.requires_matplotlib
    def test_machine_learning_evaluation(self):
        """Scenario: Machine learning model evaluation visualization"""
        import matplotlib.pyplot as plt

        from huez.intelligence.color_expansion import intelligent_color_expansion

        # Simulate the performance of 5 models
        models = ["Model A", "Model B", "Model C", "Model D", "Model E"]
        colors = intelligent_color_expansion(["#E64B35", "#4DBBD5", "#00A087"], 5)

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # ROC curves
        for i, (model, color) in enumerate(zip(models, colors)):
            fpr = np.linspace(0, 1, 100)
            tpr = 1 - (1 - fpr) ** (1 + i * 0.3)
            axes[0, 0].plot(fpr, tpr, color=color, label=model, linewidth=2)
        axes[0, 0].plot([0, 1], [0, 1], "k--", alpha=0.3)
        axes[0, 0].set_title("ROC Curves")
        axes[0, 0].set_xlabel("False Positive Rate")
        axes[0, 0].set_ylabel("True Positive Rate")
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Training curves
        epochs = np.arange(1, 51)
        for i, (model, color) in enumerate(zip(models, colors)):
            loss = 1.0 * np.exp(-epochs / (10 + i * 2)) + np.random.rand(50) * 0.05
            axes[0, 1].plot(epochs, loss, color=color, label=model, linewidth=2)
        axes[0, 1].set_title("Training Loss")
        axes[0, 1].set_xlabel("Epoch")
        axes[0, 1].set_ylabel("Loss")
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # Performance metrics
        metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
        x = np.arange(len(metrics))
        width = 0.15

        for i, (model, color) in enumerate(zip(models, colors)):
            values = 0.7 + np.random.rand(4) * 0.25
            axes[1, 0].bar(x + i * width, values, width, label=model, color=color)

        axes[1, 0].set_title("Performance Metrics")
        axes[1, 0].set_xlabel("Metric")
        axes[1, 0].set_ylabel("Score")
        axes[1, 0].set_xticks(x + width * 2)
        axes[1, 0].set_xticks_labels(metrics)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3, axis="y")

        # Confusion matrix (for one model)
        confusion = np.array([[85, 10, 5], [8, 90, 2], [12, 3, 85]])
        im = axes[1, 1].imshow(confusion, cmap="Blues")
        axes[1, 1].set_title("Confusion Matrix (Model A)")
        axes[1, 1].set_xlabel("Predicted")
        axes[1, 1].set_ylabel("Actual")
        plt.colorbar(im, ax=axes[1, 1])

        plt.tight_layout()
        plt.close()

    def test_time_series_analysis(self):
        """Scenario: Time Series Data Analysis"""
        import matplotlib.pyplot as plt

        from huez.intelligence.chart_adaptation import (
            adapt_colors_for_chart,
            detect_chart_type,
        )
        from huez.intelligence.color_expansion import intelligent_color_expansion

        # Generate 10 time series
        n_series = 10
        time = np.linspace(0, 100, 500)

        colors = intelligent_color_expansion(
            ["#E64B35", "#4DBBD5", "#00A087"], n_series
        )

        fig, ax = plt.subplots(figsize=(12, 6))

        for i, color in enumerate(colors):
            series = np.sin(time / 10 + i) * (1 + i * 0.1) + np.random.randn(500) * 0.1
            ax.plot(
                time,
                series,
                color=color,
                label=f"Series {i+1}",
                linewidth=1.5,
                alpha=0.8,
            )

        ax.set_title("Multiple Time Series")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        ax.grid(True, alpha=0.3)

        # Detect chart types and get suggestions
        info = detect_chart_type(ax)
        adapted, recs = adapt_colors_for_chart(colors, info)

        # If it is recommended to add markers, you can apply them here
        if recs.get("add_markers"):
            # In actual applications, the diagram with markers will be redrawn.
            pass

        plt.tight_layout()
        plt.close()

        assert info["type"] == "line"


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_data(self):
        """Test empty data handling"""
        from huez.intelligence.colormap_detection import detect_colormap_type

        # empty array
        try:
            result = detect_colormap_type(np.array([]), verbose=False)
            # If no error is reported, the default value should be returned
            assert result in ["sequential", "diverging"]
        except (ValueError, IndexError):
            # Reporting errors is also acceptable
            pass

    def test_extreme_values(self):
        """Test extreme values"""
        from huez.intelligence.colormap_detection import detect_colormap_type

        # very large value
        data = np.array([[1e10, 1e11], [1e12, 1e13]])
        result = detect_colormap_type(data, verbose=False)
        assert result in ["sequential", "diverging"]

        # very small value
        data = np.array([[1e-10, 1e-11], [1e-12, 1e-13]])
        result = detect_colormap_type(data, verbose=False)
        assert result in ["sequential", "diverging"]

    def test_mixed_data_types(self):
        """Test mixed data types"""
        from huez.intelligence.colormap_detection import detect_colormap_type

        # Integer data
        data = np.array([[1, 2, 3], [4, 5, 6]])
        result = detect_colormap_type(data, verbose=False)
        assert result in ["sequential", "diverging"]

        # Float data
        data = np.array([[1.5, 2.5, 3.5], [4.5, 5.5, 6.5]])
        result = detect_colormap_type(data, verbose=False)
        assert result in ["sequential", "diverging"]


class TestUserScenarios:
    """Test real user scenarios"""

    def test_beginner_user_workflow(self):
        """Scenario: Basic workflow for beginner users"""
        from huez.intelligence.accessibility import check_colorblind_safety
        from huez.intelligence.color_expansion import intelligent_color_expansion

        # The user only knows they want 10 colors
        base = ["#E64B35", "#4DBBD5", "#00A087"]

        # Simple call extension
        colors = intelligent_color_expansion(base, 10)

        # Check if color blind friendly
        safety = check_colorblind_safety(colors, verbose=False)

        assert len(colors) == 10
        assert isinstance(safety["safe"], bool)

    @pytest.mark.requires_matplotlib
    def test_advanced_user_workflow(self):
        """Scenario: Complete workflow for advanced users"""
        import matplotlib.pyplot as plt

        from huez.intelligence.accessibility import (
            check_colorblind_safety,
            simulate_colorblind_vision,
        )
        from huez.intelligence.chart_adaptation import (
            adapt_colors_for_chart,
            detect_chart_type,
        )
        from huez.intelligence.color_expansion import intelligent_color_expansion
        from huez.intelligence.colormap_detection import detect_colormap_type

        # 1. Prepare data
        data_heatmap = np.random.randn(20, 20)
        data_line = np.linspace(0, 10, 100)

        # 2. Detect colormap type
        cmap_type = detect_colormap_type(data_heatmap, verbose=False)

        # 3. Extended colors
        base = ["#E64B35", "#4DBBD5", "#00A087"]
        colors = intelligent_color_expansion(base, 8)

        # 4. Check color blindness friendliness
        safety = check_colorblind_safety(colors, verbose=False)

        # 5. If it is not safe, check the simulation effect
        if not safety["safe"]:
            simulate_colorblind_vision(colors, "deuteranopia")
            # Users can decide whether to accept

        # 6. Create charts
        fig, ax = plt.subplots()
        for i, color in enumerate(colors):
            ax.plot(data_line, np.sin(data_line + i * 0.5), color=color)

        # 7. Get chart optimization suggestions
        info = detect_chart_type(ax)
        adapted, recs = adapt_colors_for_chart(colors, info)

        plt.close()

        assert all([cmap_type, colors, safety, info, adapted, recs])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

