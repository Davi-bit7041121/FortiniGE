"""Câmera 3D para PyEngine3D, com projeção e modos orbit/free-fly."""

from __future__ import annotations
import math
from typing import Tuple
from engine.core.math3d import Vec3, Mat4, Quaternion


class Camera:
    def __init__(self) -> None:
        self.position = Vec3(0.0, 0.0, 0.0)
        self.rotation = Quaternion(0.0, 0.0, 0.0, 1.0)
        self.fov = 60.0
        self.near = 0.1
        self.far = 1000.0
        self.mode = "orbit"  # "orbit" ou "free"
        self.orbit_distance = 10.0
        self.orbit_pivot = Vec3(0.0, 0.0, 0.0)
        self.orbit_angles = Vec3(0.0, 0.0, 0.0)

    def get_view_matrix(self) -> Mat4:
        if self.mode == "orbit":
            yaw = self.orbit_angles.y
            pitch = self.orbit_angles.x
            r_yaw = Mat4.rotate_y(yaw)
            r_pitch = Mat4.rotate_x(pitch)
            rot = r_yaw.multiply(r_pitch)
            offset = Vec3(0.0, 0.0, self.orbit_distance)
            cam_dir = rot.transform_direction(offset)
            self.position = self.orbit_pivot + cam_dir
            return Mat4.look_at(self.position, self.orbit_pivot, Vec3(0.0, 1.0, 0.0))
        else:
            target = self.position + self.rotation.rotate_vector(Vec3(0, 0, 1))
            return Mat4.look_at(self.position, target, Vec3(0.0, 1.0, 0.0))

    def get_projection_matrix(self, aspect: float) -> Mat4:
        return Mat4.perspective(self.fov, aspect, self.near, self.far)

    def set_position(self, pos: Vec3) -> None:
        self.position = pos

    def set_rotation_euler(self, pitch: float, yaw: float, roll: float = 0.0) -> None:
        self.rotation = Quaternion.from_euler(math.radians(pitch), math.radians(yaw), math.radians(roll))

    def orbit(self, delta_yaw: float, delta_pitch: float) -> None:
        self.orbit_angles.y += delta_yaw
        self.orbit_angles.x = max(-math.pi / 2 + 0.01, min(math.pi / 2 - 0.01, self.orbit_angles.x + delta_pitch))

    def pan(self, dx: float, dy: float) -> None:
        right = self.rotation.rotate_vector(Vec3(1, 0, 0))
        up = self.rotation.rotate_vector(Vec3(0, 1, 0))
        self.orbit_pivot += (right * dx) + (up * dy)

    def zoom(self, delta: float) -> None:
        self.orbit_distance = max(0.5, self.orbit_distance + delta)

    def world_to_view(self, point: Vec3) -> Vec3:
        view = self.get_view_matrix()
        return view.transform_point(point)
