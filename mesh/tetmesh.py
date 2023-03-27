from itertools import chain

from mesh.point3d import Point3D
from mesh.tetrahedron import Tetrahedron


class TetMesh:
    tetrahedrons: list[Tetrahedron]

    # bound_tet: list[int]

    @classmethod
    def from_file(cls, path: str):
        with open(path) as f:
            lines = f.readlines()

        points_numbers_start = lines.index('volumeelements\n') + 1
        points_numbers = [
            tuple(map(int, i.split()[~3:])) for i in
            lines[points_numbers_start + 1: points_numbers_start + int(lines[points_numbers_start]) + 1]
        ]

        points_start = lines.index('points\n') + 1
        points = [
            tuple(map(float, line.split())) for line in
            lines[points_start + 1: points_start + int(lines[points_start]) + 1]
        ]

        del lines

        tet_mesh = cls()
        tet_mesh.tetrahedrons = []
        for n1, n2, n3, n4 in points_numbers:
            tet_mesh.tetrahedrons.append(
                Tetrahedron(
                    Point3D(*points[n1 - 1]),
                    Point3D(*points[n2 - 1]),
                    Point3D(*points[n3 - 1]),
                    Point3D(*points[n4 - 1])
                )
            )
        return tet_mesh

    def __str__(self):
        points = list(set(chain(
            *map(lambda x: x.points, self.tetrahedrons)
        )))

        tetrahedrons_with_numbers = [
            list(map(lambda x: points.index(x) + 1, tetr.points))
            for tetr in self.tetrahedrons
        ]
        return (f'TetMesh(\n'
                f'Уникальных точек: {len(points)}\n'
                f'Точки:\n'
                f'{chr(10).join(map(lambda x: f"{x[0]}. {x[1]}", enumerate(points, 1)))}\n'
                f'Тетраэдры:\n' +
                chr(10).join(map(lambda x: f"Тетраэдр ({', '.join(map(str, x))})", tetrahedrons_with_numbers)) +
                f'\n)')

