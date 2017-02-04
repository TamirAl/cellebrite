"""     the backdoor located in Download Mode, to enter Download Mode :    shut down the device    remove the battery, any power supply    insert the battery    connect to USB and imidiatly press ( and keep pressing ) Volume UP and Volume DOWN until "DOWNLOAD MODE" text will appear.
  For VS870 and phones alike its a must to pull off the battery and the usb cable before starting to dump  Otherwise the dump will cause unexpected errors and will make the device crash randomly
"""
class Client_LG_30(object):    def __init__(self, family):        self.family = family        self.protocol = family.protocols["ProtocolLgDload0x30"]        self.dumper = family.dumpers["DumperLgDload0x30"]
    def getPartitions(self):        return self.protocol.getPartitions()
    def dump(self):                NUMBER_OF_BLOCKS = 8        BYTES_PER_BLOCK = 0x200        storage_size = int(self.getPartitions())        self.dumper.dump(0, 0x200000 * int(storage_size), NUMBER_OF_BLOCKS,                          BYTES_PER_BLOCK * NUMBER_OF_BLOCKS)
