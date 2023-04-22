from dataclasses import dataclass

from mesh.facemesh import FaceMesh
from mesh.point3d import Point3D
from mesh.tetrahedron import Tetrahedron
from mesh.triangle3d import Triangle3D


@dataclass(slots=True)
class TetMesh:
    face_mesh: FaceMesh
    tetrahedrons: list[Tetrahedron]

    # bound_tet: list[int]

    @classmethod
    def read_from_file(cls, path: str):
        if path.endswith('.vol'):
            with open(path) as file:
                lines: list[str] = [x.rstrip() for x in file]

            points_start = lines.index('points') + 1
            points = []
            for point_element_row_index in range(points_start + 1, points_start + int(lines[points_start]) + 1):
                points.append(Point3D(*map(float, lines[point_element_row_index].split())))

            triangles: list[Triangle3D] = []
            surface_start = lines.index('surfaceelements') + 1
            for triangle_element_row_index in range(surface_start + 1,
                                                    surface_start + int(lines[surface_start]) + 1):
                surface_number, material_number, domin, domout, _, pn1, pn2, pn3 = map(int, lines[
                    triangle_element_row_index].split())

                triangles.append(Triangle3D(
                    [points[pn1 - 1], points[pn2 - 1], points[pn3 - 1]],
                    surface_number,
                    material_number,
                    domin,
                    domout
                ))

            face_mesh = FaceMesh(triangles)

            tetrahedrons: list[Tetrahedron] = []
            volume_start = lines.index('volumeelements') + 1
            for tetrahedron_element_row_index in range(volume_start + 1, volume_start + int(lines[volume_start]) + 1):
                material_number, _, pn1, pn2, pn3, pn4 = list(map(int, lines[tetrahedron_element_row_index].split()))
                tetrahedrons.append(Tetrahedron(
                    [points[pn1 - 1], points[pn2 - 1], points[pn3 - 1], points[pn4 - 1]],
                    material_number
                ))

            return cls(face_mesh, tetrahedrons)

    def write_mesh_to_file(self, file_name: str):
        if file_name.endswith('.vol'):
            points = set()

            if self.face_mesh:
                for triangle in self.face_mesh.triangles:
                    points.update({*triangle.points})

            if self.tetrahedrons:
                for tetrahedron in self.tetrahedrons:
                    points.update({*tetrahedron.points})

            if not self.face_mesh and not self.tetrahedrons:
                raise ValueError(f'Ошибка записи в файл. Обе сетки пусты.')

            points = tuple(points)

            open(file_name, 'w').close()
            with open(file_name, 'a') as file:

                if self.face_mesh is not None:
                    file.write('facemesh\n')
                    for triangle in self.face_mesh.triangles:
                        cur_points = triangle.points
                        file.write(f'{triangle.surface_number} {triangle.material_number} {triangle.domin}'
                                   f' {triangle.domout} 3 ' + ' '.join(map(lambda x: str(points.index(x) + 1),
                                                                          cur_points)) + '\n')

                if self.tetrahedrons:
                    file.write('tetmesh\n')
                    for tetrahedron in self.tetrahedrons:
                        cur_points = tetrahedron.points
                        file.write(f'{tetrahedron.material_number} 4 ' + ' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

                file.write('points\n')
                for point in points:
                    file.write(f"{point.x} {point.y} {point.z}\n")

    # def __str__(self):
    #     points = list(set(chain(
    #         *map(lambda x: x.points, self.tetrahedrons)
    #     )))
    #
    #     tetrahedrons_with_numbers = [
    #         list(map(lambda x: points.index(x) + 1, tetr.points))
    #         for tetr in self.tetrahedrons
    #     ]
    #     return (f'TetMesh(\n'
    #             f'Уникальных точек: {len(points)}\n'
    #             f'Точки:\n'
    #             f'{chr(10).join(map(lambda x: f"{x[0]}. {x[1]}", enumerate(points, 1)))}\n'
    #             f'Тетраэдры:\n' +
    #             chr(10).join(map(lambda x: f"Тетраэдр ({', '.join(map(str, x))})", tetrahedrons_with_numbers)) +
    #             f'\n)')