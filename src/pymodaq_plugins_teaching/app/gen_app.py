from  pymodaq_gui.utils.custom_app import CustomApp


class GenApp(CustomApp):

    def __init__(self, parent):
        super().__init__(parent)


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