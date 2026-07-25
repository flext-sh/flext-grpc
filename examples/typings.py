"""FLEXT gRPC example type aliases."""

from __future__ import annotations

from flext_grpc import FlextGrpcModels, FlextGrpcTypes


class ExamplesFlextGrpcTypes(FlextGrpcTypes):
    """Example type aliases for flext-grpc."""

    class Grpc(FlextGrpcTypes.Grpc):
        """gRPC example type namespace."""

        type CompleteSetup = FlextGrpcModels.Grpc.CompleteSetup


t = ExamplesFlextGrpcTypes

__all__: list[str] = ["ExamplesFlextGrpcTypes", "t"]
