"""This framer is used for talking with our bootloaders.it's based on the samsung Agere Framer
Written by: Nadav Horesh9/8/2010"""
import struct
from IFramer        import IFramerfrom Mits.Utils.Crc import Crc32from Mits.Utils.General import *
class FramerRETeam(IFramer):    name = "RETeam"
    class Results:        ERROR   = "-err"        OK      = "+ok+"        OK_COM  = "-ok0"        REPLAY  = "rply"
    def __init__(self, framer):        self.base = framer        self.eom_magic = "EOT." # the magic that we send and the end of the packet
    def set_oem_magic(self, magic):        "set the 4 byte end of packet magic"        self.eom_magic = magic

    def send(self, cmd, data=''):##    PC->Phone:##            4 bytes Command       this is 4 ascii letters like "info" or "SUCK"##            4 bytes Data len  the length of the data in little endian##            X bytes Payload     the data itself (present only if length > 0)##            4 bytes Data Crc    regular crc32 on the data (present only if length > 0)##            4 bytes Magic       an "end of packet" 4 ascii letters magics like "(pc)" or "EOT."        crc = Crc32()
        buf = cmd        buf += struct.pack("I",len(data))
        if data:            buf += data            buf += struct.pack("I",crc.calc(data))
        buf += self.eom_magic
        self.base.send(buf)

    def recv(self):##    Phone->PC:##            4 bytes Magic       4 ascii letter magic like "resp" or "rply"##            4 bytes Command     this is 4 ascii letters like "info" or "SUCK"##            4 bytes Result      4 ascii letter magic like "-err" or "+ok+"##            4 bytes Data Len    the length of the data in little endian##            X bytes Payload     the data itself (present only if length > 0)##            4 bytes Data Crc    regular crc32 on the data (present only if length > 0)##            4 bytes Magic       an "end of packet" 4 ascii letters magics like "(hw)" or "EOT."        data_read = 0        data = ""        head= ""        compress = False
        #read header        times = 0        while(head == ""):            head  = self.base.recv(4)            if times > 10:                raise Exception("FramerRETeam: got only empty head!")            times += 1
        if head != self.Results.REPLAY:            raise Exception ("FramerRETeam: invalid head %s"%(repr(head)))
        cmd  = self.base.recv(4)           #read command        res  = self.base.recv(4)           #read result        length  = struct.unpack("I",self.base.recv(4))[0]     #read len
        if (self.Results.OK_COM == res):            compress = True
        # read all data        while (data_read < length):            tmp = self.base.recv(length - data_read)            if len(tmp) == 0:                raise Exception("FramerRETeam: didnt get all the data in Recv")            data_read += len(tmp)            data += tmp
        if (compress):            if (len(data) != 5):                raise Exception("FramerRETeam: Invalid compression data recvd")
            data_len = unpack32L(data[:4])            data = data[4]*data_len
        if (length != 0):            crc  = self.base.recv(4)       #read crc
        i = 0        end = self.base.recv(4)           #read end        while end == "":            end = self.base.recv(4)           #read end            i += 1            if (i > 5):                break        if (end != "eom."):            raise Exception("FramerRETeam: invalid tail %r %r %x"%(repr(end), repr(crc), len(data)))
        if ((res != self.Results.OK) and (res != self.Results.OK_COM)):            word = 0            if len(data) > 4:                word = struct.unpack("<I",data[:4])[0]            raise Exception("%s recv error: %r %r %d 0x%x"%(cmd, head,data, word, word))
        return(head, data)