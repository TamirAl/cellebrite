"""
    The framer add CRC16 and escape data with "\x7E"


    Written by TamirM
"""




import time
from Mits.Framers.IFramer import IFramer
from Mits.Utils.General   import unpack16L, pack16L, pack16B


class FramerSamsungBada(IFramer):
    name = "SamsungBadaFramer"
                
    def __init__(self, base):
        self.base = base


    def send(self, command):
        command += "\x00"
        out_data = "\x00\x05" + pack16L(len(command)) + command
        
        self.base.send(out_data)


    def recv(self):
    
        response = self.base.recv()
        if response == "":
            raise Exception("Got empty response")
        elif response == "\x01":
            response = "ACK"
        else:
            if not response[:2] == "\x00\x05":
                raise Exception("No 00 05 were found, got %s instead"%repr(response[:2]))
            # Bytes 2: are the length of the inner response
            length = unpack16L(response[2:4])  
            # The inner response start from pos 2
            response = response[4: 4 + length]
        
        return response
