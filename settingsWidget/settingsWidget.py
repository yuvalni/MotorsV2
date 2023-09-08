from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys




class SettingsWidget(QtWidgets.QWidget):
    def __init__(self,axis_name, *args, **kwargs):
        super(SettingsWidget, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout()

        x_group = QtWidgets.QGroupBox("{}".format(axis_name))
        x_group.setStyleSheet("QGroupBox{font: 24px;}")
        vbox = QtWidgets.QVBoxLayout()
        x_group.setLayout(vbox)
        layout.addWidget(x_group)

        form = QtWidgets.QFormLayout()
        double_validator = QtGui.QDoubleValidator()

        LowLimit = QtWidgets.QLineEdit()
        LowLimit.setValidator(double_validator)
        form.addRow("Lower Limit",LowLimit)

        HighLimit = QtWidgets.QLineEdit()
        HighLimit.setValidator(double_validator)
        form.addRow("Higher Limit",HighLimit)


        vbox.addLayout(form)
        vbox.addWidget(QtWidgets.QPushButton("Set"))

        UpdateCurrentPos_form = QtWidgets.QFormLayout()
        update_pos = QtWidgets.QLineEdit()
        update_pos.setValidator(double_validator)
        UpdateCurrentPos_form.addRow("Set Current position to: ",update_pos)
        update_pos_Btn = QtWidgets.QPushButton("change position")

        vbox.addLayout(UpdateCurrentPos_form)
        vbox.addWidget(update_pos_Btn)

        self.setLayout(layout)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    settings = SettingsWidget("x")
    settings.show()
    app.exec()
