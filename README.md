# FLEXT-GRPC

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-GRPC** provides a robust, type-safe foundation for building gRPC microservices within the FLEXT ecosystem. It abstracts the complexities of `grpcio` and `protobuf` while enforcing Clean Architecture patterns and Railway-Oriented Programming for reliable inter-service communication.

## 🚀 Key Features

- **gRPC Abstraction**: Simplified, type-safe wrappers for creating gRPC servers and clients.
- **Streaming Support**: Comprehensive support for all four gRPC streaming patterns: Unary, Server Streaming, Client Streaming, and Bidirectional Streaming.
- **Lifecycle Management**: Robust server startup/shutdown handling and client connection management.
- **Dependency Injection**: Seamless integration with `FlextContainer` for injecting services into gRPC handlers.
- **Railway-Oriented**: Operations return `FlextResult[T]`, ensuring consistent error handling across the network boundary.
- **Interceptor Support**: Built-in support for gRPC interceptors (middleware) for logging, authentication, and tracing.

## 📦 Installation

To install `flext-grpc`:

```bash
pip install flext-grpc
```

Or with Poetry:

```bash
poetry add flext-grpc
```

## 🛠️ Usage

### Creating a Server

Define and start a gRPC server with minimal boilerplate.

```python
from flext_grpc import create_server, FlextGrpcSettings

# 1. Configure Server
settings = FlextGrpcSettings(
    host="0.0.0.0",
    port=50051,
    max_workers=10
)

# 2. Start Server
server = create_server(settings)
server.start()
print(f"Server listening on {settings.host}:{settings.port}")

# 3. Wait for termination
server.wait_for_termination()
```

### Creating a Client

Connect to a gRPC service safely.

```python
from flext_grpc import create_client, FlextGrpcSettings

# 1. Configure Client
settings = FlextGrpcSettings(
    host="localhost",
    port=50051
)

# 2. Create Client Channel
client = create_client(settings)

# 3. Use the client (example with generated stub)
# stub = MyServiceStub(client.channel)
# response = stub.MyMethod(request)
```

### Implementing a Service

Implement your gRPC service logic using FLEXT patterns.

```python
from flext_core import FlextService, FlextResult as r
# from my_proto import my_service_pb2_grpc, my_service_pb2

class MyServiceHandler(FlextService):
    def handle_request(self, request, context) -> r[str]:
        # Business logic here
        return r[str].ok(f"Processed {request.id}")

# Register handler with server...
```

## 🏗️ Architecture

FLEXT-GRPC is design to keep your transport layer clean and separated from your business logic:

- **Platform Layer**: `FlextGrpcPlatform` manages the underlying gRPC runtime.
- **Service Layer**: Business logic resides in `FlextService` implementations, detached from `protobuf` generated code where possible.
- **Interceptors**: Cross-cutting concerns like auth and logging are handled via interceptors, keeping handlers focused.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on setting up your environment and submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
