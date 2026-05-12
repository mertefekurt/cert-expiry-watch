from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from cert_expiry_watch.collector import inspect_certificate
from cert_expiry_watch.formatter import exit_code, format_json, format_table
from cert_expiry_watch.targets import load_targets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cert-expiry-watch",
        description="Check TLS certificate expiry for one or more endpoints.",
    )
    parser.add_argument("targets", nargs="*", help="domains, URLs, or host:port pairs")
    parser.add_argument("-f", "--file", help="read targets from a newline-delimited file")
    parser.add_argument("-w", "--warn-days", type=int, default=30, help="warning threshold in days")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="socket timeout in seconds")
    parser.add_argument("-j", "--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--fail-on-warning", action="store_true", help="return exit code 1 for warnings")
    parser.add_argument("--workers", type=int, default=8, help="parallel checks to run")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    targets = load_targets(args.targets, args.file)
    if not targets:
        parser.error("provide at least one target or --file")

    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(
            executor.map(
                lambda target: inspect_certificate(
                    target[0],
                    target[1],
                    timeout=args.timeout,
                    warn_days=args.warn_days,
                ),
                targets,
            )
        )

    print(format_json(results) if args.json else format_table(results))
    return exit_code(results, fail_on_warning=args.fail_on_warning)


def main(argv: Sequence[str] | None = None) -> int:
    return run(argv)
