"""
Written By: Nir Zaltsman
from IDumper import IDumper
class DumperQCLGInternal(IDumper):
    NAND = 1

    def internal_init(self):        
        if self.flash_type == self.NAND:

    def dump(self, flash_type, start = 0, end = 0):
        if end == 0:
        self.open_output('', "QC_LG_inr", start, end)
