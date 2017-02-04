from Mits.Chains.BaseChain import BaseChain
# For the SpreadTrum HDLC Framer
#from Crc         import Crc16A
# FRAMERS
from Mits.Framers.IFramer                   import IFramer
from Mits.Framers.FramerTFS                 import FramerTFS
from Mits.Framers.FramerSamsungBada         import FramerSamsungBada

# PROTOCOLS
from Mits.Protocols.ProtocolBcmUploadMode   import ProtocolBcmUploadMode

# DUMPERS
from Mits.Dumpers.DumperBcmUploadMode       import DumperBcmUploadMode

class ChainBcmUploadMode(BaseChain):
    def __init__(self, conn):
        BaseChain.__init__(self, "BcmUploadMode", conn)        
        self.framers[IFramer.name]                          = IFramer(self.conn)
        self.framers[FramerTFS.name]                        = FramerTFS(self.conn)
        self.framers[FramerSamsungBada.name]                = FramerSamsungBada(self.framers[FramerTFS.name])
        
        self.protocols[ProtocolBcmUploadMode.name]          = ProtocolBcmUploadMode(serial_framer = self.framers[FramerSamsungBada.name],
                                                                                    usb_framer    = self.framers[IFramer.name],
                                                                                    base_framer   = self.framers[IFramer.name])       
        self.dumpers[DumperBcmUploadMode.name]              = DumperBcmUploadMode(self.protocols[ProtocolBcmUploadMode.name])


