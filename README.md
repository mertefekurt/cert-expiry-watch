<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=250&section=header&text=cert-expiry-watch&fontSize=60&fontAlignY=35&desc=Catch%20TLS%20certificate%20expirations%20before%20they%20become%20production%20outages%2C%20broken%20webhooks%2C%20or%20late-night%20incident%20calls.%20Check%20domains%2C%20URLs%2C%20and%20host-port%20targets%20in%20parallel%2C%20then%20ship%20clean%20tables%2C%20JSON%2C%20and%20CI-grade%20exit%20codes%20from%20one%20Python%20CLI.&descAlignY=55&descSize=20)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TLS](https://img.shields.io/badge/Focus-TLS%20Expiry-FF4ECD?style=for-the-badge&logo=letsencrypt&logoColor=white)
![Parallel](https://img.shields.io/badge/Checks-Parallel-33C9FF?style=for-the-badge&logo=fastapi&logoColor=white)
![CI](https://img.shields.io/badge/Automation-JSON%20%2B%20Exit%20Codes-16A34A?style=for-the-badge&logo=githubactions&logoColor=white)

</div>

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=33C9FF&width=700&height=40&lines=TLS+Expiry+Monitoring+For+Humans+And+CI)

`cert-expiry-watch` inspects live certificates for domains, URLs, and `host:port` endpoints, then classifies each target as ok, warning, expired, or unreachable. It is built for maintainers who want a tiny dependency-light command that fits cron jobs, release checks, CI workflows, and operations runbooks.

<table>
  <tr>
    <td width="50%" valign="top">

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=FF4ECD&width=500&height=40&lines=Core+Features)

- 🔐 Reads real TLS certificates over sockets with SNI support
- ⏳ Calculates exact expiry dates and remaining days
- 🚨 Separates ok, warning, expired, and unreachable states
- 📄 Loads bulk target lists with comment support
- ⚡ Runs checks in parallel with a configurable worker pool
- 🤖 Prints compact tables or JSON with CI-friendly exit behavior

  </td>
  <td width="50%" valign="top">

![Code Snapshot](assets/code-snapshot.png)

  </td>
  </tr>
</table>

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=9DFF57&width=700&height=40&lines=Blazing+Fast+CLI+Demo)

![Demo](https://readme-typing-svg.demolab.com/?font=Fira+Code&duration=1500&pause=500&multiline=true&width=950&height=150&color=F8F8F2&background=282A3600&lines=%24+cert-expiry-watch+example.com+api.example.com%3A8443;%3E+example.com%3A443+ok+50+days+left;%24+cert-expiry-watch+--file+domains.txt+--fail-on-warning+--json;%3E+CI-ready+certificate+report)

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=FFB86C&width=700&height=40&lines=Certificate+Check+Pipeline)

```mermaid
flowchart TD
    A[CLI Targets and Optional File] --> B[Normalize Domains, URLs, and Host Ports]
    B --> C[Deduplicate Endpoints]
    C --> D[ThreadPoolExecutor]
    D --> E[Open TLS Socket With SNI]
    E --> F[Read Peer Certificate]
    F --> G[Parse notAfter Timestamp]
    G --> H{Expiry Classification}
    H -->|Healthy| I[OK Result]
    H -->|Inside Threshold| J[Warning Result]
    H -->|Past Expiry| K[Expired Result]
    E -->|Network or TLS Error| L[Unreachable Result]
    I --> M[Table or JSON Formatter]
    J --> M
    K --> M
    L --> M
    M --> N[Exit Policy]
    classDef input fill:#33C9FF,stroke:#0F172A,color:#0F172A,stroke-width:2px
    classDef network fill:#9DFF57,stroke:#17320E,color:#0F172A,stroke-width:2px
    classDef classify fill:#FF4ECD,stroke:#2A0A1F,color:#FFFFFF,stroke-width:2px
    classDef output fill:#FFB86C,stroke:#4A2500,color:#0F172A,stroke-width:2px
    classDef danger fill:#EF4444,stroke:#450A0A,color:#FFFFFF,stroke-width:2px
    class A,B,C input
    class D,E,F,G network
    class H classify
    class I,J,M,N output
    class K,L danger
```

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=33C9FF&width=700&height=40&lines=Quick+Start)

```bash
git clone https://github.com/mertefekurt/cert-expiry-watch.git
cd cert-expiry-watch
python -m venv .venv
. .venv/bin/activate
pip install -e .
cert-expiry-watch example.com api.example.com:8443
```

<details>
<summary>🛠️ View CLI Reference / Advanced Config</summary>

| Command | Purpose |
| --- | --- |
| `cert-expiry-watch example.com` | Check one domain on port 443 |
| `cert-expiry-watch api.example.com:8443` | Check a custom TLS port |
| `cert-expiry-watch https://example.com` | Normalize a URL into a TLS endpoint |
| `cert-expiry-watch --file domains.txt` | Read newline-delimited targets from a file |
| `cert-expiry-watch example.com --json` | Emit machine-readable JSON |

| Flag | Default | Purpose |
| --- | ---: | --- |
| `targets` | none | Domains, URLs, or `host:port` targets |
| `-f`, `--file` | none | Read additional targets from a file |
| `-w`, `--warn-days` | `30` | Mark certificates inside this window as warnings |
| `-t`, `--timeout` | `5.0` | Socket timeout in seconds |
| `-j`, `--json` | `false` | Print JSON instead of a table |
| `--fail-on-warning` | `false` | Return exit code `1` for warning results |
| `--workers` | `8` | Maximum parallel certificate checks |

| Status | Meaning |
| --- | --- |
| `ok` | Certificate expires after the warning window |
| `warning` | Certificate expires within `--warn-days` |
| `expired` | Certificate is already past its expiry timestamp |
| `unreachable` | Network, DNS, TLS, or certificate parsing failed |

</details>

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=FF4ECD&width=700&height=40&lines=Project+Map)

```text
cert-expiry-watch/
├── src/cert_expiry_watch/
│   ├── cli.py        # argument parsing, workers, and orchestration
│   ├── collector.py  # socket/TLS certificate inspection
│   ├── formatter.py  # table, JSON, and exit-code behavior
│   ├── models.py     # status and result models
│   └── targets.py    # target normalization and file loading
├── tests/
└── assets/
    └── code-snapshot.png
```

![Header](https://readme-typing-svg.demolab.com/?font=Space+Mono&weight=700&size=26&color=9DFF57&width=700&height=40&lines=License)

MIT
