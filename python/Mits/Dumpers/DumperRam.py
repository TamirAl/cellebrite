"""
Ram Dumper


Written By: Nadav Horesh
9/8/2010
"""


from IDumper import IDumper
from Mits.Utils.General import timed_xrange, get_dump_path


class DumperRam(IDumper):
    name = "Ram"
    def __init__(self, protocol, block_size = 0x1000):
        self.protocol   = protocol
        self.block_size = block_size


    def dump(self, start_address , end_address, block_size=None, step=1, name=""):
        """
        Dump ram or other memory mapped data (NOR)
        """
        if (None == block_size ):
            block_size = self.block_size


        self.open_output(name, "RAM", start_address, end_address)
        err_loop = 0
        try:
            for block_addr in timed_xrange(start_address, end_address, block_size * step):
                while (True):
                    try:
                        self.write_to_output(self.protocol.dump_ram(block_addr, block_size))


                        err_loop = 0
                        break
                    except KeyboardInterrupt, e:
                        raise e
                    except Exception, e:
                        err_loop += 1
                        print "Error occured: %d" % err_loop
                        if (err_loop > 10):
                            raise e




        except KeyboardInterrupt:
            print "User cancelled the dump"
            self.protocol.framer.flush()
            return


        finally:
            self.close_output()
