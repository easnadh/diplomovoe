from mesh.facemesh import FaceMesh
from mesh.tetmesh import TetMesh


def write_mesh(file_name: str, tet_mesh: TetMesh, face_mesh: FaceMesh):
    points = set()
    for tetrahedron in tet_mesh.tetrahedrons:
        points.update({*tetrahedron.points})
    for triangle in face_mesh.triangles:
        points.update({*triangle.points})
    points = tuple(points)

    open(file_name, 'w').close()
    with open(file_name, 'a') as file:
        file.write('facemesh\n')
        for triangle in face_mesh.triangles:
            cur_points = triangle.points
            file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

        file.write('tetmesh\n')
        for tetrahedron in tet_mesh.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

        file.write('points\n')
        for point in points:
            file.write(f"{point.x} {point.y} {point.z}\n")






