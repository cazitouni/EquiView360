import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QDesktopWidget
from PyQt5 import QtCore
import Equirec2Perspec as E2P 
import cv2
import platform 

# Linux systems need this env var
if platform.system() == 'Linux':
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
else :
    pass

# Main windows
class Window(QDialog):
    def __init__(self):

        # Initialisation of the vars
        super().__init__()
        self.title = "Equirectangular 360° Viewer"
        self.posh = 0
        self.posw = 0
        self.save = QPoint(0,0)
        self.fov = 100
        self.imgPath = cv2.imread('example.jpg', cv2.IMREAD_COLOR)
        self.equ = E2P.Equirectangular(self.imgPath)
        self.width = 1080
        self.height = 720
        self.setFixedSize(1080, 720)
        self.InitWindow()

    # Create the windows
    def InitWindow(self):

        # Setting icon title and geometry
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        # Centering the windows
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Setting the image into the windows
        self.labelImage = QLabel(self)
        self.labelImage.setPixmap(QPixmap(self.img(self.fov, self.posw, self.posh)))
        self.show()

    # Image creation photo to get the correct perspective
    def img(self, fov, tet, fi) :
        img = self.equ.GetPerspective(fov, tet, fi, 720, 1080)
        qimg = QtGui.QImage(img.data, 1080, 720, 3240, QtGui.QImage.Format_BGR888)
        return qimg

    # Key movement 
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            self.posh -= 30
            self.labelImage.setPixmap(QPixmap(self.img( self.fov, self.posw, self.posh)))
        if event.key() == QtCore.Qt.Key_Up:
            self.posh  += 30
            self.labelImage.setPixmap(QPixmap(self.img( self.fov, self.posw, self.posh)))
        if event.key() == QtCore.Qt.Key_Left:
            self.posw  -= 30
            self.labelImage.setPixmap(QPixmap(self.img(self.fov, self.posw, self.posh)))
        if event.key() == QtCore.Qt.Key_Right:
            self.posw  += 30
            self.labelImage.setPixmap(QPixmap(self.img(self.fov, self.posw, self.posh)))

    # Mouse press event for the mouse movement function
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    # Mouse movement function - Generate the correct perspective on each mouse moves
    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        self.delta =  (self.mousePos - event.pos()) + self.save
        self.labelImage.setPixmap(QPixmap(self.img(self.fov, (self.delta.x() / 10 + self.posh), (-self.delta.y() / 10 + self.posw))))

    # Update the cursor position on mouse release
    def mouseReleaseEvent(self, event):
        self.save = self.delta

# Launch the application
if __name__ =='__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())