# Cert Expiry Watch

A fast CLI for checking TLS certificate expiry across domains. The repository is intentionally plain: a small command, a visible rule surface, and enough examples to make the behavior inspectable.

![Cert Expiry Watch cover](assets/readme-cover.svg)

## Where it fits

- for deployment, cloud, CI, config, and operational safety checks
- quick local checks without a service dependency
- review notes that should stay easy to reproduce

## Run it

```bash
git clone https://github.com/mertefekurt/cert-expiry-watch.git
cd cert-expiry-watch
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cert-expiry-watch --help
```

## Project map

```text
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```
