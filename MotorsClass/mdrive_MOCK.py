from time import sleep
import re
import traceback

class Motor(object):
    """class which controls the X,Y,Z,R motors.
        """

    def __init__(self, port='COM11', timeout=1):
        print('init.')
        self.port = port
        self.timeout = timeout
        self.axes = ['X', 'Y', 'Z', 'R']
        self.pos = {"X":0,"Y":0,"Z":0,"R":0}
        self.cr = dict()
        self.cr["X"] = -0.0000026043
        self.cr["Y"] = -0.0000026043
        self.cr["R"] = -0.000070309
        self.cr["Z"] = -0.00000495547

        self.step = dict()
        self.step["X"] = 0.1
        self.step["Y"] = 0.1
        self.step["R"] = 0.5
        self.step["Z"] = 0.1
        self.connected = False

        try:
            #self.ser = serial.Serial(self.port, timeout=self.timeout)
            self.connected = True
            #self.read_all_positions()

        except Exception as e:
            traceback.print_exc()
            print('not connected')
            self.connected = False

        if self.connected:
            pass
            #self.set_limits()

    def close(self):
        return True
        if self.ser.is_open:
            self.write("XS")
            sleep(30/1000)
            self.write("YS")
            sleep(30 / 1000)
            self.write("ZS")
            sleep(30 / 1000)
            self.write("RS")
            self.ser.close()
            print('serial is closed.')
        else:
            print('serial is already closed.')

    def write(self, string):
        # maybe flush line
        pass
        #self.ser.write(str.encode(string + chr(10)))

    def read(self):
        line = self.ser.readline()
        return line

    def flush(self):
        sleep(30 / 1000)
        self.ser.read_all()

    def set_limits(self):
        #This is wrong!
        return True
        self.write("XVM=50000")
        self.flush()
        self.write("YVM=50000")
        self.flush()
        self.write("ZVM=100000")
        self.flush()
        self.write("RVM=20000")
        self.flush()
        self.write("XLM=5")
        self.flush()
        self.write("YLM=5")
        self.flush()
        self.write("ZLM=5")
        self.flush()

    def read_all_positions(self):
        # this updates the Position
        for ax in self.axes:
            self.get_pos(ax)

    def get_pos(self, axis):
        return "{:.3f}".format(self.pos[axis])
        if not self.connected:
            return 'Not Connected'
        if axis in self.axes:
            str_pr = '{0}PR P'.format(axis)
            self.write(str_pr)  # ask for axis Position
            sleep(30 / 1000)
            reply = str(self.ser.read_all())
            if len(re.findall('-?\d{1,}', reply))==0:
                return 'Not Connected'
            string_pos = re.findall('-?\d{1,}', reply)[0]
            self.pos[axis] = float(string_pos) * self.cr[axis]
            return "{:.3f}".format(self.pos[axis])
        return 'No Axes'

    def set_pos(self, axis, pos):

#        //self.ser.flush()
        assert axis == "Y" or axis == "X" or axis == "Z" or axis == "R"
        self.pos[axis] = pos
        return True
        pos = int(pos / self.cr[axis])
        assert pos < 2147483647 and pos > -2147483648  # driver limits
        self.write('{0}P={1}'.format(axis, pos))  # tell the motor its current position is pos
        self.flush()
        sleep(30 / 1000)
        return pos

    def go_to_pos(self, axis, pos):
        sleep(0.03)
        self.pos[axis] = pos
        return True
        self.ser.flush()
        assert axis == "Y" or axis == "X" or axis == "Z" or axis == "R"
        pos = int(pos / self.cr[axis])
        assert pos < 2147483647 and pos > -2147483648  # driver limits
        self.pos[axis] = float(pos) * self.cr[axis]
        print(axis + ": " + str(round(self.pos[axis], 3)))
        self.write('{0}MA {1},0,0'.format(axis,pos)) #set position return when finish
        self.flush()

    def go_step(self, axis, way):
        self.go_to_pos(axis, self.pos[axis] + way * self.step[axis])

    def stop(self):
        return True
        self.write(chr(27))
        self.flush()
