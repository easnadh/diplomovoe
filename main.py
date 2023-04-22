from mesh.tetmesh import TetMesh


def main():
    file = 'kube.vol'
    tetmesh = TetMesh.read_from_file(file)
    print(tetmesh)
    tetmesh.write_mesh_to_file('dump.vol')


if __name__ == '__main__':
    main()
