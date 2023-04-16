from itertools import chain
from mesh.triangle3d import Triangle3D


class FaceMesh:
    __slots__ = ('triangles',)
    triangles: list[Triangle3D]

    def __init__(self, triangles: list = None):
        if triangles is None:
            triangles = []
        self.triangles = triangles

    def __str__(self):
        points = list(set(chain(
            *map(lambda x: x.points, self.triangles)
        )))

        triangles_with_numbers = [
            list(map(lambda x: points.index(x) + 1, triangle.points))
            for triangle in self.triangles
        ]
        return (f'FaceMesh(\n'
                f'Уникальных точек: {len(points)}\n'
                f'Точки:\n'
                f'{chr(10).join(map(repr, points))}\n'
                f'Треугольники:\n' +
                chr(10).join(map(lambda x: f"Треугольник ({', '.join(map(str, x))})", triangles_with_numbers)) +
                f'\n)')
