from flext_core import FlextResult

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)

__all__ = [
    "create_channel",
    "create_client",
    "create_complete_setup",
    "create_config",
    "create_server",
    "create_service",
    "create_stream",
    "parse_address",
    "validate_address",
    "validate_host",
    "validate_port",
]

def create_server(
    host: str, port: int, max_workers: int = 10
) -> FlextResult[FlextGrpcServer]: ...
def create_client(target: str) -> FlextResult[FlextGrpcClient]: ...
def create_channel(target: str) -> FlextResult[FlextGrpcChannel]: ...
def create_service(
    name: str, methods: list[str] | None = None
) -> FlextResult[FlextGrpcService]: ...
def create_stream(
    stream_type: str, method_name: str
) -> FlextResult[FlextGrpcStream]: ...
def create_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextResult[object]: ...
def create_complete_setup(
    _server_id: str = "default-server",
    _client_id: str = "default-client",
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    *,
    _ssl_enabled: bool = False,
) -> FlextResult[dict[str, object]]: ...
def validate_address(address: str) -> bool: ...
def parse_address(address: str) -> FlextResult[tuple[str, int]]: ...
def validate_host(host: str) -> bool: ...
def validate_port(port: int) -> bool: ...
