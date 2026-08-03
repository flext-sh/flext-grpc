"""Runtime settings for flext-grpc tests."""

from __future__ import annotations

from flext_grpc import FlextGrpcSettings
from flext_tests import FlextTestsSettings


class TestsFlextGrpcSettings(FlextGrpcSettings, FlextTestsSettings):
    """gRPC settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextGrpcSettings"]
