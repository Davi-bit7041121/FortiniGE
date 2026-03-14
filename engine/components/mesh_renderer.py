"""Componente MeshRenderer para objetos renderizáveis."""

from __future__ import annotations
from engine.core.game_object import Component, GameObject
from engine.renderer.mesh import Mesh
from engine.core.math3d import Mat4


class MeshRenderer(Component):
    def __init__(self, game_object: GameObject, mesh: Mesh) -> None:
        super().__init__(game_object)
        self.mesh = mesh
        self.material_color = (1.0, 1.0, 1.0)
        self.cast_shadows = True
        self.receive_shadows = True

    def get_model_matrix(self) -> Mat4:
        transform = self.game_object.get_component(Transform)
        if transform:
            return transform.get_world_matrix()
        return Mat4.identity()
