from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
from settingsWidget.settingsWidget import SettingsWidget




class SettingsWindow(QtWidgets.QWidget):
    limitsChanged = QtCore.Signal(str,float,float)
    PositionIsSet = QtCore.Signal(str,float)

    def __init__(self,allowd_range,positions, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        layout = QtWidgets.QGridLayout()
        xSettings = SettingsWidget("X axis",allowd_range["X"],positions["X"])
        xSettings.limitsChanged.connect(lambda high,low: self.limitsChanged.emit("X",high,low) )
        xSettings.PositionIsSet.connect(lambda pos: self.PositionIsSet.emit("X",pos))

        ySettings = SettingsWidget("Y axis",allowd_range["Y"],positions["Y"])
        ySettings.limitsChanged.connect(lambda high,low: self.limitsChanged.emit("Y",high,low) )
        ySettings.PositionIsSet.connect(lambda pos: self.PositionIsSet.emit("Y",pos))

        zSettings = SettingsWidget("Z axis",allowd_range["Z"],positions["Z"])
        zSettings.limitsChanged.connect(lambda high,low: self.limitsChanged.emit("Z",high,low) )
        zSettings.PositionIsSet.connect(lambda pos: self.PositionIsSet.emit("Z",pos))

        pSettings = SettingsWidget("θ axis",allowd_range["R"],positions["R"])
        pSettings.limitsChanged.connect(lambda high,low: self.limitsChanged.emit("R",high,low) )
        pSettings.PositionIsSet.connect(lambda pos: self.PositionIsSet.emit("R",pos))
        layout.addWidget(xSettings,0,0)
        layout.addWidget(ySettings,1,0)
        layout.addWidget(zSettings,0,1)
        layout.addWidget(pSettings,1,1)
        self.setLayout(layout)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    allowd_range = {'X': (-10, 3), 'Y': (-9, 11.5), 'Z': ( -165,0), 'R': (-30, 2), 'P': (70, 200),
                        'T': (-400, 400)}  # this needs to be refined.
    positions = {"X":0,"Y":0,"Z":0,"R":0}
    
    settings = SettingsWindow(allowd_range,positions)

    
    settings.show()
    app.exec()