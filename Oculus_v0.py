__author__ = 'j.smith'

'''
A GUI for displaying scans collected using the EPICS scan record
'''

# import necessary modules
import sys
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg
from epics import PV, caget
from epics.devices import Scan
import time
import os


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('Oculus Mechanicus')
        self.setWindowIcon(QtGui.QIcon('eye1.png'))

        # ###self.scan_trhead = ScanThread(self)
        # ###self.scan_trhead.scan_thread_callback_signal.connect(self.draw_plot)

app = QtGui.QApplication(sys.argv)
eye = Window()
eye.show()
sys.exit(app.exec_())