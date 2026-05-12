from __future__ import annotations

import json
from datetime import datetime

from cert_expiry_watch.models import CertificateResult, Status


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def result_to_dict(result: CertificateResult) -> dict[str, object]:
    return {
        "endpoint": result.endpoint,
        "host": result.host,
        "port": result.port,
        "status": result.status.value,
        "expires_at": _iso(result.expires_at),
        "days_left": result.days_left,
        "issuer": result.issuer,
        "subject": result.subject,
        "error": result.error,
    }


def format_json(results: list[CertificateResult]) -> str:
    return json.dumps([result_to_dict(result) for result in results], indent=2)


def format_table(results: list[CertificateResult]) -> str:
    headers = ["endpoint", "status", "days", "expires", "issuer/error"]
    rows = [
        [
            result.endpoint,
            result.status.value,
            "" if result.days_left is None else str(result.days_left),
            result.expires_at.strftime("%Y-%m-%d") if result.expires_at else "",
            result.issuer or result.error or "",
        ]
        for result in results
    ]
    widths = [
        max(len(str(row[index])) for row in [headers, *rows])
        for index in range(len(headers))
    ]

    def render(row: list[str]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    divider = "  ".join("-" * width for width in widths)
    return "\n".join([render(headers), divider, *[render(row) for row in rows]])


def exit_code(results: list[CertificateResult], fail_on_warning: bool = False) -> int:
    failing = {Status.EXPIRED, Status.UNREACHABLE}
    if fail_on_warning:
        failing.add(Status.WARNING)
    return 1 if any(result.status in failing for result in results) else 0
