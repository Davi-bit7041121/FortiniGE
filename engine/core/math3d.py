"""Módulo de matemática 3D para PyEngine3D.
Contém operações vetoriais, matriciais e quaternions sem dependências externas.
"""

from __future__ import annotations
import math
from typing import List, Optional


class Vec2:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vec2:
        return Vec2(self.x / scalar, self.y / scalar)

    def dot(self, other: Vec2) -> float:
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def normalize(self) -> Vec2:
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return self / l

    def __repr__(self) -> str:
        return f"Vec2({self.x:.3f}, {self.y:.3f})"


class Vec3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vec3:
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> Vec3:
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def normalize(self) -> Vec3:
        l = self.length()
        if l == 0:
            return Vec3(0, 0, 0)
        return self / l

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]

    def __repr__(self) -> str:
        return f"Vec3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Vec4:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def to_vec3(self) -> Vec3:
        if self.w == 0:
            return Vec3(self.x, self.y, self.z)
        return Vec3(self.x / self.w, self.y / self.w, self.z / self.w)

    def __repr__(self) -> str:
        return f"Vec4({self.x:.3f}, {self.y:.3f}, {self.z:.3f}, {self.w:.3f})"


class Mat4:
    def __init__(self, m: Optional[List[List[float]]] = None) -> None:
        if m is None:
            self.m = [[0.0] * 4 for _ in range(4)]
        else:
            self.m = [[float(col) for col in row] for row in m]

    @staticmethod
    def identity() -> Mat4:
        return Mat4([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def translate(v: Vec3) -> Mat4:
        m = Mat4.identity()
        m.m[0][3] = v.x
        m.m[1][3] = v.y
        m.m[2][3] = v.z
        return m

    @staticmethod
    def scale(v: Vec3) -> Mat4:
        m = Mat4.identity()
        m.m[0][0] = v.x
        m.m[1][1] = v.y
        m.m[2][2] = v.z
        return m

    @staticmethod
    def rotate_x(angle: float) -> Mat4:
        c = math.cos(angle)
        s = math.sin(angle)
        return Mat4([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c, -s, 0.0],
            [0.0, s, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def rotate_y(angle: float) -> Mat4:
        c = math.cos(angle)
        s = math.sin(angle)
        return Mat4([
            [c, 0.0, s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def rotate_z(angle: float) -> Mat4:
        c = math.cos(angle)
        s = math.sin(angle)
        return Mat4([
            [c, -s, 0.0, 0.0],
            [s, c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def perspective(fov: float, aspect: float, near: float, far: float) -> Mat4:
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        q = far / (far - near)
        m = Mat4()
        m.m[0][0] = f / aspect
        m.m[1][1] = f
        m.m[2][2] = q
        m.m[2][3] = -near * q
        m.m[3][2] = 1.0
        m.m[3][3] = 0.0
        return m

    @staticmethod
    def look_at(eye: Vec3, center: Vec3, up: Vec3) -> Mat4:
        z = (eye - center).normalize()
        x = up.cross(z).normalize()
        y = z.cross(x)

        m = Mat4.identity()
        m.m[0][0] = x.x
        m.m[0][1] = x.y
        m.m[0][2] = x.z
        m.m[0][3] = -x.dot(eye)

        m.m[1][0] = y.x
        m.m[1][1] = y.y
        m.m[1][2] = y.z
        m.m[1][3] = -y.dot(eye)

        m.m[2][0] = z.x
        m.m[2][1] = z.y
        m.m[2][2] = z.z
        m.m[2][3] = -z.dot(eye)

        return m

    def multiply(self, other: Mat4) -> Mat4:
        result = Mat4()
        for i in range(4):
            for j in range(4):
                result.m[i][j] = sum(self.m[i][k] * other.m[k][j] for k in range(4))
        return result

    def transform_point(self, v: Vec3) -> Vec3:
        x = v.x * self.m[0][0] + v.y * self.m[0][1] + v.z * self.m[0][2] + self.m[0][3]
        y = v.x * self.m[1][0] + v.y * self.m[1][1] + v.z * self.m[1][2] + self.m[1][3]
        z = v.x * self.m[2][0] + v.y * self.m[2][1] + v.z * self.m[2][2] + self.m[2][3]
        w = v.x * self.m[3][0] + v.y * self.m[3][1] + v.z * self.m[3][2] + self.m[3][3]
        if w != 0 and w != 1:
            return Vec3(x / w, y / w, z / w)
        return Vec3(x, y, z)

    def transform_direction(self, v: Vec3) -> Vec3:
        x = v.x * self.m[0][0] + v.y * self.m[0][1] + v.z * self.m[0][2]
        y = v.x * self.m[1][0] + v.y * self.m[1][1] + v.z * self.m[1][2]
        z = v.x * self.m[2][0] + v.y * self.m[2][1] + v.z * self.m[2][2]
        return Vec3(x, y, z)

    def transpose(self) -> Mat4:
        return Mat4([[self.m[j][i] for j in range(4)] for i in range(4)])

    def inverse(self) -> Mat4:
        # Inversão genérica 4x4 via Gauss-Jordan
        mat = [row[:] for row in self.m]
        inv = Mat4.identity().m

        for i in range(4):
            pivot = mat[i][i]
            if abs(pivot) < 1e-9:
                for j in range(i + 1, 4):
                    if abs(mat[j][i]) > abs(pivot):
                        mat[i], mat[j] = mat[j], mat[i]
                        inv[i], inv[j] = inv[j], inv[i]
                        pivot = mat[i][i]
                        break
            if abs(pivot) < 1e-12:
                raise ValueError("Matriz singular não invertível")
            inv_factor = 1.0 / pivot
            mat[i] = [x * inv_factor for x in mat[i]]
            inv[i] = [x * inv_factor for x in inv[i]]
            for j in range(4):
                if j == i:
                    continue
                factor = mat[j][i]
                mat[j] = [mat[j][k] - factor * mat[i][k] for k in range(4)]
                inv[j] = [inv[j][k] - factor * inv[i][k] for k in range(4)]

        return Mat4(inv)

    def __repr__(self) -> str:
        lines = ["Mat4("]
        for row in self.m:
            lines.append("  [" + ", ".join(f"{v:.3f}" for v in row) + "]")
        lines.append(")")
        return "\n".join(lines)


class Quaternion:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    @staticmethod
    def from_euler(x: float, y: float, z: float) -> Quaternion:
        # ângulos em radianos
        cx = math.cos(x * 0.5)
        sx = math.sin(x * 0.5)
        cy = math.cos(y * 0.5)
        sy = math.sin(y * 0.5)
        cz = math.cos(z * 0.5)
        sz = math.sin(z * 0.5)

        w = cx * cy * cz + sx * sy * sz
        xq = sx * cy * cz - cx * sy * sz
        yq = cx * sy * cz + sx * cy * sz
        zq = cx * cy * sz - sx * sy * cz

        return Quaternion(xq, yq, zq, w).normalize()

    def normalize(self) -> Quaternion:
        mag = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
        if mag == 0:
            return Quaternion(0, 0, 0, 1)
        return Quaternion(self.x / mag, self.y / mag, self.z / mag, self.w / mag)

    def conjugate(self) -> Quaternion:
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def multiply(self, q: Quaternion) -> Quaternion:
        return Quaternion(
            self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y,
            self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x,
            self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.w,
            self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z,
        )

    def to_matrix(self) -> Mat4:
        x2 = self.x + self.x
        y2 = self.y + self.y
        z2 = self.z + self.z
        xx = self.x * x2
        yy = self.y * y2
        zz = self.z * z2
        xy = self.x * y2
        xz = self.x * z2
        yz = self.y * z2
        wx = self.w * x2
        wy = self.w * y2
        wz = self.w * z2

        return Mat4([
            [1 - (yy + zz), xy - wz, xz + wy, 0.0],
            [xy + wz, 1 - (xx + zz), yz - wx, 0.0],
            [xz - wy, yz + wx, 1 - (xx + yy), 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    def rotate_vector(self, v: Vec3) -> Vec3:
        qv = Quaternion(v.x, v.y, v.z, 0)
        result = self.multiply(qv).multiply(self.conjugate())
        return Vec3(result.x, result.y, result.z)

    def slerp(self, q: Quaternion, t: float) -> Quaternion:
        cos_omega = self.x * q.x + self.y * q.y + self.z * q.z + self.w * q.w
        q2 = Quaternion(q.x, q.y, q.z, q.w)
        if cos_omega < 0.0:
            cos_omega = -cos_omega
            q2 = Quaternion(-q2.x, -q2.y, -q2.z, -q2.w)

        if cos_omega > 0.9995:
            # Lerp quando ângulo pequeno
            x = self.x + t * (q2.x - self.x)
            y = self.y + t * (q2.y - self.y)
            z = self.z + t * (q2.z - self.z)
            w = self.w + t * (q2.w - self.w)
            return Quaternion(x, y, z, w).normalize()

        omega = math.acos(cos_omega)
        sin_omega = math.sin(omega)

        a = math.sin((1.0 - t) * omega) / sin_omega
        b = math.sin(t * omega) / sin_omega

        return Quaternion(
            self.x * a + q2.x * b,
            self.y * a + q2.y * b,
            self.z * a + q2.z * b,
            self.w * a + q2.w * b,
        ).normalize()

    def __repr__(self) -> str:
        return f"Quaternion({self.x:.3f}, {self.y:.3f}, {self.z:.3f}, {self.w:.3f})"
