"""Test __init__.py version handling.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib.metadata
from unittest.mock import patch


def test_version_fallback() -> None:
    """Test version fallback when package not found."""
    with patch(
        "importlib.metadata.version",
        side_effect=importlib.metadata.PackageNotFoundError,
    ):
        # Reload the module to test the exception path
        import flext_grpc

        importlib.reload(flext_grpc)
        assert flext_grpc.__version__ == "1.0.0"


def test_version_info_parsing() -> None:
    """Test version info tuple parsing."""
    import flext_grpc

    # Should be a tuple of integers
    assert isinstance(flext_grpc.__version_info__, tuple)
    assert all(isinstance(x, int) for x in flext_grpc.__version_info__)
