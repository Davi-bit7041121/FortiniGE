"""Renderizador 3D por software para PyEngine3D."""

from __future__ import annotations
from typing import List, Tuple
from PyQt6.QtGui import QImage, QColor
from engine.renderer.camera import Camera
from engine.renderer.mesh import Mesh
from engine.renderer.rasterizer import Rasterizer
from engine.core.math3d import Vec3, Mat4


class DirectionalLight:
    def __init__(self, direction: Vec3 = Vec3(0.0, -1.0, -1.0), color: Vec3 = Vec3(1.0, 1.0, 1.0), intensity: float = 1.0) -> None:
        self.direction = direction.normalize()
        self.color = color
        self.intensity = intensity


class Renderer:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.rasterizer = Rasterizer(width, height)
        self.ambient_color = Vec3(0.1, 0.1, 0.1)
        self.directional_light = DirectionalLight()

    def _compute_color(self, normal: Vec3) -> QColor:
        ndir = self.directional_light.direction * -1.0
        diff = max(0.0, normal.normalize().dot(ndir))
        r = min(1.0, self.ambient_color.x + diff * self.directional_light.color.x * self.directional_light.intensity)
        g = min(1.0, self.ambient_color.y + diff * self.directional_light.color.y * self.directional_light.intensity)
        b = min(1.0, self.ambient_color.z + diff * self.directional_light.color.z * self.directional_light.intensity)
        return QColor(int(r * 255), int(g * 255), int(b * 255))

    def render_mesh(self, image: QImage, mesh: Mesh, model_matrix: Mat4, camera: Camera) -> None:
        view = camera.get_view_matrix()
        proj = camera.get_projection_matrix(image.width() / image.height())
        mvp = proj.multiply(view).multiply(model_matrix)

        for idx in mesh.indices:
            v0 = mesh.vertices[idx[0]]
            v1 = mesh.vertices[idx[1]]
            v2 = mesh.vertices[idx[2]]
            n0 = mesh.normals[idx[0]] if idx[0] < len(mesh.normals) else Vec3(0, 1, 0)
            n1 = mesh.normals[idx[1]] if idx[1] < len(mesh.normals) else Vec3(0, 1, 0)
            n2 = mesh.normals[idx[2]] if idx[2] < len(mesh.normals) else Vec3(0, 1, 0)

            def project(v: Vec3):
                x = v.x * mvp.m[0][0] + v.y * mvp.m[0][1] + v.z * mvp.m[0][2] + mvp.m[0][3]
                y = v.x * mvp.m[1][0] + v.y * mvp.m[1][1] + v.z * mvp.m[1][2] + mvp.m[1][3]
                z = v.x * mvp.m[2][0] + v.y * mvp.m[2][1] + v.z * mvp.m[2][2] + mvp.m[2][3]
                w = v.x * mvp.m[3][0] + v.y * mvp.m[3][1] + v.z * mvp.m[3][2] + mvp.m[3][3]
                return (x, y, z, w)

            c0 = project(v0)
            c1 = project(v1)
            c2 = project(v2)

            if c0[3] == 0 or c1[3] == 0 or c2[3] == 0:
                continue

            if c0[3] < 0 or c1[3] < 0 or c2[3] < 0:
                continue

            ndc0 = (c0[0]/c0[3], c0[1]/c0[3], c0[2]/c0[3])
            ndc1 = (c1[0]/c1[3], c1[1]/c1[3], c1[2]/c1[3])
            ndc2 = (c2[0]/c2[3], c2[1]/c2[3], c2[2]/c2[3])

            if any(abs(v) > 1.5 for v in ndc0 + ndc1 + ndc2):
                continue

            s0 = self.rasterizer.ndc_to_screen(ndc0[0], ndc0[1], image.width(), image.height())
            s1 = self.rasterizer.ndc_to_screen(ndc1[0], ndc1[1], image.width(), image.height())
            s2 = self.rasterizer.ndc_to_screen(ndc2[0], ndc2[1], image.width(), image.height())

            edge1 = Vec3(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
            edge2 = Vec3(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
            face_normal = edge1.cross(edge2).normalize()
            if face_normal.dot(Vec3(0, 0, -1)) >= 0:
                continue

            self.rasterizer.rasterize_triangle(
                image,
                (s0[0], s0[1], ndc0[2]),
                (s1[0], s1[1], ndc1[2]),
                (s2[0], s2[1], ndc2[2]),
                self._compute_color(n0),
                self._compute_color(n1),
                self._compute_color(n2),
            )

    def render(self, meshes: List[Tuple[Mesh, Mat4]], camera: Camera) -> QImage:
        image = QImage(self.width, self.height, QImage.Format.Format_RGB32)
        image.fill(QColor(15, 15, 40))
        self.rasterizer.width = self.width
        self.rasterizer.height = self.height
        self.rasterizer.clear()

        for mesh, model_matrix in meshes:
            self.render_mesh(image, mesh, model_matrix, camera)

        return image
