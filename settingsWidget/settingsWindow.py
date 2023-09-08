from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
from settingsWidget.settingsWidget import SettingsWidget




class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        layout = QtWidgets.QGridLayout()
        xSettings = SettingsWidget("X axis")
        ySettings = SettingsWidget("Y axis")
        zSettings = SettingsWidget("Z axis")
        pSettings = SettingsWidget("θ axis")
        layout.addWidget(xSettings,0,0)
        layout.addWidget(ySettings,1,0)
        layout.addWidget(zSettings,0,1)
        layout.addWidget(pSettings,1,1)
        self.setLayout(layout)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)

    
    settings = SettingsWindow()

    
    settings.show()
    app.exec()