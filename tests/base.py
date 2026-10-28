"""Service base for flext-grpc tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/base
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import override

from flext_tests import FlextTestsServiceBase

from tests import TestsFlextGrpcSettings, m


class TestsFlextGrpcServiceBase(FlextTestsServiceBase):
    """gRPC test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextGrpcSettings)


s = TestsFlextGrpcServiceBase

__all__: list[str] = ["TestsFlextGrpcServiceBase", "s"]
