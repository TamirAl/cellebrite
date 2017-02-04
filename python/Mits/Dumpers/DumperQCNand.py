"""
QCNand Dumper


Written By: NirZ
14/10/10
"""


from IDumper import IDumper
from Mits.Utils.General import timed_xrange, get_dump_path
from Mits.Utils.NandCsv import NandCsv


class DumperQCNand(IDumper):
    name = "QCNand"


    def dump(self, chipset_type, base_address, start = 0, end = 0, name = "", step = 1, whichflash=0):
        """
        chipset_type: 0-7200, 1-6010, 2-6550
        """


        #get flash id from phone
        maker_id, vendor_id = self.protocol.nand_probe(chipset_type, base_address)
        #find flash data in table and print
        nand_csv = NandCsv()
        nand_data = nand_csv.get_data(maker_id, vendor_id)


        for i in nand_data.keys():
            print "%012s:"%(i),nand_data[i]


        if end == 0:
            end = nand_data["BlockCount"] * nand_data["BlockSize"]


        #init the flash
        self.protocol.nand_init(chipset_type, base_address,\
                nand_data["PageSize"], nand_data["SpareSize"], nand_data["BlockSize"], nand_data["BlockCount"], nand_data["Width"], \
                whichflash)


        #and dump it
        self.open_output(name, "QCNand", start, end)


        total_page_size = nand_data["PageSize"]+nand_data["SpareSize"]
        try:
            for page in timed_xrange (start, end, step):
                data = self.protocol.nand_read(page)[:total_page_size]
                if ('\xff\xff\xff\xff' == data):
                    data = "\xFF" * (total_page_size)
                if (len(data) <> total_page_size):
                    raise Exception ("Received invalid page length on page %d" % page)
                self.write_to_output(data)
        except KeyboardInterrupt:
            print "Dump Canceled by User!"
        finally:
            self.close_output()
