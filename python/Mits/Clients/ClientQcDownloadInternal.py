from time import sleep
from Mits.Utils.upy import upy


class ClientQcDownloadInternal(object):


    def __init__(self, family):
        self.f = family




    def reconnect(self, autowait):
        if autowait:
            print "Trying to reconnect"
            self.f.reconnect(120)
        else:
            self.f.close()
            upy.ui_msg_continue("Press continue/enter when device is in download mode...")
            self.f.connect()




    def switch_to_dload_mode(self):
        print "Switching to download mode"
        self.f.protocols["Diag"].dload_mode()




    def enter_dload_mode(self, auto_wait_4_reconnect=False):
        self.switch_to_dload_mode()
        print "Device will reboot, waiting 10 sec."
        sleep(10)
        self.reconnect(auto_wait_4_reconnect)




    def is_in_dload_mode(self):
        try:
            self.f.protocols["Download"].ping()
        except:
            return False
        return True




    def dump(self, start_from=0):
        if not self.is_in_dload_mode():
            raise RuntimeError("Dump canceled - the phone is not in dload mode!")            
        self.f.dumpers["QCLGInternal"].dump(self.f.flash_type, start_from)
