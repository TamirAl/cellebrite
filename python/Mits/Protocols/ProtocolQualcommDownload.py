"""

import struct
from ProtocolQualcommDownloadDecompressor import DecompressLGQC
class Config_QC_V0(object):
    @staticmethod

class Config_QC_V1(object):

class Config_QC_V2(Config_QC_V0):

class ProtocolQualcommDownload(object):
    HIGH_PERM_CODE = 'd|f|++-+'
        CMD_SELECT_OFFSET           = 0x21
        
    def __init__(self, framer):

    def __recv_replay(self, response):
        code = ord(received_response[0])
        if ((code <> self.Commands.CMD_NAK) and (code <> response)):
            reason = struct.unpack(">H", received_response[1:3])[0]
       
    def send_firmware_stuff_cmd(self, cmd, ret = 1, tx=''):


    def has_additional_internal_info(self) :

    def identify_configuration(self):    
    def set_config(self, config):
        request format:

        is_compressed, comp_data = self.protocol_config.parse_data(data)        

    def dload_switch(self):

    def ping(self):

    def parse_debug(self, debug):
    

    def read(self, addr, length):
    def write_addr24bit(self, addr,data):
    def write(self, addr, data):

    def go(self, addr):
    

    def reset(self):

    def get_implementation(self):
    def get_version(self):
    def get_model(self):

    def send_init_cmd(self):
        print "header_len: ", len(data)    
    # PACKET_ORDER = [CMD_PRE_FIRMWARE_UPGRADE,
    #                ]
    def start_qcsbl_cfg(self):
    def start_qcsbl(self):
    def send_oemsbl_hd(self, oemsbl_data):
    def send_partition_table(self, partition_data):
    def do_firmware_stuff(self, oemsbl_data):
    def send_chunk(self, offset, data):
    def send_big_chunk_header(self, offset, size):
    def finish_section(self):

    




class ProtocolLgDload0x30(object):

    def read_mem(self, block_num, blocks, expected_bytes):