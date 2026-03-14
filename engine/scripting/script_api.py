"""API pública de scripting para jogos PyEngine3D."""

from __future__ import annotations
from typing import Dict, List, Optional
from engine.core.game_object import GameObject
from engine.core.transform import Transform
from engine.core.math3d import Vec3


class Time:
    delta_time: float = 0.016
    time: float = 0.0
    frame_count: int = 0
    time_scale: float = 1.0

    @staticmethod
    def update(dt: float) -> None:
        Time.delta_time = dt * Time.time_scale
        Time.time += Time.delta_time
        Time.frame_count += 1


class Input:
    _keys: Dict[str, bool] = {}
    _keys_down: Dict[str, bool] = {}
    _keys_up: Dict[str, bool] = {}
    mouse_position = (0, 0)
    mouse_delta = (0, 0)
    _mouse_buttons: Dict[int, bool] = {}

    @staticmethod
    def get_key(key: str) -> bool:
        return Input._keys.get(key, False)

    @staticmethod
    def get_key_down(key: str) -> bool:
        return Input._keys_down.get(key, False)

    @staticmethod
    def get_key_up(key: str) -> bool:
        return Input._keys_up.get(key, False)

    @staticmethod
    def get_axis(name: str) -> float:
        if name == "Horizontal":
            return float(Input.get_key("D") or Input.get_key("Right")) - float(Input.get_key("A") or Input.get_key("Left"))
        if name == "Vertical":
            return float(Input.get_key("W") or Input.get_key("Up")) - float(Input.get_key("S") or Input.get_key("Down"))
        return 0.0

    @staticmethod
    def get_mouse_button(n: int) -> bool:
        return Input._mouse_buttons.get(n, False)


class Debug:
    @staticmethod
    def log(msg: str) -> None:
        print(f"[LOG] {msg}")

    @staticmethod
    def warn(msg: str) -> None:
        print(f"[WARN] {msg}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"[ERROR] {msg}")

    @staticmethod
    def draw_ray(origin: Vec3, direction: Vec3, color: str = "green") -> None:
        print(f"[DEBUG] Ray {origin} -> {direction} color={color}")

    @staticmethod
    def draw_sphere(center: Vec3, radius: float, color: str = "red") -> None:
        print(f"[DEBUG] Sphere {center}, r={radius} color={color}")


class SceneManager:
    _active_scene: List[GameObject] = []

    @staticmethod
    def load_scene(root_objects: List[GameObject]) -> None:
        SceneManager._active_scene = root_objects

    @staticmethod
    def get_active_scene() -> List[GameObject]:
        return SceneManager._active_scene


def Instantiate(prefab: GameObject, pos: Vec3 = Vec3(), rot: Vec3 = Vec3()) -> GameObject:
    obj = GameObject(prefab.name)
    transform = obj.get_component(Transform)
    if transform:
        transform.position = pos
    return obj


def Destroy(obj: GameObject, delay: float = 0.0) -> None:
    obj.destroy()


def FindObjectOfType(t: type) -> Optional[GameObject]:
    for obj in SceneManager.get_active_scene():
        if isinstance(obj, t):
            return obj
    return None


def FindObjectsByTag(tag: str) -> List[GameObject]:
    return [obj for obj in SceneManager.get_active_scene() if obj.tag == tag]


class RaycastHit:
    def __init__(self, point: Vec3, normal: Vec3, distance: float, game_object: GameObject) -> None:
        self.point = point
        self.normal = normal
        self.distance = distance
        self.game_object = game_object


class Physics:
    @staticmethod
    def raycast(origin: Vec3, direction: Vec3, max_dist: float) -> Optional[RaycastHit]:
        return None
