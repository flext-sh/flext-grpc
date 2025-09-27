from collections.abc import Callable
from typing import Protocol

from echo_pb2 import EchoRequest, EchoResponse
from grpc import (
    CallCredentials,
    Channel,
    ChannelCredentials,
    Compression,
    Server,
    ServicerContext,
)

class EchoServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    Echo: Callable[[EchoRequest], EchoResponse]

class EchoServiceServicer(Protocol):
    def Echo(self, request: EchoRequest, context: ServicerContext) -> EchoResponse: ...  # noqa: N802

def add_EchoServiceServicer_to_server(  # noqa: N802
    servicer: EchoServiceServicer, server: Server
) -> None: ...

class EchoService:
    @staticmethod
    def Echo(  # noqa: N802
        request: EchoRequest,
        target: str,
        options: tuple[()] = (),
        channel_credentials: ChannelCredentials | None = None,
        call_credentials: CallCredentials | None = None,
        insecure: bool = False,
        compression: Compression | None = None,
        wait_for_ready: bool | None = None,
        timeout: float | None = None,
        metadata: tuple[tuple[str, str], ...] | None = None,
    ) -> EchoResponse: ...
