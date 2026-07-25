"""Service base for flext-grpc tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_grpc import m
from tests.settings import TestsFlextGrpcSettings


class TestsFlextGrpcServiceBase(tests_s):
    """gRPC test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextGrpcSettings:
        """Return the typed gRPC+Tests settings singleton."""
        return TestsFlextGrpcSettings.fetch_global()

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextGrpcSettings)


s = TestsFlextGrpcServiceBase

__all__: list[str] = ["TestsFlextGrpcServiceBase", "s"]
