import sys
from PyQt4 import QtGui, QtCore, Qt


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(150, 150, 500, 500)
        self.setWindowTitle('Draw')


    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.green, 8, QtCore.Qt.DashLine))
        painter.drawEllipse(40, 40, 400, 400)
        painter.end()




















app = QtGui.QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())
