from Mits.Families.Samsung.BcmUploadMode        import FamilyBcmSerial, FamilyBcmUploadMode
from Mits.Families.Samsung.BcmUploadModeConsts  import DEBUG_LEVELS, BOOT_COMPLETE
from Crypto.Hash.SHA import SHA1Hash
from Mits.Utils.upy import upy
import time


PASSWORD_EXCEPTION = "Password is!@#$%^"
PASSWORD_END_FLAG = "!@#$%^"
PASSWORD_PATTERN = "fjskwidnwk19cnwie8h#keoslwjak%fkq]dlwor&dkeic}si)djwidlgpru12dlwodlsp}20sjeigywowi20dpfl#1ps0wprlxm\x00"
INST = "Please connect the turned off device to cable 130, and wait for device to initialize"


class ClientBcmUploadMode(object):


    def __init__(self):
        self.initialized = False
        self.serial_family  = None


    def connect(self):
        self.serial_family = FamilyBcmSerial()
    
    
    @staticmethod 
    def replace(password):
        arr = list(PASSWORD_PATTERN)
        for i in xrange(len(password)):
            arr[5*i] = password[i]
        return "".join(arr)


    # Password's length must be between 4 to 8.
    # There is no checking for the length due to
    # performance issue when guessing the password
    @staticmethod 
    def calc_hash(password):
        
        PASSWORD_PATTERN = ClientBcmUploadMode.replace(password)
        return SHA1Hash(PASSWORD_PATTERN).digest()


    @staticmethod 
    def extract_encrypted__password(data):
        start = 0000
        end = 99999999


        data_hash = data.decode("base64")
        print "Trying to find the hash %s" % (repr(data_hash))


        i = start
        try:
            while (i < end):
                if data_hash == ClientBcmUploadMode.calc_hash("%d"%i):
                    return "%d"%i
                i += 1
        except Exception as e:
            print "Got exception (i = %d)" %i
            raise e


        raise Exception("Couldn't find the password...")


        # Examples:
        # 1111     -> extract_encrypted__password('JbgEiIkmElXsBq2v3E1KTJ35q5Q=')
        # 1337     -> extract_encrypted__password('fpoiLERB+xLe2VkIi6o267ByruY=')
        # 13371337 -> extract_encrypted__password('oX1/+80cL6ks4cWU1fxqP5M+xNU=')
    def read_password(self, phone_already_booted = False):
        # TODO : Create msg in the future too allow remove 
        removeLock = False
        upy.ui_async_operation("Waiting for device...", INST)
        if not phone_already_booted:
            print "waiting for boot"
            self.serial_family.protocols['BcmUploadMode'].wait_for(BOOT_COMPLETE)
        password = ""
        if removeLock:
            upy.ui_async_operation("Please wait", "Removing password...")
            
            self.remove_password()
            password = "Removed successfully"
        else:
            upy.ui_read_password_message()
            password = str(self.serial_family.protocols['BcmUploadMode'].read_passlock())
            if password and (not (password.isdigit() and len(password) > 3 and len(password) < 9)):
                print "extracting encrypted password"
                upy.ui_async_operation("Please Wait...", "Decrypting password, this may take a few minutes...")
                password = str(ClientBcmUploadMode.extract_encrypted__password(password))
        # close must be called before saving the password and exit
        self.close()
        upy.save_password_and_exit(password)
        return password








    
    #Remember - after removing the password it cannot be recovered
    def remove_password(self):
        self.serial_family.protocols['BcmUploadMode'].remove_passlock()


    def into_upload_mode(self, phone_already_booted = False):
        print "Connect the turned-off device into the serial port"
        self.connect()
        
        upy.ui_async_operation("Waiting for device...", INST)
        
        if not phone_already_booted:
            print "waiting for boot"
            self.serial_family.protocols['BcmUploadMode'].wait_for(BOOT_COMPLETE)


        upy.ui_async_operation("Please wait", "Initializing...")
            
        time.sleep(1)
        
        if self.serial_family.protocols['BcmUploadMode'].change_debug_level(DEBUG_LEVELS.High):
            print "Waiting for the phone to complete the boot"
            self.serial_family.protocols['BcmUploadMode'].wait_for(BOOT_COMPLETE)
            print "Booting completed! Entering Upload Mode..."
        
        time.sleep(1)
        self.serial_family.protocols['BcmUploadMode'].jump_null()


        print "Please press the middle button on the device (Enter) and wait until UPLOAD mode is initiated"
        upy.ui_msg_continue("1. Please press the middle button on the device (Enter).\n2. Press continue once UPLOAD Mode is initiated.", "Enter UPLOAD Mode")
 
        self.serial_family.protocols['BcmUploadMode'].close_serial()
    
    def dump(self, phone_model):
    
        print "Connect the phone with usb cable (100) and press enter"
        upy.ui_msg_continue("Please disconnect the phone and reconnect it using cable 100 and press continue", "Cable Change")
            
        upy.ui_async_operation("Connecting", "Connecting")
        self.usb_family = FamilyBcmUploadMode(phone_model)
        
        start_address = self.usb_family.protocols['BcmUploadMode'].get_dump_start_address()
        print "Dump starting at = 0x%.8x"%(start_address)
        
        time.sleep(2)
        dump_size = self.usb_family.protocols['BcmUploadMode'].get_dump_size()
        print "Dump size = 0x%x"%(dump_size)
        
#        upy.ui_create_progress_bar("Memory dump", dump_size)
        
        end_address = start_address + dump_size
        
        self.usb_family.dumpers['BcmUploadMode'].dump(start_address, end_address)
        
        # We don't need to restart the device because we are asking the user to remove the battery anyway..
        try:
            self.usb_family.protocols['BcmUploadMode'].restart_device()
        except Exception as e:
            print "Exception ignored when trying to restart the device (%s)" % (str(e))


        self.usb_family.close()


    def restore_debug_level_and_finalize(self):        


        upy.ui_msg_continue("To finalize the dump safely, please follow the following instructions: \n1. Disconnect the phone\n2. Remove the BATTERY\n3. Insert the BATTERY\n4. Connect cable A with black tip T-130 to the computer (the phone SHOULD NOT be connected yet)\n5. Press continue", "Finalize Extraction")
        
        self.connect()
        
        upy.ui_async_operation("Waiting for device...", INST)
        
        self.serial_family.protocols['BcmUploadMode'].wait_for(BOOT_COMPLETE)
        
        upy.ui_async_operation("Please wait", "Finalizing extraction...")
        
        self.serial_family.protocols['BcmUploadMode'].change_debug_level(DEBUG_LEVELS.Low)


        self.serial_family.protocols['BcmUploadMode'].close_serial()


        #upy.target_finalize_write()


    def close(self):
        if self.serial_family  is not None :
            self.serial_family.close()
        self.serial_family  = None
