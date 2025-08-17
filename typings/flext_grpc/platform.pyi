from _typeshed import Incomplete
from flext_core import FlextResult

from flext_grpc.entities import (
    FlextGrpcClient as FlextGrpcClient,
    FlextGrpcServer as FlextGrpcServer,
    FlextGrpcStream as FlextGrpcStream,
)
from flext_grpc.services import FlextGrpcPlatformService as FlextGrpcPlatformService

class FlextGrpcPlatform:
    config: Incomplete
    container: Incomplete
    def __init__(self, config: dict[str, object] | None = None) -> None: ...
    @property
    def service(self) -> FlextGrpcPlatformService: ...
    def server_operation(
        self, operation: str, server: FlextGrpcServer, **options: object
    ) -> FlextResult[object]: ...
    def client_operation(
        self, operation: str, client: FlextGrpcClient, **options: object
    ) -> FlextResult[object]: ...
    def stream_operation(
        self, operation: str, **options: object
    ) -> FlextResult[object]: ...
    def start_server(
        self, server: FlextGrpcServer, **options: object
    ) -> FlextResult[FlextGrpcServer]: ...
    def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]: ...
    def connect_client(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextGrpcClient]: ...
    def make_call(
        self,
        client: FlextGrpcClient,
        method_name: str,
        request_data: object,
        **options: object,
    ) -> FlextResult[object]: ...
    def get_server_status(
        self, server: FlextGrpcServer
    ) -> FlextResult[dict[str, object]]: ...
    def get_client_status(
        self, client: FlextGrpcClient
    ) -> FlextResult[dict[str, object]]: ...
    def create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str,
        stream_type: str = "unary",
        **options: object,
    ) -> FlextResult[FlextGrpcStream]: ...
