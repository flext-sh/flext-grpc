from typing import Any

import grpc

class FlextServiceServicer: ...

class FlextServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...

def add_FlextServiceServicer_to_server(  # noqa: N802
    servicer: Any,
    server: grpc.Server | grpc.aio.Server,
) -> None: ...
