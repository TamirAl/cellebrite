"""
     Families
    This module contains the concrete families definitions,
    Family definition is a combination of Chain and Connection
"""


from Mits.Families.BaseFamily               import BaseFamilyUSB
from Mits.Chains.ChainQualcomm              import ChainQualcomm
from Mits.Connections.ConnectionUSBProbing import USBProbing


class LgDload0x30(BaseFamilyUSB):
    def __init__(self):
		self.name = "LgDload0x30"
		VID = [0x1004]
		PID = [0x6238, 0x61f1] #0x61f1
		CONFIGURATION = 0x1
		INTERFACE = 0x1
		OUT = 0x2
		IN = 0x3
		BaseFamilyUSB.__init__(self, "LgDload0x30", ChainQualcomm, VID, PID, \
                               configuration = CONFIGURATION, interface=INTERFACE, 
                               write_endpoint = OUT, read_endpoint=IN, to_open_connection=True, 
                               busy_waiting=True, probing_mode = [USBProbing.vendor_no_probing, USBProbing.com_data_no_probing])
