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
        HorizontalLayout = QtWidgets.QHBoxLayout()
        widget.setLayout(HorizontalLayout)
        
        plotWidget = pg.PlotWidget(widget)
        self.plot = plotWidget.plot([0,2,3,4],[2,3,4,-1],pen=None,symbol='o',symbolBrush=0.2)
        HorizontalLayout.addWidget(plotWidget)

        VerticalLayout = QtWidgets.QVBoxLayout()
        HorizontalLayout.addLayout(VerticalLayout)
        pointList = QtWidgets.QListWidget()
        #pointList.addItem()
        QtWidgets.QListWidgetItem("(1,2,3)",pointList)
        VerticalLayout.addWidget(pointList)
        setPoint_form = QtWidgets.QHBoxLayout()
        setPoint_form.addWidget(QtWidgets.QLabel("new pos"))
        setPoint_form.addWidget(QtWidgets.QLineEdit())
        setPoint_form.addWidget(QtWidgets.QLineEdit())
        setPoint_form.addWidget(QtWidgets.QLineEdit())
        VerticalLayout.addLayout(setPoint_form)
        self.setLayout(HorizontalLayout)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    tracking = TrackingWindow()
    tracking.show()
    app.exec()