from itertools import combinations

from mesh.point3d import Point3D
from mesh.triangle3d import Triangle3D


class Tetrahedron:
    points: list[Point3D]

    def __init__(self, *points: Point3D):
        self.points = list(points)

    def __repr__(self):
        return f'Tetrahedron({", ".join(map(repr, self.points))})'

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
