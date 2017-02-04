from Mits.Families.Samsung.BcmUploadModeConsts import COMMANDS, BOOT_COMPLETE, BOOT_TIMEOUT


from Mits.Utils.General import unpack32L
from Mits.Utils.upy import upy


import time






class ProtocolBcmUploadMode:
    name = "BcmUploadMode"
    
    def __init__(self, serial_framer, usb_framer, base_framer):
        self.serial_framer  = serial_framer
        self.usb_framer     = usb_framer
        self.base_framer    = base_framer


    # ***************************************************
    # This is the stage responsible for getting the phone
    # into upload mode, also can remove the password
    # ***************************************************


    def send_tfs_command(self, command):
        self.serial_framer.flush()
        self.serial_framer.send(command)
        if "ACK" != self.serial_framer.recv():
            self.close_serial()
            raise Exception("Haven't got ACK in the respone")
        return self.serial_framer.recv()
        


    def decrypt_passlock(self, passlock):
        # Here we need to find out if the passlock is encrypted (or just plaintext), and decrypt it if necessary
        return passlock


    def read_passlock(self):
        
        response = self.send_tfs_command("NvGetStr NV_SI_PHONELOCK_PASSWD")
        passlock = response[4:-1]


        passlock = self.decrypt_passlock(passlock)


        return passlock
        
    def remove_passlock(self):
        # Disabling the passlock in the device
        self.send_tfs_command("NvWriteInt NV_SI_ACCESSCONTROL_PASSWORD_FLAG 0")
        # Writing empty password
        # Pay attention that in some phones the passlock written as plain text,
        # and in others it's encrypted / hashed and base64-encoded
        password = ""
        self.send_tfs_command("NvWriteStr NV_SI_PHONELOCK_PASSWD " + password)
        


    # Waiting for a phrase coming from the device
    def wait_for(self, phrase, timeout = BOOT_TIMEOUT):
        buf = ""
        start_time = time.time()
        while (start_time + timeout > time.time()):
            buf += self.base_framer.recv(1)
            if buf.endswith(phrase) :
                return True
            
        self.close_serial()
        raise Exception("Timeout when waiting for %s, got so far %s" % (repr(phrase), repr(buf)))




    # flag should be True or False
    def change_debug_level(self, wanted_level):


        restart_needed = False
        
        print "Changing debug level...",
        response    = self.send_tfs_command("NvGetInt NV_SI_SYSTEM_DEBUG_STATE")
        state       = unpack32L(response[4:])
        if state != 1:
            self.send_tfs_command("NvWriteInt NV_SI_SYSTEM_DEBUG_STATE 1")
            restart_needed = True
            
        response      = self.send_tfs_command("NvGetInt NV_SI_SYSTEM_DEBUG_LEVEL")
        current_level = unpack32L(response[4:])
        if current_level != wanted_level:
            self.send_tfs_command("NvWriteInt NV_SI_SYSTEM_DEBUG_LEVEL %d"%(wanted_level))
            restart_needed = True


        print "Done!"
        if restart_needed:
            print "Restart needed, Restarting device.. Please wait (Keep it connected)"
            self.base_framer.send("AT+RESET\r\n")


        return restart_needed
        


    def jump_null(self):
        self.serial_framer.send("JumpNull")
        self.serial_framer.flush()
    
    def close_serial(self):
        self.serial_framer.close()


    
    # **************************************************
    # This is the stage responsible for the dump process
    # **************************************************


    def recv_command(self, command):
        response = self.usb_framer.recv(len(command + "\x00"))
        if response != command + "\x00":
            #self.usb_framer.close()
            raise Exception("Didn't receive command (%s), got %s instead!"%(repr(command), repr(response)))
     
    def send_data(self, data):
        self.usb_framer.send(data + "\x00")


    def send_upload_command(self, data):
        self.send_data(data)
        self.recv_command(COMMANDS.ACK)
     


    def before_read(self, start_address, end_address):
        self.send_upload_command(COMMANDS.START)
        self.send_upload_command(COMMANDS.START)
        self.send_upload_command(("0x%.8x"%start_address)[len("0x"):].upper()) #"01FFFFFC") #01EEEFFC
        self.send_upload_command(("0x%.8x"%end_address  )[len("0x"):].upper()) #"01FFFFFF") #01EEEFFF


        self.send_data(COMMANDS.GET_DATA)
    
    def after_read(self):


        finished_flag = False
        
        for i in range(10):
            try:
                self.after_read_simple()
                finished_flag = True
                break
            except Exception:
                time.sleep(1.5)
                self.usb_framer.recv(1024)
                
        if not finished_flag:
            print "After read failed"


    def after_read_simple(self):
        self.send_data(COMMANDS.ACK)
        self.recv_command(COMMANDS.END)
	  
    def get_addresses(self, start, end, size):


        self.before_read(start, end)
        
        response =  self.usb_framer.recv(size)


        self.usb_framer.flush()
        return response


    def get_dump_start_address(self):
        start_address = self.get_addresses(0x01FFFFFC, 0x01FFFFFF, 12)
        return unpack32L(start_address[8:])


    def get_dump_size(self):
        size_str = self.get_addresses(0x1EEEFFC, 0x1EEEFFF, 4)
        return unpack32L(size_str)


    def restart_device(self):
        self.before_read(0x3FFFFFC, 0x3FFFFFF)
    
    def dump_get_chunk(self, start_address, chunk_size, spare_size):
        
        data =  self.usb_framer.recv(chunk_size)
        if 0 == spare_size:
            time.sleep(1.5)
        self.send_data(COMMANDS.ACK)
        if spare_size:
            data += self.usb_framer.recv(spare_size)
            self.send_data(COMMANDS.ACK)   


        return data


    def abort_dump(self):
        self.usb_framer.flush()
