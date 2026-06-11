import os
import time

import pyautogui

from utils.session_calibration import load_dakota_icon_position

# Calibrated on a maximized 1920x1080 display at 100% Windows scaling.
_DEFAULT_EXTENSION_MENU_RIGHT_OFFSET = 728
_DEFAULT_TOOLBAR_Y = 52
_DEFAULT_DAKOTA_ICON_LEFT_OF_MENU = 66
_DEFAULT_PIN_OFFSET_FROM_MENU = (-44, 146)


def _env_int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def get_extension_menu_position() -> tuple[int, int]:
    """Puzzle-piece extensions menu icon in the Chrome toolbar."""
    if os.getenv("EXTENSION_MENU_ICON_X") and os.getenv("EXTENSION_MENU_ICON_Y"):
        return (
            _env_int("EXTENSION_MENU_ICON_X", 0),
            _env_int("EXTENSION_MENU_ICON_Y", 0),
        )

    screen_width, _ = pyautogui.size()
    right_offset = _env_int(
        "EXTENSION_MENU_RIGHT_OFFSET",
        _DEFAULT_EXTENSION_MENU_RIGHT_OFFSET,
    )
    toolbar_y = _env_int("CHROME_TOOLBAR_Y", _DEFAULT_TOOLBAR_Y)
    return (screen_width - right_offset, toolbar_y)


def get_dakota_extension_icon_position() -> tuple[int, int]:
    """Pinned Dakota extension icon immediately left of the extensions menu."""
    if os.getenv("CHROME_DAKOTA_EXTENSION_ICON_X") and os.getenv(
        "CHROME_DAKOTA_EXTENSION_ICON_Y"
    ):
        return (
            _env_int("CHROME_DAKOTA_EXTENSION_ICON_X", 0),
            _env_int("CHROME_DAKOTA_EXTENSION_ICON_Y", 0),
        )

    calibrated = load_dakota_icon_position()
    if calibrated:
        return calibrated

    menu_x, menu_y = get_extension_menu_position()
    left_offset = _env_int(
        "DAKOTA_ICON_LEFT_OF_MENU",
        _DEFAULT_DAKOTA_ICON_LEFT_OF_MENU,
    )
    return (menu_x - left_offset, menu_y)


def get_dakota_pin_icon_position() -> tuple[int, int]:
    """Pin icon inside the extensions dropdown menu."""
    if os.getenv("DAKOTA_PIN_ICON_X") and os.getenv("DAKOTA_PIN_ICON_Y"):
        return (
            _env_int("DAKOTA_PIN_ICON_X", 0),
            _env_int("DAKOTA_PIN_ICON_Y", 0),
        )

    menu_x, menu_y = get_extension_menu_position()
    offset_x = _env_int("DAKOTA_PIN_OFFSET_X", _DEFAULT_PIN_OFFSET_FROM_MENU[0])
    offset_y = _env_int("DAKOTA_PIN_OFFSET_Y", _DEFAULT_PIN_OFFSET_FROM_MENU[1])
    return (menu_x + offset_x, menu_y + offset_y)


def get_dakota_icon_click_candidates() -> list[tuple[int, int]]:
    """Ordered click positions to try when opening the Dakota toolbar icon."""
    base = get_dakota_extension_icon_position()
    x_offsets = (0, -16, -32, 16, -48, -64, 32, -80, 48, -96)
    y_offsets = (0, 8, 16, -8, 24, 32)

    candidates: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for dx in x_offsets:
        for dy in y_offsets:
            position = (base[0] + dx, base[1] + dy)
            if position not in seen:
                seen.add(position)
                candidates.append(position)
    return candidates


def native_left_click(position: tuple[int, int]) -> None:
    x, y = position
    pyautogui.moveTo(x, y, duration=0.15)
    time.sleep(0.2)
    pyautogui.click(x=x, y=y, button="left")
