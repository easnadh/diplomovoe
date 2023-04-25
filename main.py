from mesh.tetmesh import TetMesh
from utils.mesh_writer import write_mesh_to_file


def main():
    file = 'cube.dat'
    tetmesh = TetMesh.read_from_file(file)
    write_mesh_to_file('dump.vol', tetmesh)


if __name__ == '__main__':
    main()
