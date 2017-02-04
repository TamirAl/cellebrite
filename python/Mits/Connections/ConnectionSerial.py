import Mits.Configuration.Config as MitsConfig


if MitsConfig.IS_UFED == True :
    from ConnectionSerial_UFED import *
else :
    from ConnectionSerial_Mits import *

