from enum import Enum

import re
from select import select
from time import sleep
from PySide6.QtCore import Signal,QObject,Slot

import win32pipe, win32file, pywintypes

pipe_name = r'\\.\pipe\manipulatorPipe'

class SES_API(QObject):
    class ManipulatorStatus(Enum):
        MOVING = 0
        DONE = 1
        ABORTED = 2
        ERROR = 3

    class ConnectionStatus(Enum):
        Error = 0
        Listening = 1
        Connected = 2

    ConnectionStatusChanged = Signal(object)
    Stop = Signal()
    moveTo = Signal(float)
    

    def __init__(self):
        super(SES_API,self).__init__()
        self.run = True
        
        self.pipe = win32pipe.CreateNamedPipe(
            pipe_name,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None
        )
        self.status =  self.ManipulatorStatus.DONE
        self.pos = {"R":0.0,"T":0.0,"P":0.0,"X":0.0,"Y":0.0,"Z":0.0}
        self.move_reg = re.compile('(X|Y|Z|R|T|P)([+-]?([0-9]*[.])?[0-9]+)') #capturing X or Y or Z and float number
        self.pos_reg = re.compile('(X|Y|Z|R|T|P)(\?)') #capturing X or Y or Z and float number
        self.listening = False
        self.connected = False

        #P - polar T- tilt  F - phi

    def move(self,data):
        self.status = self.ManipulatorStatus.MOVING
        m = self.move_reg.findall(data)
        print(m)
        if m:
            axis, pos  = m[0][0] , m[0][1]
            self.moveTo.emit(float(pos))
            print(axis,pos)
        else:
            print("no axis found.")

    def send_pos(self,data):
         #axis = self.pos_reg.search(data.decode("UTF-8")).group(0)
         axis = data.replace("?","")
         print('sending pos')

         #Currently we do not implement T and phi
         if "T" in axis:
            response = "0.0\n"
            win32file.WriteFile(self.pipe, response.encode())
            return True
         if "P" in axis:
             response = "0.0\n"
             win32file.WriteFile(self.pipe, response.encode())
             return True
         response = "{}\n".format(self.pos[axis])
         print(response)
         win32file.WriteFile(self.pipe, response.encode())    
        

    def stop(self):
        print('stoping')
        self.Stop.emit()

    def send_status(self):
        print('send status',self.status)
        response = "{}\n".format(self.status.value)
        win32file.WriteFile(self.pipe, response.encode())

    def handle_req(self,data):
        #print(data)
        if "STATUS" in data:
            self.send_status()
        else:
            self.send_pos(data)

    @Slot()
    def closeLoop(self):
        print("closing SES loop.")
        self.run = False

    def handle_connection(self):#this is main loop.
        print(self.ConnectionStatus.Connected)
        self.ConnectionStatusChanged.emit(self.ConnectionStatus.Error)

        while self.run:
            print("listening")
            self.listening = True
            self.ConnectionStatusChanged.emit(self.ConnectionStatus.Listening)
            win32pipe.ConnectNamedPipe(self.pipe, None)
            self.ConnectionStatusChanged.emit(self.ConnectionStatus.Connected)
            while self.run:
                try:
                    # Read data from the pipe
                    #print("waiting for data.")
                    result, data = win32file.ReadFile(self.pipe, 64 * 1024)
                    #print("Received:", data.decode())
                    

                    if data == b'':

                        sleep(0.01)
                        continue

                    for data in data.decode("UTF-8").split('\n'):

                        if("?" in data):
                            self.handle_req(data) #Handle data request
                        elif "MOV" in data: #MOVX5.0 for example
                            self.move(data) #handle move request
                        elif "STOP" in data:
                            self.stop()
                        else:
                            if data!=r"\n":
                                #print(data) # anything else please?
                                pass

                        if data == "exit":
                            # closing connection, but awaiting another one...
                            self.connected = False
                            break
                except pywintypes.error as e:
                    if e.winerror == 109:  # ERROR_BROKEN_PIPE
                        print("Client disconnected")
                        break
                sleep(0.01)


            sleep(0.1)
        win32file.CloseHandle(self.pipe)