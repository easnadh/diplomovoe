from itertools import chain

from exceptions.surface_errors import NonequivalentPlanesError, NonequivalentPointsCountError
from mesh.point3d import Point3D
from mesh.tetmesh import TetMesh
from mesh.triangle3d import Triangle3D


def merge_meshes(surface_number1: Triangle3D.surface_number, surface_number2: Triangle3D.surface_number,
                 first_mesh: TetMesh, second_mesh: TetMesh):

    common_points: set[Point3D] = set(chain(*map(lambda x: x.points, first_mesh.tetrahedrons))).intersection(
        set(chain(*map(lambda x: x.points, second_mesh.tetrahedrons))))

    # if common_points:
    #     all_facemesh_triangles = list(set(first_mesh.face_mesh.triangles + second_mesh.face_mesh.triangles))
    #     facemesh = FaceMesh(all_facemesh_triangles)
    #     all_tetmesh_tetrahedrons = list(set(first_mesh.tetrahedrons + second_mesh.tetrahedrons))
    #     tetmesh = TetMesh(facemesh, all_tetmesh_tetrahedrons)
    #
    #     return tetmesh
    # else:
    count1, count2 = 0, 0
    for triangle in first_mesh.face_mesh.triangles:
        if triangle.surface_number == surface_number1:
            f_p1, f_p2, f_p3, *ps = triangle.points
            A1, B1, C1 = find_equation_plane(f_p1, f_p2, f_p3)
            count1 += 1
    for triangle in second_mesh.face_mesh.triangles:
        if triangle.surface_number == surface_number2:
            s_p1, s_p2, s_p3, *ps = triangle.points
            A2, B2, C2 = find_equation_plane(s_p1, s_p2, s_p3)
            count2 += 1
    if (A1, B1, C1) == (A2, B2, C2):
        if count1 == count2:
            ...
        else:
            raise NonequivalentPointsCountError(surface_number1, surface_number2)
    else:
        raise NonequivalentPlanesError(surface_number1, surface_number2)


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
