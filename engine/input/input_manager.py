"""Gerenciamento de input teclado/mouse para PyEngine3D."""

from __future__ import annotations
from typing import Dict, Tuple


class InputManager:
    keys: Dict[str, bool] = {}
    keys_down: Dict[str, bool] = {}
    keys_up: Dict[str, bool] = {}
    mouse_pos: Tuple[int, int] = (0, 0)
    mouse_delta: Tuple[int, int] = (0, 0)
    mouse_buttons: Dict[int, bool] = {}

    @classmethod
    def key_down(cls, key: str) -> None:
        cls.keys[key] = True
        cls.keys_down[key] = True

    @classmethod
    def key_up(cls, key: str) -> None:
        cls.keys[key] = False
        cls.keys_up[key] = True

    @classmethod
    def update(cls) -> None:
        cls.keys_down.clear()
        cls.keys_up.clear()

    @classmethod
    def get_axis(cls, name: str) -> float:
        if name == "Horizontal":
            return float(cls.keys.get("D", False)) - float(cls.keys.get("A", False))
        if name == "Vertical":
            return float(cls.keys.get("W", False)) - float(cls.keys.get("S", False))
        return 0.0
