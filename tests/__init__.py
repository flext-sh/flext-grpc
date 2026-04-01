# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests.conftest import *
    from tests.constants import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("tests.unit",),
    {
        "FlextGrpcTestConstants": "tests.constants",
        "FlextGrpcTestModels": "tests.models",
        "FlextGrpcTestProtocols": "tests.protocols",
        "FlextGrpcTestTypes": "tests.typings",
        "FlextGrpcTestUtilities": "tests.utilities",
        "c": ("tests.constants", "FlextGrpcTestConstants"),
        "clean_container": "tests.conftest",
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "m": ("tests.models", "FlextGrpcTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextGrpcTestProtocols"),
        "protocols": "tests.protocols",
        "r": "flext_tests",
        "s": "flext_tests",
        "sample_grpc_config": "tests.conftest",
        "t": ("tests.typings", "FlextGrpcTestTypes"),
        "test_addresses": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextGrpcTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
