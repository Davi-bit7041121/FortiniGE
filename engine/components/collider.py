"""Colisores AABB e esfera para PyEngine3D."""

from __future__ import annotations
from engine.core.game_object import Component, GameObject
from engine.core.math3d import Vec3


class Collider(Component):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(game_object)
        self.is_trigger = False

    def overlaps(self, other: Collider) -> bool:
        raise NotImplementedError


class BoxCollider(Collider):
    def __init__(self, game_object: GameObject, center: Vec3 = Vec3(0, 0, 0), size: Vec3 = Vec3(1, 1, 1)) -> None:
        super().__init__(game_object)
        self.center = center
        self.size = size

    def get_min(self) -> Vec3:
        return self.center - self.size * 0.5

    def get_max(self) -> Vec3:
        return self.center + self.size * 0.5

    def overlaps(self, other: Collider) -> bool:
        if not isinstance(other, BoxCollider):
            return False
        a_min = self.get_min(); a_max = self.get_max()
        b_min = other.get_min(); b_max = other.get_max()
        return (a_min.x <= b_max.x and a_max.x >= b_min.x and
                a_min.y <= b_max.y and a_max.y >= b_min.y and
                a_min.z <= b_max.z and a_max.z >= b_min.z)


class SphereCollider(Collider):
    def __init__(self, game_object: GameObject, center: Vec3 = Vec3(0, 0, 0), radius: float = 0.5) -> None:
        super().__init__(game_object)
        self.center = center
        self.radius = radius

    def overlaps(self, other: Collider) -> bool:
        if not isinstance(other, SphereCollider):
            return False
        delta = self.center - other.center
        dist2 = delta.dot(delta)
        r = self.radius + other.radius
        return dist2 <= r * r
