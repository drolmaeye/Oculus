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
        self.setWindowTitle('Oculus')
        self.setWindowIcon(QtGui.QIcon('eye1.png'))

        # ###self.scan_trhead = ScanThread(self)
        # ###self.scan_trhead.scan_thread_callback_signal.connect(self.draw_plot)


class CoreData:
    NUM_POSITIONERS = 1
    NUM_TRIGGERS = 1
    NUM_DETECTORS = 40

    pos_attrs = ('PV', 'SP', 'EP', 'SI', 'CP', 'WD', 'PA', 'AR', 'SM', 'PP')

    def __init__(self):
        # create dictionaries
        self.pnpv = {}
        self.rncv = {}
        self.pnra = {}

        self.dnnpv = {}
        self.dnnnv = {}
        self.dnncv = {}
        self.dnnda = {}

        self.active_detectors = {}
        self.x_values = np.zeros(1001)

        self.trunk = '16TEST1:'
        print self.__name__
        print self.trunk









app = QtGui.QApplication(sys.argv)
scan1 = CoreData()
eye = Window()
eye.show()
sys.exit(app.exec_())