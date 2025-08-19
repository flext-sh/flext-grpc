"""Test __init__.py version handling.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib
import importlib.metadata
from unittest.mock import patch

import flext_grpc


def test_version_fallback() -> None:
    """Test version fallback when package not found."""
    with patch(
        "importlib.metadata.version",
        side_effect=importlib.metadata.PackageNotFoundError,
    ):
        # Reload the module to test the exception path
        # All imports are at the top of the file

        importlib.reload(flext_grpc)
        assert flext_grpc.__version__ == "1.0.0"


def test_version_info_parsing() -> None:
    """Test version info tuple parsing."""
    # All imports are at the top of the file

    # Should be a tuple of integers
    assert isinstance(flext_grpc.__version_info__, tuple)
    assert all(isinstance(x, int) for x in flext_grpc.__version_info__)
