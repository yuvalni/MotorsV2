from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
import pyqtgraph as pg


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class TrackingWindow(QtWidgets.QWidget):
    NewPointAdded = QtCore.Signal(float,float,float)
    def __init__(self,P_vec=[],X_vec=[],Y_vec=[], *args, **kwargs):
        super(TrackingWindow, self).__init__(*args, **kwargs)
        self.P_vec = P_vec
        self.X_vec = X_vec
        self.Y_vec = Y_vec
        widget = QtWidgets.QWidget()
        HorizontalLayout = QtWidgets.QHBoxLayout()
        widget.setLayout(HorizontalLayout)
        
        plotWidget = pg.PlotWidget(widget)
        plotItem = plotWidget.getPlotItem()
        

        HorizontalLayout.addWidget(plotWidget)

        VerticalLayout = QtWidgets.QVBoxLayout()
        HorizontalLayout.addLayout(VerticalLayout)
        self.pointList = QtWidgets.QListWidget()
        
        #QtWidgets.QListWidgetItem("(1,2,3)",self.pointList)
        VerticalLayout.addWidget(self.pointList)
        
        if len(self.P_vec) == 0:
            self.Xplot = plotItem.plot(pen=None,symbol='o',symbolBrush=(0,0,200))    
            self.Yplot = plotItem.plot(pen=None,symbol='o',symbolBrush=(255,140,0))    
        else:
            self.Xplot = plotItem.plot(self.P_vec,self.X_vec,pen=None,symbol='o',symbolBrush=(0,0,200))
            self.Yplot = plotItem.plot(self.P_vec,self.Y_vec,pen=None,symbol='o',symbolBrush=(255,140,0))
            self.loadVecToList()
        
        SetNewPoint_group = QtWidgets.QGroupBox("New Point")
        #SetNewPoint_group.setStyleSheet("QGroupBox{font: 24px;}")
        SetNewPoint_grid = QtWidgets.QGridLayout() 
        SetNewPoint_group.setLayout(SetNewPoint_grid)
        self.SetNewPoint_P = QtWidgets.QLineEdit()
        self.SetNewPoint_X = QtWidgets.QLineEdit()
        self.SetNewPoint_Y = QtWidgets.QLineEdit()
        SetNewPoint_P_label = QtWidgets.QLabel("R")
        SetNewPoint_X_label = QtWidgets.QLabel("X")
        SetNewPoint_Y_label = QtWidgets.QLabel("Y")
        SetNewPoint_grid.addWidget(SetNewPoint_P_label,0,0)
        SetNewPoint_grid.addWidget(self.SetNewPoint_P,1,0)
        SetNewPoint_grid.addWidget(SetNewPoint_X_label,0,1)
        SetNewPoint_grid.addWidget(self.SetNewPoint_X,1,1)
        SetNewPoint_grid.addWidget(SetNewPoint_Y_label,0,2)
        SetNewPoint_grid.addWidget(self.SetNewPoint_Y,1,2)
        SetNewPoint_Btn = QtWidgets.QPushButton("add Point")
        SetNewPoint_Btn.clicked.connect(self.addNewPoint)
        SetNewPoint_grid.addWidget(SetNewPoint_Btn,1,3)


        DelPoint_Btn = QtWidgets.QPushButton("Delete Point")
        DelPoint_Btn.clicked.connect(self.DelPoint)
        VerticalLayout.addWidget(DelPoint_Btn)
        
        VerticalLayout.addWidget(SetNewPoint_group)

        self.setLayout(HorizontalLayout)

    def addNewPoint(self):
        P = self.SetNewPoint_P.text()
        X = self.SetNewPoint_X.text()
        Y = self.SetNewPoint_Y.text()
        if P == '' or X=='' or Y=='':
            return False
        P = float(P)
        X = float(X)
        Y = float(Y)
        self.P_vec.append(P)
        self.X_vec.append(X)
        self.Y_vec.append(Y)
        self.Xplot.setData(self.P_vec,self.X_vec)
        self.Yplot.setData(self.P_vec,self.Y_vec)
        QtWidgets.QListWidgetItem("({0},{1},{2})".format(P,X,Y),self.pointList)
        self.pointList.sortItems()
        self.NewPointAdded.emit(P,X,Y)

    def loadVecToList(self):
        for p,x,y in zip(self.P_vec,self.X_vec,self.Y_vec):
            QtWidgets.QListWidgetItem("({0},{1},{2})".format(p,x,y),self.pointList)
        self.pointList.sortItems()

    def DelPoint(self):
        print(self.pointList.currentItem())
        print(self.pointList.currentRow())

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    tracking = TrackingWindow(P_vec=[1,2,3,4],X_vec=[2.1,2.3,2.5,3],Y_vec=[5,4.9,4.6,4.2])
    tracking.show()
    app.exec()