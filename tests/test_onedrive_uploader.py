from __future__ import annotations

import io
import json
from pathlib import Path
import urllib.error
import urllib.request


class _FakeResponse:
    def __init__(self, payload: dict | None = None):
        body = payload if payload is not None else {}
        self._bytes = json.dumps(body).encode("utf-8")

    def read(self) -> bytes:
        return self._bytes

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # noqa: ANN001
        return False


def test_upload_delivery_package_skips_when_config_missing(monkeypatch, tmp_path: Path) -> None:
    from src.reporting.onedrive_uploader import upload_delivery_package

    for key in [
        "ONEDRIVE_TENANT_ID",
        "ONEDRIVE_CLIENT_ID",
        "ONEDRIVE_CLIENT_SECRET",
        "ONEDRIVE_DRIVE_ID",
        "ONEDRIVE_TARGET_DIR",
    ]:
        monkeypatch.delenv(key, raising=False)

    local_zip = tmp_path / "payload.zip"
    local_zip.write_bytes(b"dummy")

    report = upload_delivery_package(local_zip)
    assert report["status"] == "SKIPPED_CONFIG"


def test_upload_delivery_package_success_simple(monkeypatch, tmp_path: Path) -> None:
    from src.reporting.onedrive_uploader import upload_delivery_package

    monkeypatch.setenv("ONEDRIVE_TENANT_ID", "tenant")
    monkeypatch.setenv("ONEDRIVE_CLIENT_ID", "client")
    monkeypatch.setenv("ONEDRIVE_CLIENT_SECRET", "secret")
    monkeypatch.setenv("ONEDRIVE_DRIVE_ID", "drive")
    monkeypatch.setenv("ONEDRIVE_TARGET_DIR", "TTE-Capture-Prices/Audit-Runs")

    local_zip = tmp_path / "payload.zip"
    local_zip.write_bytes(b"payload-bytes")

    def fake_urlopen(req, timeout=60):  # type: ignore[no-untyped-def]
        url = getattr(req, "full_url", "")
        if "oauth2/v2.0/token" in str(url):
            return _FakeResponse({"access_token": "tok"})
        if "/content" in str(url):
            return _FakeResponse({"id": "item-1", "webUrl": "https://example/item-1"})
        raise RuntimeError(f"Unexpected URL: {url}")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    report = upload_delivery_package(local_zip)
    assert report["status"] == "UPLOADED"
    assert report["mode"] == "simple"
    assert int(report["uploaded_bytes"]) == int(local_zip.stat().st_size)


def test_upload_delivery_package_handles_http_error(monkeypatch, tmp_path: Path) -> None:
    from src.reporting.onedrive_uploader import upload_delivery_package

    monkeypatch.setenv("ONEDRIVE_TENANT_ID", "tenant")
    monkeypatch.setenv("ONEDRIVE_CLIENT_ID", "client")
    monkeypatch.setenv("ONEDRIVE_CLIENT_SECRET", "secret")
    monkeypatch.setenv("ONEDRIVE_DRIVE_ID", "drive")

    local_zip = tmp_path / "payload.zip"
    local_zip.write_bytes(b"payload-bytes")

    def fake_urlopen(req, timeout=60):  # type: ignore[no-untyped-def]
        url = getattr(req, "full_url", "")
        if "oauth2/v2.0/token" in str(url):
            return _FakeResponse({"access_token": "tok"})
        if "/content" in str(url):
            raise urllib.error.HTTPError(str(url), 403, "Forbidden", hdrs=None, fp=io.BytesIO(b'{"error":"forbidden"}'))
        raise RuntimeError(f"Unexpected URL: {url}")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    report = upload_delivery_package(local_zip)
    assert report["status"] == "FAILED"
    assert "HTTP 403" in str(report.get("error", ""))

