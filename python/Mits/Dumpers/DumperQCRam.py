"""Dump RAM with QC protocol
Written By: Nirz9/8/2010"""
from IDumper import IDumperfrom Mits.Utils.General import timed_xrange, get_dump_path
class DumperQCRam(IDumper):    def __dump(self, base_address , end_address = None, page_size = 0x800, step = 1, dumper_type = ""):        """        dump Qualcomm RAM        """
        if end_address == None:            end_address = base_address + 0x1000000
        name = self.protocol.get_model()        self.open_output(name, dumper_type, base_address, end_address)        try:            for page in timed_xrange(base_address, end_address, page_size * step):                self.write_to_output(self.protocol.read(page, page_size))        except KeyboardInterrupt:            print "User canceled the dump"        finally:            self.close_output()

class DumperQCRamDiag(DumperQCRam):    name = "DiagRam"    def dump(self, base_address , end_address = None, page_size = 0x800, step = 1, name = ""):        """        dump Qualcomm RAM in Diag Mode        """        self._DumperQCRam__dump(base_address, end_address, page_size, step, dumper_type = "QC_DIAG_RAM")

class DumperQCRamDownload(DumperQCRam):    name = "DownloadRam"    def dump(self, base_address , end_address = None, page_size = 0x800, step = 1, name = ""):        """        dump Qualcomm RAM in Download Mode        """        self._DumperQCRam__dump(base_address, end_address, page_size, step, dumper_type = "QC_DLOAD_RAM")