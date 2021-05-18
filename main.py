import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("main.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.import_btn.clicked.connect(self.import_clicked)
        self.export_btn.clicked.connect(self.export_clicked)
        self.buttonBox.clicked.connect(self.validate)

    def import_clicked(self):
        import_dir_path = str(
            QFileDialog.getExistingDirectory(
                self,
                self.tr("Open Directory"),
                os.getcwd(),
                QFileDialog.ShowDirsOnly
                | QFileDialog.DontResolveSymlinks,
            )
        )
        self.label.setText(import_dir_path)

    def export_clicked(self):
        export_dir_path = str(
            QFileDialog.getExistingDirectory(
                self,
                self.tr("Open Directory"),
                os.getcwd(),
                QFileDialog.ShowDirsOnly
                | QFileDialog.DontResolveSymlinks,
            )
        )
        self.label_2.setText(export_dir_path)

    def validate(self):
        if not os.path.exists(self.label.text()):
            QMessageBox.warning(self, self.tr("Attention"), "import path does not exist", QMessageBox.Yes)
            return

        if not os.path.exists(self.label_2.text()):
            QMessageBox.warning(self, self.tr("Attention"), "export path does not exist", QMessageBox.Yes)
            return


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
