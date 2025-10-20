# flext-grpc Configuration

## Table of Contents

- [flext-grpc Configuration](#flext-grpc-configuration)
  - [Configuration Overview](#configuration-overview)
    - [Basic Configuration](#basic-configuration)
- [Simple configuration](#simple-configuration)
  - [Environment Variables](#environment-variables)
- [Automatically loads from environment](#automatically-loads-from-environment)
  - [Configuration Parameters](#configuration-parameters)
    - [Server Configuration](#server-configuration)
      - [`host: str = FlextGrpcConstants.Network.DEFAULT_HOST`](#host-str--flextgrpcconstantsnetworkdefault_host)
- [Development](#development)
- [Production](#production) - [`port: int = FlextGrpcConstants.Network.DEFAULT_PORT`](#port-int--flextgrpcconstantsnetworkdefault_port)
- [Standard gRPC port](#standard-grpc-port)
- [Custom port](#custom-port) - [`max_workers: int = 10`](#max_workers-int--10)
- [Development (low concurrency)](#development-low-concurrency)
- [Production (high concurrency)](#production-high-concurrency)
  - [Client Configuration](#client-configuration)
    - [`timeout: float = FlextGrpcConstants.Service.DEFAULT_TIMEOUT`](#timeout-float--flextgrpcconstantsservicedefault_timeout)
- [Quick timeout](#quick-timeout)
- [Extended timeout](#extended-timeout)
  - [Advanced Configuration](#advanced-configuration)
    - [Connection Settings](#connection-settings)
    - [TLS Configuration](#tls-configuration)
  - [Configuration Validation](#configuration-validation)
    - [Built-in Validation](#built-in-validation)
    - [Business Rules](#business-rules)
    - [Custom Validation](#custom-validation)
  - [Environment-Specific Configurations](#environment-specific-configurations)
    - [Development Configuration](#development-configuration)
    - [Production Configuration](#production-configuration)
    - [Testing Configuration](#testing-configuration)
  - [Configuration from Files](#configuration-from-files)
    - [YAML Configuration](#yaml-configuration)
- [grpc_config.YAML](#grpc_configyaml)
  - [JSON Configuration](#json-configuration)
  - [Configuration Best Practices](#configuration-best-practices)
    - [Security](#security)
    - [Performance](#performance)
    - [Monitoring](#monitoring)
  - [Integration with FLEXT Patterns](#integration-with-flext-patterns)
    - [FlextResult Usage](#flextresult-usage)
    - [Container Integration](#container-integration)
- [Later retrieval](#later-retrieval)
  - [Troubleshooting Configuration](#troubleshooting-configuration)
    - [Common Issues](#common-issues)
- [Error: Port out of range](#error-port-out-of-range)
- [Error: File not found](#error-file-not-found)
- [Multiple ways to set the same value can conflict](#multiple-ways-to-set-the-same-value-can-conflict)
  - [Debugging Configuration](#debugging-configuration)

**Version**: 0.9.9 RC | **Updated**: September 17, 2025

Configuration management and settings for the flext-grpc library.

## Configuration Overview

flext-grpc provides flexible configuration through `FlextGrpcConfig` class with environment variable support and comprehensive validation.

### Basic Configuration

```python
from flext_grpc import FlextGrpcConfig

# Simple configuration
config = FlextGrpcConfig(
    host=FlextGrpcConstants.Network.DEFAULT_HOST,
    port=FlextGrpcConstants.Network.DEFAULT_PORT,
    max_workers=10
)
```

### Environment Variables

Configuration values can be set via environment variables with `GRPC_` prefix:

```bash
export GRPC_HOST="${FlextConstants.Platform.PRODUCTION_HOST}"
export GRPC_PORT="${FlextGrpcConstants.Network.DEFAULT_PORT}"
export GRPC_MAX_WORKERS="20"
export GRPC_TIMEOUT="${FlextGrpcConstants.Service.DEFAULT_TIMEOUT}"
```

```python
# Automatically loads from environment
config = FlextGrpcConfig()
```

## Configuration Parameters

### Server Configuration

#### `host: str = FlextGrpcConstants.Network.DEFAULT_HOST`

Server bind address. Common values:

- `FlextGrpcConstants.Network.DEFAULT_HOST` - Local development
- `FlextConstants.Platform.LOCALHOST_IP` - Local IPv4 only
- `FlextConstants.Platform.PRODUCTION_HOST` - All interfaces (production)

```python
# Development
config = FlextGrpcConfig(host=FlextGrpcConstants.Network.DEFAULT_HOST)

# Production
config = FlextGrpcConfig(host=FlextConstants.Platform.PRODUCTION_HOST)
```

#### `port: int = FlextGrpcConstants.Network.DEFAULT_PORT`

Server port number. Valid range: 1024-65535

```python
# Standard gRPC port
config = FlextGrpcConfig(port=FlextGrpcConstants.Network.DEFAULT_PORT)

# Custom port
config = FlextGrpcConfig(port=FlextConstants.Platform.DEFAULT_HTTP_PORT)
```

#### `max_workers: int = 10`

Maximum number of worker threads for request processing.

```python
# Development (low concurrency)
config = FlextGrpcConfig(max_workers=4)

# Production (high concurrency)
config = FlextGrpcConfig(max_workers=50)
```

### Client Configuration

#### `timeout: float = FlextGrpcConstants.Service.DEFAULT_TIMEOUT`

Request timeout in seconds.

```python
# Quick timeout
config = FlextGrpcConfig(timeout=5.0)

# Extended timeout
config = FlextGrpcConfig(timeout=120.0)
```

### Advanced Configuration

#### Connection Settings

```python
from flext_grpc import FlextGrpcConfig

config = FlextGrpcConfig(
    # Connection settings
    keepalive_time_ms=FlextConstants["Network.KEEPALIVE_TIME_MS"],      # 30 seconds
    keepalive_timeout_ms=FlextConstants["Network.KEEPALIVE_TIMEOUT_MS"],    # 5 seconds
    keepalive_permit_without_calls=True,

    # Message size limits
    max_receive_message_length=4*1024*1024,  # 4MB
    max_send_message_length=4*1024*1024,     # 4MB

    # Retry settings
    max_retry_attempts=3,
    retry_backoff_seconds=1.0
)
```

#### TLS Configuration

```python
config = FlextGrpcConfig(
    # TLS settings
    use_tls=True,
    tls_cert_file="/path/to/server.crt",
    tls_key_file="/path/to/server.key",
    tls_ca_file="/path/to/ca.crt"
)
```

## Configuration Validation

### Built-in Validation

All configuration is validated on creation:

```python
from flext_grpc import FlextGrpcConfig
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities

config = FlextGrpcConfig(host="", port=99999)  # Invalid
validation = config.validate()

if validation.is_failure:
    print(f"Configuration error: {validation.error}")
```

### Business Rules

Configuration validation enforces these rules:

- Host cannot be empty
- Port must be in range 1024-65535
- Max workers must be >= 1
- Timeout must be > 0
- File paths must exist (for TLS)

### Custom Validation

```python
from flext_grpc import FlextGrpcConfig
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities

def validate_production_config(config: FlextGrpcConfig) -> FlextResult[None]:
    """Additional validation for production environments."""

    if config.host == FlextGrpcConstants.Network.DEFAULT_HOST:
        return FlextResult.fail("Production servers cannot use localhost")

    if config.max_workers < 10:
        return FlextResult.fail("Production requires minimum 10 workers")

    if not config.use_tls:
        return FlextResult.fail("Production requires TLS encryption")

    return FlextResult.ok(None)
```

## Environment-Specific Configurations

### Development Configuration

```python
from flext_grpc import FlextGrpcConfig

def create_dev_config() -> FlextGrpcConfig:
    return FlextGrpcConfig(
        host=FlextGrpcConstants.Network.DEFAULT_HOST,
        port=FlextGrpcConstants.Network.DEFAULT_PORT,
        max_workers=4,
        timeout=10.0,
        use_tls=False,  # Simplified for development
        log_level="DEBUG"
    )
```

### Production Configuration

```python
def create_prod_config() -> FlextGrpcConfig:
    return FlextGrpcConfig(
        host=FlextConstants["Platform.PRODUCTION_HOST"],
        port=FlextGrpcConstants.Network.DEFAULT_PORT,
        max_workers=50,
        timeout=FlextGrpcConstants.Service.DEFAULT_TIMEOUT,

        # Security settings
        use_tls=True,
        tls_cert_file="/etc/ssl/server.crt",
        tls_key_file="/etc/ssl/server.key",

        # Performance settings
        keepalive_time_ms=FlextConstants["Network.KEEPALIVE_TIME_MS"],
        max_receive_message_length=16*1024*1024,  # 16MB

        # Monitoring
        enable_health_checking=True,
        enable_metrics=True,
        log_level="INFO"
    )
```

### Testing Configuration

```python
def create_test_config() -> FlextGrpcConfig:
    return FlextGrpcConfig(
        host=FlextGrpcConstants.Network.DEFAULT_HOST,
        port=0,  # Use any available port
        max_workers=2,
        timeout=5.0,
        use_tls=False,
        log_level="ERROR"  # Minimal logging in tests
    )
```

## Configuration from Files

### YAML Configuration

```yaml
# grpc_config.yaml
grpc:
  host: "${FlextConstants.Platform.PRODUCTION_HOST}"
  port: ${FlextGrpcConstants.Network.DEFAULT_PORT}
  max_workers: 20
  timeout: ${FlextGrpcConstants.Service.DEFAULT_TIMEOUT}

  tls:
    enabled: true
    cert_file: "/etc/ssl/server.crt"
    key_file: "/etc/ssl/server.key"

  performance:
    keepalive_time_ms: ${FlextConstants.Network.KEEPALIVE_TIME_MS}
    max_message_size: 4194304 # 4MB
```

```python
import yaml
from flext_grpc import FlextGrpcConfig

def load_config_from_yaml(file_path: str) -> FlextGrpcConfig:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    grpc_config = data['grpc']

    return FlextGrpcConfig(
        host=grpc_config['host'],
        port=grpc_config['port'],
        max_workers=grpc_config['max_workers'],
        timeout=grpc_config['timeout'],

        use_tls=grpc_config['tls']['enabled'],
        tls_cert_file=grpc_config['tls']['cert_file'],
        tls_key_file=grpc_config['tls']['key_file']
    )
```

### JSON Configuration

```json
{
  "grpc": {
    "host": "${FlextGrpcConstants.Network.DEFAULT_HOST}",
    "port": ${FlextGrpcConstants.Network.DEFAULT_PORT},
    "max_workers": 10,
    "timeout": ${FlextGrpcConstants.Service.DEFAULT_TIMEOUT},
    "use_tls": false
  }
}
```

## Configuration Best Practices

### Security

1. **Use TLS in Production**

   ```python
   # Always enable TLS for production
   config = FlextGrpcConfig(
       use_tls=True,
       tls_cert_file="/secure/path/server.crt",
       tls_key_file="/secure/path/server.key"
   )
   ```

2. **Secure File Permissions**

   ```bash
   # Protect certificate files
   chmod 600 /etc/ssl/private/server.key
   chmod 644 /etc/ssl/certs/server.crt
   ```

3. **Environment Variable Security**

   ```bash
   # Don't expose sensitive config in process lists
   export GRPC_TLS_KEY_FILE="/secure/path/key.pem"
   ```

### Performance

1. **Worker Thread Sizing**

   ```python
   import os

   # Scale workers with CPU cores
   cpu_count = os.cpu_count() or 1
   config = FlextGrpcConfig(
       max_workers=min(cpu_count * 4, 50)  # Cap at 50
   )
   ```

2. **Message Size Limits**

   ```python
   # Set appropriate message limits
   config = FlextGrpcConfig(
       max_receive_message_length=4*1024*1024,  # 4MB
       max_send_message_length=4*1024*1024      # 4MB
   )
   ```

3. **Timeout Configuration**

   ```python
   # Different timeouts for different operations
   config = FlextGrpcConfig(
       timeout=FlextGrpcConstants.Service.DEFAULT_TIMEOUT,  # General operations
       health_check_timeout=5.0,  # Health checks
       streaming_timeout=300.0    # Long-running streams
   )
   ```

### Monitoring

1. **Enable Health Checking**

   ```python
   config = FlextGrpcConfig(
       enable_health_checking=True,
       health_check_interval=30  # seconds
   )
   ```

2. **Metrics Collection**

   ```python
   config = FlextGrpcConfig(
       enable_metrics=True,
       metrics_port=FlextGrpcConstants.METRICS_PORT  # Prometheus metrics
   )
   ```

## Integration with FLEXT Patterns

### FlextResult Usage

Configuration operations return `FlextResult` for error handling:

```python
from flext_grpc import create_config
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities

def setup_configuration() -> FlextResult[FlextGrpcConfig]:
    return create_config(
        host=FlextGrpcConstants.Network.DEFAULT_HOST,
        port=FlextGrpcConstants.Network.DEFAULT_PORT
    ).flat_map(lambda config: validate_config(config))
```

### Container Integration

Register configuration with FlextContainer:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc import FlextGrpcConfig

container = FlextContainer.get_global()
config = FlextGrpcConfig(host=FlextGrpcConstants.Network.DEFAULT_HOST,
     port=FlextGrpcConstants.Network.DEFAULT_PORT)

container.register("grpc_config", config)

# Later retrieval
config_result = container.get("grpc_config")
if config_result.success:
    config = config_result.unwrap()
```

## Troubleshooting Configuration

### Common Issues

**Invalid Port Numbers**

```python
# Error: Port out of range
config = FlextGrpcConfig(port=70000)  # Too high
config = FlextGrpcConfig(port=80)     # Too low (reserved)
```

**TLS Certificate Issues**

```python
# Error: File not found
config = FlextGrpcConfig(
    use_tls=True,
    tls_cert_file="/nonexistent/cert.pem"  # File doesn't exist
)
```

**Environment Variable Conflicts**

```bash
# Multiple ways to set the same value can conflict
export GRPC_PORT=${FlextGrpcConstants.Network.DEFAULT_PORT}
export GRPC_PORT=${FlextConstants.Platform.DEFAULT_HTTP_PORT}  # Overwrites previous value
```

### Debugging Configuration

```python
import os
from flext_grpc import FlextGrpcConfig

def debug_config():
    print("Environment variables:")
    for key, value in os.environ.items():
        if key.startswith("GRPC_"):
            print(f"  {key}={value}")

    config = FlextGrpcConfig()
    print(f"\nActual configuration:")
    print(f"  Host: {config.host}")
    print(f"  Port: {config.port}")
    print(f"  Workers: {config.max_workers}")
    print(f"  Timeout: {config.timeout}")
```

---

This configuration guide provides comprehensive coverage of all configuration options and best practices for flext-grpc deployment and operation.
