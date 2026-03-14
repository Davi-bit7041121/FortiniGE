"""Componente Transform para GameObjects em PyEngine3D."""

from __future__ import annotations
from engine.core.math3d import Vec3, Quaternion, Mat4
from engine.core.game_object import GameObject, Component


class Transform(Component):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(game_object)
        self.position = Vec3(0.0, 0.0, 0.0)
        self.rotation = Quaternion(0.0, 0.0, 0.0, 1.0)
        self.scale = Vec3(1.0, 1.0, 1.0)

    def get_world_matrix(self) -> Mat4:
        translate = Mat4.translate(self.position)
        rotate = self.rotation.to_matrix()
        scale = Mat4.scale(self.scale)
        local = translate.multiply(rotate).multiply(scale)

        if self.game_object.parent is not None:
            parent_transform = self.game_object.parent.get_component(Transform)
            if parent_transform:
                parent_matrix = parent_transform.get_world_matrix()
                return parent_matrix.multiply(local)

        return local

    @property
    def forward(self) -> Vec3:
        return self.rotation.rotate_vector(Vec3(0, 0, 1))

    @property
    def right(self) -> Vec3:
        return self.rotation.rotate_vector(Vec3(1, 0, 0))

    @property
    def up(self) -> Vec3:
        return self.rotation.rotate_vector(Vec3(0, 1, 0))
