"""
    ConnectionNull
    implements IConnection for Dummy connection
    can be used for tests


    Written by NirZ
"""


import serial
from Mits.Connections import IConnection


class ConnectionNull(IConnection.IConnection):
    def __init__(self):
        self.is_init    = False
        self.connect()




    def connect(self, blocking = False):
        if (self.is_init):
            print "Device already connected!"
            return False
        print "Device Connected"
        self.is_init = True
        return True


    def close(self):
        self.check_init()


        print "Device Disconnected"
        self.is_init = False




    def send(self, data):
        self.check_init()
        print "Sending: ", repr(data)        
        return len(data)




    def recv(self, num_bytes = 1024):
        self.check_init()
        return raw_input("Receiving data: ")




    def get_timeout(self):
        self.check_init()
        return self.timeout
    
    def set_timeout(self, timeout):
        self.check_init()
        self.timeout = timeout
