"""
    Interface for connections
    Most of the methods require the connection to be
    initialized and connected before they called


    Written by NirZ
"""


import time


class IConnection(object):
    def __init__(self):
        self.is_init= False
    
    def connect(self):
        raise Exception(NotImplemented)
		
    def close(self):
        raise Exception(NotImplemented)
		
    def send(self, data):
        raise Exception(NotImplemented)
		
    def recv(self, num_bytes):
        raise Exception(NotImplemented)


    def raw_send(self, data):
        return self.send(data)


    def raw_recv(self, num_bytes):
        return self.recv(num_bytes)


    def set_timeout(self, timeout):
        raise Exception(NotImplemented)
    
    def get_timeout(self):
        raise Exception(NotImplemented)


    def check_init(self):
        if not (self.is_init):
            raise Exception("Device Not Initialized")
            
    def is_inited(self):
        return self.is_init
        
    def flush(self):
        self.check_init()


        while (self.recv_no_wait()):
            pass
                
    def reconnect(self, max_wait = 120):
        start_time = time.time()
        if (self.is_inited()):
            self.close()
        while (time.time() - start_time < max_wait):
            try:
                self.connect()
                print 
                break
            except Exception, e:
                time.sleep(1)
                print ".",




            




    def recv_wait(self, num_bytes = 1024, timeout = 10):
        self.check_init()
        
        tmp_timeout = self.get_timeout()
        self.set_timeout(timeout)
        data = self.recv(num_bytes)
        self.set_timeout(tmp_timeout)
        return data
        


    # Method set the timeout to zero
    # do the recv, and return the original timeout value
    def recv_no_wait(self, num_bytes = 1024):
        return self.recv_wait(num_bytes, timeout = 0)


    
    # Methods relevant only to Serial connection
    # Defined in order to keep the same interface
    def set_baudrate(self, baud):
        pass
    def set_parity(self, par):
        pass
    def set_dtr(self, n):
        pass
    def set_rts(self, n):
        pass
    def set_byte_size(self, n):
        pass
        
    # Methods relevant only to USB connection
    # Defined in order to keep the same interface
    def control_msg(self, requesttype, request, value, index, timeout):
        pass
    def clear_halt(self, endpoint):
        pass
