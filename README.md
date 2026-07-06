<p align="center">
  <img src="assets/readme-cover.svg" alt="Cert Expiry Watch cover" width="100%" />
</p>

# Cert Expiry Watch

![stack](https://img.shields.io/badge/stack-Python-dc2626?style=flat-square) ![python](https://img.shields.io/badge/python-3.10-7c3aed?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-0891b2?style=flat-square) ![tests](https://img.shields.io/badge/tests-pytest-b45309?style=flat-square)

A fast CLI for checking TLS certificate expiry across domains.

## Good for

- quick local checks around certificate monitoring
- small CI jobs where a readable report is enough
- review workflows that need deterministic output

## Run it

```bash
python -m pip install -e ".[dev]"
cert-expiry-watch --help
python -m cert_expiry_watch --help
```

## Project notes

- Command: `cert-expiry-watch`
- Language: Python
- Python: `>=3.10`
- Tests: `pytest`

## Layout

```text
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```

## Check locally

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m cert_expiry_watch --help
```
