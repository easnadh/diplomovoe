from mesh.facemesh import FaceMesh
from mesh.point3d import Point3D
from mesh.tetrahedron import Tetrahedron
from mesh.triangle3d import Triangle3D


def from_vol(lines):
    points_start = lines.index('points') + 1
    points = []
    for point_element_row_index in range(points_start + 1, points_start + int(lines[points_start]) + 1):
        points.append(Point3D(*map(float, lines[point_element_row_index].split())))

    triangles: list[Triangle3D] = []
    surface_start = lines.index('surfaceelements') + 1
    for triangle_element_row_index in range(surface_start + 1,
                                            surface_start + int(lines[surface_start]) + 1):
        surface_number, material_number, domin, domout, _, pn1, pn2, pn3 = map(int, lines[
            triangle_element_row_index].split())

        triangles.append(Triangle3D(
            [points[pn1 - 1], points[pn2 - 1], points[pn3 - 1]],
            surface_number,
            material_number,
            domin,
            domout
        ))

    face_mesh = FaceMesh(triangles)

    tetrahedrons: list[Tetrahedron] = []
    volume_start = lines.index('volumeelements') + 1
    for tetrahedron_element_row_index in range(volume_start + 1, volume_start + int(lines[volume_start]) + 1):
        material_number, _, pn1, pn2, pn3, pn4 = list(map(int, lines[tetrahedron_element_row_index].split()))
        tetrahedrons.append(Tetrahedron(
            [points[pn1 - 1], points[pn2 - 1], points[pn3 - 1], points[pn4 - 1]],
            material_number
        ))

    return face_mesh, tetrahedrons


def from_dat(lines):
    points_start = int(lines[0])
    points = [
        tuple(map(float, line.split())) for line in
        lines[1: points_start + 1]
    ]

    tetrahedrons: list[Tetrahedron] = []
    tetrahedron_points_numbers_start = int(lines[points_start + 2])
    tetrahedron_points_numbers = [
        tuple(map(int, i.split())) for i in
        lines[points_start + 3: points_start + 3 + tetrahedron_points_numbers_start]
    ]

    for n1, n2, n3, n4 in tetrahedron_points_numbers:
        tetrahedrons.append(
            Tetrahedron(
                [Point3D(*points[n1 - 1]),
                 Point3D(*points[n2 - 1]),
                 Point3D(*points[n3 - 1]),
                 Point3D(*points[n4 - 1])],
                1
            )
        )

    return None, tetrahedrons
