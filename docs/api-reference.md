# flext-grpc API Reference

**Version**: 0.9.0 | **Updated**: September 17, 2025

Intended API reference for **flext-grpc** - gRPC communication library for the FLEXT ecosystem.

> **⚠️ Status**: API documentation describes intended functionality. Cannot verify due to protobuf import blocking issue.

## Core API

### Factory Functions

#### `create_server(host: str, port: int, max_workers: int) -> FlextGrpcServer`

Creates a gRPC server with the specified parameters.

```python
from flext_grpc import create_server

server = create_server("localhost", 50051, 10)
print(f"Server created: {server.host}:{server.port}")
```

#### `create_client(host: str, port: int) -> FlextGrpcClient`

Creates a gRPC client with the specified parameters.

```python
from flext_grpc import create_client

client = create_client("localhost", 50051)
```

#### `create_config(**kwargs) -> FlextResult[FlextGrpcConfig]`

Creates and validates a gRPC configuration.

```python
from flext_grpc import create_config

config_result = create_config(
    host="localhost",
    port=50051,
    max_workers=10
)
```

### Domain Entities

#### FlextGrpcServer

Server entity with lifecycle management and state transitions.

**Properties:**
- `host: str` - Server bind address
- `port: int` - Server port number
- `state: TGrpcServerState` - Current server state
- `max_workers: int` - Maximum worker threads

**Methods:**

##### `start() -> FlextResult[FlextGrpcServer]`

Starts the server (state transition: stopped → starting).

```python
server = FlextGrpcServer(host="localhost", port=50051)
start_result = server.start()

if start_result.success:
    starting_server = start_result.unwrap()
    assert starting_server.state == "starting"
```

##### `stop() -> FlextResult[FlextGrpcServer]`

Stops the server (state transition: running → stopping).

##### `validate_business_rules() -> FlextResult[None]`

Validates server configuration and business rules.

```python
server = FlextGrpcServer(host="", port=80)  # Invalid
validation = server.validate_business_rules()

if validation.is_failure:
    print(f"Validation failed: {validation.error}")
```

#### FlextGrpcClient

Client entity for gRPC communication.

**Properties:**
- `channel: FlextGrpcChannel` - Associated gRPC channel
- `state: TGrpcClientState` - Current connection state
- `timeout: float` - Request timeout in seconds

**Methods:**

##### `connect() -> FlextResult[FlextGrpcClient]`

Establishes connection to the server.

##### `disconnect() -> FlextResult[FlextGrpcClient]`

Closes connection to the server.

#### FlextGrpcConfig

Configuration value object with validation.

**Properties:**
- `host: str = "localhost"` - Server host address
- `port: int = 50051` - Server port number
- `max_workers: int = 10` - Maximum worker threads
- `timeout: float = 30.0` - Request timeout

**Methods:**

##### `validate() -> FlextResult[None]`

Validates configuration parameters.

```python
config = FlextGrpcConfig(host="localhost", port=99999)
validation = config.validate()

if validation.is_failure:
    print(f"Invalid config: {validation.error}")
```

### Service Classes

#### FlextGrpcPlatform

Unified facade for all gRPC operations.

**Methods:**

##### `start_server(server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]`

Starts a gRPC server with complete lifecycle management.

```python
from flext_grpc import FlextGrpcPlatform, FlextGrpcServer

platform = FlextGrpcPlatform()
server = FlextGrpcServer(host="localhost", port=50051)

result = platform.start_server(server)
if result.success:
    running_server = result.unwrap()
```

##### `connect_client(client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]`

Establishes client connection with retry logic.

##### `call_service(client: FlextGrpcClient, method: str, request: dict) -> FlextResult[dict]`

Makes a service call through the client.

#### FlextGrpcServerService

Domain service for server operations.

**Methods:**

##### `execute(operation: str, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]`

Executes server operations using Command pattern.

```python
from flext_grpc import FlextGrpcServerService

service = FlextGrpcServerService()
server = FlextGrpcServer(host="localhost", port=50051)

# Start server
result = service.execute("start", server)
if result.success:
    started_server = result.unwrap()
```

### Type Definitions

#### TGrpcServerState

Server state type definition.

```python
TGrpcServerState = Literal["stopped", "starting", "running", "stopping"]
```

#### TGrpcClientState

Client state type definition.

```python
TGrpcClientState = Literal["disconnected", "connecting", "connected", "disconnecting"]
```

#### TGrpcStreamType

Streaming pattern types.

```python
TGrpcStreamType = Literal["unary", "server_streaming", "client_streaming", "bidirectional"]
```

### Exception Hierarchy

#### FlextGrpcError

Base exception for all gRPC-related errors.

```python
class FlextGrpcError(Exception):
    """Base gRPC error."""

    def __init__(self, message: str, error_code: str = "GRPC_ERROR"):
        super().__init__(message)
        self.error_code = error_code
```

#### FlextGrpcConfigurationError

Configuration-related errors.

```python
try:
    config = FlextGrpcConfig(port=-1)  # Invalid port
    config.validate().unwrap()
except FlextGrpcConfigurationError as e:
    print(f"Configuration error: {e}")
```

#### FlextGrpcConnectionError

Connection-related errors.

#### FlextGrpcTimeoutError

Timeout-related errors.

#### FlextGrpcValidationError

Validation-related errors.

## Streaming API

### FlextGrpcStream

Streaming operations for all gRPC patterns.

**Properties:**
- `stream_type: TGrpcStreamType` - Type of streaming pattern
- `method_name: str` - Associated service method
- `buffer_size: int` - Stream buffer size

**Methods:**

##### `send_data(data: dict) -> FlextResult[None]`

Sends data through the stream.

##### `receive_data() -> FlextResult[dict]`

Receives data from the stream.

##### `close() -> FlextResult[None]`

Closes the stream.

### FlextGrpcStreamService

Service for managing streaming operations.

**Methods:**

##### `create_server_stream(method: str, config: dict) -> FlextResult[FlextGrpcStream]`

Creates a server streaming operation.

##### `create_client_stream(method: str, config: dict) -> FlextResult[FlextGrpcStream]`

Creates a client streaming operation.

##### `create_bidirectional_stream(method: str, config: dict) -> FlextResult[FlextGrpcStream]`

Creates a bidirectional streaming operation.

## Utility Functions

### Address Parsing

#### `parse_address(address: str) -> FlextResult[tuple[str, int]]`

Parses a gRPC address string into host and port components.

```python
from flext_grpc import parse_address

result = parse_address("localhost:50051")
if result.success:
    host, port = result.unwrap()
    print(f"Host: {host}, Port: {port}")
```

#### `validate_address(address: str) -> FlextResult[None]`

Validates a gRPC address string.

```python
from flext_grpc import validate_address

validation = validate_address("invalid:port")
if validation.is_failure:
    print(f"Invalid address: {validation.error}")
```

## Integration with FLEXT Patterns

### Railway-Oriented Programming

All fallible operations return `FlextResult[T]` for composable error handling:

```python
from flext_grpc import create_config, create_server
from flext_core import FlextResult

def setup_grpc_server(host: str, port: int) -> FlextResult[str]:
    return (
        create_config(host=host, port=port)
        .flat_map(lambda config: create_server(config))
        .map(lambda server: f"Server ready: {server.host}:{server.port}")
    )

result = setup_grpc_server("localhost", 50051)
if result.success:
    print(result.unwrap())
```

### Dependency Injection

Integration with FlextContainer:

```python
from flext_core import FlextContainer
from flext_grpc import FlextGrpcPlatform

container = FlextContainer.get_global()
platform = container.get("grpc_platform")

if platform.success:
    grpc_platform = platform.unwrap()
```

## Protocol Buffer Integration

### Service Definitions

Current service definitions (blocked by version conflict):

```protobuf
service FlextGrpcService {
  rpc Echo(EchoRequest) returns (EchoResponse);
  rpc ServerStream(StreamRequest) returns (stream StreamResponse);
  rpc ClientStream(stream StreamRequest) returns (StreamResponse);
  rpc BidirectionalStream(stream StreamRequest) returns (stream StreamResponse);
  rpc HealthCheck(HealthRequest) returns (HealthResponse);
}
```

### Message Types

Standard message types for testing and health checking:

- `EchoRequest/EchoResponse` - Basic request/response testing
- `StreamRequest/StreamResponse` - Streaming operations
- `HealthRequest/HealthResponse` - Health checking

## Current Status

**Implementation**: Complete API surface (4,791 source lines)
**Documentation**: Docstrings and examples
**Testing**: Basic test structure in place
**Limitation**: Protobuf version conflict prevents actual usage

**Resolution Required**: Regenerate protocol buffer files to match runtime protobuf version (5.29.5).

---

This API reference describes the complete interface of flext-grpc once the protobuf compatibility issue is resolved.