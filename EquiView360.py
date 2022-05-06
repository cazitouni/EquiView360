from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5 import QtCore
import Equirec2Perspec as E2P 
import cv2

import sys
from PyQt5.QtGui import QPixmap

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Equirectangular 360° Viewer"
        self.top = 200
        self.left = 500
        self.posh = 0
        self.posw = 0
        self.save = QPoint(0,0)
        self.endpoint = QPoint(0,0)
        self.fov = 100
        self.imgPath = cv2.imread('example.jpg', cv2.IMREAD_COLOR)
        self.width = 1080
        self.height = 720
        self.setFixedSize(1080, 720)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:#202020")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.labelImage = QLabel(self)
        pixmap = QPixmap(self.img(self.imgPath, self.fov, self.posw, self.posh))
        self.labelImage.setPixmap(pixmap)
        self.show()

    def img(self, path, fov, tet, fi) :
        equ = E2P.Equirectangular(path)
        img = equ.GetPerspective(fov, tet, fi, 720, 1080)
        height, width, channel= img.shape
        bytesPerLine = 3 * width
        qimg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
        return qimg

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Down:
            self.posh = self.posh -30
            pixmap = QPixmap(self.img(self.imgPath, self.fov, self.posw, self.posh))
            self.labelImage.setPixmap(pixmap)
        event.accept()

        if event.key() == QtCore.Qt.Key_Up:
            self.posh = self.posh  + 30
            pixmap = QPixmap(self.img(self.imgPath, self.fov, self.posw, self.posh))
            self.labelImage.setPixmap(pixmap)
        event.accept()
        if event.key() == QtCore.Qt.Key_Left:
            self.posw = self.posw  - 30
            pixmap = QPixmap(self.img(self.imgPath, self.fov, self.posw, self.posh))
            self.labelImage.setPixmap(pixmap)
        event.accept()
        if event.key() == QtCore.Qt.Key_Right:
            self.posw = self.posw  + 30
            pixmap = QPixmap(self.img(self.imgPath, self.fov, self.posw, self.posh))
            self.labelImage.setPixmap(pixmap)
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):

        if event.buttons() != QtCore.Qt.LeftButton:
            return

        self.delta =  self.mousePos - event.pos()
        self.delta = self.delta + self.save
        pixmap = QPixmap(self.img(self.imgPath, self.fov, (self.delta.x() / 10 + self.posh), (-self.delta.y() / 10 + self.posw)))
        self.labelImage.setPixmap(pixmap)

    def mouseReleaseEvent(self, event):

        self.save = self.delta

if __name__ =='__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())