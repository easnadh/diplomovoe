from copy import copy
from dataclasses import dataclass
from itertools import chain

from exceptions.file_errors import FileExtensionError, FileStructureError
from mesh.facemesh import FaceMesh
from mesh.tetrahedron import Tetrahedron
from utils.mesh_reader import from_dat, from_vol


@dataclass(slots=True)
class TetMesh:
    face_mesh: FaceMesh
    tetrahedrons: list[Tetrahedron]

    def __copy__(self):
        new_face_mesh_triangles = copy(self.face_mesh.triangles)
        new_tetrahedrons = copy(self.tetrahedrons)

        all_new_points = list(set(chain(*map(lambda x: (copy(i) for i in x.points), self.face_mesh.triangles))) &
                              set(chain(*map(lambda x: (copy(i) for i in x.points), self.tetrahedrons))))

        for i in range(len(new_face_mesh_triangles)):
            for j in range(3):
                new_face_mesh_triangles[i].points[j] = all_new_points[all_new_points.index(
                    new_face_mesh_triangles[i].points[j])]

        for i in range(len(new_tetrahedrons)):
            for j in range(4):
                new_tetrahedrons[i].points[j] = all_new_points[all_new_points.index(
                    new_tetrahedrons[i].points[j])]

        face_mesh = FaceMesh(new_face_mesh_triangles)
        tetmesh = TetMesh(face_mesh, new_tetrahedrons)
        return tetmesh

    @classmethod
    def read_from_file(cls, path: str):
        with open(path) as file:
            lines: list[str] = [x.rstrip() for x in file]

        if path.lower().endswith('.vol'):
            try:
                face_mesh, tetrahedrons = from_vol(lines)
            except:
                raise FileStructureError(path)
        elif path.lower().endswith('.dat'):
            try:
                face_mesh, tetrahedrons = from_dat(lines)
            except:
                raise FileStructureError(path)
        else:
            raise FileExtensionError(path)

        return cls(face_mesh, tetrahedrons)

    def __str__(self):
        points = list(set(chain(
            *map(lambda x: x.points, self.tetrahedrons)
        )))

        tetrahedrons_with_numbers = [
            list(map(lambda x: points.index(x) + 1, tetrahedron.points))
            for tetrahedron in self.tetrahedrons
        ]
        return (f'TetMesh(\n'
                f'Уникальных точек: {len(points)}\n'
                f'Точки:\n'
                f'{chr(10).join(map(lambda x: f"{x[0]}. {x[1]}", enumerate(points, 1)))}\n'
                f'Тетраэдры:\n' +
                chr(10).join(map(lambda x: f"Тетраэдр ({', '.join(map(str, x))})", tetrahedrons_with_numbers)) +
                f'\n)')
