from itertools import chain

from mesh.facemesh import FaceMesh
from mesh.point3d import Point3D
from mesh.tetmesh import TetMesh


def merge_meshes(first_mesh: TetMesh, second_mesh: TetMesh):
    first_points: set[Point3D] = set(chain(*map(lambda x: x.points, first_mesh.tetrahedrons)))
    second_points: set[Point3D] = set(chain(*map(lambda x: x.points, second_mesh.tetrahedrons)))

    points = first_points.union(second_points)
    common_points = first_points.intersection(second_points)

    if common_points:
        all_facemesh_triangles = list(set(first_mesh.face_mesh.triangles + second_mesh.face_mesh.triangles))
        facemesh = FaceMesh(all_facemesh_triangles)
        all_tetmesh_tetrahedrons = list(set(first_mesh.tetrahedrons + second_mesh.tetrahedrons))
        tetmesh = TetMesh(facemesh, all_tetmesh_tetrahedrons)

        return tetmesh
