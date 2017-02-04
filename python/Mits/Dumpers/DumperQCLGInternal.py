"""LG Qualcomm internal protocol nand Dumper
Written By: Nir Zaltsman4/10/2010"""
from IDumper import IDumperfrom Mits.Utils.General import timed_xrangefrom Mits.Utils.upy import upy
class DumperQCLGInternal(IDumper):    name = "QCLGInternal"
    NAND = 1    EMMC = 2    def check_flash_type(self, flash_type):        if not flash_type:            raise "flash type was not provided"        t = flash_type.lower()        if t == "nand":            return self.NAND        if t == "emmc":            return self.EMMC        raise "unknown flash type:%s" % flash_type

    def internal_init(self):                self.protocol.internal_init()        self.emmc_blocks_per_read = self.protocol.protocol_config.emmc_blocks_per_read                         self.block_size  = self.protocol.max_block_size_info        self.page_size   = self.protocol.max_page_size_info        self.block_count = self.protocol.max_block_cnt_info        
        if self.flash_type == self.NAND:            self.step = 1            self.bytes_per_read = 1            self.read_func = self.protocol.internal_read        elif self.flash_type == self.EMMC:            self.step = self.emmc_blocks_per_read            self.bytes_per_read = self.block_size * self.emmc_blocks_per_read            self.read_func = self.protocol.internal_emmc_read            

    def dump(self, flash_type, start = 0, end = 0):        """        flash_type - "nand" or "emmc"        start, end - page number (NAND) or block number (EMMC)        """        self.flash_type = self.check_flash_type(flash_type)        self.internal_init()
        if end == 0:            if self.flash_type == self.NAND:                end = self.block_size * self.block_count            elif self.flash_type == self.EMMC:                end = self.block_count
        self.open_output('', "QC_LG_inr", start, end)        try:            for read_this in timed_xrange(start, end, self.step, bytes_per_iteration=self.bytes_per_read/self.step):                data = self.read_func(read_this)                self.write_to_output(data)                while self.protocol.has_additional_internal_info() :                    data = self.read_func(None)                    self.write_to_output(data)                            except KeyboardInterrupt:            print "Dump Canceled by User!"        finally:            upy.target_add_desc_set("ExtractionMethod", "ANDROID_ADB", "Image")            self.close_output()

