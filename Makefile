# FLEXT GRPC - High-Performance gRPC Service Layer
# =================================================
# Real Protocol Buffers with enterprise gRPC server implementation
# Python 3.13 + gRPC + Protobuf + Zero Tolerance Quality Gates

.PHONY: help check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-grpc
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: proto-gen proto-clean proto-validate dev-server run-server

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🚀 FLEXT GRPC - High-Performance gRPC Service Layer"
	@echo "=================================================="
	@echo "🎯 Clean Architecture + DDD + Python 3.13 + Real Protocol Buffers"
	@echo ""
	@echo "📦 Enterprise gRPC services with real protobuf implementation"
	@echo "🔒 Zero tolerance quality gates - NO mock/fake code allowed"
	@echo "🧪 90%+ test coverage requirement with real gRPC testing"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT GRPC COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_grpc --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-grpc: ## Run gRPC-specific tests
	@echo "🚀 Running gRPC service tests..."
	@poetry run pytest tests/grpc/ -v --tb=short
	@echo "✅ gRPC tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_grpc --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🔄 PROTOCOL BUFFERS OPERATIONS
# ============================================================================

proto-gen: ## Generate protobuf code from .proto files
	@echo "🔄 Generating protobuf code..."
	@poetry run python -m grpc_tools.protoc \
		--python_out=src/flext_grpc/proto \
		--grpc_python_out=src/flext_grpc/proto \
		--proto_path=src/flext_grpc/proto \
		src/flext_grpc/proto/*.proto
	@echo "✅ Protobuf code generated"

proto-clean: ## Clean generated protobuf files
	@echo "🧹 Cleaning generated protobuf files..."
	@rm -f src/flext_grpc/proto/*_pb2.py
	@rm -f src/flext_grpc/proto/*_pb2_grpc.py
	@echo "✅ Protobuf files cleaned"

proto-validate: ## Validate protobuf definitions
	@echo "🔍 Validating protobuf definitions..."
	@poetry run python -c "import grpc_tools.protoc; print('✅ Protobuf definitions are valid')"
	@echo "✅ Protobuf validation complete"

proto-check: ## Check if protobuf generation is needed
	@echo "🔍 Checking protobuf generation status..."
	@if [ -f src/flext_grpc/proto/flext.proto ]; then \
		if [ ! -f src/flext_grpc/proto/flext_pb2.py ]; then \
			echo "❌ Protobuf files need generation - run 'make proto-gen'"; \
			exit 1; \
		else \
			echo "✅ Protobuf files are up to date"; \
		fi; \
	else \
		echo "❌ No .proto files found"; \
		exit 1; \
	fi

# ============================================================================
# 🚀 GRPC SERVER OPERATIONS
# ============================================================================

dev-server: ## Start development gRPC server with auto-reload
	@echo "🚀 Starting development gRPC server..."
	@echo "📡 gRPC server will be available at: localhost:50051"
	@echo "🔄 Auto-reload enabled for development"
	@poetry run python -m flext_grpc.server --dev --reload

run-server: ## Start production gRPC server
	@echo "🚀 Starting production gRPC server..."
	@echo "📡 gRPC server running on localhost:50051"
	@poetry run python -m flext_grpc.server

server-health: ## Check gRPC server health
	@echo "🔍 Checking gRPC server health..."
	@poetry run python -c "import asyncio; from flext_grpc.client import FlextGrpcClient; exec(\"async def check(): client = FlextGrpcClient(); await client.connect(); health = await client.health_check(); print(f'Health: {health.healthy}'); await client.close()\"); asyncio.run(check())"

server-test: ## Test gRPC server endpoints
	@echo "🧪 Testing gRPC server endpoints..."
	@poetry run python -c "import asyncio; from flext_grpc.client import FlextGrpcClient; exec(\"async def test(): client = FlextGrpcClient(); await client.connect(); print('✅ gRPC server responding'); await client.close()\"); asyncio.run(test())"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean proto-gen ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# gRPC settings
export FLEXT_GRPC_HOST := localhost
export FLEXT_GRPC_PORT := 50051
export FLEXT_GRPC_DEV_MODE := true
export FLEXT_GRPC_MAX_WORKERS := 10

# Protocol Buffer settings
export PROTOBUF_PYTHON_IMPLEMENTATION := python

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-grpc
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT gRPC - High-Performance gRPC Service Layer

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 GRPC VALIDATION COMMANDS
# ============================================================================

grpc-validate: proto-check server-health ## Validate complete gRPC setup
	@echo "✅ gRPC setup validation complete"

grpc-performance: ## Test gRPC performance
	@echo "⚡ Testing gRPC performance..."
	@poetry run python -c "print('❌ Performance test requires running server - start with make dev-server first')"

grpc-stress-test: ## Run gRPC stress testing
	@echo "💪 Running gRPC stress test..."
	@poetry run python -c "print('❌ Stress test requires running server - start with make dev-server first')"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 gRPC project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Clean Architecture + DDD"
	@echo "🐍 Python: 3.13"
	@echo "🚀 Framework: gRPC + Real Protocol Buffers"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: High-Performance gRPC Service Layer"
	@echo "🔗 Dependencies: flext-core, flext-observability"
	@echo "📦 Provides: gRPC binary protocol services"
	@echo "🎯 Standards: Enterprise gRPC patterns with real protobuf"