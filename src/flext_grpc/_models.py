"""Auto-generated centralized models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_grpc.protocols import FlextGrpcProtocols


class FlextAutoConstants:
    pass


class FlextAutoTypes:
    pass


class FlextAutoProtocols:
    pass


class FlextAutoUtilities:
    pass


class FlextAutoModels:
    pass


c = FlextAutoConstants
t = FlextAutoTypes
p = FlextAutoProtocols
u = FlextAutoUtilities
m = FlextAutoModels


class GrpcCompleteSetup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    server: FlextGrpcProtocols.Grpc.GrpcServer
    client: FlextGrpcProtocols.Grpc.GrpcStub
    service: FlextGrpcProtocols.Grpc.GrpcServicer
    target: str
