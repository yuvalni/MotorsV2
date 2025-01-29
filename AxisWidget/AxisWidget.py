from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt,Signal
import sys


class DoubleClickButton(QtWidgets.QPushButton):
    doubleClicked = Signal()
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:  # Check for left button double-click
            self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)



class AxisWidget(QtWidgets.QWidget):
    MoveButtonClicked = QtCore.Signal(str,float)
    DblMoveButtonClicked = QtCore.Signal(str,float)
    GoToPosClicked = QtCore.Signal(str,float)
    SetStep = QtCore.Signal(str,float)

    def __init__(self,name,min=-10,max=10,stepsizeDefault=0.1,pos_btn_txt =u"⇦" ,neg_btn_txt=u"⇨", *args, **kwargs):
        super(AxisWidget, self).__init__(*args, **kwargs)
        self.name = name
        
        
        layout = QtWidgets.QHBoxLayout()

        posBtn = DoubleClickButton(pos_btn_txt)
        posBtn.setStyleSheet('font: 40px;')
        posBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        posBtn.clicked.connect(lambda: self.buttonPress("positive"))
        posBtn.doubleClicked.connect(lambda: self.dblbuttonPress("positive"))
        layout.addWidget(posBtn)

        axisName = QtWidgets.QLabel("{}: ".format(name))
        axisName.setStyleSheet('font: 40px;')
        layout.addWidget(axisName)
        
        self.pos = QtWidgets.QLabel("0.00")
        self.pos.setStyleSheet('font: 40px;')
        layout.addWidget(self.pos)

        negBtn = DoubleClickButton(neg_btn_txt)
        negBtn.setStyleSheet('font: 40px;')
        negBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)

        negBtn.clicked.connect(lambda: self.buttonPress("negative"))
        negBtn.doubleClicked.connect(lambda: self.dblbuttonPress("negative"))

        layout.addWidget(negBtn)

        goToPointLayout = QtWidgets.QVBoxLayout()
        goToPointForm = QtWidgets.QFormLayout()
        self.GoToPos = QtWidgets.QDoubleSpinBox()
        self.GoToPos.setMaximum(max)
        self.GoToPos.setMinimum(min)
        self.GoToPos.setStyleSheet('font: 20px;')
        goToPointForm.addRow("go to:",self.GoToPos)
        #goToPointForm.setStyleSheet('font: 40px;')
    
        GoToPosBtn = QtWidgets.QPushButton("Go")
        GoToPosBtn.clicked.connect(self.GoToPosClicked_func)
        StepSizeBtn = QtWidgets.QPushButton("Set step")
        StepSizeBtn.clicked.connect(self.SetStepClicked)
        self.SetStepSize = QtWidgets.QDoubleSpinBox(value=stepsizeDefault)
        goToPointForm.addRow("set Step size:",self.SetStepSize)

        goToPointForm.addRow(GoToPosBtn,StepSizeBtn)
        goToPointLayout.addLayout(goToPointForm)

#        goToPointLayout.addWidget(GoToPosBtn)



        layout.addLayout(goToPointLayout)

        self.setLayout(layout)

    def buttonPress(self,direction):
        if direction == 'positive':
            self.MoveButtonClicked.emit(self.name,1)
        else:
            self.MoveButtonClicked.emit(self.name,-1)

    def dblbuttonPress(self,direction):
        if direction == 'positive':
            self.DblMoveButtonClicked.emit(self.name,1)
        else:
            self.DblMoveButtonClicked.emit(self.name,-1)

    def GoToPosClicked_func(self):
        self.GoToPosClicked.emit(self.name,self.GoToPos.value())

    def SetStepClicked(self):
        self.SetStep.emit(self.name,self.SetStepSize.value())

    def setPosition(self,pos):
        self.pos.setText("{:0.2f}".format(pos))
        #self.pos.setNum(round(pos,2))


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Xaxis = AxisWidget("X")
    Xaxis.show()
    app.exec()