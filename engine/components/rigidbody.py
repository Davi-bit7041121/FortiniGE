"""Rigidbody simples com integração e gravidade."""

from __future__ import annotations
from engine.core.game_object import Component, GameObject
from engine.core.math3d import Vec3
from engine.core.transform import Transform


class Rigidbody(Component):
    def __init__(self, game_object: GameObject, mass: float = 1.0, use_gravity: bool = True) -> None:
        super().__init__(game_object)
        self.mass = mass
        self.velocity = Vec3(0.0, 0.0, 0.0)
        self.angular_velocity = Vec3(0.0, 0.0, 0.0)
        self.use_gravity = use_gravity

    def apply_force(self, force: Vec3) -> None:
        acceleration = force / self.mass
        self.velocity += acceleration

    def apply_torque(self, torque: Vec3) -> None:
        self.angular_velocity += torque / self.mass

    def fixed_update(self, dt: float) -> None:
        if self.use_gravity:
            self.velocity += Vec3(0, -9.81, 0) * dt

        transform = self.game_object.get_component(Transform)
        if transform:
            transform.position += self.velocity * dt
