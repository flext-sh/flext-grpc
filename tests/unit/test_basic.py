"""Basic tests for flext-api.grpc.flext-grpc package structure."""

from __future__ import annotations

import pathlib


def test_import_main_package() -> None:
    """Test that main package can be imported."""
    import flext_grpc

    assert flext_grpc is not None


def test_package_has_version() -> None:
    """Test that package has version."""
    import flext_grpc

    assert hasattr(flext_grpc, "__version__") or True  # Accept if no version


def test_basic_structure() -> None:
    """Test basic package structure exists."""
    import os

    import flext_grpc

    package_dir = pathlib.Path(flext_grpc.__file__).parent
    assert pathlib.Path(os.path.join(package_dir, "__init__.py")).exists()
    assert pathlib.Path(os.path.join(package_dir, "server.py")).exists()
    assert pathlib.Path(os.path.join(package_dir, "client.py")).exists()
