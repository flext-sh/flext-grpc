"""Generated FlextGrpcService RPC handlers (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_grpc import c, m, p, u

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from google.protobuf.message import Message


class FlextGrpcServiceHandlerImpl:
    """Serves the generated Echo and HealthCheck RPCs for one bound server."""

    def __init__(self, server_id: str) -> None:
        """Bind the handler to the ``host:port`` target its server listens on."""
        super().__init__()
        self._server_id = server_id

    def rpc_handlers(
        self,
    ) -> Mapping[
        c.Grpc.ServiceMethod,
        Callable[[Message, p.Grpc.GrpcServicerContext], Message],
    ]:
        """Map every generated service RPC to its handler.

        Returns:
            The handler of each ``c.Grpc.ServiceMethod``.
        """
        return MappingProxyType({
            c.Grpc.ServiceMethod.ECHO: self.echo,
            c.Grpc.ServiceMethod.HEALTH_CHECK: self.health_check,
        })

    def echo(
        self,
        request: Message,
        _context: p.Grpc.GrpcServicerContext,
    ) -> Message:
        """Echo the request message tagged with this server's bound target.

        Returns:
            The generated ``EchoResponse`` message.
        """
        echo_request = u.Grpc.decode_message(m.Grpc.EchoRequest, request).unwrap()
        return u.Grpc.encode_message(
            u.Grpc.method_descriptor(c.Grpc.ServiceMethod.ECHO).output_type,
            m.Grpc.EchoResponse(
                message=echo_request.message,
                server_id=self._server_id,
            ),
        ).unwrap()

    @staticmethod
    def health_check(
        request: Message,
        _context: p.Grpc.GrpcServicerContext,
    ) -> Message:
        """Report the serving status of the requested service.

        Returns:
            The generated ``HealthResponse`` message.
        """
        health_request = u.Grpc.decode_message(
            m.Grpc.HealthRequest,
            request,
        ).unwrap()
        return u.Grpc.encode_message(
            u.Grpc.method_descriptor(c.Grpc.ServiceMethod.HEALTH_CHECK).output_type,
            m.Grpc.HealthResponse(
                status=c.Grpc.ServingStatus.SERVING.value,
                message=health_request.service,
            ),
        ).unwrap()


__all__: list[str] = ["FlextGrpcServiceHandlerImpl"]
