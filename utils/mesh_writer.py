from exceptions.file_errors import FileExtensionError
from mesh.tetmesh import TetMesh


def write_mesh_to_file(file_name: str, tet_mesh: TetMesh):
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

    if file_name.endswith('.vol'):
        with open(file_name, 'a') as file:
            to_vol(file, tet_mesh, points)
    elif file_name.endswith('.dat'):
        with open(file_name, 'a') as file:
            to_dat(file, tet_mesh, points)
    else:
        raise FileExtensionError(file_name)


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
