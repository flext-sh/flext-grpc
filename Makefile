# =============================================================================
# FLEXT-GRPC - gRPC Communication Platform Makefile
# =============================================================================
# Python 3.13+ gRPC Framework - Clean Architecture + DDD + Zero Tolerance
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-grpc
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
COV_DIR := flext_grpc

# Quality Standards
MIN_COVERAGE := 100

# gRPC Configuration
GRPC_HOST := ${FlextGrpcConstants.Network.DEFAULT_HOST}
GRPC_PORT := ${FlextGrpcConstants.Network.DEFAULT_PORT}
GRPC_MAX_WORKERS := 10

# Export Configuration
export PROJECT_NAME PYTHON_VERSION MIN_COVERAGE GRPC_HOST GRPC_PORT GRPC_MAX_WORKERS

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "FLEXT-GRPC - gRPC Communication Platform"
	@echo "======================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}'

.PHONY: info
info: ## Show project information
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)+"
	@echo "Poetry: $(POETRY)"
	@echo "Coverage: $(MIN_COVERAGE)% minimum (MANDATORY)"
	@echo "gRPC: $(GRPC_HOST):$(GRPC_PORT) ($(GRPC_MAX_WORKERS) workers)"
	@echo "Architecture: Clean Architecture + DDD + gRPC"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install
install: ## Install dependencies
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# =============================================================================
# QUALITY GATES (MANDATORY - ZERO TOLERANCE)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates (MANDATORY ORDER)

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting (ZERO TOLERANCE)
	$(POETRY) run ruff check .

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format .

.PHONY: type-check
type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pyrefly check .

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

# =============================================================================
# TESTING (MANDATORY - 100% COVERAGE)
# =============================================================================

.PHONY: test
test: ## Run tests with 100% coverage (MANDATORY)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -q --maxfail=10000 --cov=$(COV_DIR) --cov-report=term-missing:skip-covered --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests with Docker
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m integration -v

.PHONY: test-grpc
test-grpc: ## Run gRPC specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m grpc -v

.PHONY: test-server
test-server: ## Run server tests
	$(POETRY) run pytest $(TESTS_DIR) -m server -v

.PHONY: test-client
test-client: ## Run client tests
	$(POETRY) run pytest $(TESTS_DIR) -m client -v

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	$(POETRY) run pytest $(TESTS_DIR) -m e2e -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest --cov=$(COV_DIR) --cov-report=html

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build package
	$(POETRY) build

.PHONY: build-clean
build-clean: clean build ## Clean and build

# =============================================================================
# GRPC OPERATIONS
# =============================================================================

.PHONY: proto-gen
proto-gen: ## Generate protobuf code
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. proto/*.proto

.PHONY: grpc-test
grpc-test: ## Test gRPC connectivity
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_grpc import FlextGrpcPlatform; print('gRPC test passed')"

.PHONY: grpc-server
grpc-server: ## Start development gRPC server
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_grpc import FlextGrpcServer; server = FlextGrpcServer(host='$(GRPC_HOST)', port=$(GRPC_PORT)); print('gRPC server started on $(GRPC_HOST):$(GRPC_PORT)')"

.PHONY: grpc-client
grpc-client: ## Test gRPC client connection
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_grpc import FlextGrpcClient; print('gRPC client test passed')"

.PHONY: grpc-operations
grpc-operations: grpc-test proto-gen grpc-client ## Run all gRPC validations

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# =============================================================================
# DEPENDENCIES
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# =============================================================================
# DEVELOPMENT
# =============================================================================

.PHONY: shell
shell: ## Open Python shell
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .pyrefly_cache/ .ruff_cache/
	rm -rf proto/*_pb2.py proto/*_pb2_grpc.py
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

.PHONY: diagnose
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "gRPC: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import grpc; print(grpc.__version__)' 2>/dev/null || echo 'Not available')"
	@echo "Protobuf: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import google.protobuf; print(google.protobuf.__version__)' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================

# =============================================================================

.PHONY: t l f tc c i v
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help
