"""    The framer add CRC16 and escape data with "\x7E"
    Written by NirZ    		Modified 2012-04-17 by Andrey Zagrebin to support    non-standard CRC and byte order, specifically those    used in the Spreatdrum phones (Crc16A, Big-endian)"""

import timefrom Mits.Framers.IFramer import IFramerfrom Mits.Utils.Crc       import Crc16CCITfrom Mits.Utils.General   import pack16L, pack16B
class FramerQC_HDLC(IFramer):    name = "HDLCFramer"        def hdlc_escape(self, data):        """        escape data with HDLC         """
        out_data = ""
        #excape data        for ch in data:            #check if need escaping            if ord(ch) in [0x7E, 0x7D]: # removed the 0x7f for tfs dump.                #escape                out_data += "\x7D"                out_data += chr(ord(ch) ^ 0x20)            else:                # no escaping                out_data += ch
        return out_data
                    def __init__(self, base, escaping = True, special_header = "",                 crc_big_endian = False, crc_calculator = None, empty_header = False):        self.base             = base        self.__escaping       = escaping        self.__tx_escape      = escaping        self.__rx_escape      = escaping
        self.__empty_header   = empty_header # Adding an option for the header to be empty        self.__special_header = special_header # a header to replace the 7E        if (None == crc_calculator):            self.__crc_calculator = Crc16CCIT()        else:            self.__crc_calculator = crc_calculator        self.__crc_big_endian = crc_big_endian

    def send(self, data, empty_header = False):
        crc = self.__crc_calculator.calc(data)        if self.__crc_big_endian:            data += pack16B(crc)        else:            data += pack16L(crc)                        if (self.__tx_escape):            data = self.hdlc_escape(data)
        #add 7e at beginning & end        if self.__special_header:            out_data  = self.__special_header        elif self.__empty_header or empty_header:            out_data  = ""        else:            out_data  = "\x7E"        out_data += data         out_data += "\x7E"                self.base.send(out_data)

    def handle_HDLC(self, buff):        HDLC_DELIM = '\x7E'        HDLC_ESC   = '\x7D'                HDLC_ESC_MASK = 0x20                data_out = ""        escape_next_byte = False                        for ch in buff:                        if ch == HDLC_ESC:                escape_next_byte = True                                continue
            if ch == HDLC_DELIM:                # start/end of frame                if len(data_out) == 0:                    continue                # remove CRC16                data_out = data_out[:-2]                                break
            if escape_next_byte:                ch = chr(ord(ch) ^ HDLC_ESC_MASK)                escape_next_byte = False
            data_out += ch        return data_out        def recv_all(self):        req_packet_size = 0x1000        buff = ""
        while (True):            recv_bytes = self.base.recv(req_packet_size)            buff += recv_bytes                        if (len(recv_bytes) == 0):                break                            return buff                                         def recv(self):        buff = self.recv_all()                       after = self.handle_HDLC(buff)                return after                             


class FramerQC_HDLC_Single_Side(FramerQC_HDLC):    """    This framer is an HDLC framer that sends HDLC framers but the recv side has no HDLC    """    name = "Framer_SEND_HDLC"        def __init__(self, base, escaping = True, special_header = "",                     crc_big_endian = False, crc_calculator = None, empty_header = False):        super(FramerQC_HDLC_Single_Side, self).__init__(base, escaping, special_header,                     crc_big_endian, crc_calculator, empty_header)                                    def recv(self, num_bytes = 1024):        return self.base.recv(num_bytes)               