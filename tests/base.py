"""Service base for flext-grpc tests."""

from __future__ import annotations

from typing import override

from flext_tests import FlextTestsServiceBase

from flext_grpc import m
from tests.settings import TestsFlextGrpcSettings


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
