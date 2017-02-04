"""
    ConnectionSerial
    implements IConnection for serial connection


    Written by NirZ
"""


import serial
from Mits.Connections import IConnection
from Mits.Utils.UI    import get_serial_port


class ConnectionSerial(IConnection.IConnection):
    def __init__(self, port = None, baud=115200, par=serial.PARITY_NONE, timeout=5,to_open_connection=True):
        if (None == port and to_open_connection==True):
            port = get_serial_port()
                            
        self.port       = port
        self.baud       = baud
        self.parity     = par
        self.timeout    = timeout
        self.is_init    = False


        if to_open_connection==True:
            while(True):
                try:
                    self.connect()
                    break
                except Exception, e:
                    print "ConnectionSerial:  ", e, "\r\n"
                    self.port = get_serial_port()
                    continue
        


    def __repr__(self):
        txt = ""
        txt += "Port=%d, Baudrate=%d, Parity=%s, Timeout=%d" % (self.port, \
                                                                     self.baud, \
                                                                     self.parity, \
                                                                     self.timeout )
        return txt
        


    def get_port(self):
        return self.port
    
    def set_port(self, port):
        self.port = port


    def connect_aux(self, blocking=False):
        if (self.is_init):
            print "Device already connected!"
            return False
        
        self.dev = serial.Serial(port=self.port - 1, baudrate=self.baud, parity=self.parity, timeout=self.timeout)
        self.is_init = True
        return True


    def connect(self, blocking=False):        
        while True :
            try :
                return self.connect_aux(blocking)                
            except Exception, e:
                if not blocking :
                    raise
                continue
        








    def close(self):
        self.check_init()


        self.dev.close()
        self.is_init = False




    def send(self, data):
        self.check_init()


        return self.dev.write(data)




    def recv(self, num_bytes = 1024):
        self.check_init()
        return self.dev.read(num_bytes)




    def get_timeout(self):
        self.check_init()
        return self.dev.getTimeout()


    
    def set_timeout(self, timeout):
        self.check_init()
        self.dev.setTimeout(timeout)


        
    def set_baudrate(self, baud):
        self.check_init()
        self.baud = baud
        return self.dev.setBaudrate(self.baud)
        
    def set_parity(self, par):
        self.check_init()
        return self.dev.setParity(par)
    
    def set_rts(self, n):
        self.check_init()
        return self.dev.setRTS(n)
        
    def set_dtr(self, n):
        self.check_init()
        return self.dev.setDTR(n)
     
    def set_byte_size(self, n):
        self.check_init()
        return self.dev.setByteSize(n)
