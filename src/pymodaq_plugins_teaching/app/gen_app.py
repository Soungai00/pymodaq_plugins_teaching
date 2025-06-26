from  pymodaq_gui.utils.custom_app import CustomApp
from pymodaq_gui.utils.dock import Dock

class GenApp(CustomApp):

    def __init__(self, parent):
        super().__init__(parent)

        self.setup_ui()

    def setup_docks(self):
        self.docks['daq_viewer'] = Dock('DAQViewer Generator')
        self.docks['raw_viewer'] = Dock('Raw Viewer')
        self.docks['fft_viewer'] = Dock('FFT Viewer')

        self.dockarea.addDock(self.docks['daq_viewer'])
        self.dockarea.addDock(self.docks['raw_viewer'], 'right')
        self.dockarea.addDock(self.docks['fft_viewer'], 'bottom', self.docks['raw_viewer'])

    def setup_actions(self):
        pass

    def connect_things(self):
        pass

def main():
    from pymodaq_gui.utils.utils import mkQApp
    from pymodaq_gui.utils.dock import DockArea
    from qtpy import QtWidgets
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