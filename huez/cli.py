"""
Command-line interface for huez.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import click

from .core import (
    load_config,
    use,
    current_scheme,
    palette,
    cmap,
    preview_gallery,
    check_palette,
    lint_figure,
    _current_config
)
from .config import save_config_to_file, Config
from .data.defaults import get_default_config


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """huez - Your all-in-one color solution in Python."""
    pass


@cli.command()
@click.option(
    "--preset",
    type=click.Choice(["minimal", "full"]),
    default="minimal",
    help="Configuration preset to use."
)
@click.option(
    "--out",
    type=click.Path(),
    default="huez.yaml",
    help="Output configuration file path."
)
def init(preset: str, out: str):
    """
    Initialize a new huez configuration file.

    Examples:
        huez init --preset minimal --out huez.yaml
        huez init --preset full --out config/huez.yaml
    """
    if preset == "minimal":
        config = get_default_config()
    else:
        # For "full" preset, we could add more schemes
        config = get_default_config()

    try:
        save_config_to_file(config, out)
        click.echo(f"✅ Configuration initialized and saved to {out}")
        click.echo(f"Available schemes: {', '.join(config.schemes.keys())}")
    except Exception as e:
        click.echo(f"❌ Failed to save configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("scheme_name")
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file. Uses built-in defaults if not specified."
)
def use_cmd(scheme_name: str, config: Optional[str]):
    """
    Apply a color scheme to all available visualization libraries.

    Examples:
        huez use scheme-1
        huez use scheme-2 --config myconfig.yaml
    """
    try:
        if config:
            load_config(config)

        use(scheme_name)
        click.echo(f"✅ Applied scheme '{scheme_name}' to available libraries")

        # Show which libraries were affected
        from .adapters.base import get_adapter_status
        status = get_adapter_status()
        available = [lib for lib, avail in status.items() if avail]
        if available:
            click.echo(f"Libraries updated: {', '.join(available)}")
        else:
            click.echo("⚠️  No visualization libraries found")

    except Exception as e:
        click.echo(f"❌ Failed to apply scheme: {e}", err=True)
        sys.exit(1)


@cli.command()
def current():
    """
    Show the currently active scheme.

    Examples:
        huez current
    """
    scheme = current_scheme()
    if scheme:
        click.echo(f"Current scheme: {scheme}")
    else:
        click.echo("No scheme is currently active")


@cli.command()
@click.argument("kind", type=click.Choice(["schemes", "palettes"]))
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file."
)
def list(kind: str, config: Optional[str]):
    """
    List available schemes or palettes.

    Examples:
        huez list schemes
        huez list palettes
        huez list schemes --config myconfig.yaml
    """
    try:
        if config:
            load_config(config)

        if kind == "schemes":
            if _current_config is None:
                load_config()
            if _current_config:
                click.echo("Available schemes:")
                for name, scheme in _current_config.schemes.items():
                    click.echo(f"  • {name}: {scheme.title}")
            else:
                click.echo("❌ No configuration loaded")

        elif kind == "palettes":
            from .registry import list_available_palettes
            palettes = list_available_palettes()

            click.echo("Available palettes:")
            for palette_kind, palette_names in palettes.items():
                click.echo(f"  {palette_kind}:")
                for name in palette_names:
                    click.echo(f"    • {name}")

    except Exception as e:
        click.echo(f"❌ Failed to list {kind}: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--scheme",
    help="Scheme name to export. Uses current scheme if not specified."
)
@click.option(
    "--out",
    type=click.Path(),
    default="tokens",
    help="Output directory for token files."
)
@click.option(
    "--formats",
    help="Comma-separated list of formats to export (css,json,js). Exports all if not specified."
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file."
)
@click.option(
    "--scheme",
    help="Scheme name to export. Uses current scheme if not specified."
)
@click.option(
    "--out",
    type=click.Path(),
    default="tokens",
    help="Output directory for token files."
)
@click.option(
    "--formats",
    help="Comma-separated list of formats to export (css,json,js). Exports all if not specified."
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file."
)
def tokens(scheme: Optional[str], out: str, formats: Optional[str], config: Optional[str]):
    """
    Export color tokens for web/JavaScript integration.

    Examples:
        huez export tokens --scheme scheme-1 --out tokens/
        huez export tokens --formats css,json --out web_tokens/
    """
    try:
        if config:
            load_config(config)

        if not scheme:
            scheme = current_scheme()
            if not scheme:
                click.echo("❌ No scheme is currently active. Specify --scheme or run 'huez use' first.", err=True)
                sys.exit(1)

        # Parse formats
        format_list = None
        if formats:
            format_list = [f.strip() for f in formats.split(",")]

        from .export.tokens import export_tokens
        export_tokens(_current_config.schemes[scheme], out, format_list)
        click.echo(f"✅ Exported tokens for scheme '{scheme}' to {out}")

    except Exception as e:
        click.echo(f"❌ Failed to export tokens: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--scheme",
    help="Scheme name to preview. Uses current scheme if not specified."
)
@click.option(
    "--out",
    type=click.Path(),
    default="gallery",
    help="Output directory for preview files."
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file."
)
def preview(scheme: Optional[str], out: str, config: Optional[str]):
    """
    Generate a preview gallery showing the scheme.

    Examples:
        huez preview --scheme scheme-1 --out gallery/
        huez preview --out my_preview/
    """
    try:
        if config:
            load_config(config)

        if not scheme:
            scheme = current_scheme()
            if not scheme:
                click.echo("❌ No scheme is currently active. Specify --scheme or run 'huez use' first.", err=True)
                sys.exit(1)

        preview_gallery(out, scheme)
        click.echo(f"✅ Generated preview gallery for scheme '{scheme}' to {out}")

    except Exception as e:
        click.echo(f"❌ Failed to generate preview: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--scheme",
    help="Scheme name to check. Uses current scheme if not specified."
)
@click.option(
    "--kinds",
    help="Comma-separated list of palette kinds to check (discrete,sequential,diverging,cyclic). Checks all if not specified."
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file."
)
def check(scheme: Optional[str], kinds: Optional[str], config: Optional[str]):
    """
    Check palette quality (colorblind safety, contrast, etc.).

    Examples:
        huez check --scheme scheme-1
        huez check --kinds discrete,sequential
    """
    try:
        if config:
            load_config(config)

        if not scheme:
            scheme = current_scheme()
            if not scheme:
                click.echo("❌ No scheme is currently active. Specify --scheme or run 'huez use' first.", err=True)
                sys.exit(1)

        # Parse kinds
        kind_list = None
        if kinds:
            kind_list = [k.strip() for k in kinds.split(",")]

        results = check_palette(scheme, kind_list)

        click.echo(f"✅ Quality check results for scheme '{scheme}':")
        for kind, checks in results.items():
            click.echo(f"  {kind}:")
            if "error" in checks:
                click.echo(f"    ❌ {checks['error']}")
            else:
                for check_name, status in checks.items():
                    if isinstance(status, bool):
                        icon = "✅" if status else "⚠️"
                        click.echo(f"    {icon} {check_name}")
                    else:
                        click.echo(f"    • {check_name}: {status}")

    except Exception as e:
        click.echo(f"❌ Failed to check palette: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--report",
    type=click.Path(),
    help="Optional path to save detailed report as JSON."
)
def lint(file_path: str, report: Optional[str]):
    """
    Lint a figure file for visualization best practices.

    Examples:
        huez lint figure.png
        huez lint figure.svg --report report.json
    """
    try:
        results = lint_figure(file_path, report)

        click.echo(f"✅ Lint results for {file_path}:")

        if "error" in results:
            click.echo(f"❌ {results['error']}")
            return

        issues = results.get("issues", [])
        if not issues:
            click.echo("  ✅ No issues found")
        else:
            for issue in issues:
                severity = issue.get("severity", "info")
                if severity == "error":
                    icon = "❌"
                elif severity == "warning":
                    icon = "⚠️"
                else:
                    icon = "ℹ️"

                click.echo(f"  {icon} {issue.get('message', 'Unknown issue')}")

                if "suggestion" in issue:
                    click.echo(f"      💡 {issue['suggestion']}")

        if report:
            click.echo(f"📄 Detailed report saved to {report}")

    except Exception as e:
        click.echo(f"❌ Failed to lint figure: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
