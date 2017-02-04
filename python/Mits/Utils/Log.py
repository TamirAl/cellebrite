
import time
from Mits.Utils.BinUtils    import hex_printfrom Mits.Utils.General     import get_log_path
class log:    """    make a log file    """    def __init__(self, name1, name2="mits log"):    	self.logname=get_log_path(name1, name2)
        self.__f = open(self.logname,"wb")        self.__start_time = time.time()
        self.__f.write("Log Started at: %s\r\n\r\n"%(time.ctime()))
    def __write(self, text, buffer, prefix):        s = "%3.6f - %s:"%( time.time()-self.__start_time, prefix)        if text != "":            s += "\r\n" + text        if buffer != "":            s += "\r\n" + hex_print(buffer)        s+= "\r\n\r\n"        self.__f.write(s)

    def text(self, text, prefix="DEBUG"):        self.__write(text, "", prefix)
    def buffer(self, buffer, prefix="DEBUG"):        self.__write("", buffer, prefix)
    def text_buffer(self, text, buffer, prefix="DEBUG"):        self.__write(text, buffer, prefix)
    def close(self):        self.__f.close()