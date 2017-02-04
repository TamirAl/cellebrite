"""    ConnectionSerial    Implements IConnection for serial over FTDI connection"""
from Mits.Utils.upy import upyfrom PythonExt          import gpg, ftdi, parityfrom IConnection import IConnection

#from serial           import PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACEPARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'from copy             import *
class ConnectionSerial(IConnection):    def __init__(self, port = None, baud=115200, par=PARITY_NONE, timeout=5, to_open_connection=True):        #self.serial  = gpg(upy.instance, baud, self.__to_upy_parity(par))        self.serial  = ftdi(upy.instance, baud, self.__to_upy_parity(par))        self.is_init = False        self.baud    = baud
        self.serial.set_timeout(timeout)
        if to_open_connection == True:            self.connect()

    def __repr__(self):        txt = ""        txt += "Baudrate=%d, Parity=%s, Timeout=%d" % (self.baud, \                                                       self.parity, \                                                       self.timeout )        return txt

    def __to_upy_parity(self, par):        if   par == PARITY_NONE:  return parity.parity_none        elif par == PARITY_EVEN:  return parity.parity_even        elif par == PARITY_ODD:   return parity.parity_odd        elif par == PARITY_MARK:  return parity.parity_mark        elif par == PARITY_SPACE: return parity.parity_space        else:                     raise Exception("unknown parity value")

    def get_port(self):        #print "#### get_port()"        return -1

    def set_port(self, port):        #print "#### set_port()"        pass

    def connect(self):        #print "#### connect()"        self.serial.connect()        self.is_init = True        return True

    def close(self):        #print "#### close()"        self.is_init = False        self.serial.close()

    def send(self, data):        #print "#### Sending (" + str(len(data)) + "): " + repr(data)        result = self.serial.send(data, len(data))        #print "#### Sent " + str(result)        return result

    def recv(self, num_bytes = 1024):        #print "#### recv() num_bytes: " + str(num_bytes) + " timeout: " + str(self.get_timeout())        buffer = '\x00' * (num_bytes + 1) # force buffer copy on slice        read = self.serial.read(buffer, num_bytes)        data = deepcopy(buffer[:read])        #print "#### Received (" + str(read) + "):" + repr(data[:read])        return data

    def get_timeout(self):        return self.serial.get_timeout()

    def set_timeout(self, timeout): # sec        self.serial.set_timeout(timeout)

    def set_baudrate(self, baud):        #print "#### set_baud(" + str(baud) + ")"        self.serial.set_baud(baud)

    def set_parity(self, par):        self.serial.set_parity(self.__to_upy_parity(par))

    def set_rts(self, n):        #print "#### set_rts(" + str(n) + ")"        self.serial.set_rts(n)

    def set_dtr(self, n):        #print "#### set_dtr(" + str(n) + ")"        self.serial.set_dtr(n)

    def set_byte_size(self, n):        #print "#### set_byte_size(" + str(n) + ")"        self.check_init()        pass
