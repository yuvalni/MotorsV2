from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
import pyqtgraph as pg


class TrackingWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TrackingWindow, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout()
        plot1 = pg.PlotItem()
        plot1.plot()
        layout.addWidget(plot1)
        self.setLayout(layout)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    tracking = TrackingWindow()
    tracking.show()
    app.exec()