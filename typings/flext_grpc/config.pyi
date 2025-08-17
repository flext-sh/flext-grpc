from flext_core import FlextBaseConfigModel

__all__ = ["FlextGrpcConfig"]

class FlextGrpcConfig(FlextBaseConfigModel):
    host: str
    port: int
    max_workers: int
    timeout: float
    @classmethod
    def validate_host(cls, v: str) -> str: ...
    @classmethod
    def validate_port(cls, v: int) -> int: ...
    @classmethod
    def validate_max_workers(cls, v: int) -> int: ...
    @classmethod
    def validate_timeout(cls, v: float) -> float: ...
    def get_address(self) -> str: ...
