"""
Download the Dakota Marketplace Chrome extension (.crx) from the Chrome Web Store.

Run before tests if the extension folder is missing:
    python download_extension.py
"""

import io
import zipfile
from pathlib import Path

import requests

EXTENSION_ID = "pkjcjmhoaajnghcgbkkdfgakcbdnpefj"
EXTENSION_NAME = "Dakota Marketplace"

PROJECT_ROOT = Path(__file__).resolve().parent
EXTENSIONS_DIR = PROJECT_ROOT / "extensions"
CRX_FILE = EXTENSIONS_DIR / "dakota.crx"
UNPACKED_DIR = EXTENSIONS_DIR / "dakota"

DOWNLOAD_URL = (
    "https://clients2.google.com/service/update2/crx?"
    "response=redirect&prodversion=149.0"
    "&acceptformat=crx2,crx3"
    f"&x=id%3D{EXTENSION_ID}%26installsource%3Dondemand%26uc"
)


def _find_zip_start(crx_bytes: bytes) -> int:
    zip_start = crx_bytes.find(b"PK\x03\x04")
    if zip_start == -1:
        raise ValueError("Downloaded file does not look like a valid .crx.")
    return zip_start


def unpack_crx(crx_path: Path, destination: Path) -> None:
    crx_bytes = crx_path.read_bytes()
    zip_start = _find_zip_start(crx_bytes)

    if destination.exists():
        import shutil

        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(crx_bytes[zip_start:])) as archive:
        archive.extractall(destination)


def download_extension() -> Path:
    EXTENSIONS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading '{EXTENSION_NAME}' (ID: {EXTENSION_ID})...")
    response = requests.get(DOWNLOAD_URL, timeout=60)
    response.raise_for_status()

    if len(response.content) < 100:
        raise RuntimeError("Extension download failed — file too small.")

    CRX_FILE.write_bytes(response.content)
    print(f"Saved .crx file to: {CRX_FILE}")

    unpack_crx(CRX_FILE, UNPACKED_DIR)
    print(f"Unpacked extension to: {UNPACKED_DIR}")
    return UNPACKED_DIR


if __name__ == "__main__":
    download_extension()
    print("Extension downloaded and unpacked successfully.")
