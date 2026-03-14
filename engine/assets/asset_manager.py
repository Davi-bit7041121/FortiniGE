"""Gerenciamento de assets: .obj, texturas, primitivos"""

from __future__ import annotations
from typing import Tuple, List
from engine.renderer.mesh import Mesh
from engine.core.math3d import Vec3
from PyQt6.QtGui import QImage


class AssetManager:
    @staticmethod
    def load_obj(path: str) -> Mesh:
        verts: List[Vec3] = []
        normals: List[Vec3] = []
        uvs: List[Tuple[float, float]] = []
        faces=[]

        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                if parts[0] == 'v':
                    verts.append(Vec3(float(parts[1]), float(parts[2]), float(parts[3])))
                if parts[0] == 'vn':
                    normals.append(Vec3(float(parts[1]), float(parts[2]), float(parts[3])))
                if parts[0] == 'vt':
                    uvs.append((float(parts[1]), float(parts[2])))
                if parts[0] == 'f':
                    idx = [p.split('/') for p in parts[1:4]]
                    fi = tuple(int(i[0]) - 1 for i in idx)
                    faces.append(fi)

        return Mesh(verts, normals if normals else None, uvs if uvs else None, faces)

    @staticmethod
    def load_image(path: str) -> QImage:
        img = QImage(path)
        return img

    @staticmethod
    def create_cube(size: float = 1.0) -> Mesh:
        s = size * 0.5
        verts = [
            Vec3(-s,-s,-s), Vec3(s,-s,-s), Vec3(s,s,-s), Vec3(-s,s,-s),
            Vec3(-s,-s,s), Vec3(s,-s,s), Vec3(s,s,s), Vec3(-s,s,s)
        ]
        faces = [(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(2,6,7),(2,7,3),(1,5,6),(1,6,2),(0,3,7),(0,7,4)]
        normals = [Vec3(0,1,0) for _ in verts]
        return Mesh(verts, normals, None, faces)
