from Mits.Families.Samsung.BcmUploadModeConsts import MODELS 
from Mits.Clients.ClientBcmUploadMode import ClientBcmUploadMode


c = ClientBcmUploadMode()


try :
    c.into_upload_mode(phone_already_booted=False)


    c.dump(MODELS.S8XXX)


    c.restore_debug_level_and_finalize()


except :
    pass
finally :
    c.close()
