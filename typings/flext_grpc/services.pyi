from flext_core import FlextDomainService, FlextResult

from flext_grpc.constants import FlextGrpcConstants as FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcChannel as FlextGrpcChannel,
    FlextGrpcClient as FlextGrpcClient,
    FlextGrpcEntityFactory as FlextGrpcEntityFactory,
    FlextGrpcServer as FlextGrpcServer,
    FlextGrpcService as FlextGrpcService,
    FlextGrpcStream as FlextGrpcStream,
)

class _GrpcServiceValidationMixin: ...

class FlextGrpcServerService(
    FlextDomainService[FlextGrpcServer], _GrpcServiceValidationMixin
):
    def execute(self) -> FlextResult[FlextGrpcServer]: ...
    def execute_operation(
        self, *args: object, **kwargs: object
    ) -> FlextResult[object]: ...

class FlextGrpcClientService(
    FlextDomainService[FlextGrpcClient], _GrpcServiceValidationMixin
):
    def execute(self) -> FlextResult[FlextGrpcClient]: ...
    def execute_operation(
        self, *args: object, **kwargs: object
    ) -> FlextResult[object]: ...

class FlextGrpcStreamService(FlextDomainService[FlextGrpcStream]):
    def execute(self) -> FlextResult[FlextGrpcStream]: ...
    def execute_operation(
        self, *args: object, **kwargs: object
    ) -> FlextResult[object]: ...

class FlextGrpcPlatformService(FlextDomainService[object]):
    def __init__(self) -> None: ...
    def execute(self) -> FlextResult[object]: ...
    def execute_operation(
        self, *args: object, **kwargs: object
    ) -> FlextResult[object]: ...
