__author__ = 'j.smith'

'''
Testing stuff for Oculus
'''

# import necessary modules
import sys
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg
from epics import PV, caget, caget_many
from epics.devices import Scan
import time
import os


class Window(QtGui.QMainWindow):
    tapped = QtCore.pyqtSignal()
    det_change_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('Oculus Mechanicus')
        self.setWindowIcon(QtGui.QIcon('eye1.png'))

        self.tapped.connect(find_name)
        self.det_change_signal.connect(new_detectors)



num_positioners = 1
num_triggers = 1
num_detectors = 40

pos_attrs = ('PV', 'SP', 'EP', 'SI', 'CP', 'WD', 'PA', 'AR', 'SM', 'PP')

pnpv = {}
rncv = {}
pnra = {}

dnnpv = {}
dnncv = {}
dnnda = {}

active_detectors = {}
x_values = np.zeros(1001)

trunk = '16TEST1:scan1.'


# callbacks
def val1_t(**kwargs):
    start_val = time.clock()
    current_index = cpt1.value
    x_values[current_index - 1] = rncv['R1CV'].value
    for detectors in active_detectors:
        active_detectors[detectors][current_index - 1] = dnncv[detectors].value
        # print active_detectors[detectors][:current_index]


def data1_t(**kwargs):
    print 'start/stop'
    if data1.value == 0:
        pp = pnpv['P1PP'].value
        sp = pnpv['P1SP'].value
        ep = pnpv['P1EP'].value
        if pnpv['P1AR'].value == 0:
            min = sp
            max = ep
        else:
            min = pp + sp
            max = pp + ep
        eye.tapped.emit()
    else:
        print x_values[:cpt1.value]
        for detectors in active_detectors:
            print active_detectors[detectors][:cpt1.value]


def find_name():
    ppv_trunk = os.path.splitext(pnpv['P1PV'].value)[0]
    record = caget(ppv_trunk + '.RTYP')
    print record
    if record == 'motor':
        name = caget(ppv_trunk + '.DESC')
        print name


def new_detectors():
    b = time.clock()
    global active_detectors
    active_detectors = {}
    nv_trunk = '16TEST1:scan1.'
    for j in range(1, num_detectors + 1):
        # look for any detectors with valid PVs
        nv_branch = 'D%2.2iNV' % j
        if caget(nv_trunk + nv_branch) == 0:
            temp_key = 'D%2.2iPV' % j
            new_trunk, new_branch = os.path.splitext(dnnpv[temp_key].value)
            record = caget(new_trunk + '.RTYP')
            if record == 'scaler':
                name_branch = new_branch.replace('S', 'NM')
            elif record == 'transform':
                name_branch = new_branch[:1] + 'CMT' + new_branch[1:]
            elif record == 'mca':
                name_branch = new_branch + 'NM'
            else:
                name_branch = 'None'
            name_pv = new_trunk + name_branch
            name = caget(name_pv)
            if name == '':
                print dnnpv[temp_key].value
            else:
                print name
            det_key = temp_key.replace('P', 'C')
            active_detectors[det_key] = np.zeros(1001)
    print time.clock() - b
    print active_detectors





def det_mod(**kwargs):
    print 'detector modified'
    eye.det_change_signal.emit()




# initialize all PVs
# in testing, 4 positioners and 70 detectors nets 254 PVs connected in ~2.6 seconds
for i in range(1, num_positioners + 1):
    for a in pos_attrs:
        key_pnpv = 'P%i%s' % (i, a)
        pnpv[key_pnpv] = PV(trunk + key_pnpv)
    key_rncv = 'R%iCV' % i
    rncv[key_rncv] = PV(trunk + key_rncv)
    key_pnra = 'P%iRA' % i
    pnra[key_pnra] = PV(trunk + key_pnra)

for i in range(1, num_detectors + 1):
    key_p, key_c, key_r = 'D%2.2iPV' % i, 'D%2.2iCV' % i, 'D%2.2iDA' % i
    dnnpv[key_p] = PV(trunk + key_p)
    dnncv[key_c] = PV(trunk + key_c)
    dnnda[key_r] = PV(trunk + key_r)
    dnnpv[key_p].add_callback(det_mod)

val1 = PV('16TEST1:scan1.VAL')
data1 = PV('16TEST1:scan1.DATA')
cpt1 = PV('16TEST1:scan1.CPT')

val1.add_callback(val1_t)
data1.add_callback(data1_t)

a = time.clock()
for i in range(1, num_detectors + 1):
    key = 'D%2.2iPV' % i
    if dnnpv[key].value != '':
        key_active_det = 'D%2.2iCV' % i
        active_detectors[key_active_det] = np.zeros(1001)
print time.clock() - a

tapped = QtCore.pyqtSignal(int)
#tapped.connect(find_name)

app = QtGui.QApplication(sys.argv)
eye = Window()
eye.show()
new_detectors()
sys.exit(app.exec_())