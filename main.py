from mesh.facemesh import FaceMesh
from mesh.tetmesh import TetMesh
from utils.mesh_writer import write_mesh_to_file


def main():
    file = 'cube.vol'
    facemesh = FaceMesh.read_from_file(file)
    tetmesh = TetMesh.read_from_file(file)
    write_mesh_to_file('out.vol', facemesh, tetmesh)


if __name__ == '__main__':
    main()
