from itertools import chain

from mesh.point3d import Point3D
from mesh.triangle3d import Triangle3D


class FaceMesh:
    __slots__ = ('triangles',)
    triangles: list[Triangle3D]

    @classmethod
    def from_file(cls, path: str):
        with open(path) as f:
            lines = f.readlines()

        points_numbers_start = lines.index('surfaceelements\n') + 1
        points_numbers = [
            tuple(map(int, i.split()[~2:])) for i in
            lines[points_numbers_start + 1: points_numbers_start + int(lines[points_numbers_start]) + 1]
        ]

        points_start = lines.index('points\n') + 1
        points = [
            tuple(map(float, line.split())) for line in
            lines[points_start + 1: points_start + int(lines[points_start]) + 1]
        ]

        del lines

        face_mesh = cls()
        face_mesh.triangles = []
        for n1, n2, n3 in points_numbers:
            face_mesh.triangles.append(
                Triangle3D(
                    Point3D(*points[n1 - 1]),
                    Point3D(*points[n2 - 1]),
                    Point3D(*points[n3 - 1])
                )
            )
        return face_mesh

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

