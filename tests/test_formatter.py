from datetime import datetime, timezone

from cert_expiry_watch.formatter import exit_code, format_json, format_table
from cert_expiry_watch.models import CertificateResult, Status


def test_formatters_include_core_fields() -> None:
    result = CertificateResult(
        host="example.com",
        port=443,
        status=Status.OK,
        expires_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        days_left=50,
        issuer="CN=Example CA",
    )

    assert '"endpoint": "example.com:443"' in format_json([result])
    assert "example.com:443" in format_table([result])
    assert "CN=Example CA" in format_table([result])


def test_exit_code_respects_failure_policy() -> None:
    warning = CertificateResult("soon.test", 443, Status.WARNING)
    expired = CertificateResult("old.test", 443, Status.EXPIRED)

    assert exit_code([warning]) == 0
    assert exit_code([warning], fail_on_warning=True) == 1
    assert exit_code([expired]) == 1
