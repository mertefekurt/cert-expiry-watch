from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from cert_expiry_watch.models import CertificateResult, Status, classify_expiry


def _flatten_name(cert_value: tuple[tuple[str, str], ...] | None) -> str | None:
    if not cert_value:
        return None

    parts = [f"{key}={value}" for group in cert_value for key, value in group]
    return ", ".join(parts) if parts else None


def _parse_not_after(value: str) -> datetime:
    parsed = parsedate_to_datetime(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def inspect_certificate(
    host: str,
    port: int = 443,
    *,
    timeout: float = 5.0,
    warn_days: int = 30,
) -> CertificateResult:
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=host) as tls_socket:
                cert = tls_socket.getpeercert()

        not_after = cert.get("notAfter")
        if not not_after:
            return CertificateResult(
                host=host,
                port=port,
                status=Status.UNREACHABLE,
                error="certificate did not include notAfter",
            )

        expires_at = _parse_not_after(not_after)
        status, days_left = classify_expiry(expires_at, warn_days=warn_days)
        return CertificateResult(
            host=host,
            port=port,
            status=status,
            expires_at=expires_at,
            days_left=days_left,
            issuer=_flatten_name(cert.get("issuer")),
            subject=_flatten_name(cert.get("subject")),
        )
    except Exception as exc:  # noqa: BLE001
        return CertificateResult(
            host=host,
            port=port,
            status=Status.UNREACHABLE,
            error=str(exc),
        )
