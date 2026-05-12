from datetime import datetime, timezone

from cert_expiry_watch.models import Status, classify_expiry


def test_classify_expiry_marks_expired_warning_and_ok() -> None:
    now = datetime(2026, 5, 12, tzinfo=timezone.utc)

    assert classify_expiry(datetime(2026, 5, 11, tzinfo=timezone.utc), 30, now) == (
        Status.EXPIRED,
        -1,
    )
    assert classify_expiry(datetime(2026, 6, 1, tzinfo=timezone.utc), 30, now) == (
        Status.WARNING,
        20,
    )
    assert classify_expiry(datetime(2026, 8, 1, tzinfo=timezone.utc), 30, now) == (
        Status.OK,
        81,
    )
