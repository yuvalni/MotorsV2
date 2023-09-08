from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys


class AxisWidget(QtWidgets.QWidget):

    def __init__(self,name,min=-10,max=10,stepsizeDefault=0.1, *args, **kwargs):
        super(AxisWidget, self).__init__(*args, **kwargs)

        
        
        layout = QtWidgets.QHBoxLayout()

        leftBtn = QtWidgets.QPushButton(u"⇦")
        leftBtn.setStyleSheet('font: 40px;')
        leftBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        layout.addWidget(leftBtn)

        axisName = QtWidgets.QLabel("{}: ".format(name))
        axisName.setStyleSheet('font: 40px;')
        layout.addWidget(axisName)
        
        pos = QtWidgets.QLabel("0.00")
        pos.setStyleSheet('font: 40px;')
        layout.addWidget(pos)

        rightBtn = QtWidgets.QPushButton(u"⇨")
        rightBtn.setStyleSheet('font: 40px;')
        rightBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
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


        

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Xaxis = AxisWidget("X")
    Xaxis.show()
    app.exec_()