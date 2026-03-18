"""Auto-generated centralized models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


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
    server: object
    client: object
    service: object
    target: str
