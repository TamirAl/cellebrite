"""
    Base Family
    Definition of family object, which includes a chain and a connection.
    The constructor acts as a copy-c'tor while it copy the chain members
    into Family local namespace.
    Each family contains:
        Name, Connection, Bootloader_Path, Bootloader_Addr,
        and a Chain (framers, protocols, dumpers, and uploaders)


    Written by NirZ
    12/08/10
"""


import serial
import Mits.Configuration.Config as MitsConfig


from Mits.Connections.ConnectionUSB    import ConnectionUSB
from Mits.Connections.ConnectionSerial import ConnectionSerial
from Mits.Connections.ConnectionSocket import ConnectionSocket


from Mits.Framers.IFramer import IFramer
from Mits.Protocols.ProtocolRETeam import ProtocolRETeam


class BaseFamily(object):
    def __init__(self, name, chain):
        self.__name          = name
        self.__chain         = chain(self.conn)


        self.bootloader_path = None
        self.bootloader_addr = 0


        self.framers     = self.__chain.framers
        self.protocols   = self.__chain.protocols
        self.dumpers     = self.__chain.dumpers
        self.uploaders   = self.__chain.uploaders






    def __repr__(self):
        txt = "Family: " + self.__name + " (%s)" % repr(self.conn) + "\r\n"


        if (None <> self.bootloader_path):
            txt += "Bootloader Path = %s\r\n" % self.bootloader_path
            txt += "Bootloader Addr = %X\r\n" % self.bootloader_addr


        txt += repr(self.__chain)


        return txt


    def close(self):
        self.conn.close()


    def connect(self, busy_waiting = False):
        self.conn.connect(busy_waiting)


    def reconnect(self, max_wait = 120):
        self.conn.reconnect(max_wait)




"""
    BaseFamilyUSB
"""
class BaseFamilyUSB(BaseFamily):
    def __init__(self, name, chain,  vid, pid, configuration = 1, interface = 2, 
                 write_endpoint=2, read_endpoint=2, timeout = 0.3,to_open_connection=True, 
                 busy_waiting=False, probing_mode = None):
        self.connection_type = "Usb"
        self.conn= ConnectionUSB(vid, pid, configuration, interface, write_endpoint, 
                                 read_endpoint, timeout, to_open_connection,busy_waiting, probing_mode)
        BaseFamily.__init__(self, name, chain)


    def connect(self, busy_waiting = False):
        self.conn.connect(busy_waiting)


"""
    BaseFamilySerial
"""
class BaseFamilySerial(BaseFamily):
    def __init__(self, name, chain, port = None, baud=115200, parity=serial.PARITY_NONE, timeout=5,to_open_connection=True):
        self.connection_type = "Serial"
        self.conn = ConnectionSerial(port, baud, parity, timeout,to_open_connection)
        BaseFamily.__init__(self, name, chain)






"""
    BaseFamilySocket
"""
class BaseFamilySocket(BaseFamily):
    def __init__(self, name, chain, ip, port, timeout=5,to_open_connection=True):
        self.connection_type = "Socket"
        self.conn = ConnectionSocket(ip, port, timeout,to_open_connection)
        BaseFamily.__init__(self, name, chain)




"""
    BaseFamilyUSB
"""
class BaseFamilyUSBoSerial(BaseFamily):
    """
    This class is a connection serial over USB, it should be used when the Mits connection is working with
    the device's driver (COM) and the UFED works with raw connection which is USB
    """
    def __init__(self, name, chain,  to_open_connection=True, timeout=0.3, usb_busy_waiting=False, usb_probing_mode = None, com_port = None, com_baud = 115200, com_parity=serial.PARITY_NONE):
        self.connection_type = "UsboSerial"
        if MitsConfig.IS_UFED :
            self.conn= ConnectionUSB(0, 0, 1, 2, 2, 2, timeout, to_open_connection,usb_busy_waiting, usb_probing_mode)
        else :
            self.conn = ConnectionSerial(com_port, com_baud, com_parity, timeout, to_open_connection)
        BaseFamily.__init__(self, name, chain)


    def connect(self, busy_waiting = False):
        self.conn.connect(busy_waiting)
