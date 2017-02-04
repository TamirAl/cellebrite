"""
Qualcomm internal driver nand Dumper


Written By: Nadav Horesh
4/10/2010
"""


from IDumper import IDumper
from Mits.Utils.General import timed_xrange, get_dump_path


class DumperQCInternalNand(IDumper):
    name = "QCInternal"
    # profiles:
    # block_count	block_size	page_size	total_page_size
    PROFILES = [[0x2000, None,   None,   None], #0
                [0x4000, 0x40,  0x200,  0x210], #1
                [0x2000, 0x40,  0x200,  0x210], #2
                [0x1000, 0x40,  0x800,  0x840], #3
                [0x1000, 0x40,  0x200,  0x210], #4
               ]


    def dump(self,start = 0, end = 0, search_start = 0, search_end = 0, step = 1, name = "", profile = None, version = 1):
        """
        start, end - page number
        search_start, search_end - where to look for the init function.
        """


        data = self.protocol.internal_nand_init(search_start,search_end, version)
        device_name     = data[1]
        device_maker_id = data[0][0]
        device_id       = data[0][1]
        block_count     = data[0][2]
        block_size      = data[0][3]
        page_size       = data[0][4]
        total_page_size = data[0][5]
        device_type     = data[0][6]


        if profile != None:
            print " Override:"
            if (self.PROFILES[profile][0] != None):
                block_count = self.PROFILES[profile][0]
                print "  Override block_count:", hex(block_count)
            if (self.PROFILES[profile][1] != None):
                block_size = self.PROFILES[profile][1]
                print "  Override block_size:", hex(block_size)
            if (self.PROFILES[profile][2] != None):
                page_size = self.PROFILES[profile][2]
                print "  Override page_size:", hex(page_size)
            if (self.PROFILES[profile][3] != None):
                total_page_size = self.PROFILES[profile][3]
                print "  Override total_page_size:", hex(total_page_size)


            self.protocol.internal_nand_update(page_size, total_page_size)
            print "  New size: %d MB"%(page_size*block_size*block_count)




        if end == 0:
            end = block_size * block_count


        self.open_output(name, "QC Internal Driver Nand", start, end)
        try:
            for page in timed_xrange(start, end, step):
                self.write_to_output(self.protocol.internal_nand_read(page)[:total_page_size])
        except KeyboardInterrupt:
            print "Dump Canceled by User!"
        finally:
            self.close_output()
