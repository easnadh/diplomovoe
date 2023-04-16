from itertools import chain

from exceptions.file_errors import FileExtensionError, FileStructureError
from mesh.point3d import Point3D
from mesh.tetrahedron import Tetrahedron
from mesh.facemesh import FaceMesh
from mesh.triangle3d import Triangle3D


class TetMesh:
    __slots__ = ('tetrahedrons', 'face_mesh')
    face_mesh: FaceMesh
    tetrahedrons: list[Tetrahedron]

    # bound_tet: list[int]

    def __init__(self, face_mesh: FaceMesh = None, tetrahedrons: list = None):
        if tetrahedrons is None:
            tetrahedrons = []
        self.face_mesh = face_mesh
        self.tetrahedrons = tetrahedrons


    @classmethod
    def read_from_file(cls, path: str):
        with open(path) as f:
            lines = f.readlines()

        if path.lower().endswith('.vol'):
            try:
                triangle_points_numbers, tetrahedron_points_numbers, points = cls.from_vol(lines)
            except:
                raise FileStructureError(path)
        elif path.lower().endswith('.dat'):
            try:
                triangle_points_numbers, tetrahedron_points_numbers, points = cls.from_dat(lines)
            except:
                raise FileStructureError(path)
        else:
            raise FileExtensionError(path)

        del lines

        tet_mesh = cls()

        if triangle_points_numbers:
            face_mesh = FaceMesh()
            for n1, n2, n3 in triangle_points_numbers:
                face_mesh.triangles.append(
                    Triangle3D(
                        Point3D(*points[n1 - 1]),
                        Point3D(*points[n2 - 1]),
                        Point3D(*points[n3 - 1])
                    )
                )
            tet_mesh.face_mesh = face_mesh

        for n1, n2, n3, n4 in tetrahedron_points_numbers:
            tet_mesh.tetrahedrons.append(
                Tetrahedron(
                    Point3D(*points[n1 - 1]),
                    Point3D(*points[n2 - 1]),
                    Point3D(*points[n3 - 1]),
                    Point3D(*points[n4 - 1])
                )
            )

        return tet_mesh

    @staticmethod
    def from_vol(lines):

        triangle_points_numbers_start = lines.index('surfaceelements\n') + 1
        triangle_points_numbers = [
            tuple(map(int, i.split()[~2:])) for i in
            lines[triangle_points_numbers_start + 1: triangle_points_numbers_start + int(
                lines[triangle_points_numbers_start]) + 1]
        ]

        tetrahedron_points_numbers_start = lines.index('volumeelements\n') + 1
        tetrahedron_points_numbers = [
            tuple(map(int, i.split()[~3:])) for i in
            lines[tetrahedron_points_numbers_start + 1: tetrahedron_points_numbers_start + int(
                lines[tetrahedron_points_numbers_start]) + 1]
        ]

        points_start = lines.index('points\n') + 1
        points = [
            tuple(map(float, line.split())) for line in
            lines[points_start + 1: points_start + int(lines[points_start]) + 1]
        ]

        return triangle_points_numbers, tetrahedron_points_numbers, points

    @staticmethod
    def from_dat(lines):
        points_start = int(lines[0])
        points = [
            tuple(map(float, line.split())) for line in
            lines[1: points_start + 1]
        ]

        tetrahedron_points_numbers_start = int(lines[points_start + 2])
        tetrahedron_points_numbers = [
            tuple(map(int, i.split())) for i in
            lines[points_start + 3: points_start + 3 + tetrahedron_points_numbers_start]
        ]

        return [], tetrahedron_points_numbers, points

    def difference(self, other, path: str):
        points1: set[Point3D] = set(chain(*map(lambda x: x.points, self.tetrahedrons)))
        points2: set[Point3D] = set(chain(*map(lambda x: x.points, other.tetrahedrons)))

        in_p1_and_not_in_p2 = points1 - points2
        in_p2_and_not_in_p1 = points2 - points1

        open(path, 'w').close()
        with open(path, 'a') as file:
            for p in in_p1_and_not_in_p2:
                file.write(f'{p.x} {p.y} {p.z}\n')
            file.write('\n')
            for p in in_p2_and_not_in_p1:
                file.write(f'{p.x} {p.y} {p.z}\n')

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
