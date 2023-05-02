from itertools import chain

from mesh.point3d import Point3D
from mesh.tetmesh import TetMesh


def merge_meshes(path: str, first_mesh: TetMesh, second_mesh: TetMesh):
    points1: set[Point3D] = set(chain(*map(lambda x: x.points, first_mesh.tetrahedrons)))
    points2: set[Point3D] = set(chain(*map(lambda x: x.points, second_mesh.tetrahedrons)))
    in_p2_and_not_in_p1 = points2 - points1

    open(path, 'w').close()
    with open(path, 'a') as file:

        file.write('\n# surfnr    bcnr   domin  domout      np      p1      p2      p3\n'
                   f'surfaceelements\n{len(first_mesh.face_mesh.triangles) + len(second_mesh.face_mesh.triangles)}\n')
        for triangle in first_mesh.face_mesh.triangles:
            cur_points = triangle.points
            file.write(f'{triangle.surface_number} {triangle.material_number} {triangle.domin}'
                       f' {triangle.domout} 3 ' + ' '.join(map(lambda x: str(tuple(points1).index(x) + 1),
                                                               cur_points)) + '\n')
        for triangle in second_mesh.face_mesh.triangles:
            cur_points = triangle.points
            file.write(
                f'{triangle.surface_number} {triangle.material_number} {triangle.domin} {triangle.domout} 3 ' + ' '.join(
                    map(lambda x: str(tuple(points2).index(x) + 1),
                        cur_points)) + '\n')

        file.write(f'\n#  matnr      np      p1      p2      p3      p4\n'
                   f'volumeelements\n{len(first_mesh.tetrahedrons) + len(second_mesh.tetrahedrons)}\n')
        for tetrahedron in first_mesh.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(f'{tetrahedron.material_number} 4 ' + ' '.join(
                map(lambda x: str(tuple(points1).index(x) + 1), cur_points)) + '\n')
        for tetrahedron in second_mesh.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(f'{tetrahedron.material_number} 4 ' + ' '.join(
                map(lambda x: str(tuple(points2).index(x) + 1), cur_points)) + '\n')

        file.write(f'\n#          X             Y             Z\n'
                   f'points\n{len(points1) + len(in_p2_and_not_in_p1)}\n')
        for p in points1:
            file.write(f'{p.x} {p.y} {p.z}\n')
        for p in in_p2_and_not_in_p1:
            file.write(f'{p.x} {p.y} {p.z}\n')
        file.write('\n')
