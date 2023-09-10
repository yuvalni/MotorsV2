from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
import pyqtgraph as pg


class TrackingWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TrackingWindow, self).__init__(*args, **kwargs)
        widget = QtWidgets.QWidget()
        
        Horlayout = QtWidgets.QHBoxLayout()
        widget.setLayout(Horlayout)
        plot = pg.PlotWidget(widget)
        plot.plot([0,1],[2,3])   
        Horlayout.addWidget(plot)
        verticalLayout = QtWidgets.QVBoxLayout()
        Horlayout.addLayout(verticalLayout)
        verticalLayout.addWidget(QtWidgets.QPushButton())
        self.setLayout(Horlayout)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    tracking = TrackingWindow()
    tracking.show()
    app.exec()