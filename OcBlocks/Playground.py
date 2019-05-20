__author__ = 'j.smith'

'''
Testing stuff for Oculus
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

        # self.test_9000()

    def draw_plot(self):
        print 'drawing'

    def test_9000(self):
        print 'testing . . .'


def print_new_pv(**kwargs):
    print kwargs['pvname']
    print kwargs['value']
    print caget(os.path.splitext(kwargs['value'])[0] + '.RTYP')

# print caget('16TEST1:scan1.D01PV')
# print caget(os.path.splitext(caget('16TEST1:scan1.D01PV'))[0] + '.RTYP')

t0 = time.clock()
srec1 = Scan('16TEST1:scan1')
# print time.clock() - t0


active_detectors = []
for i in range(1, 71):
    print srec1.get('D%2.2iNV' % i)
    if not srec1.get('D%2.2iPV' % i) == '':
        active_detectors.append('D%2.2iPV' % i)
print active_detectors
for each in active_detectors:
    print srec1.get(each)



for i in range(1, 71):
    srec1.add_callback('D%2.2iPV' % i, print_new_pv)


t1 = time.clock()
cv_list = []
for i in range(1, 71):
    print(srec1.get('D%2.2iCV' % i))
print time.clock() - t1
print cv_list


















app = QtGui.QApplication(sys.argv)
eye = Window()
eye.show()
sys.exit(app.exec_())
