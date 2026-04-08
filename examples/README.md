# FLEXT gRPC Examples

<!-- TOC START -->

- [Example Structure](#example-structure)
  - [Available Examples](#available-examples)
  - [Example Categories](#example-categories)
- [Basic Usage Examples](#basic-usage-examples)
  - [Server Lifecycle Management](#server-lifecycle-management)
  - [Client Connection Management](#client-connection-management)
- [Advanced Usage Examples](#advanced-usage-examples)
  - [Streaming Operations](#streaming-operations)
  - [Platform Integration](#platform-integration)
- [Error Handling Examples](#error-handling-examples)
  - [Comprehensive Error Patterns](#comprehensive-error-patterns)
  - [Recovery Strategies](#recovery-strategies)
- [Integration Examples](#integration-examples)
  - [FLEXT Ecosystem Integration](#flext-ecosystem-integration)
  - [Configuration Management](#configuration-management)
- [Running Examples](#running-examples)
  - [Development Environment](#development-environment)
  - [Execution Commands](#execution-commands)
- [Example Patterns](#example-patterns)
  - [Entity Creation Pattern](#entity-creation-pattern)
  - [Service Operation Pattern](#service-operation-pattern)
  - [Platform Usage Pattern](#platform-usage-pattern)
- [Current Status and Limitations](#current-status-and-limitations)
  - [Development Status (Honest Assessment)](#development-status-honest-assessment)
  - [What Examples Actually Demonstrate](#what-examples-actually-demonstrate)
  - [Planned Enhancements (Realistic Timeline)](#planned-enhancements-realistic-timeline)
- [Contributing Examples](#contributing-examples)
  - [Adding New Examples](#adding-new-examples)
  - [Example Quality Standards](#example-quality-standards)
  - [Example Template](#example-template)

<!-- TOC END -->

Practical examples demonstrating FLEXT gRPC usage patterns and integration scenarios for enterprise development.

## Example Structure

### Available Examples

```
examples/
├── 01_basic_usage.py           # Core functionality and entity usage
├── 02_advanced_usage.py        # Complex scenarios with streaming
├── 03_error_handling_patterns.py # Comprehensive error handling
└── README.md                   # This documentation
```

### Example Categories

- **Basic Usage**: Fundamental operations and entity management
- **Advanced Scenarios**: Complex workflows and streaming operations
- **Error Handling**: Comprehensive error handling patterns
- **Integration Patterns**: FLEXT ecosystem integration examples

## Basic Usage Examples

### Server Lifecycle Management

**File**: `basic_usage.py`\
**Purpose**: Demonstrates fundamental server entity creation, validation, and lifecycle management

**Key Concepts**:

- FlextGrpcServer entity creation and validation
- Domain rule validation patterns
- State transition management
- r pattern usage

**Usage**:

```bash
# Run basic usage example
poetry run python examples/basic_usage.py

# Run with debug output
FLEXT_LOG_LEVEL=debug poetry run python examples/basic_usage.py
```

### Client Connection Management

**File**: `basic_usage.py`\
**Purpose**: Shows client entity creation, channel management, and connection patterns

**Key Concepts**:

- FlextGrpcClient entity lifecycle
- FlextGrpcChannel state management
- Connection establishment and teardown
- SSL/TLS configuration examples

## Advanced Usage Examples

### Streaming Operations

**File**: `advanced_usage.py`\
**Purpose**: Demonstrates gRPC streaming patterns and advanced communication scenarios

**Key Concepts**:

- FlextGrpcStream entity usage
- Bidirectional streaming patterns
- Stream state management
- Performance optimization techniques

**Usage**:

```bash
# Run advanced usage example
poetry run python examples/advanced_usage.py

# Run with performance monitoring
FLEXT_GRPC_MONITOR=true poetry run python examples/advanced_usage.py
```

### Platform Integration

**File**: `advanced_usage.py`\
**Purpose**: Shows integration with FlextGrpcPlatform for unified operations

**Key Concepts**:

- FlextGrpcPlatform usage patterns
- Service registration and discovery
- Dependency injection integration
- Cross-service communication

## Error Handling Examples

### Comprehensive Error Patterns

**File**: `03_error_handling_patterns.py`\
**Purpose**: Demonstrates enterprise-grade error handling using r patterns

**Key Concepts**:

- r success/failure handling
- Domain validation error management
- Error propagation patterns
- Logging and monitoring integration

**Usage**:

```bash
# Run error handling examples
poetry run python examples/03_error_handling_patterns.py

# Run with error tracing
FLEXT_TRACE_ERRORS=true poetry run python examples/03_error_handling_patterns.py
```

### Recovery Strategies

**File**: `03_error_handling_patterns.py`\
**Purpose**: Shows error recovery and resilience patterns

**Key Concepts**:

- Connection retry mechanisms
- Circuit breaker patterns
- Graceful degradation strategies
- Health check integration

## Integration Examples

### FLEXT Ecosystem Integration

**Purpose**: Demonstrates integration with other FLEXT ecosystem components

**Key Integration Points**:

- FlexCore (Go) service communication (port ${FlextConstants.DEFAULT_HTTP_PORT})
- FLEXT Service (Go/Python) integration (port 8081)
- flext-core foundation pattern usage
- flext-observability monitoring integration

**Example Usage**:

```python
from flext_grpc import FlextGrpcPlatform, FlextGrpcClient
from flext_core import get_flext_container
from datetime import datetime, timezone

# Integration with FLEXT ecosystem
container = FlextContainer.get_global()
platform = FlextGrpcPlatform(container=container)

# Client for FlexCore service
flexcore_client = FlextGrpcClient(
    id="flexcore-client",
    host=FlextConstants["Platform.DEFAULT_HOST"],
    port=FlextConstants["Platform.DEFAULT_HTTP_PORT"],  # FlexCore gRPC port
    created_at=datetime.now(timezone.utc),
)

# Service operations (when Protocol Buffers are implemented)
# result = platform.service.execute("connect", flexcore_client)
```

### Configuration Management

**Purpose**: Shows enterprise configuration patterns and environment management

**Key Concepts**:

- FlextGrpcSettings usage patterns
- Environment variable configuration
- Development vs production settings
- Security configuration management

**Example Usage**:

```python
from flext_grpc import FlextGrpcSettings

# Production configuration
prod_config = FlextGrpcSettings(
    host=FlextConstants["Platform.PRODUCTION_HOST"],
    port=FlextGrpcConstants.Network.DEFAULT_PORT,
    max_workers=20,
    timeout=FlextGrpcConstants.Service.DEFAULT_TIMEOUT,
    use_ssl=True,
    cert_file="/etc/ssl/certs/server.pem",
    key_file="/etc/ssl/private/server.key",
)

# Development configuration
dev_config = FlextGrpcSettings(
    host=FlextGrpcConstants.Network.DEFAULT_HOST,
    port=FlextGrpcConstants.Network.DEFAULT_PORT,
    max_workers=4,
    timeout=10.0,
    dev_mode=True,
)
```

## Running Examples

### Development Environment

**Prerequisites**:

- Poetry installed and configured
- Python 3.13+ environment
- FLEXT workspace properly set up

**Setup**:

```bash
# Install dependencies
make install-dev

# Set up development environment
make setup

# Verify installation
make diagnose
```

### Execution Commands

**Basic Examples**:

```bash
# Run all examples
for example in examples/*.py; do
    echo "Running $example"
    poetry run python "$example"
done

# Run specific example
poetry run python examples/basic_usage.py
```

**Debug Mode**:

```bash
# Run with comprehensive debugging
FLEXT_LOG_LEVEL=debug \
GRPC_VERBOSITY=debug \
GRPC_TRACE=all \
poetry run python examples/basic_usage.py
```

**Performance Monitoring**:

```bash
# Run with performance metrics
FLEXT_GRPC_MONITOR=true \
FLEXT_PERFORMANCE_METRICS=true \
poetry run python examples/advanced_usage.py
```

## Example Patterns

### Entity Creation Pattern

```python
from flext_grpc import FlextGrpcServer
from datetime import datetime, timezone

# Standard entity creation with validation
server = FlextGrpcServer(
    id="example-server",
    host=FlextGrpcConstants.Network.DEFAULT_HOST,
    port=FlextGrpcConstants.Network.DEFAULT_PORT,
    max_workers=10,
    created_at=datetime.now(timezone.utc),
)

# Always validate before use
validation = server.validate_business_rules()
if validation.is_failure:
    print(f"Validation failed: {validation.error}")
    exit(1)

print(f"Server created: {server.id}")
```

### Service Operation Pattern

```python
from flext_grpc import FlextGrpcServerService

# Service operations with r handling
service = FlextGrpcServerService()
result = service.execute("start", server)

if result.success:
    started_server = result.data
    print(f"Server started: {started_server.state}")
else:
    print(f"Start failed: {result.error}")
```

### Platform Usage Pattern

```python
from flext_grpc import FlextGrpcPlatform

# Platform operations for unified management
platform = FlextGrpcPlatform()

# High-level operations through platform
server_result = platform.service.execute("create_server", server)
if server_result.success:
    print(f"Platform operation successful")
```

## Current Status and Limitations

### Development Status (Honest Assessment)

**Currently Working Examples**:

- ✅ Entity creation and validation (basic_usage.py)
- ✅ Domain service operations and state management
- ✅ Error handling patterns with r
- ✅ Configuration management and validation
- ✅ Factory function usage (API functions)

**Current Implementation Gaps**:

- ❌ **Real gRPC Communication**: No actual network communication yet
- ❌ **Protocol Buffers**: No .proto files or generated code
- ❌ **Client-Server Interaction**: Examples only show entity creation
- ❌ **Streaming Operations**: Stream entities exist but no actual streaming
- ❌ **Network Communication**: No actual gRPC calls or responses

**Example Documentation Status**:

- ✅ **examples/README.md**: Updated with honest status assessment
- ⚠️ **examples/\*.py files**: Basic docstrings, need enterprise enhancement
- ⚠️ **Working Code**: Examples run but don't demonstrate real gRPC features

### What Examples Actually Demonstrate

**Current Working Functionality** (Real, not aspirational):

1. **Entity Creation**: FlextGrpcServer, FlextGrpcClient entities with validation
1. **Domain Validation**: Entity.validate_domain_rules() with r patterns
1. **State Management**: Entity state transitions (stopped → starting → running)
1. **Configuration**: FlextGrpcSettings with validation and defaults
1. **Error Handling**: r success/failure patterns
1. **API Functions**: create_server(), create_client() factory functions

**What Examples DON'T Demonstrate** (Missing functionality):

1. **Network Communication**: No actual socket connections or gRPC calls
1. **Protocol Buffers**: No .proto files, no generated stubs
1. **Streaming**: Stream entities exist but no actual data streaming
1. **Client-Server Communication**: No request/response examples
1. **Service Methods**: No actual gRPC service method implementations

### Planned Enhancements (Realistic Timeline)

**Documentation Enhancement** (Immediate - 1-2 days):

- Update all example .py files with enterprise-level docstrings
- Add comprehensive code comments and explanations
- Create working code examples that demonstrate existing functionality

**Implementation Enhancement** (Future - requires significant development):

- Protocol Buffer definition and code generation
- Actual gRPC server/client communication implementation
- Real streaming examples with data flow
- Integration with external gRPC services

For current development gaps and realistic timelines, see [../docs/TODO.md](../docs/TODO.md).

## Contributing Examples

### Adding New Examples

1. **Follow Naming Convention**: Use descriptive names with numbered prefixes
1. **Include Documentation**: Add comprehensive docstrings and comments
1. **Test Examples**: Ensure examples run without errors
1. **Update README**: Add new examples to this documentation

### Example Quality Standards

- **Professional Code**: Enterprise-grade code quality
- **Comprehensive Comments**: Clear explanations for complex concepts
- **Error Handling**: Proper r pattern usage
- **Performance Awareness**: Efficient resource usage
- **Security Conscious**: No hardcoded secrets or insecure patterns

### Example Template

```python
"""
Example: [Brief Description]

Purpose:
    [Detailed description of what this example demonstrates]

Key Concepts:
    - [Concept 1]: [Brief explanation]
    - [Concept 2]: [Brief explanation]

Usage:
    poetry run python examples/[filename].py

Author: FLEXT Development Team
Version: 0.9.9
"""

from flext_grpc import FlextGrpcPlatform, FlextGrpcServer, FlextGrpcSettings
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from datetime import datetime, timezone


def main() -> None:
    """Main example execution function."""
    print("Starting FLEXT gRPC example...")

    # Example implementation here

    print("Example completed successfully")


if __name__ == "__main__":
    main()
```
