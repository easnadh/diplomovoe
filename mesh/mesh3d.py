from mesh.facemesh import FaceMesh

from dataclasses import dataclass


class Mesh3D:
    face_mesh: FaceMesh
    border_face: list[int]
