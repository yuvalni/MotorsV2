from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys




class SettingsWidget(QtWidgets.QWidget):
    limitsChanged = QtCore.Signal(float,float)
    PositionIsSet = QtCore.Signal(float)
    def __init__(self,axis_name,allowed_range,pos, *args, **kwargs):
        super(SettingsWidget, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout()

        x_group = QtWidgets.QGroupBox("{}".format(axis_name))
        x_group.setStyleSheet("QGroupBox{font: 24px;}")
        vbox = QtWidgets.QVBoxLayout()
        x_group.setLayout(vbox)
        layout.addWidget(x_group)

        form = QtWidgets.QFormLayout()
        double_validator = QtGui.QDoubleValidator()

        self.LowLimit = QtWidgets.QLineEdit()
        self.LowLimit.setValidator(double_validator)
        self.LowLimit.setText(str(allowed_range[0]))
        form.addRow("Lower Limit",self.LowLimit)

        self.HighLimit = QtWidgets.QLineEdit()
        self.HighLimit.setValidator(double_validator)
        self.HighLimit.setText(str(allowed_range[1]))
        form.addRow("Higher Limit",self.HighLimit)


        vbox.addLayout(form)
        setLimitsBtn = QtWidgets.QPushButton("Set")
        vbox.addWidget(setLimitsBtn)
        setLimitsBtn.clicked.connect(self.limitSet)

        UpdateCurrentPos_form = QtWidgets.QFormLayout()
        self.update_pos = QtWidgets.QLineEdit()
        self.update_pos.setValidator(double_validator)
        self.update_pos.setText(str(pos))
        UpdateCurrentPos_form.addRow("Set Current position to: ",self.update_pos)
        update_pos_Btn = QtWidgets.QPushButton("change position")
        update_pos_Btn.clicked.connect(self.setPosition)
        vbox.addLayout(UpdateCurrentPos_form)
        vbox.addWidget(update_pos_Btn)

        self.setLayout(layout)

    def limitSet(self):
        self.limitsChanged.emit(float(self.LowLimit.text()),float(self.HighLimit.text()))

    def setPosition(self):
        self.PositionIsSet.emit(float(self.update_pos.text()))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    settings = SettingsWidget("x",(-10,2),3.4)
    settings.show()
    app.exec()
