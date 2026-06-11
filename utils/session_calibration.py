import json
import os
import tempfile

_CALIBRATION_PATH = os.path.join(
    tempfile.gettempdir(),
    "dakota-playwright-toolbar-calibration.json",
)


def save_dakota_icon_position(position: tuple[int, int]) -> None:
    with open(_CALIBRATION_PATH, "w", encoding="utf-8") as handle:
        json.dump({"dakota_icon": [int(position[0]), int(position[1])]}, handle)


def load_dakota_icon_position() -> tuple[int, int] | None:
    try:
        with open(_CALIBRATION_PATH, encoding="utf-8") as handle:
            data = json.load(handle)
        x, y = data["dakota_icon"]
        return (int(x), int(y))
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None
