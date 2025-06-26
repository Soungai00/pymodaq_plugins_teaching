from  pymodaq_gui.utils.custom_app import CustomApp
from pymodaq_gui.utils.dock import Dock, DockArea
from qtpy import QtWidgets
from pymodaq_gui.plotting.data_viewers.viewer1D import Viewer1D, DataToExport

from pymodaq.control_modules.daq_viewer import DAQ_Viewer, DAQTypesEnum

from typing import Optional

class GenApp(CustomApp):

    def __init__(self, parent):
        super().__init__(parent)
        self.viewer1D_raw: Optional[Viewer1D] = None
        self.viewer1D_fft: Optional[Viewer1D] = None
        self.daq_viewer: DAQ_Viewer = None
        self.setup_ui()

    def setup_docks(self):
        self.docks['daq_viewer'] = Dock('DAQViewer Generator')
        self.docks['raw_viewer'] = Dock('Raw Viewer')
        self.docks['fft_viewer'] = Dock('FFT Viewer')

        self.dockarea.addDock(self.docks['daq_viewer'])
        self.dockarea.addDock(self.docks['raw_viewer'], 'right')
        self.dockarea.addDock(self.docks['fft_viewer'], 'bottom', self.docks['raw_viewer'])

        self.viewer1D_raw = Viewer1D(QtWidgets.QWidget())
        self.docks['raw_viewer'].addWidget(self.viewer1D_raw.parent)

        self.viewer1D_fft = Viewer1D(QtWidgets.QWidget())
        self.docks['fft_viewer'].addWidget(self.viewer1D_fft.parent)

        dockarea = DockArea()
        main_window = QtWidgets.QMainWindow()
        main_window.setCentralWidget(dockarea)
        self.docks['daq_viewer'].addWidget(main_window)
        self.daq_viewer = DAQ_Viewer(dockarea)

        self.daq_viewer.daq_type = DAQTypesEnum.DAQ1D
        QtWidgets.QApplication.processEvents()
        self.daq_viewer.detector = 'Generator'

        self.daq_viewer.init_hardware_ui(True)
        QtWidgets.QApplication.processEvents()
        self.daq_viewer.snap()

    def setup_actions(self):
        pass

    def connect_things(self):
        #self.daq_viewer.grab_done_signal.connect(self.get_dwa_and_show)
        self.daq_viewer.grab_done_signal.connect(
            lambda dte: self.viewer1D_raw.show_data(dte[0]))

    def get_dwa_and_show(self, dte: DataToExport):
        self.viewer1D_raw.show_data(dte[0])

def main():
    from pymodaq_gui.utils.utils import mkQApp


    import numpy as np

    app = mkQApp('GenApp')
    area = DockArea()
    win = QtWidgets.QMainWindow()
    win.setCentralWidget(area)
    gen_app = GenApp(area)
    win.show()
    app.exec()

if __name__ == '__main__':
    main()