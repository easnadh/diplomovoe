from mesh.tetmesh import TetMesh


def write_mesh_to_file(file_name: str, tet_mesh: TetMesh):
    points = set()

    if tet_mesh.face_mesh is not None:
        for triangle in tet_mesh.face_mesh.triangles:
            points.update({*triangle.points})

    if tet_mesh.tetrahedrons:
        for tetrahedron in tet_mesh.tetrahedrons:
            points.update({*tetrahedron.points})

    if tet_mesh.face_mesh is None and not tet_mesh.tetrahedrons:
        raise ValueError(f'Ошибка записи в файл. Обе сетки пусты.')

    points = tuple(points)

    open(file_name, 'w').close()
    with open(file_name, 'a') as file:

        if tet_mesh.face_mesh is not None:
            file.write('facemesh\n')
            for triangle in tet_mesh.face_mesh.triangles:
                cur_points = triangle.points
                file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

        if tet_mesh.tetrahedrons:
            file.write('tetmesh\n')
            for tetrahedron in tet_mesh.tetrahedrons:
                cur_points = tetrahedron.points
                file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

        file.write('points\n')
        for point in points:
            file.write(f"{point.x} {point.y} {point.z}\n")
