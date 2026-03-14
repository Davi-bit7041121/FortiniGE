"""Viewport 3D do editor PyEngine3D, renderiza com pipeline por software."""

from __future__ import annotations
import math
from typing import List, Tuple
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QTimer, Qt, QSize

from engine.renderer.renderer import Renderer
from engine.renderer.camera import Camera
from engine.renderer.mesh import Mesh
from engine.core.math3d import Vec3, Mat4


class Viewport(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.camera = Camera()
        self.renderer = Renderer(800, 600)
        self.last_time = 0.0
        self.animation_angle = 0.0

        # Cenas simples de demonstração
        self.scene: List[Tuple[Mesh, Mat4]] = []
        self._create_demo_scene()

        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def sizeHint(self) -> QSize:
        return QSize(800, 600)

    def _create_demo_scene(self) -> None:
        # cubo básico
        verts = [
            Vec3(-1, -1, -1), Vec3(1, -1, -1), Vec3(1, 1, -1), Vec3(-1, 1, -1),
            Vec3(-1, -1, 1), Vec3(1, -1, 1), Vec3(1, 1, 1), Vec3(-1, 1, 1)
        ]
        faces = [(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(2,6,7),(2,7,3),(1,5,6),(1,6,2),(0,3,7),(0,7,4)]
        normals = [Vec3(0,0,-1) for _ in verts]
        cube_mesh = Mesh(verts, normals, None, faces)

        plane_verts = [
            Vec3(-10, 0, -10), Vec3(10, 0, -10), Vec3(10, 0, 10), Vec3(-10, 0, 10)
        ]
        plane_faces = [(0,1,2),(0,2,3)]
        plane_normals = [Vec3(0,1,0) for _ in plane_verts]
        plane_mesh = Mesh(plane_verts, plane_normals, None, plane_faces)

        self.scene = [
            (plane_mesh, Mat4.translate(Vec3(0, -1.0, 0)).multiply(Mat4.scale(Vec3(1,1,1)))),
            (cube_mesh, Mat4.translate(Vec3(0, 0.5, 0)).multiply(Mat4.scale(Vec3(1,1,1))))
        ]

        self.camera.position = Vec3(5, 5, -10)
        self.camera.orbit_pivot = Vec3(0, 0, 0)
        self.camera.orbit_distance = 15
        self.camera.mode = "orbit"

    def paintEvent(self, event) -> None:
        width = max(1, self.width())
        height = max(1, self.height())
        self.renderer.width = width
        self.renderer.height = height
        self.renderer.z_buffer = [[float('inf')] * width for _ in range(height)]

        # atualiza rotação animada
        self.animation_angle += 0.01
        angle = self.animation_angle
        self.scene[1] = (self.scene[1][0], Mat4.translate(Vec3(0,0.5,0)).multiply(Mat4.rotate_y(angle)))

        image = self.renderer.render(self.scene, self.camera)
        painter = QPainter(self)
        painter.drawImage(0, 0, image)
        painter.end()

    def resizeEvent(self, event) -> None:
        self.update()
