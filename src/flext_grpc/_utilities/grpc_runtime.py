"""Internal gRPC runtime-bound utility mixin with a typed adapter boundary.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import grpc

from flext_core import r, u
from flext_grpc import c, p

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Executor
    from types import ModuleType


class FlextGrpcUtilitiesGrpcRuntime:
    """gRPC runtime-bound utilities isolated behind a typed adapter."""

    _logger = u.fetch_logger(__name__)

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
        def _exception_type(value: type[BaseException], name: str) -> type[Exception]:
            """Validate that the runtime exposes an Exception subtype.

            Returns:
                The resulting ``type[Exception]``.

            Raises:
                TypeError: If grpc.
            """
            if issubclass(value, Exception):
                return value
            msg = f"grpc.{name} is not an Exception subtype"
            raise TypeError(msg)

        def insecure_channel(self, target: str) -> p.Grpc.GrpcChannel:
            """Create a typed insecure channel from the runtime module.

            Returns:
                The resulting ``p.Grpc.GrpcChannel``.

            Raises:
                TypeError: If grpc.insecure_channel returned an invalid channel.
            """
            channel = self._runtime_module.insecure_channel(target)
            if not isinstance(channel, p.Grpc.GrpcChannel):
                msg = "grpc.insecure_channel returned an invalid channel"
                raise TypeError(msg)
            return channel

        def channel_ready_future(
            self,
            channel: p.Grpc.GrpcChannel,
        ) -> p.Grpc.GrpcReadyFuture:
            """Create a typed ready future for the given channel.

            Returns:
                The resulting ``p.Grpc.GrpcReadyFuture``.

            Raises:
                TypeError: If grpc.channel_ready_future returned an invalid future.
            """
            ready_future = self._runtime_module.channel_ready_future(channel)
            if not isinstance(ready_future, p.Grpc.GrpcReadyFuture):
                msg = "grpc.channel_ready_future returned an invalid future"
                raise TypeError(msg)
            return ready_future

        def server(self, thread_pool: Executor) -> p.Grpc.GrpcServer:
            """Create a typed gRPC server from the runtime module.

            Returns:
                The resulting ``p.Grpc.GrpcServer``.

            Raises:
                TypeError: If grpc.server returned an invalid server.
            """
            grpc_server = self._runtime_module.server(thread_pool)
            if not isinstance(grpc_server, p.Grpc.GrpcServer):
                msg = "grpc.server returned an invalid server"
                raise TypeError(msg)
            return grpc_server

    @staticmethod
    def resolve_runtime() -> p.Result[p.Grpc.GrpcRuntime]:
        """Load the grpc runtime through the typed adapter boundary.

        Returns:
            The resulting ``p.Result[p.Grpc.GrpcRuntime]``.
        """
        runtime_result = u.try_(
            lambda: grpc,
            catch=(ImportError, ModuleNotFoundError),
        )
        if runtime_result.failure:
            return r[p.Grpc.GrpcRuntime].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        return r[p.Grpc.GrpcRuntime].ok(
            FlextGrpcUtilitiesGrpcRuntime._GrpcRuntimeAdapter(runtime_result.value),
        )

    @staticmethod
    def runtime_error_message(exception: BaseException | None) -> str:
        """Normalize a runtime exception into a stable public message.

        Returns:
            The resulting ``str``.
        """
        if exception is None:
            return "Unknown gRPC error"
        if isinstance(exception, p.Grpc.GrpcCallFailure):
            code_value = exception.code()
            details_value: str = exception.details()
            if code_value is None:
                return details_value
            return f"{code_value} - {details_value}"
        return str(exception)

    @staticmethod
    def runtime_failure_message[TValue](result: p.Result[TValue]) -> str:
        """Return the most useful error message from a grpc runtime result."""
        if result.exception is not None:
            return FlextGrpcUtilitiesGrpcRuntime.runtime_error_message(result.exception)
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
        """Execute a runtime operation using the canonical grpc exception set.

        Returns:
            The resulting ``p.Result[TValue]``.
        """
        runtime_result = FlextGrpcUtilitiesGrpcRuntime.resolve_runtime()
        if runtime_result.failure:
            return r[TValue].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        runtime = runtime_result.value
        return u.try_(
            operation,
            catch=FlextGrpcUtilitiesGrpcRuntime._runtime_exception_types(runtime),
        )

    @staticmethod
    def run_runtime(operation: Callable[[], None]) -> p.Result[bool]:
        """Execute a side-effecting runtime operation.

        Returns:
            The resulting ``p.Result[bool]``.
        """

        def _run() -> bool:
            operation()
            return True

        return FlextGrpcUtilitiesGrpcRuntime.call_runtime(_run)

    @staticmethod
    def open_insecure_channel(
        target: str,
        *,
        timeout: float = c.Grpc.NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT,
    ) -> p.Result[p.Grpc.GrpcChannel]:
        """Open an insecure channel and wait until it is ready.

        Returns:
            The resulting ``p.Result[p.Grpc.GrpcChannel]``.
        """
        runtime_result = FlextGrpcUtilitiesGrpcRuntime.resolve_runtime()
        if runtime_result.failure:
            return r[p.Grpc.GrpcChannel].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        runtime = runtime_result.value

        def _open() -> p.Grpc.GrpcChannel:
            grpc_channel = runtime.insecure_channel(target)
            ready = False
            try:
                future = runtime.channel_ready_future(grpc_channel)
                try:
                    future.result(timeout=timeout)
                finally:
                    future.cancel()
                ready = True
            finally:
                if not ready:
                    grpc_channel.close()
            return grpc_channel

        return u.try_(
            _open,
            catch=FlextGrpcUtilitiesGrpcRuntime._runtime_exception_types(runtime),
        )

    @staticmethod
    def create_runtime_server(thread_pool: Executor) -> p.Result[p.Grpc.GrpcServer]:
        """Create a runtime grpc server using the canonical adapter.

        Returns:
            The resulting ``p.Result[p.Grpc.GrpcServer]``.
        """
        runtime_result = FlextGrpcUtilitiesGrpcRuntime.resolve_runtime()
        if runtime_result.failure:
            return r[p.Grpc.GrpcServer].fail(
                runtime_result.error or "gRPC runtime unavailable",
                exception=runtime_result.exception,
            )
        runtime = runtime_result.value
        return u.try_(
            lambda: runtime.server(thread_pool),
            catch=FlextGrpcUtilitiesGrpcRuntime._runtime_exception_types(runtime),
        )

    @staticmethod
    def bind_insecure_port(server: p.Grpc.GrpcServer, address: str) -> p.Result[int]:
        """Bind an address to a runtime grpc server.

        Returns:
            The resulting ``p.Result[int]``.
        """
        return FlextGrpcUtilitiesGrpcRuntime.call_runtime(
            lambda: server.add_insecure_port(address),
        )


__all__: list[str] = ["FlextGrpcUtilitiesGrpcRuntime"]
