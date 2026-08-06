# Triagem SonarCloud — flext-sh/flext-grpc

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.7`

## Resumo

**21 issues** — BLOCKER 0, CRITICAL 2, MAJOR 16, MINOR 3
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 17 · **Debt total: 107min**

| regra | issues |
|---|---|
| `shelldre:S7679` | 6 |
| `shelldre:S7688` | 3 |
| `githubactions:S8233` | 2 |
| `python:S116` | 2 |
| `python:S3776` | 1 |
| `python:S1192` | 1 |
| `githubactions:S8264` | 1 |
| `shelldre:S7677` | 1 |
| `python:S1854` | 1 |
| `text:S8565` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `examples/01_basic_usage.py:71` · **Effort**: 8min

> Refactor this function to reduce its Cognitive Complexity from 18 to the 15 allowed.

```python
       67      if invalid_server_result.failure:
       68          _emit(f"Expected validation failure: {invalid_server_result.error}")
       69  
       70  
>>>    71  def example_3_operations() -> None:
       72      """Use gRPC operations through the FlextGrpc facade."""
       73      grpc = FlextGrpc()
       74      server_result = grpc.create_server(
       75          host=FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST, port=7070
```

**Decisão**: 

### 2 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_grpc/_utilities/grpc.py:83` · **Effort**: 8min

> Define a constant instead of duplicating this literal "gRPC runtime unavailable" 4 times.

```python
       79              lambda: import_module("grpc"), catch=(ImportError, ModuleNotFoundError)
       80          )
       81          if runtime_result.failure:
       82              return r[p.Grpc.GrpcRuntime].fail(
>>>    83                  runtime_result.error or "gRPC runtime unavailable",
       84                  exception=runtime_result.exception,
       85              )
       86          return r[p.Grpc.GrpcRuntime].ok(
       87              FlextGrpcUtilitiesGrpc._GrpcRuntimeAdapter(runtime_result.value)
```

**Decisão**: 

### 3 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7688`
**Local**: `.github/scripts/install-git-hooks.sh:55` · **Effort**: 2min

> Use '[[' instead of '[' for conditional tests. The '[[' construct is safer and more feature-rich.

```bash
       51  _log "Installing Beads git hooks (chained) at ${WORKSPACE_ROOT}"
       52  bd hooks install --chain >/dev/null || fail "bd hooks install --chain failed"
       53  
       54  hook_path="$(git rev-parse --git-path hooks/prepare-commit-msg)"
>>>    55  [ -f "${hook_path}" ] || fail "prepare-commit-msg hook missing after bd hooks install"
       56  
       57  _log "Applying FLEXT agent-trailer guard to ${hook_path}"
       58  GUARD_TOKEN="BD_ALLOW_AGENT_COMMIT_TRAILERS" python3 - "${hook_path}" <<'PY'
       59  import os
```

**Decisão**: 

### 4 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7688`
**Local**: `.github/scripts/install-git-hooks.sh:104` · **Effort**: 2min

> Use '[[' instead of '[' for conditional tests. The '[[' construct is safer and more feature-rich.

```bash
      100  grep -q 'BD_ALLOW_AGENT_COMMIT_TRAILERS' "${hook_path}" \
      101  	|| fail "guard token missing after injection"
      102  grep -q 'bd hooks run prepare-commit-msg' "${hook_path}" \
      103  	|| fail "bd delegation missing; refusing to leave hook without beads integration"
>>>   104  [ -f "$(git rev-parse --git-path hooks/pre-commit)" ] \
      105  	|| fail "pre-commit hook missing after provisioning"
      106  [ -f "$(git rev-parse --git-path hooks/pre-push)" ] \
      107  	|| fail "pre-push hook missing after provisioning"
      108  
```

**Decisão**: 

### 5 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7688`
**Local**: `.github/scripts/install-git-hooks.sh:106` · **Effort**: 2min

> Use '[[' instead of '[' for conditional tests. The '[[' construct is safer and more feature-rich.

```bash
      102  grep -q 'bd hooks run prepare-commit-msg' "${hook_path}" \
      103  	|| fail "bd delegation missing; refusing to leave hook without beads integration"
      104  [ -f "$(git rev-parse --git-path hooks/pre-commit)" ] \
      105  	|| fail "pre-commit hook missing after provisioning"
>>>   106  [ -f "$(git rev-parse --git-path hooks/pre-push)" ] \
      107  	|| fail "pre-push hook missing after provisioning"
      108  
      109  echo "install-git-hooks: prepare-commit-msg guarded (BD_ALLOW_AGENT_COMMIT_TRAILERS opt-in)"
```

**Decisão**: 

### 6 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: 

### 7 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: 

### 8 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: 

### 9 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7679`
**Local**: `docs/architecture/tools/generate-diagrams.sh:21` · **Effort**: 5min

> Assign this positional parameter to a local variable.

```bash
       17  NC='\033[0m' # No Color
       18  
       19  # Logging functions
       20  log_info() {
>>>    21  	echo -e "${BLUE}[INFO]${NC} $1"
       22  }
       23  
       24  log_success() {
       25  	echo -e "${GREEN}[SUCCESS]${NC} $1"
```

**Decisão**: 

### 10 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7679`
**Local**: `docs/architecture/tools/generate-diagrams.sh:25` · **Effort**: 5min

> Assign this positional parameter to a local variable.

```bash
       21  	echo -e "${BLUE}[INFO]${NC} $1"
       22  }
       23  
       24  log_success() {
>>>    25  	echo -e "${GREEN}[SUCCESS]${NC} $1"
       26  }
       27  
       28  log_warning() {
       29  	echo -e "${YELLOW}[WARNING]${NC} $1"
```

**Decisão**: 

### 11 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7679`
**Local**: `docs/architecture/tools/generate-diagrams.sh:29` · **Effort**: 5min

> Assign this positional parameter to a local variable.

```bash
       25  	echo -e "${GREEN}[SUCCESS]${NC} $1"
       26  }
       27  
       28  log_warning() {
>>>    29  	echo -e "${YELLOW}[WARNING]${NC} $1"
       30  }
       31  
       32  log_error() {
       33  	echo -e "${RED}[ERROR]${NC} $1"
```

**Decisão**: 

### 12 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7677`
**Local**: `docs/architecture/tools/generate-diagrams.sh:33` · **Effort**: 5min

> Redirect this error message to stderr (>&2).

```bash
       29  	echo -e "${YELLOW}[WARNING]${NC} $1"
       30  }
       31  
       32  log_error() {
>>>    33  	echo -e "${RED}[ERROR]${NC} $1"
       34  }
       35  
       36  # Check dependencies
       37  check_dependencies() {
```

**Decisão**: 

### 13 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7679`
**Local**: `docs/architecture/tools/generate-diagrams.sh:33` · **Effort**: 5min

> Assign this positional parameter to a local variable.

```bash
       29  	echo -e "${YELLOW}[WARNING]${NC} $1"
       30  }
       31  
       32  log_error() {
>>>    33  	echo -e "${RED}[ERROR]${NC} $1"
       34  }
       35  
       36  # Check dependencies
       37  check_dependencies() {
```

**Decisão**: 

### 14 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7679`
**Local**: `docs/architecture/tools/generate-diagrams.sh:226` · **Effort**: 5min

> Assign this positional parameter to a local variable.

```bash
      222  	local skip_validation=false
      223  
      224  	# Parse arguments
      225  	while [[ $# -gt 0 ]]; do
>>>   226  		case $1 in
      227  		--png-only)
      228  			generate_svg=false
      229  			generate_ascii=false
      230  			shift
```

**Decisão**: 

### 15 · 🟡 MAJOR · CODE_SMELL · `shelldre:S7679`
**Local**: `docs/architecture/tools/generate-diagrams.sh:257` · **Effort**: 5min

> Assign this positional parameter to a local variable.

```bash
      253  			echo "  --help           Show this help"
      254  			exit 0
      255  			;;
      256  		*)
>>>   257  			log_error "Unknown option: $1"
      258  			exit 1
      259  			;;
      260  		esac
      261  	done
```

**Decisão**: 

### 16 · 🟡 MAJOR · CODE_SMELL · `python:S1854`
**Local**: `docs/architecture/tools/validate_docs.py:193` · **Effort**: 1min

> Remove this assignment to local variable 'adr_files'; the value is never used.

```python
      189                  "message": "ADR README documentation missing",
      190              })
      191  
      192          # Check for ADR files
>>>   193          adr_files = list(adr_dir.glob("adr-*.md"))
      194  
      195          # Check for ADR files
      196          adr_files = list(adr_dir.glob("adr-*.md"))
      197          if len(adr_files) < self.MIN_ADR_FILES:
```

**Decisão**: 

### 17 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, poetry.lock, pdm.lock or pylock.toml) is missing.


**Decisão**: 

### 18 · 🟡 MAJOR · CODE_SMELL · `python:S8786`
**Local**: `src/flext_grpc/constants.py:97` · **Effort**: 20min

> Simplify this regular expression to reduce its runtime, as it has super-linear performance due to backtracking.

```python
       93  
       94          # ===== Validation constants =====
       95          VALIDATION_ADDRESS_PARTS_COUNT: Final[int] = 2
       96          VALIDATION_MAX_PORT_NUMBER: Final[int] = 65535
>>>    97          VALIDATION_VERSION_PATTERN: Final[str] = r"Version.*(\d+\.\d+\.\d+)"
       98          VALIDATION_VERSION_RE: ClassVar[t.RegexPattern] = re.compile(
       99              VALIDATION_VERSION_PATTERN, re.IGNORECASE
      100          )
      101  
```

**Decisão**: 

### 19 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: 

### 20 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_grpc/_utilities/grpc.py:28` · **Effort**: 2min

> Rename this field "RpcError" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       24  
       25      class _GrpcRuntimeAdapter:
       26          """Typed adapter that isolates the untyped grpc runtime module."""
       27  
>>>    28          RpcError: type[Exception]
       29          FutureTimeoutError: type[Exception]
       30  
       31          def __init__(self, runtime_module: ModuleType) -> None:
       32              """Store the imported grpc module."""
```

**Decisão**: 

### 21 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_grpc/_utilities/grpc.py:29` · **Effort**: 2min

> Rename this field "FutureTimeoutError" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       25      class _GrpcRuntimeAdapter:
       26          """Typed adapter that isolates the untyped grpc runtime module."""
       27  
       28          RpcError: type[Exception]
>>>    29          FutureTimeoutError: type[Exception]
       30  
       31          def __init__(self, runtime_module: ModuleType) -> None:
       32              """Store the imported grpc module."""
       33              self._runtime_module = runtime_module
```

**Decisão**: 

