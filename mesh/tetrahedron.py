from copy import copy
from dataclasses import dataclass
from itertools import combinations

from mesh.point3d import Point3D
from mesh.triangle3d import Triangle3D


@dataclass(slots=True)
class Tetrahedron:
    points: list[Point3D]
    material_number: int = 1

    def __repr__(self):
        return f'Tetrahedron([{", ".join(map(repr, self.points))}], {self.material_number})'

    def __hash__(self):
        return hash(repr(self))

    def __copy__(self):
        return Tetrahedron([copy(point) for point in self.points], self.material_number)

    @classmethod
    def from_triangles(cls, *triangles: Triangle3D):
        points = set()
        for triangle in triangles:
            points |= set(triangle.points)
        return cls(*points)

    @property
    def triangles(self) -> list[Triangle3D]:
        triangles: list[Triangle3D] = []
        for cur_triangle_points in combinations(self.points, 3):
            triangles.append(Triangle3D(*cur_triangle_points))
        return triangles
