"""
this protocol uses the FramerRETeam to talk with our bootloader.


Written By: Nadav Horesh
9/8/2010
"""


#this is for the change_baudrate_function
from serial import PARITY_NONE


import hashlib
import time
import struct
from Mits.Utils.General import pack32L, unpack32L, unpack16L
from Mits.Utils.General import gen_response


class ProtocolRETeam(object):
    name = "RETeam"


    class Commands:
        INIT_BTL        = "INTB"
        CHANGE_BAUD     = "BAUD"
        INIT_ONE_NAND   = "INIT"    # this commands is used to init the samsung nand or the onenand.
                                     # different bootloaders will do with this different things
                                     # i know it sucks, but it's to late to change it now.
        INIT_MMC        = "MMCI"   
        READ_MMC        = "MMCR"                             


        PROB_NAND       = "PRBN"   
        INIT_NAND       = "INTN"           
        
        TEST            = "TEST"
        DEBUG_PRINT     = "DBGP"
        BRANCH          = "JUMP"
        ONENAND_READ    = "ONND"
        NAND_READ       = "NAND"
        RESET_TIMER     = "TIME"
        RAM_READ        = "READ"
        PING            = "PING"
        WRITE_RAM       = "SAVE" # used in preloader
        DONE            = "DONE"
        INIT_EXTMEM     = "IEXM" # returns external memory size
        INVALIDATE_CACHE = "INVD"
        RPC             = "RPC!"
        AUTH            = "CONF"
        REPLAY          = "rply"
        SCANMEM         = "SCAN"


        
        # K9F1G NAND.
        KAFIG_INIT = "K9FI"
        KAFIG_INFO = "K9FN"
        KAFIG_READ = "K9FR"
        


    def __init__(self, framer, safe_recv = False):
        self.framer = framer
        self.safe_recv = safe_recv
        
    def __recv_replay(self):
        head, rx = self.framer.recv()
        if (head != self.Commands.REPLAY):
            raise Exception("ProtocolRETeamBootloader: got invalid head: "+repr(head))
        return rx
        
    def __send_command(self, cmd, tx='', sleep = 0, max_retry_count = 10):
        """ send a command and recv a reply"""
        count = 0
        recv = ''
        self.framer.send(cmd, tx)
        if (self.safe_recv):
            sleep = 0.03
            
        time.sleep(sleep)
        if (self.safe_recv):
            while (count < max_retry_count):
                try:
                    recv = self.__recv_replay()
                    break
                except Exception, e:
                    if ("Invalid Command" in repr(e)):
                        print repr(e)
                        return
                    print "RETeam Protocol Error Occured, retrying...",
                    print repr(e)
                    #self.framer.flush()
                    count += 1
                    raise
        else:
            recv = self.__recv_replay()
            
        return recv


    def init_bootloader(self, param_vector):
        print "Initializing bootloader using these values: ", map(hex, param_vector)
        init_data = self.__send_command(self.Commands.INIT_BTL, "".join([pack32L(x) for x in param_vector]))
        
    def authenticate(self):
        """
        send 32 bit value, get back challenge.
        send response, get back some value if it's the correct response
        """
        time.sleep(1) # give the bootloader time to unpack
        self.framer.raw_send("CLBR")
        challange = struct.unpack("I",self.framer.raw_recv(4))[0]
        print "Authenticate, Received: : " + struct.pack(">I",challange).encode('hex')
        resp = gen_response(challange)
        self.framer.raw_send(struct.pack("I",resp))
        time.sleep(1) #give the bootloader time to calculate the response 
        result = self.framer.raw_recv(4)
        return result
        
        
    def change_baudrate(self, baud = 921600, par = PARITY_NONE, reconnect = False, delay = 0, test = True, use_enum = True):
        if (use_enum) :
            if baud == 921600:
                send = 1
            elif baud == 460800:
                send = 2
            elif baud == 230400:
                send = 4
            elif baud == 115200:
                send = 8
            elif baud == 57600:
                send = 16
            else:
                raise Exception("ProtocolRETeamBootloader: unknown baudrate")
        else :
            send = baud
            
        self.framer.send(self.Commands.CHANGE_BAUD, pack32L(send))
        
        time.sleep(delay)
        if reconnect:
            self.framer.close()
            self.framer.connect()
        
        self.framer.set_baudrate(baud)
        self.framer.set_parity(par)        
        if (test):
            time.sleep(0.1)
            self.framer.recv_no_wait()
                
            #If the changing fails, then ping with raise an exception
            try:
                self.ping("TEST", False)
            except Exception, e:
                raise Exception("Change Baudrate: " + repr(e))


                
    def init_onenand(self, addr, ahb_addr = 0x20000000):
        """
        get the address of the nand, and send an INIT command.
        display the result values and returns (number of blocks, pages in block)
        """
        #send command and parse replay
        init_data = self.__send_command(self.Commands.INIT_ONE_NAND, pack32L(addr)+pack32L(ahb_addr))
        init_data_a = struct.unpack("<" + "I" * 16, init_data)
        
        #print replay
        print "  number of blocks:", init_data_a[0]
        print "  pages in block  :", init_data_a[1]
        print "  page size (b)   :", init_data_a[2]
        print "  manufacturer ID :", init_data_a[3]
        print "  device id       :", init_data_a[4]
        print "  size (mb)       :", init_data_a[5]
        print "  VCC 0-1.8 1-2.65:", init_data_a[6]
        print "  muxing (1-demux):", init_data_a[7]
        print "  cores (0-single):", init_data_a[8]
        print "  boot type       :", init_data_a[9]
        print "  Version ID      :", init_data_a[10]
        print "  data buffer size:", init_data_a[11]
        print "  boot buffer size:", init_data_a[12]
        print "  data buf number :", init_data_a[13]
        print "  boot buf number :", init_data_a[14]
        print "  tech 0-slc 1-mlc:", init_data_a[15]
        pages_in_block, number_of_blocks = init_data_a[1], init_data_a[0]
        page_size = init_data_a[2]
        
        self.__onenand_page_size = init_data_a[2]
        return (number_of_blocks, pages_in_block, page_size) # return number of blocks




    def mmc_init(self, version = 0):
        data = self.__send_command(self.Commands.INIT_MMC, pack32L(version))
        product_name = data[6:6+6][::-1]
        block_count  = unpack32L(data[16:16+4])
        block_size   = unpack32L(data[20:24])
        card_mid     = unpack16L(data[14:16])
        print "Product Name: ", product_name
        print "Manufacturer Id: 0x%X" % card_mid
        print "Block Count: 0x%X" % block_count
        print "Block Size : 0x%X" % block_size
        print "Capacity:  : %d(MB)" % ((block_count * block_size) / (1024*1024))
        return block_count, block_size


    def mmc_read(self, block_start, block_count,ram_address):
        result = (self.__send_command(self.Commands.READ_MMC, pack32L(block_start)+pack32L(block_count)+pack32L(ram_address)))
        return struct.unpack("<l", result)[0]




    def nand_init(self, page_size, spare_size, block_size, block_count, width):
        return unpack32L(self.__send_command(self.Commands.INIT_NAND, pack32L(page_size)+pack32L(spare_size) + \
                                             pack32L(block_size) + pack32L(block_count) + pack32L(width) ))
    
    def extmem_init(self):
        extmem_entry_fmt = "<III"
        extmem_entry_size = struct.calcsize(extmem_entry_fmt)
        reply = self.__send_command(self.Commands.INIT_EXTMEM, "")
        count, data = unpack32L(reply[:4]), reply[4:]
        memory = []
        if (count * extmem_entry_size != len(data)):
            raise Exception("Malformed IEXM packet.")
            
        for i in range(count):
            memory.append(struct.unpack(extmem_entry_fmt,
                                        data[i:i+extmem_entry_size]))
        return memory
        
    def nand_probe(self, version, chip_select = 0):
        nand_id =self.__send_command(self.Commands.PROB_NAND, pack32L(version)+pack32L(chip_select))
        maker_id  = ord(nand_id[0])
        device_id = ord(nand_id[1])
        return maker_id, device_id
            
    def dump_onenand_page(self, page, block):
        """
        dump a page in a spesific block
        """
        tx = pack32L(block) + pack32L(page) + pack32L(1)
        return self.__send_command(self.Commands.ONENAND_READ, tx)[:self.__onenand_page_size]
    
    def init_samsung_nand(self, addr):
        """
        init samsung nands
        """
        self.__send_command(self.Commands.INIT_ONE_NAND, pack32L(addr))
    
    def nand_read(self, addr, multi_page = False, multi_page_init = False, use_dma = True):
        """
        return a single page
        """
        return self.__send_command(self.Commands.NAND_READ, pack32L(addr) + pack32L(int(multi_page)) + pack32L(int(use_dma)))
        
    def kafig_init(self, nandAddress):
        self.__send_command(self.Commands.KAFIG_INIT, pack32L(nandAddress))
        infoData = self.__send_command(self.Commands.KAFIG_INFO)
        
        chipName, pageSize, blockSize, numBlocks, extraPageSize, wordSize = struct.unpack("16s5L", infoData)
        if chipName[0] == "\0":
            raise Exception("Unsupported K9F1G NAND chip")
            
        numPagesInBlock = blockSize / pageSize
        
        chipName = chipName.replace("\0","")
        print "Kafig NAND chip: '%s'" % chipName
        print "\tPage Size: %d" % pageSize
        print "\tBlock Size: %d" % blockSize
        print "\tExtra Page Bytes: %d" % extraPageSize
        print "\tWord Size: %d" % wordSize
        print "\tNum Blocks: %d" % numBlocks
        print "Total Size: %dMbit" % ((pageSize + extraPageSize) * numPagesInBlock * numBlocks / 1024 / 1024 * 8)
        
        self.__kafigPagesInBlock = numPagesInBlock
        return chipName, pageSize, blockSize, numBlocks, extraPageSize, wordSize        
                
    def kafig_read(self, pageNum):
        blockNum = pageNum / self.__kafigPagesInBlock
        pageNum = pageNum % self.__kafigPagesInBlock
        return self.__send_command(self.Commands.KAFIG_READ, pack32L(blockNum) + pack32L(pageNum))
        
    def dump_ram(self, addr, size):
        """
        dump a section of ram
        """
        tx = pack32L(size) + pack32L(addr)
        return self.__send_command(self.Commands.RAM_READ, tx)[:size]
        
    def reset_timer(self):
        """
        send a string to phone and verify that you receive the same string back
        """
        ret = self.__send_command(self.Commands.RESET_TIMER, "")
        return ret




    def invalidate_cache(self):
        """
        invalidate cache
        """
        ret = self.__send_command(self.Commands.INVALIDATE_CACHE, "pasten")   




    def rpc(self,address,arg0=0,arg1=0,arg2=0,arg3=0,arg4=0):
        """
        invalidate cache
        """
        data = "".join([pack32L(i) for i in [address,arg0,arg1,arg2,arg3,arg4]])
        ret = self.__send_command(self.Commands.RPC, data)




    def ping(self, string,shouldPrint=True):
        """
        send a string to phone and verify that you receive the same string back
        """
        ret = self.__send_command(self.Commands.PING, string)
        if shouldPrint:
            if string != ret:
                print "raw: ", ret.encode("hex")
                if len(ret)==4:
                    print "bitfield: "
                    for i in xrange(32):
                        print i, " : ", not(2**i & unpack32L(ret) == 0)
                    print "ping returned\n%s\ninsted of\n%s"%(hex(unpack32L(ret)),string)
                    return string
            else:
                print "ping successfull"
        return ret


    def debug_print(self):
        """
        print the debug log
        """
        
        log = self.__send_command(self.Commands.DEBUG_PRINT)
        print log
        
    def branch(self, addr, params = []):
        """Branch to a given address."""
        return self.__send_command(self.Commands.BRANCH, pack32L(addr)+"".join(map(pack32L, params)))
    
    def test(self, number, param2=0, param3=0):
        """
        send 4 bytes to test method of bootloader
        """
        
        return self.__send_command(self.Commands.TEST, pack32L(number)+pack32L(param2)+pack32L(param3))


    def test_params(self, param_list):
        return self.__send_command(self.Commands.TEST, "".join(map(pack32L, param_list)))
        
    def test_str(self, txt):
        return self.__send_command(self.Commands.TEST, txt)


    def write_ram(self, address, data, max_retry_count = 10):
        """
        write a bootloader chunk to a spesific address
        """
        tx = pack32L(address) + pack32L(len(data)) + data
        return self.__send_command(self.Commands.WRITE_RAM, tx, max_retry_count = max_retry_count)
    
    def write_ram_wrap(self, address, data, max_chunk_size):
        """
        write a bootloader chunk to a spesific address
        """
        i = 0
        last_trans = False
        while True :
            offset = i * max_chunk_size
            length = len(data) - offset            
            if max_chunk_size < length :
                length = max_chunk_size
            else :
                last_trans = True


            res = self.write_ram(address + offset, data[offset:offset+length])
#            print hex(address + offset), length
            i += 1
            if last_trans :
                return res


    def finish(self):
        """
        sends the done command that resets the phone 
        """
        self.__send_command(self.Commands.DONE)
        
        
    # Unified Ram Reading interface
    def read_ram(self, addr, size):
        return self.dump_ram(addr, size)
        
    def auth(self):
        hash_res = hashlib.md5("This is a Cellebrite Proprietary Program").digest()
        to_send = ''.join(pack32L(ord(c)) for c in hash_res[:4]) + hash_res[4:8]
        return self.__send_command(self.Commands.AUTH, to_send)


    def scan_mem(self, start=0, end=0x100000000, step=0x10000):
        """
        Sends the ScanMem command, with size 0, only to check validity of memory parts.
        """
        ranges = []
        cur = 0
        rangeStart = 0
        
        buf = self.__send_command(self.Commands.SCANMEM, pack32L(start) + pack32L(end-1) + pack32L(0) + pack32L(step))
        buf += "\x00" # If the last block is valid, this will make the code work.
        
        for i, v in enumerate(buf):
             v = ord(v)
             if cur == 0:
                if v == 0:
                    continue
                rangeStart = start + i * step
             else: # 1
                if v == 1:
                    continue
                ranges.append((rangeStart, start + i * step))
             cur = v
        return ranges
        
    def make_mem_map(self):
        ranges = self.scan_mem()
        print "Device Memory Map"
        print "-----------------"
        for start, end in ranges:
            print "0x%.8x - 0x%.8x" % (start, end)
        return ranges
        
    def read_mem_chunks(self, start=0, end=0x100000000, step=0x1000, chunkSize=4):
        """
        Sends the ScanMem command in order to read the chunks.
        """        
        assert chunkSize > 0
        
        buf = self.__send_command(self.Commands.SCANMEM, pack32L(start) + pack32L(end-1) + pack32L(chunkSize) + pack32L(step))
        chunks = []
        numSteps = len(buf) / (chunkSize + 1)
        for i in range(numSteps):
            tmpChunk = buf[i * (chunkSize + 1):(i + 1) * (chunkSize + 1)]
            if tmpChunk[0] == '\0':
                continue
            chunks.append((start + i * step,tmpChunk[1:]))
        
        return chunks
