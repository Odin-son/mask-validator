import sys
import os
import cv2
import os.path as osp

from PyQt5.QtWidgets import *
from PyQt5 import uic
from glob import glob

PROJ_DIR = osp.dirname(osp.abspath(__file__))
form_class = uic.loadUiType(osp.join(PROJ_DIR, 'main.ui'))[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('mask validator')
        self.import_btn.clicked.connect(self.import_clicked)
        self.progressBar.setVisible(False)

        self.color_map = [(0, 0, 0),
                          (0, 0, 255),
                          (0, 255, 255),
                          (255, 0, 255),
                          (0, 150, 255),
                          (255, 0, 0),
                          (0, 255, 0),
                          (255, 255, 0)]

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
        self.validate()

    def validate(self):
        if not os.path.exists(self.label.text()):
            QMessageBox.warning(self, self.tr("Attention"), "Directory does not exist", QMessageBox.Yes)
            return

        imgs_path = glob(os.path.join(self.label.text(), '*{}'.format('.png')))

        have_problem = False
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(len(imgs_path))

        for step, img_path in enumerate(imgs_path):
            img = cv2.imread(img_path)

            result = img.copy()
            for idx in range(1, len(self.color_map)):
                extracted_mask = (img[:, :, 0] == self.color_map[idx][0]) & (img[:, :, 1] == self.color_map[idx][1]) & (
                        img[:, :, 2] == self.color_map[idx][2])
                result[extracted_mask] = 0

            if result.max() > 0:
                have_problem = True
                result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
                result[result > 0] = 255

                out_path = os.path.join(os.path.split(img_path)[0],
                                        '{}_problem.png'.format(os.path.basename(img_path).split('.')[0]))

                cv2.imwrite(out_path, result)

            self.progressBar.setValue(step+1)

        if have_problem:
            QMessageBox.warning(self, self.tr("Attention"), "There are some problem", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, self.tr("Attention"), "Checked", QMessageBox.Yes)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
