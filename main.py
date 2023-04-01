from mesh.facemesh import FaceMesh
from mesh.tetmesh import TetMesh
from utils.mesh_writer import write_mesh


def main():
    tetmesh = TetMesh.from_file('kube.vol')
    facemesh = FaceMesh.from_file('kube.vol')
    write_mesh("out.vol", tetmesh, facemesh)


if __name__ == '__main__':
    main()
