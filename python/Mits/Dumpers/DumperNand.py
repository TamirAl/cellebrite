"""
Generic Nand Dumper


Written By: NirZ
14/10/10
"""




from IDumper import IDumper
from Mits.Utils.General import timed_xrange, get_dump_path
from Mits.Utils.NandCsv import NandCsv


class DumperNand(IDumper):
    name = "Nand"


    def dump(self, chipset_version, start = 0, end = 0, name = "", whichflash=0, consequence_size = 1, dma_transfer = True):
        """
        """
        #get flash id from phone
        maker_id, device_id = self.protocol.nand_probe(chipset_version, whichflash)
        if (0 == maker_id) and (0 == device_id):
            raise Exception("Nand Not Found!")


        #find flash data in table and print
        print "Maker Id: \t%X" % maker_id
        print "Device Id: \t%X" % device_id


        nand_csv = NandCsv()
        nand_data = nand_csv.get_data(maker_id, device_id)


        for i in nand_data.keys():
            print "%012s:"%(i),nand_data[i]


        if end == 0:
            end = nand_data["BlockCount"] * nand_data["BlockSize"]


        #init the flash
        self.protocol.nand_init(nand_data["PageSize"], nand_data["SpareSize"], nand_data["BlockSize"], nand_data["BlockCount"], nand_data["Width"])


        #and dump it
        self.open_output(name, "Nand", start, end)


        total_page_size = nand_data["PageSize"]+nand_data["SpareSize"]
        single_read_size = total_page_size*consequence_size
        try:
            for addr in timed_xrange (start, end * total_page_size, single_read_size):
                page = addr / total_page_size
                data = self.protocol.nand_read(page, multi_page=consequence_size, use_dma = dma_transfer)[:single_read_size]
                if ('\xff\xff\xff\xff' == data):
                    data = "\xFF" * (single_read_size)
                if (len(data) <> single_read_size):
                    raise Exception ("Received invalid page length on page %d got %d expected %d" % (page, len(data), single_read_size))
                self.write_to_output(data)
        except KeyboardInterrupt:
            print "Dump Canceled by User!"
        finally:
            self.close_output()
