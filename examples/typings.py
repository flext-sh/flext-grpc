"""FLEXT gRPC example type aliases."""

from __future__ import annotations

from flext_grpc import FlextGrpcModels

type CompleteSetup = dict[
    str,
    FlextGrpcModels.Grpc.Server
    | FlextGrpcModels.Grpc.Client
    | FlextGrpcModels.Grpc.Service
    | str,
]
