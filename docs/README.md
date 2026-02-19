# FLEXT gRPC Documentation


<!-- TOC START -->
- [Table of Contents](#table-of-contents)
- [Documentation Structure](#documentation-structure)
  - [gRPC-Specific Documentation](#grpc-specific-documentation)
- [Current Status](#current-status)
- [Documentation Scope](#documentation-scope)
- [What This Documentation Does NOT Cover](#what-this-documentation-does-not-cover)
- [Contributing to Documentation](#contributing-to-documentation)
<!-- TOC END -->

## Table of Contents

- [FLEXT gRPC Documentation](#flext-grpc-documentation)
  - [Documentation Structure](#documentation-structure)
    - [gRPC-Specific Documentation](#grpc-specific-documentation)
  - [Current Status](#current-status)
  - [Documentation Scope](#documentation-scope)
  - [What This Documentation Does NOT Cover](#what-this-documentation-does-not-cover)
  - [Contributing to Documentation](#contributing-to-documentation)

**Version**: 0.9.9 RC | **Updated**: September 17, 2025

Technical documentation for **flext-grpc** gRPC library implementation.

## Documentation Structure

### gRPC-Specific Documentation

- **[Getting Started](getting-started.md)** - flext-grpc installation and setup
- **[Architecture](architecture.md)** - gRPC-specific architecture within FLEXT patterns
- **[API Reference](api-reference.md)** - flext-grpc API documentation
- **[Configuration](configuration.md)** - gRPC service configuration
- **[Development](development.md)** - gRPC service development workflow
- **[Integration](guides/integration.md)** - gRPC integration with FLEXT projects
- **[Troubleshooting](troubleshooting.md)** - gRPC-specific issues and solutions

## Current Status

- **Core Operations**: Server/client creation functional
- **Test Coverage**: 39% (needs improvement to reach 90% target)
- **Import System**: All modules importable after protobuf fixes
- **Code Statistics**: 4,923 source lines, 18,018 test lines

## Documentation Scope

This documentation covers **only** flext-grpc specific functionality:

1. **gRPC Service Implementation** - How to use flext-grpc APIs
2. **gRPC Configuration** - Service-specific settings
3. **gRPC Integration Patterns** - How flext-grpc connects to FLEXT ecosystem
4. **gRPC Development Workflow** - Development procedures specific to gRPC services

## What This Documentation Does NOT Cover

For general FLEXT concepts, refer to workspace documentation:

- **FLEXT-Core patterns** → See `flext-core` documentation
- **General Clean Architecture** → See workspace architecture documentation
- **FLEXT ecosystem overview** → See workspace documentation
- **General development standards** → See workspace development guidelines

## Contributing to Documentation

1. **Focus**: Only document flext-grpc specific functionality
2. **Accuracy**: Base all content on verified, tested capabilities
3. **Standards**: Follow [FLEXT documentation standards](../../docs/standards/documentation.md)
4. **No Duplication**: Reference workspace docs instead of duplicating general concepts

---

For current development status, see the main [README.md](../README.md).
