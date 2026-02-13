from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_TARGET_DIR = "TTE-Capture-Prices/Audit-Runs"
_CHUNK_THRESHOLD = 4 * 1024 * 1024
_DEFAULT_CHUNK_SIZE = 5 * 1024 * 1024


def _env(name: str) -> str:
    return str(os.environ.get(name, "")).strip()


def onedrive_is_configured() -> bool:
    required = [
        "ONEDRIVE_TENANT_ID",
        "ONEDRIVE_CLIENT_ID",
        "ONEDRIVE_CLIENT_SECRET",
        "ONEDRIVE_DRIVE_ID",
    ]
    return all(bool(_env(k)) for k in required)


def _graph_token(timeout_sec: int = 30) -> str:
    tenant = _env("ONEDRIVE_TENANT_ID")
    client_id = _env("ONEDRIVE_CLIENT_ID")
    client_secret = _env("ONEDRIVE_CLIENT_SECRET")
    if not (tenant and client_id and client_secret):
        return ""
    token_url = f"https://login.microsoftonline.com/{urllib.parse.quote(tenant)}/oauth2/v2.0/token"
    payload = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        token_url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        data = resp.read()
    parsed = json.loads(data.decode("utf-8")) if data else {}
    return str(parsed.get("access_token", "")).strip()


def _json_request(req: urllib.request.Request, timeout_sec: int = 60) -> dict[str, Any]:
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        payload = resp.read()
    if not payload:
        return {}
    try:
        return json.loads(payload.decode("utf-8"))
    except Exception:
        return {}


def _encode_graph_path(path: str) -> str:
    clean = "/".join([p for p in str(path).replace("\\", "/").split("/") if p])
    return urllib.parse.quote(clean, safe="/")


def _upload_simple(
    token: str,
    drive_id: str,
    target_path: str,
    local_file: Path,
    timeout_sec: int,
) -> dict[str, Any]:
    url = f"https://graph.microsoft.com/v1.0/drives/{urllib.parse.quote(drive_id)}/root:/{_encode_graph_path(target_path)}:/content"
    data = local_file.read_bytes()
    req = urllib.request.Request(
        url,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/zip",
        },
    )
    response = _json_request(req, timeout_sec=timeout_sec)
    return {
        "status": "UPLOADED",
        "mode": "simple",
        "uploaded_bytes": int(local_file.stat().st_size),
        "target_path": target_path,
        "item_id": str(response.get("id", "")),
        "web_url": str(response.get("webUrl", "")),
    }


def _upload_chunked(
    token: str,
    drive_id: str,
    target_path: str,
    local_file: Path,
    timeout_sec: int,
    chunk_size: int,
) -> dict[str, Any]:
    session_url = (
        f"https://graph.microsoft.com/v1.0/drives/{urllib.parse.quote(drive_id)}"
        f"/root:/{_encode_graph_path(target_path)}:/createUploadSession"
    )
    session_req = urllib.request.Request(
        session_url,
        data=json.dumps({"item": {"@microsoft.graph.conflictBehavior": "replace"}}).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    session_resp = _json_request(session_req, timeout_sec=timeout_sec)
    upload_url = str(session_resp.get("uploadUrl", "")).strip()
    if not upload_url:
        raise RuntimeError("OneDrive upload session URL manquante.")

    total_size = int(local_file.stat().st_size)
    uploaded = 0
    with local_file.open("rb") as f:
        while uploaded < total_size:
            remaining = total_size - uploaded
            this_size = min(int(chunk_size), remaining)
            chunk = f.read(this_size)
            if not chunk:
                break
            end = uploaded + len(chunk) - 1
            req = urllib.request.Request(
                upload_url,
                data=chunk,
                method="PUT",
                headers={
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {uploaded}-{end}/{total_size}",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                payload = resp.read()
            uploaded = end + 1
            if uploaded >= total_size:
                final = json.loads(payload.decode("utf-8")) if payload else {}
                return {
                    "status": "UPLOADED",
                    "mode": "chunked",
                    "uploaded_bytes": total_size,
                    "target_path": target_path,
                    "item_id": str(final.get("id", "")),
                    "web_url": str(final.get("webUrl", "")),
                }
    raise RuntimeError("Upload chunked interrompu avant completion.")


def upload_delivery_package(
    local_file: Path | str,
    *,
    target_filename: str | None = None,
    target_dir: str | None = None,
    timeout_sec: int = 60,
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
) -> dict[str, Any]:
    file_path = Path(local_file)
    if not file_path.exists():
        return {"status": "FAILED", "error": f"Fichier introuvable: {file_path}"}

    if not onedrive_is_configured():
        return {
            "status": "SKIPPED_CONFIG",
            "message": "Variables OneDrive absentes; upload ignore.",
        }

    drive_id = _env("ONEDRIVE_DRIVE_ID")
    filename = str(target_filename).strip() if str(target_filename or "").strip() else file_path.name
    folder = str(target_dir or _env("ONEDRIVE_TARGET_DIR") or DEFAULT_TARGET_DIR).strip().strip("/")
    target_path = f"{folder}/{filename}" if folder else filename

    try:
        token = _graph_token(timeout_sec=timeout_sec)
        if not token:
            return {"status": "FAILED", "error": "Token OneDrive vide."}
        file_size = int(file_path.stat().st_size)
        if file_size <= _CHUNK_THRESHOLD:
            return _upload_simple(token, drive_id, target_path, file_path, timeout_sec)
        return _upload_chunked(
            token=token,
            drive_id=drive_id,
            target_path=target_path,
            local_file=file_path,
            timeout_sec=timeout_sec,
            chunk_size=max(int(chunk_size), 1024 * 1024),
        )
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="ignore")
        except Exception:
            body = ""
        return {"status": "FAILED", "error": f"HTTP {exc.code} {exc.reason}", "body": body}
    except Exception as exc:
        return {"status": "FAILED", "error": str(exc)}

