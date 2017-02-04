from Mits.Families.Qualcomm.LgDload0x30 import *
from Mits.Clients.Client_LG_30 import *
from Mits.Families.Qualcomm.DLoadMode import *
from Mits.Utils.upy import upy




"""
the backdoor located in Download Mode, to enter Download Mode :
     shut down the device
    remove the battery, any power supply
    insert the battery
    connect to USB and imidiatly press ( and keep pressing ) Volume UP and Volume DOWN until "DOWNLOAD MODE" text will appear.


  For VS870 and phones alike its a must to pull off the battery and the usb cable before starting to dump
  Otherwise the dump will cause unexpected errors and will make the device crash randomly


"""


upy.ui_async_operation("Connecting", "Please wait")
f = LgDload0x30()


c = Client_LG_30(f)


c.dump()




print "Finished."
