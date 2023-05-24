from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.uic import loadUi

from exceptions.file_errors import *
from exceptions.surface_errors import *
from mesh.tetmesh import TetMesh
from utils.mesh_merger import merge_meshes
from utils.mesh_writer import write_mesh_to_file


class UiMerge(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(r'C:\Users\first\PycharmProjects\diplomovoe\ui\ui_merger.ui', self)
        self.load_mesh1_file_button.clicked.connect(self.load_mesh1_file)
        self.load_mesh2_file_button.clicked.connect(self.load_mesh2_file)
        self.surface_number1_lineedit.setValidator(QIntValidator())
        self.surface_number2_lineedit.setValidator(QIntValidator())

        self.get_result_button.clicked.connect(self.get_result)
        self.setWindowIcon(QIcon(r'C:\Users\first\PycharmProjects\diplomovoe\ui\mesh.ico'))


    def load_mesh1_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '*.vol')
        self.mesh1_lineedit.setText(file_name[0])

    def load_mesh2_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '*.vol')
        self.mesh2_lineedit.setText(file_name[0])

    def get_result(self):
        mesh1 = self.mesh1_lineedit.text()
        mesh2 = self.mesh2_lineedit.text()
        surface_number1 = self.surface_number1_lineedit.text()
        surface_number2 = self.surface_number2_lineedit.text()

        if not mesh1 or not mesh2 or not surface_number1 or not surface_number2:
            msg = QMessageBox()
            msg.setText("Field can't be empty")
            msg.setWindowTitle('Error')
            msg.exec()
        else:
            tetmesh1 = self.check_and_read_file(mesh1)
            tetmesh2 = self.check_and_read_file(mesh2)
            if tetmesh1 and tetmesh2:
                try:
                    tetmesh = merge_meshes(int(surface_number1), int(surface_number2), tetmesh1, tetmesh2)
                    file_name = QFileDialog.getSaveFileName(self, 'Save File', '*.vol; *.dat')
                    write_mesh_to_file(file_name[0], tetmesh)
                    if file_name[0]:
                        self.close()
                except SurfacesNotFoundError as e:
                    self.error_label.setText(str(e))
                except NonequivalentPointsCountError as e:
                    self.error_label.setText(str(e))
                except NonequivalentPlanesError as e:
                    self.error_label.setText(str(e))
                except ValueError as e:
                    self.error_label.setText(e)
                except FileExtensionError as e:
                    self.error_label.setText(str(e))

    def check_and_read_file(self, mesh):
        try:
            tetmesh = TetMesh.read_from_file(mesh)
            return tetmesh
        except FileExtensionError as e:
            self.error_label.setText(str(e))
        except FileStructureError as e:
            self.error_label.setText(str(e))
