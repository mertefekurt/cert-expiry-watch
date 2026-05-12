from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse


def normalize_target(raw: str, default_port: int = 443) -> tuple[str, int]:
    value = raw.strip()
    if not value:
        raise ValueError("target cannot be empty")

    parsed = urlparse(value if "://" in value else f"//{value}", scheme="https")
    host = parsed.hostname
    if not host:
        raise ValueError(f"invalid target: {raw}")

    return host.lower(), parsed.port or default_port


def load_targets(values: list[str], file_path: str | None, default_port: int = 443) -> list[tuple[str, int]]:
    raw_targets = list(values)
    if file_path:
        for line in Path(file_path).read_text(encoding="utf-8").splitlines():
            clean = line.strip()
            if clean and not clean.startswith("#"):
                raw_targets.append(clean)

    seen: set[tuple[str, int]] = set()
    targets: list[tuple[str, int]] = []
    for raw in raw_targets:
        target = normalize_target(raw, default_port=default_port)
        if target not in seen:
            seen.add(target)
            targets.append(target)
    return targets
