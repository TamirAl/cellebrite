import struct
from Mits.Framers.IFramer   import IFramerfrom Mits.Utils.General     import pack16B, pack16L, unpack16Lfrom Mits.Utils.Crc         import Crc16
class FramerTFS(IFramer):    """    sends and recives data in the tfs protocol.    """    name = "TFS"
    def __init__(self, base):        IFramer.__init__(self, base)        self.crc = Crc16()

    def send(self, data):        # 42 is always there in the tfs        # the +2 is for the crc        data = pack16L(len(data)+2)+ "\x42" + data + pack16B(self.crc.calc(data))        data = "\x7f" + data + "\x7e"        self.base.send(data)

    def recv(self, length=0):        if length == 0:            data = self.base.recv(4)            length = unpack16L(data[1:3])            data += self.base.recv(length+1)        else:            data = self.base.recv(length)        return self.__parse(data)
    def __parse(self, data):        if data[0] != "\x7F":            raise Exception("no TFS packet header!")        length = unpack16L(data[1:3])        if (data[3] != "\x42"):            raise Exception("TFS received invalid response! (No 42)")        return data [4:4+length]