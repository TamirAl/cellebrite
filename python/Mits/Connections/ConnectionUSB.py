import Mits.Configuration.Config as MitsConfig


if MitsConfig.IS_UFED == True :
    from ConnectionUSB_UFED import *
else :
    from ConnectionUSB_Mits import *

