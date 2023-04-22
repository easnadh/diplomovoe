from dataclasses import dataclass
from itertools import chain

from mesh.triangle3d import Triangle3D


@dataclass(slots=True)
class FaceMesh:
    triangles: list[Triangle3D] = None

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
