# Integrating flext-grpc

<!-- TOC START -->

- [Runtime verification](#runtime-verification)

<!-- TOC END -->

`FlextGrpc` is the public facade for gRPC entity construction, server lifecycle, client
connections, streams, metrics, and connection pools. Obtain the facade from
`flext_grpc`; avoid importing service implementation classes as application contracts.

```python
from flext_grpc import FlextGrpc, settings

grpc = FlextGrpc()
server_result = grpc.create_server(
    host=settings.Grpc.host,
    port=settings.Grpc.port,
    max_workers=settings.Grpc.max_workers,
)
if server_result.failure:
    raise RuntimeError(server_result.error)
server = server_result.value
```

The result above is a typed server entity. A real listener is established by
`start_server(server)`; callers must observe its result and eventually call
`stop_server(server)`. The implementation in
`src/flext_grpc/services/_entities/server_manager.py` owns the transport lifecycle. Do
not infer listener readiness from `create_server` alone.

For clients, `create_client(target=...)` constructs a typed `m.Grpc.Client`;
`connect_client(target)` performs a connection attempt and returns a result.
`validate_target(target)` checks the address form, and `parse_address(target)` returns a
typed host/port result. Consumers pass `m.Grpc` payloads and handle failures at the
application boundary.

For streams, `create_stream(method_name=..., stream_type=...)` returns an
`m.Grpc.GrpcStream`; `send_data` and `close_stream` act on that model. Use the exported
`c.Grpc.STREAM_TYPES` vocabulary when selecting a stream type. Business rules and
configurable values come from `config.Grpc` and `settings.Grpc`, not duplicated
constants in an integration layer.

## Runtime verification

Integration tests should create a real server and client through public operations,
exercise the transport, assert the returned results and payloads, and release the
listener. Use bounded timeouts. Avoid mocked containers, canned responses, and
private-method assertions; they do not prove the installed gRPC cycle. See
[Testing](../testing.md) for the canonical test route.

Run lifecycle and validation commands from the active workspace root:

```bash
make setup
make gen
make check
make test
make docs
```

The root Makefile and its `make help` output are the command authority for this branch.
A local green report must be reproduced at the integrated commit.
