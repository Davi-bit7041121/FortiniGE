"""Mesh de geometria para a renderização por software."""

from __future__ import annotations
from typing import List, Optional, Tuple
from engine.core.math3d import Vec3


class Mesh:
    def __init__(
        self,
        vertices: List[Vec3],
        normals: Optional[List[Vec3]] = None,
        uvs: Optional[List[Tuple[float, float]]] = None,
        indices: Optional[List[Tuple[int, int, int]]] = None,
    ) -> None:
        self.vertices = vertices
        self.normals = normals if normals is not None else [Vec3(0, 1, 0) for _ in vertices]
        self.uvs = uvs if uvs is not None else [(0.0, 0.0) for _ in vertices]
        self.indices = indices if indices is not None else [(i, i + 1, i + 2) for i in range(0, len(vertices), 3)]
