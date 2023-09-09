from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
from AxisWidget.AxisWidget import AxisWidget
from settingsWidget.settingsWindow import SettingsWindow
from MotorsClass.mdrive_MOCK import Motor
from time import sleep
import threading


        
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




class MainWindow(QtWidgets.QMainWindow):
    def show_settings_window(self):
        self.settings_window = SettingsWindow(self.allowd_range,self.positions)
        self.settings_window.limitsChanged.connect(lambda name,h,l: print(name,h,l))
        self.settings_window.PositionIsSet.connect(lambda name,pos: print(name,pos) )
        self.settings_window.show()

    def CreateButtonPanel(self):
        Button_Grid_layout = QtWidgets.QGridLayout()
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
        SafeMode_Btn.toggled.connect(self.set_safeMode)
        #SafeMode_Btn.toggled.connect()  This will pass True/False if btn is checked or not.
        Button_Grid_layout.addWidget(SafeMode_Btn)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        Button_Grid_layout.addItem(verticalSpacer)

        
        LED_form = QtWidgets.QFormLayout()
        self.manipulatorStopdMoving_LED = QtWidgets.QCheckBox()
        self.manipulatorStopdMoving_LED.setChecked(True)
        self.manipulatorStopdMoving_LED.setEnabled(False)


        self.manipulatorStopdMoving_LED.setStyleSheet(u"QCheckBox::indicator {\n"
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
        LED_form.addRow("Stoped Moving ",self.manipulatorStopdMoving_LED)
        

        
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
        return Button_Grid_layout
    def CreateAxisLayout(self):
        self.axis = {}
        Axis_Grid_layout = QtWidgets.QGridLayout()
        Xaxis = AxisWidget("X",-20,20)
        Xaxis.MoveButtonClicked.connect(self.moveStep)
        Xaxis.GoToPosClicked.connect(self.go_to_pos)
        Xaxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(Xaxis)
        self.axis["X"] = Xaxis
        Yaxis = AxisWidget("Y",-10,10)
        Yaxis.MoveButtonClicked.connect(self.moveStep)
        Yaxis.GoToPosClicked.connect(self.go_to_pos)
        Yaxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Yaxis)
        self.axis["Y"] = Yaxis
        Zaxis = AxisWidget("Z",-135,0)
        Zaxis.MoveButtonClicked.connect(self.moveStep)
        Zaxis.GoToPosClicked.connect(self.go_to_pos)
        Zaxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Zaxis)
        self.axis["Z"] = Zaxis
        #Paxis = AxisWidget(u"θ",-30,30,1)
        Paxis = AxisWidget("R",-30,30,1)
        Paxis.MoveButtonClicked.connect(self.moveStep)
        Paxis.GoToPosClicked.connect(self.go_to_pos)
        Paxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Paxis)
        #self.axis["θ"] = Paxis
        self.axis["R"] = Paxis
        return Axis_Grid_layout
    
    def createLayout(self):
        layout = QtWidgets.QHBoxLayout()
        Axis_Grid_layout = self.CreateAxisLayout()
        
        layout.addLayout(Axis_Grid_layout)
        layout.addWidget(create_Vseperator())
        buttonPanel = self.CreateButtonPanel()
        layout.addLayout(buttonPanel)
        return layout
    

    def __init__(self,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool()
        #locks:
        self.update_loop = threading.Event()
        self.serial_up = threading.Lock()
        self.stoped = threading.Event()

        window = QtWidgets.QWidget()
        layout = self.createLayout()
        window.setLayout(layout)
        self.setCentralWidget(window)

        self.moving = False
        self.PolarLock = False

        self.motors = Motor()
        self.positions = dict()
        self.positions = {"X":0,"Y":0,"Z":0,"R":0}
        self.set_positions = dict() # this is the set positions... rather then the actual positions...
        self.allowd_range = {'X': (-10, 3), 'Y': (-9, 11.5), 'Z': ( -165,0), 'R': (-30, 2), 'P': (70, 200),
                        'T': (-400, 400)}  # this needs to be refined.
        self.step_sizes = {**self.motors.step}
        self.safeMode = True

    @QtCore.Slot(float)
    def set_step(self, ax, step):
        self.step_sizes[ax] = step
        if ax in self.motors.axes:
            self.motors.step[ax] = step
    
    @QtCore.Slot(bool)
    def set_safeMode(self,mode):
        self.safeMode = mode
    
    @QtCore.Slot(float)
    def go_to_pos(self,ax,pos):
        #logger.info('{} sent to: {}. position: {}.'.format(ax, point, positions[ax]))
        if self.safeMode:
            if float(pos) < self.allowd_range[ax][0] or float(pos) > self.allowd_range[ax][1]:
                #logger.info('{} Out of range: {} of {} '.format(ax, point, allowd_range[ax]))
                return False

        self.moving = True
        self.set_positions[ax] = float(pos)
        if ax in self.motors.axes:
            self.motors.go_to_pos(ax, float(pos))

        self.stoped.clear() #initiated a new movement
        #eel.set_gui_moving(True)
        self.manipulatorStopdMoving_LED.setChecked(False)
        self.threadpool.start(self.check_movement)
        


    def moveStep(self,ax,direction):
        #logger.info('{} moved one step. direction:{}. current position: {}.'.format(ax, way, positions[ax]))
        if self.safeMode:
            if (self.positions[ax] + direction * self.step_sizes[ax]) < self.allowd_range[ax][0] or (self.positions[ax] + direction * self.step_sizes[ax]) > self.allowd_range[ax][1]:
                #logger.info('{} Out of range:{} of {} '.format(ax, positions[ax] + way * step_sizes[ax], allowd_range[ax]))
                return False
        if ax in self.motors.axes:
            self.motors.go_step(ax, direction)

    def updateLoop(self):
        self.serial_up.acquire(blocking=False) #Do not close serial!
        while self.update_loop.is_set():
            for ax in self.motors.axes:
                pos = self.motors.get_pos(ax)
                if pos != 'Not Connected':
                    self.positions[ax] = float(pos)
                    self.axis[ax].setPosition(float(pos))
            #api.pos = positions #this needs to speak the same language with API!
            #if moving:
            #    api.status = Status.MOVING
            #    eel.set_gui_moving(True)
            #else:
            #    api.status = Status.DONE
            #    eel.set_gui_moving(False)
            sleep(0.05)
        self.serial_up.release() #Now you can close the serial connection

    def startUpdateLoop(self):
        self.update_loop.set()
        self.threadpool.start(self.updateLoop)
        
    def check_movement(self):
        while True:
            flag = True
            for ax in self.set_positions.keys():
                if round(self.set_positions[ax],3) != round(self.positions[ax],3):
                    flag = False
            if flag:
                self.moving = False
                self.manipulatorStopdMoving_LED.setChecked(True)
                return True
            if self.stoped.is_set():
                self.stoped.clear()
                #if stoped is pressed. movement is done!
                #so set the set_pos to be the current one,
                #end we have finished movement!
                for ax in self.set_positions.keys():
                    self.set_positions[ax] = self.positions[ax]
                self.moving = False
                self.manipulatorStopdMoving_LED.setChecked(True)
                return True

            sleep(0.05)

    def closeWindowCallback(self):
        print("closing motor connection.")
        self.update_loop.clear() # now update loop is shutting down
        sleep(3)
        self.serial_up.acquire(blocking=True,timeout=15)
        self.motors.close()

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindow()
    app.aboutToQuit.connect(window.closeWindowCallback)
    window.show() 
    window.startUpdateLoop()
    app.exec()