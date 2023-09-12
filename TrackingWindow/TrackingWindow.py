from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
import pyqtgraph as pg


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class TrackingWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TrackingWindow, self).__init__(*args, **kwargs)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)
        
        plotWidget = pg.PlotWidget(widget)
        self.plot = plotWidget.plot(pen=None,symbol='o',symbolBrush=0.2)
        layout.addWidget(plotWidget)
        self.plot.plot([0,1],[2,3])
        self.setLayout(layout)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    tracking = TrackingWindow()
    tracking.show()
    app.exec()