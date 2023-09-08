from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys


class AxisWidget(QtWidgets.QWidget):
    MoveButtonClicked = QtCore.Signal(str,float)

    def __init__(self,name,min=-10,max=10,stepsizeDefault=0.1, *args, **kwargs):
        super(AxisWidget, self).__init__(*args, **kwargs)
        self.name = name
        
        
        layout = QtWidgets.QHBoxLayout()

        leftBtn = QtWidgets.QPushButton(u"⇦")
        leftBtn.setStyleSheet('font: 40px;')
        leftBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        leftBtn.clicked.connect(lambda: self.buttonPress("left"))
        layout.addWidget(leftBtn)

        axisName = QtWidgets.QLabel("{}: ".format(name))
        axisName.setStyleSheet('font: 40px;')
        layout.addWidget(axisName)
        
        self.pos = QtWidgets.QLabel("0.00")
        self.pos.setStyleSheet('font: 40px;')
        layout.addWidget(self.pos)

        rightBtn = QtWidgets.QPushButton(u"⇨")
        rightBtn.setStyleSheet('font: 40px;')
        rightBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)

        rightBtn.clicked.connect(lambda: self.buttonPress("right"))

        layout.addWidget(rightBtn)

        goToPointLayout = QtWidgets.QVBoxLayout()
        goToPointForm = QtWidgets.QFormLayout()
        GoToPos = QtWidgets.QDoubleSpinBox()
        GoToPos.setMaximum(max)
        GoToPos.setMinimum(min)
        GoToPos.setStyleSheet('font: 20px;')
        goToPointForm.addRow("go to:",GoToPos)
        #goToPointForm.setStyleSheet('font: 40px;')
    
        GoToPosBtn = QtWidgets.QPushButton("Go")
        StepSizeBtn = QtWidgets.QPushButton("Set step")
        SetStepSize = QtWidgets.QDoubleSpinBox(value=stepsizeDefault)
        goToPointForm.addRow("set Step size:",SetStepSize)

        goToPointForm.addRow(GoToPosBtn,StepSizeBtn)
        goToPointLayout.addLayout(goToPointForm)

#        goToPointLayout.addWidget(GoToPosBtn)



        layout.addLayout(goToPointLayout)

        self.setLayout(layout)

    def buttonPress(self,direction):
        if direction == 'right':
            self.MoveButtonClicked.emit(self.name,1)
        else:
            self.MoveButtonClicked.emit(self.name,-1)

    def setPosition(self,pos):
        self.pos.setNum(pos)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Xaxis = AxisWidget("X")
    Xaxis.show()
    app.exec()