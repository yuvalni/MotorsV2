from enum import Enum
import socket
import re
from select import select
from time import sleep
from PySide6.QtCore import Signal



class SES_API:
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
    moveTo = Signal(str,float)
    
    def __init__(self):
        self.HOST = "127.0.0.1" 
        self.PORT = 5011  # Port to listen on
        self.status =  self.ManipulatorStatus.DONE
        self.conn = None
        self.pos = {"R":0.0,"T":0.0,"P":0.0,"X":0.0,"Y":0.0,"Z":0.0}
        self.move_reg = re.compile('(X|Y|Z|R|T|P)([+-]?([0-9]*[.])?[0-9]+)') #capturing X or Y or Z and float number
        self.pos_reg = re.compile('(X|Y|Z|R|T|P)(\?)') #capturing X or Y or Z and float number
        self.listening = False
        self.connected = False

        #P - polar T- tilt  F - phi

    def move(self,data):
        self.status = self.ManipulatorStatus.MOVING
        m = self.move_reg.findall(data)
        if m:
            axis, pos  = m[0][0] , m[0][1]
            self.moveTo.emit(axis,pos)
            print(axis,pos)
        else:
            print("no axis found.")

    def send_pos(self,data):
         #axis = self.pos_reg.search(data.decode("UTF-8")).group(0)
         axis = data.replace("?","")
         #print('sending pos')
         #print("{}\n".format(self.pos[axis]))
         self.conn.send("{}\n".format(self.pos[axis]).encode())

    def stop(self):
        print('stoping')
        self.Stop.emit()

    def send_status(self):
        print('send status',self.status)
        self.conn.send("{}\n".format(self.status.value).encode())

    def handle_req(self,data):
        #print(data)
        if "STATUS" in data:
            self.send_status()
        else:
            self.send_pos(data)

    def handle_connection(self):#this is main loop.
        self.ConnectionStatusChanged.emit(self.ConnectionStatus.Error)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setblocking(True)
            s.settimeout(0.01)
            s.bind((self.HOST, self.PORT))
            s.listen()

            while True:
                print("listening")
                self.listening = True
                self.ConnectionStatusChanged.emit(self.ConnectionStatus.Listening)
                read,write,_ = select([s],[s],[],0.01)
                while(not read):
                    #waiting for connection without blocking
                    #This works good
                    read, write, _ = select([s], [s], [],0)
                    sleep(0.1)

                self.conn, addr = s.accept()
                self.conn.settimeout(0.1)
                with self.conn:
                    self.ConnectionStatusChanged.emit(self.ConnectionStatus.Connected)
                    self.listening = False
                    self.connected = True
                    print("Connected by {}".format(addr))

                    while self.connected:
                        #we are stuck here!
                        try:
                            data = self.conn.recv(512)
                        except socket.timeout as e:
                            #print(e)
                            #print("non blocking")
                            sleep(0.1)
                            continue

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

                            if data=="exit":
                                # closing connection, but awaiting another one...
                                self.connected = False
                                break

                        sleep(0.01)


                sleep(0.1)