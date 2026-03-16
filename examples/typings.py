from __future__ import annotations

type CompleteSetup = dict[
    str,
    FlextGrpcModels.Grpc.Server
    | FlextGrpcModels.Grpc.Client
    | FlextGrpcModels.Grpc.Service
    | str,
]
