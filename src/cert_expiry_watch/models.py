from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class Status(str, Enum):
    OK = "ok"
    WARNING = "warning"
    EXPIRED = "expired"
    UNREACHABLE = "unreachable"


@dataclass(frozen=True)
class CertificateResult:
    host: str
    port: int
    status: Status
    expires_at: datetime | None = None
    days_left: int | None = None
    issuer: str | None = None
    subject: str | None = None
    error: str | None = None

    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.port}"


def classify_expiry(expires_at: datetime, warn_days: int, now: datetime | None = None) -> tuple[Status, int]:
    current = now or datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    days_left = (expires_at - current).days
    if days_left < 0:
        return Status.EXPIRED, days_left
    if days_left <= warn_days:
        return Status.WARNING, days_left
    return Status.OK, days_left
