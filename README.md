![Project Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=180&section=header&text=cert-expiry-watch&fontSize=50&fontAlignY=38)

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

# cert-expiry-watch

Check TLS certificate expiry across domains before renewals become incidents.

![Terminal Output](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=400&size=14&duration=1500&pause=500&center=false&vCenter=false&multiline=true&width=600&height=200&lines=%24+cert-expiry-watch+example.com;example.com%3A443+ok+50+days+left;%24+cert-expiry-watch+--file+domains.txt+--fail-on-warning)

## What It Does

| Capability | Detail |
| --- | --- |
| expiry checks | reads live TLS certificates from domains, URLs, or `host:port` targets |
| warning policy | marks certificates inside `--warn-days` as `warning` |
| CI-friendly | returns non-zero for expired or unreachable certificates |
| output modes | prints compact tables or JSON for automation |
| bulk input | accepts newline-delimited target files with comments |

## Install

```bash
git clone https://github.com/mertefekurt/cert-expiry-watch.git
cd cert-expiry-watch
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Usage

```bash
cert-expiry-watch example.com api.example.com:8443
cert-expiry-watch --file domains.txt --warn-days 21
cert-expiry-watch example.com --json
```

## CLI Reference

| Argument / Flag | Purpose | Default |
| --- | --- | --- |
| `targets` | domains, URLs, or `host:port` values | none |
| `-f`, `--file` | newline-delimited targets file | none |
| `-w`, `--warn-days` | days before expiry to mark `warning` | `30` |
| `-t`, `--timeout` | socket timeout in seconds | `5.0` |
| `-j`, `--json` | print machine-readable JSON | `false` |
| `--fail-on-warning` | return exit code `1` for warnings | `false` |
| `--workers` | parallel certificate checks | `8` |

## Architecture

```mermaid
flowchart TD
    A["CLI args"] --> B["target loader"]
    B --> C["normalized endpoints"]
    C --> D["thread pool"]
    D --> E["TLS collector"]
    E --> F["expiry classifier"]
    F --> G{"output mode"}
    G --> H["table formatter"]
    G --> I["JSON formatter"]
    H --> J["exit policy"]
    I --> J
```

## Code Snapshot

![Code Snippet](assets/code-snapshot.png)

## Project Layout

```text
src/cert_expiry_watch/
  cli.py          argument parsing and orchestration
  collector.py    TLS socket inspection
  formatter.py    table, JSON, and exit policy
  models.py       result and status types
  targets.py      target parsing and file loading
tests/
  test_*.py       focused unit tests
```

## Development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT
