import socketfrom time import sleep
from Mits.Connections import IConnectionfrom Mits.Configuration.Config import LOGS_ENABLEDfrom Mits.Utils.Log import log 
class ConnectionSocket(IConnection.IConnection):    def __init__(self, ip="localhost", port = 0, timeout = 5, to_open_connection=True):            self.ip         = ip        self.port       = port        self.timeout    = timeout        self.is_init    = False                if LOGS_ENABLED:            self.__log = log("SOCKET")
        if to_open_connection==True:            self.connect()
    def __del__(self):        if LOGS_ENABLED:            self.__log.close()
    def __repr__(self):        txt = ""        txt += "IP=%r, Port=%r" % (self.ip, self.port)        return txt        
    def get_port(self):        return self.port        def set_port(self, port):        self.port = port
    def connect(self, blocking=False):        if (self.is_init):            print "Device already connected!"            return False                self.dev = socket.socket()        self.dev.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        self.dev.connect((self.ip,self.port))        self.is_init = True        return True
    def close(self):        self.check_init()        self.dev.close()        self.is_init = False

    def send(self, data):        self.check_init()        if LOGS_ENABLED:                self.__log.buffer(data, "SEND")        return self.dev.send(data)
    def recv(self, num_bytes = 1024):        self.check_init()        data = self.dev.recv(num_bytes)        if LOGS_ENABLED:                self.__log.buffer(data, "RECV")        return data

    def get_timeout(self):        self.check_init()        return self.dev.getTimeout()
        def set_timeout(self, timeout):        print "Setting timeout"        self.check_init()        self.dev.settimeout(timeout)        self.dev.setblocking(1)
