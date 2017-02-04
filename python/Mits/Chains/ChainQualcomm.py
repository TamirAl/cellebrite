"""
    Chains
    Concrete implementations for families Chains
    Each chain may contain framers, protocols, uploaders and dumpers
"""
from Mits.Chains.BaseChain import BaseChain
# FRAMERS
from Mits.Framers.FramerQC_HDLC                 import FramerQC_HDLC, FramerQC_HDLC_Single_Side
from Mits.Framers.FramerQCExploit               import FramerQCExploit
from Mits.Framers.FramerRETeam                  import FramerRETeam


# PROTOCOLS
from Mits.Protocols.ProtocolQualcommDownload    import ProtocolQualcommDownload
from Mits.Protocols.ProtocolQualcommDownload    import ProtocolLgDload0x30
from Mits.Protocols.ProtocolQualcommDiag        import ProtocolQualcommDiag
from Mits.Protocols.ProtocolQCExploit           import ProtocolQCExploit


# UPLOADERS
from Mits.Uploaders.UploaderQCDownload          import UploaderQCDownload


# DUMPERS
from Mits.Dumpers.DumperQCRam                   import DumperQCRamDiag, DumperQCRamDownload
from Mits.Dumpers.DumperRam                     import DumperRam
from Mits.Dumpers.DumperQCInternalNand          import DumperQCInternalNand
from Mits.Dumpers.DumperQCNand                  import DumperQCNand
from Mits.Dumpers.DumperOneNand                 import DumperOneNand
from Mits.Dumpers.DumperQCLGInternal            import DumperQCLGInternal
from Mits.Dumpers.DumperLgDload0x30             import DumperLgDload0x30


class ChainQualcomm(BaseChain):
    def __init__(self, conn, name = "Qualcomm", command_const = 1):
        BaseChain.__init__(self, name, conn)
        self.framers[FramerQC_HDLC.name]                    = FramerQC_HDLC(self.conn, escaping = True)
        self.framers[FramerQCExploit.name]                  = FramerQCExploit(self.framers[FramerQC_HDLC.name], command_const)
        self.framers[FramerQC_HDLC_Single_Side.name]        = FramerQC_HDLC_Single_Side(self.conn, escaping = True)

        # overwrite default framer
        self.framers[FramerRETeam.name]                     = FramerRETeam(self.framers[FramerQCExploit.name])
        
        self.protocols[ProtocolQualcommDownload.name]       = ProtocolQualcommDownload(self.framers[FramerQC_HDLC.name])
        self.protocols[ProtocolQualcommDiag.name]           = ProtocolQualcommDiag(self.framers[FramerQC_HDLC.name])
        self.protocols[ProtocolQCExploit.name]              = ProtocolQCExploit(self.framers[FramerRETeam.name])
        self.protocols[ProtocolLgDload0x30.name]            = ProtocolLgDload0x30(self.framers[FramerQC_HDLC_Single_Side.name])


        self.dumpers[DumperQCRamDiag.name]                  = DumperQCRamDiag(self.protocols[ProtocolQualcommDiag.name])
        self.dumpers[DumperQCRamDownload.name]              = DumperQCRamDownload(self.protocols[ProtocolQualcommDownload.name])
        self.dumpers[DumperRam.name]                        = DumperRam(self.protocols[ProtocolQCExploit.name])
        self.dumpers[DumperLgDload0x30.name]                = DumperLgDload0x30(self.protocols[ProtocolLgDload0x30.name])
        self.dumpers[DumperQCInternalNand.name]             = DumperQCInternalNand(self.protocols[ProtocolQCExploit.name])
        self.dumpers[DumperQCLGInternal.name]               = DumperQCLGInternal(self.protocols[ProtocolQualcommDownload.name])        
        self.dumpers[DumperQCNand.name]                     = DumperQCNand(self.protocols[ProtocolQCExploit.name])
        self.dumpers[DumperOneNand.name]                    = DumperOneNand(self.protocols[ProtocolQCExploit.name])


        self.uploaders[UploaderQCDownload.name]             = UploaderQCDownload(self.protocols[ProtocolQualcommDownload.name])
