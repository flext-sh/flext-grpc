"""FLEXT gRPC example type aliases."""

from __future__ import annotations

from collections.abc import Mapping

from flext_grpc import FlextGrpcModels

type CompleteSetup = Mapping[
    str,
    FlextGrpcModels.Grpc.Server
    | FlextGrpcModels.Grpc.Client
    | FlextGrpcModels.Grpc.Service
    | str,
]
