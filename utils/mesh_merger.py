import math
from copy import copy
from functools import partial
from itertools import chain

from exceptions.surface_errors import NonequivalentPlanesError, NonequivalentPointsCountError, SurfacesNotFoundError
from mesh.facemesh import FaceMesh
from mesh.point3d import Point3D
from mesh.tetmesh import TetMesh


def merge_meshes(surface_number1: int, surface_number2: int, mesh1: TetMesh, mesh2: TetMesh) -> TetMesh:
    face_points1 = list(chain(*map(lambda x: x.points,
                                   filter(lambda x: x.surface_number == surface_number1, mesh1.face_mesh.triangles)
                                   )))
    face_points2 = list(chain(*map(lambda x: x.points,
                                   filter(lambda x: x.surface_number == surface_number2, mesh2.face_mesh.triangles)
                                   )))

    if face_points1 and face_points2:
        if set(face_points1) == set(face_points2):
            all_facemesh_triangles = list(set(mesh1.face_mesh.triangles + mesh2.face_mesh.triangles))
            facemesh = FaceMesh(all_facemesh_triangles)
            all_tetmesh_tetrahedrons = list(set(mesh1.tetrahedrons + mesh2.tetrahedrons))
            tetmesh = TetMesh(facemesh, all_tetmesh_tetrahedrons)

            return tetmesh
        else:
            if len(face_points1) == len(face_points2):
                for triangle in mesh1.face_mesh.triangles:
                    if triangle.surface_number == surface_number1:
                        f_p1, f_p2, f_p3, *ps = triangle.points
                        A1, B1, C1 = find_equation_plane(f_p1, f_p2, f_p3)
                for triangle in mesh2.face_mesh.triangles:
                    if triangle.surface_number == surface_number2:
                        s_p1, s_p2, s_p3, *ps = triangle.points
                        A2, B2, C2 = find_equation_plane(s_p1, s_p2, s_p3)
                if (A1, B1, C1) == (A2, B2, C2):
                    return mid_merge(mesh1, mesh2, face_points1, face_points2)
                else:
                    raise NonequivalentPlanesError(surface_number1, surface_number2)
            else:
                raise NonequivalentPointsCountError(surface_number1, surface_number2)
    else:
        raise SurfacesNotFoundError(surface_number1, surface_number2)


def mid_merge(mesh1: TetMesh, mesh2: TetMesh, face_points1, face_points2) -> TetMesh:
    mesh_copy = copy(mesh1)

    print(*sorted(face_points1, key=lambda x: (x.x, x.y, x.z)), sep='\n', end='\n\n')
    print(*sorted(face_points2, key=lambda x: (x.x, x.y, x.z)), sep='\n')

    for point in face_points1:
        mn = min(face_points2, key=partial(dist, point))
        mean_x = (point.x + mn.x) * 0.5
        mean_y = (point.y + mn.y) * 0.5
        mean_z = (point.z + mn.z) * 0.5
        point.x = mean_x
        point.y = mean_y
        point.z = mean_z
    mesh_copy.tetrahedrons.extend(mesh2.tetrahedrons)
    mesh_copy.face_mesh.triangles.extend(mesh2.face_mesh.triangles)

    return mesh_copy


def dist(p1: Point3D, p2: Point3D):
    return math.hypot(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)


def find_equation_plane(p1, p2, p3):
    x1, y1, z1 = p1.x, p1.y, p1.z
    x2, y2, z2 = p2.x, p2.y, p2.z
    x3, y3, z3 = p3.x, p3.y, p3.z

    A = y1 * (z2 - z3) + y2 * (z3 - z1) + y3 * (z1 - z2)
    B = z1 * (x2 - x3) + z2 * (x3 - x1) + z3 * (x1 - x2)
    C = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)

    if A < 0:
        A *= -1
        B *= -1
        C *= -1

    return A, B, C
