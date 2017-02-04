from Mits.Families.BaseFamily               import BaseFamilySerial, BaseFamilyUSB


from Mits.Chains.ChainBcmUploadMode         import ChainBcmUploadMode
from BcmUploadModeConsts  import MODELS
import serial


class FamilyBcmSerial(BaseFamilySerial):        
    def __init__(self, port = None):
        BaseFamilySerial.__init__(self, "Broadcomm Serial", ChainBcmUploadMode, port, baud = 115200, parity = serial.PARITY_NONE)


class FamilyBcmUploadMode(BaseFamilyUSB):
    def __init__(self, phone_model):


        vid = [0x04e8]
        pid = [0x684E, 0x685d, 0x6795]


        # Models start with GT-S5xxx or GT-S7xxx, the write_endpoint is 2
        if (phone_model is MODELS.S7XXX) or (phone_model is MODELS.S5XXX):
            custom_write_endpoint = 2
        # Models start with GT-S8xxx, the write_endpoint is 3
        elif (phone_model is MODELS.S8XXX):
            custom_write_endpoint = 3
        else:
            raise Exception("Trying to create family for unknown model!")
        BaseFamilyUSB.__init__(self, "Broadcomm USB Upload Mode", ChainBcmUploadMode, vid, pid, configuration=1, interface=1, write_endpoint=custom_write_endpoint, read_endpoint=2)
