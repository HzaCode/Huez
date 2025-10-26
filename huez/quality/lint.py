"""
Figure linting tools for visualization best practices.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import warnings


def lint_figure_file(
    file_path: str, report_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lint a figure file for visualization best practices.

    Args:
        file_path: Path to the figure file
        report_path: Optional path to save detailed report

    Returns:
        Dictionary with linting results
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}

    # Get file extension
    ext = file_path.suffix.lower()

    if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return _lint_raster_image(file_path, report_path)
    elif ext in [".svg", ".pdf"]:
        return _lint_vector_image(file_path, report_path)
    else:
        return {"error": f"Unsupported file format: {ext}"}


def _lint_raster_image(file_path: Path, report_path: Optional[str]) -> Dict[str, Any]:
    """Lint a raster image file."""
    issues = []

    try:
        from PIL import Image
        import numpy as np

        img = Image.open(file_path)
        img_array = np.array(img)

        # Check image dimensions
        width, height = img.size
        if width < 300 or height < 200:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"Image dimensions ({width}x{height}) may be too small for publication",
                    "suggestion": "Consider increasing resolution to at least 600x400 pixels",
                }
            )

        # Check color space
        if img.mode not in ["RGB", "RGBA", "L", "LA"]:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"Image color mode '{img.mode}' may not be suitable for all publications",
                    "suggestion": "Convert to RGB or grayscale for better compatibility",
                }
            )

        # Check for transparency
        if img.mode in ["RGBA", "LA", "P"]:
            if "A" in img.mode or (hasattr(img, "info") and "transparency" in img.info):
                issues.append(
                    {
                        "severity": "info",
                        "message": "Image contains transparency",
                        "suggestion": "Ensure transparency is handled correctly in your publication system",
                    }
                )

        # Basic color analysis
        if img.mode == "RGB":
            color_analysis = _analyze_colors(img_array)
            issues.extend(color_analysis)

        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > 10:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"File size ({file_size_mb:.1f} MB) is quite large",
                    "suggestion": "Consider optimizing compression or reducing resolution",
                }
            )

    except ImportError:
        issues.append(
            {
                "severity": "info",
                "message": "PIL not available for detailed image analysis",
                "suggestion": "Install pillow for more comprehensive image linting",
            }
        )
    except Exception as e:
        return {"error": f"Failed to analyze image: {e}"}

    result = {
        "file_path": str(file_path),
        "file_type": "raster",
        "issues": issues,
        "summary": {
            "total_issues": len(issues),
            "errors": len([i for i in issues if i["severity"] == "error"]),
            "warnings": len([i for i in issues if i["severity"] == "warning"]),
            "info": len([i for i in issues if i["severity"] == "info"]),
        },
    }

    if report_path:
        _save_report(result, report_path)
        result["report_path"] = report_path

    return result


def _lint_vector_image(file_path: Path, report_path: Optional[str]) -> Dict[str, Any]:
    """Lint a vector image file."""
    issues = []

    try:
        # Read file content
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Check file size
        file_size_kb = len(content) / 1024
        if file_size_kb > 500:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"Vector file size ({file_size_kb:.1f} KB) is quite large",
                    "suggestion": "Consider simplifying the graphic or using raster format",
                }
            )

        # SVG-specific checks
        if file_path.suffix.lower() == ".svg":
            svg_issues = _lint_svg_content(content)
            issues.extend(svg_issues)

        # PDF-specific checks
        elif file_path.suffix.lower() == ".pdf":
            pdf_issues = _lint_pdf_content(content)
            issues.extend(pdf_issues)

        # Check for embedded fonts
        if "font-family" in content.lower():
            if "embedded" not in content.lower() and "fontfile" not in content.lower():
                issues.append(
                    {
                        "severity": "warning",
                        "message": "Custom fonts detected but may not be embedded",
                        "suggestion": "Ensure fonts are embedded in the final document",
                    }
                )

    except UnicodeDecodeError:
        issues.append(
            {
                "severity": "warning",
                "message": "Could not read file as text - may be binary PDF",
                "suggestion": "For PDFs, ensure text is properly encoded",
            }
        )
    except Exception as e:
        return {"error": f"Failed to analyze vector file: {e}"}

    result = {
        "file_path": str(file_path),
        "file_type": "vector",
        "issues": issues,
        "summary": {
            "total_issues": len(issues),
            "errors": len([i for i in issues if i["severity"] == "error"]),
            "warnings": len([i for i in issues if i["severity"] == "warning"]),
            "info": len([i for i in issues if i["severity"] == "info"]),
        },
    }

    if report_path:
        _save_report(result, report_path)
        result["report_path"] = report_path

    return result


def _lint_svg_content(content: str) -> List[Dict[str, Any]]:
    """Lint SVG content for specific issues."""
    issues = []

    # Check for rainbow colormaps (problematic for colorblind)
    rainbow_indicators = ["rainbow", "jet", "hsv", "spectral"]
    content_lower = content.lower()

    for indicator in rainbow_indicators:
        if indicator in content_lower:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"Potential rainbow colormap detected ('{indicator}')",
                    "suggestion": "Consider using perceptually uniform colormaps like viridis or cividis",
                }
            )

    # Check for red-green color combinations
    if "stroke:#ff" in content_lower or "fill:#ff" in content_lower:
        if "stroke:#00ff00" in content_lower or "fill:#00ff00" in content_lower:
            issues.append(
                {
                    "severity": "warning",
                    "message": "Red-green color combination detected",
                    "suggestion": "This combination is problematic for colorblind viewers",
                }
            )

    # Check for very thin lines
    if "stroke-width:0." in content or "stroke-width:1" in content:
        issues.append(
            {
                "severity": "info",
                "message": "Very thin lines detected",
                "suggestion": "Ensure line widths are appropriate for the output medium",
            }
        )

    # Check for missing alt text or descriptions
    if "<desc>" not in content and "<title>" not in content:
        issues.append(
            {
                "severity": "info",
                "message": "No title or description found in SVG",
                "suggestion": "Add <title> and <desc> elements for accessibility",
            }
        )

    return issues


def _lint_pdf_content(content: str) -> List[Dict[str, Any]]:
    """Lint PDF content for specific issues."""
    issues = []

    # Check for font embedding
    if "/Font" in content:
        if "/Embedded" not in content and "/FontFile" not in content:
            issues.append(
                {
                    "severity": "warning",
                    "message": "Fonts may not be embedded",
                    "suggestion": "Ensure all fonts are embedded in the PDF",
                }
            )

    # Check for images
    if "/Image" in content:
        issues.append(
            {
                "severity": "info",
                "message": "PDF contains raster images",
                "suggestion": "Consider using vector graphics for better scalability",
            }
        )

    return issues


def _analyze_colors(img_array) -> List[Dict[str, Any]]:
    """Analyze colors in an image array."""
    issues = []

    try:
        # Get unique colors
        unique_colors = set()
        for row in img_array:
            for pixel in row:
                if len(pixel) >= 3:  # RGB or RGBA
                    unique_colors.add(tuple(pixel[:3]))

        n_colors = len(unique_colors)

        if n_colors > 20:
            issues.append(
                {
                    "severity": "info",
                    "message": f"Image uses {n_colors} unique colors",
                    "suggestion": "Consider if this level of color variation is necessary",
                }
            )

        # Check for grayscale
        is_grayscale = True
        for color in unique_colors:
            r, g, b = color
            if r != g or g != b:
                is_grayscale = False
                break

        if is_grayscale:
            issues.append(
                {
                    "severity": "info",
                    "message": "Image appears to be grayscale",
                    "suggestion": "Ensure contrast is sufficient for all viewing conditions",
                }
            )

    except Exception as e:
        issues.append(
            {
                "severity": "info",
                "message": f"Could not analyze colors: {e}",
                "suggestion": "Manual color review recommended",
            }
        )

    return issues


def _save_report(result: Dict[str, Any], report_path: str) -> None:
    """Save linting report to file."""
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    except Exception as e:
        warnings.warn(f"Failed to save report to {report_path}: {e}")


def lint_batch(file_paths: List[str], output_dir: str) -> Dict[str, Any]:
    """
    Lint multiple figure files and save individual reports.

    Args:
        file_paths: List of file paths to lint
        output_dir: Directory to save individual reports

    Returns:
        Summary of all linting results
    """
    os.makedirs(output_dir, exist_ok=True)

    all_results = {}
    summary = {
        "total_files": len(file_paths),
        "total_issues": 0,
        "errors": 0,
        "warnings": 0,
        "info": 0,
    }

    for file_path in file_paths:
        file_name = Path(file_path).stem
        report_path = os.path.join(output_dir, f"{file_name}_lint.json")

        result = lint_figure_file(file_path, report_path)
        all_results[file_path] = result

        if "summary" in result:
            s = result["summary"]
            summary["total_issues"] += s["total_issues"]
            summary["errors"] += s["errors"]
            summary["warnings"] += s["warnings"]
            summary["info"] += s["info"]

    # Save summary
    summary_path = os.path.join(output_dir, "lint_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(
            {"summary": summary, "files": all_results}, f, indent=2, ensure_ascii=False
        )

    return {"summary": summary, "files": all_results}
