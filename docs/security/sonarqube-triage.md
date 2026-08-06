# Triagem SonarCloud — flext-sh/flext-grpc

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.7`

## Resumo

**21 issues** — BLOCKER 0, CRITICAL 2, MAJOR 16, MINOR 3
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 17

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

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | CODE_SMELL | `python:S3776` | `examples/01_basic_usage.py` | 71 | |
| 2 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_grpc/_utilities/grpc.py` | 83 | |
| 3 | MAJOR | CODE_SMELL | `shelldre:S7688` | `.github/scripts/install-git-hooks.sh` | 55 | |
| 4 | MAJOR | CODE_SMELL | `shelldre:S7688` | `.github/scripts/install-git-hooks.sh` | 104 | |
| 5 | MAJOR | CODE_SMELL | `shelldre:S7688` | `.github/scripts/install-git-hooks.sh` | 106 | |
| 6 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 7 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 8 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 9 | MAJOR | CODE_SMELL | `shelldre:S7679` | `docs/architecture/tools/generate-diagrams.sh` | 21 | |
| 10 | MAJOR | CODE_SMELL | `shelldre:S7679` | `docs/architecture/tools/generate-diagrams.sh` | 25 | |
| 11 | MAJOR | CODE_SMELL | `shelldre:S7679` | `docs/architecture/tools/generate-diagrams.sh` | 29 | |
| 12 | MAJOR | CODE_SMELL | `shelldre:S7677` | `docs/architecture/tools/generate-diagrams.sh` | 33 | |
| 13 | MAJOR | CODE_SMELL | `shelldre:S7679` | `docs/architecture/tools/generate-diagrams.sh` | 33 | |
| 14 | MAJOR | CODE_SMELL | `shelldre:S7679` | `docs/architecture/tools/generate-diagrams.sh` | 226 | |
| 15 | MAJOR | CODE_SMELL | `shelldre:S7679` | `docs/architecture/tools/generate-diagrams.sh` | 257 | |
| 16 | MAJOR | CODE_SMELL | `python:S1854` | `docs/architecture/tools/validate_docs.py` | 193 | |
| 17 | MAJOR | VULNERABILITY | `text:S8565` | `pyproject.toml` | - | |
| 18 | MAJOR | CODE_SMELL | `python:S8786` | `src/flext_grpc/constants.py` | 97 | |
| 19 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 20 | MINOR | CODE_SMELL | `python:S116` | `src/flext_grpc/_utilities/grpc.py` | 28 | |
| 21 | MINOR | CODE_SMELL | `python:S116` | `src/flext_grpc/_utilities/grpc.py` | 29 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-grpc.json`

