from pathlib import Path

from cert_expiry_watch.targets import load_targets, normalize_target


def test_normalize_target_handles_domains_urls_and_ports() -> None:
    assert normalize_target("Example.com") == ("example.com", 443)
    assert normalize_target("https://example.com:8443/path") == ("example.com", 8443)
    assert normalize_target("api.example.com:9443") == ("api.example.com", 9443)


def test_load_targets_uses_file_and_deduplicates(tmp_path: Path) -> None:
    target_file = tmp_path / "targets.txt"
    target_file.write_text("# ignored\nexample.com\nhttps://example.com\napi.test:444\n", encoding="utf-8")

    assert load_targets(["api.test:444"], str(target_file)) == [
        ("api.test", 444),
        ("example.com", 443),
    ]
