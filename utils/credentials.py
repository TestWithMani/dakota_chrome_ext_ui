"""Load Dakota portal credentials from environment or credentials.env."""

import os
from pathlib import Path

from pages.dakota_auth import DakotaCredentials

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_dakota_credentials() -> DakotaCredentials:
    creds_file = PROJECT_ROOT / "credentials.env"
    if creds_file.exists():
        for line in creds_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

    username = os.environ.get("DAKOTA_USERNAME", "").strip()
    password = os.environ.get("DAKOTA_PASSWORD", "").strip()
    if not username or not password:
        raise RuntimeError(
            "Dakota credentials not found. Set DAKOTA_USERNAME and DAKOTA_PASSWORD "
            "environment variables or create credentials.env from credentials.env.example."
        )
    return DakotaCredentials(username=username, password=password)
