"""Quick preflight checks before running Dakota UI tests."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

from download_extension import UNPACKED_DIR, download_extension

PROJECT_ROOT = Path(__file__).resolve().parent
PORTAL_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/"
EXTENSION_DOWNLOAD_HOST = "https://clients2.google.com"


def _read_credentials_file() -> tuple[str, str]:
    creds_file = PROJECT_ROOT / "credentials.env"
    if not creds_file.exists():
        return "", ""

    username = ""
    password = ""
    for line in creds_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key == "DAKOTA_USERNAME":
            username = value
        elif key == "DAKOTA_PASSWORD":
            password = value
    return username, password


def _check_python() -> bool:
    ok = sys.version_info >= (3, 10)
    version = ".".join(str(v) for v in sys.version_info[:3])
    print(f"[{'OK' if ok else 'FAIL'}] Python version: {version} (requires 3.10+)")
    return ok


def _check_credentials() -> bool:
    env_user = os.environ.get("DAKOTA_USERNAME", "").strip()
    env_pass = os.environ.get("DAKOTA_PASSWORD", "").strip()
    file_user, file_pass = _read_credentials_file()

    username = env_user or file_user
    password = env_pass or file_pass
    ok = bool(username and password)
    source = "env vars" if env_user and env_pass else "credentials.env"
    if ok:
        masked = f"{username[:2]}***{username[-4:]}" if len(username) > 6 else "***"
        print(f"[OK] Credentials found ({source}): {masked}")
    else:
        print("[FAIL] Credentials missing. Set DAKOTA_USERNAME/DAKOTA_PASSWORD or create credentials.env.")
    return ok


def _check_extension(download_if_missing: bool) -> bool:
    manifest = UNPACKED_DIR / "manifest.json"
    if manifest.exists():
        print(f"[OK] Extension manifest found: {manifest}")
        return True

    if not download_if_missing:
        print(f"[FAIL] Extension missing: {manifest}")
        print("       Run: python download_extension.py")
        return False

    print("[INFO] Extension missing; downloading now...")
    try:
        download_extension()
    except Exception as exc:  # pragma: no cover - network/runtime dependent
        print(f"[FAIL] Extension download failed: {exc}")
        return False

    ok = manifest.exists()
    print(f"[{'OK' if ok else 'FAIL'}] Extension download verification")
    return ok


def _check_url(url: str, label: str) -> bool:
    try:
        response = requests.get(url, timeout=20, allow_redirects=True)
        ok = response.status_code < 500
    except Exception as exc:  # pragma: no cover - network/runtime dependent
        print(f"[FAIL] {label} unreachable: {exc}")
        return False
    print(f"[{'OK' if ok else 'FAIL'}] {label} reachable (status {response.status_code})")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local preflight checks for Dakota UI tests.")
    parser.add_argument(
        "--download-extension",
        action="store_true",
        help="Download extension automatically if missing.",
    )
    args = parser.parse_args()

    checks = [
        _check_python(),
        _check_credentials(),
        _check_extension(download_if_missing=args.download_extension),
        _check_url(PORTAL_URL, "Dakota portal"),
        _check_url(EXTENSION_DOWNLOAD_HOST, "Chrome extension host"),
    ]
    if all(checks):
        print("\nPreflight passed. Safe to run pytest.")
        return 0

    print("\nPreflight failed. Fix items above, then rerun preflight.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
