"""
Pytest configuration and fixtures for huez tests.
"""

import os
import pytest


# Module-level config to ensure persistence
_test_config = None


def pytest_configure(config):
    """Configure pytest with test config at startup."""
    import huez.core as core

    global _test_config

    # Get path to test config
    test_dir = os.path.dirname(__file__)
    test_config_path = os.path.join(test_dir, "test_config.yaml")

    # Load test configuration once
    if os.path.exists(test_config_path):
        _test_config = core.load_config(test_config_path)
        core._current_config = _test_config


@pytest.fixture(autouse=True)
def ensure_test_config():
    """Ensure test configuration is loaded for each test."""
    import huez.core as core
    import matplotlib.pyplot as plt

    # Save original state
    original_config = core._current_config
    original_scheme = core._current_scheme

    # Ensure config is loaded
    if _test_config is not None:
        core._current_config = _test_config

    yield

    # Restore test config if it was changed (but keep scheme reset)
    if _test_config is not None:
        core._current_config = _test_config

    # Close any matplotlib figures after each test
    plt.close("all")
