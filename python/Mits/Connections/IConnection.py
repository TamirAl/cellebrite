"""
    Written by NirZ
import time
class IConnection(object):
    def raw_send(self, data):
    def raw_recv(self, num_bytes):
    def set_timeout(self, timeout):
    def check_init(self):
        while (self.recv_no_wait()):

            

    def recv_wait(self, num_bytes = 1024, timeout = 10):
    # Method set the timeout to zero
    