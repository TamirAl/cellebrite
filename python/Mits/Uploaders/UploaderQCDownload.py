# uploader for Qualcomm DownloadMode 
#
# Written By: NirZ
# 10/8/2010


from IUploader import IUploader
import struct


class UploaderQCDownload(IUploader):
    name = "Download"      
    def handshake(self):
        self.protocol.dload_switch()
        
    def upload(self, bootloader_path, load_address,watchdog_address,  chunk_size=0x200):
        bootloader = file(bootloader_path, "rb").read()
        bootloader = bootloader[:4*1]  + struct.pack("<I", load_address)*6+ bootloader[4*7:]
        bootloader = bootloader[:0x2C] + struct.pack("<I", watchdog_address) + bootloader[0x2C+4:]


        
        current_addr = load_address
        
        for i in xrange(0, len(bootloader), chunk_size):
            #if not at the end
            if i < (len(bootloader) - chunk_size):
                sent_chunk = bootloader[i:i + chunk_size]
            #at the end, smaller chunk
            else:
                sent_chunk = bootloader[i:]
            #send chunk
            self.protocol.write(current_addr, sent_chunk)
            
            current_addr += chunk_size
            
        self.protocol.go(load_address)
        
    def upload_firmware(self, partition_path, qcsbl_cfg_path, qcsbl_path, oemsbl_path):
        partition = file(partition_path, 'rb').read()
        qcsbl_cfg = file(qcsbl_cfg_path, 'rb').read()
        qcsbl = file(qcsbl_path, 'rb').read()
        # oemsbl_cfg = file(oemsbl_cfg_path, 'rb').read()
        oemsbl = file(oemsbl_path, 'rb').read()


        self.protocol.start_firmware_update()
        self.protocol.send_partition_table(partition)
        self.protocol.do_firmware_stuff(oemsbl)
        
        self.protocol.start_qcsbl_cfg()
        self.upload_file(qcsbl_cfg)


        self.protocol.start_qcsbl()
        self.upload_file(qcsbl)


        self.protocol.send_oemsbl_hd(oemsbl)
        self.upload_file(oemsbl)


        self.protocol.shut()




    def upload_file(self, file_data):
        for i in xrange(0, len(file_data), 0x4000):
            self.upload_chunk(i, file_data[i:i+0x4000])
        self.protocol.finish_section()


    def upload_chunk(self, offset, data):
        for i in xrange(0, len(data), 0x800):
            self.protocol.send_chunk(i, data[i:i+0x800])
        self.protocol.send_big_chunk_header(offset, len(data))
