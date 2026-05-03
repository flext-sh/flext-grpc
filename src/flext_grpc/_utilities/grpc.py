"""Internal gRPC utility mixin with typed entity factories."""

from __future__ import annotations

from collections.abc import (
    Callable,
)
from concurrent.futures import ThreadPoolExecutor
from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING
from uuid import uuid4

from flext_core import u
from flext_grpc import c, m, p, r, t

if TYPE_CHECKING:
    from flext_grpc import FlextGrpcModels

logger = u.create_module_logger(__name__)


class FlextGrpcUtilitiesGrpc:
    """gRPC utility namespace composed into ``FlextGrpcUtilities.Grpc``."""

    class _GrpcRuntimeAdapter:
        """Typed adapter that isolates the untyped grpc runtime module."""

        RpcError: type[Exception]
        FutureTimeoutError: type[Exception]

        def __init__(self, runtime_module: ModuleType) -> None:
            """Store the imported grpc module."""
            self._runtime_module = runtime_module
            self.RpcError = self._exception_type(
                self._runtime_module.RpcError,
                "RpcError",
            )
            self.FutureTimeoutError = self._exception_type(
                self._runtime_module.FutureTimeoutError,
                "FutureTimeoutError",
            )

        @staticmethod
        def _exception_type(
            value: type[BaseException],
            name: str,
        ) -> type[Exception]:
            """Validate that the runtime exposes an Exception subtype."""
            if issubclass(value, Exception):
                return value
            msg = f"grpc.{name} is not an Exception subtype"
            raise TypeError(msg)

        def insecure_channel(self, target: str) -> p.Grpc.GrpcChannel:
            """Create a typed insecure channel from the runtime module."""
            channel = self._runtime_module.insecure_channel(target)
            if not isinstance(channel, p.Grpc.GrpcChannel):
                msg = "grpc.insecure_channel returned an invalid channel"
                raise TypeError(msg)
            return channel

        def channel_ready_future(
            self,
            channel: p.Grpc.GrpcChannel,
        ) -> p.Grpc.GrpcReadyFuture:
            """Create a typed ready future for the given channel."""
            ready_future = self._runtime_module.channel_ready_future(channel)
            if not isinstance(ready_future, p.Grpc.GrpcReadyFuture):
                msg = "grpc.channel_ready_future returned an invalid future"
                raise TypeError(msg)
            return ready_future

        def server(
            self,
            thread_pool: ThreadPoolExecutor,
        ) -> p.Grpc.GrpcServer:
            """Create a typed gRPC server from the runtime module."""
            grpc_server = self._runtime_module.server(thread_pool)
            if not isinstance(grpc_server, p.Grpc.GrpcServer):
                msg = "grpc.server returned an invalid server"
                raise TypeError(msg)
            return grpc_server

    @staticmethod
    def resolve_runtime() -> p.Result[p.Grpc.GrpcRuntime]:
        """Load the grpc runtime through the typed adapter boundary."""
        runtime_result = u.try_(
            lambda: import_module("grpc"),
            catch=(ImportError, ModuleNotFoundError),
        )
        if runtime_result.failure:
            return r[p.Grpc.GrpcRuntime].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        return r[p.Grpc.GrpcRuntime].ok(
            FlextGrpcUtilitiesGrpc._GrpcRuntimeAdapter(runtime_result.value),
        )

    @staticmethod
    def _grpc_models() -> type[FlextGrpcModels]:
        """Resolve the local models facade after package initialization."""
        models_module = import_module("flext_grpc.models")
        return models_module.FlextGrpcModels

    @staticmethod
    def runtime_error_message(exception: BaseException | None) -> str:
        """Normalize a runtime exception into a stable public message."""
        if exception is None:
            return "Unknown gRPC error"
        if isinstance(exception, p.Grpc.GrpcCallFailure):
            code_value = exception.code()
            details_value = exception.details()
            if code_value is None:
                return details_value
            return f"{code_value} - {details_value}"
        return str(exception)

    @staticmethod
    def runtime_failure_message[TValue](result: p.ResultLike[TValue]) -> str:
        """Return the most useful error message from a grpc runtime result."""
        if result.exception is not None:
            return FlextGrpcUtilitiesGrpc.runtime_error_message(result.exception)
        return result.error or "Unknown gRPC error"

    @staticmethod
    def _runtime_exception_types(
        runtime: p.Grpc.GrpcRuntime,
    ) -> tuple[type[Exception], ...]:
        """Return the canonical exception types raised by the grpc runtime."""
        return (
            ConnectionError,
            TimeoutError,
            runtime.RpcError,
            runtime.FutureTimeoutError,
        )

    @staticmethod
    def call_runtime[TValue](operation: Callable[[], TValue]) -> p.Result[TValue]:
        """Execute a runtime operation using the canonical grpc exception set."""
        runtime_result = FlextGrpcUtilitiesGrpc.resolve_runtime()
        if runtime_result.failure:
            return r[TValue].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        runtime = runtime_result.value
        return u.try_(
            operation,
            catch=FlextGrpcUtilitiesGrpc._runtime_exception_types(runtime),
        )

    @staticmethod
    def run_runtime(operation: Callable[[], None]) -> p.Result[bool]:
        """Execute a side-effecting runtime operation."""

        def _run() -> bool:
            operation()
            return True

        return FlextGrpcUtilitiesGrpc.call_runtime(_run)

    @staticmethod
    def open_insecure_channel(
        target: str,
        *,
        timeout: float = c.Grpc.NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT,
    ) -> p.Result[p.Grpc.GrpcChannel]:
        """Open an insecure channel and wait until it is ready."""
        runtime_result = FlextGrpcUtilitiesGrpc.resolve_runtime()
        if runtime_result.failure:
            return r[p.Grpc.GrpcChannel].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        runtime = runtime_result.value

        def _open() -> p.Grpc.GrpcChannel:
            grpc_channel = runtime.insecure_channel(target)
            runtime.channel_ready_future(grpc_channel).result(timeout=timeout)
            return grpc_channel

        return u.try_(
            _open,
            catch=FlextGrpcUtilitiesGrpc._runtime_exception_types(runtime),
        )

    @staticmethod
    def create_runtime_server(
        thread_pool: ThreadPoolExecutor,
    ) -> p.Result[p.Grpc.GrpcServer]:
        """Create a runtime grpc server using the canonical adapter."""
        runtime_result = FlextGrpcUtilitiesGrpc.resolve_runtime()
        if runtime_result.failure:
            return r[p.Grpc.GrpcServer].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        runtime = runtime_result.value
        return u.try_(
            lambda: runtime.server(thread_pool),
            catch=FlextGrpcUtilitiesGrpc._runtime_exception_types(runtime),
        )

    @staticmethod
    def bind_insecure_port(
        server: p.Grpc.GrpcServer,
        address: str,
    ) -> p.Result[int]:
        """Bind an address to a runtime grpc server."""
        return FlextGrpcUtilitiesGrpc.call_runtime(
            lambda: server.add_insecure_port(address),
        )

    @staticmethod
    def create_channel_entity(
        target: str,
        options: t.JsonMapping | None = None,
    ) -> p.Result[m.Grpc.Channel]:
        """Create a typed channel entity from validated inputs."""
        resolved_options = {} if options is None else dict(options)
        grpc_models = FlextGrpcUtilitiesGrpc._grpc_models()
        return r[grpc_models.Grpc.Channel].create_from_callable(
            lambda: grpc_models.Grpc.Channel(
                target=target,
                options=resolved_options,
            ),
        )

    @staticmethod
    def create_client_entity(
        target: str,
        options: t.JsonMapping | None = None,
    ) -> p.Result[m.Grpc.Client]:
        """Create a typed client entity backed by a typed channel entity."""
        resolved_options = {} if options is None else dict(options)
        channel_result = FlextGrpcUtilitiesGrpc.create_channel_entity(
            target=target,
            options=resolved_options,
        )
        grpc_models = FlextGrpcUtilitiesGrpc._grpc_models()
        if channel_result.failure:
            return r[grpc_models.Grpc.Client].fail(
                channel_result.error or "Client channel creation failed",
            )
        return r[grpc_models.Grpc.Client].create_from_callable(
            lambda: grpc_models.Grpc.Client(
                channel=channel_result.value,
                options=resolved_options,
            ),
        )

    @staticmethod
    def create_server_entity(
        host: str = c.Grpc.NETWORK_DEFAULT_HOST,
        port: int = c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.SERVICE_DEFAULT_MAX_WORKERS,
    ) -> p.Result[m.Grpc.Server]:
        """Create a typed server entity from validated inputs."""
        grpc_models = FlextGrpcUtilitiesGrpc._grpc_models()
        return r[grpc_models.Grpc.Server].create_from_callable(
            lambda: grpc_models.Grpc.Server(
                host=host,
                port=port,
                max_workers=max_workers,
            ),
        )

    @staticmethod
    def create_service_entity(
        name: str,
        methods: t.StrSequence | None = None,
    ) -> p.Result[m.Grpc.Service]:
        """Create a typed service entity with a minimal valid method set."""
        resolved_methods = ["HealthCheck"] if methods is None else list(methods)
        grpc_models = FlextGrpcUtilitiesGrpc._grpc_models()
        return r[grpc_models.Grpc.Service].create_from_callable(
            lambda: grpc_models.Grpc.Service(
                name=name,
                methods=resolved_methods,
            ),
        )

    @staticmethod
    def create_stream_entity(
        method_name: str,
        stream_type: c.Grpc.GrpcOperations | str,
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create a typed stream entity from validated inputs."""
        resolved_stream_type = c.Grpc.GrpcOperations(stream_type)
        grpc_models = FlextGrpcUtilitiesGrpc._grpc_models()
        return r[grpc_models.Grpc.GrpcStream].create_from_callable(
            lambda: grpc_models.Grpc.GrpcStream(
                id=str(uuid4()),
                method_name=method_name,
                stream_type=resolved_stream_type,
            ),
        )

    @staticmethod
    def parse_address(address: str) -> tuple[str, int]:
        """Parse a validated gRPC address into host and port."""
        return FlextGrpcUtilitiesGrpc.parse_target(address)

    @staticmethod
    def parse_target(target: str) -> tuple[str, int]:
        """Parse a validated gRPC target into (host, port)."""
        if not FlextGrpcUtilitiesGrpc.validate_target(target):
            msg = f"Invalid gRPC target: {target}"
            raise ValueError(msg)
        host, port_str = target.split(":", 1)
        return (host, int(port_str))

    @staticmethod
    def validate_target(target: str) -> bool:
        """Validate a gRPC target string in the form host:port."""
        if not target or ":" not in target:
            return False
        try:
            host, port_str = target.split(":", 1)
            if not host or not port_str:
                return False
            if not all(
                ch.isalnum() or ch in c.Grpc.NETWORK_HOST_ALLOWED_PUNCTUATION
                for ch in host
            ):
                return False
            port = int(port_str)
            max_port = 65535
            return 1 <= port <= max_port
        except (ValueError, AttributeError):
            logger.debug("Invalid gRPC target: %s", target)
            return False

    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate that a port is within the permitted gRPC range."""
        return c.Grpc.NETWORK_MIN_PORT <= port <= c.Grpc.NETWORK_MAX_PORT

    @staticmethod
    def validate_host(host: str) -> bool:
        """Validate that a host string is non-empty."""
        return bool(host and host.strip())

    @staticmethod
    def format_address(host: str, port: int) -> str:
        """Format a gRPC ``host:port`` address."""
        return f"{host}:{port}"

    @staticmethod
    def channel_state_name(state: str) -> str:
        """Return a normalized channel state name."""
        normalized = state.lower()
        if normalized in c.Grpc.CHANNEL_STATES:
            return normalized
        return "unknown"

    @staticmethod
    def server_state_name(state: str) -> str:
        """Return a normalized server state name."""
        normalized = state.lower()
        if normalized in c.Grpc.SERVER_STATES:
            return normalized
        return "unknown"

    @staticmethod
    def system_info() -> dict[str, t.JsonValue]:
        """Return gRPC utility system info."""
        channel_states: list[t.JsonValue] = list(c.Grpc.CHANNEL_STATES)
        server_states: list[t.JsonValue] = list(c.Grpc.SERVER_STATES)
        info: dict[str, t.JsonValue] = {
            "default_host": c.Grpc.NETWORK_DEFAULT_HOST,
            "default_port": c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
            "min_port": c.Grpc.NETWORK_MIN_PORT,
            "max_port": c.Grpc.NETWORK_MAX_PORT,
            "channel_states": channel_states,
            "server_states": server_states,
        }
        return info


__all__: list[str] = ["FlextGrpcUtilitiesGrpc"]
