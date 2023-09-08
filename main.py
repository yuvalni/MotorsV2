from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
from AxisWidget.AxisWidget import AxisWidget
from settingsWindow import SettingsWindow

asdjlkad
def create_Hseperator():
    seperator = QtWidgets.QFrame()
    seperator.setFrameShape(QtWidgets.QFrame.HLine)
    seperator.setLineWidth(3)
    return seperator
def create_Vseperator():
    seperator = QtWidgets.QFrame()
    seperator.setFrameShape(QtWidgets.QFrame.VLine)
    seperator.setLineWidth(3)
    return seperator




class MainWindow(QtWidgets.QWidget):
    def show_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def __init__(self,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QtWidgets.QHBoxLayout()

        Axis_Grid_layout = QtWidgets.QGridLayout()
        layout.addLayout(Axis_Grid_layout)
        Button_Grid_layout = QtWidgets.QGridLayout()
        layout.addWidget(create_Vseperator())
        layout.addLayout(Button_Grid_layout)
        Xaxis = AxisWidget("X",-20,20)

        #X_dock = QtWidgets.QDockWidget()
        #X_dock.setWidget(Xaxis)
        #X_dock.setFloating(False)
        Axis_Grid_layout.addWidget(Xaxis)

        Yaxis = AxisWidget("Y",-10,10)
        
        #Y_dock = QtWidgets.QDockWidget()
        #Y_dock.setFloating(False)
        #Y_dock.setWidget(Yaxis)

        
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Yaxis)
        
        Zaxis = AxisWidget("Z",-135,0)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Zaxis)

        Paxis = AxisWidget(u"θ",-30,30,1)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Paxis)
        
        

        Settings_Btn = QtWidgets.QPushButton(U"⚙️")
        Settings_Btn.setStyleSheet("QPushButton { font: 40px; }")
        Settings_Btn.setToolTip("Settings")
        Button_Grid_layout.addWidget(Settings_Btn)

        Settings_Btn.pressed.connect(self.show_settings_window)

        CopyPos_Btn = QtWidgets.QPushButton(U"📋")
        CopyPos_Btn.setStyleSheet("QPushButton { font: 40px; }")
        CopyPos_Btn.setToolTip("Copy Position to clipboard")
        Button_Grid_layout.addWidget(CopyPos_Btn)

        Tracking_Btn = QtWidgets.QPushButton(U"🗺️")
        Tracking_Btn.setStyleSheet("QPushButton { font: 40px; }")
        Tracking_Btn.setToolTip("Track XY Polar map")
        Button_Grid_layout.addWidget(Tracking_Btn)

        SafeMode_Btn = QtWidgets.QPushButton(U"👶")
        SafeMode_Btn.setStyleSheet("QPushButton { font: 40px; }")
        SafeMode_Btn.setToolTip("Safe Mode")
        SafeMode_Btn.setCheckable(True)
        SafeMode_Btn.setChecked(True)
        #SafeMode_Btn.toggled.connect()  This will pass True/False if btn is checked or not.
        Button_Grid_layout.addWidget(SafeMode_Btn)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        Button_Grid_layout.addItem(verticalSpacer)

        
        LED_form = QtWidgets.QFormLayout()
        manipulatorStopdMoving_LED = QtWidgets.QCheckBox()
        manipulatorStopdMoving_LED.setStyleSheet(u"QCheckBox::indicator {\n"
                                                                        "    width:                  20px;\n"
                                                                        "    height:                 20px;\n"
                                                                        "    border-radius:          5px;\n"
                                                                        "}\n"
                                                                        "\n"
                                                                        "QCheckBox::indicator:checked {\n"
                                                                        "    background-color:       rgb(85, 255, 0);\n"
                                                                        "    border:                 2px solid black;\n"
                                                                        "}\n"
                                                                        "\n"
                                                                        "QCheckBox::indicator:unchecked {\n"
                                                                        "    background-color:       rgb(255, 0, 0);\n"
                                                                        "    border:                 2px solid black;\n"
                                                                        "}")
        LED_form.addRow("Moving ",manipulatorStopdMoving_LED)
        

        
        SESConnected = QtWidgets.QCheckBox()
        SESConnected.setStyleSheet(u"QCheckBox::indicator {\n"
                                                                        "    width:                  20px;\n"
                                                                        "    height:                 20px;\n"
                                                                        "    border-radius:          5px;\n"
                                                                        "}\n"
                                                                        "\n"
                                                                        "QCheckBox::indicator:checked {\n"
                                                                        "    background-color:       rgb(85, 255, 0);\n"
                                                                        "    border:                 2px solid black;\n"
                                                                        "}\n"
                                                                        "\n"
                                                                        "QCheckBox::indicator:unchecked {\n"
                                                                        "    background-color:       rgb(255, 0, 0);\n"
                                                                        "    border:                 2px solid black;\n"
                                                                        "}")
        LED_form.addRow("SES con.",SESConnected)
        
        Button_Grid_layout.addItem(LED_form)
        


        Stop_Btn = QtWidgets.QPushButton(U"🛑")
        Stop_Btn.setStyleSheet("QPushButton { font: 40px;}")
        Stop_Btn.setToolTip("Stop")
        Button_Grid_layout.addWidget(Stop_Btn)
        #window = QtWidgets.QMainWindow()
        #window = QtWidgets.QWidget()
        #window.setCentralWidget(layout)
        #window.addDockWidget(QtCore.Qt.TopDockWidgetArea,X_dock)
        #window.addDockWidget(QtCore.Qt.RightDockWidgetArea,Y_dock)
        #window.setCentralWidget(None)
        self.setLayout(layout)
        #window.setDockNestingEnabled(True)
        
    

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyleSheet("QPushButton { font: 40px; }")
    window = MainWindow()
    window.show() 
    
    app.exec()