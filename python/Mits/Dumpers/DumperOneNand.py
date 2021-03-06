"""
OneNand Dumper


Written By: Nadav Horesh
9/8/2010
"""


from IDumper import IDumper
from Mits.Utils.General import timed_xrange, get_dump_path


class DumperOneNand(IDumper):
    name = "OneNand"


    def dump(self, address, start=0, end=0, step=1, name=""):
        """
        onanand mapped address, firt block to dump,last block to dump,
        pages to jump(for faster but partial dump), name to add to dump filename
        """
        number_of_blocks, pages_in_block, page_size = self.protocol.init_onenand(address)
        block_size = pages_in_block * page_size
        if end == 0:
            end = number_of_blocks


        self.open_output(name, "OneNand", address + start, address + end)


        try:
            page = 0
            for block in timed_xrange(start, end, bytes_per_iteration = block_size):
                while page < pages_in_block:
                    self.write_to_output(self.protocol.dump_onenand_page(page, block))
                    page += step
                page -= pages_in_block
        except KeyboardInterrupt:
            print "User cancelled the dump"
            self.protocol.framer.flush()
            return
        finally:
            self.close_output()
