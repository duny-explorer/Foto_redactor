import sys
from PyQt5 import uic
from PIL import Image
import numpy as np
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Меню')
        self.first_page.clicked.connect(self.change_page)
        self.second_page.clicked.connect(self.change_page)

    def change_page(self):
        if self.sender().text() == ">":
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
