from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
from AxisWidget.AxisWidget import AxisWidget
from settingsWidget.settingsWindow import SettingsWindow
from TrackingWindow.TrackingWindow import TrackingWindow

#from MotorsClass.mdrive_MOCK import Motor
from MotorsClass.mdrive import Motor
from time import sleep, time

import threading
from SESInterface.SESInterface import SES_API
import numpy as np
from time import time
import logging
from logging.handlers import TimedRotatingFileHandler


root = logging.getLogger()
root.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
root.addHandler(ch)

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
InfoLog = logging.handlers.TimedRotatingFileHandler('./logs/info.log', when='D', interval=1,
                                                    backupCount=7)  # log errors in a weekly file, save monthly backup
InfoLog.setLevel(logging.INFO)
InfoLog.setFormatter(formatter)
logger.addHandler(InfoLog)

Poslogger = logging.getLogger('Pos')
Poslogger.setLevel(logging.DEBUG)
PosLog = logging.handlers.TimedRotatingFileHandler('./logs/postion.log', when='D', interval=1,
                                                   backupCount=7)  # log errors in a weekly file, save monthly backup
PosLog.setLevel(logging.DEBUG)
PosLog.setFormatter(formatter)
Poslogger.addHandler(PosLog)


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
        self.settings_window.limitsChanged.connect(lambda name,h,l: self.changeLimits(name,h,l))
        self.settings_window.PositionIsSet.connect(lambda name,pos: self.redefineMotorPosition(name,pos) )
        self.settings_window.sendToSignalSet.connect(lambda set: self.sendToSignalSet(set))
        self.settings_window.show()

    def show_Tracking_window(self):
        self.Tracking_window = TrackingWindow(self.polar_vec,self.x_vec,self.y_vec)
        self.Tracking_window.VecsUpdated.connect(self.updateVec)
        self.Tracking_window.show()

    def updateVec(self,polar_vec,x_vec,y_vec):
        self.polar_vec = polar_vec
        self.x_vec = x_vec
        self.y_vec = y_vec

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
        Tracking_Btn.clicked.connect(self.show_Tracking_window)
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

        PolarLock_Btn = QtWidgets.QPushButton(U"🔒")
        PolarLock_Btn.setStyleSheet("QPushButton { font: 40px; }")
        PolarLock_Btn.setToolTip("Safe Mode")
        PolarLock_Btn.setCheckable(True)
        PolarLock_Btn.setChecked(False)
        PolarLock_Btn.toggled.connect(self.togglePolarLock)
        Button_Grid_layout.addWidget(PolarLock_Btn)

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
        LED_form.addRow("Movement Done ",self.manipulatorStopdMoving_LED)
        LED_form.setHorizontalSpacing(4)



        self.SESConnected = QtWidgets.QCheckBox()
        self.SESConnected.setTristate(True)
        self.SESConnected.setCheckState(Qt.CheckState.Unchecked)
        self.SESConnected.setEnabled(False)
        self.SESConnected.setStyleSheet(u"QCheckBox::indicator {\n"
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
                                                                        "}\n"
                                                                        "\n"
                                                                        "QCheckBox::indicator:partiallychecked {\n"
                                                                        "    background-color:       rgb(255, 255, 0);\n"
                                                                        "    border:                 2px solid black;\n"
                                                                        "}")
        self.SESConnected.setStyleSheet(u"QCheckBox::indicator {\n"
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
        LED_form.addRow("SES connection",self.SESConnected)

        Button_Grid_layout.addItem(LED_form)



        Stop_Btn = QtWidgets.QPushButton(U"🛑")
        Stop_Btn.setStyleSheet("QPushButton { font: 40px;}")
        Stop_Btn.setToolTip("Stop")
        Stop_Btn.clicked.connect(self.stop)
        Button_Grid_layout.addWidget(Stop_Btn)
        return Button_Grid_layout
    def CreateAxisLayout(self):
        self.axis = {}
        Axis_Grid_layout = QtWidgets.QGridLayout()
        Xaxis = AxisWidget("X",-20,20,pos_btn_txt=u"⇦",neg_btn_txt=u"⇨")
        Xaxis.MoveButtonClicked.connect(self.moveStep)
        Xaxis.GoToPosClicked.connect(self.go_to_pos)
        Xaxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(Xaxis)
        self.axis["X"] = Xaxis
        Yaxis = AxisWidget("Y",-10,10,pos_btn_txt=u"⊙",neg_btn_txt=u"⊗")
        Yaxis.MoveButtonClicked.connect(self.moveStep)
        Yaxis.GoToPosClicked.connect(self.go_to_pos)
        Yaxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Yaxis)
        self.axis["Y"] = Yaxis
        Zaxis = AxisWidget("Z",-135,0,pos_btn_txt=u"⇑",neg_btn_txt=u"⇓")
        Zaxis.MoveButtonClicked.connect(self.moveStep)
        Zaxis.GoToPosClicked.connect(self.go_to_pos)
        Zaxis.SetStep.connect(self.set_step)
        Axis_Grid_layout.addWidget(create_Hseperator())
        Axis_Grid_layout.addWidget(Zaxis)
        self.axis["Z"] = Zaxis
        #Paxis = AxisWidget(u"θ",-30,30,1)
        Paxis = AxisWidget("R",-30,30,1,pos_btn_txt=u"↺",neg_btn_txt=u"↻")
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
        self.Tracking_window = None
        self.threadpool = QtCore.QThreadPool()
        #locks:
        self.update_loop = threading.Event()
        self.serial_in_use = threading.Lock()
        self.serial_up = threading.Lock()
        self.stoped = threading.Event()

        window = QtWidgets.QWidget()
        layout = self.createLayout()
        window.setLayout(layout)
        self.setCentralWidget(window)

        self.moving = False
        self.PolarLock = False
        self.polar_vec = []
        self.x_vec = []
        self.y_vec = []

        self.sendToSignal = False

        self.motors = Motor()
        self.positions = dict()
        self.positions = {"X":0.0,"Y":0.0,"Z":0.0,"R":0.0}
        self.set_positions = dict() # this is the set positions... rather then the actual positions...
        self.allowd_range = {'X': (-10, 4), 'Y': (-9, 10), 'Z': ( -140,0), 'R': (-30, 15), 'P': (70, 200),
                        'T': (-400, 400)}  # this needs to be refined.
        self.step_sizes = {**self.motors.step}
        self.safeMode = True

    @QtCore.Slot(float)
    def set_step(self, ax, step):
        self.step_sizes[ax] = step
        if ax in self.motors.axes:
            self.serial_in_use.acquire(blocking=True, timeout=- 1) #this will wait until reading position is done.
            self.motors.step[ax] = step
            self.serial_in_use.release()

    @QtCore.Slot(bool)
    def set_safeMode(self,mode):
        logger.info('Safe mode on: {}'.format(mode))
        self.safeMode = mode


    @QtCore.Slot(float)
    def go_to_pos(self,ax,pos):
        
        #print(ax,pos)
        #logger.info('{} sent to: {}. position: {}.'.format(ax, pos, positions[ax]))
        if self.safeMode:
            if float(pos) < self.allowd_range[ax][0] or float(pos) > self.allowd_range[ax][1]:
                logger.info('{} Out of range: {} of {} '.format(ax, pos, self.allowd_range[ax]))
                return False

        self.moving = True
        self.set_positions[ax] = float(pos)
        if ax in self.motors.axes:
            self.serial_in_use.acquire(blocking=True, timeout=- 1) #this will wait until reading position is done.
            self.motors.go_to_pos(ax, float(pos))
            self.serial_in_use.release()

        self.stoped.clear() #initiated a new movement
        #eel.set_gui_moving(True)
        self.manipulatorStopdMoving_LED.setChecked(False)
        self.threadpool.start(self.check_movement)



    def moveStep(self,ax,direction):
        #logger.info('{} moved one step. direction:{}. current position: {}.'.format(ax, direction, self.positions[ax]))
        if self.safeMode:
            if (self.positions[ax] + direction * self.step_sizes[ax]) < self.allowd_range[ax][0] or (self.positions[ax] + direction * self.step_sizes[ax]) > self.allowd_range[ax][1]:
                logger.info('{} Out of range:{} of {} '.format(ax, self.positions[ax] + direction * self.step_sizes[ax], self.allowd_range[ax]))
                return False
        if ax in self.motors.axes:
            self.serial_in_use.acquire(blocking=True, timeout=- 1) #this will wait until reading position is done.
            self.motors.go_step(ax, direction)
            self.serial_in_use.release()

    def stop(self):
        self.serial_in_use.acquire(blocking=True, timeout=2)
        self.motors.stop()
        self.stoped.set()
        self.serial_in_use.release()


    def updateLoop(self):
        self.serial_up.acquire(blocking=False) #Do not close serial!
        last_update = time()
        while self.update_loop.is_set():
            self.serial_in_use.acquire(blocking=True, timeout=2) #this will wait for serial to clear (at most 2sec)
            for ax in self.motors.axes:
                pos = self.motors.get_pos(ax)
                if pos != 'Not Connected':
                    self.positions[ax] = float(pos)
                    self.axis[ax].setPosition(float(pos))
            self.serial_in_use.release()
            SESapi.pos = self.positions #this needs to speak the same language with API!
            if self.moving:
                SESapi.status = SES_API.ManipulatorStatus.MOVING
            else:
                SESapi.status = SES_API.ManipulatorStatus.DONE
            if self.Tracking_window is not None:
                if self.Tracking_window.isVisible():
                    if time()-last_update > 1:
                        last_update = time()
                        self.Tracking_window.update_current_position(self.positions["R"],self.positions["X"],self.positions["Y"])
            sleep(0.05)
        self.serial_up.release() #Now you can close the serial connection



    def check_movement(self):
        loop_start_time = time()
        while True:
            flag = True
            for ax in self.set_positions.keys():
                if round(self.set_positions[ax],2) != round(self.positions[ax],2): #changed from 3 to 2, 2 is enough.
                    flag = False

            if time() - loop_start_time > 30:   #if we wait more then ... seconds (!) just assume we have arrived.
                #send notification to signal!
                flag = True

            if flag:
                self.moving = False
                self.manipulatorStopdMoving_LED.setChecked(True)
                if self.Tracking_window is not None:
                    if self.Tracking_window.isVisible():
                        self.Tracking_window.update_position_graph(self.positions["R"],self.positions["X"],self.positions["Y"])

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
                if self.Tracking_window is not None:
                    #if self.Tracking_window.isVisible():
                    self.Tracking_window.update_position_graph(self.positions["R"],self.positions["X"],self.positions["Y"])
                return True

            sleep(0.05)

    def redefineMotorPosition(self,ax,pos):
        print(ax,pos)

        realPos = self.motors.set_pos(ax, float(pos))
        logger.info('Set Postion of {0} to: {1} (internal corr: {2})'.format(ax, pos, str(realPos)))

    def changeLimits(self,ax,low,high):
        logger.info('Set limit of {0} from ({1},{2})to: ({3},{4})'.format(ax,self.allowd_range[ax][0],self.allowd_range[ax][1], low,high))
        self.allowd_range[ax] = (low,high)

    def sendToSignalSet(self,set):
        self.sendToSignal = set
        print(set)

    def closeWindowCallback(self,SESapi):
        logger.info("closing motor connection.")
        self.update_loop.clear() # now update loop is shutting down
        SESapi.closeLoop()
        sleep(3)
        self.serial_up.acquire(blocking=True,timeout=15)
        self.motors.close()
        self.serial_up.release()

    def startUpdateLoop(self):
        self.update_loop.set()
        self.threadpool.start(self.updateLoop)


    def ChangeConnectionLED(self,state):
        if state == SES_API.ConnectionStatus.Listening:
            self.SESConnected.setCheckState(Qt.CheckState.PartiallyChecked)
        if state == SES_API.ConnectionStatus.Connected:
            print("green")
            self.SESConnected.setCheckState(Qt.CheckState.Checked)
        if state == SES_API.ConnectionStatus.Error:
            self.SESConnected.setCheckState(Qt.CheckState.Unchecked)

    @QtCore.Slot(bool)
    def togglePolarLock(self,state):
        logger.info('Polar Lock on: {}'.format(state))
        self.PolarLock = state


    def SESmove(self,axis,pos):
        #print("in SES")
        #print(axis,pos)
        assert axis == "R"
        pos = float(pos)
        #this will be called by the SES API to move an axis- probably the polar
        #print(self.PolarLock)
        #print(self.polar_vec)
        if not self.PolarLock:
            self.go_to_pos(axis, pos)
            return True
        else:
            #check if there is a polar data in current location,
            if pos in self.polar_vec:
                idx = self.polar_vec.index(pos)
                _x = self.x_vec[idx]
                _y = self.y_vec[idx]
                _P = self.polar_vec[idx]

            else:
                if((pos>max(self.polar_vec))or(pos<min(self.polar_vec))):
                    print("polar out of range.")
                    return False
                #if not, interpolat between nearest points.
                p_array = np.array(self.polar_vec)
                x_array = np.array(self.x_vec)
                y_array = np.array(self.y_vec)
                idx_sorted = p_array.argsort()

                _x = np.interp(pos, p_array[idx_sorted], x_array[idx_sorted], left=None, right=None, period=None)
                _y = np.interp(pos, p_array[idx_sorted], y_array[idx_sorted], left=None, right=None, period=None)
                _P = pos

            print("moving")
            print(_x,_y,_P)
            self.go_to_pos("X", _x)
            self.go_to_pos("Y", _y)
            self.go_to_pos("R",_P)

    def keyPressEvent(self,event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            pass
            #print(app.focusWidget().text)
        if event.key() == Qt.Key.Key_Escape:
            self.stop()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    window.startUpdateLoop()
    SESapi = SES_API()
    SESapi.ConnectionStatusChanged.connect(lambda state: window.ChangeConnectionLED(state))
    SESapi.Stop.connect(window.stop)
    SESapi.moveTo.connect(lambda _pos: window.SESmove("R",_pos))
    window.threadpool.start(SESapi.handle_connection)

    app.aboutToQuit.connect(lambda: window.closeWindowCallback(SESapi))



    app.exec()
