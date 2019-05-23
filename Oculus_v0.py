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


class CoreData(QtCore.QObject):
    NUM_POSITIONERS = 1
    NUM_TRIGGERS = 2
    NUM_DETECTORS = 40
    MAX_NUM_POINTS = 1001

    pos_attrs = ('PV', 'SP', 'EP', 'SI', 'CP', 'WD', 'PA', 'AR', 'SM', 'PP')

    update_pos_name_signal = QtCore.pyqtSignal()
    update_detectors_signal = QtCore.pyqtSignal()

    def __init__(self, root, stump):

        super(CoreData, self).__init__()
        # create dictionaries
        self.pnpv = {}
        self.rncv = {}
        self.pnra = {}

        self.dnnpv = {}
        self.dnnnv = {}
        self.dnncv = {}
        self.dnnda = {}

        self.active_detectors = {}
        self.x_values = np.zeros(self.MAX_NUM_POINTS)

        self.trunk = root + stump

        # initialize PVs in dictionaries, with callbacks where necessary
        for i in range(1, self.NUM_POSITIONERS + 1):
            for a in self.pos_attrs:
                key_pnpv = 'P%i%s' % (i, a)
                self.pnpv[key_pnpv] = PV(self.trunk + key_pnpv)
            key_rncv = 'R%iCV' % i
            key_pnra = 'P%iRA' % i
            self.rncv[key_rncv] = PV(self.trunk + key_rncv)
            self.pnra[key_pnra] = PV(self.trunk + key_pnra)

        for i in range(1, self.NUM_DETECTORS + 1):
            key_pv = 'D%2.2iPV' % i
            key_nv = 'D%2.2iNV' % i
            key_cv = 'D%2.2iCV' % i
            key_da = 'D%2.2iDA' % i
            self.dnnpv[key_pv] = PV(self.trunk + key_pv)
            self.dnnnv[key_nv] = PV(self.trunk + key_nv)
            self.dnncv[key_cv] = PV(self.trunk + key_cv)
            self.dnnda[key_da] = PV(self.trunk + key_da)
            # callbacks for DnnPV fields
            self.dnnpv[key_pv].add_callback(self.detectors_modified)

        self.val = PV(self.trunk + 'VAL')
        self.data = PV(self.trunk + 'DATA')
        self.cpt = PV(self.trunk + 'CPT')
        self.npts = PV(self.trunk + 'NPTS')
        # callback for individual PVs
        self.val.add_callback(self.val_triggered)
        self.data.add_callback(self.data_triggered)

        # connect signals to slots
        self.update_pos_name_signal.connect(self.update_pos_name)
        self.update_detectors_signal.connect(self.update_detectors)


    # PV callbacks
    def detectors_modified(self, **kwargs):
        print 'detector modified'
        self.update_detectors_signal.emit()

    def val_triggered(self, **kwargs):
        print 'val triggered'
        current_index = self.cpt.value - 1
        self.x_values[current_index] = self.rncv['R1CV'].value
        for detectors in self.active_detectors:
            self.active_detectors[detectors][current_index] = self.dnncv[detectors].value
            print self.active_detectors[detectors][:current_index + 1]

    def data_triggered(self, **kwargs):
        print 'start/stop'
        if self.data.value == 0:
            # scan is starting
            self.update_pos_name_signal.emit()
            pp = self.pnpv['P1PP'].value
            sp = self.pnpv['P1SP'].value
            ep = self.pnpv['P1EP'].value
            if self.pnpv['P1AR'].value == 0:
                min = sp
                max = ep
            else:
                min = pp + sp
                max = pp + ep
            # TODO send these values out to GUI for initial draw
        else:
            # in reality, probably need to plot DddDA and PnRA arrays
            num_points = self.npts.value
            print self.x_values[:num_points]
            for detectors in self.active_detectors:
                print self.active_detectors[detectors][:num_points]

    # slots
    def update_pos_name(self):
        pv_trunk = os.path.splitext(self.pnpv['P1PV'].value)[0]
        record = caget(pv_trunk + '.RTYP')
        if record == 'motor':
            name = caget(pv_trunk + '.DESC')
        else:
            name = self.pnpv['P1PV'].value
        print name
        # TODO send this name out to GUI for initial draw

    def update_detectors(self):
        self.active_detectors.clear()
        for i in range(1, self.NUM_DETECTORS + 1):
            nv_branch = 'D%2.2iNV' % i
            if caget(self.trunk + nv_branch) == 0:
                pv_key = 'D%2.2iPV' % i
                new_trunk, new_branch = os.path.splitext(self.dnnpv[pv_key].value)
                record = caget(new_trunk + '.RTYP')
                if record == 'scaler':
                    # consider IDD case of timer here
                    name_branch = new_branch.replace('S', 'NM')
                elif record == 'transform':
                    name_branch = new_branch[:1] + 'CMT' + new_branch[1:]
                elif record == 'mca':
                    name_branch = new_branch + 'NM'
                else:
                    name_branch = None
                if name_branch:
                    name = caget(new_trunk + name_branch)
                    if name == '':
                        name = new_trunk + new_branch
                else:
                    name = new_trunk + new_branch
                print name
                # TODO send name out to GUI labels
                det_key = pv_key.replace('P', 'C')
                self.active_detectors[det_key] = np.zeros(self.MAX_NUM_POINTS)
        print self.active_detectors


app = QtGui.QApplication(sys.argv)
root, stump1 = '16TEST1:', 'scan1.'
scan1 = CoreData(root, stump1)
eye = Window()
scan1.update_detectors()
eye.show()
sys.exit(app.exec_())
