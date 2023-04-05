from mesh.facemesh import FaceMesh
from mesh.tetmesh import TetMesh


def write_mesh(file_name: str, face_mesh: FaceMesh = None, tet_mesh: TetMesh = None):
    points = set()

    if face_mesh is not None:
        for triangle in face_mesh.triangles:
            points.update({*triangle.points})

    if tet_mesh is not None:
        for tetrahedron in tet_mesh.tetrahedrons:
            points.update({*tetrahedron.points})

    points = tuple(points)

    open(file_name, 'w').close()
    with open(file_name, 'a') as file:

        if face_mesh is not None:
            file.write('facemesh\n')
            for triangle in face_mesh.triangles:
                cur_points = triangle.points
                file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

        if tet_mesh is not None:
            file.write('tetmesh\n')
            for tetrahedron in tet_mesh.tetrahedrons:
                cur_points = tetrahedron.points
                file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

        file.write('points\n')
        for point in points:
            file.write(f"{point.x} {point.y} {point.z}\n")
