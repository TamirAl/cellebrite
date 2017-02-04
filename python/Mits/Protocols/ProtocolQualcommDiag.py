"""
    Qualcomm Diagnostic Protocol
    see 80-V1294-1_YP_DMSS_Serial_Data_ICD.pdf ("CDMA Dual-Mode Subscriber Station Serial Data Interface")


    Written by NirZ
"""




import struct
from Mits.Utils.General import pack16L, pack32L, unpack16L, unpack32L






class ProtocolQualcommDiag:
    name = "Diag"
    
    class Commands:        
            DIAG_VERNO_F			        = 0x00			       #  Version Number Request/Response      
            DIAG_ESN_F		                = 0x01				   #  Mobile Station ESN Request/Response        
            DIAG_PEEKB_F			        = 0x02			       #  Peek byte Request/Response                 
            DIAG_PEEKW_F			        = 0x03			       #  Peek word Request/Response                 
            DIAG_PEEKD_F			        = 0x04			       #  Peek dword Request/Response                
            DIAG_POKEB_F			        = 0x05			       #  Poke byte Request/Response                 
            DIAG_POKEW_F			        = 0x06			       #  Poke word Request/Response                 
            DIAG_POKED_F			        = 0x07			       #  Poke dword Request/Response                
            DIAG_OUTP_F			            = 0x08			       #  Byte output Request/Response               
            DIAG_OUTPW_F			        = 0x09			       #  Word output Request/Response               
            DIAG_INP_F			            = 0x0A			       #  Byte input Request/Response                
            DIAG_INPW_F			            = 0x0B			       #  Word input Request/Response                
            DIAG_STATUS_F			        = 0x0C			       #  DMSS status Request/Response               
            DIAG_LOGMASK_F			        = 0x0F			       #  Set logging mask Request/Response          
            DIAG_LOG_F			            = 0x10			       #  Log packet Request/Response                
            DIAG_NV_PEEK_F			        = 0x11			       #  Peek at NV memory Request/Response         
            DIAG_NV_POKE_F			        = 0x12			       #  Poke at NV memory Request/Response         
            DIAG_BAD_CMD_F			        = 0x13			       #  Invalid Command Response                   
            DIAG_BAD_PARM_F		            = 0x14				   #  Invalid parameter Response
            DIAG_BAD_LEN_F			        = 0x15			       #  Invalid packet length Response             
            DIAG_BAD_MODE_F		            = 0x18				   #  Packet not allowed in this mode 
            DIAG_TAGRAPH_F			        = 0x19			       #  info for TA power and voice graphs         
            DIAG_MARKOV_F			        = 0x1A			       #  Markov statistics                          
            DIAG_MARKOV_RESET_F		        = 0x1B				   #  Reset of Markov statistics                 
            DIAG_DIAG_VER_F			        = 0x1C			       #  Return diag version for comparison to
            DIAG_TS_F			            = 0x1D			       #  Return a timestamp                         
            DIAG_TA_PARM_F			        = 0x1E			       #  Set TA parameters                          
            DIAG_MSG_F			            = 0x1F			       #  Request for msg report                     
            DIAG_HS_KEY_F			        = 0x20			       #  Handset Emulation -- keypress              
            DIAG_HS_LOCK_F			        = 0x21			       #  Handset Emulation -- lock or unlock        
            DIAG_HS_SCREEN_F		        = 0x22				   #  Handset Emulation -- display request       
            DIAG_PARM_SET_F			        = 0x24			       #  Parameter Download                         
            DIAG_NV_READ_F			        = 0x26                 #  Read NV item                               
            DIAG_NV_WRITE_F			        = 0x27		 	       #  Write NV item                              
            DIAG_CONTROL_F			        = 0x29			       #  Mode change request                        
            DIAG_ERR_READ_F			        = 0x2A			       #  Error record retreival                     
            DIAG_ERR_CLEAR_F		        = 0x2B				   #  Error record clear                         
            DIAG_SER_RESET_F		        = 0x2C				   #  Symbol error rate counter reset            
            DIAG_SER_REPORT_F		        = 0x2D			 	   #  Symbol error rate counter report           
            DIAG_TEST_F			            = 0x2E			       #  Run a specified test                       
            DIAG_GET_DIPSW_F		        = 0x2F				   #  Retreive the current dip switch setting    
            DIAG_SET_DIPSW_F		        = 0x30				   #  Write new dip switch setting               
            DIAG_VOC_PCM_LB_F		        = 0x31				   #  Start/Stop Vocoder PCM loopback            
            DIAG_VOC_PKT_LB_F		        = 0x32				   #  Start/Stop Vocoder PKT loopback            
            DIAG_ORIG_F			            = 0x35			       #  Originate a call                           
            DIAG_END_F			            = 0x36			       #  End a call                                 
            DIAG_DLOAD_F			        = 0x3A			       #  Switch to downloader                       
            DIAG_TMOB_F			            = 0x3B			       #  Test Mode Commands and FTM commands        
            DIAG_FTM_CMD_F			        = 0x3B		 	       #  Test Mode Commands and FTM commands        
            DIAG_STATE_F			        = 0x3F			       #  Return the current state of the phone      
            DIAG_PILOT_SETS_F		        = 0x40				   #  Return all current sets of pilots          
            DIAG_SPC_F			            = 0x41			       #  Send the Service Prog. Code to allow SP    
            DIAG_BAD_SPC_MODE_F		        = 0x42				   #  Invalid nv_read/write because SP is locked 
            DIAG_PARM_GET0x02_F		        = 0x43				   #  get parms obsoletes PARM_GET               
            DIAG_SERIAL_CHG_F		        = 0x44				   #  Serial mode change Request/Response        
            DIAG_MTC_F			            = 0x45			       #  FEATURE_MT
            DIAG_PASSWORD_F		            = 0x46				   #  Send password to unlock secure operations  
            DIAG_BAD_SEC_MODE_F		        = 0x47				   #  An operation was attempted which required  
            DIAG_PR_LIST_WR_F		        = 0x48				   #  Write Preferred Roaming list to the phone. 
            DIAG_PR_LIST_RD_F		        = 0x49				   #  Read Preferred Roaming list from the phone.
            DIAG_SUBSYS_CMD_F		        = 0x4B				   #  Subssytem dispatcher (extended diag cmd)   
            DIAG_FEATURE_QUERY_F		    = 0x51				   #  Asks the phone what it supports            
            DIAG_SMS_READ_F		            = 0x53				   #  Read SMS message out of NV                 
            DIAG_SMS_WRITE_F		        = 0x54				   #  Write SMS message into NV                  
            DIAG_SUP_FER_F			        = 0x55			       #  info for Frame Error Rate          
            DIAG_SUP_WALSH_CODES_F		    = 0x56				   #  Supplemental channel walsh codes           
            DIAG_SET_MAX_SUP_CH_F		    = 0x57				   #  Sets the maximum # supplemental 
            DIAG_PARM_GET_IS0x5FB_F		    = 0x58				   #  get parms including SUPP and MUX0x02: 
            DIAG_FS_OP_F			        = 0x59			       #  Performs an Embedded File System
            DIAG_AKEY_VERIFY_F		        = 0x5A				   #  AKEY Verification.                         
            DIAG_BMP_HS_SCREEN_F		    = 0x5B				   #  Handset emulation - Bitmap screen          
            DIAG_CONFIG_COMM_F		        = 0x5C				   #  Configure communications                   
            DIAG_EXT_LOGMASK_F		        = 0x5D				   #  Extended logmask for > 0x20 bits.            
            DIAG_EVENT_REPORT_F		        = 0x60				   #  Static Event reporting.                    
            DIAG_STREAMING_CONFIG_F	        = 0x61				   #  Load balancing and more!                   
            DIAG_PARM_RETRIEVE_F		    = 0x62				   #  Parameter retrieval                        
            DIAG_STATUS_SNAPSHOT_F		    = 0x63				   #  A state/status snapshot of the DMSS.      
            DIAG_RPC_F			            = 0x64			       #  Used for RPC                               
            DIAG_GET_PROPERTY_F		        = 0x65				   #  Get_property requests                      
            DIAG_PUT_PROPERTY_F		        = 0x66				   #  Put_property requests                      
            DIAG_GET_GUID_F			        = 0x67			       #  Get_guid requests                          
            DIAG_USER_CMD_F		            = 0x68				   #  Invocation of user callbacks               
            DIAG_GET_PERM_PROPERTY_F	    = 0x69				   #  Get permanent properties                   
            DIAG_PUT_PERM_PROPERTY_F	    = 0x6A				   #  Put permanent properties                   
            DIAG_PERM_USER_CMD_F		    = 0x6B				   #  Permanent user callbacks                   
            DIAG_GPS_SESS_CTRL_F		    = 0x6C				   #  GPS Session Control                        
            DIAG_GPS_GRID_F			        = 0x6D			       #  GPS search grid                            
            DIAG_GPS_STATISTICS_F		    = 0x6E				   #  GPS Statistics                             
            DIAG_ROUTE_F			        = 0x6F			       #  Packet routing for multiple instances of diag 
            DIAG_IS0xC80x00_STATUS_F	    = 0x70				   #  IS0xC80x00 status                              
            DIAG_RLP_STAT_RESET_F		    = 0x71				   #  RLP statistics reset                       
            DIAG_TDSO_STAT_RESET_F		    = 0x72				   #  (S)TDSO statistics reset                   
            DIAG_LOG_CONFIG_F		        = 0x73				   #  Logging configuration packet               
            DIAG_TRACE_EVENT_REPORT_F	    = 0x74				   #  Static Trace Event reporting 
            DIAG_SBI_READ_F			        = 0x75			       #  SBI Read 
            DIAG_SBI_WRITE_F			    = 0x76			       #  SBI Write 
            DIAG_SSD_VERIFY_F		        = 0x77				   #  SSD Verify 
            DIAG_LOG_ON_DEMAND_F		    = 0x78				   #  Log on Request 
            DIAG_EXT_MSG_F			        = 0x79			       #  Request for extended msg report 
            DIAG_ONCRPC_F			        = 0x7A			       #  ONCRPC diag packet 
            DIAG_PROTOCOL_LOOPBACK_F	    = 0x7B				   #  Diagnostics protocol loopback. 
            DIAG_EXT_BUILD_ID_F		        = 0x7C				   #  Extended build ID text 
            DIAG_EXT_MSG_CONFIG_F		    = 0x7D				   #  Request for extended msg report 
            DIAG_EXT_MSG_TERSE_F		    = 0x7E				   #  Extended messages in terse format 
            DIAG_EXT_MSG_TERSE_XLATE_F	    = 0x7F				   #  Translate terse format message identifier 
            DIAG_SUBSYS_CMD_VER_0x02_F	    = 0x80				   #  Subssytem dispatcher Version 0x02 (delayed response capable) 
            DIAG_EVENT_MASK_GET_F		    = 0x81				   #  Get the event mask 
            DIAG_EVENT_MASK_SET_F		    = 0x82				   #  Set the event mask 
            DIAG_CHANGE_PORT_SETTINGS	    = 0x8C				   #  Command Code for Changing Port Settings. 


            responses = {DIAG_BAD_CMD_F      : "DIAG_BAD_CMD",   \
                     DIAG_BAD_PARM_F         : "DIAG_BAD_PARM",  \
                     DIAG_BAD_LEN_F          : "DIAG_BAD_LEN",   \
                     DIAG_BAD_MODE_F         : "DIAG_BAD_MODE",  \
                     DIAG_BAD_SEC_MODE_F     : "DIAG_BAD_SEC_MODE", \
                     DIAG_BAD_SPC_MODE_F     : "DIAG_BAD_SPC_MODE"}


    class FS_Operations:
        CREATE_DIRECTORY = 0
        REMOVE_DIRECTORY = 1
        DISPLAY_DIRECTORY_LIST = 2
        DISPLAY_FILE_LIST = 3
        READ_FILE = 4
        WRITE_FILE = 5
        REMOVE_FILE = 6
        GET_FILE_ATTRIBUTES = 7
        SET_FILE_ATTRIBUTES = 8
        ITERATIVE_DIRECTORY_LIST = 10
        ITERATIVE_FILE_LIST = 11
        SPACE_AVAILABLE = 12




    class FS_Item_Types:
        DIRECTORY = 0x0A
        FILE = 0x0B


    class FS_Status:
        OK = 0
        ACCESS_DENIED = 0x0D
        NO_MORE_ITEMS = 0x1C


    class ControlModes:
        DIAG_CONTROL_OFFLINE_A = 0
        DIAG_CONTROL_OFFLINE_D = 1
        DIAG_CONTROL_RESET     = 2
        DIAG_CONTROL_FTM       = 3
        DIAG_CONTROL_ONLINE    = 4
        DIAG_CONTROL_LOWPOWER  = 5


        
    def __init__(self, framer):
        self.framer = framer




    def __recv_replay(self, response):
        received_response = self.framer.recv()
            
        code = ord(received_response[0])


        if (code == response):
            return received_response[1:]
        else:
            if (self.Commands.responses.has_key(code)):
                reason = self.Commands.responses[code]
            else:
                reason = hex(code)
                
            raise Exception("ProtocolQualcommDiag, received error: " + reason)


       
    def __send_command(self, cmd, tx='', response=None, empty_header=False):
        """ send a command and recv a reply"""
        if (None == response):
            response = cmd
        self.framer.send(chr(cmd) + tx, empty_header=empty_header)
        return self.__recv_replay(response)


    def __next_seq(self, seq):
        if seq == 0xFF:
            return 0x01
        return seq+1


    def get_version(self):
        return self.__send_command(self.Commands.DIAG_VERNO_F)


    def get_chipset(self):
        return self.__send_command(self.Commands.DIAG_EXT_BUILD_ID_F)
        
    def send_password(self, sp="FFFFFFFFFFFFFFFF"):
        return self.__send_command(self.Commands.DIAG_PASSWORD_F, sp.decode('hex'))
    
    def send_spc(self, spc="000000"):
        return self.__send_command(self.Commands.DIAG_SPC_F, spc)
        
    def __peek(self, command, addr, codeword_count, codeword_size):
        return self.__send_command(command,                            
                            tx = pack32L(addr) + pack16L(codeword_count))[6:6+codeword_count * codeword_size]


    def __poke(self, command, addr, data, codeword_size, max_codeword_size):
        if ((len(data) % codeword_size) > 0) or (len(data) > max_codeword_size * codeword_size):
            raise Exception ("ProtocolQualcommDiag: __poke got invalid data length: " + repr(len(data)))


        padding = "\x00" * ( (max_codeword_size * codeword_size)  - (len(data)))


        return self.__send_command(command,
                            tx = pack32L(addr) + chr(len(data) / codeword_size ) + data + padding)


    def poke_byte(self, addr, data):
        DIAG_MAX_POKE_B = 4
        return self.__poke(self.Commands.DIAG_POKEB_F, addr, data, 1, DIAG_MAX_POKE_B)
    
    def poke_word(self, addr, data):
        DIAG_MAX_POKE_W = 2
        return self.__poke(self.Commands.DIAG_POKEW_F, addr, data, 2, DIAG_MAX_POKE_W)
    
    def poke_dword(self, addr, data):
        DIAG_MAX_POKE_D = 2
        return self.__poke(self.Commands.DIAG_POKED_F, addr, data, 4,  DIAG_MAX_POKE_D)




    
    def peek_byte(self, addr, count = 1):
        return self.__peek(self.Commands.DIAG_PEEKB_F, addr, count, 1)
    
    def peek_word(self, addr, count = 1):
        return self.__peek(self.Commands.DIAG_PEEKW_F, addr, count, 2)
    
    def peek_dword(self, addr, count = 1):
        return self.__peek(self.Commands.DIAG_PEEKD_F, addr, count, 4)


    def write(self, addr, buf):
        "poke it aligned buffer to address. align if necessary"


        last_byte_align = 8 * (len(buf) / 8)
        for i in xrange(0,last_byte_align,8):
            self.poke_dword(addr+i, buf[i:i+8])
            
        for i in xrange(last_byte_align, len(buf), 1 ):
            self.poke_byte(addr + i, buf[i])




    def read(self, addr, length):
        codeword_size = 4
        codeword_max  = 4
        max_bytes     = codeword_size * codeword_max
        data = ""
        last_byte_align = max_bytes * (length / max_bytes)
        for i in xrange(0,last_byte_align,max_bytes):
            data += self.peek_dword(addr+i, codeword_max)


        for i in xrange(last_byte_align, length, 1 ):
            data += self.peek_byte(addr + i)


        return data
        
    def get_peek_ranges(self, start = 0, end = 0x70000000, step = 0x10000):
        good = False
        for i in xrange(start, end,step):
            try:
                self.peek_dword(i)
                if good == False:
                    good = True
                    print "0x%08X -"%(i),
            except Exception, e:
                if "DIAG_BAD_PARM" in repr(e):
                    if good == True:
                        good = False
                        print "0x%08X"%(i) 
                else:
                    print "Error at 0x%08X"%(i) 
                    raise
            


    def get_nv_item(self, item):
        """
        read non volatile item 
        """
        return self.__send_command(self.Commands.DIAG_NV_READ_F, pack32L(item))


    def get_esn(self):
        """
        read NVM item number 0, and decode the ESN from there
        """
        return unpack32L(self.get_nv_item(0)[2:2+4])


    def get_nam_banner(self):
        try:
            data = self.get_nv_item(0x47)[2:]
            pos  = data.find("\x00")
        except Exception, e:
            return ""
        return data[:pos]


    def get_nam_name(self):
        try:            
            data = self.get_nv_item(0x2B)[3:]
            pos  = data.find("\x00")
        except Exception, e:
            return ""        
        return data[:pos]
    
    def dload_mode(self):
        """
        go to download mode (send 0x3a, try with and without 7E header)
        """
        try:
            self.__send_command(self.Commands.DIAG_DLOAD_F)
        except:
            self.__send_command(self.Commands.DIAG_DLOAD_F, empty_header=True)




    def get_first_filesystem_item_name(self, is_dirs = False, parent_dir = '/'):
        seq_number_to_indicate_start = 0
        return self.get_next_filesystem_item_name(seq_number_to_indicate_start, is_dirs, parent_dir)




    def get_next_filesystem_item_name(self, seq = 1, is_dirs = False, parent_dir = '/'):
        """
        iterate over files in a directory of the phone filesystem
        seq number 0 means first, any other means next (but maybe best to have a counter, just make sure it elapse to 1 rather than 0)
        send:0x59,cmd(0x0B=files/0x0A=dirs),seq[4],dir_name_len[1],sz_dir_name[len]
        get: 0x59,cmd(0x0B/0x0A),status[1],seq[4],attributes[4],creation_date[4],logical_size[4],physical_size[4],path_part_len[1],path_and_name_len[1],sz_name[path_and_name_len]
        if status 0 a valid name is returned
        status 0x0D means bad filename (probably a dir) so just ignore
        status 0x1C end of file list
        exception is raised by send_command() if listing a protected directory like ".efs_private" since device replies with 0x13 (DIAG_BAD_CMD)
        """
        nullTerm = '\x00'
        cmd = self.FS_Item_Types.FILE #files
        if is_dirs:
            cmd = self.FS_Item_Types.DIRECTORY #dirs
        cmd_params = chr(cmd) + pack32L(seq) + chr(len(parent_dir)+len(nullTerm)) + parent_dir + nullTerm
        return self.__send_command(self.Commands.DIAG_FS_OP_F, cmd_params)




    def list_filesystem_item_names(self, is_dirs = False, parent_dir = '/'):
        listNames = []
        try: #try to list items, if fail then return what we got so far
            recFile = self.get_first_filesystem_item_name(is_dirs, parent_dir)
            status = ord(recFile[1])
            seq = 1
            #while (status != self.FS_Status.NO_MORE_ITEMS):
            while ((status == self.FS_Status.OK) or (status == self.FS_Status.ACCESS_DENIED)):
                #print 'rec: ',recFile.encode('hex') #DEBUG
                if (status == self.FS_Status.OK):
                    name = recFile[24:]
                    listNames.append(name)
                    #print repr(recFile) #DEBUG
                #get next file name
                seq = self.__next_seq(seq)
                recFile = self.get_next_filesystem_item_name(seq, is_dirs, parent_dir)
                status = ord(recFile[1])
        except Exception:
            pass
        return listNames








    def read_filesystem_file(self, fname = ''):
        """
        read content of a file that resides on the phone filesystem
        send:0x59,0x04,seq[1],name_len[1],sz_name[len]
        get: 0x59,0x04,status[1],seq[1],isMore[1],file_size[4],data_len[2],data[len]
        if status 0 means OK
        status 0x0D means bad filename (probably a dir) so just ignore
        status 0x1C end of file list
        """
        nullTerm = '\x00'
        data = ''
        #read 1st block
        seq = 0
        resp = self.__send_command(self.Commands.DIAG_FS_OP_F, chr(self.FS_Operations.READ_FILE) + chr(seq) + chr(len(fname)+len(nullTerm)) + fname + nullTerm)
        status = ord(resp[1])
        if (status != self.FS_Status.OK):
            return None #error reading file
        file_length = unpack32L(resp[4:8])
        block_len = unpack16L(resp[8:10])
        data += resp[10:10+block_len]
        #read next blocks if needed
        isMore = (ord(resp[3]) != 0)
        while (isMore): #the MORE field is false, so no more data blocks
            seq = self.__next_seq(seq)
            resp = self.__send_command(self.Commands.DIAG_FS_OP_F, chr(self.FS_Operations.READ_FILE) + chr(seq))
            status = ord(resp[1])
            if (status != self.FS_Status.OK):
                break #error reading rest of the file (but we'll just quit the loop to return what data we got)
            isMore = (ord(resp[3]) != 0)
            block_len = unpack16L(resp[4:6])
            data += resp[6:6+block_len]
        #print 'file',fname,' was read data(',len(data),'): ',repr(data)
        return data[:file_length]






    def change_mode(self, mode):
        """
        change to offline mode. gets an enum ControlModes.
        """
        return self.__send_command(self.Commands.DIAG_CONTROL_F, pack16L(mode))


    def reset(self):
        return self.change_mode(self.ControlModes.DIAG_CONTROL_RESET)


    def offline(self):
        return self.change_mode(self.ControlModes.DIAG_CONTROL_OFFLINE_A)
    
    def online(self):
        return self.change_mode(self.ControlModes.DIAG_CONTROL_ONLINE)


    def get_model(self):
        ver_string = self.get_version()
        ver_string = ver_string[38:min(filter(lambda x: x <> -1, [ver_string.find(x, 38) for x in ["\x00", ":"]]))]
        return ver_string
    


    def ping(self):
        return self.get_version()


    def printscreen(self):
        return self.__send_command(self.Commands.DIAG_SUBSYS_CMD_F, struct.pack("<III",0x110, 0, 0xFFFFFFFF) + "\x00" + "Disp.bmp" + "\x00")
        
    # Unified Ram Reading interface
    def read_ram(self, addr, size):
        return self.read(addr,size)
