from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
from settingsWidget.settingsWidget import SettingsWidget




class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout()
        xSettings = SettingsWidget("X axis")
        ySettings = SettingsWidget("Y axis")
        zSettings = SettingsWidget("Z axis")
        layout.addWidget(xSettings)
        layout.addWidget(ySettings)
        layout.addWidget(zSettings)
        self.setLayout(layout)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)

    
    settings = SettingsWindow()

    
    settings.show()
    app.exec()