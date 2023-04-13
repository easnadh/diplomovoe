from mesh.facemesh import FaceMesh
from mesh.tetmesh import TetMesh
from utils.mesh_writer import write_mesh_to_file


def main():
    tetmesh1 = TetMesh.read_from_file('kube.vol')
    tetmesh2 = TetMesh.read_from_file('kube1.vol')

    tetmesh1.intersection(tetmesh2, 'int.vol')


if __name__ == '__main__':
    main()
