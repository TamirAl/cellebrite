import Mits.Configuration.Config as MitsConfig


from Mits.Utils.upy import upy
from Mits.Utils.General import get_dump_path, get_dump_file_name




class IDumperBase(object):
    """this is an interface for dumpers. for example a OneNand Dumper"""
    def __init__(self, protocol):
        self.protocol = protocol


    def dump(self):
        raise Exception(NotImplemented)


    def open_output(self, prefix, middle, start=None, end=None, baseAddr=None) :
        pass


    def write_to_output(self, data, offset = None) :
        pass


    def close_output(self) :
        pass




class IDumperMitsBase(IDumperBase):


    def open_output(self, prefix, middle, start=None, end=None, baseAddr=None) :
        self.output_file = file(get_dump_path(prefix, middle, start, end, baseAddr), "wb")


    def write_to_output(self, data, offset = None) :
        self.output_file.write(data)


    def close_output(self) :
        self.output_file.close()


class IDumperUFEDBase(IDumperBase):


    def __init__(self, protocol):
        super(IDumperUFEDBase, self).__init__(protocol)




    def open_output(self, prefix, middle, start=None, end=None, baseAddr=None) :
        self.cur_offset = 0
        self.fn = get_dump_file_name(prefix, middle, start, end, baseAddr)


    def write_to_output(self, data, offset = None) :
        _offset = offset 
        if offset == None :
            _offset = self.cur_offset        
        upy.target_write_chunk(data, _offset, self.fn)
        self.cur_offset += len(data)


    def close_output(self) :
        upy.target_finalize_write(self.fn)




if MitsConfig.IS_UFED :
    IDumper = IDumperUFEDBase
else :
    IDumper = IDumperMitsBase
