"""
    Written by NirZ

from Mits.Connections import IConnection
from Mits.Configuration.Config import LOGS_ENABLED
class ConnectionUSB(IConnection.IConnection):
        self.configuration  = configuration
        self.__recv_buffer = ""
        self.timeout         = timeout
        if LOGS_ENABLED:
        if to_open_connection==True:

    @staticmethod
    def __repr__(self):
    def __del__(self):
     #   self.close()

    def connect(self, busy_waiting=False, configuration=None, interface=None, write_endpoint = None, read_endpoint = None):

        self.dev, devInfo = self.__get_device(self.vid, self.pid, busy_waiting)



        return True
    def is_conn_alive(self):
    def close(self):
        if LOGS_ENABLED:


    def control_msg(self, requesttype, request, buffer, value=0, index=0, timeout=0.1):
        if LOGS_ENABLED:
    def clear_halt(self, endpoint):
        return self.dev.clearHalt(endpoint)
    @staticmethod
    def __get_device(self, vid,pid, busy_waiting=False):
    def get_timeout(self):

    def set_timeout(self, timeout):
        if LOGS_ENABLED:
    def send(self, buf):
    def recv(self, size):

        if LOGS_ENABLED:
    def flush(self):