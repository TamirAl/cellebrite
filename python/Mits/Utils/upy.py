import Mits.Configuration.Config as MitsConfig
if MitsConfig.IS_UFED :    from upy_UFED import *    upy = UfedUpyelse :    from Iupy import *    upy = Iupy