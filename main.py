from mesh.facemesh import FaceMesh
from mesh.tetmesh import TetMesh
from utils.mesh_writer import write_mesh


def main():
    tetmesh = TetMesh.read_from_file('cube.dat')
    facemesh = FaceMesh.read_from_file('cube.dat')
    write_mesh("out.vol", facemesh, tetmesh)


if __name__ == '__main__':
    main()
