# flext-grpc Troubleshooting

<!-- TOC START -->
- [Table of Contents](#table-of-contents)
- [Fixed Issues](#fixed-issues)
  - [Protobuf Import Compatibility (RESOLVED)](#protobuf-import-compatibility-resolved)
- [Current Issues](#current-issues)
  - [Test Execution Investigation Required](#test-execution-investigation-required)
- [Common Development Issues](#common-development-issues)
  - [Import Path Problems](#import-path-problems)
  - [gRPC Version Conflicts](#grpc-version-conflicts)
  - [Server Startup Issues](#server-startup-issues)
- [Development Best Practices](#development-best-practices)
  - [gRPC Service Development](#grpc-service-development)
  - [Performance Considerations](#performance-considerations)
  - [Security Patterns](#security-patterns)
- [Diagnostic Commands](#diagnostic-commands)
  - [Check Installation](#check-installation)
  - [Verify Dependencies](#verify-dependencies)
  - [Test Core Functionality](#test-core-functionality)
- [Getting Help](#getting-help)
- [Future Improvements](#future-improvements)
<!-- TOC END -->

## Table of Contents

- [flext-grpc Troubleshooting](#flext-grpc-troubleshooting)
  - [Fixed Issues](#fixed-issues)
    - [Protobuf Import Compatibility (RESOLVED)](#protobuf-import-compatibility-resolved)
- [or](#or)
- [1. Regenerate protobuf files](#1-regenerate-protobuf-files)
- [2. Fix import paths in generated files](#2-fix-import-paths-in-generated-files)
- [Changed: import flext_grpc_pb2 as flext**grpc**pb2](#changed-import-flext_grpc_pb2-as-flext__grpc__pb2)
- [To: from . import flext_grpc_pb2 as flext**grpc**pb2](#to-from--import-flext_grpc_pb2-as-flext__grpc__pb2)
  - [Current Issues](#current-issues)
    - [Test Execution Investigation Required](#test-execution-investigation-required)
- [Check test discovery](#check-test-discovery)
- [Run specific test modules](#run-specific-test-modules)
- [Full test execution](#full-test-execution)
  - [Common Development Issues](#common-development-issues)
    - [Import Path Problems](#import-path-problems)
- [or use poetry run for installed package](#or-use-poetry-run-for-installed-package)
  - [gRPC Version Conflicts](#grpc-version-conflicts)
  - [Server Startup Issues](#server-startup-issues)
- [Check server state](#check-server-state)
- [Attempt startup with error handling](#attempt-startup-with-error-handling)
  - [Development Best Practices](#development-best-practices)
    - [gRPC Service Development](#grpc-service-development)
    - [Performance Considerations](#performance-considerations)
    - [Security Patterns](#security-patterns)
  - [Diagnostic Commands](#diagnostic-commands)
    - [Check Installation](#check-installation)
    - [Verify Dependencies](#verify-dependencies)
    - [Test Core Functionality](#test-core-functionality)
  - [Getting Help](#getting-help)
  - [Future Improvements](#future-improvements)

**Version**: 0.12.0-dev | **Updated**: April 14, 2026

Common issues and solutions for flext-grpc development and deployment.

## Fixed Issues

### Protobuf Import Compatibility (RESOLVED)

**Issue**: Import failures due to protobuf generated code compatibility.

**Error Messages**:

```yaml
ModuleNotFoundError: No module named 'flext_grpc_pb2'
# or
The grpc package installed is at version X.X.X, but the generated code depends on grpcio>=Y.Y.Y
```

**Root Cause**: Generated protobuf files using incorrect import paths or version mismatches.

**Solution Applied**:

```bash
# 1. Regenerate protobuf files
cd src/flext_grpc/proto
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. flext_grpc.proto

# 2. Fix import paths in generated files
# Changed: import flext_grpc_pb2 as flext__grpc__pb2
# To: from . import flext_grpc_pb2 as flext__grpc__pb2
```

**Verification**:

```bash
python -c "from flext_grpc import FlextGrpcPlatform; print('Import successful')"
```

## Current Issues

### Test Execution Investigation Required

**Issue**: Test suite execution needs validation.

**Current Status**: Test structure exists but execution reliability needs verification.

**Investigation Steps**:

```bash
# Check test discovery
poetry run pytest --collect-only

# Run specific test modules
poetry run pytest tests/unit/test_config.py -v

# Full test execution
poetry run pytest tests/ -v
```

**Expected Resolution**: Validate test execution and fix any remaining issues.

## Common Development Issues

### Import Path Problems

**Symptom**: Module not found errors when importing flext-grpc components.

**Solution**: Ensure correct Python path setup:

```python
import sys

sys.path.insert(0, "src")  # For development
# or use poetry run for installed package
```

### gRPC Version Conflicts

**Symptom**: Version mismatch warnings or errors.

**Solution**: Use Poetry for consistent dependency management:

```bash
poetry install --all-extras
poetry show grpcio grpcio-tools protobuf  # Check versions
```

### Server Startup Issues

**Symptom**: Server creation succeeds but startup fails.

**Debugging**:

```python
from flext_grpc import create_server, FlextGrpcPlatform

server = create_server("localhost", 50051, 10)
platform = FlextGrpcPlatform()

# Check server state
print(f"Server state: {server.state}")

# Attempt startup with error handling
start_result = platform.start_server(server)
if start_result.failure:
    print(f"Startup failed: {start_result.error}")
```

## Development Best Practices

### gRPC Service Development

1. **Always use r patterns**:

   ```python
   def my_grpc_method() -> p.Result[ResponseType]:
       # Explicit error handling, no exceptions
   ```

2. **Validate inputs using Pydantic models**:

   ```python
   from flext_grpc import FlextGrpcSettings

   settings = FlextGrpcSettings(host="localhost", port=50051, max_workers=10)
   ```

3. **Use platform for complex operations**:

   ```python
   from flext_grpc import FlextGrpcPlatform

   platform = FlextGrpcPlatform()
   # Use platform methods for lifecycle management
   ```

### Performance Considerations

Based on 2025 gRPC Python best practices:

1. **Reuse channels and stubs** to avoid connection overhead
2. **Use keepalive pings** for long-lived connections
3. \*_Consider_ for improved streaming performance
4. **Validate inputs** even with protobuf type checking

### Security Patterns

1. **Authentication**: Implement interceptors following gRPC security patterns
2. **TLS Configuration**: Use secure channels for production deployment
3. **Input Validation**: Always validate business logic beyond protobuf types

## Diagnostic Commands

### Check Installation

```bash
poetry show flext-grpc
poetry run python -c "import flext_grpc; print('Installation OK')"
```

### Verify Dependencies

```bash
poetry run python -c "
import grpc
import google.protobuf
print(f'gRPC: {grpc.__version__}')
print(f'Protobuf: {google.protobuf.__version__}')
"
```

### Test Core Functionality

```bash
poetry run python -c "
from flext_grpc import create_server, FlextGrpcPlatform
server = create_server('localhost', 50051, 10)
platform = FlextGrpcPlatform()
print(f'Server: {server.address}')
print(f'Platform: {platform is not None}')
print('Core functionality verified')
"
```

## Getting Help

1. **Check this troubleshooting guide** for common issues
2. **Review logs** using FlextLogger output for detailed error information
3. **Validate configuration** using provided diagnostic commands
4. **Test minimal examples** to isolate issues

## Future Improvements

Planned enhancements to reduce troubleshooting needs:

1. **Comprehensive test validation** - Ensure all test execution scenarios work
2. **Better error messages** - More descriptive failure information
3. **Configuration validation** - Early detection of setup issues
4. **Development utilities** - Debugging and diagnostic tools

---

For development workflow and architectural guidance,
see [Development](development.md) and [Architecture](architecture.md) documentation.
