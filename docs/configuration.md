# flext-grpc Configuration

<!-- TOC START -->

- [Runtime settings](#runtime-settings)
  - [Environment variables](#environment-variables)
- [Using settings with the public facade](#using-settings-with-the-public-facade)
- [TLS and advanced options](#tls-and-advanced-options)
- [Configuration files](#configuration-files)
- [Troubleshooting](#troubleshooting)

<!-- TOC END -->

`flext-grpc` exposes two distinct, typed configuration surfaces:

- `settings.Grpc` contains the environment-adjustable runtime values used for a gRPC
  endpoint: `host`, `port`, `max_workers`, and `timeout`.
- `config.Grpc` exposes the package-owned business configuration loaded from
  `src/flext_grpc/config/grpc.yaml`. The YAML file is the writable source of truth for
  those values; `config` is its read-only runtime projection.

Import the pre-instantiated objects from the public package boundary. Access
package-owned fields through the `Grpc` namespace, not top-level attributes.

```python
from flext_grpc import config, settings

endpoint = settings.Grpc
print(endpoint.host, endpoint.port, endpoint.max_workers, endpoint.timeout)
print(config.Grpc.name, config.Grpc.version)
```

## Runtime settings

The `Grpc` settings model validates the following fields on input:

| Field         | Type    | Constraint      | Purpose                    |
| ------------- | ------- | --------------- | -------------------------- |
| `host`        | `str`   | String          | Server bind host           |
| `port`        | `int`   | 1 through 65535 | Server bind port           |
| `max_workers` | `int`   | At least 1      | Worker thread count        |
| `timeout`     | `float` | Greater than 0  | Request timeout in seconds |

Read current defaults from `settings.Grpc` or the model fields. The fields are declared
in `src/flext_grpc/_settings.py`; avoid duplicating their current values in application
code or tests.

Construct an independently validated settings value with Pydantic v2 when an application
needs an explicit override:

```python
from flext_grpc import FlextGrpcSettings, settings

configured = FlextGrpcSettings.model_validate(
    {"Grpc": {"host": settings.Grpc.host, "port": settings.Grpc.port}}
)
print(configured.Grpc.host, configured.Grpc.port)
```

For JSON input, use `FlextGrpcSettings.model_validate_json` with the same `Grpc` object
shape. Invalid values raise a Pydantic validation error at this boundary. Do not call
`settings.validate()`; that method is not part of the public settings contract.

### Environment variables

`FlextGrpcSettings` uses the `FLEXT_GRPC_` prefix and `__` to separate nested fields.
For example, `FLEXT_GRPC_GRPC__PORT` selects `Grpc.port` and `FLEXT_GRPC_GRPC__TIMEOUT`
selects `Grpc.timeout`. Set environment variables before the process imports
`flext_grpc`; the exported `settings` singleton is created on import. A new
`FlextGrpcSettings()` instance reads the current settings sources. Environment values
still pass the same model validation.

## Using settings with the public facade

The package facade accepts endpoint values, and returns a typed `Result`. The settings
model is not a server or client factory. Creating a server entity does not itself start
a network listener.

```python
from flext_grpc import grpc, settings

server_result = grpc.create_server(
    host=settings.Grpc.host,
    port=settings.Grpc.port,
    max_workers=settings.Grpc.max_workers,
)
if server_result.failure:
    raise RuntimeError(server_result.error)

server = server_result.value
print(server.host, server.port)
```

`grpc.create_client(target)` accepts a target address and also returns a typed `Result`.
Use `grpc.connect_client(target)` when a client connection is needed. The timeout field
belongs to settings and is not a keyword argument of either method. A failed connection
attempt cancels its readiness subscription and closes the runtime channel before
returning a failure result.

## TLS and advanced options

`FlextGrpcSettings.Grpc` has no TLS, keepalive, retry, metrics, logging, or message-size
fields. Do not pass those names to `FlextGrpcSettings`: with its declared
`extra="ignore"` policy, unsupported input could be silently dropped.

The public `m.Grpc.SecurityConfig` model represents TLS certificate paths and
authentication choices for consumers that explicitly implement those features. It does
not install credentials or enable TLS on a server by itself. Channel options are passed
through the public `grpc.create_channel(target, options)` boundary where applicable.
Validate transport behavior through the actual consumer before claiming TLS or option
propagation.

## Configuration files

The package-owned YAML at `src/flext_grpc/config/grpc.yaml` is loaded into
`config.Grpc`; it is separate from environment-adjustable `settings.Grpc`. There is no
`load_config_from_yaml` helper or arbitrary `grpc_config.yaml` schema in the public
package API. Applications accepting external JSON can parse it once with
`FlextGrpcSettings.model_validate_json`; applications accepting other formats must
convert them to the same model shape at their own input boundary.

## Troubleshooting

- For an invalid `port`, `max_workers`, or `timeout`, inspect the original Pydantic
  validation error and the corresponding `FLEXT_GRPC_GRPC__*` environment value.
- If an environment change appears ineffective, confirm it was present before the
  process imported the pre-instantiated `settings` object.
- If a TLS or other advanced keyword has no effect, check whether the field actually
  exists in `FlextGrpcSettings.Grpc`; use the relevant transport model and runtime
  consumer instead of adding an ignored setting.
