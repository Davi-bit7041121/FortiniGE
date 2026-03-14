"""Rasterizador 3D com z-buffer e interpolação baricêntrica."""

from __future__ import annotations
from typing import Tuple
from PyQt6.QtGui import QColor, QImage
from engine.core.math3d import Vec3


class Rasterizer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.z_buffer = [[float('inf')] * width for _ in range(height)]

    def clear(self) -> None:
        for y in range(self.height):
            self.z_buffer[y] = [float('inf')] * self.width

    @staticmethod
    def ndc_to_screen(x: float, y: float, width: int, height: int) -> Tuple[int, int]:
        sx = int((x * 0.5 + 0.5) * (width - 1))
        sy = int((1.0 - (y * 0.5 + 0.5)) * (height - 1))
        return sx, sy

    @staticmethod
    def edge_function(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> int:
        return (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])

    def rasterize_triangle(
        self,
        image: QImage,
        p0: Tuple[int, int, float],
        p1: Tuple[int, int, float],
        p2: Tuple[int, int, float],
        c0: QColor,
        c1: QColor,
        c2: QColor,
    ) -> None:
        x0, y0, z0 = p0
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        min_x = max(0, min(x0, x1, x2))
        max_x = min(self.width - 1, max(x0, x1, x2))
        min_y = max(0, min(y0, y1, y2))
        max_y = min(self.height - 1, max(y0, y1, y2))

        area = self.edge_function((x0, y0), (x1, y1), (x2, y2))
        if area == 0:
            return

        for py in range(min_y, max_y + 1):
            for px in range(min_x, max_x + 1):
                w0 = self.edge_function((x1, y1), (x2, y2), (px, py))
                w1 = self.edge_function((x2, y2), (x0, y0), (px, py))
                w2 = self.edge_function((x0, y0), (x1, y1), (px, py))
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    alpha = w0 / area
                    beta = w1 / area
                    gamma = w2 / area
                    z = alpha * z0 + beta * z1 + gamma * z2
                    if z < self.z_buffer[py][px]:
                        self.z_buffer[py][px] = z
                        r = int(alpha * c0.red() + beta * c1.red() + gamma * c2.red())
                        g = int(alpha * c0.green() + beta * c1.green() + gamma * c2.green())
                        b = int(alpha * c0.blue() + beta * c1.blue() + gamma * c2.blue())
                        image.setPixelColor(px, py, QColor(r, g, b))
