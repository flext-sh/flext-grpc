# FLEXT-GRPC Makefile - Enterprise gRPC Services
# ===============================================

.PHONY: help install test clean lint format build docs dev server proto security grpc-test

# Default target
help: ## Show this help message
	@echo "📡 FLEXT-GRPC - Enterprise gRPC Services"
	@echo "========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation & Setup
install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies for flext-grpc services..."
	poetry install --all-extras

install-dev: ## Install with dev dependencies
	@echo "🛠️  Installing dev dependencies..."
	poetry install --all-extras --group dev --group test --group security

# gRPC Server Management
server: ## Run gRPC development server
	@echo "🚀 Starting gRPC development server..."
	poetry run python -m flext_grpc.server --port 50051 --workers 4 --debug

server-prod: ## Run gRPC production server
	@echo "🏭 Starting gRPC production server..."
	poetry run python -m flext_grpc.server --port 50051 --workers 10 --ssl

# Protocol Buffers Management
proto-generate: ## Generate Python code from .proto files
	@echo "⚙️  Generating Python code from proto files..."
	poetry run python -m grpc_tools.protoc \
		-I src/flext_grpc/proto \
		--python_out=src/flext_grpc/proto \
		--grpc_python_out=src/flext_grpc/proto \
		--mypy_out=src/flext_grpc/proto \
		src/flext_grpc/proto/*.proto
	@echo "✅ Proto files generated"

proto-validate: ## Validate .proto files
	@echo "🔍 Validating proto files..."
	@for proto in src/flext_grpc/proto/*.proto; do \
		echo "Validating $$proto..."; \
		poetry run python -c "import grpc_tools.protoc; grpc_tools.protoc.main(['-I', 'src/flext_grpc/proto', '--python_out=/tmp', '$$proto'])" || exit 1; \
	done
	@echo "✅ Proto validation complete"

# gRPC Testing
grpc-test: ## Test gRPC endpoints
	@echo "🔍 Testing gRPC endpoints..."
	poetry run pytest tests/grpc/ -v --grpc-server=localhost:50051

grpc-health: ## Check gRPC server health
	@echo "💓 Checking gRPC server health..."
	@command -v grpcurl >/dev/null 2>&1 && poetry run grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check || echo "grpcurl not installed or server not running"

grpc-list: ## List available gRPC services
	@echo "📋 Listing gRPC services..."
	@command -v grpcurl >/dev/null 2>&1 && poetry run grpcurl -plaintext localhost:50051 list || echo "grpcurl not installed or server not running"

load-test: ## Run gRPC load tests
	@echo "⚡ Running gRPC load tests..."
	@if [ -f tests/load/grpc_load_test.py ]; then \
		poetry run python tests/load/grpc_load_test.py; \
	else \
		echo "Load tests not configured"; \
	fi

# Testing
test: ## Run gRPC tests
	@echo "🧪 Running gRPC tests..."
	poetry run pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage
	@echo "📊 Running tests with coverage..."
	poetry run pytest tests/ --cov=src/flext_grpc --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=95

# Code Quality - Maximum Strictness
lint: ## Run all linters with maximum strictness
	@echo "🔍 Running maximum strictness linting for gRPC services..."
	poetry run ruff check . --output-format=verbose
	@echo "✅ Ruff linting complete"

format: ## Format code with strict standards
	@echo "🎨 Formatting gRPC code..."
	poetry run black .
	poetry run ruff check --fix .
	@echo "✅ Code formatting complete"

type-check: ## Run strict type checking
	@echo "🎯 Running strict MyPy type checking..."
	poetry run mypy src/flext_grpc --strict --show-error-codes
	@echo "✅ Type checking complete"

security: ## Run security analysis
	@echo "🔒 Running security analysis for gRPC..."
	poetry run bandit -r src/ -f json -o reports/security.json || true
	poetry run bandit -r src/ -f txt
	@echo "✅ Security analysis complete"

check: lint type-check security test ## Run all quality checks
	@echo "✅ All quality checks complete for flext-grpc!"

# Build & Distribution
build: ## Build the gRPC package
	@echo "🔨 Building flext-grpc package..."
	poetry build
	@echo "📦 Package built successfully"

# Development Workflow
dev-setup: install-dev proto-generate ## Complete development setup
	@echo "🎯 Setting up gRPC development environment..."
	poetry run pre-commit install
	mkdir -p reports logs
	@echo "📡 Run 'make server' to start gRPC server"
	@echo "💓 Run 'make grpc-health' to check server health"
	@echo "✅ Development setup complete!"

dev: server ## Alias for development server

# Client Tools
client-test: ## Test gRPC client
	@echo "📞 Testing gRPC client..."
	poetry run python -c "
from flext_grpc.client import FlextGrpcClient
client = FlextGrpcClient('localhost:50051')
try:
    health = client.health_check()
    print(f'✅ Server health: {health}')
except Exception as e:
    print(f'❌ Connection failed: {e}')
"

# Cleanup
clean: ## Clean build artifacts and generated files
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf reports/ logs/ .coverage htmlcov/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true

# Environment variables
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export GRPC_PORT := 50051
export GRPC_DEBUG := true
export FLEXT_GRPC_DEV := true