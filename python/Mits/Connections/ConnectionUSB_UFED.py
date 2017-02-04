"""
    ConnectionUSB UFED
"""


from Mits.Utils.upy import upy


from Mits.Connections.IConnection import IConnection
from Mits.Connections.ConnectionUSBProbing     import USBProbing
from Mits.Configuration.Config                 import LOGS_ENABLED
#from Log                     import log


LOGS_ENABLED = False


import time


# descriptor type
DESC_TYPE_DEVICE = 0x01
DESC_TYPE_CONFIG = 0x02
DESC_TYPE_STRING = 0x03
DESC_TYPE_INTERFACE = 0x04
DESC_TYPE_ENDPOINT = 0x05


# endpoint direction
ENDPOINT_IN = 0x80
ENDPOINT_OUT = 0x00


# endpoint type
ENDPOINT_TYPE_CTRL = 0x00
ENDPOINT_TYPE_ISO = 0x01
ENDPOINT_TYPE_BULK = 0x02
ENDPOINT_TYPE_INTR = 0x03


# control request type
CTRL_TYPE_STANDARD = (0 << 5)
CTRL_TYPE_CLASS = (1 << 5)
CTRL_TYPE_VENDOR = (2 << 5)
CTRL_TYPE_RESERVED = (3 << 5)


# control request recipient
CTRL_RECIPIENT_DEVICE = 0
CTRL_RECIPIENT_INTERFACE = 1
CTRL_RECIPIENT_ENDPOINT = 2
CTRL_RECIPIENT_OTHER = 3


# control request direction
CTRL_OUT = 0x00
CTRL_IN = 0x80




class ConnectionUSB(IConnection):


    def __init__(self, vid, pid, configuration = 1, interface = 2, 
                 write_endpoint=2, read_endpoint=2, timeout = 0.1,
                 to_open_connection=True, busy_waiting=False, probing_mode = None):
        
        self.vid = vid
        self.pid = pid
        self.configuration  = configuration
        self.interface      = interface
        self.write_endpoint = write_endpoint
        self.read_endpoint  = read_endpoint
        self.is_init         = False
        self.timeout         = timeout
        self.recv_buffer     = ''
        self.prev_probing    = None


        if LOGS_ENABLED:
            self.__log = log("USB")


        if to_open_connection==True:
            self.connect(False, 0, 0, 0, 0, probing_mode)


        self.set_timeout(timeout)


    @staticmethod
    def seconds_to_ms(sec):
        return int(sec * 1000)


    def __repr__(self):
        txt = ""
        txt += "vid=%s, pid=%s,  configuration=%d,  interface=%d,  write_endpoint=%d,  read_endpoint=%d,  timeout=%d" % \
               (self.vid, self.pid, self.configuration, self.interface, self.write_endpoint, self.read_endpoint, self.timeout)
        return txt




    def __del__(self):
        if LOGS_ENABLED:
            self.__log.close()




    def __to_ufed_probing_mode(self, probing_mode):
        if probing_mode == USBProbing.fbus_probing:
            return upy.usb_probing_mode.fbus_probing
        elif probing_mode == USBProbing.at_probing:
            return upy.usb_probing_mode.at_probing
        elif probing_mode == USBProbing.at_probing:
            return upy.usb_probing_mode.at_probing
        elif probing_mode == USBProbing.at_with_vendor_probing:
            return upy.usb_probing_mode.at_with_vendor_probing
        elif probing_mode == USBProbing.generic_obex_probing:
            return upy.usb_probing_mode.generic_obex_probing
        elif probing_mode == USBProbing.nok7160_obex_probing:
            return upy.usb_probing_mode.nok7160_obex_probing
        elif probing_mode == USBProbing.nokS40_obex_probing:
            return upy.usb_probing_mode.nokS40_obex_probing
        elif probing_mode == USBProbing.CDC_at_probing:
            return upy.usb_probing_mode.CDC_at_probing
        elif probing_mode == USBProbing.Client_probing:
            return upy.usb_probing_mode.Client_probing
        elif probing_mode == USBProbing.vendor_no_probing:
            return upy.usb_probing_mode.vendor_no_probing
        elif probing_mode == USBProbing.qcp_info_probing:
            return upy.usb_probing_mode.qcp_info_probing
        elif probing_mode == USBProbing.vendor_interval_no_probing:
            return upy.usb_probing_mode.vendor_interval_no_probing
        elif probing_mode == USBProbing.vendor_BB_find_Endpoint:
            return upy.usb_probing_mode.vendor_BB_find_Endpoint
        elif probing_mode == USBProbing.zte_info_probing:
            return upy.usb_probing_mode.zte_info_probing
        elif probing_mode == USBProbing.no_probing_use_previous_info:
            return upy.usb_probing_mode.no_probing_use_previous_info
        elif probing_mode == USBProbing.qcp_filesystem_probing:
            return upy.usb_probing_mode.qcp_filesystem_probing
        elif probing_mode == USBProbing.p2k_probing:
            return upy.usb_probing_mode.p2k_probing
        elif probing_mode == USBProbing.unknown_no_probing:
            return upy.usb_probing_mode.unknown_no_probing
        elif probing_mode == USBProbing.generic_obex_probing_no_disconnect:
            return upy.usb_probing_mode.generic_obex_probing_no_disconnect
        elif probing_mode == USBProbing.at_probing_control_interface:
            return upy.usb_probing_mode.at_probing_control_interface
        elif probing_mode == USBProbing.at_probing_ctl_with_interrupt:
            return upy.usb_probing_mode.at_probing_ctl_with_interrupt
        elif probing_mode == USBProbing.at_probing_thuraya_class:
            return upy.usb_probing_mode.at_probing_thuraya_class
        elif probing_mode == USBProbing.com_control_no_probing:
            return upy.usb_probing_mode.com_control_no_probing
        elif probing_mode == USBProbing.com_data_no_probing:
            return upy.usb_probing_mode.com_data_no_probing
        elif probing_mode == USBProbing.printer_no_probing:
            return upy.usb_probing_mode.printer_no_probing
        elif probing_mode == USBProbing.at_probing_thuraya_interrupt:
            return upy.usb_probing_mode.at_probing_thuraya_interrupt
        elif probing_mode == USBProbing.mass_storage_no_probing:
            return upy.usb_probing_mode.mass_storage_no_probing
        elif probing_mode == USBProbing.android_adb_probe:
            return upy.usb_probing_mode.android_adb_probe
        elif probing_mode == USBProbing.qcp_status_probing:
            return upy.usb_probing_mode.qcp_status_probing
        elif probing_mode == USBProbing.obex_linux_probing:
            return upy.usb_probing_mode.obex_linux_probing
        elif probing_mode == USBProbing.at_no_ctrl_lines_probing:
            return upy.usb_probing_mode.at_no_ctrl_lines_probing
        elif probing_mode == USBProbing.at_zte_u210_probing:
            return upy.usb_probing_mode.at_zte_u210_probing
        elif probing_mode == USBProbing.android_adb_probe_with_clear:
            return upy.usb_probing_mode.android_adb_probe_with_clear
        elif probing_mode == USBProbing.at_willcom_with_vendor_probing:
            return upy.usb_probing_mode.at_willcom_with_vendor_probing
        elif probing_mode == USBProbing.Nexperia_protocol_probing:
            return upy.usb_probing_mode.Nexperia_protocol_probing
        elif probing_mode == USBProbing.qcp_info_com_control:
            return upy.usb_probing_mode.qcp_info_com_control
        elif probing_mode == USBProbing.qcp_download_mode_probing:
            return upy.usb_probing_mode.qcp_download_mode_probing
        elif probing_mode == USBProbing.at_LG_probing:
            return upy.usb_probing_mode.at_LG_probing
        else:
            raise Exception('Unknown probing mode: %s' % probing_mode)






    def connect(self, busy_waiting=False, configuration=None, interface=0, write_endpoint=1, read_endpoint=2, probing_mode_list = None):
        TIMEOUT_CONNECTION = 120 # 2 minutes
        if probing_mode_list is None :
            probing_mode = [USBProbing.at_probing]
            if self.prev_probing != None :
                probing_mode = self.prev_probing
        else :
            probing_mode = probing_mode_list


        if self.is_init:
            self.close()
            time.sleep(8)


        print "#### connect(%s)" % probing_mode_list
        res = upy.instance.com_connect()        
        if not res :
            print "Failed to connect to USB"
            return False 
        
        start_time = time.time()
        while not upy.instance.com_connected(upy.side.source):
            print "."
            time.sleep(0.1)
            cur_time = time.time()
            if cur_time - start_time > TIMEOUT_CONNECTION :
                print "Failed to connect to USB - TIMEOUT(%s)" % TIMEOUT_CONNECTION 
                return False
                


        upy.instance.com_set_config(0x80, True)


        if probing_mode_list != None :
            self.prev_probing = probing_mode_list


        for probing_mode_i in probing_mode :
            if upy.instance.usb_probe_interface(self.__to_ufed_probing_mode(probing_mode_i)) :
                break


        time.sleep(0.02)


        self.is_init = True


        if LOGS_ENABLED:
            self.__log.text("New Connection!\r\n", "CONNECT")


        return True




    def close(self):
        print "#### close()"
        self.check_init()


        upy.instance.com_disconnect()


        self.is_init = False


        if LOGS_ENABLED:
            self.__log.text("Device Closed!", "CLOSE")






    def control_msg(self, requesttype, request, buffer, value=0, index=0, timeout=0.1):
        self.check_init()


        if (requesttype & 0x80) == 0: # out
            return upy.instance.usb_control_transfer(requesttype, request, value, index, buffer, len(buffer))
        else: # in
            size = buffer
            bufferData = "\x00" * (size + 1) # force realloc
            print "#### usb_control_transfer(" + str(requesttype) + ", " + str(request) + ", " + str(value) + ", " + str(index) + ", " + str(bufferData) + ", " + str(size)
            read = upy.instance.usb_control_transfer(requesttype, request, value, index, bufferData, size)
            return bufferData[:read]


        if LOGS_ENABLED:
            self.__log.text_buffer( "Request Type | Request | Value | index | timeout" +
                                    "0x%03X       | 0x%03X  | 0x%03X| 0x%03X| %d"%(requesttype, request, value, index, timeout),
                                    buffer, "CONTROL")


    def clear_halt(self, endpoint):
        print "#### clear_halt()"
        self.check_init()


        # TODO




    def get_timeout(self):
        return self.timeout




    def set_timeout(self, timeout):
        self.timeout = timeout


        if LOGS_ENABLED:
            self.__log.text("new timeout: %d"%(timeout), "TIMEOUT")


        print "#### setting timeout to " + str(timeout)


        upy.instance.usb_set_read_timeout(self.seconds_to_ms(timeout))
        upy.instance.usb_set_write_timeout(self.seconds_to_ms(timeout))


    def send(self, buf):
        self.check_init()


        if LOGS_ENABLED:
            self.__log.buffer(buf, "SEND")


        #print "#### sending:" + repr(buf)


        return upy.instance.io_send(buf, len(buf))




    def recv(self, size):
        self.check_init()


        chunk_size = 4096
        while (size > len(self.recv_buffer)):
            buffer = '\x00' * (chunk_size+1)
            read = upy.instance.io_receive(buffer, chunk_size)
            if (read == -1):
                raise Exception("Connection with the device is damaged - aborting")
            self.recv_buffer += buffer[:read]


            if read < chunk_size:
                break


        result = self.recv_buffer[:size]
        self.recv_buffer = self.recv_buffer[size:]


        if LOGS_ENABLED:
            self.__log.buffer(result, "RECV")


        return result




    def flush(self):
        self.check_init()


        if LOGS_ENABLED:
            self.__log.text("flusing!", "FLUSH")


        while (self.recv(1024)):
            pass

