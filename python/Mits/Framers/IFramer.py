from Mits.Connections.IConnection import IConnection
class IFramer(IConnection):    """    this is the basic framer. every other framer must inharit from it.    """
    name = "Null"
    def __init__(self, base):        self.base = base
    def connect(self):        self.base.connect()
    def close(self):        self.base.close()
    def send(self, data):        return self.base.send(data)
    def recv(self, num_bytes = 1024):        return self.base.recv(num_bytes)
    def recv_no_wait(self, num_bytes = 1024):        return self.base.recv_no_wait(num_bytes)
    def recv_wait(self, num_bytes = 1024, timeout = 10):        return self.base.recv_wait(num_bytes, timeout)
    #do not overload this function - so you can send raw data    def raw_send(self, data):        return self.base.raw_send(data)
    #do not overload this function - so you can send raw data    def raw_recv(self, num_bytes = 1024):        return self.base.raw_recv(num_bytes)
    def set_timeout(self, timeout):        self.base.set_timeout(timeout)
    def get_timeout(self):        return self.base.get_timeout()
    def flush(self):        self.base.flush()
    #serial functions    def set_parity(self, par):        return self.base.set_parity(par)
    def set_baudrate(self, baud):        return self.base.set_baudrate(baud)
    def set_dtr(self, n):        return self.base.set_dtr(n)
    def set_rts(self, n):        return self.base.set_rts(n)
    def set_byte_size(self, n):        return self.base.set_byte_size(n)
    #usb functions    def control_msg(self, requesttype, request, value, index, timeout):        return self.base.control_msg(requesttype, request, value, index, timeout)
    def clear_halt(self, endpoint):        return self.base.clear_halt(endpoint)