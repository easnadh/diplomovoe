from mesh.tetmesh import TetMesh


def convert_mesh(file_name: str, tet_mesh: TetMesh):
    points = set()

    if tet_mesh.face_mesh is not None:
        for triangle in tet_mesh.face_mesh.triangles:
            points.update({*triangle.points})

    if tet_mesh.tetrahedrons:
        for tetrahedron in tet_mesh.tetrahedrons:
            points.update({*tetrahedron.points})

    if not tet_mesh.face_mesh and not tet_mesh.tetrahedrons:
        raise ValueError(f'Ошибка записи в файл. Обе сетки пусты.')

    points = tuple(points)

    open(file_name, 'w').close()
    with open(file_name, 'a') as file:

        if file_name.endswith('.vol'):
            to_vol(file, tet_mesh, points)

        if file_name.endswith('.dat'):
            to_dat(file, tet_mesh, points)


def to_vol(file, tet_mesh, points):
    if tet_mesh.face_mesh is not None:
        file.write('\n# surfnr    bcnr   domin  domout      np      p1      p2      p3\n'
                   f'surfaceelements\n{len(tet_mesh.face_mesh.triangles)}\n')
        for triangle in tet_mesh.face_mesh.triangles:
            cur_points = triangle.points
            file.write(f'{triangle.surface_number} {triangle.material_number} {triangle.domin}'
                       f' {triangle.domout} 3 ' + ' '.join(map(lambda x: str(points.index(x) + 1),
                                                               cur_points)) + '\n')

    if tet_mesh.tetrahedrons:
        file.write('\n#  matnr      np      p1      p2      p3      p4\n'
                   f'volumeelements\n{len(tet_mesh.tetrahedrons)}\n')
        for tetrahedron in tet_mesh.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(f'{tetrahedron.material_number} 4 ' + ' '.join(
                map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')

    file.write('\n#          X             Y             Z\n'
               f'points\n{len(points)}\n')
    for point in points:
        file.write(f"{point.x} {point.y} {point.z}\n")


def to_dat(file, tet_mesh, points):
    file.write(f'{len(points)}\n')
    for point in points:
        file.write(f"{point.x} {point.y} {point.z}\n")

    if tet_mesh.tetrahedrons:
        file.write(f'\n{len(tet_mesh.tetrahedrons)}\n')
        for tetrahedron in tet_mesh.tetrahedrons:
            cur_points = tetrahedron.points
            file.write(' '.join(map(lambda x: str(points.index(x) + 1), cur_points)) + '\n')
