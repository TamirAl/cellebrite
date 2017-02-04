"""
    ConnectionUSB
    implements IConnection for serial connection


    Written by NirZ
"""




from Mits.Connections import IConnection
import usb,time
import logging


from Mits.Configuration.Config import LOGS_ENABLED
from Mits.Utils.Log import log


class ConnectionUSB(IConnection.IConnection):
    def __init__(self, vid, pid, configuration = 1, interface = 2, write_endpoint=2, 
                 read_endpoint=2, timeout = 0.1, to_open_connection=True, 
                 busy_waiting=False, probing_mode = None):
        
        self.d = None
        self.vid = vid
        self.pid = pid
        self.devnum = None
        self.is_init = False


        self.configuration  = configuration
        self.interface      = interface
        self.write_endpoint = write_endpoint
        self.read_endpoint  = read_endpoint


        self.__recv_buffer = ""


        self.timeout         = timeout


        if LOGS_ENABLED:
            self.__log = log("USB")


        if to_open_connection==True:
            self.connect(busy_waiting,configuration, interface, write_endpoint, read_endpoint)




    @staticmethod
    def seconds_to_ms(sec):
        return int(sec * 1000)


    def __repr__(self):
        txt = ""
        txt += "vid=%s, pid=%s,  configuration=%d,  interface=%d,  write_endpoint=%s,  read_endpoint=%s,  timeout=%d" % \
               (self.vid, self.pid, self.configuration, self.interface, str(self.write_endpoint), str(self.read_endpoint), self.timeout)
        return txt


    def __del__(self):
        if LOGS_ENABLED:
            self.__log.close()


     #   self.close()




    def connect(self, busy_waiting=False, configuration=None, interface=None, write_endpoint = None, read_endpoint = None):
        if configuration != None:
            self.configuration = configuration
        if interface != None:
            self.interface = interface
        if write_endpoint != None:
            self.write_endpoint = write_endpoint
        if read_endpoint != None:
            self.read_endpoint = read_endpoint




        self.dev, devInfo = self.__get_device(self.vid, self.pid, busy_waiting)
        self.devnum = devInfo.devnum
        self.is_init = True        
        self.dev.setConfiguration(self.configuration)
        if self.interface is not None:
            self.dev.claimInterface(self.interface)
            if not self.write_endpoint and not self.read_endpoint:                
                # This experimental code automatically sets the IN/OUT endpoint numbers of the interface, in case the caller didn't specify them.
                try:
                    # Go through all endpoints belonging to the chosen interface
                    cfg = [cfg for cfg in devInfo.configurations if cfg.value == self.configuration]
                    if cfg:
                        cfg = cfg[0]
                        interface = [inf[0] for inf in cfg.interfaces if inf[0].interfaceNumber == self.interface]
                        if interface:
                            interface = interface[0]
                            for ep in interface.endpoints:
                                # We only handle data endpoints.
                                if ep.type != usb.ENDPOINT_TYPE_BULK:
                                    continue
                                # If the EP address's MSB is set, it's IN, otherwise OUT.
                                dirIN = bool(ep.address >> 7)
                                epNum = ep.address & 0x7F # Take the address without the MSB.
                                if dirIN:
                                    if self.read_endpoint:
                                        logging.warning("Detected multiple IN endpoints. Using first (%d)" % self.read_endpoint)
                                    else:
                                        self.read_endpoint = epNum
                                        logging.debug("Detected IN endpoint %d" % epNum)
                                else:
                                    if self.write_endpoint:
                                        logging.warning("Detected multiple OUT endpoints. Using first (%d)" % self.write_endpoint)
                                    else:
                                        self.write_endpoint = epNum
                                        logging.debug("Detected OUT endpoint %d" % epNum)
                except:
                    import traceback
                    traceback.print_exc()
                    pass
        
        if LOGS_ENABLED:
            self.__log.text("New Connection!\r\n" +
                    "    VID  = %r\r\n"%(self.vid) +
                    "    PID  = %r\r\n"%(self.pid) +
                    "    Conf = %d\r\n"%(self.configuration) +
                    "    Interface = %d\r\n"%(self.interface) +
                    "    read endpoint  = %d\r\n"%(self.read_endpoint) +
                    "    write endpoint = %d\r\n"%(self.write_endpoint),
                    "CONNECT")








        return True


    def is_conn_alive(self):
        self.check_init()
        # First, let's validate the device is connected.
        found = False
        for bus in usb.busses():
            for device in bus.devices:
                # Find the device with the devnum of our device.
                if device.devnum == self.devnum:
                    # Validate it has the same PID and VID of our device
                    if device.idProduct in self.pid and device.idVendor in self.vid:
                        found = True
                        break
        if not found:
            return False
        # Now, let's get the device descriptor, just to validate the link is alive.
        try:
            self.dev.getDescriptor(1,0,256)
            return True
        except:
            return False
        


    def close(self):
        self.check_init()
        self.dev = None
        self.devnum = None
        self.is_init = False
        #        self.dev.releaseInterface()


        if LOGS_ENABLED:
            self.__log.text("Device Closed!", "CLOSE")






    def control_msg(self, requesttype, request, buffer, value=0, index=0, timeout=0.1):
        self.check_init()
        
        ret = self.dev.controlMsg(requesttype, request, buffer, value, 
                                  index, self.seconds_to_ms(timeout) )
        #it can return an int (for send), or array (for recv).
        # if an array, convert to string
        if isinstance(ret, int):
            return ret
        else:
            return "".join([chr(x) for x in ret])


        if LOGS_ENABLED:
            self.__log.text_buffer( "Request Type | Request | Value | index | timeout" +
                                    "0x%03X       | 0x%03X  | 0x%03X| 0x%03X| %d"%(requesttype, request, value, index, timeout),
                                    buffer, "CONTROL")


    def clear_halt(self, endpoint):
        self.check_init()


        return self.dev.clearHalt(endpoint)


    @staticmethod
    def get_connected_device():
        found = False
        res = None
        
        for bus in usb.busses():
            for device in bus.devices:
                if found:
                    raise Exception("More than one device connected and faked")
                found = True
                
                res = (device.idVendor, device.idProduct)
        return res
        
    def __find_device(self, vid, pid):
        for bus in usb.busses():
            for device in bus.devices:
                if device.idVendor in vid and device.idProduct in pid:
                    return device
        return None
        


    def __get_device(self, vid,pid, busy_waiting=False):
        if busy_waiting == False:
            device = self.__find_device(vid, pid)
            if device is None:
                raise Exception("Device not found!")
            return device.open(), device
        else:
            while(True):
                time.sleep(0.1)
                device = self.__find_device(vid, pid)
                if device is not None:
                    return device.open(), device


    def get_timeout(self):
        return self.timeout




    def set_timeout(self, timeout):
        self.timeout = timeout


        if LOGS_ENABLED:
            self.__log.text("new timeout: %d"%(timeout), "TIMEOUT")


    def send(self, buf):
        self.check_init()
        assert self.write_endpoint is not None
        try:
            if LOGS_ENABLED:
                self.__log.buffer(buf, "SEND")
            return self.dev.bulkWrite(self.write_endpoint, buf, self.seconds_to_ms(self.timeout))
        except usb.USBError, e:
            if e.args[0] == "usb_reap: timeout error":
                return 0
            else:
                raise e


    def recv(self, size):
        self.check_init()
        assert self.read_endpoint is not None
        chunk_size = 4096
        while (size > len(self.__recv_buffer)):
            try:
                data = self.dev.bulkRead(0x80+self.read_endpoint, chunk_size, self.seconds_to_ms(self.timeout))
                self.__recv_buffer += "".join([chr(x) for x in data])
            except usb.USBError, e:
                if "timeout error" in repr(e):
                    break
                else:
                    raise e
            if len(data) < chunk_size:
                break
        result = self.__recv_buffer[:size]
        self.__recv_buffer = self.__recv_buffer[size:]




        if LOGS_ENABLED:
            self.__log.buffer(result, "RECV")
        return result


    def flush(self):
        self.check_init()
        if LOGS_ENABLED:
            self.__log.text("flusing!", "FLUSH")
        while (self.recv(1024)):
            pass
