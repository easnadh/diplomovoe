from itertools import chain

from mesh.point3d import Point3D
from mesh.tetmesh import TetMesh


def mesh_composition(path: str, tet_mesh: TetMesh, other: TetMesh):
    points1: set[Point3D] = set(chain(*map(lambda x: x.points, tet_mesh.tetrahedrons)))
    points2: set[Point3D] = set(chain(*map(lambda x: x.points, other.tetrahedrons)))
    in_p2_and_not_in_p1 = points2 - points1

    t_points1 = tuple(points1)
    t_points2 = tuple(points2)

    open(path, 'w').close()
    with open(path, 'a') as file:
        file.write(f'{len(points1) + len(in_p2_and_not_in_p1)}\n')
        for p in points1:
            file.write(f'{p.x} {p.y} {p.z}\n')
        for p in in_p2_and_not_in_p1:
            file.write(f'{p.x} {p.y} {p.z}\n')
        file.write('\n')

        file.write(f'{len(tet_mesh.tetrahedrons) + len(other.tetrahedrons)}\n')
        for tetrahedron in tet_mesh.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(' '.join(map(lambda x: str(t_points1.index(x) + 1), cur_points)) + '\n')
        for tetrahedron in other.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(' '.join(map(lambda x: str(t_points2.index(x) + 1), cur_points)) + '\n')
